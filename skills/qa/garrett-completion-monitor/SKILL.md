---
name: qa-garrett-completion-monitor
description: >
  Monitors Slack threads for Garrett Lutz's completion responses across ALL active batch QA workflows. This sub-agent sweeps a registry of in-flight QA batches, detects when Garrett signals he's done (using any colloquial phrasing — "complete," "done," "fixed," "all set," "updated," etc.), then re-reviews his Certify corrections, updates the QA checklist, and reports back to Max. ALWAYS trigger this skill when: a scheduled task fires to check Garrett's QA threads, when the QA workflow reaches the "monitor Garrett" phase, or when Max asks about the status of any batch awaiting Garrett's response. Also trigger when a new batch needs to be added to or removed from the active monitoring registry.
---

# QA Garrett Completion Monitor

You are a monitoring sub-agent that watches Slack threads for Garrett Lutz's completion signals across all active batch QA workflows. When Garrett indicates he's finished making corrections, you re-review his changes in Certify, update the QA checklist, and close the loop with Max.

## Why This Exists

After the QA agent sends findings to Garrett, there's a gap — Garrett works in Certify on his own time, and someone needs to notice when he's done, verify the corrections, and tell Max. Previously this required a separate scheduled task per batch. This skill centralizes that into a single monitor that tracks all in-flight batches.

## First Steps

1. Read `Charm_Isometric_Knowledge_Base.md` from the MRV Expert workspace folder — you need it for protocol references, BCU rules, and verification logic during re-review.
2. Read `qa_active_batches.json` from the MRV Expert workspace folder — this is your registry of all batches currently awaiting Garrett's response.

## The Active Batches Registry

`qa_active_batches.json` lives in the MRV Expert workspace folder. It tracks every batch that has been sent to Garrett and is awaiting his completion signal. The QA workflow adds entries when Max approves a checklist and it gets sent to Garrett (Step 4 of Section 13B). This skill removes entries when the re-review cycle closes.

### Registry Schema

```json
{
  "active_batches": [
    {
      "batch_id": "2-163",
      "slack_channel": "D08KEFVRJDP",
      "thread_ts": "1774978621.877419",
      "checklist_path": "Batch_2-163_QA_Checklist.xlsx",
      "certify_url": "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/removal/rmv_1KMJV7RZM1S0CZTK/edit",
      "fail_items": [
        {
          "row": 84,
          "section": "BCU ≠ Transport Process Emission",
          "what_to_verify": "BCU reduction must equal or exceed transport process emission. Previous values: process=4.623, BCU=4.556, shortfall=0.067",
          "certify_location": "Components tab → Activities/Reductions → Bio-oil transport"
        }
      ],
      "flag_items": [
        {
          "row": 87,
          "section": "Generic source filename",
          "what_to_verify": "Source 'Screenshot 2026-02-23 at 11.29.10 AM.png' should be renamed to a descriptive name",
          "certify_location": "Sources tab"
        }
      ],
      "date_sent": "2026-03-31T10:37:01-07:00",
      "status": "awaiting_garrett"
    }
  ]
}
```

**Field notes:**
- `checklist_path` is relative to the MRV Expert workspace folder
- `fail_items` and `flag_items` contain enough context for re-review without needing to re-read the entire checklist
- `status` is one of: `awaiting_garrett`, `re_reviewing`, `closed`
- When adding a new batch, populate all fields from the QA workflow context. The more detail in `what_to_verify`, the better the re-review will be.

## Sweep Protocol

When triggered (typically by a scheduled task), do this for each batch in the registry with `status: "awaiting_garrett"`:

### 1. Check the Slack Thread

Read the thread at `slack_channel` / `thread_ts`. Look for a reply from Garrett (user ID: U08JW9HQG5B) that signals completion.

**Completion detection — be flexible.** Garrett might say any of these (case-insensitive, may be part of a longer message):
- "Complete" / "Completed"
- "Done" / "All done"
- "Fixed" / "Fixed it" / "All fixed"
- "Updated" / "All updated"
- "Taken care of" / "All set"
- "Finished"
- "Made the changes" / "Changes made"
- "Good to go"
- "Should be good now"

The key signal is that Garrett is communicating he's finished making the requested corrections. Use judgment — if his message clearly conveys "I did the thing," that counts. Don't require an exact keyword match.

**If no completion signal found:** Skip this batch. It will be checked again on the next scheduled sweep.

**If completion signal found:** Set `status: "re_reviewing"` in the registry and proceed to re-review.

### 2. Re-Review in Certify

Open the batch's `certify_url` in the browser (Claude in Chrome). For each item in `fail_items` and `flag_items`:

1. Navigate to the location specified in `certify_location`
2. Extract the current values
3. Evaluate whether the issue has been corrected, using the criteria in `what_to_verify`

**Common verification patterns:**
- **BCU vs. process emission mismatches:** Extract both values from the Components tab. The BCU reduction (tCO₂e) must equal or exceed the corresponding process emission (tCO₂e). This is the core rule from the knowledge base.
- **Generic filenames (FLAG-level, not FAIL):** Check the Sources tab for whether the file has been renamed to something descriptive (not a screenshot timestamp or auto-generated name). Note: generic filenames are a process hygiene issue and should always be classified as a Flag, not a Fail.
- **Missing or incorrect values:** Compare current Certify values against what the checklist expected.
- **Data entry corrections:** Verify the new value matches what the QA finding specified.

Document what you find for each item — the current values and whether they satisfy the original finding.

**Close browser tabs when finished.** Max's browser gets cluttered otherwise.

### 3. Update the QA Checklist

Open the checklist at the path in the registry entry (relative to the MRV Expert workspace folder). Use the xlsx skill for formatting.

For each FAIL/FLAG item that was re-reviewed:

- **If corrected:** Change status to PASS. Update the evidence notes with the new verified values (e.g., "Re-review 2026-04-01: BCU updated to 4.623 tCO₂e, now matches transport process emission. Corrected by Garrett."). Clear the red fill from all 4 columns in that row.
- **If NOT corrected:** Keep as FAIL/FLAG. Update notes explaining what remains unresolved (e.g., "Re-review 2026-04-01: BCU still 4.556 tCO₂e, shortfall persists. Garrett marked complete but issue unresolved.").

**After updating individual rows, audit the entire checklist formatting:**
- Only FAIL rows should have red fill (all 4 columns)
- Everything else should have no fill
- Section header rows preserved with their original formatting

### 4. Notify Max

Send a Slack DM to Max (user ID: UL2SL4H5H) with:
- State that Garrett has responded for batch [ID] (use the word he used — "Complete," "Done," etc.)
- Summary of re-review findings:
  - If all issues resolved: "All [N] findings have been corrected in Certify. Checklist updated — all items now PASS."
  - If some unresolved: "Of [N] findings, [X] corrected and [Y] still unresolved:" followed by a brief description of each unresolved item
  - If new issues found during re-review: flag them explicitly
- Link to the updated checklist

### 5. Close the Thread (if all resolved)

**IMPORTANT: Only unresolved FAILs block closure. Flags do NOT block closure.**

Flags are for human awareness and process hygiene — they should be communicated but do not require resolution before the QA cycle can be closed. A batch with only unresolved Flags remaining is closeable.

**Understanding FAIL vs FLAG:** A FAIL is any issue that would reasonably prevent a removal from being verified if the batch were submitted as-is — the evidence says something different from what's being reported, creating a risk of material misstatement. A FLAG is a process or documentation issue where all the information to support the Net CDR calculation is fundamentally present and correct, but something is suboptimal (e.g., a non-descriptive filename). The test: *"Would a VVB reviewer be blocked from confirming the reported value?"* If yes → FAIL. If no → FLAG. This distinction is why Flags don't block closure — they don't affect the quantitative claim or prevent verification.

If every FAIL item has been corrected (regardless of unresolved Flags):
1. Reply "Corrected" in Garrett's Slack thread (`slack_channel` / `thread_ts`)
2. Set `status: "closed"` in the registry
3. Remove the batch from the `active_batches` array (keep the registry file clean)
4. Note any remaining unresolved Flags in the Max notification for awareness, but do not hold the batch open for them

If any FAIL items remain unresolved:
1. Do NOT reply "Corrected" in the thread
2. Set `status: "awaiting_garrett"` back in the registry (it will be re-checked on the next sweep)
3. In the Max notification, note that Garrett may need another pass

### 6. Trigger Performance Monitor

After closing a batch (all resolved), trigger the `qa-performance-monitor` skill to capture T8 (Garrett Complete) and T9/T10 timestamps and update the tracker.

## Adding a New Batch to the Registry

When the QA workflow reaches Step 4 of Section 13B (Slack Garrett with findings after Max approves), the calling agent should add an entry to `qa_active_batches.json`. The entry needs:

1. `batch_id` — from the QA session
2. `slack_channel` and `thread_ts` — from the Slack message sent to Garrett
3. `checklist_path` — relative path to the xlsx in MRV Expert
4. `certify_url` — the removal edit URL
5. `fail_items` and `flag_items` — populated from the checklist findings, with enough detail for re-review
6. `date_sent` — timestamp of when Garrett was notified
7. `status` — set to `"awaiting_garrett"`

This registration step is what makes the monitoring generic — no need to create per-batch scheduled tasks anymore.

## Key References

- **Knowledge base:** `Charm_Isometric_Knowledge_Base.md` in MRV Expert workspace
- **BCU rule (Section 13B):** BCU quantity (tCO₂e) must equal or exceed the corresponding transport process emission (tCO₂e)
- **Garrett's user ID:** U08JW9HQG5B
- **Max's user ID:** UL2SL4H5H
- **Garrett's DM channel:** D08KEFVRJDP

## Principles

- **Be thorough in re-review.** The whole point is to verify Garrett's work before telling Max it's done. Don't just check that *something* changed — check that the *right thing* changed and the values are correct.
- **Be flexible in detection.** Garrett is a human, not a bot. He'll phrase completion however feels natural. Match intent, not keywords.
- **Keep the registry clean.** Closed batches get removed. The registry should only contain batches that genuinely need monitoring.
- **Don't re-review prematurely.** Only trigger on messages from Garrett (U08JW9HQG5B), not from Max or the QA bot. And make sure the message actually signals completion — a question like "is this the right value?" is not completion.
- **Close browser tabs.** Always clean up after navigating Certify.
