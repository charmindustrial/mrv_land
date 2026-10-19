---
name: mrv-standup
description: Daily MRV standup digest. Scans ~33 Charm Slack channels for MRV-relevant cross-team activity and posts a tiered summary to the #team-mrv-alerts channel. Designed primarily for a scheduled weekday-morning remote agent, but also runs ad-hoc. ALWAYS trigger this skill when someone says "run the MRV standup," "MRV digest," "morning digest," "what's MRV been missing," "give me the standup," or when a scheduled cron fires the digest. The skill is read-only on Slack except for the single #team-mrv-alerts post it makes. Do NOT trigger for one-off "what's happening in #channel-X" questions — this is a multi-channel daily sweep, not an ad-hoc lookup.
---

# MRV Standup

A pre-loaded morning digest of MRV-relevant cross-team activity. The MRV team is structurally on the back-foot when other teams (forestry, ag, sales, eng, biz dev) explore new feedstocks, offtakes, methodologies, or regulatory positions — by the time the work lands in MRV's lap, bandwidth's been spent. This skill closes that loop daily so the MRV team starts the workday already aware.

## Invocation paths

- **Scheduled cron** (primary path): a remote agent fires this skill on weekday mornings.
- **Ad-hoc**: someone says "run the MRV standup," "give me today's digest," "MRV digest," etc. Same procedure.
- **Don't run on weekends**. If asked on a weekend, run with a Friday-5pm-PT lookback anyway.

## Lookback window

Determined by the day the skill runs (Pacific time):

| Day | Lookback start |
|---|---|
| Tue–Fri | Previous calendar day, 6:00am PT |
| Monday | Previous Friday, 5:00pm PT |
| Weekend ad-hoc | Previous Friday, 5:00pm PT |

`slack_read_channel` accepts `oldest` as a Unix epoch timestamp — compute it from the rule above and pass per-channel.

## Channel registry

Each entry: `(name, channel_id, default_tier)`. The default tier sets the prior on what counts as "interesting" in that channel. The filter rules below still apply — default tier only nudges the bar.

### Tier-A — MRV core (low bar to surface)
- `#team-mrv` (private) — `C07AK8ESJ4T`
- `#mrv-ops-charm` — `C080XSUU2PK`
- `#mrv-ops-la` — `C088BL7DHV1`
- `#mrv-ops-co` — `C06PL0M23RQ`
- `#mrv-ledger` — `C05FPPNCV62`
- `#mrv-protocol` — `C05C1867GSV`
- `#team-mrv-alerts` — `C0944NQH1RP` *(Jira feed; surface only ticket creations and transitions to `Done`; skip `In progress` / `Review` transitions. Also the digest's own delivery channel: skip any message starting `*MRV Standup —`, i.e. earlier digests)*

### Tier-B — Verifier-facing (Isometric workspace + cross-org)
- `#isometric-charm` (private, Isometric workspace) — `C03V684HHBK`
- `#ext-proj-charm-350-isometric` (Isometric workspace) — `C095G0XRHFA`
- `#private-external-charm-isometric` (private) — `C07U40HBAGN`

### Tier-C — Adjacent (high bar; relevance must be earned)
- `#oil-research` — `C07BPTQ12BG`
- `#oil-materials` — `C09A9JGPZ45`
- `#char-organization` — `C0AMTJDMVRD`
- `#char-industry` — `C08V56SQWKT`
- `#char-agriculture` — `C05DU297HMH`
- `#aecn-low-benzene-trials` — `C09BB7P1XGR`
- `#reservoir-injection-research` — `C07EXKHF8P4`
- `#biomass-sourcing` — `C0647C9TYL9`
- `#biomass-working-group` (private) — `C06GB4P02NT`
- `#chemical-analysis` — `C045V0YN0F3`
- `#chemical-analysis-notifs` — `C04TBR79A9W`
- `#co-benefits` — `C0A9XHB4K0A`
- `#communityengagement` — `C04V1PEKWN4`
- `#cots-bio-oil` — `C044ADHLALE`
- `#finance-and-carbon` (private) — `C07LE2M8QUF`
- `#forestry` (private) — `C0AQ3MEG2JE`
- `#injection-dev-ks` — `C07FH5M4CG1`
- `#injection-ops-la` — `C097R1NQ0F9`
- `#injection-permitting` — `C04MDNJ5G4B`
- `#ironmaking-dri` — `CH7KW63LN`
- `#logistics` — `C07F9A8HB9S`
- `#proposals` — `C03E02ZU91D`
- `#regulatory-compliance-triage` (private) — `C0AR9U0K83Y`
- `#safety` — `CCQUBU8N9`
- `#sales` — `C04RR3T24Q6`

**Unresolved:** `#co` — no exact match exists in the workspace channel index (the closest hit was `#colorado-ski-snowboard`, which is unrelated). Skip it silently on each run; add its channel ID to the registry once one is identified.

## The filter

Every message gets bucketed into one of three tiers. **Lean liberal.** False negatives (the team misses a thing) cost more than false positives (a reader skims past a line). When in doubt between Watch and FYI → Watch. Between FYI and Drop → FYI.

### Watch (top of the digest)
Anything that *would change a future GHG calc, verification posture, or methodology stance*:
- New feedstock category being evaluated (forestry sourcing strategy, novel biomass, third-party oil)
- New offtake/end-use being explored (char→AD, char→steelmaking, oil-to-product)
- Regulatory or methodology question — explicit MRV / protocol / verification touch; mentions of Isometric, VVB, Certify, GHG statement, EAC, BCU, REC, buffer pool, Section 9, leakage, additionality, baseline, BECCS, SBTi
- Operational change at Basco/CO/KS that would alter component metrics (new equipment, fuel/energy switch, transport routing change, new salting protocol)
- New buyer or external party requiring an MRV story (new RFP, due diligence ask, ratings agency rerating)
- Compliance/permit/regulatory development (KDHE, LA Office of Conservation, EPA, USDA NRCS, UK BECCS, EU CRCF)

### FYI (second tier)
- Novel commercial activity (new RFPs, sales discussions framing new product positioning)
- Cross-team experiments not yet MRV-bound but plausibly will be (water/CDR co-application, Google water conservation, wildfire mitigation, oil plugging, community benefits)
- Internal tooling or analytical method changes that touch how MRV data is collected
- Conference/external commentary on Charm or peers (BeZero rerating threads, SBTi guidance, peer methodology drama)

### Drop silently
- Routine ops chatter, safety incidents that don't touch MRV scope, sales updates without a methodology angle, social/admin
- Bot noise that isn't a Jira CREATE or DONE transition (`#team-mrv-alerts` filter above)
- Threaded acknowledgments ("ack", "thx", emoji-only reactions)
- Anything already covered by a Watch/FYI bullet from the same thread (deduplicate)

## Procedure

### 1. Compute lookback
- Get current PT date/time
- Apply the day-of-week rule above
- Convert to Unix epoch seconds → `oldest_ts`

### 2. Scan channels
For each registry entry, in parallel batches of ~6:
- `slack_read_channel(channel_id, oldest=oldest_ts, limit=50)` — use the default detailed response so each message includes `ts` and `permalink` fields. Concise format strips the permalink, which breaks step 4.
- If a parent message looks load-bearing and has replies, fetch the thread with `slack_read_thread`
- Skip channels that error (likely archived) — log and continue silently
- Skip the `#co` placeholder

### 3. Filter
Apply tier rules. Tier-A messages get the lower bar; Tier-C messages must clear the higher bar (explicit MRV/methodology/regulatory hook).

### 4. Format the digest
Single Slack message in mrkdwn so it renders cleanly in the channel:

```
*MRV Standup — {YYYY-MM-DD}*  _(lookback: {lookback_start} → now)_

🔴 *Watch*
• [#channel-name] {one-line summary} — <permalink|thread>
• ...

🟡 *FYI*
• [#channel-name] {one-line summary} — <permalink|thread>
• ...

📊 _{N_watch} Watch · {N_fyi} FYI · {N_scanned} channels scanned_
```

- Bullets: ≤140 chars, neutral phrasing (no editorializing), `[#channel-name]` prefix
- If Watch is empty, omit the Watch section entirely (don't print "no items")
- If both Watch and FYI are empty, post a single line: `*MRV Standup — {date}* — quiet morning, nothing material.`
- **Each link MUST be a per-message Slack permalink, not a channel link.** Use the `permalink` field from the message object returned by `slack_read_channel`. If for any reason the field is missing, construct it manually:
  - Charm workspace: `https://charmindustrial.slack.com/archives/<CHANNEL_ID>/p<TS_NO_DOTS>` where `TS_NO_DOTS` is the message `ts` with the period removed (e.g. `1714946400.000200` → `p1714946400000200`)
  - Isometric workspace channels (#isometric-charm, #ext-proj-charm-350-isometric, #private-external-charm-isometric): same pattern but `https://isometric-hq.slack.com/archives/...`
- For threaded posts, link to the thread parent's permalink. To deep-link to the thread view (opens with replies expanded in the side panel), append `?thread_ts=<parent_ts>&cid=<CHANNEL_ID>` to the parent's permalink.

### 5. Deliver
- `slack_send_message` to channel = `C0944NQH1RP` (#team-mrv-alerts)
- Workspace: Charm Industrial
- Do NOT post anywhere other than #team-mrv-alerts. Never DM a person (including Max or Garrett). Ever.

### 6. Log the run
Append one JSON line to `outputs/digests/mrv-standup/run-log.jsonl`:
```json
{"date":"2026-05-06","lookback_start":"2026-05-05T06:00-07:00","channels_scanned":33,"channels_errored":0,"watch_count":4,"fyi_count":7,"dropped_count":42,"duration_s":47}
```
Lets the team audit cadence and noise level over time without re-reading old digests.

## Calibration

After the first 1–2 weeks the team will have feedback on what's surfacing as Watch that should have been FYI (or vice versa), and which channels are pure noise.

- **Update this SKILL.md** — the channel registry and filter rules are the version-controlled spec. There is no separate config file.
- If a channel produces zero useful signal across a full month, drop it from the registry rather than tuning the filter around it.
- If a channel keeps generating false-positive Watch items, demote its default tier or add an exclusion clause.

## Constraints

- **Read-only on Slack** except for the one #team-mrv-alerts post. No reactions, no replies, no DMs, no posting to any channel other than `C0944NQH1RP`.
- **Don't fabricate.** If a channel returns nothing or errors, skip it silently — don't pad the digest with "no activity in #X."
- **One message per run.** No follow-up threads, no second messages.
- **No auto-memory writes.** This skill produces information for the team; it doesn't generalize to things to remember about anyone.
- **Don't try to be clever about deduplication across days.** Today's lookback is independent of yesterday's. If a multi-day thread keeps developing, surface it again — readers can skim past repeats faster than he can dig up things he missed.

## Output destination

`outputs/digests/mrv-standup/`:
- `run-log.jsonl` — append-only audit trail
- (no other persistent artifacts; the digest itself lives in Slack)
