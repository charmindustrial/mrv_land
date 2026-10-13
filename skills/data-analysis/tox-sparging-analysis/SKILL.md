---
name: tox-sparging-analysis
description: >
  Thermal oxidizer (ToX) temperature analysis agent for Charm Industrial's Basco injection site.
  Processes catalyst temperature data from Train 1 and Train 2 for a reporting period and produces
  the "CatOx" reporting package: a Raw workbook (readings as received) and a verifier-facing
  Processed workbook of exactly two clean charts, one per train, against the 600°F setpoint.
  ALWAYS trigger when: the user asks to analyze ToX temperature data, process sparging oxidizer
  data, review oxidizer performance, prepare a ToX / CatOx report for a reporting period, or
  references the Basco thermal oxidizer, catalyst temperatures, TIT-2151/2152/2251/2252 sensors,
  "CatOx," or "TOx monitoring data." Also trigger for any reference to the Basco air permit, VOC
  destruction, or sparging/oxidizer performance reporting for any Charm reporting period.
---

# Basco ToX — CatOx Reporting Package

You analyze catalyst temperature data from Charm Industrial's Basco thermal oxidizer (two
independent catalyst trains, each with an inlet and outlet sensor) and produce the **CatOx
reporting package** for a reporting period. This matches the verified precedent set in the May
2026 reporting — not a generic analysis workbook.

## What the reporting package is (verified precedent — do not deviate)

Each reporting period, deliver exactly three things (the first two you build; the third is static):

1. **`{Month} CatOx -- Raw.xlsx`** — the raw readings exactly as received, one sheet.
2. **`{Month} CatOx -- Processed.xlsx`** — **verifier-facing. Three tabs** (declared in
   `references/catox_config.json` → `processed_tabs`): two chart tabs, one per train
   ("Train 1 — Temperature", "Train 2 — Temperature"), each a single clean chart (inlet + outlet
   lines, the 600°F minimum-setpoint line, grey offline shading), plus a **"Raw Data"** tab with
   the readings exactly as received (added per Max, July 2026 — carried in the Processed workbook
   as well as in the standalone Raw workbook). The script asserts the built tab set matches the
   config.
3. **CatOx Engineering Brief** (Google Drive doc id `1pBwtOUc78e5ayvgTxMhiOJsPrO5L9ZPP681Oy3CApJg`) —
   the interpretation and controls narrative. Static; reused each period. You do not regenerate it.

**Do NOT add** Operational Log, Transition Events, Combustion Signal, or Notes tabs to the
Processed workbook. Those are TMI for a verifier (confirmed by Max, July 2026). The interpretation
belongs in the Brief, not in the workbook.

## How the data destroys VOCs (context)

The ToX destroys VOCs (primarily benzene) stripped from bio-oil during sparging. The **compliance
guarantee is a hardware interlock, not the temperature record**: per the CatOx Engineering Brief,
*"The sparging blower cannot activate unless the oxidizer is on. This is a hard control with no
operator override."* Site SOP also requires the catalyst inlet to be at 600°F before the gate
valve is **closed** — the Brief's words are *"confirm the catalyst inlet is at 600°F before
closing the gate valve and introducing air into the tank"* (earlier versions of this skill said
"opened", which was wrong) — and an E-stop stops the blower. The temperature data **corroborates** this
record; it does not carry the compliance burden.

**Reading the temperature data (from the Brief — quote it, do not invent):** *"There is no single
sensor signal that cleanly distinguishes actively stripping benzene from blower running with
benzene exhausted. At the end of a sparging campaign, the blower continues to run as benzene
concentration approaches zero. In this phase the catalyst outlet may not show a significant
exothermic rise above the setpoint, because there is no remaining benzene to react with. This is
the expected completion state of a sparging campaign — not evidence of uncontrolled release."*
So a below-setpoint outlet during a campaign means **no VOCs present to drive the exothermic
reaction** — not a failure to destroy VOCs. Active destruction shows as an outlet of 850–1000°F.

## Source data format

Max provides the period's export or points you to it in Drive (typically the reporting period's
`Additional Documentation/Oxidizer Data` folder). Since September 2026 that folder sits in
Garrett's Drive area and is **not** on Max's local Drive mount — download through the Drive
connector (the result lands in a saved file; decode it into its own scratchpad folder).

**September 2026 onward:** Garrett pulls the data from BigQuery as **one combined CSV**
(`timestamp_central` + four `train{1,2}_ox{2100,2200}_catalyst_{inlet,outlet}_F` columns,
`M/D/YYYY H:MM` Central). Pass the single file to `--input`.
**July–August 2026:** two CSVs, one per train (`t_stamp, InletTemp, OutletTemp`,
`YYYY-MM-DD HH:MM:SS.fff`). Pass **both** to `--input` in either order; the script merges them on
the timestamp and identifies each train from its column headers.
All shapes: 5-minute readings, **`0` marks offline**, **empty cells mark single dropped readings**
(new in September 2026), columns **correctly labeled (no swap)**.
Read `references/column_mapping.md` and `references/thresholds.md` before processing.

Run the script with `python3 -P -E` (not `-I`): pandas lives in the user package folder, which
`-I` hides. `-P` still keeps the script's and current folder out of the import path.

## Workflow

### Step 1: Run the script
```bash
python3 "skills/data-analysis/tox-sparging-analysis/scripts/generate_tox_charts.py" \
  --input "<train 1 csv>" "<train 2 csv>" \
  --output "outputs/data-analysis/tox-analysis/" \
  --month "July 2026"
```
It builds both workbooks, runs a **column-orientation self-check** (warns if a train's outlet
reads colder than its inlet), runs a **stuck-reading check**, and prints per-train summary stats
for your chat report.

### Step 2: Confirm orientation, then read the stuck-reading check
Confirm the script reported orientation OK for both trains. If it warns, stop and verify before
delivering — do not blindly apply any historical swap (see column_mapping.md).

Then read the stuck-reading output. If it reports an **all-channel frozen block**, the historian
held last-good values and those rows are not live readings — and if the held outlet sits above the
setpoint it inflates the at-temperature share. Report the at-temperature figure **both ways** (as
recorded, and excluding held readings) and say what the site was doing. This is a data-
completeness note, not a compliance finding. See `references/thresholds.md`.

Also read the **one-train hold** lines (added September 2026): one train frozen above setpoint
while the other moves. Same treatment — report both ways, and check the reading after each hold
for a jump too large to be real cooling.

### Step 3: Optional — Slack context for your understanding
For any long offline or below-setpoint stretch, you may check `#injection-ops-la` to understand
what happened (turnaround, campaign completion, equipment work). This is for your **chat summary
to Max only** — it does NOT go into the workbook. Search: `slack_search_channels` → channel id →
`slack_read_channel` with `oldest`/`latest` (±1 day around the event). Never invent context; if
the data pattern is self-explanatory (planned turnaround, campaign completion), say so.

### Step 4: Open the Processed workbook and report to Max
```bash
open "outputs/data-analysis/tox-analysis/{Month} CatOx -- Processed.xlsx"
```
Report: date range and reading count; per train, % at/above 600°F, % below, % offline, and peak
outlet; the operational story in plain words (from Step 3); and confirm no swap was needed.
Keep files **local** — never place anything in Drive without Max's explicit go-ahead.

## Threshold and other changeable facts live in `references/catox_config.json`

Drift-prone facts — the outlet setpoint (currently 600°F, the confirmed Intellishare ECO300
manufacturer spec), the offline sentinels, the Processed tab names, the package filenames — are
NOT restated as literals in this document or in code. They live once, in
`references/catox_config.json`, which the script reads at runtime and refuses to run without.
This exists because a stale 650°F figure once survived in code while the true value was 600°F:
duplicating a fact across prose and code is what lets it drift. Change a value there and it
changes everywhere; the script prints the setpoint and its source on every run.

## Train 2 column swap — history, not a standing rule

In the **April 2026** export, Train 2's columns were reversed from their labels and had to be
swapped. That was fixed at the equipment when Train 2 came back from fan service **~May 5–6,
2026** (confirmed in May CatOx Raw: labeled-inlet TIT-2251 ≈ 600°F, labeled-outlet TIT-2252 ≈
850–900°F — correctly labeled). **Current exports need no swap.** Never apply the old swap
blindly: the script verifies orientation empirically every run, which is the safeguard.

## Offline / sentinel convention

Current exports use **`0`** for offline / no reading (not a real temperature). Legacy combined
exports used **`-238`**. Both are converted to blank and shown as grey shaded gaps in the charts.
The script handles both.

## Important principles

- **Match the precedent, not a template.** The deliverable is the two-workbook CatOx package
  above. If a past session's ad-hoc output differs, the precedent (May reporting) wins.
- **Persist learnings here.** Anything decided with Max about ToX reporting (threshold,
  format, interpretation, swap status) gets written back into this SKILL.md and its references
  in the same session — do not leave it only in chat. This skill going stale is what caused a
  wrong first draft in July 2026.
- **Verifier-first, minimal.** The Processed workbook shows only what a verifier needs: two
  charts against the setpoint. Interpretation lives in the Brief.
- **Compliance rests on the interlock**, corroborated by temperature — not on the temperature
  record alone. Below-setpoint during a campaign = absence of VOCs, per the Brief.
