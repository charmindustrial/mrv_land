#!/usr/bin/env python3
"""
discover.py — find Certify removals that can be QA'd and resolve each one's run inputs.

There is no canonical link from a Certify removal to a batch, but each week has at most
one removal per batch type, so (week, type) identifies a removal. For each recent removal:

  1. type     from its component names (Kerry / QOWV / WODO / AECN rail / AECN truck).
  2. week     the Saturday-to-Friday injection week its dates fall in: month and
              W{ceil(day/7)} of completed_on, i.e. INJ-MM-YYYY-Wn.
  3. proof    the removal's injected mass (the kg inputs of its Injection sequestration
              component) must appear in that week's Ops Notes, on the type's tab. Labels
              have drifted (e.g. INJ-06-2026-W2-QOWV is dated W4), so when the mass is
              not in the computed week, the neighbouring weeks are tried. Found nowhere:
              the row needs a person.
  4. inputs   batch ID (INJ-MM-YYYY-Wn + suffix), QA mode, Certify URL, the week's Drive
              folder (parent of its Ops Notes), reporting period (from the RP folder).
  5. status   from earlier container runs (gs://<bucket>/runs/*/summary.json) and the
              QA registries.

A row is "ready" only when type and week are unambiguous and the mass check passed.
Everything else carries the reason, never a guess.

  discover.py [--limit 40] [--out candidates.json]
Needs ISO_PROD_* (Certify) and Drive access (ADC, or an injected service in tests).
"""
from __future__ import annotations

import argparse
import datetime
import io
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certify_read  # noqa: E402

# Confirmed naming (2026-10-23). Older batches did not always follow it.
SUFFIX = {"AECN": "", "AECN-Truck": "-AECN-Truck", "QOWV": "-QOWV", "KERRY": "-KERRY", "WODO": "-WODO"}
MODE = {"AECN": "batch-qa-aecn", "AECN-Truck": "batch-qa-aecn", "QOWV": "batch-qa-charm",
        "WODO": "batch-qa-charm", "KERRY": "batch-qa-kerry"}
OPS_TAB = {"AECN": ["AECN Rail", "AECN Truck"], "AECN-Truck": ["AECN Truck"], "QOWV": ["QOWV"],
           "WODO": ["WODO"], "KERRY": ["Kerry"]}
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/{prj}/ghg-entry/{rmv}/edit"
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july",
                                      "august", "september", "october", "november", "december"], 1)}


def classify(component_names: list[str]) -> tuple[str | None, str]:
    """(type, note). Site-emission components are ignored; two batch types = ambiguous."""
    text = " | ".join(component_names).lower()
    found = []
    if "kerry" in text:
        found.append("KERRY")
    if "qowv" in text:
        found.append("QOWV")
    if "wodo" in text:
        found.append("WODO")
    if "aecn" in text:
        rail = "rail loads" in text or "rail transport" in text
        truck = "truck loads" in text or "aecn to la tanker" in text
        found.append("AECN-Truck" if truck and not rail else "AECN")
        if rail and truck:
            return ("AECN" if len(found) == 1 else None,
                    "AECN rail and truck loads in one removal" if len(found) == 1 else f"several batch types: {found}")
    if len(found) == 1:
        return found[0], ""
    return None, ("no batch type recognised in component names" if not found else f"several batch types: {found}")


def week_label(completed_on: str, shift: int = 0) -> str:
    d = datetime.date.fromisoformat(completed_on) + datetime.timedelta(days=7 * shift)
    return f"INJ-{d.month:02d}-{d.year}-W{math.ceil(d.day / 7)}"


def injected_masses(dump: dict) -> list[float]:
    """kg inputs of the Injection sequestration component(s)."""
    out = []
    for comp in dump["components"]:
        if "injection sequestration" not in (comp["component"].get("display_name") or "").lower():
            continue
        for inp in comp["inputs"]:
            for dp in inp["datapoints"]:
                q = dp.get("quantity") or {}
                if "kilogram" in str(q.get("unit", "")).lower() and isinstance(q.get("magnitude"), (int, float)):
                    out.append(float(q["magnitude"]))
    return out


class DriveIndex:
    """Week -> Ops Notes / week folder / RP, from the Drive API, cached per run."""

    def __init__(self, svc):
        self.svc, self.cache, self.tabs = svc, {}, {}

    def _get(self, fid, fields="id,name,parents,webViewLink"):
        return self.svc.files().get(fileId=fid, fields=fields, supportsAllDrives=True).execute()

    def week(self, label: str) -> list[dict]:
        """Every working copy of the week's Ops Notes, best first. The same Ops Notes is
        copied into Final Reporting Package snapshots and Verified Periods; snapshots are
        never used, the working RP folder ranks above Verified Periods."""
        if label in self.cache:
            return self.cache[label]
        res = self.svc.files().list(
            q=f"name = '{label} Ops Notes' and trashed = false", fields="files(id,name,parents,webViewLink)",
            supportsAllDrives=True, includeItemsFromAllDrives=True, corpora="allDrives").execute().get("files", [])
        copies = []
        for ops in res:
            if not ops.get("parents"):
                continue
            wk = self._get(ops["parents"][0])
            ibd = self._get(wk["parents"][0]) if wk.get("parents") else {}
            rp = self._get(ibd["parents"][0]) if ibd.get("parents") else {}
            above = self._get(rp["parents"][0]) if rp.get("parents") else {}
            names = [ibd.get("name", ""), rp.get("name", ""), above.get("name", "")]
            if ibd.get("name") != "Injection Batch Data" or any(
                    n.startswith("Copy of") or "Final Reporting Package" in n for n in names):
                continue                                    # snapshot or stray copy
            copies.append({"rank": 1 if "Verified Periods" in names else 0,
                           "where": " / ".join(reversed([n for n in names if n])) + f" / {wk.get('name')}",
                           "ops_notes_id": ops["id"], "ops_notes_url": ops.get("webViewLink"),
                           "week_folder_id": wk["id"], "week_folder_url": wk.get("webViewLink") or
                           f"https://drive.google.com/drive/folders/{wk['id']}",
                           "rp_folder": rp.get("name"), "reporting_period": rp_period(rp.get("name") or "", label)})
        self.cache[label] = sorted(copies, key=lambda c: c["rank"])
        return self.cache[label]

    def tab_numbers(self, ops_id: str, tab_keys: list[str]) -> list[float] | None:
        """Every numeric cell on the Ops Notes tabs for this type (cached per file)."""
        if ops_id not in self.tabs:
            import openpyxl
            from googleapiclient.http import MediaIoBaseDownload
            buf = io.BytesIO()
            req = self.svc.files().export_media(
                fileId=ops_id, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            dl = MediaIoBaseDownload(buf, req)
            done = False
            while not done:
                _, done = dl.next_chunk()
            wb = openpyxl.load_workbook(io.BytesIO(buf.getvalue()), data_only=True, read_only=True)
            self.tabs[ops_id] = {ws.title: [float(v) for row in ws.iter_rows(values_only=True) for v in row
                                            if isinstance(v, (int, float)) and not isinstance(v, bool)]
                                 for ws in wb.worksheets}
        tabs = self.tabs[ops_id]
        hits = [t for t in tabs if any(k.lower() in t.lower() for k in tab_keys)]
        return None if not hits else [n for t in hits for n in tabs[t]]

    def numbers_by_tab(self, ops_id: str, tab_key: str) -> list[float]:
        self.tab_numbers(ops_id, [tab_key])
        return [n for t, nums in self.tabs[ops_id].items() if tab_key.lower() in t.lower() for n in nums]


def rp_period(rp_name: str, label: str) -> str | None:
    """'October 1 - October 31 RP' -> '2026-10-01 to 2026-10-31' (year from the week label)."""
    m = re.match(r"\s*([A-Za-z]+)\s+(\d{1,2})\s*-\s*([A-Za-z]+)\s+(\d{1,2})", rp_name)
    if not m or m.group(1).lower() not in MONTHS or m.group(3).lower() not in MONTHS:
        return None
    year = int(label.split("-")[2])
    a = datetime.date(year, MONTHS[m.group(1).lower()], int(m.group(2)))
    b = datetime.date(year, MONTHS[m.group(3).lower()], int(m.group(4)))
    return f"{a.isoformat()} to {b.isoformat()}"


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= max(0.5, 1e-6 * max(abs(a), abs(b)))


def mass_in(numbers: list[float], masses: list[float]) -> float | None:
    for mass in masses:
        if any(_close(n, mass) for n in numbers):
            return mass
    return None


def mass_as_sum(rail: list[float], truck: list[float], masses: list[float]) -> tuple[float, float, float] | None:
    """Mixed AECN removal: Certify holds one injected mass, the Ops Notes split it across
    the AECN Rail and AECN Truck tabs. (mass, rail value, truck value) when they add up."""
    import bisect
    ts = sorted(t for t in truck if t > 0)
    for mass in masses:
        for r_ in (x for x in rail if 0 < x < mass):
            need = mass - r_
            i = bisect.bisect_left(ts, need - 0.01)    # tight: a coincidental pair must be very unlikely
            if i < len(ts) and abs(ts[i] - need) <= 0.01:
                return mass, r_, ts[i]
    return None


def check_mass(drive: "DriveIndex", ops_id: str, btype: str, masses: list[float], mixed: bool) -> str | None:
    if not masses:
        return None
    nums = drive.tab_numbers(ops_id, OPS_TAB[btype])
    if not nums:
        return None
    m = mass_in(nums, masses)
    if m is not None:
        return f"{m:,.2f} kg found on the {'/'.join(OPS_TAB[btype])} tab"
    if mixed:
        pair = mass_as_sum(drive.numbers_by_tab(ops_id, "AECN Rail"), drive.numbers_by_tab(ops_id, "AECN Truck"), masses)
        if pair:
            return f"{pair[0]:,.2f} kg = {pair[1]:,.2f} (AECN Rail tab) + {pair[2]:,.2f} (AECN Truck tab)"
    return None


def resolve(dump: dict, drive: DriveIndex) -> dict:
    r = dump["removal"]
    names = [c["component"].get("display_name") or "" for c in dump["components"]]
    btype, note = classify(names)
    row = {"removal_id": dump["removal_id"], "started_on": r.get("started_on"), "completed_on": r.get("completed_on"),
           "net_t": round((r.get("co2e_net_removed_kg") or 0) / 1000, 3), "ghg_statement_id": r.get("ghg_statement_id"),
           "type": btype, "certify_url": CERTIFY_URL.format(prj=dump["project_id"], rmv=dump["removal_id"]),
           "problems": [note] if note and btype is None else [], "notes": [note] if note and btype else []}
    if btype is None or not r.get("completed_on"):
        return {**row, "ready": False}
    masses = injected_masses(dump)
    if not masses:
        row["problems"].append("no injected mass (kg) on the Injection sequestration component")
    computed = week_label(r["completed_on"])
    mixed = btype == "AECN" and any("rail and truck" in n for n in row["notes"])
    found = []                                         # (label, copy, description), one per week at most
    for shift in (0, -1, 1, -2, 2):
        label = week_label(r["completed_on"], shift)
        hits = [(wk, d) for wk in drive.week(label) for d in [check_mass(drive, wk["ops_notes_id"], btype, masses, mixed)] if d]
        best = [h for h in hits if h[0]["rank"] == min((x[0]["rank"] for x in hits), default=0)]
        if len(best) > 1:
            row["problems"].append(f"mass found in {len(best)} equally ranked copies of {label} Ops Notes: "
                                   + "; ".join(h[0]["where"] for h in best))
        elif best:
            found.append((label, best[0][0], best[0][1]))
    if len(found) > 1:
        row["problems"].append("injected mass found in more than one week's Ops Notes: " + ", ".join(f[0] for f in found))
    elif not found:
        row["problems"].append(f"injected mass not found in the Ops Notes of {computed} or the two weeks either side")
    else:
        label, wk, desc = found[0]
        row.update(week=label, batch_id=label + SUFFIX[btype], mode=MODE[btype], drive_folder=wk["week_folder_url"],
                   ops_notes_url=wk["ops_notes_url"], reporting_period=wk["reporting_period"], rp_folder=wk["rp_folder"],
                   ops_notes_where=wk["where"], mass_check=f"{desc} of {label} Ops Notes")
        if label != computed:
            row["notes"].append(f"dates point to {computed}, but the mass is in {label} Ops Notes")
    row["ready"] = not row["problems"] and "batch_id" in row
    return row


def discover_all(limit: int = 40, drive_service=None) -> dict:
    """Resolve the most recent `limit` removals. One failing removal never hides the rest."""
    import drive_read
    cl = certify_read.ReadOnlyCertify()
    drive = DriveIndex(drive_service or drive_read.service())
    recent = sorted(cl.get("/removals", last=limit).get("nodes", []),
                    key=lambda x: x.get("completed_on") or "", reverse=True)
    rows = []
    for rem in recent:
        try:
            rows.append(resolve(certify_read.dump_removal(cl, rem["id"]), drive))
        except Exception as e:  # noqa: BLE001
            rows.append({"removal_id": rem["id"], "ready": False, "problems": [f"lookup failed: {e}"]})
    return {"generated_at_utc": certify_read._now(), "candidates": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=40, help="most recent removals to consider")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = discover_all(a.limit)
    text = json.dumps(out, indent=1, default=str)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}: {sum(r['ready'] for r in rows)} ready, {sum(not r['ready'] for r in rows)} need a person")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
