# Site Emissions QA — Lessons Learned

This document captures specific failure patterns from real QA sessions. The QA agent should read this alongside `category_evidence_guide.md` at the start of each session. These aren't theoretical risks — they are things that actually went wrong and caused rework.

## Session: Basco 6 LA, March 2026

### Failure 1: Describing Work Instead of Doing It

**What happened:** The checklist contained entries like "Verify all column headers, EF cells, and totals in diesel calc sheet include unit labels." This was flagged as a laziness violation — the agent was writing instructions for a future reviewer rather than reporting its own findings.

**Root cause:** Context fatigue in a long session. The agent shifted from actually reading documents to producing template-like entries that looked complete but contained no real verification.

**Fix applied:** SKILL.md now includes Anti-Pattern 1 ("Verify X" Cop-Outs) and Universal Requirement U1 (Units on All Labels) which specifies the expected output format: "Column headers: Date (no units needed), Volume (gallons), Mass (kg), EF (kgCO₂e/kg), Total (kgCO₂e) — all present."

### Failure 2: Quoting Max's Notes Verbatim

**What happened:** The agent included entries like "Per Max: 'It looks like they drove the truck to fill up'" in the QA checklist. Max had shared this as a question for Garrett (a process conversation), not as a QA finding. The agent treated it as a confirmed fact.

**Root cause:** The agent conflated process context (things Max said to help the agent understand the workflow) with evidence-based findings. The checklist should only contain what the agent verified from the evidence.

**Fix applied:** Universal Requirement U8 (QA Output Standards) now explicitly prohibits quoting Max or including process conversations. Anti-Pattern 4 documents this in detail.

### Failure 3: Treating Feedback as One-Off Corrections

**What happened:** Max flagged that the diesel calc sheet was missing units on column headers. The agent added a units check for diesel but didn't check any other category's calc sheets for units. Similarly, when Max flagged missing distance evidence for methanol, the agent didn't check distance evidence for other transport categories.

**Root cause:** The agent treated each piece of feedback as a specific correction rather than extracting the universal principle. This is the single most important lesson from the session — every gap Max identifies represents a class of checks, not a single instance.

**Fix applied:** Anti-Pattern 2 (Treating Feedback as Case-Specific) and the Universal Cross-Cutting Requirements section in SKILL.md. The key principle is now in Key Principles: "When a requirement exists (units on labels, distance evidence, BCU cross-check), it applies to every category."

### Failure 4: Wrong FAIL/FLAG Classification

**What happened:** A missing diesel transaction record (receipt #013317) was marked as FLAG instead of FAIL. The reasoning was that other receipts supported most of the total, so the missing one was a minor gap.

**Root cause:** Misunderstanding of the FAIL/FLAG distinction. FLAG = hygiene issue where the data still supports the reported value. FAIL = you cannot independently confirm the reported value. A missing receipt means you can't confirm that receipt's contribution to the total — that's a FAIL.

**Fix applied:** Universal Requirement U4 (Missing Evidence = FAIL) with the decision rule: "Can you independently confirm the reported value from the available evidence? Yes → FLAG. No → FAIL."

### Failure 5: Missing BCU Cross-Check for Methanol Transport

**What happened:** Methanol transport process emissions (36.17 kgCO₂e) are BCU-eligible, but the agent didn't check whether a BCU offset was applied or whether the BCU Quant sheet had a corresponding line item.

**Root cause:** The agent checked BCU eligibility for diesel and brine (the most obvious categories) but missed methanol transport, argon transport, and other eligible components. BCU cross-checking was applied inconsistently across categories.

**Fix applied:** Universal Requirement U3 (BCU Quant Sheet Cross-Check) now includes the complete list of BCU-eligible site emission components and requires that every one be cross-checked against the BCU Quant sheet.

### Failure 6: Wrong EF Source Year

**What happened:** The agent initially cited diesel EF source as "GREET 2024." The actual source on the correct tab of the Standard EF Sheet is "GLEC V3.2 2025." The agent was reading from the wrong tab.

**Root cause:** The Standard EF Sheet has multiple tabs (one per year). The agent didn't confirm which tab it was reading from, or read from a prior-year tab.

**Fix applied:** Universal Requirement U7 (Correct Year Tab) with the specific Google Sheet ID and the rule: always confirm which tab you're reading from before citing any EF values.

### Failure 7: Including Process Questions as Findings

**What happened:** The agent included a WEX card question (whether WEX fuel card transactions are captured in the diesel calc sheet) as a checklist item. This was a question Max had raised with Garrett — a process discussion, not a QA finding.

**Root cause:** Same as Failure 2 — the agent didn't distinguish between process context and QA findings.

**Fix applied:** Covered by U8 and Anti-Pattern 4.

### Failure 8: SP&C Finding Incorrectly Diagnosed

**What happened:** The agent reported SP&C as FAIL due to "missing calc." The actual issue was that the calc sheet existed but had a formula error — an extra space in the Total Weekly Penalty function causing the totals to error out.

**Root cause:** The agent either didn't open the calc sheet or didn't read it carefully enough to identify the actual problem. It reported a blanket "missing" when the issue was more nuanced.

**Fix applied:** This reinforces the core principle: actually open and read every document. Don't infer from the absence of a result that the document is missing — it might be present but broken. Report what you actually see.

## General Takeaways

1. **Every piece of feedback represents a class.** If Max says "methanol is missing distance evidence," check distance evidence for EVERY transport category. If he says "diesel headers need units," check headers for EVERY calc sheet.

2. **The checklist is a report, not a to-do list.** Every entry should describe a completed check with specific values, not an instruction to perform a check.

3. **Context fatigue is real and predictable.** After ~100+ checklist items in a long session, quality degrades. The agent should self-monitor and recommend a fresh session rather than producing template-filled output.

4. **The three-layer chain is the backbone.** Certify value → Certify evidence → Drive folder. Every break is a FAIL. This is the single most important structural concept in site emissions QA.

5. **BCU eligibility requires exhaustive checking.** No automated guardrail prevents erroneous BCU applications. The agent must check every eligible component and every applied BCU, every time. The BCU Quant sheet is the reconciliation tool — use it.
