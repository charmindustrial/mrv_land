import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HDR   = PatternFill("solid", fgColor="D6E4F0")
FAIL  = PatternFill("solid", fgColor="FFC7CE")
FLAG  = PatternFill("solid", fgColor="FFF2CC")
FLAGF = Font(color="996600", size=10)
NAF   = Font(color="808080", italic=True, size=10)
BODY  = Font(size=10)
BOLD  = Font(bold=True, size=10)
TITLE = Font(bold=True, size=13)
thin  = Side(style="thin", color="BFBFBF")
BORD  = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook(); ws = wb.active; ws.title = "QA Checklist"

meta = [
 ("Charm WODO Injection Batch QA Checklist", None),
 ("Batch ID", "INJ-07-2026-W1 (Charm WODO portion)"),
 ("Reporting Period", "July 1 - July 31 2026 RP; batch week 2026-06-27 to 2026-07-04 (Certify removal window 01-04 Jul 2026)"),
 ("Reviewer", "Claude (QA agent) - for Max Lavine review"),
 ("Date", "2026-08-06"),
 ("Injection Site", "Basco 6 (Louisiana)"),
 ("Oil Type", "WODO (Charm-produced, Fort Lupton CO) - 17 IBC totes, shipping order COLA19"),
 ("Production Periods", "Jan 2026 (6 totes), Feb 2026 (2), Mar 2026 (2), Apr 2026 (3), May 2026 (4)"),
 ("Certify Removal ID", "rmv_1KYWMYBJ51S0HH3N  |  Net 18.937 tCO2e  |  GHG statement ggs_1KZBX6AX41S029JS"),
]
r = 1
ws.cell(row=1, column=1, value=meta[0][0]).font = TITLE
r = 2
for k, v in meta[1:]:
    ws.cell(row=r, column=1, value=k).font = BOLD
    ws.cell(row=r, column=2, value=v).font = BODY
    r += 1

r += 1
for i, h in enumerate(["#", "Question", "Status", "Evidence / Finding", "Reference"], start=1):
    c = ws.cell(row=r, column=i, value=h); c.font = BOLD; c.fill = HDR; c.border = BORD
HEADER_ROW = r
r += 1

def section(title):
    global r
    for col in range(1, 6):
        c = ws.cell(row=r, column=col, value=title if col == 1 else None)
        c.fill = HDR; c.font = BOLD; c.border = BORD
    r += 1

def item(num, q, status, ev, ref):
    global r
    vals = [num, q, status, ev, ref]
    for col, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=col, value=v)
        c.border = BORD
        c.alignment = Alignment(vertical="top", wrap_text=(col in (2, 4)))
        c.font = BODY
        if status == "Fail":
            c.fill = FAIL
        elif status == "Flag":
            c.fill = FLAG; c.font = FLAGF
        elif status == "N/A":
            c.font = NAF
    r += 1

section("Section 1 - Batch Folder")
item("1.1","Is there testing in the testing folder for the batch?","Pass",
 "Testing/ holds WODO CoA '7-2026-W1 WODO.pdf' - SGS Certificate SR26-04242.001, Client ID '7-2026-W1 WODO', product 'Oil - WODO JAR #2', location FORT LUPTON CO, sampled 14-Jul-2026 10:10. Carbon 51.6 % (m/m) ASTM D5291 Method C; Hydrogen 7.3 %; Nitrogen <0.75 %; Kinematic Viscosity 40 C 129.1 cSt; Acid Number 78 mg KOH/g; Density 15 C 1.217 g/cm3 (above the 1.01 g/cm3 formation-fluid minimum). Signed Tiffany Scott, Lab Supervisor. [log:lab_results] [log:lab_results._primary_source_opened]","VR Appendix 1")
item("1.2","Are Ops Notes in the folder and fully completed?","Pass",
 "'INJ-07-2026-W1 Ops Notes' present (8 tabs). WODO tab fully populated: all 17 tote rows carry tag, gross mass, tote mass, net oil produced, measured empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty - no blanks, no formula errors. All five summary cells populated and formula-driven (B29, D29, F29, H29, I29, J29). [log:totes] [log:ops_notes]","VR Appendix 1")
item("1.3","Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?","Pass",
 "Allocation carried as the 'WODO Shipments & EE Allocation' tab inside the Ops Notes workbook (weekly-batch schema, same as INJ-06-2026-W1). Complete: batch summary row (17 totes, COLA19), one-way distance input B8 = 1201 mi, EE allocation table (COLA19: 17 on truck / 17 batch-relevant), batch mileage allocation block, and the full 17-tote roster with tag, fraction, production period, shipping order and batch. [log:shipment_tracker]","VR Appendix 1")

section("Section 2 - Ops Notes")
item("2.1","Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?","Pass",
 "Reported 18,926.00 kg (WODO!A33 = '=B29'; B29 = '=SUM(B11:B27)'). Independent sum of the 17 per-tote gross masses = 18,926.00 kg; delta 0.0000 kg. The SUM range B11:B27 covers all 17 tote rows with none omitted. [log:ops_notes] [log:totes] [log:ops_notes._primary_source_opened]","Ops Notes WODO tab, Section 1 IBC Ledger")
item("2.2","Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?","Pass",
 "Reported 17,946.80 kg (WODO!B33 = '=SUM(D11:D27)'). Each per-tote cell is a formula '=B-C' (gross minus 57.60 kg standard tote tare) - not hard-coded. Independent sum of (gross - 57.60) across all 17 totes = 17,946.80 kg; delta 0.0000 kg. [log:ops_notes] [log:totes] [log:_derived_values]","Ops Notes WODO tab, column D")
item("2.3","Is the 'Total Oil in Batch' value correctly computed (WODO: net-in-tote less tote loss per tote)?","Pass",
 "Reported 17,885.00 kg (WODO!D33 = '=SUM(F11:F27)'); each per-tote cell is a formula '=IF(E=\"\",\"\",B-E)' = gross minus the directly measured empty tote weight. Independent sum across all 17 totes = 17,885.00 kg; delta 0.0000 kg. A tote-loss deduction is applied: 17,946.80 - 17,885.00 = 61.80 kg over 17 totes. Measured actual weights are the operative basis (Max-stated 2026-08-06); the fixed 4.73 kg/tote figure in the 'WODO Tote Standard Loss - 2026 Dataset' sheet is not approved for use and is therefore correctly not applied here. [log:ops_notes] [log:totes] [log:wodo_standard_loss_dataset] [log:_derived_values]","Ops Notes WODO tab column F"),
item("2.4","Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?","Pass",
 "Reported 19.27766 kg (WODO!J29 = '=SUM(J11:J27)'); each per-tote cell is '=2.5*$L$4' where L4 = 0.453592 kg/lb, giving 1.13398 kg per tote. Expected 2.5 lb / 2.20462 x 17 totes = 19.27770 kg; delta 0.00004 kg (the sheet applies the kg/lb constant rather than dividing by lb/kg - identical to six decimal places). Charm per-tote precision correctly applied; this is not the AECN 72.57 kg per-truck spec. [log:ops_notes] [log:totes] [log:_derived_values]","Isometric Standard S3.7.3 Option B (variance propagation)")

section("Section 3 - Bio-Oil Shipment Tracker (WODO Shipments & EE Allocation tab)")
item("3.1","Are totes for the RP correctly identified?","Pass",
 "17 totes listed under shipping order COLA19, and all 17 appear in the Ops Notes IBC ledger. Tag set is identical between the two tabs (verified programmatically, not sampled): 300063, 300077, 300065, 300064, 300099, 300095, 300054, 301020, 301012, 301001, 301016, 301055, 301149, 301130, 301131, 301174, 301187. No tote present in one tab and absent from the other. [log:shipment_tracker] [log:totes]","Shipment tracker tab, rows 21-37")
item("3.2","Do all totes identified for RP match the Ops Notes for the applicable batch?","Pass",
 "17/17 match with zero mismatches on every attribute the tracker carries: tag, fraction (all WODO), production period, shipping order (all COLA19) and batch (all INJ-07-2026-W1). Production-period counts agree exactly between tabs - Jan 2026 x6, Feb 2026 x2, Mar 2026 x2, Apr 2026 x3, May 2026 x4. Gross mass is not a column on the tracker tab; it is held in the IBC ledger of the same workbook, which is the cell Certify draws from, so no divergent second copy exists. [log:shipment_tracker] [log:totes]","Shipment tracker roster vs Ops Notes IBC ledger")
item("3.3","Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?","Pass",
 "Every computed cell read from the workbook is a live formula, none is a typed constant: Batch Share of Truck E12 = '=D12/C12'; Mileage one-way F12 = '=$B$8'; Allocated Miles G12 = '=E12*F12'; totals C13 = '=SUM(C12)', D13 = '=SUM(D12)', G13 = '=SUM(G12)'; Batch Mileage Allocation C17 = '=G13'; tote count D17 = '=D13'. A verifier can reconstruct the allocation from the tote-count and mileage inputs. [log:shipment_tracker_cells_are_formulas] [log:shipment_tracker._primary_source_opened]","Auditability - Transportation Emissions Accounting v1.1")
item("3.4","Are computed outputs computed correctly per the allocation formulas?","Pass",
 "All three reproduce the specification independently. Batch Share of Truck = 17 batch-relevant / 17 on truck = 100.00 %. RP Allocated Miles = 1,201 mi one-way x 100.00 % = 1,201.00 mi. Batch Mileage Allocation = 1,201.00 mi for 17 totes. The mileage input cell B8 is labelled 'Charm CO -> Basco LA distance (one-way mi)' and is used one-way with no round-trip doubling, which is correct for this batch. The 100 % share is not an override: all 17 totes on COLA19 belong to this batch, so the allocated distance legitimately equals the full one-way distance. [log:shipment_tracker] [log:shipment_tracker_cells_are_formulas] [log:_derived_values]","Shipment tracker EE Allocation table")
item("3.5","Do the totes assigned to each batch match the Ops Notes on (a) tag number, (b) fraction, (c) gross mass, (d) production period?","Pass",
 "(a) Tag - 17/17 identical. (b) Fraction - 17/17 WODO on both tabs. (c) Gross mass - single-sourced: the tracker tab carries no mass column (headers are Metal Tag, Fraction, Production Period, Shipping Order, Batch), so mass exists once, in IBC ledger column B, which is the cell feeding Certify's mass of load; sum verified at 18,926.00 kg in item 2.1. (d) Production period - 17/17 identical, per-tote and in aggregate. Zero mismatches on any attribute. [log:shipment_tracker] [log:totes]","Per-attribute roster comparison")

section("Section 4 - Certify: Injection Sequestration (33.841 tCO2e)")
item("4.1","Does the C content in the testing match the C content in the Sequestration component?","Pass",
 "Lab SR26-04242.001 reports Carbon 51.6 % (m/m). Certify 'Carbon Content of Bio-oil Injected (per injection)' reads 51.6 % in the component INPUTS (read from the modal). Delta 0.0 % absolute. Single WODO fraction this week, so no weighted-average step applies. [log:lab_results] [log:lab_results._primary_source_opened] [log:certify]","Certify Injection sequestration cmp_1KYWMYBJ51S0DPFZ")
item("4.2","Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?","Pass",
 "Both evidence types are attached to the Carbon Content datapoint itself, not merely at removal level - the modal shows '2 sources' against Carbon content of product, and the Sources tab confirms them as '7-2026-W1 WODO.pdf' (the SGS CoA) and 'INJ-07-2026-W1 Ops Notes.xlsx'. [log:certify.attachment_map] [log:certify.certify_sources_enumeration]","Certify Sources tab (6 sources enumerated)")
item("4.3","Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?","Pass",
 "Modal INPUTS read: Mass of product = 'Mass of Injectant (per injection)' 17,885 +/-19.28 kg. Ops Notes uncertainty cell J29 = 19.27766 kg, which Certify displays to two decimals as 19.28. Match. Entered as an absolute mass, not a percentage. [log:certify] [log:ops_notes]","Certify Injection sequestration INPUTS")
item("4.4","Does the C content have the appropriately computed 0.4% relative uncertainty?","Pass",
 "Modal INPUTS read: Carbon content 51.6 +/-0.2064 %. Expected 0.004 x 51.6 = 0.2064 % absolute; delta 0.0000. Independently corroborated by Ops Notes Summary!F18 = '=D18*G18' = 0.516 x 0.004 = 0.002064. Correctly entered as an absolute percentage-point value, not as '0.4'. [log:certify] [log:ops_notes] [log:_derived_values]","Isometric Standard S3.7.3; MRV Uncertainty cheat sheet")

section("Section 5 - Certify: Transport Process Emissions (3.146 tCO2e)")
item("5.1","Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?","Pass",
 "Modal INPUTS read 0.1384 kgCO2e/(t*mi). Live Standard Emission Factors sheet, tab 2026 (gid 684080705, tab identity confirmed by page title '2026'), row 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck' = 0.0001384 MT CO2e/t-mi, cited GLEC V3.2 2025, marked 'Updated'. Exact match in native units. Correctly the flatbed factor, not the tanker factor on the adjacent row (0.0001143). Recomputed from full precision: 0.0001384 x 1,201 mi x 18.926 t = 3.1458 t vs Certify 3.146 t. [log:standard_efs] [log:standard_efs._primary_source_opened] [log:recomputation] [log:_derived_values]","Standard EFs sheet, 2026 tab; GLEC V3.2 2025")
item("5.2","Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?","Pass",
 "'CO to Basco Routing Map.png' (1842x863, read from the image pixels) shows three route options: via US-287 S and US-287 S, 17 hr 22 min, 1,132 miles (marked 'Fastest route now'); via US-287 S, US-287 S and I-20 E, 17 hr 32 min, 1,129 miles; and via I-70 E, 17 hr 36 min, 1,201 miles. Certify uses 1,201 mi = the longest of the three, correctly not the fastest. Destination reads '4675 LA-115, St Landry, LA 71367'. The origin field reads 'Your location' with the pin in the Denver-Fort Lupton corridor; origin confirmed as Fort Lupton (Max-stated 2026-08-06), which is also the sample location on the batch CoA. [log:google_maps_options] [log:google_maps_options_artifact] [log:certify]","Certify Transport Process INPUTS; CO to Basco Routing Map.png"),
item("5.3","Does the Mass of Load match the Total Mass Transported value in Ops Notes?","Flag",
 "Value correct; one word left in the datapoint title. Modal INPUTS read 18,926 kg = Ops Notes Total Mass Transported (WODO!A33) exactly - the gross basis including tote tares, correctly not Total Oil Produced (17,946.80) and not Total Oil in Batch (17,885.00). Title history this session: read 'QOWV (Aqueous Oil) - Mass (Net) (CO to KS)' at 18:22Z, 'WODO - Mass (Net) (CO to KS)' at 19:29Z, and 'WODO - Mass (Net) (CO to LA)' at 19:34Z. Oil type and destination are now both right. Remaining: '(Net)' describes a gross figure - 18,926 kg includes the 17 tote tares, and neither net value equals it. Location: the 'Mass of load' input on cmp_1KYWMYBJ51S01BBM; the datapoint feeds no other component. Value needs no change. [log:certify] [log:certify.recheck3_2026_08_06] [log:ops_notes]","Certify Transport Process cmp_1KYWMYBJ51S01BBM, Mass of load input"),
item("5.4","Is the Mass of Load evidenced by a copy of the batch Ops Notes?","Pass",
 "'INJ-07-2026-W1 Ops Notes.xlsx' is linked to this mass datapoint (modal shows '1 source'; Sources tab lists the Ops Notes against it as one of its five datapoints). [log:certify.attachment_map]","Certify Sources tab")
item("5.5","Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?","Pass",
 "Modal INPUTS read 18,926 +/-19.28 kg = Ops Notes J29 19.27766 kg. Identical to the Mass of Product uncertainty on the Sequestration component, which is correct - the same 17 totes, weighed on the same scale. [log:certify] [log:ops_notes]","Certify Transport Process INPUTS")

section("Section 6 - Certify: Transport Embodied Emissions (0.232 tCO2e)")
item("6.1","Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?","Pass",
 "Modal INPUTS read 0.19279 kgCO2e/mi. Live Standard EFs sheet, 2026 tab, row 'Vehicle Embodied Emissions --Non-Tanker Truck' = 0.0001927908256 MT CO2e/mi, cited GLEC V3.2 2025, marked 'Updated'. Match. Correctly the non-tanker variant, not the tanker row (0.00023756059), and correctly per-mile rather than per-ton-mile, which is the required embodied convention. Recomputed: 0.0001927908256 x 1,201 mi = 0.2315 t vs Certify 0.232 t. [log:standard_efs] [log:standard_efs._primary_source_opened] [log:recomputation] [log:_derived_values]","Standard EFs sheet, 2026 tab; GLEC V3.2 2025")
item("6.2","Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?","Pass",
 "Certify 'Aggregate Distance Transported CO to LA - WODO' = 1,201 mi. Shipment tracker Batch Mileage Allocation C17 = 1,201.00 mi. Match to 0.0 mi. The allocated figure equals the full one-way distance because the batch share of truck COLA19 is 17/17 = 100 %, so no reduction is due - this is the allocated value, not the unallocated distance substituted for it. [log:shipment_tracker] [log:certify] [log:_derived_values]","Certify Transport Embodied cmp_1KYWMYBJ51S0N079")
item("6.3","Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?","Pass",
 "RESOLVED 2026-08-06 (re-read live at 19:20Z). The 'Aggregate Distance Transported CO to LA - WODO' datapoint now carries two sources: 'CO to Basco Routing Map.png' and 'INJ-07-2026-W1 Ops Notes.xlsx'. Certify's Sources tab went from 6 rows to 7, the added row being the Ops Notes against this datapoint, and the datapoint row now reads 'CO to Basco Routing Map.png + 1 more'. The attached Ops Notes embeds the 'WODO Shipments & EE Allocation' tab carrying the 17/17 allocation that yields 1,201.00 mi, so the allocation basis is now evidenced at the datapoint alongside the route map. No separate Charm Contents sheet exists under the weekly-batch schema; the per-period breakdown it carried lives in the attached Ops Notes. Net unchanged at 18.937 tCO2e. [log:certify.attachment_map] [log:certify.recheck_2026_08_06] [log:charm_contents_search_artifact]","Certify Sources tab; VR Appendix 1"),

section("Section 7 - Certify: Production Emissions (Pyrolysis - Charm WODO PP, 14.532 tCO2e)")
item("7.1","Are there Production Emissions components for ALL Production Periods in the batch?","Pass",
 "All five production periods feeding this batch are captured: Jan 2026 (6 totes), Feb 2026 (2), Mar 2026 (2), Apr 2026 (3), May 2026 (4). They are carried in one component, 'Pyrolysis - Charm WODO PP Emissions', using a production-mass-weighted blended CI of 0.809711 tCO2e/t. That aggregation reconciles exactly to the per-period sum: Jan 5,918.54 + Feb 1,750.62 + Mar 1,650.68 + Apr 2,580.77 + May 2,631.12 = 14,531.73 kg = 14.532 t, the component value. No period's emissions are omitted. Aggregating periods into one mass-weighted component is not a deviation - no primary source requires one Certify component per production period. [log:production_periods] [log:certify] [log:_derived_values]","Certify Components tab; Bio-oil Geological Storage v1.2")
item("7.2","Does the CI match the Ops Notes weighted-average CI across all totes in the injection?","Pass",
 "Modal INPUTS read Carbon emission factor 0.809711 tCO2e/t. Ops Notes weighted average WODO!H29 = '=IFERROR(I29/D29,\"\")' = 14,531.73 / 17,946.80 = 0.809711 - agreement to all six decimals, and correctly production-mass-weighted (over net oil produced) rather than a simple average. Each period's own CI is applied to its own totes in column H, verified per tote: Jan 0.931994 x6, Feb 0.849896 x2, Mar 0.790065 x2, Apr 0.784500 x3, May 0.632846 x4. No cross-wiring of one period's CI onto another period's totes. [log:ops_notes] [log:production_periods] [log:certify] [log:_derived_values]","Certify Pyrolysis cmp_1KYWMYBJ51S03KNX")
item("7.3","Is the CI evidenced (Ops Notes weighted-average across totes)?","Pass",
 "'INJ-07-2026-W1 Ops Notes.xlsx' is linked to the 'WODO Tote - Carbon Intensity' datapoint (modal shows '1 source'; Sources tab lists this datapoint against the Ops Notes). The attached workbook carries both the per-tote CIs and the H29 weighted-average cell that produces 0.809711, so the figure is reconstructible from the evidence. [log:certify.attachment_map]","Certify Sources tab")
item("7.4","Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?","Pass",
 "Modal INPUTS read Mass 17,946.8 kg = Ops Notes Total Oil Produced (WODO!D29/B33), the sum of net oil produced across all 17 totes, verified independently in item 2.2. Correct production basis - net oil produced (pre-loss), not the post-loss injected mass of 17,885.00. Because the component aggregates all five periods, the batch-total mass is the right pairing for the blended CI; per-period masses sum to it: 6,350.40 + 2,059.80 + 2,089.30 + 3,289.70 + 4,157.60 = 17,946.80 kg. [log:totes] [log:production_periods] [log:_derived_values]","Certify Pyrolysis INPUTS")
item("7.5","Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?","Pass",
 "Modal INPUTS read Mass 17,946.8 +/-19.277659999999997 kg, matching Ops Notes J29 = 19.27766 kg = 1.13398 kg x 17 totes. The uncertainty is present on the dominant emission input - pyrolysis is 14.532 t, 76.73 % of activities and 77 % of net - as Bio-oil Geological Storage v1.2 6.5.1 requires for measured input variables. Per-period slices sum to the batch figure: 6.80389 + 2.26796 + 2.26796 + 3.40195 + 4.53593 = 19.27769 kg. [log:certify] [log:production_periods] [log:_derived_values]","Bio-oil Geological Storage v1.2 6.5.1")
item("7.6","Is the mass evidenced with a copy of the Charm Contents sheet for the batch?","Pass",
 "The mass basis is evidenced, by the Ops Notes rather than by a document named Charm Contents. 'INJ-07-2026-W1 Ops Notes.xlsx' is linked to 'WODO Tote - Mass (Gross-Tote) for pyrolysis' (modal shows '1 source'). No Charm Contents sheet exists for this batch: a Drive title search for 'Charm Contents' returns only legacy per-batch sheets (5-10, 3-55, 3-56, 5-08, 5-07), the newest last modified 2026-05-12, none for any INJ-07-2026 week. Under the weekly-batch schema the per-period mass breakdown that Charm Contents used to carry now sits in the Ops Notes IBC ledger (column G production period against column D net oil produced), so the attached workbook does evidence batch membership and the per-period split. Same basis accepted on INJ-06-2026-W1. [log:certify.attachment_map] [log:charm_contents_search] [log:charm_contents_search_artifact]","Certify Sources tab; VR Appendix 1")

section("Section 8 - Other (BCUs)")
item("8.1","Are all diesel transport-process emissions offset by BCUs, and does the BCU total >= the transport-process sum?","Pass",
 "The batch has exactly one diesel transport-process emission - the CO-to-LA flatbed transport process, 3.146 tCO2e - and it is fully offset. A 'BCU - Transport Process' component is present under Adjustments at 3.146 tCO2e (modal INPUTS: Constant CO2 reduction 3,146 kgCO2e), evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf'. BCU 3.146 t >= transport process 3.146 t, offset exactly with no shortfall. Embodied emissions are correctly not offset. [log:certify]","Transportation Emissions Accounting v1.1; Certify Reductions")

section("Section 9 - Aqueous Buffering (LCS)")
item("9.1","If LCS use is reported in Ops Notes, does a matching Certify component exist?","N/A",
 "WODO batch - LCS buffering is Aqueous-only. No LCS reported: the WODO tab has no LCS, Liquid Calcium Sulfate or buffer column anywhere (columns A-J are Tag, Gross Mass, Tote Mass, Net Oil Produced, Empty Tote Weight, Net Oil Injected, Production Period, Carbon Intensity, Production Emissions, Scale Uncertainty), and no LCS component exists among the removal's 5 components. [log:ops_notes] [log:certify] [log:charm_contents_search_artifact]","Aqueous-only item")

r += 1
for col in range(1, 6):
    c = ws.cell(row=r, column=col, value="Sidebar Observations (no Pass/Fail - flagged for attention)" if col == 1 else None)
    c.fill = HDR; c.font = BOLD; c.border = BORD
r += 1

side = [
 "WODO CoA flags: SGS marks both Carbon (51.6 %) and Hydrogen (7.3 %) with '#' = 'Result is outside of test method limits and/or analytical range used in method precision study'. ASTM D5291 is a petroleum-matrix method, so bio-oil routinely falls outside its precision study; carbon at 51.6 % is in family with the 51.8 % on INJ-06-2026-W1. Noting it because the marker appears on the face of the evidence a verifier will read.",
 "CoA sampling timing and point: sampled 14-Jul-2026, ten days after the batch week closed on 2026-07-04, at Fort Lupton CO as 'Oil - WODO JAR #2'. The sample characterises the produced oil on the production side, not a draw at injection.",
 "Ops Notes Summary tab, Charm WODO row: 979.20 kg sits under a column headed 'Sparging Loss (kg)' (Summary!E10 = '=WODO!C33' = A33-B33 = 18,926.00 - 17,946.80). That figure is the standard tote tare, 17 x 57.60 kg - it is neither sparging (WODO receives none) nor an oil loss. The row consequently does not chain: 17,946.80 - 979.20 = 16,967.60, not the 17,885.00 shown as MOBI, and the real oil loss of 61.80 kg appears in no Summary column. No Certify value derives from this row - all five components trace to the WODO tab directly - so this is presentation only, but the AECN Rail row on the same table does chain correctly, which makes the WODO row look like an error to a reader.",
 "Uncertainty basis, noted for the record: each tote is weighed twice here - gross at load and empty after unload - yet uncertainty is counted as one weighing event per tote (1.13398 kg). Propagating two independent weighings per tote gives sqrt(1.13398^2 + 1.13398^2) = 1.6036 kg, and under Charm's linear-summation convention the batch figure would be 17 x 1.6036 = 27.26 kg rather than the 19.28 kg reported. The reported value does match the documented 1.134 kg x N specification, which is why items 2.4, 4.3, 5.5 and 7.5 pass; raising it here because the measured-empty-weight method introduces a second weighing that the one-event-per-tote spec predates.",
 "BCU vintage: the offset is evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf', a 18-Dec-2025 retirement applied against a July 2026 removal - a drawdown from the standing EAC inventory rather than a period-matched retirement. Eligibility and headroom sit with the EAC inventory tracker, not this batch.",
 "Removal window: Certify scopes the removal to 01-04 Jul 2026 while the Ops Notes batch week is 2026-06-27 to 2026-07-04, i.e. the removal covers the portion of the week falling inside the July RP. Flagging so the 27-30 Jun portion is confirmed as reported in the June RP and not dropped between periods.",
 "Scale Tickets subfolder holds only AECN railcar folders (GRPX5188, GPRX5098, GPRX5107, GPRX5236). Correct and expected - WODO arrives in totes and is tote-weighed, so no WODO scale tickets are due; the tote weights are the Ops Notes IBC ledger.",
 "Filtration deduction scope: the WODO stream carries no filtration loss (Summary!F10 = 0.00), while AECN Rail carries 602.33 kg. The 0.195 % Filtration Solids Content constant is implemented only on the AECN Rail tab (N7/O7) and its linked dataset is built entirely from AECN certificates - the source sheet states its window as 'ASTM D7579 (BioEnergie AE Cote-Nord)' across 152 loads / 78 unique CofAs, all RS1/RS2/RS3 AECN sample IDs. So the constant is AECN-derived and AECN-scoped by construction. Raising it only because the RP folder also holds 'CAR-474 Solids Loading in Kerry, AECN and WODO Oils (2026-05-28)', which covers WODO solids; whether WODO warrants its own deduction is an RP-level scope question, not a defect in this batch.",
 "Note for the RP-level record: Garrett's 'July 1 - July 31 RP - Submission Checklist' lists the W1 scale-ticket railcar as 'GRPX5188' and flags it as a likely typo for GPRX5188. The Ops Notes AECN Rail tab carries the same 'GRPX5188' spelling. Out of scope for this WODO checklist; belongs to the AECN W1 batch.",
]
for s in side:
    ws.cell(row=r, column=1, value="•").font = BODY
    c = ws.cell(row=r, column=4, value=s); c.font = BODY
    c.alignment = Alignment(vertical="top", wrap_text=True)
    r += 1

r += 1
counts = {}
for rr in range(HEADER_ROW + 1, r):
    v = ws.cell(row=rr, column=3).value
    if v in ("Pass", "Fail", "Flag", "N/A"):
        counts[v] = counts.get(v, 0) + 1
total = sum(counts.values())
summary = ("STATUS SUMMARY: %d Pass · %d Flag · %d Fail · %d N/A  (%d items)  |  "
           "Net 18.937 tCO2e verified against all sources. Zero Fails. 6.3 cleared on re-read 2026-08-06: the Ops Notes is now attached to the Aggregate Distance datapoint (Certify sources 6 -> 7), net unchanged. "
           "One Flag remains (5.3): the mass-of-load datapoint on cmp_1KYWMYBJ51S01BBM now reads 'WODO - Mass (Net) (CO to LA)' as of 19:34Z - oil type and destination both corrected; only '(Net)' is left, describing a gross 18,926 kg figure. Value correct. "
           "Max rulings 2026-08-06: measured tote weights are the operative loss basis (2.3 Pass, fixed 4.73 kg/tote standard loss not approved); routing-map origin confirmed Fort Lupton (5.2 Pass)." % (
    counts.get("Pass", 0), counts.get("Flag", 0), counts.get("Fail", 0), counts.get("N/A", 0), total))
c = ws.cell(row=r, column=1, value=summary); c.font = BOLD
c.alignment = Alignment(vertical="top", wrap_text=True)

ws.column_dimensions["A"].width = 7
ws.column_dimensions["B"].width = 52
ws.column_dimensions["C"].width = 9
ws.column_dimensions["D"].width = 98
ws.column_dimensions["E"].width = 30
ws.freeze_panes = ws.cell(row=HEADER_ROW + 1, column=1)

out = "Charm_WODO_QA_Checklist_INJ-07-2026-W1.xlsx"
wb.save(out)
print("saved", out)
print("counts", counts, "total", total)
