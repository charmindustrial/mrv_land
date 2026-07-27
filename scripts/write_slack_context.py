"""
Populate the Basco ToX workbook Operational Log with Slack-sourced context
for every non-running period ≥ 2 hours, and update the Sparging Compliance tab.
"""

import openpyxl
from openpyxl.styles import Alignment
from pathlib import Path

WORKBOOK = Path(
    "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/"
    "outputs/data-analysis/tox-analysis/Basco_ToX_Analysis_Apr01_May01_2026.xlsx"
)

# ── Ops Context mapping ──────────────────────────────────────────────────────
# Only populate for Operational Log rows that contain a flagged sparging violation.
# All other non-running periods get no comment — they are shutdowns with no
# compliance concern and do not warrant explanation in a verifier-facing log.
#
# Key: (train_label, start_str prefix) → context string

OPS_CONTEXT: dict[tuple[str, str], str] = {
    # Sparging compliance context belongs in the Sparging Compliance tab, not here.
    # This mapping is intentionally empty — Operational Log Ops Context stays blank.
}

# ── Sparging Compliance context ───────────────────────────────────────────────
# All 5 violations are Train 2. Key: row identifier via (train, timestamp prefix)
# Value: context note to write in the "Ops Context" column of Sparging Compliance tab

SPARGE_CONTEXT: dict[tuple[str, str], str] = {
    ("Train 2", "2026-04-13 17:"): (
        "Batch 2-193 sparging active Apr 13. This 2-hour below-threshold dip "
        "(473°F) falls within T2 operational recovery between two running windows "
        "on that date. Hourly resolution caveat applies; likely a brief transition. "
        "Engineering control cuts blower when catalyst below temp, so no "
        "undestructed VOC release."
    ),
    ("Train 2", "2026-04-15 06:"): (
        "Single-hour reading at 630°F — 20°F below 650°F threshold. "
        "Surrounded by above-threshold hours (859°F at 05:00, 796°F at 07:00). "
        "Hourly resolution caveat applies strongly; consistent with brief "
        "transient during continuous operation. Engineering control cuts "
        "blower when catalyst below temp."
    ),
    ("Train 2", "2026-04-15 09:"): (
        "Single-hour reading at 554°F. Located within active sparging window; "
        "system ran at 668–852°F in hours surrounding this reading. "
        "Hourly resolution caveat applies; consistent with brief temperature "
        "dip during continuous operation. Engineering control cuts blower "
        "when catalyst below temp."
    ),
    ("Train 2", "2026-04-16 09:"): (
        "Single offline hour (sensor reading -238) within T2 operating sequence. "
        "Surrounded by above-threshold operation: 667–932°F at 08:00, "
        "724–905°F at 10:00. Sensor briefly offline; not a system shutdown. "
        "Engineering control cuts blower when catalyst below temp."
    ),
    ("Train 2", "2026-04-18 05:"): (
        "First hour of T2's 203-hour below-temp period. T2 was shutting down "
        "at this hour; sparging binary may reflect residual on-state at "
        "moment of shutdown rather than active injection. Engineering control "
        "cuts blower when catalyst below temp, so no undestructed VOC release. "
        "T2 remained offline/below-temp through Apr 26."
    ),
}


def match_key(cell_val: str, key_prefix: str) -> bool:
    """Match cell value (datetime string) against a 16-char prefix key."""
    if not cell_val:
        return False
    s = str(cell_val).strip()
    return s.startswith(key_prefix)


def write_context() -> None:
    wb = openpyxl.load_workbook(WORKBOOK)

    # ── Operational Log ───────────────────────────────────────────────────────
    ws_log = wb["Operational Log"]

    # Find column indices (row 1 = header)
    header = {cell.value: cell.column for cell in ws_log[1]}
    col_train   = header.get("Train")
    col_start   = header.get("Start")
    col_status  = header.get("Status")
    col_dur     = header.get("Duration (hrs)")
    col_context = header.get("Ops Context (Slack)")

    print(f"Operational Log columns: train={col_train} start={col_start} "
          f"status={col_status} dur={col_dur} context={col_context}")

    written = 0
    skipped = 0
    for row in ws_log.iter_rows(min_row=2):
        train_cell  = row[col_train  - 1].value if col_train  else None
        start_cell  = row[col_start  - 1].value if col_start  else None
        status_cell = row[col_status - 1].value if col_status else None
        dur_cell    = row[col_dur    - 1].value if col_dur    else None

        if train_cell is None:
            break  # past data rows

        try:
            dur_h = float(dur_cell) if dur_cell is not None else 0
        except (ValueError, TypeError):
            dur_h = 0

        # Only non-running (below temp or offline) periods ≥ 2h
        if str(status_cell).strip() == "At temperature (≥ 650°F)" or dur_h < 2:
            skipped += 1
            continue

        # Look up context
        start_str = str(start_cell).strip() if start_cell else ""
        ctx = None
        for (t, prefix), text in OPS_CONTEXT.items():
            if str(train_cell).strip() == t and start_str.startswith(prefix):
                ctx = text
                break

        # Leave blank if no sparging violation in this period
        cell = row[col_context - 1]
        cell.value = ctx if ctx is not None else None
        if ctx:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        written += 1

    print(f"Operational Log: {written} rows written, {skipped} skipped (running or <2h)")

    # ── Sparging Compliance ───────────────────────────────────────────────────
    if "Sparging Compliance" not in wb.sheetnames:
        print("WARNING: 'Sparging Compliance' tab not found — skipping")
    else:
        ws_sc = wb["Sparging Compliance"]
        sc_header = {cell.value: cell.column for cell in ws_sc[1]}
        sc_col_train   = sc_header.get("Train")
        sc_col_time    = sc_header.get("Time")
        sc_col_context = sc_header.get("Ops Context (Slack)")

        print(f"Sparging Compliance columns: train={sc_col_train} time={sc_col_time} "
              f"context={sc_col_context}")

        sc_written = 0
        for row in ws_sc.iter_rows(min_row=2):
            if sc_col_train is None or sc_col_time is None or sc_col_context is None:
                break
            train_cell = row[sc_col_train  - 1].value
            time_cell  = row[sc_col_time   - 1].value

            if train_cell is None:
                break

            time_str = str(time_cell).strip() if time_cell else ""
            ctx = None
            for (t, prefix), text in SPARGE_CONTEXT.items():
                if str(train_cell).strip() == t and time_str.startswith(prefix):
                    ctx = text
                    break

            if ctx is None:
                ctx = "No corresponding activity found in ops channel."

            cell = row[sc_col_context - 1]
            cell.value = ctx
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            sc_written += 1

        print(f"Sparging Compliance: {sc_written} rows written")

    wb.save(WORKBOOK)
    print(f"\nSaved: {WORKBOOK}")


if __name__ == "__main__":
    write_context()
