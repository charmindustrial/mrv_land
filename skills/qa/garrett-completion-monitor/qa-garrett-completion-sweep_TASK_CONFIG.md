# Scheduled Task Configuration: qa-garrett-completion-sweep

**Status:** Ready to create. Run this from a regular Cowork session (not a scheduled task session).

**To set up, tell Claude:**
> "Create a scheduled task called `qa-garrett-completion-sweep` that runs weekdays at 9am, 12pm, 3pm, and 6pm. Use the prompt from `qa-garrett-completion-sweep_TASK_CONFIG.md`."

---

## Task ID
`qa-garrett-completion-sweep`

## Description
Sweep all active QA batch threads for Garrett's completion signals — triggers re-review and closes the loop with Max

## Cron Expression
`0 9,12,15,18 * * 1-5` (weekdays at 9am, 12pm, 3pm, 6pm local)

## Prompt

You are running the QA Garrett Completion Monitor sweep. This is an automated task — execute autonomously without asking clarifying questions. Make reasonable choices and note them in your output. For "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if explicitly described below.

### Objective

Sweep all active QA batch threads sent to Garrett Lutz for completion signals. When Garrett indicates he's finished making corrections, re-review his changes in Certify, update the QA checklist, and notify Max.

### Step 1: Load context

1. Read the `qa-garrett-completion-monitor` skill (SKILL.md in the skills folder) for detailed re-review instructions.
2. Read `skills/qa/batch-qa/qa_active_batches.json` from the MRV Expert workspace folder. This is the registry of all batches currently awaiting Garrett's response.
3. Read `knowledge-base/Charm_Isometric_Knowledge_Base.md` from the MRV Expert workspace folder for protocol references and verification logic.

### Step 2: Check for empty registry

If the registry has no entries or no batches with `status: "awaiting_garrett"`, do nothing and end the task.

### Step 3: For each batch with status "awaiting_garrett"

#### 3a. Read the Slack thread
Read the thread at the batch's `slack_channel` / `thread_ts`.

#### 3b. Detect completion signal
Check if Garrett (user ID: U08JW9HQG5B) has replied with a completion signal. Be flexible with detection — any of these count (case-insensitive, may be part of a longer message):
- "complete" / "completed"
- "done" / "all done"
- "fixed" / "fixed it" / "all fixed"
- "updated" / "all updated"
- "taken care of" / "all set"
- "finished"
- "made the changes" / "changes made"
- "good to go" / "should be good now"
- Or any message that clearly conveys he's finished making corrections

Use judgment — if his message clearly communicates "I did the thing," that counts. Don't require an exact keyword match. But don't count questions or partial updates as completion.

**Important:** Only match messages from Garrett (U08JW9HQG5B), not from Max or the QA bot.

#### 3c. If NO completion signal found
Skip this batch. It will be checked on the next sweep. Move to the next batch.

#### 3d. If completion signal IS found — run the full re-review

Follow the re-review workflow from the skill. In summary:

1. **Open Certify** at the batch's `certify_url` using Claude in Chrome
2. **For each fail_item and flag_item in the registry entry:**
   - Navigate to the `certify_location` specified
   - Extract the current values
   - Evaluate whether the issue has been corrected per `what_to_verify`
   - Document current values and whether they satisfy the original finding
3. **Close browser tabs** when done with Certify
4. **Update the QA checklist** at the batch's `checklist_path` (relative to MRV Expert workspace, inside `outputs/qa/batch-qa/`):
   - If a FAIL/FLAG is corrected: change status to PASS, update notes with new verified values and date, clear red fill from all 4 columns
   - If NOT corrected: keep as FAIL/FLAG, update notes explaining what remains unresolved
   - After updates, audit entire checklist formatting: only FAIL rows should have red fill (all 4 columns), everything else no fill, section headers preserved
5. **Slack Max** (user ID: UL2SL4H5H) with a DM:
   - State that Garrett has responded for batch [ID]
   - Summarize re-review findings (all resolved, or specify unresolved items)
   - Include a link to the updated checklist
6. **If ALL findings resolved:**
   - Reply "Corrected" in Garrett's Slack thread (batch's `slack_channel` / `thread_ts`)
   - Remove the batch from the `active_batches` array in the registry
   - Disable this scheduled task if the registry is now empty (no more batches to monitor)
7. **If any findings NOT resolved:**
   - Do NOT reply "Corrected"
   - Keep `status: "awaiting_garrett"` in the registry
   - Note in Max's notification that Garrett may need another pass

### Step 4: Save the updated registry

Write the updated `qa_active_batches.json` back to `skills/qa/batch-qa/` in the MRV Expert workspace folder.

### Key references
- Skill: qa-garrett-completion-monitor (skills folder)
- Registry: skills/qa/batch-qa/qa_active_batches.json (MRV Expert workspace folder)
- Knowledge base: knowledge-base/Charm_Isometric_Knowledge_Base.md (MRV Expert workspace folder)
- Garrett's user ID: U08JW9HQG5B
- Garrett's DM channel: D08KEFVRJDP
- Max's user ID: UL2SL4H5H
