#!/usr/bin/env python3
"""
Shared library for AECN batch QA checklist build + audit.

Two entry points:

1. Build-time pre-flight validation
   `build_with_validation(rows, source_reads_path, out_path, build_workbook_fn,
                          derived_values=None)`
   - Optionally merges a dict of script-computed derived values into the
     `_derived_values` block of source_reads.json.
   - Walks every `[log:KEY]` in evidence cells, resolves each key against the
     source-read log, and verifies any quoted numerics match log values to the
     precision shown.
   - If any gaps exist, raises BuildAborted with the full list BEFORE the
     workbook is written. This catches bad citations at build time instead of
     after a 5-cycle audit + rebuild loop.

2. Post-build audit (used by `audit_checklist.py`)
   `audit_evidence(item, status, notes, log)` runs the same checks on an
   already-built xlsx row. The CLI wrapper in `audit_checklist.py` walks an
   xlsx and reports/rewrites failures.

Both share regex constants and resolution helpers so the rules can't drift
between build-time and audit-time.

Convention (FC10):
- Every Pass/Fail/Flag evidence note must contain at least one `[log:KEY]`
  citation tag pointing to a key in `batch_<id>_source_reads.json`.
- Quoted numerics following `=` must match a value reachable through one of
  the cited keys (or one nested inside a cited dict/list).
- Script-computed values (sums, allocations, recalcs) live in the
  `_derived_values` block of source_reads.json and are auto-emitted by
  build_with_validation when a per-batch build script passes them in via the
  `derived_values` argument.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

LOG_KEY_RE = re.compile(r"\[log:([^\]]+)\]")
# Match an explicit "= NUMBER" where the number is a complete numeric token
# (digits with optional commas and at most one decimal point), followed by a
# non-numeric/non-dash/non-slash boundary so we don't capture partial pieces
# like "2" from "2-184" or "4" from "4/2/2026".
QUOTED_VALUE_RE = re.compile(r"=\s*([\d,]+(?:\.\d+)?)(?![\d/.\-])")
BLOCKING_RE = re.compile(r"\b(blocking|blocked|needs[\s_]?max)\b", re.IGNORECASE)
ATTEMPT_RE = re.compile(r"\(\d\)\s*[^;]+;")

# Primary-source-open rule (feedback_primary_source_open_rule.md).
# Mode 1: confabulated negative. Phrases that assert absence trigger the
# negative-claim audit — the cited keys must include a _primary_source_opened
# entry for the location being claimed empty.
NEGATIVE_CLAIM_RE = re.compile(
    r"\b(is empty|are empty|empty in drive|empty subfolder|"
    r"is absent|are absent|absence of|not present in|not in |"
    r"no spill(s)? documented|no vaulted|no incident|no \w+ events?|"
    r"never (?:opened|read|verified)|did not (?:open|read|find))\b",
    re.IGNORECASE,
)
# Mode 2: SKILL-doc-as-proxy. Numeric-bearing nouns that demand a live-source
# citation rather than a SKILL doc citation. Flagged when no
# _primary_source_opened entry with a live_source_url is found among the cited
# keys.
SKILL_PROXY_TERMS = (
    "emission factor", "emissions factor", "kgco2e/kg", "kgco2e/mi",
    "kgco2e/(km", "kgco2e/(t", "mtco2e/", "carbon range", "carbon content range",
    "2-sd", "2sd", "± 72.57", "±72.57", "± 0.004", "±0.004",
)
SKILL_PROXY_RE = re.compile("|".join(re.escape(t) for t in SKILL_PROXY_TERMS), re.IGNORECASE)
SOURCE_OPENED_KEY = "_primary_source_opened"
LIVE_URL_KEY = "live_source_url"
ARTIFACT_PATH_KEY = "artifact_path"
NEGATIVE_CHECK_TOKENS_KEY = "negative_check_tokens"
SOURCE_OPENED_ACTIONS = (
    "image_read", "pdf_read", "modal_opened", "csv_exported", "sheet_grid_read"
)
# A "file row" in a Drive snapshot YAML / file listing typically carries one of
# these markers. If a negative claim says "folder empty" but the artifact
# contains any of these, the claim is unsupported and the audit fails the row.
FILE_PRESENCE_MARKERS = (
    ".pdf", ".docx", ".xlsx", ".xls", ".csv", ".jpg", ".jpeg", ".png",
    ".gif", ".heic", ".tif", ".tiff", ".eml", ".msg", ".zip", ".gz",
    " Owned by ", " Modified ", " Size: ", "Shared\"",
)

CHECKLIST_STATUSES = ("Pass", "Fail", "Flag")
NON_ROW_KINDS = ("HEADER", "META", "SPACER", "COLUMNS", "SECTION")


class BuildAborted(RuntimeError):
    """Raised by build_with_validation when pre-flight finds bad citations."""


def get_path(obj: Any, dotted_path: str) -> tuple[bool, Any]:
    """
    Resolve a dotted path into a nested dict/list. Supports list indices via
    '.0', '.1', etc. Returns (found, value). If any segment is missing, returns
    (False, None).
    """
    cur = obj
    for seg in dotted_path.split("."):
        seg = seg.strip()
        if isinstance(cur, list):
            try:
                idx = int(seg)
            except ValueError:
                return False, None
            if idx < 0 or idx >= len(cur):
                return False, None
            cur = cur[idx]
        elif isinstance(cur, dict):
            if seg not in cur:
                return False, None
            cur = cur[seg]
        else:
            return False, None
    return True, cur


def numeric_match(quoted: str, log_value: Any) -> bool:
    """
    Compare a numeric string from an evidence note (e.g. "21,844.99") against a
    value from the log (which may be int, float, or stringified number). Match
    to the precision shown in `quoted` (number of decimal places after stripping
    commas).
    """
    try:
        q = float(quoted.replace(",", ""))
    except ValueError:
        return False
    if isinstance(log_value, str):
        try:
            lv = float(log_value.replace(",", ""))
        except ValueError:
            return False
    else:
        try:
            lv = float(log_value)
        except (TypeError, ValueError):
            return False
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 10 ** (-decimals) / 2 + 1e-9
    return abs(q - lv) <= tol


def collect_numerics(val: Any, acc: list[float]) -> list[float]:
    """Walk a value (scalar / dict / list / str) and append every numeric
    reachable inside it to `acc`. Strings contribute every numeric token they
    contain."""
    if isinstance(val, bool):
        return acc
    if isinstance(val, (int, float)):
        acc.append(float(val))
    elif isinstance(val, str):
        for tok in re.findall(r"[-+]?\d[\d,]*(?:\.\d+)?", val):
            try:
                acc.append(float(tok.replace(",", "")))
            except ValueError:
                pass
    elif isinstance(val, dict):
        for v in val.values():
            collect_numerics(v, acc)
    elif isinstance(val, list):
        for v in val:
            collect_numerics(v, acc)
    return acc


def _find_source_opened_entries(log: dict) -> list[dict]:
    """Return every dict that lives under a `_primary_source_opened` list anywhere
    in the source-read log. Each entry should have at least {file, action} and
    optionally evidence/live_source_url."""
    out: list[dict] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == SOURCE_OPENED_KEY and isinstance(v, list):
                    for entry in v:
                        if isinstance(entry, dict):
                            out.append(entry)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(log)
    return out


def _cited_source_opened_entries(flat_keys: list[str], log: dict) -> list[dict]:
    """Return _primary_source_opened entries reachable through the cited keys.
    A key resolves directly to the list if it ends in `._primary_source_opened`;
    otherwise we walk the subtree at the key and collect any nested entries."""
    out: list[dict] = []
    for key in flat_keys:
        ok, val = get_path(log, key)
        if not ok:
            continue
        # Walk only this subtree to find nested _primary_source_opened lists
        def walk(node: Any) -> None:
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == SOURCE_OPENED_KEY and isinstance(v, list):
                        for entry in v:
                            if isinstance(entry, dict):
                                out.append(entry)
                    else:
                        walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(val)
    return out


def audit_evidence(item: Any, status: Any, notes: Any, log: dict) -> tuple[bool, list[str]]:
    """
    Pure audit of a single (item, status, notes) triple against the source-read
    log. Returns (ok, gaps). ok=True means the row passes.

    Used both at build time (via validate_rows) and at audit time (via
    audit_checklist.py). Identical rule set in both contexts.
    """
    gaps: list[str] = []

    if not isinstance(notes, str) or not notes.strip():
        gaps.append("evidence note is empty")
        return False, gaps

    # FC10 Rule 4: blocking enumeration
    if BLOCKING_RE.search(notes):
        attempts = len(ATTEMPT_RE.findall(notes))
        if attempts < 3:
            gaps.append(
                f"label invokes 'blocking'/'needs Max' but enumerates only {attempts} "
                "tooling-path attempt(s) (rule requires ≥3 distinct attempts with "
                "specific failure mode each)"
            )

    # FC10 Rule 1: log key citation present
    keys = LOG_KEY_RE.findall(notes)
    if not keys:
        gaps.append("no [log:KEY] citation in evidence note")
        return False, gaps

    flat_keys: list[str] = []
    for k in keys:
        flat_keys.extend([s.strip() for s in k.split(",")])

    for key in flat_keys:
        ok, _ = get_path(log, key)
        if not ok:
            gaps.append(f"cited key not found in source-read log: {key}")

    # FC10 Rule 5: quoted numerics must reconcile to a value reachable through
    # one of the cited keys.
    quoted_numbers = QUOTED_VALUE_RE.findall(notes)
    if quoted_numbers:
        log_values: list[float] = []
        for key in flat_keys:
            ok, val = get_path(log, key)
            if ok:
                collect_numerics(val, log_values)
        for q in quoted_numbers:
            if not any(numeric_match(q, lv) for lv in log_values):
                gaps.append(
                    f"quoted numeric '{q}' in evidence note doesn't match any cited "
                    f"log value (cited keys: {flat_keys})"
                )

    # Primary-source-open rule Mode 1: negative-claim audit.
    # If the evidence asserts absence, the cited keys must reach a
    # _primary_source_opened entry. Otherwise the claim is unsupported by an
    # actual open-and-search.
    if NEGATIVE_CLAIM_RE.search(notes):
        opened_entries = _cited_source_opened_entries(flat_keys, log)
        if not opened_entries:
            gaps.append(
                "negative claim (empty/absent/no-X) but no _primary_source_opened "
                "entry reachable from cited keys — open the location and run an "
                "exhaustive search, then add a _primary_source_opened entry, or "
                "downgrade the claim to 'not present in [specific sources opened]'"
            )
        else:
            # FC1 hardening (2026-05-12): every reachable negative-claim
            # _primary_source_opened entry must point to an artifact file on
            # disk that the audit can re-open and scan. The artifact must
            # actually exist; if any cited entry is missing artifact_path or
            # the file does not exist, the claim is unverifiable at audit
            # time and we fail it. Then we re-read each artifact and look for
            # file-presence markers; if any match, the "absent" claim is
            # contradicted by the rendered source and we fail.
            artifact_entries = [
                e for e in opened_entries if e.get(ARTIFACT_PATH_KEY)
            ]
            if not artifact_entries:
                gaps.append(
                    "negative claim cites _primary_source_opened entries but "
                    "none has an artifact_path — every absence claim must "
                    "cite a saved artifact (snapshot YAML, downloaded PDF, "
                    "exported CSV, image file) so the audit can re-read it"
                )
            else:
                for entry in artifact_entries:
                    path_str = entry.get(ARTIFACT_PATH_KEY) or ""
                    path = Path(path_str)
                    if not path.is_absolute():
                        # Resolve relative to the source-read log file location
                        log_path_hint = log.get("_audit_log_path_hint")
                        if log_path_hint:
                            path = Path(log_path_hint).parent / path_str
                        else:
                            path = Path.cwd() / path_str
                    if not path.exists():
                        gaps.append(
                            f"negative claim cites artifact_path '{path_str}' "
                            f"in _primary_source_opened entry but file does "
                            f"not exist on disk — artifact must be saved "
                            f"persistently for re-audit"
                        )
                        continue
                    # Re-read the artifact and look for evidence that
                    # contradicts the absence claim. Per-entry overrides
                    # via negative_check_tokens; default to FILE_PRESENCE_MARKERS
                    # for "folder empty" style claims.
                    try:
                        content = path.read_text(errors="replace")
                    except Exception as e:
                        gaps.append(
                            f"negative claim's artifact_path '{path_str}' "
                            f"could not be read at audit time: {e}"
                        )
                        continue
                    tokens = entry.get(NEGATIVE_CHECK_TOKENS_KEY) or FILE_PRESENCE_MARKERS
                    hits = [t for t in tokens if t in content]
                    # If the entry declares items_found == [] (i.e. "we saw
                    # no items") AND the artifact actually contains file
                    # markers, the claim is contradicted by the source.
                    items_found = entry.get("items_found")
                    if items_found == [] and hits:
                        gaps.append(
                            f"negative claim contradicted by artifact "
                            f"'{path_str}': scan found file-presence markers "
                            f"{hits[:5]} in the rendered source — the claim "
                            f"that the location is empty/absent is not "
                            f"supported by the artifact's content"
                        )

    # Primary-source-open rule Mode 2: SKILL-doc-as-proxy audit.
    # If the evidence cites an EF / numeric constant / range / threshold, at
    # least one cited _primary_source_opened entry must include a
    # live_source_url. SKILL.md is reference material, not a primary source.
    if SKILL_PROXY_RE.search(notes):
        opened_entries = _cited_source_opened_entries(flat_keys, log)
        if not any(e.get(LIVE_URL_KEY) for e in opened_entries):
            gaps.append(
                "evidence cites an EF / numeric constant / range / threshold but "
                "no cited _primary_source_opened entry has a live_source_url — "
                "open the live primary source (Standard EFs sheet, MRV analysis "
                "xlsx, protocol PDF) and record the live URL"
            )

    return len(gaps) == 0, gaps


def _row_triple(entry: tuple) -> tuple[Any, Any, Any] | None:
    """
    Pull (item, status, notes) out of a build_checklist ROWS entry. Returns
    None for non-checklist entries (HEADER/META/SPACER/COLUMNS/SECTION) and for
    rows whose status is not Pass/Fail/Flag (e.g. N/A — by convention those
    skip the [log:KEY] requirement).
    """
    if not entry or not isinstance(entry, tuple):
        return None
    kind = entry[0]
    if kind in NON_ROW_KINDS:
        return None
    # Checklist row shape: (item, check, status, evidence, verifier)
    if len(entry) < 5:
        return None
    item, _check, status, evidence, _verifier = entry[:5]
    if status not in CHECKLIST_STATUSES:
        return None
    return item, status, evidence


def validate_rows(rows: Iterable[tuple], log: dict) -> list[tuple[Any, Any, list[str]]]:
    """
    Walk a build_checklist ROWS list and audit every Pass/Fail/Flag entry.
    Returns a list of (item, status, gaps) for entries that failed audit.
    Empty list = clean. Pure: no I/O, no mutation.
    """
    failures: list[tuple[Any, Any, list[str]]] = []
    for entry in rows:
        triple = _row_triple(entry)
        if triple is None:
            continue
        item, status, notes = triple
        ok, gaps = audit_evidence(item, status, notes, log)
        if not ok:
            failures.append((item, status, gaps))
    return failures


def merge_derived_values(source_reads_path: Path, new_derived: dict) -> dict:
    """
    Merge `new_derived` into the `_derived_values` block of the source-read log
    on disk and write the file back. Existing keys in `_derived_values` not
    present in `new_derived` are preserved; existing keys with the same name are
    overwritten by `new_derived`'s values (most-recent-build-wins). Returns the
    updated log dict.

    The intent: a per-batch build_checklist.py declares the values it computed
    in one place (its DERIVED dict), and this function ensures those values
    land in source_reads.json so [log:_derived_values.KEY] citations resolve at
    audit time without a separate manual sync step.
    """
    if not new_derived:
        return json.loads(source_reads_path.read_text())

    log = json.loads(source_reads_path.read_text())
    existing = log.get("_derived_values") or {}
    if not isinstance(existing, dict):
        raise BuildAborted(
            f"_derived_values in {source_reads_path} is not a dict — refusing to "
            "merge; fix the JSON shape upstream"
        )
    merged = {**existing, **new_derived}
    log["_derived_values"] = merged
    source_reads_path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")
    return log


def format_failures(failures: list[tuple[Any, Any, list[str]]]) -> str:
    """Human-readable failure list for stderr / BuildAborted message."""
    if not failures:
        return "(no failures)"
    lines = []
    for item, status, gaps in failures:
        head = f"{item} [{status}]" if item else f"[{status}]"
        lines.append(f"  • {head}")
        for g in gaps:
            lines.append(f"      - {g}")
    return "\n".join(lines)


def build_with_validation(
    rows: Iterable[tuple],
    source_reads_path: Path | str,
    out_path: Path | str,
    build_workbook_fn: Callable[[Iterable[tuple]], Any],
    derived_values: dict | None = None,
    *,
    print_summary: bool = True,
) -> None:
    """
    Pre-flight + build entry point for per-batch build_checklist.py scripts.

    Sequence:
      1. If `derived_values` is supplied, merge it into source_reads.json's
         `_derived_values` block and rewrite the file.
      2. Reload source_reads.json so validation sees the merged state.
      3. Run validate_rows. If any failures, raise BuildAborted with the full
         list BEFORE the workbook is written. The build script aborts; nothing
         is saved; the operator fixes ROWS or DERIVED and re-runs.
      4. Otherwise, call `build_workbook_fn(rows)` (which returns an openpyxl
         Workbook), save to `out_path`, print a one-line summary.

    The build script stays small — it owns ROWS, DERIVED, and a function that
    converts ROWS into an openpyxl Workbook. The shared library owns the
    validation contract.
    """
    source_reads_path = Path(source_reads_path)
    out_path = Path(out_path)

    if not source_reads_path.exists():
        raise BuildAborted(f"source-read log not found: {source_reads_path}")

    if derived_values:
        merge_derived_values(source_reads_path, derived_values)

    log = json.loads(source_reads_path.read_text())
    log["_audit_log_path_hint"] = str(source_reads_path.resolve())
    rows_list = list(rows)
    failures = validate_rows(rows_list, log)

    if failures:
        msg = (
            f"Pre-flight validation found {len(failures)} bad citation(s) in ROWS. "
            f"Workbook NOT written.\n{format_failures(failures)}\n\n"
            "Fix the cited keys in source_reads.json (or in the build script's "
            "DERIVED dict) and re-run."
        )
        raise BuildAborted(msg)

    wb = build_workbook_fn(rows_list)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    if print_summary:
        n_rows = sum(1 for r in rows_list if _row_triple(r) is not None)
        print(f"Pre-flight clean ({n_rows} rows). Saved {out_path}")
