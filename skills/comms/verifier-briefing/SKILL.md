---
name: verifier-briefing
description: >
  Proactive verifier communication workflow for Charm Industrial. Drafts briefings to 350Solutions (Tim Hansen, tim@350solutions.com) and Isometric (Tom Sellers, tom.sellers@isometric.com) about Charm's ongoing MRV workstreams. Two modes: quarterly (comprehensive quarterly update on what changed and what's in flight) and pre-verification (targeted memo before a verification window opens). Output is always a Gmail draft + Slack DM to Max — never sends autonomously. ALWAYS trigger when Max says "run the quarterly briefing," "draft the verifier briefing," "pre-verification memo," "brief Tim," "prepare a briefing for 350Solutions," or invokes this from a scheduled cron. Do NOT trigger for one-off Slack messages or quick email replies — those don't need this workflow.
---

# Verifier Briefing

Proactive communication to 350Solutions and Isometric about Charm's longer-horizon MRV workstreams. The problem this solves: Charm has ongoing methodology work, data quality initiatives, and operational changes that Tim Hansen (VVB) only encounters cold at verification time — leading to issues that could have been pre-empted. This skill drafts the briefings that close that loop.

## HARD RULE — NO AUTONOMOUS SENDS. EVER.

Output is always a draft. The last step is always a Slack self-DM to Max with the Gmail draft link. Max reviews, edits, and hits send himself. This rule has no exceptions. Do not attempt to send, share, or transmit anything.

## Contacts

- **Tim Hansen (VVB, 350Solutions):** `tim@350solutions.com`, Slack `U04RP46UVNJ`
- **Tom Sellers (Isometric, Head of Registry Operations):** `tom.sellers@isometric.com`, Slack `U08G9RVP3FV`
- **Max Lavine (Charm):** `max@charmindustrial.com`, Slack `UL2SL4H5H`

---

## Mode 1 — Quarterly Briefing

**When invoked:** Scheduled cron fires quarterly (15th of January, April, July, October) OR Max says "quarterly briefing" / "run the quarterly briefing."

**Purpose:** Keep Tim and Tom informed on Charm's MRV workstreams on a cadence, so verification cycles aren't the first time they hear about methodology evolutions or data quality initiatives.

**Lookback window:** 90 days from today.

### Step 1 — Load context

Read in parallel:

1. **Knowledge base:** `knowledge-base/Charm_Isometric_Knowledge_Base.md` — institutional context, GHG statement history, verification history.
2. **Recent workspace outputs:** List files modified in the last 90 days under `outputs/deliverables/isometric/` and `outputs/mrv-operational-documents/`. Skim any that look methodology- or protocol-relevant.
3. **Recent Slack activity:** Read `#ext-proj-charm-350-isometric` (channel ID `C095G0XRHFA`, Isometric workspace) and `#mrv-protocol` (channel ID `C05C1867GSV`) for the last 90 days. Surface methodology decisions, data quality discussions, operational changes.
4. **MRV standup run log:** Read `outputs/digests/mrv-standup/run-log.jsonl` for a sense of Watch-tier activity over the quarter.
5. **Certify (read-only):** Navigate to `registry.isometric.com` via Playwright and check the current GHG statement status + any open/recently closed issues. Follow the Certify read-only hard rule — no writes of any kind.

### Step 2 — Draft content

Structure the briefing as a concise email (aim for 400–700 words in the body):

```
Subject: Charm MRV Quarterly Update — Q[X] [YYYY]

Hi Tim (and Tom),

[One sentence on what this is — a standing quarterly update on Charm's longer-horizon MRV workstreams so they're not a surprise at verification time.]

**What changed this quarter**
[Bullet list: methodology updates, data source changes, operational changes at injection sites, new oil types or delivery modes, protocol questions resolved. One bullet per item, max 2 sentences each. Only items with actual substance — don't pad.]

**What's in flight**
[Bullet list: workstreams Tim will encounter in upcoming verification cycles. The embodied emissions amortization / true-up work is the canonical example of what belongs here — things Charm is actively working on that will affect MRV. Include expected timeline if known.]

**Open questions / items for discussion**
[Optional. Only include if there are genuine open questions where Tim's input would be useful. Skip this section if empty.]

[Closing line — one sentence max. Something like: "Happy to discuss any of this on a call or in the channel." Do not add throat-clearing.]

Max
```

Apply the brief-writer compliance language rules: no throat-clearing, no volunteering context not asked for, active voice, omit needless words. This is a relationship-maintenance communication, not a compliance doc, so the collegial register applies — but keep it tight.

### Step 3 — Create Gmail draft

Use `mcp__claude_ai_Gmail__create_draft` with:
- `to`: `tim@350solutions.com`
- `cc`: `tom.sellers@isometric.com`
- `subject`: `Charm MRV Quarterly Update — Q[X] [YYYY]`
- `body`: The full drafted content from Step 2

### Step 4 — Self-DM Max

Use `mcp__claude_ai_Slack__slack_send_message` to channel `UL2SL4H5H` (Max's self-DM) with:

```
*Quarterly verifier briefing draft ready for review.*

To: tim@350solutions.com | Cc: tom.sellers@isometric.com
Quarter: Q[X] [YYYY] | Lookback: [start date] → [today]

*What's in the draft:*
• [3–5 bullet summary of what the brief covers]

Find it in Gmail drafts. Review, edit, and send when ready. I don't send on your behalf.
```

---

## Mode 2 — Pre-Verification Memo

**When invoked:** Max says "pre-verification memo," "brief Tim before this verification," "prepare the pre-verification brief," or similar. Also invocable manually when Tim signals a verification window is opening.

**Purpose:** Get Tim up to speed on what's changed since the last verification before he opens Certify, so he can file issues faster and with more context — and so fewer surprises emerge during the cycle.

### Step 1 — Load context

Read in parallel:

1. **Knowledge base:** `knowledge-base/Charm_Isometric_Knowledge_Base.md` — GHG statement history, recent verification periods.
2. **Recent batch QA outputs:** List and skim files under `outputs/qa/` modified in the last 60 days. Look for recurring QA flags, methodology edge cases, or known data quality issues.
3. **Recent workspace outputs:** Skim `outputs/deliverables/isometric/` and `outputs/mrv-operational-documents/` for anything since the last verified GHG statement date.
4. **Certify (read-only):** Check the current verification window's batch list, open issues, and recent issue history. Follow the Certify read-only hard rule.
5. **`#ext-proj-charm-350-isometric` Slack:** Read recent messages since the last GHG statement close date for any unresolved threads or outstanding asks.

### Step 2 — Draft content

Structure as a short memo (aim for 300–500 words):

```
Subject: Charm Pre-Verification Brief — [Reporting Period, e.g., "Apr–May 2026"]

Hi Tim,

[One sentence: here's what's changed since last verification and what to expect in this cycle.]

**Changes since last verification**
[Methodology updates, new data sources, operational changes, new emission categories. One bullet per item. Only material changes.]

**What's in scope this cycle**
[Brief summary: oil types, delivery modes, batch count if known, injection sites. Helps Tim calibrate scope before he opens Certify.]

**Known items / heads-up flags**
[Anything Charm knows will look unusual or generate questions — flag it here with an explanation so Tim doesn't need to file an issue. The embodied emissions situation from May 2026 is the canonical example: if we'd flagged it pre-verification, ISS-34 and ISS-36 would have been clean before the cycle opened.]

**Open questions**
[Optional. Only if there's something Charm genuinely wants Tim's input on before verification.]

Max
```

Same tone rules as Mode 1 — collegial but tight.

### Step 3 — Create Gmail draft

Use `mcp__claude_ai_Gmail__create_draft` with:
- `to`: `tim@350solutions.com`
- `cc`: `tom.sellers@isometric.com`
- `subject`: `Charm Pre-Verification Brief — [Reporting Period]`
- `body`: The full drafted content from Step 2

### Step 4 — Self-DM Max

Use `mcp__claude_ai_Slack__slack_send_message` to channel `UL2SL4H5H` with:

```
*Pre-verification memo draft ready for review.*

To: tim@350solutions.com | Cc: tom.sellers@isometric.com
Reporting period: [period]

*What's in the draft:*
• [3–5 bullet summary]

Find it in Gmail drafts. Review, edit, and send when ready. I don't send on your behalf.
```

---

## What NOT to include in either mode

- Charm's internal business strategy or commercial plans (pricing, customer mix, burn rate)
- Specific batch-level data not yet submitted to Certify
- Internal disagreements or unresolved positions — only surface things Charm has decided
- Speculation about what Isometric or 350Solutions will do — state Charm's position, not predictions
- Anything Max has flagged as sensitive in the `#ext-proj-charm-350-isometric` channel or in prior briefs

When in doubt about whether something is too sensitive to include, leave it out and flag it in the self-DM to Max as "omitted — check if you want to add."

---

## Certify Read-Only Rule (applies to both modes)

Certify (`registry.isometric.com`) is read-only. Use Playwright for navigation and snapshots only. No typing, no form fills, no button clicks except tab/accordion navigation. If you need information that requires a write to surface (e.g., a draft comment), note it in the self-DM to Max instead.

---

## Output destination

Drafts live in Gmail (no local artifact). Run logs (if any) append to `outputs/comms/verifier-briefing/run-log.jsonl`.

```jsonl
{"date":"2026-07-15","mode":"quarterly","quarter":"Q3 2026","lookback_start":"2026-04-15","draft_created":true,"duration_s":62}
```
