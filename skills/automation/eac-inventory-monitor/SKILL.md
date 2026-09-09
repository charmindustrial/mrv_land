---
name: eac-inventory-monitor
description: >
  Daily headroom check on the BCU and REC inventories in the "Charm EAC Verification
  Inventory tracker" Google Sheet. Fired once a day by launchd, and safe to run ad-hoc.
  Reads the BCU Inventory tab ("Total Attributes Remaining", alert below 200) and the
  RECs Inventory tab ("Volume Remaining", alert below 50), ignoring every row the sheet
  has hidden (hidden means expired or fully drawn down) and any still-visible REC row
  whose Expiry Date has passed. If any active certificate is below its threshold, posts
  one alert to #team-mrv-alerts tagging Max with the certificate and the value. If
  everything is above threshold, it does nothing and stays silent. STRICTLY READ-ONLY on
  the sheet — it never writes anything back. ALWAYS trigger when: a scheduled run fires
  this job, Max says "run the EAC inventory check", "check the BCU/REC inventory",
  "check EAC headroom", or asks about the state of this automation or how much BCU or
  REC volume is left.
---

# EAC Inventory Monitor (BCUs and RECs)

Daily check that Charm has enough BCU and REC headroom left to keep applying against
reporting periods. One pass per run. Silent unless something is low.

## Hard rules

- **Never write to the sheet.** Reading only. No edits, no new tabs, no comments.
- **Never invent a number.** Every figure in the Slack alert comes verbatim from the
  script's output. If the script fails, say so — do not read the sheet by hand and
  substitute your own arithmetic.
- **One alert per run, maximum.** Both inventories go in the same message.
- **Stay silent when all clear.** No "nothing to report" posts. The channel only hears
  from this job when there is something to act on.

## What counts, and what does not

The sheet's hidden rows are the record of what is out of play — Max hides a row once the
certificate has expired or been fully drawn down. The script reads that hidden flag
directly from the Sheets API, so it never has to guess which rows are spent.

A row is **skipped** when either:
- the sheet has the row hidden, or
- (RECs only) its Expiry Date is earlier than today, even if the row is still visible.

Every other row is **checked**. Thresholds live in `config.json`, not in this document.

## Step 1 — Run the checker

```
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
  /Users/maxlavine/.eac-inventory-monitor/check_eac_inventory.py
```

It prints one JSON object and exits 0 when it ran cleanly, 1 when it could not finish.
All settings — sheet ID, tab titles, column headers, thresholds, Slack channel, the
member ID to tag — come from `/Users/maxlavine/.eac-inventory-monitor/config.json`.
The script fails loudly rather than guessing if any of those are missing or no longer
match the sheet.

Read these fields from the output:

| Field | Meaning |
|---|---|
| `ok` | `false` means it could not complete; `error` says why |
| `alert` | `true` means post; `false` means stay silent |
| `reason` | `breach` (something is low), `unreadable` (a value would not parse), or `none` |
| `summary` | Ready-to-use plain lines, one per finding |
| `results[].breaches` | Per certificate: `cert`, `value`, `row` |
| `results[].skipped` | What was ignored and why — useful when Max asks |

## Step 2 — Decide

- `ok: true` and `alert: false` → **do nothing.** Print one status line and stop:
  `NO-ACTION: all inventories above threshold` followed by the `summary` lines.
- `ok: true` and `alert: true` → go to step 3.
- `ok: false` → go to step 4.

## Step 3 — Post the alert

Post to the channel in `slack_channel_id`, tagging `slack_tag_user_id`. Use the numbers
from `breaches` exactly as the script reported them, rounded to two decimals.

Shape (drop whichever inventory has no breach):

```
<@UL2SL4H5H> EAC inventory running low.

*BCUs* — Total Attributes Remaining below 200:
• 13-47206-50000 — 45.12 MT CO2e left (row 16)

*RECs* — Volume Remaining below 50:
• 94-243 — 12.40 MWh left, expires 1/1/27 (row 11)

Sheet: Charm EAC Verification Inventory tracker
```

Link the sheet name to
`https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit`.

If `reason` is `unreadable`, add a line naming the certificate and what the cell
actually contains, so Max can see it is a sheet problem rather than a low balance.

Then print: `ALERTED: <n> BCU breach(es), <n> REC breach(es)`.

## Step 4 — When the check fails

`ok: false` means the job could not answer the question, which is itself worth knowing.
Post to the same channel, tagging Max:

```
<@UL2SL4H5H> The daily EAC inventory check could not run.

Error: <the error string, verbatim>

BCU and REC headroom was not verified today.
```

Then print: `FAILED: <error>`.

Do not attempt to route around the failure by reading the sheet another way in the same
run. A silent fallback hides a broken check. Report it and stop.

## Common causes of `ok: false`

| Error mentions | What happened |
|---|---|
| `Google token missing` or `lacks the spreadsheets scope` | The shared max@ token at `~/.basco-intake/token.json` is gone or was re-issued with narrower access |
| `tab not found` | A tab was renamed — update `tab_title` in `config.json` |
| `column header not found` | A column was renamed; the error lists the headers actually present |
| `invalid_grant` | The token's refresh permission was revoked and needs re-authorizing |

## Files

| Path | What it is |
|---|---|
| `~/.eac-inventory-monitor/config.json` | Every changeable setting. Single source of truth. |
| `~/.eac-inventory-monitor/check_eac_inventory.py` | The check itself. Read-only on the sheet. |
| `~/.eac-inventory-monitor/run.sh` | Runner launchd fires. Safe to run by hand. |
| `~/.eac-inventory-monitor/run.log` | Every pass, appended. |
| `~/Library/LaunchAgents/com.charm.eac-inventory-monitor.plist` | The daily schedule. |

## Changing a threshold or a channel

Edit `config.json`. Do not edit thresholds into this document or into the script —
there must be exactly one place each number lives.
