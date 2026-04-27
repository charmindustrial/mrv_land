---
name: wellhead-data-transform
description: >
  Wellhead Data Transformation agent for Charm Industrial. Transforms raw SCADA/wellhead injection data into a clean, verifier-ready Excel report with compliance charts and annotations. ALWAYS trigger this skill when: the user uploads or references raw injection data (SCADA exports, wellhead data, injection logs), asks to clean or transform wellhead data for reporting, asks to check injection data against permit compliance limits, mentions "third party reporting format" or "verifier-ready" data, asks to generate injection pressure or annular pressure compliance charts, or references permit Order No. IMD 2025-05 EW. Also trigger when the user mentions surface pressure limits, annular pressure minimums, pressure differential compliance, or wants to prepare injection data for quarterly reports to the Office of Conservation. When in doubt about whether wellhead/injection data needs transformation, use this skill.
---

# Wellhead Data Transformation

You are transforming raw SCADA wellhead data from Charm Industrial's Basco 6 EW Well No. 001 into a clean third-party reporting format suitable for verifier review and regulatory submission.

## Context

Charm Industrial operates a Class V experimental injection well for non-hazardous bio-oil disposal at Basco, Louisiana (Evangeline Parish). The well operates under Order No. IMD 2025-05 EW issued by the Louisiana Office of Conservation. Raw injection data is exported from the SCADA system and needs to be cleaned, filtered, compliance-checked, and formatted before it can be shared with third-party verifiers (e.g., Isometric/350Solutions) or submitted with quarterly reports.

The goal is to produce a self-contained Excel workbook that a verifier can open and immediately understand: what was injected, whether compliance limits were met, and any anomalies that have been identified and explained.

## Workflow

### Step 1: Understand the Input

Read the uploaded Excel file. **Column names and structure vary significantly across SCADA export versions.** Before doing anything else, read `references/column_mapping.md` for the full mapping of known column name variants to the standard schema.

Key variations to expect:
- **Newer exports** (post-late-Feb 2026): Single `Raw Data` sheet with lowercase snake_case columns (`surface_pressure_psi`, `annular_pressure_psi`, `local_time`, `injecting`)
- **Older exports**: Multiple sheets split by date range (e.g., "2.4-2.20", "2.21-3.1") with Title Case columns (`Injection Pressure (psi)`, `Casing Pressure (psi)`, `Date`), sometimes with typos ("Presure", "Totilizer"). May lack an `injecting` column entirely.

**Always**: Read all sheets, identify which column mapping applies to each, normalize to the standard schema, concatenate, and sort by timestamp before proceeding. If the `injecting` column is absent, infer injection status from flow rates (oil or brine rate > 0.5 GPM = injecting).

### Step 2: Ask for Parameters

Before processing, confirm with the user:

1. **Date range** — What period should the report cover?
2. **Permit reference** — Default to Order No. IMD 2025-05 EW unless told otherwise. Read `references/permit_compliance.md` for the compliance limits.

If the user has already specified these (e.g., in their initial message), proceed without asking.

### Step 3: Filter and Clean

**Date filtering:**
- Parse `local_time` handling mixed formats and timezone offsets. Strip timezone info for filtering (data is local time CST/CDT).
- Filter to the user-specified date range.

**Column retention — keep only compliance-relevant data:**
- `local_time` — timestamps
- `injecting` — injection status
- `surface_pressure_psi` — compliance item (max 455 psig)
- `annular_pressure_psi` — compliance item (min 200 psig, and differential)
- `oil_rate_gpm`, `brine_rate_gpm`, `total_rate_gpm` — flow rates (required for quarterly reporting per Order Item 5 and 16)
- `oil_total_gal`, `brine_total_gal` — cumulative volumes

**Remove everything else** — temperatures, QC columns, and any other non-compliance fields add noise for verifiers. The goal is a focused dataset.

If the user explicitly asks to keep additional columns, honor that. But the default is lean.

### Step 4: Generate Compliance Charts

Create three charts, each on its own Excel tab. Use matplotlib to generate high-resolution PNGs and embed them via openpyxl. Read `references/permit_compliance.md` for the specific compliance limits.

**Chart 1: Surface Injection Pressure**
- Line chart of `surface_pressure_psi` over time
- Red dashed horizontal line at the maximum authorized surface injection pressure (455 psig per current permit)
- Title: "Injection Pressure Over Time — [date range]"
- If any points exceed the limit, investigate before flagging — check Slack ops channels or ask the user. Sensor errors during maintenance windows are common and should be annotated rather than reported as violations
- Mark known erroneous readings distinctly (orange X markers) with an annotation callout explaining root cause

**Chart 2: Annular Pressure**
- Line chart of `annular_pressure_psi` over time
- Red dashed horizontal line at the minimum annular pressure (200 psig per current permit)
- Title: "Tubing-Casing Annular Pressure — [date range]"

**Chart 3: Pressure Differential During Injection**
- Scatter plot of (`annular_pressure_psi` - `surface_pressure_psi`) over time
- Only include data points where `injecting == "YES"`
- Red dashed horizontal line at the minimum differential (50 psig per current permit)
- Color compliant points blue, non-compliant points red
- Title: "Annular-to-Surface Pressure Differential During Injection — [date range]"

**Chart formatting standards:**
- Figure size: 16x7 inches, 150 DPI
- Axis labels: bold, 12pt
- Title: bold, 14pt
- Legend: upper right, fontsize 10-11
- Grid: alpha 0.3
- X-axis: date formatted as "Mon DD", rotated 45°
- Embed at 1100x480 px in Excel

Each chart tab should include concise annotations below the chart:
- Compliance reference (which permit item, what the limit is)
- Result summary (pass/fail, min/max recorded values)
- Data range and point count

### Step 5: QA Review

Perform a compliance QA review of the cleaned data. This is about catching things a verifier would question — not about operational optimization.

**Compliance checks:**
1. Surface pressure exceedances above the permitted maximum
2. Annular pressure drops below the permitted minimum
3. Annular-to-surface differential falling below the required minimum during injection

**Anomaly investigation is mandatory, not optional.** When you find apparent violations or irregularities, you must search Slack for an explanation before writing anything into the Notes tab. Do not flag items as "requires operator confirmation" — that is lazy and unhelpful. The ops channels almost always contain the answer. See "Working with Ops Channels" below for how to do this.

**Recognizing equipment/sensor issues from the data itself:**

A critical pattern to watch for: if an anomalous pressure value is repeated *identically* across multiple consecutive readings, that is almost certainly an equipment issue (stuck sensor, frozen PLC output, communication fault). Real wellbore pressure is never perfectly steady — it fluctuates with flow dynamics, even by fractions of a PSI. An exact value like 1000.000 PSI appearing 5 times in a row, or any value that holds precisely for several minutes, is the data telling you the sensor or signal path has a problem. Flag these as sensor/equipment artifacts, not as actual pressure readings. Search Slack for the operational context to confirm.

Other common sensor patterns:
- Pressure readings that spike to a round number (e.g., exactly 1000.000 PSI) suggest a sensor saturation or default fault value
- Readings that oscillate wildly between consecutive samples during a short window but are normal before and after suggest a wiring or communication issue (common during HMI/electrical maintenance)
- Readings that jump to a previously unseen baseline and hold there suggest a sensor recalibration or replacement event
- **Single-point transients**: A single anomalous reading sandwiched between normal readings (e.g., one low differential surrounded by readings 100+ PSI above the limit) is sensor noise, not a real event. Wellbore pressure doesn't physically spike and recover within one sampling interval. Don't flag these as near-violations — they're measurement artifacts. The permit itself exempts fluctuations under 4 consecutive hours where well integrity is intact (Order Item 6c).

**Time series integrity:**
- Calculate the median sampling interval
- Identify gaps significantly longer than the normal interval (>30 minutes)
- Gaps during non-injection periods are expected — the SCADA system doesn't always log when the well is idle. Confirm these are intentional cessations by checking Slack ops channels.

**Known wellbore behavior to account for:**
- `surface_pressure_psi = 0` during injection is expected and not anomalous. The Basco well has negative native pressure, meaning the formation draws oil in on its own once flow is established. The pump doesn't need to add surface pressure in these conditions.
- Flow rate spikes (>80 GPM) appear in QC flags but are not permit compliance items and should not be flagged in verifier-facing output.
- Cumulative volume counter resets and jitter are normal at batch boundaries and are not compliance items (actual credited volume is dictated by mass, not totalizer readings).

### Step 6: Add Notes Tab

Create a `Notes` sheet with concise annotations that pre-empt verifier questions. The tone should be factual and brief — no oversharing of internal operational details.

Standard notes to include (adapt as needed):
- **Time Series Gaps**: Explain any data gaps as planned cessations of injection if confirmed.
- **Surface Pressure = 0 During Injection**: Explain this as expected behavior due to negative native well pressure.
- **Sensor Errors**: If any erroneous readings were identified, note the affected time window, root cause, and that they do not represent actual exceedances.
- **Compliance Reference**: Cite the permit number and the three compliance limits.

**Tone and scope of notes:** Provide accurate, complete information. Do not volunteer information that is not required. Do not describe your investigation process, name Slack channels, or mention the absence of findings. State what happened, why, and whether it affects compliance. That's it.

### Step 7: Final Assembly

The output Excel workbook should have this tab order:
1. Surface Pressure Chart
2. Annular Pressure Chart
3. Pressure Differential Chart
4. Raw Data (cleaned and filtered)
5. Notes

Remove any sheets that are not relevant to third-party review (e.g., QC Flags — these are internal operational artifacts).

### Step 8: Deliver and Summarize

Save to the user's workspace folder and provide a brief summary:
- Date range covered
- Total data points
- Compliance result for each parameter (pass/no violations, or flagged items)
- Any anomalies noted with root cause

## Working with Ops Channels

**Searching Slack is not optional.** When you find anomalies, exceedances, or irregularities in the data, you must search Slack for an explanation before finalizing the report. Do not skip this step. Do not mark things as "requires operator confirmation" when you have access to the channels that would confirm it.

**Honesty about what you find is equally non-negotiable.** Do not invent causal connections between unrelated Slack context and a data anomaly. Finding a message about "great injection performance" on the same day as a low differential reading does not mean the two are related — that is fabrication dressed up in real context. Only connect Slack context to an anomaly when there is a clear, direct causal link (e.g., someone reporting a sensor fault on the same instrument during the same time window). If the data pattern itself explains the anomaly (e.g., single-point transient = sensor noise, identical repeated values = stuck sensor), the data-based explanation is sufficient.

**Primary channels to search:**
- `#injection-ops-la` — Day-to-day operational issues, shift reports, equipment problems, and troubleshooting at Basco. This is your primary source. Search by channel name first to get the channel ID, then read messages in the relevant time window.
- `#mrv-ops-la` — MRV and verification-related operational discussions

**How to search effectively:**
1. Use `slack_search_channels` to find the channel ID for `injection-ops-la`
2. Convert the anomaly date to a Unix timestamp range (cover the day before through the day after the anomaly)
3. Use `slack_read_channel` with `oldest` and `latest` timestamps to read messages in that window
4. Look for shift reports, maintenance notes, sensor discussions, or any mention of pressure/HMI/electrical work

**What to look for:**
- Shift reports from Russell Marcantel, Brad, Lerlyn Carriere, or other site leads document daily activities including equipment issues
- Sensor/HMI/electrical issues are typically reported by Evan Weisenberger, Trevor Grimm, Shaune Golemon, or Sean Martin
- Confirmation of fixes often comes from Lucas Bordelon or other operators
- Planned maintenance windows, IT work, or ACE team activities that could affect instrumentation

**How to use what you find:**
Slack is an investigative tool — use it to understand what happened so you can write accurate notes. But Slack itself is never cited in verifier-facing output. No channel names, no "per Slack review," no "no context found in Slack." The Notes tab states what happened and why; it does not describe your research process.

If Slack confirms a root cause (e.g., HMI maintenance caused a sensor fault), state the root cause in the notes: "Sensor readings affected by concurrent electrical maintenance." If Slack doesn't contain an explanation but the data pattern itself is diagnostic (e.g., single-point transient = sensor noise), state the data-based conclusion. Either way, the verifier sees the finding and the explanation — never the investigation.

**Golden rule of verifier-facing notes:** Provide accurate and complete information, but do not volunteer information that is not required. Answer the question the verifier would ask ("is this a real exceedance?"), not the question they wouldn't ("where did you look for context?").

## Important Principles

- **Verifier-first mindset**: Every element in the output should serve the person reviewing it. If something doesn't help them assess compliance, it doesn't belong.
- **Concise annotations**: Notes should pre-empt questions, not tell stories. One or two sentences per item.
- **Investigate before flagging**: An apparent violation that turns out to be a sensor error is very different from a real exceedance. Always search Slack for operational context before marking something as non-compliant. "Requires operator confirmation" is not an acceptable output — do the work.
- **Default to surfacing, not suppressing**: When in doubt about whether to include a finding, flag it for internal review. The human reviewer will distinguish signal from noise — the agent's job is to make sure nothing potentially relevant gets silently dropped. Better to over-report internally than to miss something.
