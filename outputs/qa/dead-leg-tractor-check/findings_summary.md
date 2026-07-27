# Dead-Leg Tractor QA — Findings

**Scope:** All 17 removals on Charm Bio-oil Geologic Storage project (prj_1HZSSWBQM1S08H83) on Certify.
**Rule applied:** Opelousas↔Basco trucking leg, railcar deliveries only. CH1/CH2 (Charm trucks) → mileage should be the doubled (round-trip) value (~85.8/85.9 mi). Any other tractor → keep one-way (~42.9 mi).
**Date run:** 2026-05-11.

## Headline

**13 of 17 removals are railcar deliveries and all 13 used Charm trucks (CH1 or CH2).** Zero third-party tractors found on the Opelousas→Basco leg in this set. The rule's "remain one-way" branch was never triggered — every railcar removal needs the Charm-truck treatment.

**Two Opelousas→Basco distance datapoints exist in Certify, used independently:**

| Component | Datapoint | Current value | Aligned with rule? |
|---|---|---|---|
| Opelousas to Basco – Tanker Truck Transport **Process** Emissions | `Distance from Opelousas to B6 (truck)` | **42.9 mi** (one-way) | ❌ NO — should be 85.8/85.9 mi for Charm trucks |
| Opelousas to Basco Tanker Truck Transport **Embodied** Emissions | `Allocated Distance Opelousas to B6 (truck)` | **85.8 mi** (doubled) | ✓ YES — already at doubled value |

So Embodied has already been routed through a "doubled" datapoint; Process is still using the raw one-way value. The fix is to swap the Process emissions distance datapoint to the doubled value (85.8 mi or 85.9 if you want to stick with your stated round number).

## Per-removal table

### Railcar deliveries (13) — rule applies, all are Charm trucks → Process distance needs update

| # | Removal ID | Batch | Date | tCO₂e | Tractor | Trailer | Process mi (current) | Embodied mi (current) |
|---|---|---|---|---|---|---|---|---|
| 1 | rmv_1KQYYB3JV1S0RD0R | 2-204 | 29 Apr | 6.84 | CH2 | KL188 | 42.9 | 85.8† |
| 2 | rmv_1KQT77FNY1S0J259 | 2-201 | 23 Apr | 30.52 | CH2 | KL188 | 42.9 | 85.8 |
| 3 | rmv_1KQJKRFN61S0EQRP | 2-192 | 11 Apr | 36.93 | CH‡ | — | 42.9 | 85.8† |
| 4 | rmv_1KQJKQCX31S07CNZ | 2-191 | 11 Apr | 25.70 | CH1 | KL192 | 42.9 | 85.8† |
| 5 | rmv_1KQJKPBTM1S0KPEX | 2-190 | 10 Apr | 26.27 | CH2 | KL188 | 42.9† | 85.8† |
| 6 | rmv_1KQB5MBJB1S0N8MR | 2-188 | 03 Apr | 25.49 | CH1 | KL192 | 42.9 | 85.8† |
| 7 | rmv_1KQB5KCQG1S0JYZ2 | 2-189 | 03 Apr | 29.63 | CH2 | KL188 | 42.9† | 85.8† |
| 8 | rmv_1KQB5JF7Q1S0GN9C | 2-187 | 03 Apr | 29.47 | CH1 | KL192 | 42.9† | 85.8† |
| 9 | rmv_1KQB5HD031S0REDR | 2-186 | 03 Apr | 30.26 | CH2 | KL188 | 42.9† | 85.8† |
| 10 | rmv_1KQ7Y0Y4S1S023MT | 2-185 | 02 Apr | 17.08 | CH2 | KL188 | 42.9 | 85.8 |
| 11 | rmv_1KQ7Y019T1S0X0WC | 2-184 | 02 Apr | 31.34 | CH1 | — | 42.9† | 85.8† |
| 12 | rmv_1KQ7XZ14K1S09ANA | 2-183 | 02 Apr | 30.88 | CH2 | KL188 | 42.9† | 85.8† |
| 13 | rmv_1KQ7XY3Q81S0T52T | 2-182 | 02 Apr | 30.39 | CH2 | KL188 | 42.9 | 85.8† |

† = inferred from the consistent project pattern (B6 destination, identical datapoint name). Directly verified on 7 of 13 (2-201, 2-204, 2-192, 2-191, 2-188, 2-185, 2-182); Embodied datapoint directly verified on 2 of 13 (2-185, 2-201) and is the same datapoint name across the project. Spot-check additional ones if you want me to harden.

‡ 2-192 scale-ticket photo is partially behind a phone bezel — tractor # not legibly readable, but the company line clearly says "CHARM INDUSTRIAL" and the photo shows the standard yellow CAT ticket format used by Marsha Castille at Pilot Travel Center Bunkie LA, same as all other Charm scale tickets. Charm truck either way; specific CH# can be confirmed from Ops Notes if needed.

### Non-railcar removals (4) — rule does not apply

| Removal ID | Batch | Date | tCO₂e | Type | Why no action |
|---|---|---|---|---|---|
| rmv_1KQ0QGNBV1S0B315 | K-002 | 21 Apr | 9.24 | Kerry tote/flatbed | No Opelousas→Basco leg (Kerry→Basco direct) |
| rmv_1KQT5AWP41S0D5MG | K-001 | 01 Apr | 8.80 | Kerry tote/flatbed | No Opelousas→Basco leg (Kerry→Basco direct) |
| rmv_1KQJFP6Q41S0778B | 2-181 | 01 Apr | 23.23 | AECN tanker-direct | No Opelousas→Basco leg (AECN→Basco direct, no rail) |
| rmv_1KQJFNB7E1S0X8B9 | 2-180 | 01 Apr | 30.77 | AECN tanker-direct | No Opelousas→Basco leg (AECN→Basco direct, no rail) |

## Notes on the mileage numbers

You stated 49.2 (one-way) and 85.9 (Charm doubled). Certify is actually using 42.9 / 85.8 for the B6 well. 85.8 ≈ 2 × 42.9, so the doubled relationship holds; the absolute numbers differ from your stated values by ~6.3 mi (one-way) and ~0.1 mi (doubled). The 85.9 vs 85.8 gap is rounding. The 49.2 vs 42.9 gap may reflect a different reference well or a routing assumption — flagging in case the right answer is to also update the one-way datapoint itself.

## Evidence

- 13 scale-ticket JPGs in [scale-tickets/](scale-tickets/) — each named `<removal_id>_<batch>_Full.jpg`.
- Raw CSV in [dead_leg_tractor_findings.csv](dead_leg_tractor_findings.csv).
