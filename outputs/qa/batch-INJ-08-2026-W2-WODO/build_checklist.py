#!/usr/bin/env python3
"""Build the Charm WODO QA checklist for batch INJ-08-2026-W2."""
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "skills" / "qa" / "batch-qa-aecn" / "scripts"))
from checklist_lib import build_with_validation, BuildAborted  # noqa: E402

LOG = HERE / "batch_INJ-08-2026-W2-WODO_source_reads.json"
OUT = HERE / "Charm_WODO_QA_Checklist_INJ-08-2026-W2.xlsx"

DERIVED = {
    "sum_gross_kg": 19583.0,
    "sum_net_produced_kg": 18603.8,
    "sum_net_injected_kg": 18470.52,
    "sum_standard_loss_kg": 133.28,
    "delta_gross_kg": 0.0,
    "delta_net_produced_kg": 0.0,
    "delta_net_injected_kg": 0.0,
    "uncertainty_expected_kg": 19.27766,
    "uncertainty_per_tote_kg": 1.13398,
    "uncertainty_delta_kg": 0.0,
    "c_uncertainty_expected_pct": 0.2616,
    "weighted_ci_recomputed": 0.9694719419,
    "production_emissions_recomputed_kg": 18035.86211,
    "seq_recomputed_t": 44.296,
    "process_recomputed_t": 3.255,
    "embodied_recomputed_t": 0.197,
    "pyrolysis_recomputed_t": 18.036,
    "net_recomputed_t": 25.879,
    "batch_share_of_truck": 0.85,
    "batch_mileage_allocation_mi": 1020.85,
    "bcu_kg": 3255,
    "n_totes": 17,
    "lb_per_weighing_event": 2.5,
}

P, F, FL, NA = "Pass", "Fail", "Flag", "N/A"

ROWS = [
    ("SECTION 1 — BATCH FOLDER",),
    ("1.1", "Is there testing in the testing folder for the batch?", P,
     "Testing subfolder holds two certificates, one per oil type in the week. The WODO one is "
     "'8-2026-W2 WODO - SR26-04856.001.pdf', SGS order 5482329, client ID '8-2026-W2 WODO', product "
     "description 'Oil - WODO', sampled at Fort Lupton CO, received 13-Aug-2026 10:00, completed "
     "13-Aug-2026 14:31. Read from the PDF: carbon 65.4 % (m/m) by ASTM D5291 Method C, hydrogen 8.4 %, "
     "nitrogen <0.75 %, kinematic viscosity at 40 C 1136 cSt, acid number 57 mg KOH/g, density at 15 C "
     "1.188 g/cm3. Carbon and hydrogen carry a lab '#' note (result outside the method's precision-study "
     "range) — a lab QA flag, not a missing or unusable result; carbon content is present, which is what "
     "this item turns on. [log:lab_results]",
     "VR Appendix 1"),
    ("1.2", "Are Ops Notes in the folder and fully completed?", P,
     "'INJ-08-2026-W2 Ops Notes' is in the batch folder, eight tabs. The WODO tab carries a complete "
     "17-tote ledger with no blank cells in any populated row: tag, gross mass, tote mass, net oil "
     "produced, standard loss, net oil injected, production period, carbon intensity, production "
     "emissions and scale uncertainty are all filled for every tote. Every summary cell resolves to a "
     "number with no formula errors: 19583.0, 18603.8, 18470.52, 0.9694719419, 18035.86211 and 19.27766. "
     "The header block carries batch ID INJ-08-2026-W2 and week 2026-08-01 to 2026-08-08. "
     "[log:ops_notes_totals, totes]",
     "VR Appendix 1"),
    ("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", P,
     "Under the weekly time-block schema the shipment tracker is the Ops Notes tab 'WODO Shipments & EE "
     "Allocation'. It covers this batch completely: shipping order COLA28, 20 totes on the truck, 17 "
     "batch-relevant (=COUNTA(WODO!A11:A27), a live formula reading the WODO tab directly rather than an "
     "independently-typed count), Charm CO to Basco LA one-way distance 1201 mi, and a full EE allocation "
     "row with batch share, mileage and allocated miles. [log:shipment_tracker_location, "
     "shipment_tracker_roster, shipment_tracker_truck]",
     "VR Appendix 1"),

    ("SECTION 2 — OPS NOTES",),
    ("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", P,
     "Ops Notes reports 19583.0 kg at B29 with formula =SUM(B11:B27). Summing the 17 ledger rows "
     "independently reproduces 19583.0 kg exactly, a delta of 0.0 kg. The cell is a live SUM over the "
     "gross-mass column, not a typed constant. [log:_derived_values.sum_gross_kg, "
     "_derived_values.delta_gross_kg, ops_notes_totals]",
     "Ops Notes WODO B29"),
    ("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", P,
     "Ops Notes reports 18603.8 kg at D29 with formula =SUM(D11:D27), each per-tote cell a live formula "
     "=B{row}-C{row} against a uniform 57.6 kg tote tare. Summed independently across all 17 totes: "
     "18603.8 kg against the reported 18603.8, a delta of 0.0 kg. [log:_derived_values.sum_net_produced_kg, "
     "_derived_values.delta_net_produced_kg, totes]",
     "Ops Notes WODO D29"),
    ("2.3", "Is the 'Total Oil in Batch' value correctly computed (WODO: net-in-tote less Standard Loss per tote)?", P,
     "Reported 18470.52 kg at F29 with formula =SUM(F11:F27). Each per-tote figure is "
     "=D{row}-E{row}, where E11:E27 all reference $L$8, the 2026 WODO Standard Loss constant of 7.84 "
     "kg/tote (mean + 1 SD, hyperlinked to the Tote Loss Dataset). Standard Loss IS applied, correctly — "
     "this is the WODO branch, not Aqueous. Summed independently: 18603.8 - (7.84 x 17) = 18603.8 - "
     "133.28 = 18470.52 kg, a delta of 0.0 kg against the reported total, and the sheet's own Standard "
     "Loss column total (E29) is 133.28 kg, matching. [log:_derived_values.sum_net_injected_kg, "
     "_derived_values.delta_net_injected_kg, _derived_values.sum_standard_loss_kg, ops_notes_totals]",
     "Ops Notes WODO F29 / v1.2 6.5"),
    ("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", P,
     "Reported 19.27766 kg at J29 with formula =SUM(J11:J27) over per-tote cells that each read "
     "=2.5*$L$4, where L4 is the sheet's kg-per-lb constant 0.453592. Recomputed: 2.5 x 0.453592 = "
     "1.13398 kg per tote, times 17 totes = 19.27766 kg, a delta of 0.0 kg. This is the Charm per-tote "
     "weighing precision, not AECN's 72.57 kg per-truck figure. [log:_derived_values.uncertainty_expected_kg, "
     "_derived_values.uncertainty_per_tote_kg, _derived_values.uncertainty_delta_kg, "
     "_derived_values.lb_per_weighing_event, _derived_values.n_totes]",
     "Isometric Standard S3.7.3"),

    ("SECTION 3 — BIO-OIL SHIPMENT TRACKER",),
    ("3.1", "Are totes for the RP correctly identified?", P,
     "All 17 WODO totes for the week are identified on the allocation tab as batch-relevant, and the tote "
     "count there (17) is not independently typed — it is =COUNTA(WODO!A11:A27), a live formula counting "
     "rows directly off the WODO tab. Because the tracker computes its roster count from the source tab "
     "rather than maintaining a second, separately-entered list, the two-sheets-drift failure mode this "
     "item is designed to catch cannot occur here by construction. [log:shipment_tracker_roster, totes]",
     "Ops Notes WODO / allocation tab"),
    ("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", P,
     "Same reasoning as 3.1: the allocation tab's batch-relevant-tote count (D6=17) is a live formula "
     "over the WODO tab's own tote rows (A11:A27), not an independent transcription, so there is nothing "
     "for it to disagree with. All 17 tags on the WODO tab (301011 through 301293) are WODO-fraction, "
     "matching the single shipping order COLA28 the allocation tab records. [log:shipment_tracker_roster, "
     "totes]",
     "WODO Shipments & EE Allocation tab"),
    ("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", P,
     "Every computed cell was opened and its formula read, not inferred from appearance. Batch share of "
     "truck E12 = '=IFERROR(D12/C12,\"\")'. Allocated miles G12 = '=IFERROR(E12*F12,\"\")'. Mileage F12 = "
     "'=$B$8'. The totals row is live too: C14 = '=SUM(C12)', D14 = '=SUM(D12)', G14 = '=SUM(G12)'. Every "
     "computed output is a formula referencing tote counts and the distance input; none is a typed "
     "constant. The only hard value in the chain is the distance itself at B8 (1201), an input rather "
     "than a computed output, evidenced by the routing map. [log:shipment_tracker_cells_are_formulas]",
     "Auditability"),
    ("3.4", "Are computed outputs computed correctly?", P,
     "Reproduced independently against the spec. Batch share of truck = 17 batch-relevant totes / 20 "
     "totes on truck COLA28 = 0.85, matching the sheet. Allocated miles = 0.85 x 1201 = 1020.85 mi, "
     "matching G12 exactly. This batch shares its truck with 3 non-WODO totes (20 total, 17 batch-"
     "relevant), so unlike a batch that takes the whole truck, the embodied share here is genuinely "
     "apportioned rather than defaulting to 1.0. Mileage is one-way throughout with no round-trip "
     "doubling, correct for a per-batch truck-share allocation (not the round-trip scenario the doubling "
     "rule addresses). [log:_derived_values.batch_share_of_truck, "
     "_derived_values.batch_mileage_allocation_mi, shipment_tracker_truck]",
     "WODO Shipments & EE Allocation tab"),
    ("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", P,
     "The allocation tab does not restate a per-tote roster with tag/fraction/gross/PP columns — it "
     "carries only the aggregate batch-relevant count (17), which is itself a live formula over the WODO "
     "tab's tote rows (see 3.1/3.2). There is therefore no second, independently-maintained tote list to "
     "compare against and no possibility of a per-attribute mismatch of the kind this item is designed to "
     "catch; the WODO tab is the single source of truth for tag, fraction, gross mass and production "
     "period for all 17 totes. [log:shipment_tracker_roster, totes]",
     "WODO Shipments & EE Allocation tab vs Ops Notes"),

    ("SECTION 4 — CERTIFY: INJECTION SEQUESTRATION",),
    ("4.1", "Does the C content in the testing match the C content in the Sequestration component?", P,
     "Certificate SR26-04856.001 reports carbon 65.4 % (m/m) by ASTM D5291 Method C, read from the PDF. "
     "The Certify sequestration component modal shows carbon content of product 65.4 %. Exact match. "
     "[log:lab_results, certify_components]",
     "Certify cmp_1M0DA1NG01S0EC8P"),
    ("4.2", "Is the C content in the Sequestration component properly evidenced (test copy plus Ops Notes copy)?", P,
     "The carbon content datapoint shows 2 sources in the component modal. Expanding the source list "
     "returns 'INJ-08-2026-W2 Ops Notes.xlsx' and '8-2026-W2 WODO - SR26-04856.001.pdf' — both required "
     "evidence types, linked to the datapoint itself rather than only at removal level. Confirmed "
     "independently from the Sources tab (6 sources total, this certificate maps to exactly this "
     "datapoint). [log:certify.attachment_map, certify_sources_tab_files]",
     "Certify Sources tab"),
    ("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS: mass of product 18,470.52 kg plus or minus 19.28 kg. The Ops "
     "Notes uncertainty cell is 19.27766 kg, which rounds to the displayed 19.28. Match. [log:certify_components, "
     "_derived_values.uncertainty_expected_kg]",
     "Certify cmp_1M0DA1NG01S0EC8P INPUTS"),
    ("4.4", "Does the C content have the appropriately computed 0.4 % relative uncertainty?", P,
     "Certify shows carbon content 65.4 plus or minus 0.2616 %. Recomputed: 0.004 relative uncertainty "
     "times the 65.4 % carbon content gives 0.2616 percentage points on a value expressed in percent. "
     "Exact match. "
     "[log:certify_components, _derived_values.c_uncertainty_expected_pct]",
     "Certify cmp_1M0DA1NG01S0EC8P INPUTS"),

    ("SECTION 5 — CERTIFY: TRANSPORT PROCESS EMISSIONS",),
    ("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", P,
     "The component modal shows 0.1384 kgCO2e per tonne-mile. The 2026 tab of the Standard Emission "
     "Factors sheet, row 7, 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck', gives a final "
     "quantity of 0.0001384 MT CO2e per tonne-mile from GLEC V3.2 2025, marked Updated. Same figure in "
     "native units, and it is the flatbed row (not tanker), correct for tote-on-flatbed delivery. The "
     "VVB guidance for this period independently confirms 0.1384 kg/tonne-mile as 'the factors the "
     "equivalent WODO tote transport has always used.' [log:standard_efs_2026, certify_components, "
     "vvb_guidance.sections_present]",
     "Standard EFs 2026 tab row 7"),
    ("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", P,
     "Distance in Certify is 1,201 mi. The routing map attached to this removal was pulled at full "
     "resolution (1842x863 px, via the signed storage URL rather than the shrunk in-app preview) and read "
     "directly. It offers three routes to 4675 LA-115, St Landry, LA 71367: via US-287 S at 1,132 mi "
     "(17 hr 22 min, marked fastest); via US-287 S, US-287 S and I-20 E at 1,129 mi (17 hr 32 min); and "
     "via I-70 E at 1,201 mi (17 hr 36 min, tolls). Certify uses 1,201, the longest of the three. "
     "[log:google_maps_options, certify_components]",
     "CO to Basco Routing Map.png"),
    ("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", FL,
     "The value is right and the label is wrong. Mass of load in Certify is 19,583 kg, exactly the Ops "
     "Notes Total Mass Transported of 19583.0 kg — the gross basis including tote tare, not Total Oil "
     "Produced (18,603.8) and not Total Oil in Batch (18,470.52). But the datapoint carrying it is titled "
     "'QOWV Trip Count Source' on a WODO removal — QOWV is Charm's aqueous fraction, not WODO, and the "
     "name doesn't even describe a mass ('Trip Count'). Flag rather than Fail because the quantity "
     "feeding the calculation is correct and the emission reproduces exactly. This is a recurring pattern "
     "on WODO batches — INJ-07-2026-W1 carried 'WODO - Mass (Net) (CO to KS)' (wrong basis word, wrong "
     "state) and INJ-07-2026-W2 carried 'QOWV (Aqueous Oil) - Mass (Net) (CO to KS)' (wrong oil type, "
     "wrong basis word, wrong state) on the same slot — worth raising with Garrett/ops as a template "
     "default to fix at the source rather than re-flagging every week. [log:certify_components, "
     "certify.attachment_map, ops_notes_totals]",
     "Certify cmp_1M0DA1NG01S0214B"),
    ("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", P,
     "The mass of load datapoint shows 1 source: 'INJ-08-2026-W2 Ops Notes.xlsx', linked to the specific "
     "datapoint rather than only at removal level. [log:certify.attachment_map]",
     "Certify Sources tab"),
    ("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS: mass of load 19,583 kg plus or minus 19.28 kg, matching the "
     "Ops Notes uncertainty exactly (19.27766 rounds to 19.28) and identical to the mass-of-product "
     "uncertainty on the sequestration component — correct, since it is the same 17 totes weighed once "
     "each. [log:certify_components, _derived_values.uncertainty_expected_kg]",
     "Certify cmp_1M0DA1NG01S0214B INPUTS"),

    ("SECTION 6 — CERTIFY: TRANSPORT EMBODIED EMISSIONS",),
    ("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", P,
     "The component modal shows 0.19279 kgCO2e per mile. The 2026 tab row 12, 'Vehicle Embodied "
     "Emissions --Non-Tanker Truck', gives 0.0001927908256 MT CO2e per mile from GLEC V3.2 2025, marked "
     "Updated. Same value in native units, correctly the non-tanker row, and the datapoint's own label "
     "reads 'Emissions Factor - Vehicle Embodied Emissions - Non-Tanker Truck' — label and source row "
     "agree, unlike the mass-of-load naming issue at 5.3. [log:standard_efs_2026, certify_components]",
     "Standard EFs 2026 tab row 12"),
    ("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", P,
     "Certify aggregate distance is 1,020.9 mi (displayed, 2 sig figs after the decimal). The allocation "
     "tab's Allocated Miles at G12 resolves to 1020.85 mi, which rounds to the Certify figure exactly. "
     "This is a genuinely apportioned share (0.85 of the truck), not the full one-way distance — this "
     "batch shares its truck with 3 non-WODO totes this week, unlike prior weeks where WODO took the "
     "whole truck. [log:_derived_values.batch_mileage_allocation_mi, shipment_tracker_cells_are_formulas, "
     "certify_components]",
     "Certify cmp_1M0DA1NG01S0NP00 INPUTS"),
    ("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", P,
     "The aggregate distance datapoint carries 2 sources: 'CO to Basco Routing Map.png' and 'INJ-08-2026-"
     "W2 Ops Notes.xlsx'. Under the weekly time-block schema the Ops Notes workbook IS the shipment "
     "tracker (its 'WODO Shipments & EE Allocation' tab derives the 1,020.85 mi through the live formulas "
     "read at 3.3/3.4), so this single file satisfies both the tracker and the mass/allocation-basis "
     "evidence roles the older three-document convention split apart. No standalone 'Charm Contents' "
     "sheet exists for this batch, or for any WODO batch under the current schema (validated absent on "
     "INJ-06-2026-W1 through INJ-07-2026-W2) — its role is folded into the same Ops Notes workbook. A "
     "verifier can reconstruct the mileage fully from the two attached documents. "
     "[log:certify.attachment_map, shipment_tracker_location, shipment_tracker_cells_are_formulas]",
     "Certify Sources tab"),

    ("SECTION 7 — CERTIFY: PRODUCTION EMISSIONS",),
    ("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", P,
     "The batch draws on three production periods: February 2026 (3 totes, CI 0.84989612258998), June "
     "2026 (9 totes, CI 1.1105355635937064) and the H2 2026 rolling 6-month CI (5 totes actually produced "
     "in July 2026, CI 0.795241). All three are captured in a single aggregated component, 'Pyrolysis - "
     "Charm WODO PP Emissions' at 18.036 tCO2e, carrying a production-mass-weighted blended intensity of "
     "0.9695 that reconciles to the per-tote sum: Ops Notes I29 = SUM of per-tote (CI x Net Oil Produced) "
     "= 18035.86211 kg = 18.036 t against Certify's 18.036 t. No period is omitted. Aggregating periods "
     "into one weighted component is not a finding — no primary source requires per-period component "
     "granularity. [log:production_periods, _derived_values.production_emissions_recomputed_kg, "
     "certify_components]",
     "Certify Components tab"),
    ("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", P,
     "Certify carries 0.9695 tCO2e per tonne. The Ops Notes weighted average at H29 is 0.9694719419, "
     "computed as SUMPRODUCT(D11:D27,H11:H27)/SUMIF(...) — total production emissions over total net oil "
     "produced. Match to displayed precision. Each production period's CI is applied to the right totes: "
     "the H2 2026 rolling CI (0.795241) is applied ONLY to the 5 totes actually produced in July 2026 "
     "(301233/301234/301235/301243/301259), consistent with the corrected Charm CI policy that the "
     "rolling/blended figure governs oil produced within the new window, not older-production oil merely "
     "injected later (workspace memory project_charm_h1_2026_ci_policy.md, itself corrected 2026-08-26 "
     "against Charm's monitoring-decoupling response doc); the 12 Feb/Jun-produced totes retain their "
     "per-month PP CIs. [log:_derived_values.weighted_ci_recomputed, ops_notes_totals, production_periods, "
     "certify_components]",
     "Ops Notes WODO H29"),
    ("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", P,
     "The carbon intensity datapoint ('WODO Tote - Carbon Intensity') shows 1 source, "
     "'INJ-08-2026-W2 Ops Notes.xlsx', linked to the datapoint itself. That is the required evidence "
     "standard for Charm production intensity — the Ops Notes weighted average across the totes used in "
     "the injection; a standalone PP Summary is not required. [log:certify.attachment_map]",
     "Certify Sources tab"),
    ("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", P,
     "Certify mass is 18,603.8 kg (component 'WODO Tote - Mass (Gross-Tote) for pyrolysis'). The Ops "
     "Notes sum of net oil produced across all 17 totes is 18603.8 kg (D29), a delta of 0.0 kg. The "
     "component correctly uses net-in-tote (produced mass), not net-in-injection-batch (18,470.52) — "
     "production emissions attach to what was produced, not to what survived transfer. "
     "[log:_derived_values.sum_net_produced_kg, _derived_values.delta_net_produced_kg, certify_components]",
     "Certify cmp_1M0DA1NG01S049EM INPUTS"),
    ("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", P,
     "Read from the component modal INPUTS: mass 18,603.8 kg plus or minus 19.28 kg. That matches the Ops "
     "Notes uncertainty (19.27766, rounds to 19.28) and the expected 1.13398 kg per tote across 17 totes. "
     "Uncertainty is present on this dominant input — pyrolysis is 69.69 % of activities and 40.72 % of "
     "gross sequestration, well above the negligible-input threshold that would qualify for a v1.2 §6.5 "
     "omission carve-out. [log:certify_components, _derived_values.uncertainty_expected_kg]",
     "v1.2 6.5.1"),
    ("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", P,
     "No Charm Contents sheet exists for this batch or for any WODO batch under the current weekly "
     "time-block schema (validated absent on prior batches INJ-06-2026-W1 through INJ-07-2026-W2 by Drive "
     "enumeration and Certify Sources-tab review). The per-period mass breakdown it used to carry now "
     "lives directly in the Ops Notes WODO tab, column G (production period) against column D (net oil "
     "produced), and the Ops Notes is attached to this mass datapoint (1 source, confirmed by expanding "
     "the source list). Same basis accepted on every prior WODO batch, so this passes on the successor "
     "document. [log:certify.attachment_map, shipment_tracker_location]",
     "VR Appendix 1"),

    ("SECTION 8 — OTHER",),
    ("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total meet or exceed the transport-process sum?", P,
     "There is one diesel transport-process emission on this removal, the flatbed leg at 3.255 tCO2e, and "
     "it is offset exactly. Reductions carries a 'BCU - Transport Process' Constant CO2 reduction of 3,255 "
     "kgCO2e, evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf'. Recomputing the process "
     "emission from primary sources gives 19.583 t x 1201 mi x 0.0001384 MT per tonne-mile = 3.2551 t, so "
     "the 3,255 kgCO2e offset equals it to the tonne. Embodied emissions are correctly not offset. "
     "[log:_derived_values.bcu_kg, _derived_values.process_recomputed_t, certify_components]",
     "Certify cmp_1M0DC8EXN1S00NER"),

    ("SECTION 9 — AQUEOUS BUFFERING (LCS)",),
    ("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist?", NA,
     "Not applicable to a WODO batch — LCS is an aqueous pre-treatment. Confirmed rather than assumed: "
     "the Ops Notes WODO tab (A1:O33) and WODO Shipments & EE Allocation tab (A1:G34) were dumped cell "
     "by cell with no LCS/calcium/buffer column or reference found, and all 5 Certify components were "
     "enumerated with no LCS component among them. [log:lcs_use_kg_detail, certify_components]",
     "Aqueous-only item"),
]

BOLD = Font(bold=True, size=11)
BODY = Font(size=10)
TITLE = Font(bold=True, size=14)
HDR = PatternFill("solid", fgColor="D6E4F0")
FAIL_FILL = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT = Font(size=10, color="996600")
NA_FONT = Font(size=10, italic=True, color="808080")

HEADER_ROW = 12


def build_workbook(rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "WODO QA INJ-08-2026-W2"

    ws.cell(row=1, column=1, value="Charm WODO Injection Batch QA Checklist").font = TITLE
    meta = [
        ("Batch ID", "INJ-08-2026-W2 (WODO)"),
        ("Reporting Period", "August 1 - August 31 2026 RP; injection week 2026-08-01 to 2026-08-08 (Certify window 02-08 Aug 2026)"),
        ("Reviewer", "Claude (MRV QA agent)"),
        ("Date", "2026-08-27"),
        ("Injection Site", "Basco 6, Louisiana (Class V UIC)"),
        ("Oil Type", "WODO (Charm-produced, Fort Lupton CO), 17 IBC totes"),
        ("Production Periods", "February 2026 (3 totes, CI 0.8499); June 2026 (9 totes, CI 1.1105); H2 2026 rolling CI 0.795241 (5 totes produced Jul 2026)"),
        ("Certify Removal ID", "rmv_1M0DA1NG01S0J6WC"),
        ("Certify Net", "25.879 tCO2e = Sequestrations 44.296 + BCU 3.255 - Activities 21.488 - Uncertainty 0.184"),
    ]
    r = 2
    for k, v in meta:
        ws.cell(row=r, column=1, value=k).font = BOLD
        ws.cell(row=r, column=2, value=v).font = BODY
        r += 1

    hdrs = ["#", "Check", "Status", "Evidence / Finding", "Reference"]
    for i, h in enumerate(hdrs, start=1):
        c = ws.cell(row=HEADER_ROW, column=i, value=h)
        c.font = BOLD
        c.fill = HDR
        c.alignment = Alignment(vertical="center")

    r = HEADER_ROW + 1
    for row in rows:
        if len(row) == 1:
            c = ws.cell(row=r, column=1, value=row[0])
            c.font = BOLD
            c.fill = HDR
            for col in range(2, 6):
                ws.cell(row=r, column=col).fill = HDR
            r += 1
            continue
        num, check, status, notes, ref = row
        vals = [num, check, status, notes, ref]
        for col, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = BODY
            c.alignment = Alignment(vertical="top", wrap_text=True)
            if status == "Fail":
                c.fill = FAIL_FILL
            elif status == "Flag":
                c.fill = FLAG_FILL
                c.font = FLAG_FONT
            elif status == "N/A":
                c.font = NA_FONT
        r += 1

    r += 1
    c = ws.cell(row=r, column=1, value="Sidebar Observations (no Pass/Fail status - flagged for attention)")
    c.font = BOLD
    c.fill = HDR
    for col in range(2, 6):
        ws.cell(row=r, column=col).fill = HDR
    r += 1

    sidebar = [
        "Lab certificate SR26-04856.001 flags both Carbon (65.4%) and Hydrogen (8.4%) results with '#' — "
        "'Result is outside of test method limits and/or analytical range used in method precision study.' "
        "This is the lab's own precision-study caveat, not a missing or unreliable result, and both values "
        "flow through Certify unchanged and reconcile exactly. Worth a periodic check that ASTM D5291 "
        "Method C remains the right method for this oil's carbon range, given it now recurs across "
        "multiple WODO batches this year.",

        "This is the first WODO batch reviewed this year where the 17 totes do NOT occupy the whole "
        "truck: shipping order COLA28 carried 20 totes, 3 of them non-WODO. The batch share of truck "
        "(0.85) and the resulting embodied-distance allocation (1,020.85 of 1,201 one-way miles) are "
        "genuinely apportioned rather than defaulting to 1.0 as on every prior single-occupant-truck WODO "
        "batch. Worth confirming with ops which fraction the other 3 totes on COLA28 belong to, since "
        "nothing in this batch's own documents says.",

        "The H2 2026 rolling 6-month CI (0.795241) is applied correctly and narrowly in this batch — only "
        "to the 5 totes whose Ops Notes production-period label reads 'July 2026', not to the 12 Feb/Jun-"
        "produced totes riding through this same injection week. This is the corrected reading of the "
        "Charm CI policy (Max reviewed the underlying Isometric monitoring-decoupling response doc "
        "directly on 2026-08-26 after an earlier over-broad verbal ruling): the blended/rolling figure "
        "governs oil PRODUCED in the new window, not older-production oil merely injected later. This "
        "batch is a clean positive example of the policy working as intended.",

        "The Bio-Oil Shipment Tracker role (allocation-tab tote count) is now a live formula reading "
        "directly off the WODO tab rather than an independently re-typed roster. This is a structural "
        "improvement over the older convention items 3.1/3.2/3.5 were originally written to police (two "
        "sheets drifting out of sync) — the tracker literally cannot disagree with the ledger it counts "
        "from. Worth noting in the checklist item text itself going forward, since the current items ask "
        "questions the sheet's own design has made moot.",

        "The Scale Tickets subfolder holds no WODO records this week either — only the four AECN railcar "
        "offload folders. Consistent with every prior WODO batch: the Ops Notes ledger header states tote "
        "tag mass is authoritative for IBC deliveries, so this is expected, not a gap.",
    ]
    for s in sidebar:
        ws.cell(row=r, column=1, value="-").font = BODY
        c = ws.cell(row=r, column=4, value=s)
        c.font = BODY
        c.alignment = Alignment(vertical="top", wrap_text=True)
        r += 1

    r += 1
    counts = {}
    for rr in range(HEADER_ROW + 1, r):
        v = ws.cell(row=rr, column=3).value
        if v in ("Pass", "Fail", "Flag", "N/A"):
            counts[v] = counts.get(v, 0) + 1
    total = sum(counts.values())

    summary = (
        "STATUS SUMMARY: {} Pass - {} Flag - {} Fail - {} N/A  ({} items)  |  "
        "All five Certify components independently recomputed from primary sources and reconcile exactly: "
        "sequestration 18,470.52 kg x 65.4% x 3.667 = 44.296 t; transport process 19.583 t x 1,201 mi x "
        "0.0001384 = 3.255 t; transport embodied 1,020.85 mi x 0.0001927908256 = 0.197 t; pyrolysis "
        "18,603.8 kg x weighted-avg CI 0.9694719419 = 18.036 t; net closes at 25.879 t against Certify's "
        "25.88 t displayed. Both emission factors match the live 2026 Standard EFs tab in native units. "
        "All four Ops Notes totals reconcile to a zero delta across the 17-tote ledger. Uncertainty is "
        "present and correct on all three components that need it, including the dominant pyrolysis mass. "
        "The BCU offsets the flatbed transport-process emission exactly (3,255 kg = 3.255 t). Distance is "
        "the longest of three routes, confirmed from the full-resolution routing map (not the shrunk "
        "in-app preview). All six Certify sources are linked at the specific-datapoint level, not merely "
        "at removal level — attachment gate clean, no evidence gaps. The H2 2026 rolling CI is applied "
        "correctly to only the 5 totes actually produced in July 2026. THE ONE OUTSTANDING ITEM IS A FLAG, "
        "not a Fail: item 5.3, the Transport Process mass-of-load datapoint is titled 'QOWV Trip Count "
        "Source' on a WODO removal — wrong oil type, and doesn't even describe a mass. The value (19,583 "
        "kg) and uncertainty are correct and the emission reproduces exactly, so it does not block "
        "verification. This is a recurring naming-hygiene defect across WODO batches this reporting "
        "period and prior — worth fixing at the Mangrove/ops template level rather than re-flagging every "
        "batch."
        .format(counts.get("Pass", 0), counts.get("Flag", 0), counts.get("Fail", 0), counts.get("N/A", 0), total)
    )
    c = ws.cell(row=r, column=1, value=summary)
    c.font = BOLD
    c.alignment = Alignment(vertical="top", wrap_text=True)

    ws.column_dimensions["A"].width = 7
    ws.column_dimensions["B"].width = 52
    ws.column_dimensions["C"].width = 9
    ws.column_dimensions["D"].width = 100
    ws.column_dimensions["E"].width = 32
    ws.freeze_panes = ws.cell(row=HEADER_ROW + 1, column=1)
    return wb


try:
    build_with_validation(ROWS, LOG, OUT, build_workbook, derived_values=DERIVED)
except BuildAborted as e:
    print("BUILD ABORTED\n", e)
    raise SystemExit(1)
