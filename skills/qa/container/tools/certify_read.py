#!/usr/bin/env python3
"""
certify_read.py — READ-ONLY Isometric Certify access for the QA container.

The QA skills read Certify only through this file, which uses the Certify
REST API: components and their inputs, datapoints, and sources. There is no
write path in this file: only GET requests exist.

Credentials (set by the Cloud Run job from Secret Manager):
  ISOMETRIC_ENV              prod | sandbox   (default prod in the container)
  ISO_PROD_CLIENT_SECRET     X-Client-Secret header
  ISO_PROD_JWT               Bearer token
  (ISO_SANDBOX_* for sandbox)

Commands:
  removal <rmv_id | Certify removal URL> [--out FILE]
      Writes FILE (the full dump) and FILE_summary.md (a compact table of every
      component, input value, SD and source, each with its JSON path into the
      full dump). Read the summary; open the full dump when a check needs a
      field the summary does not show. The full dump holds the removal totals, every attributed
      component with its blueprint (the formula Certify evaluates), every
      input resolved to its datapoint(s) (magnitude, unit, standard_deviation,
      uncertainty_justification, source_ids), and every source referenced by
      those datapoints. This is the container's equivalent of opening all
      four Certify tabs and every component modal.

  source <src_id> --out DIR
      Download one source file (via its private URL) into DIR so it can be
      opened with the Read tool (PDF / image) or openpyxl (xlsx).

  datapoint <dp_id>            One datapoint.
  ghg-statement <ggs_id>       One GHG statement.
  get <api_path> [k=v ...]     Any other GET, e.g. `get /components removal_id=rmv_X`.

Output is JSON on stdout (or --out FILE). Every dump carries `fetched_at_utc`
and `live_source_url` so the source-read log can cite it.

Known gaps vs the UI (also listed in CONTAINER_MODE.md):
  - The REST API does not return the per-component tCO2e figure the UI shows.
    Component values must be computed from the blueprint expression and the
    inputs; the removal-level net (co2e_net_removed_kg) IS returned and is the
    cross-check for that computation.
  - Sources attached at removal level only (not linked to any datapoint) are
    not reachable through REST. `sources` here is the union of every
    datapoint's source_ids.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterator

BASE_URLS = {
    "sandbox": "https://api.sandbox.isometric.com/mrv/v0",
    "prod": "https://api.isometric.com/mrv/v0",
}
UI_REMOVAL_URL = "https://registry.isometric.com/account/certify/project/{prj}/ghg-entry/{rmv}/edit"
RMV_RE = re.compile(r"rmv_[A-Z0-9]+")
PRJ_RE = re.compile(r"prj_[A-Z0-9]+")


class CertifyError(RuntimeError):
    pass


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ReadOnlyCertify:
    def __init__(self, env: str | None = None):
        self.env = env or os.environ.get("ISOMETRIC_ENV", "prod")
        if self.env not in BASE_URLS:
            raise CertifyError(f"ISOMETRIC_ENV must be sandbox|prod, got {self.env!r}")
        prefix = f"ISO_{self.env.upper()}"
        self._secret = os.environ.get(f"{prefix}_CLIENT_SECRET")
        self._jwt = os.environ.get(f"{prefix}_JWT")
        if not self._secret or not self._jwt:
            raise CertifyError(f"Missing {prefix}_CLIENT_SECRET / {prefix}_JWT in the environment.")
        self.base_url = BASE_URLS[self.env]

    def get(self, path: str, **params: Any) -> Any:
        url = self.base_url + path
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {self._jwt}")
        req.add_header("X-Client-Secret", self._secret)
        req.add_header("Accept", "application/json")
        for attempt in (1, 2):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    raw = resp.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt == 1:
                    time.sleep(30)
                    continue
                detail = e.read().decode("utf-8", errors="replace")
                raise CertifyError(f"GET {path} -> HTTP {e.code}: {detail[:500]}") from e
            except urllib.error.URLError as e:
                raise CertifyError(f"GET {path} -> network error: {e}") from e

    def list_all(self, path: str, page_size: int = 50, **params: Any) -> Iterator[dict]:
        cursor = None
        while True:
            page = self.get(path, **params, first=page_size, after=cursor)
            for node in (page or {}).get("nodes") or []:
                yield node
            info = (page or {}).get("page_info") or {}
            cursor = info.get("end_cursor")
            if not info.get("has_next_page") or not cursor:
                return


def _input_datapoint_ids(inp: dict) -> list[str]:
    if inp.get("datapoint_id"):
        return [inp["datapoint_id"]]
    return list(inp.get("datapoint_ids") or [])


def dump_removal(c: ReadOnlyCertify, ref: str) -> dict:
    m = RMV_RE.search(ref)
    if not m:
        raise CertifyError(f"No rmv_ id found in {ref!r}")
    rmv_id = m.group(0)
    prj_from_url = PRJ_RE.search(ref)

    removal = c.get(f"/removals/{rmv_id}")
    attributions = list(c.list_all(f"/removals/{rmv_id}/component_attributions"))

    dp_cache: dict[str, dict] = {}
    blueprint_cache: dict[str, dict] = {}
    source_ids: list[str] = []
    components = []
    for att in attributions:
        comp = c.get(f"/components/{att['component_id']}")
        bp_key = comp.get("blueprint_key")
        if bp_key and bp_key not in blueprint_cache:
            blueprint_cache[bp_key] = c.get(f"/component_blueprints/{bp_key}")
        inputs = []
        for inp in comp.get("inputs") or []:
            dps = []
            for dp_id in _input_datapoint_ids(inp):
                if dp_id not in dp_cache:
                    dp_cache[dp_id] = c.get(f"/datapoints/{dp_id}")
                dp = dp_cache[dp_id]
                for s in dp.get("source_ids") or []:
                    if s not in source_ids:
                        source_ids.append(s)
                dps.append(dp)
            inputs.append({"input_key": inp.get("input_key"), "datapoints": dps})
        components.append({
            "attribution": att,
            "component": {k: v for k, v in comp.items() if k != "inputs"},
            "blueprint_key": bp_key,
            "inputs": inputs,
        })

    sources = []
    for s in source_ids:
        src = c.get(f"/sources/{s}")
        linked = [dp_id for dp_id, dp in dp_cache.items() if s in (dp.get("source_ids") or [])]
        sources.append({**src, "linked_datapoint_ids": linked})

    project_id = (prj_from_url.group(0) if prj_from_url else
                  next((dp.get("project_id") for dp in dp_cache.values() if dp.get("project_id")), None))
    return {
        "fetched_at_utc": _now(),
        "env": c.env,
        "removal_id": rmv_id,
        "project_id": project_id,
        "live_source_url": UI_REMOVAL_URL.format(prj=project_id, rmv=rmv_id) if project_id else None,
        "removal": removal,
        "components": components,
        "blueprints": blueprint_cache,
        "sources": sources,
        "certify_sources_via_datapoints_total": len(sources),
        "gaps": [
            "Per-component tCO2e is not returned by the REST API; compute it from `blueprints` "
            "expressions and the input datapoints, and cross-check the sum against "
            "removal.co2e_net_removed_kg.",
            "Removal-level sources not linked to any datapoint are not visible here.",
        ],
    }


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        # Full precision: the checklist cites exact values and compares to ~0.001 tCO2e.
        return repr(v)
    return "" if v is None else str(v)


def summarize(dump: dict, full_path: str) -> str:
    """Compact view for the agent's context. Every value carries its JSON path in
    the full dump, so it can be cited and re-checked there."""
    r = dump["removal"] or {}
    src_names = {s["id"]: s.get("original_filename") or s.get("display_name") for s in dump["sources"]}
    out = [
        f"# Certify removal {dump['removal_id']} (summary)",
        f"Full dump: `{full_path}` · fetched {dump['fetched_at_utc']} · env {dump['env']} · "
        f"live: {dump['live_source_url']}",
        "",
        f"- removal.co2e_net_removed_kg: {_fmt(r.get('co2e_net_removed_kg'))} "
        f"(SD {_fmt(r.get('co2e_net_removed_standard_deviation_kg'))}); "
        f"without discount: {_fmt(r.get('co2e_net_removed_without_discount_kg'))}",
        f"- started_on {r.get('started_on')} · completed_on {r.get('completed_on')} · "
        f"supplier_reference_id {r.get('supplier_reference_id')} · ghg_statement_id {r.get('ghg_statement_id')}",
        "",
    ]
    for ci, comp in enumerate(dump["components"]):
        c, a = comp["component"], comp["attribution"]
        out.append(f"## [{ci}] {c.get('display_name')}  (components.{ci})")
        out.append(f"blueprint `{comp['blueprint_key']}` · type {c.get('type')} · scope {c.get('scope')} · "
                   f"attribution_factor {_fmt(a.get('attribution_factor'))} · group {a.get('component_group_key')}")
        out.append("")
        out.append("| input_key | datapoint (path) | magnitude | unit | SD | SD % | sources |")
        out.append("|---|---|---|---|---|---|---|")
        for ii, inp in enumerate(comp["inputs"]):
            for di, dp in enumerate(inp["datapoints"]):
                q = dp.get("quantity") or {}
                mag, sd = q.get("magnitude"), q.get("standard_deviation")
                pct = f"{100 * sd / mag:.3g}" if isinstance(mag, (int, float)) and isinstance(sd, (int, float)) and mag else ""
                srcs = "; ".join(src_names.get(s, s) for s in dp.get("source_ids") or []) or "**none**"
                path = f"components.{ci}.inputs.{ii}.datapoints.{di}"
                out.append(f"| {inp['input_key']} | {dp.get('display_name')} (`{path}`) | {_fmt(mag)} | "
                           f"{_fmt(q.get('unit'))} | {_fmt(sd)} | {pct} | {srcs} |")
        out.append("")
    out.append(f"## Sources via datapoints ({dump['certify_sources_via_datapoints_total']})")
    for si, s in enumerate(dump["sources"]):
        out.append(f"- `{s['id']}` {s.get('original_filename') or s.get('display_name')} "
                   f"(sources.{si}; linked to {len(s['linked_datapoint_ids'])} datapoint(s))")
    out += ["", "## API gaps (see CONTAINER_MODE.md)"] + [f"- {g}" for g in dump["gaps"]]
    return "\n".join(out) + "\n"


def download_source(c: ReadOnlyCertify, src_id: str, out_dir: Path) -> dict:
    src = c.get(f"/sources/{src_id}")
    url = c.get(f"/sources/{src_id}/private_url")
    if not isinstance(url, str) or not url.startswith("http"):
        raise CertifyError(f"Source {src_id} returned no downloadable URL: {url!r}")
    out_dir.mkdir(parents=True, exist_ok=True)
    name = src.get("original_filename") or src.get("display_name") or src_id
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    dest = out_dir / f"{src_id}__{name}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return {"fetched_at_utc": _now(), "source": src, "saved_to": str(dest), "bytes": dest.stat().st_size}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("removal"); p.add_argument("ref"); p.add_argument("--out")
    p = sub.add_parser("source"); p.add_argument("src_id"); p.add_argument("--out", required=True)
    p = sub.add_parser("datapoint"); p.add_argument("dp_id"); p.add_argument("--out")
    p = sub.add_parser("ghg-statement"); p.add_argument("ggs_id"); p.add_argument("--out")
    p = sub.add_parser("get"); p.add_argument("path"); p.add_argument("params", nargs="*"); p.add_argument("--out")
    args = ap.parse_args()

    try:
        c = ReadOnlyCertify()
        if args.cmd == "removal":
            result = dump_removal(c, args.ref)
        elif args.cmd == "source":
            result = download_source(c, args.src_id, Path(args.out))
            print(json.dumps(result, indent=1))
            return 0
        elif args.cmd == "datapoint":
            result = {"fetched_at_utc": _now(), "datapoint": c.get(f"/datapoints/{args.dp_id}")}
        elif args.cmd == "ghg-statement":
            result = {"fetched_at_utc": _now(), "ghg_statement": c.get(f"/ghg_statements/{args.ggs_id}")}
        else:
            params = dict(kv.split("=", 1) for kv in args.params)
            result = {"fetched_at_utc": _now(), "path": args.path, "response": c.get(args.path, **params)}
    except CertifyError as e:
        print(f"CERTIFY ERROR: {e}", file=sys.stderr)
        return 1

    text = json.dumps(result, indent=1)
    if args.cmd == "removal":
        # The full dump goes to disk only; the agent reads the summary.
        out = Path(args.out or f"certify_{result['removal_id']}.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        summary_path = out.with_name(out.stem + "_summary.md")
        summary_path.write_text(summarize(result, out.as_posix()), encoding="utf-8")
        print(f"wrote {out} (full dump, {len(text) // 1000} KB) and {summary_path} (read this)")
    elif getattr(args, "out", None):
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
