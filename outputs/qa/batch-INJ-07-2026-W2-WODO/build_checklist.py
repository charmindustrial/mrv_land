#!/usr/bin/env python3
"""Build the Charm WODO QA checklist for batch INJ-07-2026-W2."""
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "skills" / "qa" / "batch-qa-aecn" / "scripts"))
from checklist_lib import build_with_validation, BuildAborted  # noqa: E402

LOG = HERE / "batch_INJ-07-2026-W2-WODO_source_reads.json"
OUT = HERE / "Charm_WODO_QA_Checklist_INJ-07-2026-W2.xlsx"

# Values recomputed independently this session from the primary sources.
DERIVED = {
    "sum_gross_kg": 3246.00,
    "sum_net_produced_kg": 3073.20,
    "sum_net_injected_kg": 3068.00,
    "measured_tote_loss_kg": 5.20,
    "delta_gross_kg": 0.00,
    "delta_net_produced_kg": 0.00,
    "delta_net_injected_kg": 0.00,
    "uncertainty_expected_kg": 3.40194,
    "uncertainty_per_tote_kg": 1.13398,
    "uncertainty_delta_kg": 0.00000,
    "c_uncertainty_expected_pct": 0.1956,
    "weighted_ci_recomputed": 0.7865839125,
    "production_emissions_recomputed_kg": 2417.32968,
    "pe_tote_301041_kg": 817.27944,
    "pe_tote_301089_kg": 800.80992,
    "pe_tote_301128_kg": 799.24032,
    "seq_recomputed_t": 5.501424,
    "process_recomputed_t": 0.539545,
    "embodied_recomputed_t": 0.231542,
    "pyrolysis_recomputed_t": 2.417330,
    "net_recomputed_t": 2.829,
    "batch_mileage_allocation_mi": 1201.0,
    "batch_share_of_truck": 1.0,
    "bcu_kg": 540,
    "process_recomputed_kg": 539.545,
    "lb_per_weighing_event": 2.5,
    "totes_on_truck": 3,
    "batch_relevant_totes": 3,
    "n_totes": 3,
    "net_injected_301041_kg": 1034,
    "net_injected_301089_kg": 1020,
    "net_injected_301128_kg": 1014,
    "tote_301128_inventory_fraction": "QOWV",
    "tote_301128_net_injected_kg": 1014,
    "tote_301128_share_of_batch_pct": 33.05,
    "aqueous_april_ci": 0.1314,
    "aqueous_april_c_pct": 7.86,
    "wodo_april_c_pct": 46.94,
    "c_overstatement_if_aqueous_kg": 1506.0,
    "ci_overstatement_if_aqueous_kg": 665.4,
    "net_exposure_if_aqueous_kg": 840.6,
    "blend_c_pct_if_one_third_aqueous": 35.41,
    "blend_c_pct_if_all_wodo": 48.33,
    "measured_composite_c_pct": 48.90,
    "gap_to_all_wodo_pp": 0.57,
    "gap_to_one_third_aqueous_pp": 13.49,
    "march_wodo_c_pct": 51.06,
    "april_2026_qowv_rows_in_inventory": 34,
    "april_2026_wodo_rows_in_inventory": 13,
    "w1_fraction_matches": 13,
    "w1_totes_checked": 13,
}

P, F, FL, NA = "Pass", "Fail", "Flag", "N/A"

ROWS = [
    ("SECTION 1 — BATCH FOLDER",),
    ("1.1", "Is there testing in the testing folder for the batch?", P,
     "Testing subfolder holds three certificates of analysis, one per oil type in the week. The WODO one is "
     "'CHARM INDUSTRIAL - 7-2026-W2 WODO (SR26-04432.001).pdf', SGS order 5470884, client ID '7-2026-W2 WODO', "
     "product description 'Oil - WODO', sampled at Fort Lupton CO, received 22-Jul-2026 10:20 and completed "
     "22-Jul-2026 13:31. Read from the PDF itself: carbon 48.9 % (m/m) by ASTM D5291 Method C, hydrogen 7.6 %, "
     "nitrogen <0.75 %, kinematic viscosity at 40 C 4.114 cSt, acid number 106 mg KOH/g, density at 15 C "
     "1.180 g/cm3. Carbon content for the fraction is present, which is what this item turns on. Density is "
     "well above the 1.01 g/cm3 formation-fluid threshold. [log:lab_results]",
     "VR Appendix 1"),
    ("1.2", "Are Ops Notes in the folder and fully completed?", P,
     "'INJ-07-2026-W2 Ops Notes' is in the batch folder, eight tabs. The WODO tab carries a complete three-tote "
     "ledger with no blank cells in any populated row: tag, gross mass, tote mass, net oil produced, empty tote "
     "weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty "
     "are all filled for 301041, 301089 and 301128. Every summary cell resolves to a number with no formula "
     "errors: 3246.0, 3073.2, 3068.0, 0.7865839125, 2417.32968 and 3.40194. The header block carries the batch "
     "ID INJ-07-2026-W2 and the week 2026-07-04 to 2026-07-11. [log:ops_notes_totals, totes]",
     "VR Appendix 1"),
    ("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", P,
     "Under the weekly time-block schema the shipment tracker is the Ops Notes tab 'WODO Shipments & EE "
     "Allocation', which carries the full tracker structure: batch summary, the Charm CO to Basco LA one-way "
     "distance, an EE allocation table and a per-shipping-order tote roster. It covers this batch completely — "
     "shipping order COLA18, 3 totes on the truck, 3 batch-relevant, and all three tags rostered with fraction, "
     "production period and batch assignment. The standalone 'Bio Oil Shipment Tracker' sheet was also opened "
     "live and covers only the legacy Apr/May 2026 batches 3-55, 3-56 and 5-10, so it is not the operative "
     "document here. [log:shipment_tracker_location, shipment_tracker_roster, shipment_tracker_truck]",
     "VR Appendix 1"),

    ("SECTION 2 — OPS NOTES",),
    ("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", P,
     "Ops Notes reports 3246.0 kg at B26 with formula =SUM(B11:B24). Summing the three ledger rows independently: "
     "1092.00 + 1078.00 + 1076.00 = 3246.0 kg, a delta of 0.0 kg. The cell is a live SUM over the tote column, not "
     "a typed constant, and the range covers every populated row. [log:_derived_values.sum_gross_kg, "
     "_derived_values.delta_gross_kg, ops_notes_totals]",
     "Ops Notes WODO B26"),
    ("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", P,
     "Ops Notes reports 3073.2 kg. Each per-tote net is a live formula =B{row}-C{row}, and all three were "
     "recomputed: 1092.00-57.60 = 1034.40, 1078.00-57.60 = 1020.40, 1076.00-57.60 = 1018.40. They sum to 3073.2 kg "
     "against the reported 3073.2, a delta of 0.0 kg. The uniform 57.60 kg in column C is the IBC container's own "
     "empty weight, which is the documented basis. [log:_derived_values.sum_net_produced_kg, "
     "_derived_values.delta_net_produced_kg, totes]",
     "Ops Notes WODO D26"),
    ("2.3", "Is the 'Total Oil in Batch' value correctly computed (WODO: net-in-tote less Standard Loss per tote)?", P,
     "Reported 3068.0 kg. Each per-tote figure is =IF(E{row}=\"\",\"\",B{row}-E{row}), that is gross less the "
     "measured post-unload weight of the container: 1092.00-58.00 = 1034, 1078.00-58.00 = 1020, 1076.00-62.00 = "
     "1014. They sum to 3068.0 against the reported 3068.0, a delta of 0.0 kg, and the implied loss of 5.2 kg "
     "closes against the sheet's own 5.2. No Standard Loss column exists and none is applied, which is correct: "
     "Max ruled on INJ-07-2026-W1 that measured actual tote weights are the operative loss basis and that the "
     "fixed 4.73 kg per tote standard loss is not approved for use. [log:_derived_values.sum_net_injected_kg, "
     "_derived_values.delta_net_injected_kg, _derived_values.measured_tote_loss_kg, _derived_values.net_injected_301041_kg, _derived_values.net_injected_301089_kg, _derived_values.net_injected_301128_kg, ops_notes_totals]",
     "Ops Notes WODO F26 / v1.2 6.5"),
    ("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", P,
     "Reported 3.40194 kg at J26 with formula =SUM(J9:J24) over per-tote cells that each read =2.5*$L$4, where L4 "
     "is the sheet's kg-per-lb constant 0.453592. Recomputed: 2.5 x 0.453592 = 1.13398 kg per tote, times 3 totes "
     "= 3.40194 kg, a delta of 0.0 kg. This is the Charm per-tote weighing precision, not AECN's 72.57 kg "
     "per-truck figure. [log:_derived_values.uncertainty_expected_kg, _derived_values.uncertainty_per_tote_kg, "
     "_derived_values.uncertainty_delta_kg, _derived_values.lb_per_weighing_event, _derived_values.n_totes]",
     "Isometric Standard S3.7.3"),

    ("SECTION 3 — BIO-OIL SHIPMENT TRACKER",),
    ("3.1", "Are totes for the RP correctly identified?", P,
     "All three totes are now identified consistently across everything attached to this removal. Tags 301041, "
     "301089 and 301128 appear as WODO on the Ops Notes ledger and on the allocation-tab roster, assigned to "
     "INJ-07-2026-W2 on shipping order COLA18, with production periods March 2026, April 2026 and April 2026. "
     "The conflict raised at first delivery is resolved: the production inventory file that classified tote "
     "301128 as QOWV was detached from this removal on 2026-08-06, verified live at 23:18Z, and the two mass "
     "datapoints it sat on now carry the batch Ops Notes alone. Nothing attached to the removal now contradicts "
     "the WODO classification. The certificate independently supports it — mass-weighting the period carbon "
     "contents gives 48.33 % expected for an all-WODO batch against 35.41 % if that tote had been aqueous, and "
     "SR26-04432.001 measured 48.90 %, which is 0.57 points from the first figure and 13.49 from the second. "
     "[log:shipment_tracker_roster, totes, inventory_bulk_upload, "
     "_derived_values.blend_c_pct_if_all_wodo, _derived_values.blend_c_pct_if_one_third_aqueous, "
     "_derived_values.measured_composite_c_pct, _derived_values.gap_to_all_wodo_pp, "
     "_derived_values.gap_to_one_third_aqueous_pp, lab_results]",
     "Ops Notes WODO / allocation tab / Certify Sources tab"),
    ("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", P,
     "Tag for tag against the Ops Notes ledger: 301041 WODO March 2026, 301089 WODO April 2026, 301128 WODO April "
     "2026, all three assigned to INJ-07-2026-W2 on shipping order COLA18. The allocation tab and the ledger "
     "agree on every tote with no orphans on either side and no tote appearing in a second batch — a workbook-wide "
     "scan for the three tags returns hits only on the WODO tab and its allocation tab, so none of them is also "
     "claimed by the aqueous batch in the same week. The disagreement raised at 3.1 is with the inventory file, "
     "not between these two. [log:shipment_tracker_roster, totes]",
     "Shipment allocation tab A21:E23"),
    ("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", P,
     "Every computed cell was opened and its formula read, not inferred from appearance. Batch share of truck "
     "E12 = '=D12/C12'. Mileage F12 = '=$B$8'. Allocated miles G12 = '=E12*F12'. The totals row is live too: "
     "C13 = '=SUM(C12)', D13 = '=SUM(D12)', G13 = '=SUM(G12)'. Batch mileage allocation C17 = '=G13' and its tote "
     "count D17 = '=D13'. Nine of nine computed outputs are formulas referencing tote counts and the distance "
     "input; none is a typed constant. The only hard value in the chain is the distance itself at B8 (1201), "
     "which is an input rather than a computed output and is evidenced by the routing map. "
     "[log:shipment_tracker_cells_are_formulas]",
     "Auditability"),
    ("3.4", "Are computed outputs computed correctly?", P,
     "Reproduced independently against the spec. Batch share of truck = 3 batch-relevant totes / 3 totes on truck "
     "COLA18 = 1.0, matching the sheet. Allocated miles = 1.0 x 1201 = 1201.0 mi, matching. Batch mileage "
     "allocation = (3 batch totes / 3 totes on truck) x 1201 mi one-way = 1201.0 mi, matching C17. The batch is "
     "the sole occupant of this truck, so it carries the full one-way distance rather than a share of it. "
     "One-way is used throughout with no round-trip doubling, which is correct for the process leg. "
     "[log:_derived_values.batch_share_of_truck, _derived_values.batch_mileage_allocation_mi, "
     "shipment_tracker_truck]",
     "Shipment allocation tab"),
    ("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", P,
     "Compared attribute by attribute between the allocation tab and the ledger. Tags 301041, 301089, 301128 "
     "match. Fraction reads WODO on both sides for all three. Production period matches on both sides: March 2026 "
     "for 301041, April 2026 for 301089 and 301128. Gross mass is carried only on the ledger (1092.00, 1078.00, "
     "1076.00) and the allocation tab does not restate it, so there is nothing to contradict. No mismatch on any "
     "attribute between these two documents. [log:shipment_tracker_roster, totes]",
     "Shipment allocation tab vs Ops Notes"),

    ("SECTION 4 — CERTIFY: INJECTION SEQUESTRATION",),
    ("4.1", "Does the C content in the testing match the C content in the Sequestration component?", P,
     "Certificate SR26-04432.001 reports carbon 48.9 % (m/m) by ASTM D5291 Method C, read from the PDF. The "
     "Certify sequestration component modal shows carbon content of product 48.9 %. Exact match, no rounding "
     "gap. The Ops Notes summary tab carries the same 48.9 % against composite sample ID '7-2026-W2 WODO'. "
     "[log:lab_results, certify_components, summary_tab_wodo_row]",
     "Certify cmp_1KYWWAQ3J1S05G96"),
    ("4.2", "Is the C content in the Sequestration component properly evidenced (test copy plus Ops Notes copy)?", P,
     "The carbon content datapoint shows 2 sources in the component modal and both required evidence types are "
     "there. Expanding the source list on the datapoint returns the laboratory certificate 'CHARM INDUSTRIAL - "
     "7-2026-W2 WODO (SR26-04432.001).pdf' alongside 'INJ-07-2026-W2 Ops Notes.xlsx'. Confirmed from the Sources "
     "tab in the other direction as well, where the certificate maps to exactly this datapoint. "
     "[log:certify_attachment_map, certify_sources]",
     "Certify Sources tab"),
    ("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS section: mass of product 3,068 kg plus or minus 3.40194 kg. The Ops "
     "Notes uncertainty cell is 3.40194 kg. Exact match, and it is an absolute kilogram figure rather than a "
     "percentage. It equals the expected 1.13398 kg per weighing event across 3 totes. "
     "[log:certify_components, _derived_values.uncertainty_expected_kg]",
     "Certify cmp_1KYWWAQ3J1S05G96 INPUTS"),
    ("4.4", "Does the C content have the appropriately computed 0.4 % relative uncertainty?", P,
     "Certify shows carbon content 48.9 plus or minus 0.1956 %. Recomputed: 0.489 x 0.004 = 0.001956, which is "
     "0.1956 percentage points on a value expressed in percent. Exact match. The Ops Notes summary tab derives it "
     "the same way, with the testing uncertainty held as 0.004 and the carbon content uncertainty as the product. "
     "[log:certify_components, _derived_values.c_uncertainty_expected_pct, summary_tab_wodo_row]",
     "Certify cmp_1KYWWAQ3J1S05G96 INPUTS"),

    ("SECTION 5 — CERTIFY: TRANSPORT PROCESS EMISSIONS",),
    ("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", P,
     "The component modal shows 0.1384 kgCO2e per tonne-mile. The 2026 tab of the Standard Emission Factors sheet, "
     "row 6, 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck', gives a final quantity of 0.0001384 "
     "MT CO2e per tonne-mile from GLEC V3.2 2025 and is marked Updated for 2026. Same number in native units. It "
     "is the flatbed row, not the tanker row, which is correct for tote-on-flatbed delivery. The same value "
     "appears in the emission-factor tables of both production period summaries read this session. "
     "[log:standard_efs_2026, certify_components]",
     "Standard EFs 2026 tab row 6"),
    ("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", P,
     "Distance in Certify is 1,201 mi. The routing map attached to this removal was downloaded from Certify and "
     "read from its pixels. It offers three routes to 4675 LA-115, St Landry, LA 71367: via US-287 S at 1132 mi "
     "and 17 hr 22 min, marked fastest; via US-287 S and I-20 E at 1129 mi; and via I-70 E at 1201 mi and 17 hr "
     "36 min. Certify uses 1201, the longest of the three, which is the convention. The origin field renders as "
     "'Your location'; Max confirmed it as Fort Lupton on INJ-07-2026-W1 and dropped the unnamed-origin flag, so "
     "it is not raised again here. [log:google_maps_options, certify_components]",
     "CO to Basco Routing Map.png"),
    ("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", FL,
     "The value is right and the label is wrong. Mass of load in Certify is 3,246 kg, which is exactly the Ops "
     "Notes Total Mass Transported of 3246.0 kg — the gross basis including tote tare, not Total Oil Produced "
     "(3073.2) and not Total Oil in Batch (3068.0). But the datapoint carrying it is titled 'QOWV (Aqueous Oil) - "
     "Mass (Net) (CO to KS)' on a WODO removal whose destination is Louisiana. Three things are wrong in one "
     "title: the oil type is the aqueous product rather than WODO, the basis is described as Net when the figure "
     "is gross, and the destination is Kansas when the route is Colorado to Louisiana. Flag rather than Fail "
     "because the quantity feeding the calculation is correct and the emission reproduces exactly. Worth noting "
     "that this mislabel is what makes the tote-fraction question at 3.1 harder to see, since the transport "
     "datapoint already says aqueous. The sibling Week 1 batch carries the same family of defect. "
     "[log:certify_components, certify_attachment_map, ops_notes_totals]",
     "Certify cmp_1KYWWAQ3J1S0S54V"),
    ("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", P,
     "The mass of load datapoint shows 2 sources. Expanding it returns 'INJ-07-2026-W2 Ops Notes.xlsx' alongside "
     "'Charm Inv Bulk Upload March.csv'. The batch Ops Notes is attached and linked to this specific datapoint "
     "rather than only at removal level. [log:certify_attachment_map]",
     "Certify Sources tab"),
    ("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS: mass of load 3,246 kg plus or minus 3.40194 kg, matching the Ops "
     "Notes uncertainty exactly. It is also identical to the mass-of-product uncertainty on the sequestration "
     "component, which is correct — the same three totes, weighed once each. "
     "[log:certify_components, _derived_values.uncertainty_expected_kg]",
     "Certify cmp_1KYWWAQ3J1S0S54V INPUTS"),

    ("SECTION 6 — CERTIFY: TRANSPORT EMBODIED EMISSIONS",),
    ("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", P,
     "The component modal shows 0.19279 kgCO2e per mile. The 2026 tab row 11, 'Vehicle Embodied Emissions "
     "--Non-Tanker Truck', gives 0.0001927908256 MT CO2e per mile from GLEC V3.2 2025, marked Updated. Same value "
     "in native units, and it is the non-tanker row rather than the tanker row, which is correct here. The "
     "datapoint title also reads Non-Tanker Truck, so label and source row agree — the mismatch flagged on the "
     "aqueous sibling this period is not present on this removal. The factor is per-mile and is applied per-mile, "
     "with no mass term, which matches the embodied convention. [log:standard_efs_2026, certify_components]",
     "Standard EFs 2026 tab row 11"),
    ("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", P,
     "Certify aggregate distance is 1,201 mi. The allocation tab's batch mileage allocation at C17 resolves to "
     "1201.0 mi, and the same figure carries through to the Ops Notes summary tab as the WODO row's Colorado to "
     "Louisiana embodied distance. Exact match. The allocated figure equals the full one-way distance in this "
     "case because the batch took the entire truck, 3 of 3 totes — the allocation is genuinely computed rather "
     "than the full distance being substituted for it, since the share cell is a live formula returning 1.0. "
     "[log:_derived_values.batch_mileage_allocation_mi, shipment_tracker_cells_are_formulas, "
     "summary_tab_wodo_row, certify_components]",
     "Certify cmp_1KYWWAQ3J1S0CT0G INPUTS"),
    ("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", P,
     "Cleared on the live entry. Re-read at 23:18Z on 2026-08-06: the aggregate distance datapoint now carries two "
     "sources, 'CO to Basco Routing Map.png' and 'INJ-07-2026-W2 Ops Notes.xlsx', the second confirmed by expanding "
     "the source list rather than inferred. That puts both applicable evidence types on the datapoint — the route "
     "map, and the Ops Notes whose 'WODO Shipments & EE Allocation' tab derives the 1,201 mi through live formulas "
     "(batch share =D12/C12 returning 1.0, allocated miles =E12*F12, batch allocation =G13). The third type, a "
     "Charm Contents sheet, does not exist for this batch under the weekly schema and its absence is accepted on "
     "the INJ-06-2026-W1 and INJ-07-2026-W1 precedent. The stale inventory file that previously stood in this slot "
     "and carried no distance, route or allocation of any kind has been detached. A verifier can now reconstruct "
     "the mileage from the attached documents. [log:certify_attachment_map, charm_contents, "
     "inventory_bulk_upload, shipment_tracker_cells_are_formulas]",
     "Certify Sources tab / VR Appendix 1"),

    ("SECTION 7 — CERTIFY: PRODUCTION EMISSIONS",),
    ("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", P,
     "The batch draws on two production periods, March 2026 for tote 301041 and April 2026 for totes 301089 and "
     "301128. Both are captured. Certify carries a single aggregated component, 'Pyrolysis - Charm WODO PP "
     "Emissions' at 2.417 tCO2e, holding a production-mass-weighted blended intensity of 0.786584 that reconciles "
     "exactly to the per-period sum: 1034.40 x 0.7901 = 817.27944, plus 1020.40 x 0.7848 = 800.80992, plus "
     "1018.40 x 0.7848 = 799.24032, totalling 2417.32968 kgCO2e against Certify's 2.417 t. No period is omitted. "
     "Aggregating periods into one weighted component is not a finding — no primary source requires per-period "
     "component granularity. [log:production_periods, _derived_values.production_emissions_recomputed_kg, "
     "_derived_values.pe_tote_301041_kg, _derived_values.pe_tote_301089_kg, "
     "_derived_values.pe_tote_301128_kg, certify_components]",
     "Certify Components tab"),
    ("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", P,
     "Certify carries 0.786584 tCO2e per tonne. The Ops Notes weighted average at H26 is 0.7865839125, computed "
     "as =I26/D26, that is total production emissions over total net oil produced. Recomputed from the per-tote "
     "rows: 2417.32968 / 3073.2 = 0.7865839125. Match to the displayed precision. Each period's intensity is "
     "applied to the right totes and both trace to their period summaries — the March 2026 summary gives WODO "
     "0.7901 kg emissions per kg material against 16,307 kg of WODO output, and the April 2026 summary gives "
     "0.7848 against 17,580 kg. Neither is a cross-wired aqueous figure; the April summary's aqueous intensity is "
     "0.1314 and appears nowhere in this batch. [log:_derived_values.weighted_ci_recomputed, pp_summaries, "
     "certify_components, ops_notes_totals]",
     "Ops Notes WODO H26 / PP summaries"),
    ("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", P,
     "The carbon intensity datapoint shows 1 source and it is 'INJ-07-2026-W2 Ops Notes.xlsx', linked to the "
     "datapoint rather than sitting at removal level only. That is the required evidence standard for a Charm "
     "production intensity — the Ops Notes weighted average across the totes used in the injection. A standalone "
     "production period summary is not required here, so its non-attachment is not a finding. "
     "[log:certify_attachment_map]",
     "Certify Sources tab"),
    ("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", P,
     "Certify mass is 3,073.2 kg. The Ops Notes sum of net oil produced across the three totes is 3073.2 kg "
     "(1034.40 + 1020.40 + 1018.40), a delta of 0.0 kg. The component correctly uses net-in-tote, the produced "
     "mass, rather than net-in-injection-batch (3068.0) — production emissions attach to what was produced, not "
     "to what survived the transfer. [log:_derived_values.sum_net_produced_kg, "
     "_derived_values.delta_net_produced_kg, certify_components]",
     "Certify cmp_1KYWWAQ3J1S0VDF4 INPUTS"),
    ("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", P,
     "Read from the component modal INPUTS: mass 3,073.2 kg plus or minus 3.40194 kg. That matches the Ops Notes "
     "uncertainty and the expected 1.13398 kg per tote across 3 totes. The uncertainty is present, which is the "
     "point that mattered here — this is the dominant input on the removal at 85.41 % of activities, so it does "
     "not qualify for any omission carve-out. Both June batches shipped without it; this one has it. "
     "[log:certify_components, _derived_values.uncertainty_expected_kg]",
     "v1.2 6.5.1"),
    ("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", P,
     "No Charm Contents sheet exists for this batch. That was established by three independent routes and the "
     "search is recorded: a walk of the batch Drive folder, a Drive-wide title search that returned only legacy "
     "per-batch 3-XX and 5-XX sheets with the newest modified 2026-05-12, and a full enumeration of all 7 Certify "
     "sources. Under the weekly time-block schema the per-period mass breakdown it used to carry now lives in the "
     "Ops Notes WODO tab, column G production period against column D net oil produced, and the Ops Notes is "
     "attached to this mass datapoint. Same basis accepted on INJ-06-2026-W1 and INJ-07-2026-W1, so this passes "
     "on the successor document. [log:charm_contents, certify_attachment_map]",
     "VR Appendix 1"),

    ("SECTION 8 — OTHER",),
    ("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total meet or exceed the transport-process sum?", P,
     "There is one diesel transport-process emission on this removal, the flatbed leg at 0.540 tCO2e, and it is "
     "offset. Reductions carries a Constant CO2 reduction of 540 kgCO2e under bio-oil transport, evidenced by "
     "'Charm-RetirementCertificate-RD-EACs-20251218.pdf'. Recomputing the process emission from primary sources "
     "gives 3.246 t x 1201 mi x 0.0001384 MT per tonne-mile = 539.545 kgCO2e, so the 540 kgCO2e offset meets and "
     "slightly exceeds it. Embodied emissions are correctly not offset. "
     "[log:_derived_values.bcu_kg, _derived_values.process_recomputed_t, _derived_values.process_recomputed_kg, certify_components]",
     "Certify cmp_1KYX8TD3K1S00F1C"),

    ("SECTION 9 — AQUEOUS BUFFERING (LCS)",),
    ("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist?", NA,
     "Not applicable to a WODO batch — LCS is an aqueous pre-treatment. Confirmed rather than assumed: the Ops "
     "Notes WODO tab was dumped cell by cell and scanned case-insensitively along with the allocation tab for "
     "'lcs', 'calcium' and 'buffer', returning no hits, and all 5 Certify components were enumerated with no LCS "
     "component among them. [log:lcs_use_kg_detail, certify_components]",
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
    ws.title = "WODO QA INJ-07-2026-W2"

    ws.cell(row=1, column=1, value="Charm WODO Injection Batch QA Checklist").font = TITLE
    meta = [
        ("Batch ID", "INJ-07-2026-W2 (WODO)"),
        ("Reporting Period", "July 1 - July 31 2026; injection week 2026-07-04 to 2026-07-11 (Certify window 05-11 Jul 2026)"),
        ("Reviewer", "Claude (MRV QA agent)"),
        ("Date", "2026-08-06"),
        ("Injection Site", "Basco 6, Louisiana (Class V UIC)"),
        ("Oil Type", "WODO (Charm-produced, Fort Lupton CO), 3 IBC totes"),
        ("Production Periods", "March 2026 (1 tote, CI 0.7901); April 2026 (2 totes, CI 0.7848)"),
        ("Certify Removal ID", "rmv_1KYWWAQ3J1S09AWW  (GHG statement ggs_1KZBX6AX41S029JS)"),
        ("Certify Net", "2.830 tCO2e = Sequestrations 5.501 + BCU 0.540 - Activities 3.188 - Uncertainty 0.023"),
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
        "The tote-fraction question is closed on this removal but the production record still carries it. "
        "'Charm Inv Bulk Upload March.csv' has been detached, so nothing a verifier opens on this entry now "
        "classifies tote 301128 as aqueous. The row inside that file still reads QOWV against 1,138 kg gross, "
        "and April 2026 tote tags interleave across both fractions there — 34 aqueous rows against 13 WODO — so "
        "the tag number gives no warning either way. The lab result says the material was WODO, so the removal is "
        "right; worth correcting the inventory row so Charm's own production books agree with what was injected.",

        "That file had also been standing as the evidence for a mileage figure. Before it was detached it sat on "
        "the aggregate distance datapoint, and it is a tote-weight ledger with no distance, route or shipping-order "
        "column in any of its 224 rows. The batch Ops Notes has now taken that slot, which is the document that "
        "actually derives the 1,201 mi.",

        "Collection method flipped on the aggregate distance datapoint. It now reads REPORTED where it previously "
        "read DERIVED. No value changed and the 1,201 mi still ties to the allocation tab. The same flip appeared "
        "on four datapoints of the aqueous sibling this reporting period when they were re-entered, so it looks "
        "like a side effect of re-attaching rather than a deliberate reclassification. Worth a glance.",

        "Tote 301128 retained more oil than its two siblings. Its post-unload container weight is 62.00 kg "
        "against 58.00 kg for the other two, so 4.40 kg stayed behind where they each left 0.40 kg. That is 85 % "
        "of the batch's entire 5.20 kg transfer loss in one tote. The direction is conservative because the "
        "residual is deducted from the injected mass and the weights are measured rather than assumed, so nothing "
        "is held against the batch. Worth an operational look given the same tote is the one the inventory file "
        "classifies as aqueous - a heavier residual would be consistent with a different product, though it is "
        "equally consistent with an ordinary drain problem on one unit.",

        "The Scale Tickets subfolder holds no WODO records. It contains only the two AECN railcar folders for "
        "this week, TIMX201060 and SHPX215079. This is not held against the batch: the Ops Notes ledger header "
        "states that tote tag mass is authoritative for IBC deliveries, and that is the accepted weighing record. "
        "It does mean the three gross weights and three measured empty weights rest on that ledger alone.",

        "Two production periods, two documentation states, both fine. The July reporting-period VVB guidance "
        "names January, March and April 2026 as new this period with a full documentation package each, which "
        "covers both periods feeding this batch. No gap of the kind found on the aqueous sibling, where October "
        "2025 supplied 19 totes and was absent from the guidance list.",

        "The removal is small and the emission profile is dominated by production. Pyrolysis is 85.41 % of "
        "activities at 2.417 tCO2e against a 5.501 tCO2e sequestration, so net removal is 2.830 tCO2e from "
        "3,068 kg of injected oil. Nothing wrong with that - it is what a 3-tote batch of high-intensity March "
        "and April oil looks like - but it means any error in the tote-fraction question at 3.1 moves the net a "
        "long way in percentage terms.",
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
        "POST-FIX STATE, re-read live against Certify on 2026-08-06 at 23:17-23:18Z. Net is unchanged at 2.830 "
        "tCO2e = Sequestrations 5.501 + BCU 0.540 - Activities 3.188 - Uncertainty 0.023, and the source count is "
        "still 7. "
        "BOTH FAILS ARE CLOSED, each re-verified against the live entry rather than taken on report. Item 3.1: "
        "'Charm Inv Bulk Upload March.csv' was detached from all three datapoints it sat on, so nothing attached "
        "to this removal now classifies tote 301128 as the aqueous product; the two mass datapoints carry the "
        "batch Ops Notes alone and their values are untouched at 3.246 t and 3.073 t. Item 6.3: the batch Ops "
        "Notes was attached to the aggregate distance datapoint in the same pass, confirmed by expanding the "
        "source list, so that datapoint now carries the route map and the document whose allocation tab derives "
        "the 1,201 mi through live formulas. "
        "THE ARITHMETIC WAS CLEAN AT FIRST DELIVERY AND IS UNCHANGED. All four Ops Notes totals reconcile to a "
        "zero delta across the three-tote ledger: transported 3246.0 kg, produced 3073.2 kg, injected 3068.0 kg, "
        "uncertainty 3.40194 kg. Each of the five components reproduces from primary sources - sequestration 3068 "
        "kg x 48.9 % x 3.667 = 5.501 t; transport process 3.246 t x 1201 mi x 0.0001384 = 0.540 t; transport "
        "embodied 1201 mi x 0.0001927908256 = 0.232 t; pyrolysis 3.0732 t x 0.786584 = 2.417 t; and the net closes "
        "at 2.829 against Certify's 2.830. Both emission factors match the live 2026 tab in native units. "
        "Uncertainty is present and correct on all three components that need it, including the pyrolysis mass "
        "that both June batches shipped without. The BCU offsets the flatbed process emission exactly. Distance is "
        "the longest of the three routes read from the map pixels. All nine allocation cells are live formulas. "
        "ONE FLAG REMAINS. Item 5.3: the transport mass datapoint is still titled 'QOWV (Aqueous Oil) - Mass (Net) "
        "(CO to KS)' on a WODO removal shipping to Louisiana - wrong oil type, wrong basis word, wrong state. The "
        "value 3,246 kg is correct and the emission reproduces exactly, so it does not block verification, but it "
        "is the one label on this entry that still says aqueous."
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
