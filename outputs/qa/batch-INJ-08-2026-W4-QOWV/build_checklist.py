#!/usr/bin/env python3
"""Build the Charm Aqueous (QOWV) QA checklist for batch INJ-08-2026-W4."""
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = Path(__file__).parent
LOG = HERE / "batch_INJ-08-2026-W4-QOWV_source_reads.json"
log = json.loads(LOG.read_text())

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
    ("Batch ID", "INJ-08-2026-W4  (QOWV / Aqueous portion)"),
    ("Reporting Period", "Certify removal window 16 Aug 2026 to 22 Aug 2026; Ops Notes injection week 2026-08-15 to 2026-08-22"),
    ("Reviewer", "Claude (QA agent) - for Max Lavine review"),
    ("Date", "2026-09-01 (independent fresh re-verification; all findings below re-derived from primary sources in this session)"),
    ("Injection Site", "Basco 6 (Louisiana)"),
    ("Oil Type", "Aqueous / QOWV (Charm-produced, Fort Lupton CO) - 42 IBC totes, two transport lanes: 41 direct CO->Basco, 1 routed via Charm Kansas"),
    ("Production Periods", "November 2025 (3 totes, CI 0.1392140548), December 2025 (3 totes, CI 0.1630616644), February 2026 (2 totes, CI 0.1330497939), March 2026 (21 totes, CI 0.1185251532), April 2026 (7 totes, CI 0.1314184532), PP#7 (1 tote, CI 0.1373671128), PP#8 (2 totes, CI 0.1575553395)"),
    ("Certify Removal ID", "rmv_1M105QK8B1S046XF  |  Net 5.139 tCO2e"),
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
     "The Testing subfolder holds one SGS certificate covering both this week's oil types in a single two-page report, SR26-05110. Page 1 (.001, client id '08-2026-W4 AECN') covers the AECN fraction and is not used here. Page 2 (.002, client id '08-2026-W4 QOWV', location BASCO LOUISIANA) is this batch: sampled 20-Aug-2026 08:00, analysed 26-Aug-2026 13:23-15:15, signed by Rachel Oxley. It reports Carbon 8.1% (m/m) by ASTM D5291 Method C, Hydrogen 10.0%, Nitrogen <0.75%, kinematic viscosity 0.9016 cSt, acid number 51 mg KOH/g, density 1.046 g/cm3. "
     "The PDF pages were downloaded as rendered images and read as pixels this session, not OCR'd. The 8.1% carbon figure is exactly what the Certify Sequestration component reports, so the certificate supports the claim. [log:lab_results] [log:lab_results._primary_source_opened] [log:batch_folder_inventory]",
     "VR Appendix 1; SGS CoA SR26-05110.002"),
item("1.2", "Are Ops Notes in the folder and fully completed?", "Pass",
     "'INJ-08-2026-W4 Ops Notes' is in the batch folder with five tabs, and the QOWV tab is complete. All 42 tote rows (301000-301035 range plus Kansas tag 118846) carry tag, gross mass, tote mass, net oil produced, empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty, with no blanks. Every totals cell at row 55 is a live SUM/SUMPRODUCT formula, confirmed by Name Box navigation to H55: '=IFERROR(SUMPRODUCT(D11:D53,H11:H53)/SUMIF(H11:H53,\"<>\",D11:D53),\"\")', not a typed number. Per-tote net-injected formula (F11) is '=IF(E11=\"\",\"\",B11-E11)', confirmed live. [log:ops_notes_qowv] [log:ops_notes_qowv._primary_source_opened] [log:batch_folder_inventory]",
     "VR Appendix 1; Ops Notes QOWV tab"),
item("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Pass",
     "Present as the 'QOWV Shipments & EE Allocation' tab inside the same Ops Notes workbook (2026 weekly schema). It carries the batch summary row (42 totes, injection week 2026-08-15 to 2026-08-22), the one-way direct distance input (1,201 mi), a six-truck direct-lane allocation table (Table A), a two-leg via-Kansas allocation table (Table B, 537 mi + 684 mi = 1,221 mi one-way), and an explicit reconciliation row stating '42 = 42, OK - every tote allocated'. Five numbered notes document the Kansas routing basis, precedent, and required route-map evidence. [log:shipment_tracker] [log:shipment_tracker._primary_source_opened] [log:batch_folder_inventory]",
     "VR Appendix 1; Ops Notes 'QOWV Shipments & EE Allocation' tab")

# ---------------------------------------------------------------- SECTION 2
section("Section 2 - Ops Notes")
item("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", "Pass",
     "Reported 42,850.00 kg at QOWV!B55 (a SUM formula, not a constant). This is the sum of 42 per-tote gross masses. It also splits cleanly by lane: 'Total CO->LA' = 41,961.00 kg (41 totes) + 'Total CO->KS->LA' = 889.00 kg (1 tote, tag 118846) = 42,850.00 kg, matching exactly. [log:ops_notes_qowv.totals_row_55] [log:ops_notes_qowv.lane_split_rows_56_57]",
     "Ops Notes QOWV!B55"),
item("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", "Pass",
     "Reported 40,430.80 kg at QOWV!D55. Each per-tote Net Oil Produced cell = Gross Mass - Tote Mass (uniform 57.60 kg IBC tare); summing gross (42,850.00) less total tote mass (2,419.20 = 57.60 x 42 totes) gives 40,430.80 kg exactly, matching the reported total. [log:ops_notes_qowv.totals_row_55] [log:_derived_values]",
     "Ops Notes QOWV!D55"),
item("2.3", "Is the 'Total Oil in Batch' value correctly computed (Aqueous: measured pre-unload minus measured post-unload per tote, no Standard Loss)?", "Pass",
     "Reported 36,568.50 kg at QOWV!F55, and the Aqueous method is correctly applied. Per-tote formula (spot-checked live at F11) is '=IF(E11=\"\",\"\",B11-E11)' - Gross Mass less the measured Empty Tote Weight (post-unload weight including residue), a genuine measured pair, not a fixed allowance. Total Mass Transported 42,850.00 kg less Total Empty Tote Weight 6,281.50 kg = 36,568.50 kg, matching the reported Total Oil in Batch exactly. No Standard Loss column or term exists anywhere on the QOWV tab - the tab has only Gross Mass, Tote Mass (tare), Net Oil Produced, Empty Tote Weight and Net Oil Injected. [log:ops_notes_qowv.totals_row_55] [log:ops_notes_qowv.per_tote_formulas]",
     "Ops Notes QOWV!F55; FC-C1 (Aqueous branch)"),
item("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
     "Reported 47.62716 kg at QOWV!J55. Per-tote precision is 2.5 lb / 2.20462 = 1.13398 kg per weighing event. For 42 totes: 1.13398 x 42 = 47.62716 kg exactly, matching the reported figure to five decimal places. The lane split also ties: 41 direct totes x 1.13398 = 46.49318 kg (matches row 56) and 1 Kansas tote x 1.13398 = 1.13398 kg (matches row 57), summing to 47.62716 kg. This is the Charm per-tote precision, not AECN's 72.57 kg per-truck figure. [log:ops_notes_qowv.totals_row_55] [log:ops_notes_qowv.lane_split_rows_56_57]",
     "Isometric Standard S3.7.3 Option B; FC-C8"),

# ---------------------------------------------------------------- SECTION 3
section("Section 3 - Bio-Oil Shipment Tracker")
item("3.1", "Are totes for the RP correctly identified?", "Pass",
     "42 totes are identified for the batch: 41 across six direct shipping orders (COLA_27, COLA_30, COLA21, COLA_29, COLA_25, and 'Truck 2') plus 1 via the two-leg Kansas route (tag 118846). The tracker carries an explicit reconciliation row: 'totes allocated vs QOWV ledger: 42, 42, OK - every tote allocated', tying the allocation tables to the Ops Notes ledger's own tote count. [log:shipment_tracker.reconciliation_note] [log:shipment_tracker.table_a_direct] [log:shipment_tracker.table_b_via_kansas]",
     "Ops Notes 'QOWV Shipments & EE Allocation' tab"),
item("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Pass",
     "The reconciliation row confirms count-level agreement (42 = 42) between the allocation tables and the Ops Notes ledger. This tracker's schema apportions totes by shipping-order/truck-count rather than carrying a per-tag roster (the per-tag roster with fraction, gross mass and production period lives solely in the Ops Notes QOWV ledger, whose header states 'tote tag mass is authoritative') - the same schema limitation seen on every 2026 weekly QOWV batch to date. Truck-level tote counts (18+11+6+2+2+2=41 direct, 1 Kansas) sum correctly to 42. [log:shipment_tracker.reconciliation_note] [log:shipment_tracker.table_a_direct]",
     "Ops Notes ledger vs allocation tables; FC-C5"),
item("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
     "Every computed cell checked live via Name Box navigation is a formula, not a constant. Batch Share of Truck: E12 = '=IFERROR(D12/C12,\"\")' (direct lane). Allocated Miles: G12 = '=IFERROR(E12*F12,\"\")'. Kansas leg 1 share: E26 = '=IFERROR(D26/C26,\"\")'. Grand Total: G30 = '=G18+G28'. All formulas reference tote-count and mileage inputs; none is a typed number. [log:shipment_tracker_cells_are_formulas]",
     "Auditability; FC-C3"),
item("3.4", "Are computed outputs computed correctly per the allocation formulas?", "Pass",
     "Direct lane (Table A) reproduces exactly: COLA_27 18/20=90.0% x 1,201mi=1,080.9mi; COLA_30 11/20=55.0%=660.6mi; COLA21 6/20=30.0%=360.3mi; COLA_29 2/20=10.0%=120.1mi; COLA_25 2/20=10.0%=120.1mi; Truck2 2/36=5.6%=66.7mi. Subtotal A = 2,408.7mi, matching the sheet exactly. "
     "Kansas lane (Table B): Leg 1 = 1 of 34 totes across 2 trucks x (537x2=1,074.0mi) = 31.6mi; Leg 2 = 1 of 6 totes x 684.0mi = 114.0mi. Subtotal B = 145.6mi. Grand Total A+B = 2,408.7 + 145.6 = 2,554.3mi, matching the sheet's Grand Total Allocated Miles exactly. Distances applied one-way with no round-trip doubling, correct for this batch. [log:shipment_tracker.table_a_direct] [log:shipment_tracker.table_b_via_kansas] [log:shipment_tracker.grand_total_allocated_mi]",
     "RP Share x one-way mileage; process vs embodied distance convention"),
item("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", "Pass",
     "Tag-level cross-check is not possible against this tracker's schema - it apportions by shipping-order/truck tote-counts, not a per-tag roster, the same limitation present on every 2026 weekly QOWV batch reviewed to date ('Totals-on-truck counted from BGN master Ship Status', an external system outside this Ops Notes file). What IS checkable ties exactly: total tote count (42=42, explicit reconciliation row), lane split (41 direct + 1 Kansas matching the Ops Notes lane-split rows 56-57 exactly on both gross mass and uncertainty), and the single identifiable tag (118846, Kansas) matches between the tracker's Table B note and the Ops Notes ledger row. [log:shipment_tracker.reconciliation_note] [log:ops_notes_qowv.lane_split_rows_56_57] [log:shipment_tracker.table_b_via_kansas]",
     "Ops Notes ledger vs allocation tables; FC-C5"),

# ---------------------------------------------------------------- SECTION 4
section("Section 4 - Certify: Injection Sequestration")
item("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
     "Read from the component modal INPUTS: carbon content of product = 'Carbon Content of Bio-oil Injected (per injection)' at 8.1%. SGS certificate SR26-05110.002 (client id '08-2026-W4 QOWV') reports Carbon 8.1% (m/m). Exact match. Gross sequestration reproduces from these inputs: 36,568.5 kg x 8.1% carbon = 2,962.0485 kg carbon x (44/12) = 10,861.85 kg CO2e = 10.862 tCO2e, matching the Certify-displayed 10.862 tCO2e exactly. [log:certify.components.injection_sequestration] [log:lab_results] [log:_derived_values]",
     "Certify Injection sequestration cmp_1M105QK8B1S00C9S"),
item("4.2", "Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?", "Pass",
     "The modal shows '2 sources' against carbon content of product. The Sources tab resolves them as 'CHARM INDUSTRIAL - 08-2026-W4 AECN + QOWV (SR26-05110.001-002).pdf' (the SGS certificate) and 'INJ-08-2026-W4 Ops Notes.xlsx' - confirmed by expanding the Ops Notes source row's '+6 more' datapoint list, which explicitly includes 'Carbon Content of Bio-oil Injected (per injection)'. Both evidence types are linked to the datapoint itself. [log:certify.attachment_map] [log:certify.components.injection_sequestration]",
     "Certify Sources tab"),
item("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
     "Read from the modal INPUTS: mass of product = 36,568.5 kg with uncertainty +/-47.627 kg. Ops Notes QOWV!J55 total uncertainty is 47.62716 kg - the same value to the precision Certify displays. Entered as an absolute mass, not a percentage. [log:certify.components.injection_sequestration] [log:ops_notes_qowv.totals_row_55]",
     "Isometric Standard S3.7.3; MRV Uncertainty Cheat Sheet"),
item("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty?", "Pass",
     "Read from the modal INPUTS: carbon content 8.1% with uncertainty +/-0.0324%. Expected value = 0.004 x 8.1 = 0.0324, matching exactly. Entered as an absolute percentage-point value, not the literal 0.4. [log:certify.components.injection_sequestration] [log:_derived_values]",
     "0.4% relative uncertainty on carbon content"),

# ---------------------------------------------------------------- SECTION 5
section("Section 5 - Certify: Transport Process Emissions (two lanes: direct CO->LA and via-Kansas CO->KS->LA)")
item("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
     "Both Transport Process components display the same emission factor datapoint, 'Flatbed, Northern America, WTW' at 0.086 kgCO2e/(km.t). This ties to the live 2026 Standard EFs tab row 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck' = 0.0001384 MT CO2e/t-mi (0.1384/1.60934 = 0.0860 per km, matching the display). Full-precision native mile-basis math reproduces both component outputs exactly: CO to LA lane 41.961t x 1,201mi x 0.0001384 = 6.97469t (Certify shows 6.975t); CO->KS->LA lane 0.889t x 1,221mi x 0.0001384 = 0.15023t (Certify shows 0.150t). Neither lane uses the Tanker Truck factor (0.0001143 MT/t-mi, which would give materially different results). [log:certify.components.transport_process_co_to_la] [log:certify.components.transport_process_co_to_ks_to_la] [log:standard_efs] [log:_derived_values]",
     "Standard EFs 2026 tab; GLEC V3.2 2025"),
item("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used, for BOTH lanes?", "Fail",
     "DIRECT LANE (CO to LA): Pass. 'Distance from Miniforge CO to Basco' = 1,201mi, matching the Shipment Tracker's one-way input exactly, evidenced by 'CO to Basco Routing Map.png' attached specifically to this datapoint. "
     "KANSAS LANE (CO->KS->LA): Fail. The 'Distance traveled' datapoint reports 1,221mi - the correct VALUE, reconciling exactly to the Shipment Tracker's two-leg sum (537mi Charm CO->Charm KS + 684mi Charm KS->Basco LA = 1,221mi one-way). But its sole attached source is 'CO to Basco Routing Map.png' - the SAME direct-route map used for the 1,201mi datapoint above, which by definition cannot depict a different, longer, two-leg 1,221mi route through Kansas. "
     "The Shipment Tracker's own sheet note explicitly names the required evidence: 'filed route maps linked at B21:C22 - \"Charm CO to Charm KS.png\" (537mi, I-70 E) and \"Charm KS to Charm LA.png\" (684mi, I-49 S). Attach both to the Certify transport-distance datapoints for these removals.' Neither of those two named files appears anywhere among the removal's 38 Certify sources - confirmed by a full enumeration of every source filename. The 1,221mi figure is independently correct and derivable from the Shipment Tracker's own B21:B23 inputs, but the datapoint AS FILED IN CERTIFY carries evidence that misrepresents what was traveled, which is the same failure the checklist standard treats as 'distance not evidenced' or 'distance from a different routing tool'. [log:certify.components.transport_process_co_to_ks_to_la] [log:shipment_tracker.distance_source_note] [log:certify.certify_sources_tab_total]",
     "PDD Supplemental Doc 3 longest-route rule; FC-C6; Ops Notes sheet note 5"),
item("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes, for BOTH lanes?", "Pass",
     "CO to LA lane: mass of load = 'QOWV Transport Mass (CO to B6) [Certify input]' at 41,961kg, matching Ops Notes QOWV!row56 'Total CO->LA' gross mass exactly. CO->KS->LA lane: mass of load = 889kg, matching Ops Notes QOWV!row57 'Total CO->KS->LA' gross mass exactly (the single Kansas tote 118846's own gross mass). Both are the gross basis including tote tare, not the net-of-tare figures. [log:certify.components.transport_process_co_to_la] [log:certify.components.transport_process_co_to_ks_to_la] [log:ops_notes_qowv.lane_split_rows_56_57]",
     "Ops Notes QOWV lane-split rows; FC-C7"),
item("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes, for BOTH lanes?", "Pass",
     "Both mass-of-load datapoints carry 'INJ-08-2026-W4 Ops Notes.xlsx' as their source, confirmed via the Sources-tab expansion of the Ops Notes row's linked-datapoint list ('Mass of load' and 'QOWV Transport Mass (CO to B6) [Certify input]' both present). [log:certify.attachment_map]",
     "Certify Sources tab"),
item("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes, for BOTH lanes?", "Pass",
     "CO to LA lane: 41,961kg +/-46.49kg, matching Ops Notes row56 uncertainty 46.49318kg. CO->KS->LA lane: 889kg +/-1.134kg, matching Ops Notes row57 uncertainty 1.13398kg (single tote). Both correctly use the per-lane uncertainty slice rather than the batch-total 47.62716kg. [log:certify.components.transport_process_co_to_la] [log:certify.components.transport_process_co_to_ks_to_la] [log:ops_notes_qowv.lane_split_rows_56_57]",
     "Isometric Standard S3.7.3 Option B"),

# ---------------------------------------------------------------- SECTION 6
section("Section 6 - Certify: Transport Embodied Emissions")
item("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Flag",
     "The value is correct; the label is not. The datapoint reads 'Emissions Factor - Vehicle Embodied Emissions - Tanker Truck' at 0.119794 kgCO2e/km, but this is the live 2026 tab's Non-Tanker Truck row (0.0001927908256 MT CO2e/mi / 1.60934 = 0.119794 kg/km, matching to six figures) - not the Tanker Truck row (0.00023756059 MT/mi, which would display materially higher). The component output confirms the Non-Tanker factor is genuinely applied: 2,554.3mi x 0.0001927908256 = 0.49247t, matching the Certify-displayed 0.492t. This is the same recurring tanker/non-tanker mislabeling pattern seen on every QOWV batch this year (INJ-07-2026-W1/W2-QOWV, INJ-08-2026-W1-QOWV) - a template default that consistently mislabels a genuinely-correct value. [log:certify.components.transport_embodied] [log:standard_efs] [log:_derived_values]",
     "Standard EFs 2026 tab; naming/scope-clarity issue only"),
item("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Pass",
     "'QOWV Embodied Distance (CO to B6) [Certify input]' reads 2,554.3mi (2,554mi on the rounded Datapoints list), matching the Shipment Tracker's Grand Total Allocated Miles (Table A 2,408.7mi + Table B 145.6mi = 2,554.3mi) exactly. This is the fully-allocated aggregate, correctly used in place of either the 1,201mi or 1,221mi one-way lane distances. [log:certify.components.transport_embodied] [log:shipment_tracker.grand_total_allocated_mi]",
     "Ops Notes 'QOWV Shipments & EE Allocation' Grand Total"),
item("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Flag",
     "Three sources are attached to the aggregate-distance datapoint: 'INJ-08-2026-W4 Ops Notes.xlsx' (discharges both the Shipment Tracker requirement, since the allocation tab is embedded in the Ops Notes file, and the Charm Contents requirement, per established precedent - no standalone Charm Contents artifact exists for 2026 weekly batches), 'Charm Inv Bulk Upload March.csv' (a legacy/carried-over attachment of unclear current relevance to a batch spanning totes from seven different production periods, not just March), and 'CO to Basco Routing Map.png'. "
     "The gap: the routing-map evidence covers only the direct-lane portion of the aggregate (2,408.7 of 2,554.3mi, ~94%). The Kansas-leg maps that the Shipment Tracker's own sheet note instructs be attached ('Charm CO to Charm KS.png', 'Charm KS to Charm LA.png', covering the remaining 145.6mi) are absent from all 38 sources - the same gap identified in item 5.2. This does NOT block verification of the reported value: the Shipment Tracker's live formulas independently reconstruct 2,554.3mi from tote counts and the two mileage inputs, so a verifier can confirm the number without the maps. Graded Flag rather than Fail because the value is independently confirmable; the missing Kansas map evidence is a documentation completeness gap. [log:certify.components.transport_embodied] [log:certify.attachment_map] [log:shipment_tracker.distance_source_note]",
     "Certify Sources tab; Document Location Rule"),

# ---------------------------------------------------------------- SECTION 7
section("Section 7 - Certify: Production Emissions")
item("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", "Pass",
     "All seven Production Periods that contributed mass - November 2025 (3 totes), December 2025 (3), February 2026 (2), March 2026 (21), April 2026 (7), PP#7 (1), PP#8 (2) - are captured in one aggregated component, 'Pyrolysis - Charm QOWV PP Emissions', carrying a production-mass-weighted blended carbon intensity of 0.12820663526489975 tCO2e/t. "
     "This exactly matches the Ops Notes weighted-average formula result at QOWV!H55 (0.1282066353), and the component's mass input (40,430.8kg) matches the Ops Notes Total Oil Produced (QOWV!D55, 40,430.80kg) exactly. Component output 40,430.8kg x 0.1282066353 = 5,183.49kg, matching both Certify's displayed 5.183t and the Ops Notes Total Production Emissions cell (5,183.50kg) to rounding. No period is omitted; aggregating seven periods into one mass-weighted component is an accepted structure. [log:certify.components.pyrolysis] [log:ops_notes_qowv.totals_row_55] [log:_derived_values]",
     "Charm Contents role carried by Ops Notes ledger; FC-C2"),
item("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Pass",
     "Certify carbon emission factor = 0.12820663526489975 tCO2e/t. Ops Notes QOWV!H55 (live formula '=IFERROR(SUMPRODUCT(D11:D53,H11:H53)/SUMIF(H11:H53,\"<>\",D11:D53),\"\")') returns 0.1282066353 - matching to the full precision Certify carries. None of this batch's totes are dated Jul-Dec 2026 production, so the newer '6-Mo CI (Jul-Dec 2026)' blended rate (0.120947) correctly does not apply to any tote here, consistent with the corrected Charm H1/H2 2026 CI policy (keyed to production month, not injection date). [log:certify.components.pyrolysis] [log:ops_notes_qowv.header] [log:ops_notes_qowv.totals_row_55]",
     "Production Period Summaries; FC-C10"),
item("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Pass",
     "'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' carries 34 sources, and 'INJ-08-2026-W4 Ops Notes.xlsx' is among them - confirmed by expanding the Ops Notes source row's linked-datapoint list, which explicitly includes this CI datapoint. This is the required evidence standard (Max-stated 2026-06-30: Ops Notes weighted-average, not a PP Summary). The other 33 sources are legacy per-PP backing documents (PP Summaries, biomass throughput, waste-disposal calc sheets, route maps, CAR certificates) carried over from the underlying production periods; their presence is extra, not a substitute for the Ops Notes link that is actually required. [log:certify.components.pyrolysis] [log:certify.attachment_map]",
     "Certify Sources tab; CI evidence standard (Ops Notes weighted average)"),
item("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", "Pass",
     "'QOWV Pyrolysis Mass [Certify input]' = 40,430.8kg. Ops Notes Total Oil Produced at QOWV!D55 is 40,430.80kg - the sum of the per-tote gross-minus-tare column across all 42 rows. Exact match on the correct basis (net oil produced, what pyrolysis actually made), not the net-injected figure of 36,568.50kg. [log:certify.components.pyrolysis] [log:ops_notes_qowv.totals_row_55]",
     "Ops Notes QOWV!D55"),
item("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", "Pass",
     "Mass 40,430.8kg with uncertainty +/-47.63kg, against the Ops Notes total at QOWV!J55 of 47.62716kg - present and correct. This matters because the pyrolysis term (5.183t) is a dominant fraction of net removal (5.139t), so it does not qualify for any uncertainty-omission carve-out; a missing figure here would have been a Fail. [log:certify.components.pyrolysis] [log:ops_notes_qowv.totals_row_55]",
     "Bio-oil Geological Storage v1.2 S6.5.1; FC-C12"),
item("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
     "No Charm Contents sheet exists as an artifact for 2026 weekly time-block batches - confirmed absent from both the Drive batch folder (Completed QA Checklists, Scale Tickets, Testing, Ops Notes only) and Certify's full 38-source enumeration. Per established precedent (validated on every 2026 weekly Charm batch to date), this function is carried by the Ops Notes ledger itself, which is attached and linked specifically to the 'QOWV Pyrolysis Mass [Certify input]' datapoint. [log:batch_folder_inventory] [log:certify.attachment_map] [log:certify.certify_sources_tab_total]",
     "Certify Sources tab; Document Location Rule"),

# ---------------------------------------------------------------- SECTION 8
section("Section 8 - Other")
item("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total >= the transport-process sum?", "Pass",
     "'BCU - Transport Process' applies a constant reduction of 7,125kgCO2e = 7.125tCO2e, evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf' linked to the datapoint. The removal carries two diesel transport-process emissions - CO to LA (6.975t) and CO->KS->LA (0.150t) - summing to 7.125t exactly. The BCU equals the sum of both lanes' process emissions precisely (7.125 = 6.975 + 0.150), so the offset is complete across both lanes, not just the larger one. [log:certify.components.bcu_transport_process] [log:certify.components.transport_process_co_to_la] [log:certify.components.transport_process_co_to_ks_to_la]",
     "Charm methodology - all diesel transport-process emissions must be BCU-offset")

# ---------------------------------------------------------------- SECTION 9
section("Section 9 - Aqueous Buffering (LCS)")
item("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist (correct mass, correct EF, evidenced)?", "N/A",
     "No LCS use is reported for this batch. The QOWV tab header lists only Sparging Mass Loss (0.0129) and a target pH range (2.0-4.0) as process constants; no LCS / Liquid Calcium Sulfate / buffer column appears anywhere in the tab's header row or per-tote columns. [log:ops_notes_qowv.lcs_search]",
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
    "Kansas-leg route-map evidence is a systemic gap, not a one-off. This is the second consecutive QOWV batch with a genuine two-lane transport split (INJ-08-2026-W3-QOWV was the first). Both times, the Ops Notes sheet correctly documents and instructs attaching two named Kansas-specific route maps ('Charm CO to Charm KS.png', 'Charm KS to Charm LA.png'), and both times those two files do not appear among the removal's Certify sources. Worth fixing at the template/process level so it stops recurring on the next Kansas-routed batch.",
    "'Charm Inv Bulk Upload March.csv' is attached to the Embodied Distance datapoint on a batch whose totes span November 2025 through PP#8/PP#7 - none dated March specifically as the controlling record. This same filename was flagged and later detached as weak evidence on a prior WODO batch (INJ-07-2026-W2-WODO, 2026-08-06). Worth checking whether it is doing any real evidentiary work here or is a stale carry-over.",
    "The Injection Sequestration component's Carbon Content datapoint carries only 2 sources despite the certificate covering two oil types across two pages - the linking is clean (certificate + Ops Notes, both pointed at the datapoint specifically), no issue found, noted only because the combined AECN+QOWV PDF naming convention makes this worth a second look on future weeks.",
    "Scale Tickets subfolder holds only AECN Truck and SHPX215076 (a railcar) contents - no QOWV-specific weighing records. Not held against the batch: the Ops Notes IBC ledger's own header states 'tote tag mass is authoritative', consistent with every other QOWV batch reviewed this year.",
    "Certify Sources tab reads 38 total sources today (heading 'Sources (38)', confirmed by enumerating all 38 rowheader filenames). A prior session's notes on this same batch recorded 39. Re-flagging in case a source was genuinely removed between sessions rather than simply miscounted - does not change any finding either way, since the Kansas-leg route maps are absent from the list at both counts.",
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
    "Net CO2e Removed = 5.139 tCO2e = Sequestrations 10.862 + BCU 7.125 - Activities 12.801 - Uncertainty Discount 0.047. All five Ops Notes totals reconcile to a zero delta across the 42-tote ledger; the Aqueous measured-loss method is applied correctly with no Standard Loss anywhere; uncertainty is 1.13398 kg per tote across 42 totes, correct on all components that need it including the dominant pyrolysis mass; all Shipment Tracker allocation cells (direct and Kansas legs) are live formulas that independently reproduce the reported 2,554.3 mi aggregate; both correct emission factors (Flatbed Process, Non-Tanker Embodied) are genuinely applied, confirmed against the live Standard EFs sheet; the BCU offsets both diesel transport-process lanes combined exactly; all seven Production Periods are captured in one reconciling aggregated component with the CI properly evidenced via the batch Ops Notes; Section 9 LCS correctly N/A. "
    "ONE FAIL: item 5.2 for the Kansas lane - the 1,221 mi via-Kansas Process distance is the correct value (ties exactly to the Shipment Tracker's 537+684 mi two-leg sum) but its only attached Certify evidence is the DIRECT route's map, not the Kansas-specific route maps the Shipment Tracker's own sheet note names and instructs be attached. Those two named files do not exist anywhere among the removal's 38 sources. "
    "TWO FLAGS: item 6.1, the Transport Embodied emission factor genuinely applies the correct Non-Tanker value but its datapoint is labelled 'Tanker Truck' - the same recurring mislabeling pattern across every QOWV batch this year. Item 6.3, the aggregate Embodied distance's Google-Map evidence covers only the direct-lane 94 percent of the mileage, missing the same Kansas-leg maps as item 5.2 - not blocking, since the Shipment Tracker's own formulas independently reconstruct the number."
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

out = HERE / "Charm_Aqueous_QOWV_QA_Checklist_INJ-08-2026-W4.xlsx"
wb.save(out)
print("saved", out)
print("counts", counts, "total", total)
