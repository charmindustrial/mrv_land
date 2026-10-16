#!/usr/bin/env python3
"""
kb_slices.py — build the per-mode Knowledge Base slices the container reads.

Every QA run reads the Knowledge Base in full and carries it in context for
every turn. Parts of it can never apply to a given QA mode (biochar for an
AECN batch, external-document standards, the KDHE permit schedule). A slice is
the Knowledge Base with only those sections removed.

Rules that keep this safe:
  - EXCLUDE-LIST, not include-list. A section is in every slice unless it is
    named below with a reason. A section Max adds later is therefore in every
    slice automatically; nothing new is ever dropped silently.
  - Every exclusion must match exactly one heading. If a heading is renamed or
    removed, the build fails instead of quietly keeping or dropping text.
  - Each slice starts with a banner naming what was removed and pointing at
    the full file, so the agent can read an excluded section if a batch turns
    out to touch it.
  - Built from the Knowledge Base at image build time (Dockerfile), so a slice
    can never be older than the Knowledge Base in the same image.

Usage:
  python3 kb_slices.py            build knowledge-base/slices/*.md, print sizes
  python3 kb_slices.py --check    validate exclusions only, write nothing
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[3]
KB = WS / "knowledge-base/Charm_Isometric_Knowledge_Base.md"
OUT = WS / "knowledge-base/slices"

# Heading prefix (text after the #'s) -> reason. Shared by every bio-oil mode.
_NOT_QA_WORK = {
    "0C. Session Naming Convention": "interactive session naming; no sessions to name in a container run",
    "0B. Session Naming Convention": "duplicate of 0C (same text under a second number)",
    "7. Service Level Agreements": "contract SLA terms with Isometric; no QA check uses them",
    "8. Vaulted KDHE Monitoring": "KDHE permit reporting schedule for the former Vaulted site; not batch or site-emissions QA",
    "13. Active Scheduled Tasks": "Max's scheduled PDF monitor; not QA",
    "14. Connected Services & Integrations": "Mac connectors; the container has none",
    "13. External-Facing Document Standards": "rules for external documents and briefs; QA checklists are internal",
    "Browser Tab Management": "browser tab hygiene; QA uses no browser",
}
_BIOCHAR = {
    "Protocol Version Policy — Biochar Modules": "biochar protocol versions; bio-oil QA only",
    "Biochar Production and Storage v1.0": "biochar protocol; bio-oil QA only",
    "Biochar Storage in Agricultural Soils v1.0": "biochar protocol; bio-oil QA only",
    "Biochar Production and Storage v1.2": "biochar protocol (reference only); bio-oil QA only",
    "Biochar Storage in Soil Environments v1.2": "biochar protocol (reference only); bio-oil QA only",
    "Biochar Characterization & Safety": "biochar characterization; bio-oil QA only",
    "11B. Biochar Project": "biochar registry history; bio-oil QA only",
}
_SITE_EMISSIONS_ONLY = {
    "10B. Site Emissions QA — Agent Architecture": "site-emissions agent design; batch QA uses its own skill",
}

SLICES: dict[str, dict[str, str]] = {
    "aecn": {**_NOT_QA_WORK, **_BIOCHAR, **_SITE_EMISSIONS_ONLY,
             "Charm WODO": "other oil type; the AECN skill stops on a non-AECN batch",
             "Charm Aqueous": "other oil type; the AECN skill stops on a non-AECN batch",
             "Kerry Oil": "other oil type; the AECN skill stops on a non-AECN batch"},
    "charm": {**_NOT_QA_WORK, **_BIOCHAR, **_SITE_EMISSIONS_ONLY,
              "Kerry Oil": "other oil type; the Charm skill covers WODO and Aqueous only",
              "AECN Rail Batch Reference": "AECN railcar mechanics; Charm oil is not railed from AECN",
              "AECN Bill of Lading Formats": "AECN BOL layouts; Charm batches have no AECN BOLs"},
    # Kerry batches carry sparged AECN mass, so every AECN section stays.
    "kerry": {**_NOT_QA_WORK, **_BIOCHAR, **_SITE_EMISSIONS_ONLY,
              "Charm WODO": "other oil type; the Kerry skill covers Kerry only",
              "Charm Aqueous": "other oil type; the Kerry skill covers Kerry only"},
    "site-emissions": {**_NOT_QA_WORK, **_BIOCHAR,
                       "AECN Rail Batch Reference": "per-batch railcar mechanics; site emissions are not batch QA",
                       "AECN Bill of Lading Formats": "per-batch BOL layouts; site emissions are not batch QA"},
}

HEADING = re.compile(r"^(#{1,6}) (.+?)\s*$")


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """(line index, level, text) for every markdown heading outside code fences."""
    out, fence = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def plan(lines: list[str], exclusions: dict[str, str]) -> tuple[list[tuple[int, int, str, str]], list[str]]:
    """Resolve each exclusion to one (start, end, heading, reason) span, or report errors."""
    hs = headings(lines)
    spans, errors = [], []
    for prefix, reason in exclusions.items():
        hits = [(i, lvl, t) for i, lvl, t in hs if t.startswith(prefix)]
        if len(hits) != 1:
            errors.append(f"exclusion {prefix!r} matches {len(hits)} headings (must be exactly 1)")
            continue
        i, lvl, text = hits[0]
        end = next((j for j, l2, _ in hs if j > i and l2 <= lvl), len(lines))
        spans.append((i, end, text, reason))
    return sorted(spans), errors


def build(mode: str, write: bool) -> tuple[int, int, list[str]]:
    raw = KB.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    spans, errors = plan(lines, SLICES[mode])
    if errors:
        return 0, 0, errors
    drop = set()
    for start, end, _, _ in spans:
        drop.update(range(start, end))
    kept = "".join(l for i, l in enumerate(lines) if i not in drop)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    banner = [
        f"<!-- {mode} slice of knowledge-base/Charm_Isometric_Knowledge_Base.md "
        f"(sha256 {digest}), generated by skills/qa/container/kb_slices.py. Do not edit. -->\n",
        f"> **Knowledge Base, {mode} slice.** Everything in the full Knowledge Base is here except "
        f"the sections below, which cannot apply to this QA mode. If this batch turns out to touch "
        f"one of them, read it in the full file: `knowledge-base/Charm_Isometric_Knowledge_Base.md`.\n>\n",
    ] + [f"> - **{t}**: {r}\n" for _, _, t, r in spans] + ["\n"]
    text = "".join(banner) + kept
    if write:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{mode}.md").write_text(text, encoding="utf-8")
    return len(raw), len(text), []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    args = ap.parse_args()
    failed = False
    for mode in SLICES:
        full, sliced, errors = build(mode, write=not args.check)
        if errors:
            failed = True
            for e in errors:
                print(f"[{mode}] ERROR {e}")
        else:
            print(f"[{mode}] {full // 1000} KB -> {sliced // 1000} KB "
                  f"({100 - round(100 * sliced / full)}% smaller)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
