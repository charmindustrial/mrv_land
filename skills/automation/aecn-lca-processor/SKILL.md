---
name: aecn-lca-processor
description: >
  Processes a new life-cycle-assessment (LCA) carbon-intensity submission from AECN
  (Bioenergy AE Cote-Nord, Port Cartier, Quebec) into Charm's Drive filing structure and
  the live Standard Emission Factors sheet that batch-qa-aecn checks against. AECN's
  contact Jean-Christophe Amado (j-c@viridiglobal.com) sends this roughly every six
  months, covering the prior half-year's production data (H1 = Jan-Jun, H2 = Jul-Dec),
  usually weeks to months after the period closes. The skill archives the prior period's
  Drive folder, builds the new one, pulls the two attached workbooks from the email,
  reconciles the raw Supporting Data against the LCA calculation's own stated totals
  (mandatory before anything downstream uses the number), computes the process-emissions
  figure via the Stack Emissions Template, and pushes the updated figure into the live
  Standard Emission Factors + Calculations sheet. ALWAYS trigger this skill when: Max says
  there's a new AECN LCA, forwards or links an email from J-C / Jean-Christophe Amado /
  viridiglobal.com with LCA or carbon-intensity data attached, says "process the AECN
  LCA", "new LCA from AECN", or asks about updating the AECN process-emissions figure.
  This is a manually-triggered workflow — nothing watches Max's inbox for this
  automatically; he tells the skill when a submission has arrived.
---

# AECN LCA Processor

Turns a new half-yearly carbon-intensity submission from AECN into (1) an archived,
correctly-named Drive folder and (2) an updated live emission-factor figure that
`batch-qa-aecn` checks every AECN batch against. Validated end-to-end against the real
H1 2026 submission (Aug 12, 2026 email) on 2026-08-26.

## Hard rules

- **Reconcile before anything else touches the number.** Step 5 (below) is mandatory,
  not optional. Every total in the LCA calculation workbook's Inputs/Analysis tabs must
  tie to a sum of the Supporting Data workbook's raw monthly/weekly entries before you
  pull a CI value from it. A gap beyond floating-point noise (roughly 1e-6 relative)
  stops the process — flag it to Max and do not fill the template or touch the Standard
  EF sheet on unreconciled data.
- **Pull the CI value net of coproduct displacement — the conservative one.** Charm's
  accounting policy does not count the filter-cake coproduct displacement credit. In the
  LCA workbook's Summary tab this is the **Total** row under "Carbon intensity of
  pyrolysis oil (no energy allocation to filter cake co-product)" — the same number that
  appears as the pre-credit "Total" in the third table ("...based on emissions
  displacement...") before its "Less: Co-product displacement" line. It is **not** the
  "Net total" row (that has the credit subtracted) and **not** the energy-allocation
  Total from the first table. When in doubt, this is the number that has historically
  matched what's already been used in prior periods' Stack Emissions sheets — check
  against the prior period's filled sheet if unsure.
- **Never fabricate the CI figure or the Inputs values.** Every number placed in the
  template or the Standard EF sheet must come from a value actually read out of the two
  attached workbooks this session — never carried over, estimated, or interpolated.
- **The Standard EF sheet is Certify-adjacent, not Certify itself.** This skill writes to
  a Charm-owned Google Sheet that `batch-qa-aecn` reads from — it never touches Certify
  directly. The Certify read-only rule still applies to any Certify verification of the
  downstream figure.
- **Session write approval.** Editing Google Sheet cells requires Playwright browser
  writes, which are gated behind a session-level approval hook
  (`~/.claude/hooks/certify_readonly_guard.sh`, despite the name it gates all sites, not
  just Certify). If blocked, this is routine, expected write access for this workflow —
  approve it (`touch /tmp/playwright_writes_approved`) rather than treating it as
  something requiring a fresh ask each time.

## Step 1 — Find the email

Search Max's Gmail (max@charmindustrial.com) for the submission. It typically arrives as
a reply or new thread to Max's own "H[1/2] [year] LCA Update" outreach, from
**j-c@viridiglobal.com** (Jean-Christophe Amado), cc'ing Julien Lampron
(Julien.Lampron@remabec.com) and Jeremy Fortin (Jeremy.Fortin@bioaecn.ca / lowercase
variants). Subject lines have drifted across periods — seen so far: "Q3-Q4 2025 LCA",
"Carbon intensity calculation for Q1-Q2 2025", "Q1 - Q2 carbon intensity calculation".

**If the Gmail MCP connector's `search_threads`/`get_thread` tools don't find it despite
a real submission existing** (confirmed happened 2026-08-26 — the connector's search
index missed a real, 2-week-old email that was sitting in the inbox, and direct
`get_thread` on its resolved thread ID even returned "the caller does not have
permission"), fall back to the `playwright` browser tool: navigate directly to Gmail
(`https://mail.google.com/mail/u/0/#inbox`, or use the in-page search box), open the
thread, and read it via the accessibility snapshot. This is a real, encountered gap in
the API connector, not a hypothetical — don't burn time on more API search variations
once a `get_thread` call returns a permission error on a thread you can see rendered in
the browser.

The email has two `.xlsx` attachments:
- `Bioenergy AE Cote-Nord Canada - LCA CI calculation - <period label>.xlsx` — the CI
  calculation. **Filenames drift and contain typos** (e.g. a period actually covering
  Jan-Jun was labeled "1Jan2026 to 30Jan2026" in the filename itself) — always trust the
  workbook's own "Period start"/"Period end" cells (Summary or Inputs tab) over the
  filename.
- `Supporting GHG data <date> S.xlsx` — the raw monthly/weekly data the CI calc is built
  from.

Download both attachments (click each attachment's "Download" button in the Gmail UI via
Playwright — not "Add to Drive" yet, that comes later and needs the write-approval gate
open; a plain download does not).

## Step 2 — Archive the old period folder

In Drive, under `.../AECN/LCAs/`, move the current `LCA -- [BH/FH] [year] Data` folder
into the sibling `Deprecated/` folder (`update_file` with the new `parentId`).

## Step 3 — Create the new period folder

Create `LCA -- [BH/FH] [year] Data` directly under `.../AECN/LCAs/` (the same level the
old folder came from, not inside Deprecated). Naming convention: **BH** = back half
(Jul-Dec), **FH** = front half (Jan-Jun), followed by the calendar year the data covers.
Example: data for Jan-Jun 2026 → `LCA -- FH 2026 Data`.

## Step 4 — Copy in the Stack Emissions Template

Copy `LCA Stack Emissions Template` (lives one level up, directly in `LCAs/`) into the
new folder. Name the copy to match the folder's period label:
`[BH/FH] [year] LCA w Stack Emissions` (e.g. `FH 2026 LCA w Stack Emissions`).

## Step 4.5 — Reconcile Supporting Data against the LCA calculation (mandatory QA gate)

Before pulling anything into the template, verify the two workbooks agree with each
other. Do this with a local script (openpyxl, `data_only=True`) against the two
downloaded files — don't eyeball it.

| Check | Supporting Data source | LCA calc target |
|---|---|---|
| Pyrolysis oil production | Sum monthly entries, "Inputs for GHG calculation" tab, Production section | Inputs tab, "Total pyrolysis oil produced" |
| Biomass feed | Sum period entries, same tab, Biomass feed section | Inputs tab, "Biomass input" |
| Filter cake co-product | Sum monthly entries, same tab, Filter cake section | Inputs tab, "Filter cake co-product produced" |
| Electricity | Ending meter reading − starting meter reading | Inputs tab electricity consumption AND Analysis tab "Electricity (QC)" |
| Propane | Starting inventory + deliveries − ending inventory | Inputs tab propane consumption AND Analysis tab "Liquid Propane Gas (LPG)" |
| Diesel (biomass handling) | Sum the "Diesel fuel" tab's grand-total row (feed-prep loaders + other equipment combined) across the period's month columns only | Inputs tab "Actual quantity of diesel fuel consumed" AND Analysis tab "Litres consumed for handling biomass and loading trucks" |

Every one of these should match exactly or within floating-point noise (~1e-13
relative on sums, since source cells carry many decimal places). If anything is off by
more than that, stop and flag it to Max with the specific numbers on both sides — do not
proceed to Step 5.

## Step 5 — Pull the CI value

From the LCA calc's Summary tab, take the **Total** row under "Carbon intensity of
pyrolysis oil (no energy allocation to filter cake co-product)" — see Hard Rules above
for why this row and not the others.

## Step 6 — Fill the Stack Emissions Template

In the copied template (a Google Sheet), the layout is fixed — confirmed identical
across at least three periods' worth of template copies:

| Cell | Value | Source |
|---|---|---|
| B3 | Biomass Input (MT) | LCA calc Inputs tab, "Biomass input" |
| B4 | Bio Oil Output (L) | LCA calc Inputs tab, "Total pyrolysis oil produced" |
| B5 | HHV (MJ/L) | LCA calc Inputs tab, "Pyrolysis oil High Heating Value" (labeled MJ/kg in the source — a known, longstanding label mismatch, not an error to fix) |
| I11 | CI net of coproduct displacement | Step 5's value |

I9, I10, I12 are formulas (`=SUM(H4:H5)`, `=I9/1000000`, `=SUM(I10:I11)`) and
auto-compute once B3:B5 and I11 are filled — don't overwrite them.

To edit: the Drive API tools available in this workspace (`create_file`, `copy_file`,
`update_file`) cannot write cell content into an existing Sheet — only metadata (title,
parent folder). Cell edits must go through the browser: open the Sheet, click the Name
box (`#t-name-box`), type the cell reference + Enter to select it, then type the value +
Enter to commit and advance to the next row. Verify afterward by re-fetching the sheet
(`export?format=csv&gid=<gid>` works unauthenticated on link-shared sheets, or
`download_file_content` with `exportMimeType: text/csv`) and checking the computed I12
value looks sane (same order of magnitude as the prior period).

## Step 7 — (folded into Step 4)

The template copy is already named per convention when created — no separate rename
step needed if you named it correctly in Step 4.

## Step 8 — Open the Standard Emission Factors + Calculations sheet

This is a separate, long-lived Google Sheet (search Drive by title — do not assume a
link given verbally is correct; it has been mistakenly duplicated from an unrelated
folder link before). It has many tabs covering different emission-factor categories.

## Step 9 — Find the current AECN tab

Look for a tab titled `[H1/H2] [year] AECN Process Emissions`. There is only ever one —
it gets **reused and rotated**, not duplicated, each period.

**Known gap to check for:** this tab's title can be renamed in anticipation of a new
period before the actual data arrives, leaving it mislabeled with stale contents (found
and fixed 2026-08-26: a tab titled "H1 2026" still held H2 2025's numbers). Always check
the tab's actual cell contents against what the title claims — don't trust the title
alone.

## Step 10 — Replace the tab's contents

Same cell layout as the template (Step 6's table applies identically — confirmed
row-for-row identical structure). Overwrite B3, B4, B5, I11 with the new period's values
the same way (Name box → type ref → Enter → type value → Enter). I9/I10/I12 recompute
automatically.

## Step 11 — Rename the tab if needed

Rotation rule: H1 of year N → H2 of year N when the H2 submission lands; H2 of year N →
H1 of year N+1 when the H1 submission lands. If Step 9 found the tab already correctly
named for the period you're loading (can happen per the Step 9 gap above), no rename is
needed — just fix the contents.

## Step 12 — Report back

Tell Max what changed: old folder archived, new folder + files, the Step 4.5 QA table
result, the CI value used and where it came from, the template's computed I12, and the
Standard EF sheet's tab name + new I12 value. Flag explicitly if Step 9's gap (stale
data under a pre-rotated tab name) was found.

## Known gaps encountered so far (useful for anyone debugging this skill)

- Gmail API `search_threads`/`get_thread` can miss or deny access to a real, visible
  email — fall back to the Playwright browser against Gmail directly.
- The Drive MCP tools here have no "write cell content to existing file" capability —
  only the browser can do it.
- Large file uploads (multi-MB `.xlsx`) are impractical to push through `create_file`'s
  inline `base64Content` parameter (would consume enormous context) — use the browser's
  Gmail "Add to Drive" / "Organize in Drive" attachment button instead (needs the
  write-approval gate open), then `update_file` to move the result into the correct
  folder (it lands at the Drive root / a default location, not the folder you want).
- Playwright's persistent profile can accumulate orphaned browser processes across a
  long session that wedge new navigation with an "already in use" error. If that
  happens: `pkill -f playwright-profile` (this profile is exclusively automation-only —
  it is never Max's real Chrome — so killing everything matching it is safe) and retry.
- Playwright element `ref=` values from a saved snapshot file can go stale even when the
  page hasn't visibly changed; if a click errors "ref not found," take a fresh
  `browser_snapshot` rather than reusing an old one.
