# Isometric Proposal Review — Decoupling Durability Monitoring from Verification

**Source document:** `[External] Bio-oil Monitoring Requirements: Decoupling from Verification.docx` (Isometric, April 2026)
**Reviewer:** Max Lavine
**Date:** April 28, 2026
**Audience:** Internal (Charm team)

---

## What Isometric Is Proposing

A change to the Bio-oil Geological Storage protocol (v1.1) that splits **durability monitoring** off from per-verification submission and onto a fixed six-month calendar cadence (Jan–Jun, Jul–Dec), with reports due within 30 days of period end. The VVB performs a separate **monitoring verification** on each report. Credit verifications then "draw on already-submitted monitoring reports as the evidence base."

The categorical split, as proposed:

| Stays at each verification | Moves to six-monthly Monitoring Report |
|---|---|
| Bio-oil Carbon Content (per batch / per Method A or B) | Storage Monitoring (pressure, brine chemistry, gas monitoring at wellheads/brine tanks, reversal indicators) |
| Injected Mass (scale tickets, calibration certs) | Embodied Emissions (updated when changes occur; confirmed six-monthly) |
| Tailgas Emissions | Incident / Excursion Log |
| Energy & Fuel Use | |
| Transportation | |

The scientific rationale is sound: a reversal affects **all** carbon stored across the project lifetime, not just the most recent reporting period — so durability assurance shouldn't be gated by an arbitrary RP boundary.

---

## Pros — Why This Is Genuinely Good for Charm

**Earlier issue surfacing.** Gas sensor anomalies, instrument calibration gaps, and minor excursions show up between verifications instead of inside the SLA window. Garrett and ops get lead time to fix; Isometric and the VVB get proactive oversight. This is the right model — it's how regulatory monitoring works in every other regulated industry. It also adds robustness: even though current SLA performance is strong (RP-13 was submitted Monday, credits issued Friday — 4 working days), decoupling protects the SLA from outlier monitoring-data events as Charm scales volume and complexity.

**Predictability.** Charm's RP cadence has been variable (14 days to ~6 months across the 13 statements). A fixed Jan–Jun / Jul–Dec rhythm makes annual planning, calibration scheduling, and ops review meetings easier to lay out — independent of whatever credit verification cadence Charm chooses.

**Doesn't constrain credit verification cadence.** Verifications can still happen as often as Charm wants. The roughly monthly cadence we've been running on RPs 8–13 is unaffected.

**Real cross-pathway efficiency for Fort Lupton-origin streams.** Charm's WODO and Aqueous bio-oil fractions and Charm's biochar are all produced at Fort Lupton from the same pyrolysis operation. Pyrolysis production parameters, feedstock data, facility energy metering, embodied emissions for shared equipment, and outbound transport from Fort Lupton are genuinely shared upstream data between the bio-oil and biochar pathways. With Range & Plains Biochar now validated (51.25 tCO₂e issued, 350Solutions verified), there's a defined channel for submitting this data once rather than per-protocol — a meaningful operational saving. The exception is AECN bio-oil (third-party vendor, Quebec), which is a separate upstream chain and stays in its own bucket. We should scope the sharing convention explicitly so Isometric and the VVB are clear about what's shared (Fort Lupton-origin) and what isn't (AECN).

**Scientific defensibility.** A reversal affects all credits issued whose stored carbon is at risk, not just the most recent RP. Continuous oversight of durability is the right framing.

---

## Cons / Risks / Ripple Effects

**A new VVB workstream: "monitoring verification."** The proposal introduces a separate VVB-conducted verification on each 6-monthly report. Open questions for Charm:
- Does it produce a public Monitoring Statement on the registry, or stay internal to Isometric?
- What's the scope and timeline of that engagement from Charm's side (data requests, response windows, evidence package)?
- What's the failure mode if the monitoring verification finds an issue — does it freeze in-flight credit verifications, or run on its own track?

(VVB engagement scope and cost is between Isometric and 350Solutions — 350 contracts with Isometric, not Charm — so resourcing is not Charm's problem to solve.)

**Reversal-investigation workflow needs to be explicit.** The legal blast radius of a reversal doesn't actually change with decoupling — a monitoring issue that called already-issued credits into question triggers a reversal under either regime. What changes is *detection timing* (earlier, which is good) and the procedural surface (a separate workflow with its own findings, freeze, and resolution steps). Charm should push for an explicit reversal-investigation procedure that defines: trigger criteria, investigation timeline, whether and how it freezes pending credit verifications, retroactive buffer pool mechanics, and stakeholder notification. None of this is conceptually new, but it should be written down rather than improvised.

**Categorization ambiguity in the table.** Three rows need tightening before Charm endorses:

1. *Storage Monitoring* covers "pressure data" — but Charm has both **wellhead injection pressure data** (operational, batch-tied) and **reservoir post-injection pressure** (durability). Where do they each live? Today they're commingled at verification.
2. *Embodied Emissions* says "updated when changes occur; confirmed six-monthly" — but EFs themselves and the **application** of EFs to specific batches need separate handling. The application stays at credit verification (per-batch); only the LCA refresh confirmation should be at 6-monthly cadence.
3. *Transportation* is at verification, but transportation **incidents** (a tanker spill) presumably go in the Incident Log on the 6-monthly side. Make this explicit.

**30-day filing window does not fit KDHE's external timeline.** This is the most important fix. KDHE monthly reporting flows: Charm submits June reporting to KDHE by July 31 (one-month lag is built in), and then it can take a couple of weeks for KDHE to turn the reporting back to Charm via public records request. So under the proposal, a Jan–Jun Monitoring Report due Jul 30 wouldn't have June's KDHE reporting back from public records yet — let alone a chance to reconcile and QA it. Charm should request a longer filing window (e.g., 60 days, or a sliding window indexed to KDHE turnaround) or an explicit lag convention where the most recent month's external regulatory data comes in the *next* Monitoring Report. This is solvable but needs to be in the protocol/agreement text, not assumed.

**Vaulted decommissioning — straightforward to clarify.** Some Vaulted post-injection monitoring is biennial (elevation survey ~Jun 2026) or 5-yearly (mechanical integrity test ~2029). The clean rule is: if the test/measurement due date falls within a Monitoring Report period (with adequate buffer for any KDHE turnaround), it's included in that period's package. If no test is due, the Monitoring Report simply confirms no scheduled monitoring activity occurred. Pin this convention in writing.

**Internal QA workflow expansion.** The QA architecture I've built (batch QA gates 1–4, site emissions QA, adversarial reviewer, performance tracker) is structured around RP boundaries. Decoupled monitoring needs its own QA flow — likely a new checklist + skill covering wellhead/brine tank monitoring, calibration certs, embodied EF refresh confirmations, and the incident log. Real scope expansion for me.

**Backward compatibility / first-cycle plan.** Statements 1–13 already submitted durability data per-RP. Charm needs to know:
- Does the first Monitoring Report start fresh (e.g., H1 2026)?
- Does it pull in data already submitted under RP-12 and RP-13?
- For Vaulted (in decommissioning), do post-injection monitoring obligations get a separate cadence, or fold in?

**Documentation duplication risk.** The proposal says "any monitoring data not required for durability assurance must still be submitted at each verification" and verifications "draw on already-submitted monitoring reports." Good in principle. But if the VVB needs to re-verify the same calibration cert for both monitoring and credit verification, we're doing the work twice.

**Vehicle for the change.** Per Isometric this is intended as an operational agreement, not a new protocol module version. That avoids the §2.4.5 renewal-trigger question entirely and lets Charm benefit immediately. We should still get the categorization table and the reversal-investigation workflow into a document with the same operational status as the current SLA — written, signed, and referenceable — so the agreement isn't living in email threads.

---

## What We'd Need for a Successful Implementation

Before Charm endorses, I'd want answers and commitments on:

1. **Definition of the monitoring verification deliverable.** Does the monitoring verification produce a public Monitoring Statement on the registry? Its own findings letter? What's the scope of evidence requests Charm should expect, and on what response windows?
2. **Filing window indexed to KDHE turnaround.** A flat 30-day window doesn't fit. Either lengthen to ~60 days or adopt a one-period-lag convention so external regulatory data has time to come back via public records before a report is due.
3. **Categorization table pinned in the agreement.** The table in the cover note is illustrative. Push for an explicit appendix that maps every data element — wellhead injection pressure (operational vs. durability), embodied EF *application* vs. *refresh*, transportation incidents — into one bucket. Without this, every borderline case becomes a negotiation.
4. **Defined reversal-investigation workflow.** Trigger criteria, investigation timeline, freeze-pending-verifications policy, retroactive buffer pool mechanics, stakeholder notification. Write it down.
5. **Cross-pathway sharing convention scoped correctly.** Explicit list of Fort Lupton upstream data (pyrolysis production parameters, feedstock, facility energy, embodied emissions for shared equipment, outbound transport from Fort Lupton) that's submitted once and referenced by both Charm bio-oil (WODO/Aqueous) and Charm biochar. Equally explicit that AECN bio-oil — third-party Quebec vendor — stays in its own pathway-specific bucket. Avoids both duplication on the Fort Lupton side and false sharing on the AECN side.
6. **Vaulted decommissioning convention.** Confirm the rule "if a test's due date falls in the Monitoring Report period, it goes in that report; otherwise the report confirms no monitoring activity occurred."
7. **First-cycle plan.** Start fresh on H1 2026, or backfill from a defined date? Whatever the answer, make sure Vaulted's existing KDHE submissions feed cleanly without re-doing already-verified durability data.
8. **Calendar alignment.** Map KDHE monthly/quarterly + Isometric 6-monthly + credit verification cadence on one timeline. Confirm no scheduling collisions around the Monitoring Report due dates.
9. **Vehicle for the agreement.** Per Isometric this is operational, not a protocol module bump. Get it written and signed at the same status as the current SLA so it's referenceable, not living in email.
10. **Internal QA build-out.** Need to scope a new QA skill / checklist for the 6-monthly Monitoring Report. Realistic 1–2 week internal lift before we're ready for the first report.

---

## Bottom Line

Strategically this is the right direction. It aligns with how durability monitoring should work scientifically, gives us a predictable annual rhythm, surfaces issues earlier, and creates a clean channel for the narrow set of corporate-level data that's actually shared with the biochar project — all without constraining our credit verification cadence.

The benefits aren't where the proposal advertises them, though: KDHE reporting is already on a 6-month cadence, the 2-week SLA is already routinely beaten (RP-13 was credits-issued in 4 working days), and most "shared" upstream data turns out to be pathway-specific in our footprint. So the case for endorsement isn't "this fixes major pain points" — it's "this is the right operating model for monitoring at our scale and beyond."

The risks are all in execution details: monitoring verification engagement scope and cost, the reversal-investigation workflow, the precise categorization of every data element, the filing window vs. KDHE turnaround, and the internal QA lift on our side. None are deal-breakers, but each needs explicit answers before signing on. I'd respond endorsing the direction and listing the conditions above.
