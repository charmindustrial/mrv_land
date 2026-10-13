# INJ-09-2026-W4-QOWV — steps on hold for permission (temporary)

Held only because they need an approval prompt or a decision. None is dropped; each runs when you're back.

1. **Slack message to you (skill Gate 4, delivery step 2).** `slack_send_message` is on the "ask" list in ~/.claude/settings.json, so it stops for approval. Draft below, ready to send. On sending, stamp `T_final_max_delivery` in batch_timestamps.json and `T_max_notified` in the registry, then rerun run_gates.py if anything changed.
2. **Garrett post in #team-mrv-alerts (delivery step 4).** Only after you approve the checklist. Draft below.
3. **File the finished checklist to the Drive mount (delivery step 7).** Runs after the review loop closes.
4. **Performance monitor at approval and close-out (T5-T10).** Runs as each event happens.

## Rulings applied (2026-10-07)

- **7.2 BCU scope:** "BCUs should be applied to diesel transport, including biomass transport process emissions and handling (not embodied emissions)." June and February totes move to after-BCU CIs. On the package versions of the summaries (the blend's sources): June 0.117288728, February 0.1227182507, July 0.120947, production emissions 5,009.9151 → 4,790.2737 kg (−219.6414). On the linked sheets with the blend rebuilt: 4,786.3316 kg (−223.5835).
- **2.3 COBB:** "On COBB, I defer to Garrett." COBB is not used as a cross-check; 301215 dropped. 301274 stays: its 1,080.0 kg comes from the production system's own weighing, and BGN's 1,036.0 kg is 301277's weighing (rows look shifted).

## Still open

- **7.2, which summary copy governs:** referred to Garrett (Max, 2026-10-07: "Refer it to Garrett."). Difference on W4: 3.9 kg of production emissions.

## Draft — Slack DM to you (not sent)

🚨 QA + adversarial review complete: INJ-09-2026-W4-QOWV (Aqueous / QOWV), Certify rmv_1M3SG7D701S0HZ1Z — Pass 20 / Flag 5 / Fail 7 / N/A 1. Delivery checks green (receipt time to be stamped at send).
Fails: 2.3 tote 301274 gross 1,036.0 (BGN, likely a shifted row) vs 1,080.0 kg (production weighing) · 3.4 COLA-38 divided by 6 totes instead of 18 · 4.4 carbon uncertainty 0.03523 vs 0.0316 · 5.1 tanker fuel factor on the flatbed leg · 6.1 tanker embodied factor · 7.2 June/February CIs count biomass transport before its BCUs (−219.6414 kg on the package summaries, −223.5835 kg on the linked sheets) · 8.1 BCU short of the process emission.
Flags: 1.3 no tote-to-truck list · 2.2 standard 57.6 kg tare · 3.1 tag 300020 shared by two lots · 3.5 no fill date on any 2026 tote (eight totes weighed the month after their label; records place them in the labelled month, no change to the removal) · 7.3 blended CI unlinked, July summary files hold June's figures.
Checklist: outputs/qa/batch-INJ-09-2026-W4-QOWV/Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W4.xlsx

## Draft — Garrett, #team-mrv-alerts (after your approval; not sent)

<@U08JW9HQG5B> INJ-09-2026-W4-QOWV (Aqueous) — QA findings to fix:
• 5.1 Transport process uses the Tanker fuel factor (0.0001143); switch to Flatbed (0.0001384 MT/t-mi).
• 8.1 Then set the BCU to exactly the corrected process output (7,138.2492 kg on the sheet factor).
• 6.1 Embodied uses the Tanker factor; switch to Non-Tanker (0.0001927908256 MT/mi).
• 3.4 Allocation tab C13: COLA-38 carried 18 totes (12 Whole Oil), not 6; carry the new G17 (2,568.8056 mi) into Certify.
• 4.4 Carbon uncertainty should be 0.0316 (0.4 % of 7.9 %), not 0.03523.
• 7.2 BCUs cover biomass transport process and handling, not embodied, so the June and February CIs need recalculating with biomass transport after its BCUs. The June and February summaries exist in two copies: the 11 Aug July-package copies (source of the Jan-Jun blend) give June 0.117288728 and February 0.1227182507 (production emissions 4,790.2737 kg); the Google Sheets the Ops Notes link give June 0.1173329448 and February 0.1230857484 (4,786.3316 kg). Pick the copy, enter the CIs in Ops Notes L18 and L14, and update the Certify CI. The July blend (0.120947) stays.
• 2.3 Confirm 301274's gross: 1,036.0 kg in the Ops Notes and BGN inventory vs 1,080.0 kg in the production system (OIL260721143336). BGN's 1,036.0 kg is 301277's weighing (OIL260721142141), and BGN's 301277 row carries 301227's 1,070.0 kg, so the BGN rows look shifted.
• Flags: 1.3 add tote-to-truck rows; 3.1 lot 4746 shares tag 300020 with lot LOT00004770; 3.5 record each tote's fill date (or the rule that assigns its production period) in the production inventory: Form/tote Date is blank on all 2026 rows, and the production system's production_date is the weigh-in; 7.3 link the blended CI's source. Both "Jul 26 Production Period Summary" files on Drive still hold June's figures.
Reply in this thread when addressed and I'll re-verify in Certify.
