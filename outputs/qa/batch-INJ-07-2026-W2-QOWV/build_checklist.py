#!/usr/bin/env python3
"""Build the Charm Aqueous (QOWV) QA checklist for batch INJ-07-2026-W2."""
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = Path(__file__).parent
LOG = HERE / "batch_INJ-07-2026-W2-QOWV_source_reads.json"

# ---------------------------------------------------------------- DERIVED
DERIVED = {
    # Ops Notes independent recomputation (36-tote ledger)
    "sum_gross_kg": 31529.00,
    "sum_tote_mass_kg": 2073.60,
    "sum_net_produced_kg": 29455.40,
    "sum_empty_tote_weight_kg": 6008.00,
    "sum_net_injected_kg": 25521.00,
    "delta_gross_kg": 0.00,
    "delta_net_produced_kg": 0.00,
    "delta_net_injected_kg": 0.00,
    "measured_tote_loss_kg": 3934.40,
    "measured_tote_loss_pct_of_net_produced": 13.3571,
    "mean_tote_residual_kg": 109.29,
    "min_tote_residual_kg": 29.90,
    "max_tote_residual_kg": 322.40,
    "uncertainty_expected_kg": 40.82328,
    "uncertainty_delta_kg": 0.00000,
    "c_uncertainty_expected_pct": 0.0336,
    "weighted_ci_recomputed": 0.121048588035,
    "production_emissions_recomputed_kg": 3565.53458,
    # allocation recomputation
    "share_cola_8": 0.888889,
    "share_co_aqueous_12_3": 0.058824,
    "share_co_aqueous_12_3_02": 1.000000,
    "share_co_aqueous_12_01_25": 0.050000,
    "share_co_aqueous_12_1_25_t2": 0.050000,
    "share_cola20": 0.473684,
    "share_cola_8_pct": 88.8889,
    "share_co_aqueous_12_3_pct": 5.8824,
    "share_co_aqueous_12_3_02_pct": 100.0000,
    "share_co_aqueous_12_01_25_pct": 5.0000,
    "share_co_aqueous_12_1_25_t2_pct": 5.0000,
    "share_cola20_pct": 47.3684,
    "lb_per_weighing_event": 2.5,
    "alloc_cola_8_mi": 1067.555556,
    "alloc_co_aqueous_12_3_mi": 70.647059,
    "alloc_co_aqueous_12_3_02_mi": 1201.000000,
    "alloc_co_aqueous_12_01_25_mi": 60.050000,
    "alloc_co_aqueous_12_1_25_t2_mi": 60.050000,
    "alloc_cola20_mi": 568.894737,
    "alloc_total_mi": 3028.197351,
    "ton_miles": 37866.329,
    # emission-factor effects
    "process_at_tanker_t": 4.328121,
    "process_at_flatbed_t": 5.240700,
    "process_understatement_t": 0.912579,
    "embodied_at_tanker_t": 0.719380,
    "embodied_at_nontanker_t": 0.583809,
    "embodied_overstatement_t": 0.135572,
    # sequestration + pyrolysis recomputation
    "gross_sequestration_t": 7.861183,
    "pyrolysis_recomputed_t": 3.565535,
    "net_recomputed_t": 3.541,
    "activities_sum_t": 8.613,
    # July-2025 period intensity effect
    "july_pe_at_applied_ci_kg": 181.75,
    "july_pe_at_july_2025_ci_kg": 208.41,
    "july_pe_delta_kg": 26.66,
    "blended_ci_if_july_corrected": 0.121953736,
    "pyrolysis_if_july_corrected_t": 3.592196,
    "net_if_july_corrected_t": 3.5143,
    # BCU
    "net_removal_overstatement_from_july_ci_t": 0.026661,
    "bcu_as_filed_kg": 4328.000,
    "bcu_shortfall_as_filed_kg": 0.121,
    "bcu_required_after_flatbed_kg": 5240.700,
    "bcu_shortfall_after_flatbed_kg": 912.700,
    # post-correction state, re-read live 2026-08-06 21:16Z
    "filed_process_t_after_fix": 5.241,
    "filed_embodied_t_after_fix": 0.584,
    "filed_bcu_t_after_fix": 5.241,
    "filed_activities_t_after_fix": 9.390,
    "filed_net_t_after_fix": 3.677,
    "uncertainty_discount_kg": 35,
    "sources_before_fix": 38,
    "sources_after_fix": 41,
    "process_ef_displayed_kg_per_km_t": 0.09,
    "embodied_ef_displayed_kg_per_km": 0.1198,
    "km_per_mi": 1.609344,
    "net_improvement_from_fixes_t": 0.136,
}

log = json.loads(LOG.read_text())
log["_derived_values"] = DERIVED
LOG.write_text(json.dumps(log, indent=2))

# ---------------------------------------------------------------- STYLES
HDR = PatternFill("solid", fgColor="D6E4F0")
FAIL = PatternFill("solid", fgColor="FFC7CE")
FLAG = PatternFill("solid", fgColor="FFF2CC")
FLAGF = Font(color="996600", size=10)
NAF = Font(color="808080", italic=True, size=10)
BODY = Font(size=10)
BOLD = Font(bold=True, size=10)
TITLE = Font(bold=True, size=13)
thin = Side(style="thin", color="BFBFBF")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "QA Checklist"

meta = [
    ("Charm Aqueous (QOWV) Injection Batch QA Checklist", None),
    ("Batch ID", "INJ-07-2026-W2  (QOWV / Aqueous portion)"),
    ("Reporting Period", "July 1 - July 31 2026 RP; injection week per Ops Notes 2026-07-04 to 2026-07-11; Certify removal window 05 Jul 2026 to 11 Jul 2026"),
    ("Reviewer", "Claude (QA agent) - for Max Lavine review"),
    ("Date", "2026-08-06  (first delivery 20:45Z; re-reviewed against live Certify 21:16-21:18Z after corrections)"),
    ("Injection Site", "Basco 6 (Louisiana)"),
    ("Oil Type", "Aqueous / QOWV (Charm-produced, Fort Lupton CO) - 36 IBC totes across 6 shipping orders"),
    ("Production Periods", "July 2025 (2 totes, CI 0.1374), August 2025 (23 totes, CI 0.1106), September 2025 (2 totes, CI 0.1287), November 2025 (8 totes, CI 0.1392), December 2025 (1 tote, CI 0.1631)"),
    ("Certify Removal ID", "rmv_1KYWCXFBK1S0Y3NV  |  Net 3.677 tCO2e after corrections (was 3.541 at first delivery)  |  GHG statement ggs_1KZBX6AX41S029JS"),
]
ws.cell(row=1, column=1, value=meta[0][0]).font = TITLE
r = 2
for k, v in meta[1:]:
    ws.cell(row=r, column=1, value=k).font = BOLD
    c = ws.cell(row=r, column=2, value=v)
    c.font = BODY
    c.alignment = Alignment(vertical="top", wrap_text=True)
    r += 1

r += 1
for i, h in enumerate(["#", "Question", "Status", "Evidence / Finding", "Reference"], start=1):
    c = ws.cell(row=r, column=i, value=h)
    c.font = BOLD
    c.fill = HDR
    c.border = BORD
HEADER_ROW = r
r += 1


def section(title):
    global r
    for col in range(1, 6):
        c = ws.cell(row=r, column=col, value=title if col == 1 else None)
        c.fill = HDR
        c.font = BOLD
        c.border = BORD
    r += 1


def item(num, q, status, ev, ref):
    global r
    for col, v in enumerate([num, q, status, ev, ref], start=1):
        c = ws.cell(row=r, column=col, value=v)
        c.border = BORD
        c.alignment = Alignment(vertical="top", wrap_text=(col in (2, 4)))
        c.font = BODY
        if status == "Fail":
            c.fill = FAIL
        elif status == "Flag":
            c.fill = FLAG
            c.font = FLAGF
        elif status == "N/A":
            c.font = NAF
    r += 1


# ---------------------------------------------------------------- SECTION 1
section("Section 1 - Batch Folder")
item("1.1", "Is there testing in the testing folder for the batch?", "Pass",
     "The Testing subfolder holds three SGS certificates, one per oil type in the week, and the QOWV one carries this batch's own composite sample id. 'CHARM INDUSTRIAL - QOWV 7-2026-W2 (SR26-04220.002).pdf' is certificate SR26-04220.002, client id 'QOWV 7-2026-W2', location BOSCO LA, sampled 08-Jul-2026 14:00, analysed and completed 13-Jul-2026 15:01, signed by Jaszmine Eugene. It reports Carbon 8.4 % (m/m) by ASTM D5291 Method C, Hydrogen 8.8 %, Nitrogen <0.75 %, kinematic viscosity at 40 C of 1.026 cSt, acid number 34 mg KOH/g and density at 15 C of 1.050 g/cm3. "
     "That 8.4 % is exactly the carbon content this batch reports, so the certificate supports the claim rather than merely accompanying it. The other two files cover the same week's other oil types and are not used here: AECN 7-2026-W2 (SR26-04370.001) at 41.6 % and 7-2026-W2 WODO (SR26-04432.001) at 48.9 %. Density 1.050 g/cm3 exceeds the 1.01 g/cm3 formation-fluid density required for injection. [log:lab_results] [log:lab_results._primary_source_opened] [log:batch_folder_inventory]",
     "VR Appendix 1; SGS CoA SR26-04220.002"),
item("1.2", "Are Ops Notes in the folder and fully completed?", "Pass",
     "'INJ-07-2026-W2 Ops Notes' is in the batch folder with eight tabs, and the QOWV tab is complete. All 36 tote rows carry tag, gross mass, nominal tote mass, net oil produced, measured empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty, with no blanks and no formula errors, and every totals cell on row 53 is a live SUM or SUMPRODUCT formula rather than a typed number. "
     "The Summary tab's QOWV row is internally consistent with the detail tab and with the lab file: transport mass B20 = 31529 pulls '=QOWV!B53', pyrolysis mass D20 = 29455.4 pulls '=QOWV!D53', sequestration mass E20 = 25521 pulls '=QOWV!F53', composite sample id F20 reads 'QOWV 7-2026-W2', C % G20 = 0.084 matches the certificate's 8.4 %, the Lab COA Link cell is a live hyperlink to the same certificate file it names ('COA SR26-04220.002'), and the carbon-content uncertainty I20 = 0.000336 is the formula '=G20*J20' on a testing uncertainty of 0.004. The workbook carries no cell notes anywhere, checked by loading it without data_only so annotations would be visible. [log:ops_notes_qowv] [log:ops_notes_qowv._primary_source_opened] [log:ops_notes_summary_tab_qowv_row]",
     "VR Appendix 1; Ops Notes QOWV + Summary tabs"),
item("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Pass",
     "The tracker is in the batch folder and carries everything the allocation needs. Under the 2026 weekly schema it lives as the 'QOWV Shipments & EE Allocation' tab inside the batch Ops Notes rather than as its own file. Present and populated: the batch summary row (36 totes, injection week 2026-07-04 to 2026-07-11, six named shipping orders with their tote counts), the one-way distance input B8 = 1201, the six-row allocation table, the batch mileage allocation block at C22 = 3028.197351, and the full 36-tote roster broken out per shipping order. "
     "The Ship Date column (B12 through B17) carries no dates. Nothing in the emissions calculation reads it - the allocation is built from tote counts and the single distance input - so no reported figure depends on it, and Max reviewed the point and ruled it immaterial on 2026-08-06. Recorded here for the audit trail, not as a finding. [log:shipment_tracker] [log:shipment_tracker._primary_source_opened] [log:batch_folder_inventory]",
     "VR Appendix 1; Ops Notes 'QOWV Shipments & EE Allocation' tab")
# ---------------------------------------------------------------- SECTION 2
section("Section 2 - Ops Notes")
item("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", "Pass",
     "Reported 31,529.00 kg at QOWV!B53, which is the live formula '=SUM(B11:B46)' over the 36 tote rows and not a typed constant. Summing the 36 per-tote gross masses independently gives 31,529.00 kg, so the delta is 0.00 kg. The formula's range covers every populated ledger row - rows 11 to 46 inclusive, 36 rows for 36 totes - so no tote is left out of the bottom of the range. [log:ops_notes_qowv.totals_row_53] [log:_derived_values]",
     "Ops Notes QOWV!B53"),
item("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", "Pass",
     "Reported 29,455.40 kg at QOWV!D53 = '=SUM(D11:D46)'. Each per-tote cell in column D is the formula '=B-C', gross mass less the tote's own mass, and none is hard-coded. Independent recomputation of gross minus tote mass across all 36 rows gives 29,455.40 kg, a delta of 0.00 kg. The arithmetic also closes against the tare column: 31,529.00 kg gross less 2,073.60 kg of tote mass (36 totes at the 57.60 kg tote-tag mass) equals 29,455.40 kg exactly. [log:ops_notes_qowv.totals_row_53] [log:ops_notes_qowv.per_tote_formulas] [log:_derived_values]",
     "Ops Notes QOWV!D53"),
item("2.3", "Is the 'Total Oil in Batch' value correctly computed (Aqueous: measured pre-unload minus measured post-unload per tote, no Standard Loss)?", "Pass",
     "Reported 25,521.00 kg at QOWV!F53 = '=SUM(F11:F46)', and the Aqueous method is correctly applied. Each per-tote cell in column F is the formula '=IF(E=\"\",\"\",B-E)', gross mass less the directly measured empty tote weight recorded after unloading - a measured pre/post pair, not an allowance. Independent summation across the 36 rows gives 25,521.00 kg, delta 0.00 kg. "
     "No Standard Loss deduction appears anywhere: a programmatic check of all 36 net-in-batch formulas found no Standard Loss term, and the measured empty weights vary genuinely from 87.50 kg to 380.00 kg against the 57.60 kg nominal, which is measurement rather than a fixed per-tote figure. The loss closes both ways: 6,008.00 kg of measured empty weight less 2,073.60 kg of nominal tote mass = 3,934.40 kg, which equals net oil produced 29,455.40 kg less net oil injected 25,521.00 kg exactly. [log:ops_notes_qowv.totals_row_53] [log:ops_notes_qowv.per_tote_formulas] [log:_derived_values]",
     "Ops Notes QOWV!F53; FC-C1 (Aqueous branch)"),
item("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
     "Reported 40.82328 kg at QOWV!J53 = '=SUM(J11:J46)'. Every per-tote cell is the formula '=2.5*$L$4' against the sheet's own kg-per-lb constant L4 = 0.453592, giving 1.13398 kg per tote - one weighing event per tote. For 36 totes the expected total is 1.13398 x 36 = 40.82328 kg, matching the reported figure to a delta of 0.00000 kg. This is the Charm per-tote precision, not the AECN per-truck figure. [log:ops_notes_qowv.totals_row_53] [log:ops_notes_qowv.per_tote_uncertainty_kg] [log:ops_notes_qowv.constants] [log:_derived_values]",
     "Isometric Standard S3.7.3 Option B; FC-C8"),

# ---------------------------------------------------------------- SECTION 3
section("Section 3 - Bio-Oil Shipment Tracker"),
item("3.1", "Are totes for the RP correctly identified?", "Pass",
     "36 totes are listed for the batch across six shipping orders - COLA_8 (16), CO_AQUEOUS_12.3 (1), CO_AQUEOUS_12.3_02 (8), CO_AQUEOUS_12.01.25 (1), CO_AQUEOUS_12.1.25_T2 (1) and COLA20 (9) - and the per-order counts sum to 36, matching both the batch summary row's tote count and the 36 rows of the Ops Notes IBC ledger. Every roster row carries fraction QOWV and batch INJ-07-2026-W2. The comparison was run programmatically over the full tag sets rather than sampled: no tote appears in one tab and is absent from the other, and there are no duplicate tags in either. [log:shipment_tracker] [log:roster_reconciliation] [log:roster_reconciliation._primary_source_opened]",
     "Ops Notes 'QOWV Shipments & EE Allocation' tab"),
item("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Pass",
     "All 36 tags match between the two tabs with no orphans in either direction, and every roster row's fraction (QOWV) and batch (INJ-07-2026-W2) agrees with the ledger. The production-period month and year agree for all 36 totes as well: the roster's Production Period date and the ledger's period label resolve to the same month and year in every case, with zero mismatches. [log:roster_reconciliation] [log:shipment_tracker]",
     "Ops Notes ledger vs roster; FC-C5"),
item("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
     "Every computed cell read from the workbook is a live formula and not one is a typed constant. Batch Share of Truck: E12 = '=D12/C12' through E17 = '=D17/C17', all six rows. Mileage one-way: F12 through F17 all read '=$B$8', pointing at the single distance input. Allocated Miles: G12 = '=E12*F12' through G17 = '=E17*F17'. Totals: C18 = '=SUM(C12:C17)', D18 = '=SUM(D12:D17)', G18 = '=SUM(G12:G17)'. Batch Mileage Allocation: C22 = '=G18' with tote count D22 = '=D18'. A verifier can rebuild the entire allocation from six tote-count pairs and one mileage input. [log:shipment_tracker_cells_are_formulas] [log:shipment_tracker._primary_source_opened]",
     "Auditability; FC-C3"),
item("3.4", "Are computed outputs computed correctly per the allocation formulas?", "Pass",
     "All three reproduce the specification independently, per truck. COLA_8: 16 batch totes of 18 on the truck = 88.8889 %, times 1,201 mi = 1,067.555556 mi. CO_AQUEOUS_12.3: 1 of 17 = 5.8824 %, = 70.647059 mi. CO_AQUEOUS_12.3_02: 8 of 8 = 100.0000 %, = 1,201.000000 mi. CO_AQUEOUS_12.01.25: 1 of 20 = 5.0000 %, = 60.050000 mi. CO_AQUEOUS_12.1.25_T2: 1 of 20 = 5.0000 %, = 60.050000 mi. COLA20: 9 of 19 = 47.3684 %, = 568.894737 mi. "
     "The six allocated figures sum to 3,028.197351 mi, matching G18 and the Batch Mileage Allocation at C22 exactly. The mileage input is labelled 'Charm CO -> Basco LA distance (one-way mi)' and is applied one-way with no round-trip doubling, which is correct for this batch. The allocated total legitimately exceeds the 1,201 mi one-way distance because six separate truck movements each contribute a share. [log:shipment_tracker.allocation_table] [log:shipment_tracker.totals] [log:_derived_values]",
     "RP Share x one-way mileage; process vs embodied distance convention"),
item("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", "Pass",
     "Three of the four attributes are cross-checkable and all three match for every tote: tags 36 of 36 with no orphans and no duplicates, fraction QOWV on every roster row, and production-period month and year agreeing on all 36. "
     "Gross mass cannot be compared between the two tabs because the roster carries no mass column - its fields are Metal Tag, Fraction, Production Period, Shipping Order and Batch. That is the schema, not an omission: gross mass has a single source in this design, the IBC ledger, whose own section header states 'one row per IBC tote; tote tag mass is authoritative'. The ledger's gross column was verified against its own totals under item 2.1. [log:roster_reconciliation] [log:shipment_tracker.roster_columns] [log:ops_notes_qowv.section1_header]",
     "Ops Notes ledger vs roster; FC-C5"),

# ---------------------------------------------------------------- SECTION 4
section("Section 4 - Certify: Injection Sequestration")
item("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
     "Read from the component modal INPUTS: carbon content of product = 'Carbon Content of Bio-oil Injected (per injection)' at 8.4 %. The certificate carrying this batch's own composite sample id, SR26-04220.002 client id 'QOWV 7-2026-W2', reports Carbon 8.4 % (m/m) by ASTM D5291 Method C. The Ops Notes Summary QOWV row states the same value at G20 = 0.084. Three sources, one number, zero difference. "
     "The gross sequestration reproduces from these inputs: 25,521 kg of injectant at 8.4 % carbon gives 2,143.764 kg of carbon, and applying the CO2-to-carbon mass ratio gives 7.861183 tCO2e against the 7.861 tCO2e Certify displays. [log:certify.components] [log:lab_results] [log:ops_notes_summary_tab_qowv_row] [log:_derived_values]",
     "Certify Injection sequestration cmp_1KYWCXFBK1S0T925"),
item("4.2", "Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?", "Pass",
     "Both required evidence types are attached and both are linked to the carbon-content datapoint itself, not merely to the removal. The modal shows '2 sources' against carbon content of product, and the Sources tab resolves them as 'CHARM INDUSTRIAL - AECN 7-2026-W1, QOWV 7-2026-W2.pdf' - the SR26-04220 certificate, whose .002 section is this batch's QOWV sample - and 'INJ-07-2026-W2 Ops Notes.xlsx'. "
     "The Certify copy of the certificate is named for both batches it covers because SGS issued one report with two sections (.001 AECN Week 1, .002 QOWV Week 2); the Drive Testing-folder copy of the same certificate is filed under the QOWV-specific name. The naming is traceable in both directions, so this is not a filename concern. [log:certify.attachment_map] [log:certify.certify_sources_enumeration] [log:lab_results]",
     "Certify Sources tab"),
item("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
     "Read from the modal INPUTS: mass of product = 25,521 kg with uncertainty +/-40.82328000000002 kg. The Ops Notes uncertainty total at QOWV!J53 is 40.82328 kg. The values agree to the full precision Certify carries, and both reconstruct as 1.13398 kg per tote across 36 totes. The uncertainty is entered as an absolute mass, not as a percentage. [log:certify.components] [log:ops_notes_qowv.totals_row_53] [log:_derived_values]",
     "Isometric Standard S3.7.3; MRV Uncertainty Cheat Sheet"),
item("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty?", "Pass",
     "Read from the modal INPUTS: carbon content 8.4 % with uncertainty +/-0.0336 %. The expected value is 0.004 times the reported carbon content, 0.004 x 8.4 = 0.0336, so the reported figure matches exactly. It is correctly entered as an absolute percentage-point value rather than as the literal 0.4. The Ops Notes derives the same figure independently at Summary!I20 = '=G20*J20' = 0.000336 in decimal form on a testing uncertainty of 0.004. [log:certify.components] [log:ops_notes_summary_tab_qowv_row] [log:_derived_values]",
     "0.4% relative uncertainty on carbon content"),

# ---------------------------------------------------------------- SECTION 5
section("Section 5 - Certify: Transport Process Emissions")
item("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
     "CORRECTED AND RE-VERIFIED LIVE 2026-08-06 21:16Z. The component now reads 'CO to LA Flatbed Truck Transport Process Emissions - QOWV' and its emission factor datapoint reads 'Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Flatbed Truck', displayed as 0.09 kgCO2e/(km.t). That display value is the live 2026 tab's Flatbed Truck row (row 6, final quantity 0.0001384 MT CO2e/t-mi, cited GLEC V3.2 2025, marked Updated) expressed per km: 0.0001384 divided by 1.609344 gives 0.0000860 MT/(km.t), which Certify shows rounded to 0.09. "
     "The component output confirms the full-precision factor is in use, not the rounded display value: 31.529 t x 1,201 mi = 37,866.329 t-mi at 0.0001384 MT/(t-mi) = 5.240700 tCO2e, and Certify reports 5.241 tCO2e. The tanker factor of 0.0001143 that was previously applied would give 4.328121 tCO2e. The 0.912579 tCO2e understatement is cleared. "
     "ORIGINAL FINDING (Fail, first delivery): the component applied the Tanker Truck factor to a flatbed IBC-tote delivery. The Basco 6 PDD supplemental sets the rule in terms: 'the mass of cargo is multiplied by the journey distance and the product is multiplied by a Well-to-Wheel emission factor for the appropriate vehicle type used for the journey'. [log:certify.components] [log:standard_efs] [log:standard_efs._primary_source_opened] [log:pdd_supplemental] [log:_derived_values]",
     "Standard EFs 2026 tab row 6; PDD Supplemental Doc 3")
item("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
     "'CO to Basco Routing Map.png' is attached to the distance datapoint and was downloaded and read as pixels this session (1842 x 863). It shows three route options to destination '4675 LA-115, St Landry, LA 71367': via US-287 S and US-287 S, 17 hr 22 min, 1,132 miles, labelled 'Fastest route now, avoids road closures'; via US-287 S, US-287 S and I-20 E, 17 hr 32 min, 1,129 miles; and via I-70 E, 17 hr 36 min, 1,201 miles, carrying the notes 'This route has tolls' and 'Your destination is in a different time zone'. "
     "Certify's 'Distance from Miniforge CO to Basco' reads 1,201 mi - the longest of the three and correctly not the fastest - and it agrees with the Ops Notes allocation input B8 = 1201. The PDD supplemental states the convention in terms: 'The route between origin and destination will be set using Google maps, selecting the longest route if multiple are presented'. The origin field displays 'Your location' with the pin in the Fort Lupton corridor north of Denver; the unnamed-origin point was reviewed and closed on the Week 1 batch and is not re-raised. [log:google_maps_options] [log:google_maps_options._primary_source_opened] [log:shipment_tracker.one_way_distance_B8] [log:pdd_supplemental]",
     "PDD Supplemental Doc 3 longest-route rule; FC-C6"),
item("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
     "Read from the modal INPUTS: mass of load = 'QOWV Transport Mass (CO to B6) [Certify input]' at 31,529 kg. The Ops Notes Total Mass Transported at QOWV!B53 is 31,529.00 kg. Exact match on the correct basis - the gross figure including tote tare, which is what the truck actually hauled. "
     "The two wrong candidates were checked and neither was used: Total Oil Produced is 29,455.40 kg and Total Oil in Batch is 25,521.00 kg, and the reported mass of load matches neither. The Summary tab routes the same value through '=QOWV!B53' into its transport-mass column, so the chain from ledger to Certify is one number. [log:certify.components] [log:ops_notes_qowv.totals_row_53] [log:ops_notes_summary_tab_qowv_row] [log:_derived_values]",
     "Ops Notes QOWV!B53; FC-C7"),
item("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
     "The 'QOWV Transport Mass (CO to B6) [Certify input]' datapoint carries one source and it is the right one: 'INJ-07-2026-W2 Ops Notes.xlsx', linked to that datapoint specifically rather than only to the removal. A verifier opening it lands on the workbook whose QOWV!B53 produces the 31,529 kg figure. [log:certify.attachment_map] [log:certify.certify_sources_enumeration]",
     "Certify Sources tab"),
item("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
     "Read from the modal INPUTS: mass of load 31,529 kg with uncertainty +/-40.82 kg, against the Ops Notes total at QOWV!J53 of 40.82328 kg - the same value at the two decimals this field displays. It is also identical to the Mass of Product uncertainty on the sequestration component, which is correct: the same 36 totes were weighed once each, so the same 1.13398 kg per weighing propagates to both. [log:certify.components] [log:ops_notes_qowv.totals_row_53] [log:_derived_values]",
     "Isometric Standard S3.7.3 Option B"),

# ---------------------------------------------------------------- SECTION 6
section("Section 6 - Certify: Transport Embodied Emissions")
item("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Pass",
     "CORRECTED AND RE-VERIFIED LIVE 2026-08-06 21:16Z. The component now reads 'CO to LA Flatbed Truck Transport Embodied Emissions - QOWV' and its factor datapoint shows 0.1198 kgCO2e/km. That is the live 2026 tab's Non-Tanker Truck embodied row (row 11, final quantity 0.0001927908256 MT CO2e/mi) expressed per km: 0.0001927908256 divided by 1.609344 gives 0.0001198 MT/km. "
     "The output confirms the correct factor: 3,028.197351 mi x 0.0001927908256 MT/mi = 0.583809 tCO2e, and Certify reports 0.584 tCO2e. The tanker embodied factor of 0.0002375605888 previously applied would give 0.719380 tCO2e. The 0.135572 tCO2e overstatement is cleared, and the per-mile basis with no mass term is retained. "
     "ONE LABELLING POINT, not a value issue: the datapoint is titled 'Emissions Factor - Vehicle Embodied Emissions - Flatbed Truck', but the 2026 tab has no Flatbed row on the embodied side - the row the value comes from is titled 'Vehicle Embodied Emissions --Non-Tanker Truck'. Its internal reference id also still reads inj-07-2026-w2-qowv-tanker-embodied-ef. See the sidebar. "
     "ORIGINAL FINDING (Fail, first delivery): the component applied the Tanker Truck embodied factor to a flatbed tote delivery. [log:certify.components] [log:standard_efs] [log:standard_efs._primary_source_opened] [log:_derived_values]",
     "Standard EFs 2026 tab row 11")
item("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Pass",
     "Read from the modal INPUTS: distance travelled = 'Aggregate Distance Transported CO to B6 - QOWV' at 3,028.1973512211907 mi. The tracker's Batch Mileage Allocation at C22 = '=G18' is 3,028.197351 mi. Exact match, carried at full precision rather than the 3,028 mi shown rounded on the Datapoints list. The allocated figure - not the 1,201 mi one-way distance - is correctly what the embodied component uses. [log:certify.components] [log:shipment_tracker.batch_mileage_allocation_C22] [log:shipment_tracker_cells_are_formulas]",
     "Ops Notes 'QOWV Shipments & EE Allocation'!C22"),
item("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Pass",
     "CORRECTED AND RE-VERIFIED LIVE 2026-08-06 21:16Z. All three required evidence types are now attached to the aggregate-distance datapoint. The Sources tab shows 'CO to Basco Routing Map_src_1KSTWP2AP1S0QQPF.png' linked to 'Aggregate Distance Transported CO to B6 - QOWV', alongside 'INJ-07-2026-W2 Ops Notes.xlsx' on the same datapoint, and the removal's source count has gone from 38 to 41. "
     "The Ops Notes discharges the Shipment Tracker requirement through its 'QOWV Shipments & EE Allocation' tab and the Charm Contents requirement through its per-tote production-period ledger; neither exists as a standalone file for 2026 weekly batches. So the reported 3,028.197351 mi is now provable end to end from documents attached to the figure itself: the map evidences the 1,201 mi leg and the Ops Notes evidences the six per-truck tote-count shares that apportion it. "
     "ORIGINAL FINDING (Fail, first delivery): only the Ops Notes was attached to this datapoint; the route map sat on the removal but was linked to the separate 'Distance from Miniforge CO to Basco' datapoint instead, so the mileage the allocation multiplies was not evidenced on the figure being reported. [log:certify.attachment_map] [log:certify.certify_sources_enumeration] [log:batch_folder_inventory] [log:shipment_tracker]",
     "Certify Sources tab; Document Location Rule")
# ---------------------------------------------------------------- SECTION 7
section("Section 7 - Certify: Production Emissions")
item("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", "Pass",
     "Every period that contributed mass is accounted for. The batch draws on five monthly production periods - July 2025 (2 totes), August 2025 (23), September 2025 (2), November 2025 (8) and December 2025 (1), together 36 totes - and all five are captured in one aggregated component, 'Pyrolysis - Charm QOWV PP Emissions', carrying a production-mass-weighted blended carbon intensity. "
     "The aggregation reconciles exactly. Per-period mass times per-period intensity gives July 1,322.80 kg at 0.1374, August 18,805.70 kg at 0.1106, September 1,671.80 kg at 0.1287, November 6,687.70 kg at 0.1392 and December 967.40 kg at 0.1631, summing to 3,565.53458 kg, which equals the Ops Notes per-tote emissions total at I53 = 3565.53458 kg and reproduces the component's own output of 3.565535 tCO2e against the 3.566 Certify displays. No period is omitted, and aggregating periods into a single mass-weighted component is an accepted structure. [log:production_periods] [log:ops_notes_qowv.totals_row_53] [log:certify.components] [log:_derived_values]",
     "Charm Contents role carried by Ops Notes ledger; FC-C2"),
item("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Fail",
     "The Certify aggregate is faithful to the Ops Notes, but one period's totes carry another period's intensity. Read from the modal INPUTS: carbon emission factor = 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' at 0.12104858803479154 tCO2e/t. Ops Notes H53 is the formula '=IFERROR(SUMPRODUCT(D11:D46,H11:H46)/SUM(D11:D46),\"\")' and returns 0.121048588; recomputing the weighted average independently from the 36 per-tote net-produced masses and intensities gives 0.121048588035. So Certify reproduces the sheet exactly, and the defect is upstream in the sheet's period-to-intensity pairing. "
     "Four of the five periods tie to their own Production Period Summary, reading the 'Kg Emissions/Kg Material' figure on the row whose Output Type is 'Aqueous': August 2025 = 0.1105698239 against the 0.1106 applied, September 2025 = 0.128689567 against 0.1287, November 2025 = 0.1392 against 0.1392, and December 2025 = 0.1630616644 against 0.1631. "
     "The fifth does not. The two totes labelled 'July 2025' - tags 120555 (MFO Lot 2808) and 120504 (MFO Lot 2908) - carry 0.1374, but the July 2025 Production Period Summary reports Aqueous 0.1575553395; its 'Days in Production Period 8' cell reads 31 and the separately titled 'Production Period 8 Summary' holds an identical output table, so July 2025 and PP8 are the same period. The 0.1374 applied is instead the PP7 figure, whose summary reads 'Aqueous | 73,495 | 72.98% | 9.21% | 6,768.89 | 27.93% | 10.096 | 0.1374' and whose 'Days in Production Period 7' cell reads 30, i.e. June 2025. The sister QOWV batch in this reporting period applies 0.1373671128 to totes it labels PP#7 and 0.1575553395 to totes it labels PP#8, which is the same pairing read the other way round. "
     "RE-CHECKED LIVE 2026-08-06 21:17Z - STILL OPEN. Nothing has moved on this item. The Ops Notes QOWV tab rows 11 and 12 still read 'MFO Lot 2808 (LOT00002808), July 2025' and 'MFO Lot 2908 (LOT00002908), July 2025', both still carrying 0.1374. The July 2025 Production Period Summary still reports Aqueous 'Kg Emissions/Kg Material' 0.1576. The Ops Notes weighted average at H53 is still 0.121048588 and the Certify pyrolysis component is still 3.566 tCO2e. Neither the month label nor the intensity was changed. "
     "TWO READINGS remain open and the evidence does not settle which. If the label is wrong and these are June 2025 totes, the intensity stands and the label needs correcting. If the label is right, the intensity should be 0.1575553395: production emissions on those two totes would rise from 181.75 kg to 208.41 kg, a delta of 26.66 kg, the blended intensity would move from 0.121048588 to 0.121953736, the pyrolysis component from 3.566 to 3.592196 tCO2e and net removal from 3.677 to 3.650 tCO2e. "
     "THE DIRECTION MATTERS: the intensity applied is the lower of the two, so if the July label is correct then production emissions are understated and net removal is overstated by 0.026661 tCO2e. An error that inflates the claim has to be resolved before submission, not after. "
     "Lot numbers do not decide it: the sister QOWV batch's June totes run lots 2374 to 2790 and its July totes run 3042 to 3072, and these two sit between at 2808 and 2908. The July reporting-period VVB guidance names 'June, August, and September 2025' as the previously reported periods supplying this period's QOWV oil and does not name July 2025, which points toward the label. [log:certify.components] [log:ops_notes_qowv] [log:pp_summaries] [log:pp_summaries._primary_source_opened] [log:vvb_guidance] [log:_derived_values]",
     "Production Period Summaries; FC-C10"),
item("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Fail",
     "The required evidence is not attached to the datapoint. The 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' datapoint carries 32 sources, and the batch Ops Notes is not among them. Every one of the 32 is a November 2025 production-period document or an artefact of that period's package: the November 2025 Production Period Summary appears four times, alongside November biomass throughput, November waste disposal, November water usage, the November propane calculator three times, November diesel, SP&C November, Cap Ex MRV November, Miniforge up-time, eleven copies of 'Nov-16-2025-distance-transported-route_map.png', one Nov-04-2025 route map, one Aug-31-2025 route map, route.geojson, an invoice PDF and a csv. "
     "The Ops Notes is attached to this removal and linked to five other datapoints - aggregate distance, transport mass, pyrolysis mass, mass of injectant and carbon content - but not to the carbon intensity. It is the required evidence standard for production intensity because it is the document that computes the production-mass-weighted average across all totes in the injection, at H53. No Production Period Summary is attached for July, August, September or December 2025 either, so four of the five contributing periods have no period-level corroboration in the package while November has eleven route maps. "
     "RE-CHECKED LIVE 2026-08-06 21:16Z - STILL OPEN, and known to be outstanding. The removal's source count rose from 38 to 41 with the other corrections, but every new attachment went to the aggregate-distance and embodied-factor datapoints. The 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' datapoint still carries 32 sources and 'INJ-07-2026-W2 Ops Notes.xlsx' is still not among them. "
     "On the sister QOWV batch in this same reporting period, 'INJ-07-2026-W1 Ops Notes.xlsx' is attached to that batch's carbon-intensity datapoint, so the linking convention is established and this removal departs from it. Linking the batch Ops Notes to this datapoint closes the item. [log:certify.attachment_map] [log:certify.certify_sources_enumeration] [log:certify.ci_datapoint_source_count] [log:sister_batch_same_rp] [log:ops_notes_qowv.totals_row_53]",
     "Certify Sources tab; CI evidence standard (Ops Notes weighted average)"),
item("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", "Pass",
     "Read from the modal INPUTS: mass = 'QOWV Pyrolysis Mass [Certify input]' at 29,455.400000000016 kg. The Ops Notes total net oil produced at QOWV!D53 is 29,455.40 kg, the sum of the per-tote gross-minus-tote-mass column across all 36 rows. Exact match on the correct basis - net oil produced, which is what the pyrolysis stage actually made - and not the injected mass of 25,521.00 kg, which would have understated production emissions. [log:certify.components] [log:ops_notes_qowv.totals_row_53] [log:_derived_values]",
     "Ops Notes QOWV!D53"),
item("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", "Pass",
     "Read from the modal INPUTS: mass 29,455.400000000016 kg with uncertainty +/-40.82328000000002 kg, against the Ops Notes total at QOWV!J53 of 40.82328 kg. The uncertainty is present and correct - 1.13398 kg per tote across 36 totes - which matters because the pyrolysis term at 3.566 tCO2e is a dominant input on this removal, so it does not qualify for any omission carve-out and a missing figure here would have been a Fail. [log:certify.components] [log:ops_notes_qowv.totals_row_53] [log:_derived_values]",
     "Bio-oil Geological Storage v1.2 S6.5.1; FC-C12"),
item("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
     "No Charm Contents sheet exists as an artifact for 2026 weekly time-block batches - the batch folder holds the Ops Notes, a Testing subfolder, a Scale Tickets subfolder and a Completed QA Checklists subfolder, and none of the 38 Certify sources is a Charm Contents file. Its function, the per-production-period mass breakdown for the batch, is carried by the Ops Notes QOWV IBC ledger, where column G gives each tote's production period against column D's net oil produced. "
     "That workbook is attached in Certify and linked to the 'QOWV Pyrolysis Mass [Certify input]' datapoint specifically, so the 29,455.40 kg figure is evidenced by the document that now holds the content. [log:batch_folder_inventory] [log:certify.attachment_map] [log:certify.certify_sources_tab_total] [log:ops_notes_qowv.totals_row_53]",
     "Certify Sources tab; Document Location Rule"),

# ---------------------------------------------------------------- SECTION 8
section("Section 8 - Other")
item("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total >= the transport-process sum?", "Pass",
     "CORRECTED AND RE-VERIFIED LIVE 2026-08-06 21:16Z. 'BCU - Transport Process' now applies a constant reduction of 5.241 tCO2e, evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf' linked to the datapoint. The only diesel transport-process emission on the removal is 'CO to LA Flatbed Truck Transport Process Emissions - QOWV' at 5.241 tCO2e, which recomputes at full precision as 31.529 t x 1,201 mi x 0.0001384 MT/(t.mi) = 5.240700 tCO2e. The BCU equals the emission it offsets, so the offset is complete. "
     "ORIGINAL FINDING (Fail, first delivery): the BCU was 4,328 kgCO2e against a filed emission of 4,328.121 kgCO2e, 0.121 kg short, and it was pegged to the tanker factor - so once the flatbed factor went in the required figure rose to 5,240.700 kgCO2e and the shortfall would have widened to 912.700 kg. Both moved together, which is the right way to make this correction. [log:certify.components] [log:certify.attachment_map] [log:standard_efs] [log:_derived_values]",
     "Charm methodology - all diesel transport-process emissions must be BCU-offset")
# ---------------------------------------------------------------- SECTION 9
section("Section 9 - Aqueous Buffering (LCS)")
item("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist (correct mass, correct EF, evidenced)?", "N/A",
     "No LCS use is reported for this batch, so no matching Certify component is required. An every-cell scan of all eight Ops Notes tabs for LCS, liquid calcium, calcium sulfate, buffer, caustic, NaOH and pre-treat returns zero hits, run twice - once against cached cell values and once against formulas - and the QOWV tab carries no pre-treatment column of any kind. The Summary tab's QOWV row corroborates it, recording Sparging Loss 0.00 kg and Filtration Loss 0.00 kg. The July reporting-period VVB guidance, read in full, contains no LCS section. [log:lcs_absence] [log:lcs_absence._primary_source_opened] [log:ops_notes_summary_tab_qowv_row] [log:vvb_guidance]",
     "Ops Notes; FC-C4")

# ---------------------------------------------------------------- SIDEBAR
r += 1
c = ws.cell(row=r, column=1, value="Sidebar Observations (no Pass/Fail status - flagged for attention)")
c.font = BOLD
c.fill = HDR
for col in range(2, 6):
    ws.cell(row=r, column=col).fill = HDR
r += 1

sidebar = [
    "Measured tote residual is large. Across the 36 totes, 3,934.40 kg of oil stayed in the containers - 13.36 % of net oil produced, averaging 109.29 kg per tote and ranging from 29.90 kg (tag 245156) to 322.40 kg (tag 120504, which retained 53 % of its own oil). The direction is conservative because the residual is deducted from the injected mass, and the figures are measured rather than assumed, so nothing is held against the batch. Still worth a look operationally: a tote that discharges only 286 kg of the 608.40 kg it produced suggests a drain or viscosity problem on that unit.",
    "Nominal tote tare in the production-mass basis. Net oil produced is computed as gross less the 57.60 kg tote-tag mass, a nominal figure, while net oil injected uses the measured post-unload weight. That is the documented basis - the PDD supplemental states oil mass is 'the gross weight of the tote less its tare weight' and the ledger header states 'tote tag mass is authoritative' - and it is the same convention carried on the sibling WODO and Week 1 QOWV batches, so it is graded Pass here. Noting it rather than dropping it, because the Week 1 QOWV checklist left the identical convention as an open question for Max and the two oil types should be graded alike.",
    "Embodied factor label points at a row that is not on the emission-factor sheet. After the correction the datapoint is titled 'Emissions Factor - Vehicle Embodied Emissions - Flatbed Truck' and carries the right number, but the 2026 tab has no Flatbed row on the embodied side - the row supplying 0.0001927908256 MT CO2e/mi is titled 'Vehicle Embodied Emissions --Non-Tanker Truck'. A verifier matching the datapoint title against the sheet will not find it. The datapoint's internal reference id also still reads inj-07-2026-w2-qowv-tanker-embodied-ef. Both are labels only; the value is correct. Retitle to Non-Tanker Truck to match the source row.",
    "Collection method flipped on four datapoints. Aggregate distance, both emission factors and the transport mass now show Collection method REPORTED where they previously showed DERIVED. No value changed. Worth a glance to confirm the switch was intended rather than a side effect of re-entering the datapoints.",
    "The batch Ops Notes is now also attached to the embodied emission-factor datapoint. An emission factor is evidenced by the emission-factor sheet, which is also attached there. Harmless, but it is the Ops Notes attachment that item 7.3 needs and it went to the factor instead of to the carbon intensity.",
    "Duplicate source attachments on the carbon-intensity datapoint. Of its 32 sources, 'Nov-16-2025-distance-transported-route_map.png' appears eleven times, 'November 2025 Production Period Summary.xlsx' four times and 'Propane Consumption Calculator 11_1_25-11_30_25 (1).xlsx' three times. De-duplicating would make the evidence set legible without removing anything.",
    "A WODO document is attached to the QOWV carbon-intensity datapoint: 'WODO 20251216 CAR-445 (1).pdf'. It may belong there as co-product allocation input, but on a QOWV intensity it invites a verifier question.",
    "VVB guidance production-period coverage. The July 1 - July 31 guidance states that 'The earlier Periods (June, August, and September 2025) correspond to the aqueous-fraction (QOWV) oil injected this period, and November-December 2025 correspond to the oil-fraction (WODO) oil'. This batch's QOWV oil draws on periods labelled July, August, September, November and December 2025 - so November and December supply QOWV here despite being assigned to WODO in the guidance, and the July label is not in the guidance list at all. The paragraph needs updating for the actual period mix, and doing so will also force a decision on item 7.2's July-versus-June question.",
    "Scale Tickets subfolder. It holds only AECN rail offload tickets and no QOWV tote weighing records. This is not held against the batch - the Ops Notes IBC ledger is the accepted weighing record for tote deliveries - but it means the 36 gross weights and 36 measured empty weights rest on that ledger alone.",
    "Template remnants. QOWV tab rows 56 to 73 retain sparging-loss template formulas in columns G and H that evaluate to blank. No data and no effect on any total; worth clearing so the used range ends at the totals row.",
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
    "STATUS SUMMARY: %d Pass - %d Flag - %d Fail - %d N/A  (%d items)  |  "
    "RE-REVIEW STATE, read live against Certify on 2026-08-06 at 21:16-21:18Z. Certify Net is now 3.677 tCO2e = Sequestrations 7.861 + BCU 5.241 - Activities 9.390 - Uncertainty 0.035, against 3.541 tCO2e at first delivery. The improvement of 0.136 tCO2e is exactly what the first delivery forecast for these corrections. "
    "FOUR OF THE SIX FINDINGS ARE CLOSED, each re-verified against the live entry rather than taken on report. Item 5.1: the process factor is now the flatbed row, 31.529 t x 1,201 mi x 0.0001384 = 5.240700 tCO2e against the 5.241 Certify shows, and the component is retitled Flatbed Truck. Item 6.1: the embodied factor is now the non-tanker value, 3,028.197351 mi x 0.0001927908256 = 0.583809 tCO2e against the 0.584 Certify shows. Item 8.1: the BCU was resized in the same pass to 5.241 tCO2e, equal to the corrected process emission. Item 6.3: the routing map is now attached to the aggregate-distance datapoint and the removal source count went from 38 to 41. Item 1.3, the blank ship-date column, was reviewed by Max and ruled immaterial. "
    "TWO FINDINGS REMAIN OPEN, both in Section 7. Item 7.3, the known one: the batch Ops Notes is still not attached to the carbon-intensity datapoint, which still carries 32 sources all drawn from November 2025 paperwork for a figure that averages five months. The sister QOWV batch in this reporting period does have its Ops Notes attached there. "
    "Item 7.2 is ALSO STILL OPEN, which is worth flagging because it was expected to be closed. Nothing moved: Ops Notes rows 11 and 12 still read July 2025 with intensity 0.1374, the July 2025 Production Period Summary still reports Aqueous 0.1576, the weighted average at H53 is still 0.121048588 and the pyrolysis component is still 3.566 tCO2e. Either those two totes are June oil and the month label needs changing, or they are July oil and the intensity should be 0.1575553395 - worth 26.66 kg, and in the direction that overstates net removal by 0.026661 tCO2e. The July reporting-period guidance lists June, August and September as the months feeding this period Aqueous oil and does not list July, which points at the label. "
    "EVERYTHING ELSE WAS CLEAN AT FIRST DELIVERY AND IS UNCHANGED: all five Ops Notes totals reconcile to a zero delta against the 36-tote ledger, the Aqueous measured-loss method is applied with no Standard Loss anywhere and the measured residual closes both ways at 3,934.40 kg, the uncertainty is 1.13398 kg per tote across 36 totes on all three components that need it, all fifteen allocation cells are live formulas, the 36-tote roster matches the ledger with no orphans, the carbon content of 8.4 percent matches certificate SR26-04220.002, and the distance of 1,201 mi is the longest of the three routes read from the map. "
    "Two label-only points are in the sidebar: the corrected embodied factor datapoint is titled Flatbed Truck while the sheet row supplying its value is titled Non-Tanker Truck, and that datapoint internal reference id still says tanker."
    % (counts.get("Pass", 0), counts.get("Flag", 0), counts.get("Fail", 0), counts.get("N/A", 0), total)
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

out = HERE / "Charm_Aqueous_QOWV_QA_Checklist_INJ-07-2026-W2.xlsx"
wb.save(out)
print("saved", out)
print("counts", counts, "total", total)
