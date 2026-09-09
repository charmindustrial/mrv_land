---
name: resume-echo-review
description: >
  Recurring applicant-screening check for Charm's open "MRV Analyst" Lever posting.
  Runs roughly twice a day, around 9am and 5pm local -- launchd actually wakes the
  wrapper script every 30 minutes and it only starts a real pass when one is due,
  which is what makes it self-healing if the machine was off or asleep through a
  scheduled time (added 2026-09-07 per Max: a missed trigger must not be silently
  skipped). Safe to run ad-hoc. Reads
  every candidate currently in the "New applicant" stage of the posting's pipeline,
  runs each new one through three gates -- Gate 1 (does the resume copy language from
  the job posting/materials, or does the candidate's own LinkedIn contradict what
  the resume claims -- either one disqualifies, no exceptions), an experience gate
  (does the candidate have 3+ cumulative years of work experience of any kind, with
  internships not the majority of that time -- disqualifying, same as Gate 1), and
  Gate 2 (does the candidate have any MRV, carbon accounting, ESG, life-cycle-analysis,
  or related sustainability program experience or education at all -- not disqualifying,
  just a priority split) -- then updates the persistent "Resume Echo Audit" artifact and
  candidate_registry.json, and tells Max via a desktop notification (never Slack --
  see "Why desktop notification, not Slack" below) that a new pass completed.
  Candidates whose Lever stage has moved away from "New applicant" since the last
  run are dropped from the registry and the report -- that stage change means Max
  already reviewed them elsewhere. ALWAYS trigger when: a scheduled run fires this
  job, Max says "run the echo review", "check for new MRV Analyst applicants",
  "update the echo report", or asks about the state of this automation. This skill
  is STRICTLY READ-ONLY on Lever and LinkedIn -- it never archives, notes, tags, or
  moves a candidate; Max does that himself in Lever after reading the report.
---

# Resume Echo Review

Twice-daily applicant screen for the MRV Analyst posting, building on the one-time
manual "Resume Echo Audit" from 2026-09-03. Same two source-integrity checks as that
audit, now applied to every new applicant automatically, plus a minimum-experience gate
(added 2026-09-04, disqualifying) and a non-disqualifying gate for sustainability/MRV
subject-matter background.

## Hard rules

- **Read-only on Lever and LinkedIn.** Navigate, snapshot, read. Never click Archive,
  Add note, Edit, Email, Schedule, Snooze, or any stage-change control, and never type
  or fill a form field. (`~/.claude/hooks/certify_readonly_guard.sh` hard-blocks all of
  this at the tool level regardless of what this skill does — Lever is enforced the same
  way as Certify. This is defense in depth, not the only thing keeping you honest here.)
- **No copies of resumes or candidate documents persist anywhere.** If Lever's "Parsed"
  view fails and you have to view a resume as a rendered image, write it to
  `~/.resume-echo-review/tmp/`, read it, then delete it before moving to the next
  candidate — never let one sit past the read that needed it. Delete the whole
  `~/.resume-echo-review/tmp/` directory's contents at the end of every run regardless.
  Nothing about a candidate's resume file itself — text, image, or otherwise — goes to
  Drive, gets attached to a message, or gets embedded in the artifact. The artifact
  and this registry carry your written findings and short verbatim quotes only.
- **A disqualification requires a real quote or a real, checked link — never a guess.**
  Same standard as the original audit: read the actual resume text and the actual
  LinkedIn page in this run before writing a verdict.
- **Gate 2 is never disqualifying.** "No sustainability background" is a priority
  category, not a rejection. Say so plainly in the report; don't let the tone imply
  otherwise.
- **Stopping rule for a broken login.** If Lever or LinkedIn shows a sign-in page
  instead of the expected content, that is a dead end for this unattended run: do not
  try another browser profile or any other way to get back in on your own. Write
  `FAILED: <site> session expired` to the run log, fire a desktop notification saying
  a re-login is needed, and stop. Re-authentication needs `playwright-login` with Max
  physically present, which an unattended run cannot do.
- **Never propose or take a hiring action.** This skill screens for authenticity and
  subject-matter background. It does not, and should not, rank candidates on fit,
  seniority, or anything else — that's Max's read of the report, not this skill's.

## Catch-up scheduler (added 2026-09-07)

Between 2026-09-04 5pm and 2026-09-07 9am the scheduled job failed to produce a
single successful pass -- two network timeouts, an OAuth token revocation, and a
run that hung across a system sleep long enough to blow through its own 900-second
watchdog (the watchdog is an in-process `sleep`, which itself gets suspended if the
Mac sleeps, so it can't enforce a real wall-clock deadline once that happens). Max's
instruction: a missed trigger must never be silently skipped -- when the machine
comes back, it must catch up on its own.

The fix changes how this job is scheduled, not what it does: `com.charm.resume-echo-review.plist`
now uses `StartInterval: 1800` (every 30 minutes) plus `RunAtLoad: true`, instead of
fixed `StartCalendarInterval` entries at 9:00/17:00. `run.sh` decides on each tick
whether a real pass is actually due, using two files instead of an in-process timer:

- `~/.resume-echo-review/run.lock` -- written (`pid epoch`) at the start of a real
  pass, removed at the end. A tick that finds this file checks the recorded PID and
  start time against wall-clock `now`: still running and under `HARD_LIMIT` (900s) →
  exit quietly, nothing to do. Alive but past `HARD_LIMIT` → the process hung across
  a sleep; kill it, log it, reclaim the lock. Dead already → reclaim silently.
- `~/.resume-echo-review/last_success_epoch` -- a unix timestamp written only after
  a pass that actually completed (`RC=0`, `DONE` or `NO-ACTION` both count). A tick
  where `now - last_success < 25200` (7 hours) is not due yet and exits quietly, no
  log line. Past that window -- whether because a slot was missed by hours or days,
  or the machine only just woke up -- the next tick runs a real pass immediately.

This means a genuinely idle tick (most of the 48/day) produces no log output at
all; only a tick that actually starts a pass writes anything to `run.log`. Don't
read log silence as the job being down -- check `last_success_epoch`'s mtime or
`candidate_registry.json`'s `last_run` field for the real answer to "when did this
last actually run."

## Why desktop notification, not Slack

Two reasons, both learned the hard way on sibling automations in this workspace:

1. Every message this workspace's Slack connector sends is posted **as Max's own
   account**. Slack does not push a notification for a user mentioning or DM'ing
   themselves, on any workspace, by design — a Slack alert here would silently never
   reach him (see `garrett-completion-monitor`'s run.sh for the same finding).
2. Keeping candidate names and disqualification reasons out of a chat transcript
   entirely is the safer default here, consistent with Max's 2026-09-03 instruction
   that no resume/candidate data should sit anywhere it doesn't have to.

So the alert is a plain macOS notification (`osascript -e 'display notification ...'`)
with a count-only summary and no candidate names — detail lives only in the artifact,
which is private by default. This mirrors `eac-inventory-monitor`'s post-incident
redesign: no delivery step exists here for anything to get stuck approving.

## Step 1 — Load state

Read, in order:
1. `config.json` in this skill's folder — posting ID, artifact URL, Job Materials
   Drive file ID.
2. `candidate_registry.json` in this skill's folder — every candidate assessed so far,
   with their gate verdicts and last known Lever stage.
3. The live job posting text: `https://jobs.lever.co/charmindustrial/<posting_id>`
   (public, no login) — re-read it fresh each run in case Erik has edited it; don't
   assume the wording from a prior run still matches.
4. The internal "Job Materials: MRV Analyst" brief from Drive (`job_materials_drive_file_id`
   in config.json) — same reason.

## Step 2 — Read the live Lever pipeline

Open `lever_candidates_url` from config.json (this needs Max's own logged-in Lever
session via the persistent `playwright` profile — if it hits a sign-in wall, that's
the stopping-rule case above). The candidate table lazy-loads: scroll the
`.stages-and-profile-list` container to the bottom (as needed, checking the unique
candidate link count against the "Applicant" count shown in the sidebar) before
reading the full list, or you will silently miss candidates the same way the very
first manual audit did.

For every candidate currently shown with pipeline stage **"New applicant"**, note
their candidate ID, name, org, and Lever URL.

## Step 3 — Reconcile against the registry

For every candidate already in `candidate_registry.json`:
- If they no longer appear in Lever's "New applicant" stage (moved to another stage,
  or archived) — **remove them from the registry entirely.** Append one line to
  `outputs/automation/resume-echo-review/run-log.jsonl`:
  `{"ts": "<now>", "event": "removed", "candidate_id": "...", "name": "...", "reason": "stage no longer New applicant"}`.
  This is what Max asked for (2026-09-03): a stage change means he already reviewed
  them elsewhere, so they drop out of this report's flow.
- If they're still in "New applicant" — leave their entry untouched. Do not re-run
  the gates on someone already assessed; a resume doesn't change after submission.

For every candidate in Lever's current "New applicant" list who is **not yet** in
`candidate_registry.json` — that's a new applicant. Continue to Step 4 for each.

## Step 4 — Gate 1: source-integrity check

Exactly the method from the original 2026-09-03 audit. For the new candidate:

1. Open their resume (Lever's "Parsed" tab; if parsing failed, use the
   `docviewer-assets/.../page1.png` fallback — view once, delete immediately per the
   hard rules above). Read the full text.
   - **The Parsed tab can render successfully and still silently drop entire
     sections** — a case on 2026-09-07 (Shashank Reddy Pisati) had its Parsed view
     show only "Experience" and "Education," completely omitting a "Professional
     Summary" and "Technical Skills" section that existed on the actual PDF and
     contained the resume's most damning content (posting-specific platform names,
     reused phrasing). This is a different, more dangerous failure than the Parsed
     tab failing outright, because a clean-looking partial render doesn't prompt a
     fallback check on its own. Whenever the Parsed text credits the candidate with
     any Charm-specific-sounding platform name, methodology term, or unusually
     specific terminology (Mangrove, Isometric Certify, GHG Accounting, etc.), open
     the Original tab (renders the actual PDF as an image, no text layer — screenshot,
     read, delete per the no-persist rule) and confirm that content actually exists
     verbatim before crediting it or clearing the candidate on it. Don't wait for the
     Parsed tab to fail before checking the original — check it any time Gate 1 or
     Gate 2 leans on specific terminology.
   - **Navigating to a candidate whose Lever stage is no longer "New applicant"**:
     a direct URL to `https://hire.lever.co/candidates/<id>` loads a reduced view
     with no working resume-viewer click target. Instead, open the stage-filtered
     candidate list (`.../candidates?postingIds%5B%5D=<posting_id>&pipeline=applicant&stageId=<stage_id>`),
     use `browser_find` for the candidate's name, and click their row link — that
     loads the full view with working Original/Parsed tabs.
2. **Language match**: compare against the live posting text and the Job Materials
   brief. A hit is identical or near-identical phrasing, a fabricated job title that
   is this posting's own exact title, or a Charm-specific business detail (e.g.
   "bio-oil injection") with no plausible source outside Charm's own materials.
3. **Identity/experience check**: open whatever LinkedIn URL the candidate submitted
   with their application (Lever's "Add link" section). Read the main profile page
   to confirm identity (name, headline, location, current employer). Then navigate
   directly to `linkedin.com/in/{username}/details/experience/` to read the
   Experience section — **never** rely on the main profile page's DOM to determine
   whether an Experience section exists. LinkedIn lazy-loads sections on the main
   profile, and multiple runs (Alec Bennington, Rochak Nath, Jenil Gopani on
   2026-09-08/09) falsely concluded "no Experience section" because the section
   hadn't rendered when the DOM was inspected. The `/details/experience/` URL loads
   the Experience entries as a standalone page and is reliable.
   - No LinkedIn on file → note it, don't disqualify on absence alone.
   - Resolves to a different, unrelated person, or the link is dead/a bare
     homepage → **disqualify** (`identity_mismatch`).
   - `/details/experience/` page loads but shows no entries → the Experience section
     is genuinely empty. Treat this the same as a contradiction, not as an absence
     to excuse: **disqualify** (`experience_mismatch`), especially if the resume's
     bullets follow the templated, tool-name-dropping pattern already seen in this
     posting's confirmed fabrications (near-identical bullet structure across claimed
     jobs, domain word swapped) — that combination is the actual fabrication
     signature, not the missing LinkedIn data alone in isolation.
   - Resolves to the candidate but the profile's real work history contradicts a
     specific resume claim (different current employer, wildly different career) →
     **disqualify** (`experience_mismatch`). No benefit of the doubt for a plausible
     innocent explanation (a stale LinkedIn, etc.) — Max's standing instruction
     (2026-09-03) is that a confirmed mismatch disqualifies on its own.
4. Note any literal leftover AI-drafting artifact in the text (e.g. "(please
   confirm)") as `ai_artifact`.

If ANY of `language_match` / `identity_mismatch` / `experience_mismatch` / `ai_artifact`
applies: `gate1_status: "disqualified"`, list every reason that applies, write
`gate1_evidence` as 1–2 sentences with the actual quotes/facts (not a vague summary),
set `gate2_status: "not_applicable"`, and skip Step 5 for this candidate.

If none apply: `gate1_status: "clean"`, `gate1_evidence` notes briefly that language
and identity both checked out, and continue to Step 5.

## Step 4B — Experience gate: minimum 3 years total work experience (added 2026-09-04)

Disqualifying, same severity as Gate 1. Applies only to candidates clean on Gate 1 (a
Gate-1 disqualification already sets this to `not_applicable`).

**Method:** sum the duration of every job listed in "Experience" on the resume — total
cumulative time, literally summed across all roles regardless of employer, field, or
whether roles overlap in time. It does not matter what the work was ("doesn't matter
what," per Max, 2026-09-03) — a soccer-officiating role, a graduate research
assistantship, and a corporate job all count the same way, as long as it's presented on
the resume as a role with dates and duties. A role still open (no end date given, or
explicitly "Present") runs through today's date.

**Internship exception:** internships count toward the total, but if internship time is
**a majority** (strictly more than half) of the total, the candidate fails regardless of
the raw total. Exactly half does not trigger this — "majority" means >50%, not ≥50%.

**Threshold:** total must be ≥ 3.0 years. Under that: `experience_status: "insufficient"`,
disqualifying — the candidate drops out of the report the same as a Gate 1 failure.
`experience_evidence` states the total, computed from the listed date ranges, e.g.
"Data Analyst, Akamai, Jan 2026–present (~8 months) + Data Analyst, Subex, Jan 2023–Apr
2024 (1y4m) = ~2 years total. Under the 3-year minimum."

If ≥ 3.0 years: `experience_status: "sufficient"`, and continue to Gate 2 (sustainability
background) below. `experience_evidence` states the total and the breakdown so the
figure is checkable, not asserted.

**Ambiguous formatting calls (documented so future runs stay consistent):**
- A vocational/clinical placement or research assistantship listed under "Experience"
  with an employer, dates, and duties counts as work, even if it's academic in nature or
  oddly placed near an Education entry.
- Side/occasional paid work (e.g. licensed officiating, adjunct work) counts on the same
  basis as any other listed role.
- When a genuinely ambiguous case comes up that could flip the pass/fail outcome (not
  just a marginal detail), surface it to Max rather than deciding silently — this
  happened for 3 of the first 24 candidates checked against this gate and all 3 were
  resolved in the "count it, it passes" direction by Max directly.

## Step 5 — Gate 2: sustainability / MRV subject-matter check (clean candidates only)

Only reached if `experience_status: "sufficient"`. Read the same resume text (and the
LinkedIn page already open) for **any** experience
or education touching a sustainability-related program or subject matter. This is
deliberately broad — it is not limited to literal "MRV." Counts:

- MRV / monitoring, reporting, verification work in any industry
- Corporate carbon accounting or GHG inventory work
- ESG reporting or ESG data/analytics roles
- Life-cycle assessment (LCA) or techno-economic assessment (TEA) of environmental
  impact
- Environmental monitoring, ecological research, conservation, renewable-energy
  impact research, or similar environmental-science subject matter
- A degree in an environmental, sustainability, or closely related field (even
  without matching work experience)
- Anything else that is genuinely a sustainability-related program or subject
  matter, even if it doesn't fit the categories above — use judgment, but the bar is
  "this is substantively about environmental/sustainability/carbon subject matter,"
  not "this industry is adjacent to energy or utilities." Forecasting utility bills,
  managing disaster logistics, or doing IT/data-governance work for an energy-sector
  client are NOT sustainability experience on their own — they need an actual
  environmental/carbon/ESG/sustainability component to count.

If the resume or profile turns up a match: `gate2_status: "sustainability_experience"`,
and `gate2_evidence` quotes the specific degree/role/bullet that qualifies.

If a full read of the resume and LinkedIn profile turns up nothing on this front:
`gate2_status: "no_sustainability_experience"`, and `gate2_evidence` names what
industries/employers/degrees you did see (so the negative claim is grounded in what
was actually reviewed, not just an unsupported "nothing here").

## Step 6 — Update the registry

Add each new candidate to `candidate_registry.json` following the existing schema
(see `_schema_notes` at the top of that file) — `first_assessed` and `last_updated`
both set to now. Update `last_run` at the top of the file. Save.

**Save incrementally, one candidate at a time (added 2026-09-08).** Write and save
each new candidate to `candidate_registry.json` as soon as its own gates are
decided — do not hold multiple new candidates in memory and write them in one
batch after finishing the whole list. On 2026-09-08 a backlog of 11 new candidates
(built up during the prior outage) hit the run's time limit after only 3 were
assessed, and because nothing had been saved yet, all 3 were lost and the next
run started completely over. Saving after each one means a run that gets cut off
keeps everything it already finished, and the next tick only has to pick up
whoever's left.

## Step 7 — Regenerate and republish the artifact

Rebuild `artifact_url`'s HTML (read it back first via `Artifact` with `action: "read"`
so you're editing the current published version, not a stale local copy) reflecting
the full current registry, organized into exactly these sections, in this order:

1. **Disqualified** — same evidence-block format as the original audit (posting-vs-resume
   quote pairs, identity-check blocks) for Gate 1 failures, plus a distinct block style
   for `experience_status: "insufficient"` failures (state the computed total and
   breakdown, not just a verdict). Rank Gate 1 fabrications first, experience failures
   after.
2. **Sustainability / MRV background** — clean candidates with `gate2_status:
   sustainability_experience`. This is the priority-review tier; say so.
3. **No sustainability background** — clean candidates with `gate2_status:
   no_sustainability_experience`. Frame this plainly as "not disqualifying, just
   lower priority," never as a rejection.

Keep the summary strip, legend, and method footer from the original design, updated
with current counts and a note that this report is now a living, twice-daily-refreshed
document rather than a one-time audit.

**Two-session split architecture (2026-09-04 — do not try to publish from this run):**
verified directly that the `Artifact` tool does not exist in this local unattended
`claude -p` session, but IS fully available in a cloud-scheduled routine (confirmed by
a live test: a cloud CCR session read this artifact and read a Drive file successfully
via `Artifact` and the Google Drive MCP connector with no ToolSearch needed). Neither
session type can do the whole job alone: this local session has Lever/LinkedIn access
but no Artifact tool; the cloud routine has the Artifact tool but no local file or
browser access. So the job is split:

1. **This local run** does the browsing, gating, and registry update as always, then
   copies the current `candidate_registry.json` verbatim to
   `/Users/maxlavine/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/Team/Hiring/MRV Analyst/resume_echo_state.json`
   (overwrite in place). That's the full extent of this session's artifact-related work
   — do not attempt to call `Artifact` here.
2. **A separate cloud routine**, `resume-echo-artifact-publish` (routine id
   `trig_01EhVHSUcy77VEiGg6GYWa6y`, cron `0 16,0 * * *` UTC = 9:00am/5:00pm Pacific,
   same clock as this job, per Max), reads that Drive file, rebuilds the report HTML
   reusing the artifact's existing CSS, and publishes to `artifact_url` directly. It
   no-ops if the state hasn't changed since the last publish. This is what actually
   keeps the visible page current — this local run does not do it and should not try.

## Step 8 — Log and notify

Append one line to `outputs/automation/resume-echo-review/run-log.jsonl`:
`{"ts": "<now>", "event": "run_complete", "new_candidates": N, "disqualified": N, "sustainability": N, "no_sustainability": N, "removed": N}`.

Then fire exactly one desktop notification, no candidate names or PII:

```
osascript -e 'display notification "N new applicant(s) reviewed — X disqualified, Y sustainability match, Z no sustainability bg. See Resume Echo Audit." with title "Resume Echo Review"'
```

The artifact link is safe to reference here even though this session didn't publish it
directly — the cloud routine publishes ~20 minutes later on its own schedule.

If there were zero new candidates and zero removals this pass, still log a
`no_action` line to run-log.jsonl, but do **not** fire a notification, and still write
the Drive relay file (the cloud routine no-ops itself if nothing changed, so this is
harmless, and skipping it risks the two staying out of sync).

## End-of-run checklist

- [ ] `~/.resume-echo-review/tmp/` is empty
- [ ] `candidate_registry.json` reflects exactly the current "New applicant" list —
      no stale entries for candidates who moved stage
- [ ] `resume_echo_state.json` in Drive was overwritten with the current registry
- [ ] `run-log.jsonl` has one new line for this pass
- [ ] Notification fired only if something actually changed
