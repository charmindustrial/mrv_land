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
 ("Charm Aqueous (QOWV) Injection Batch QA Checklist", None),
 ("Batch ID", "INJ-08-2026-W3"),
 ("Reporting Period", "Certify removal window 09 Aug 2026 to 15 Aug 2026; Ops Notes injection week 2026-08-08 to 2026-08-15"),
 ("Reviewer", "Claude (QA agent) - for Max Lavine review"),
 ("Date", "2026-08-31"),
 ("Injection Site", "Basco 6 (Louisiana)"),
 ("Oil Type", "Aqueous / QOWV (Charm-produced) - 37 IBC totes. 33 totes shipped Colorado direct to Basco (1,201 mi one-way). 4 totes (tags 118811, 118837, 118872, 118886, all PP#7) shipped Colorado -> Charm Kansas (2025-10-21, stored) -> Basco, a 1,221 mi routed path, per VVB Guidance August 1-31."),
 ("Production Periods", "PP#8, November 2025, February 2026, March 2026, April 2026 (33 direct totes) + PP#7 (4 Kansas-routed totes) - all captured in one aggregated Pyrolysis component, weighted CI 0.12697098348438993 tCO2e/t"),
 ("Certify Removal ID", "rmv_1M0ZD6K9J1S0WPD4  |  Net 4.669 tCO2e  |  6 components"),
]
ws.cell(row=1, column=1, value=meta[0][0]).font = TITLE
r = 2
for k, v in meta[1:]:
    ws.cell(row=r, column=1, value=k).font = BOLD
    c = ws.cell(row=r, column=2, value=v); c.font = BODY
    c.alignment = Alignment(vertical="top", wrap_text=True)
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
    for col, v in enumerate([num, q, status, ev, ref], start=1):
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

# ---------------------------------------------------------------- SECTION 1
section("Section 1 - Batch Folder")
item("1.1", "Is there testing in the testing folder for the batch?", "Pass",
 "Testing subfolder contains 'CHARM INDUSTRIAL - 08-2026-W3 AECN + QOWV + Kerry (SR26-05021.001-003).pdf' (SGS order 5482329). Read all 3 pages as PDF. Page 2 is Certificate of Analysis SR26-05021.002, client id '08-2026-W3 QOWV', sampled 19-Aug-2026, location Basco Louisiana: Carbon 8.2% (m/m) ASTM D5291 Method C, Hydrogen 10.1%, Nitrogen <0.75%, kinematic viscosity 0.9260 cSt, acid number 31 mg KOH/g, density 1.044 g/cm3. This is present in both the Drive Testing folder and attached in Certify to the Carbon Content datapoint. [log:testing]",
 "VR Appendix 1; Document Location Rule")
item("1.2", "Are Ops Notes in the folder and fully completed?", "Pass",
 "'INJ-08-2026-W3 Ops Notes' (5 tabs: Summary, AECN Rail, Kerry, QOWV, QOWV Shipments & EE Allocation) is in the batch folder. The QOWV tab is fully populated for all 37 tote rows (33 direct-lane rows 11-43, 4 Kansas-lane rows 45-48, visually confirmed row-by-row): tag, gross mass, tote mass, net oil produced, empty tote weight, net oil injected, production period, carbon intensity, production emissions, scale uncertainty - no blanks, no formula errors. All five totals-row cells (row 50) and both lane-subtotal cells (rows 51-52) are live SUM/SUMPRODUCT formulas, not typed constants. [log:ops_notes] [log:totes]",
 "VR Appendix 1")
item("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Pass",
 "Carried as the 'QOWV Shipments & EE Allocation' tab inside the batch Ops Notes workbook (2026 weekly-batch convention; no standalone Bio-Oil Shipment Tracker file exists). The tab is complete: batch summary row (37 totes, week 2026-08-08 to 2026-08-15, direct one-way distance input 1,201 mi), EE Allocation Table A (5 trucks, 33 direct totes, subtotal 1,693.3 allocated mi), EE Allocation Table B (2 legs via Kansas, 4 totes, subtotal 582.4 allocated mi), and a Grand Total row (2,275.7 mi). [log:shipment_tracker]",
 "VR Appendix 1")

# ---------------------------------------------------------------- SECTION 2
section("Section 2 - Ops Notes")
item("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", "Pass",
 "Reported 38,152.00 kg at QOWV!B50 = '=SUM(B11:B48)', spanning both lanes' 37 tote rows (blank divider row 44 does not affect the sum). Independent sum of all 37 per-tote gross masses reproduces 38,152.00 kg; delta 0.00 kg. Lane subtotals also verified as live formulas: B51 '=SUM(B11:B43)' = 34,113.00 kg (direct 33 totes), B52 '=SUM(B45:B48)' = 4,039.00 kg (Kansas 4 totes); 34,113.00 + 4,039.00 = 38,152.00, ties exactly. [log:ops_notes.totals_row_50] [log:ops_notes.lane_subtotals]",
 "Ops Notes QOWV tab, Section 1 IBC Ledger")
item("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", "Pass",
 "Reported 36,020.80 kg at QOWV!D50 = '=SUM(D11:D48)'; per-tote formula confirmed at D11 = '=B11-C11'. Tare (column C) is a uniform 57.60 kg per tote - the IBC container's own empty weight, applied identically across both lanes. Independent sum of (gross - 57.60) across all 37 totes reproduces 36,020.80 kg; delta 0.00 kg. [log:ops_notes]",
 "Ops Notes QOWV tab, column C/D")
item("2.3", "Is the 'Total Oil in Batch' value correctly computed (Aqueous: measured pre-unload minus measured post-unload per tote, no Standard Loss)?", "Pass",
 "Reported 32,333.50 kg at QOWV!F50 = '=SUM(F11:F48)'; per-tote formula confirmed at F11 = '=IF(E11=\"\",\"\",B11-E11)', i.e. gross mass (pre-unload) minus the measured empty-tote weight after unloading (post-unload, varies 82.50-270.00 kg across totes - genuine measurement, not a fixed allowance). No 'Standard Loss' column exists anywhere on the QOWV tab; a full visual scan of all 37 rows across all columns found none. The Aqueous method is correctly applied with no Standard Loss deduction. [log:ops_notes] [log:totes]",
 "Ops Notes QOWV tab column F; FC-C1")
item("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
 "Reported 41.95726 kg at QOWV!J50 = '=SUM(J11:J48)'; each per-tote cell reads 1.13398 kg, uniform across all 37 totes. Expected 2.5 lb / 2.20462 x 37 totes = 41.95726 kg; exact match. Charm's per-tote precision (1.134 kg) is correctly applied, not AECN's 72.57 kg per-truck spec. [log:ops_notes.totals_row_50]",
 "Isometric Standard S3.7.3 Option B; FC-C8")

# ---------------------------------------------------------------- SECTION 3
section("Section 3 - Bio-Oil Shipment Tracker (QOWV Shipments & EE Allocation tab)")
item("3.1", "Are totes for the RP correctly identified?", "Pass",
 "37 totes identified for the batch: 33 on the direct Colorado-to-Basco lane (Table A, summed across 5 trucks: 1+6+18+7+1=33) and 4 on the Kansas-routed lane (Table B, tags 118811/118837/118872/118886 named explicitly in the table header). Both counts tie to the Ops Notes IBC ledger's 33+4=37 split exactly, and to the batch summary header (D6=37). [log:shipment_tracker] [log:totes]",
 "Shipment tracker Tables A and B")
item("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Pass",
 "Kansas lane: all 4 tags (118811, 118837, 118872, 118886) named in the Table B header match the Ops Notes yellow-highlighted 4-row block exactly, same PP#7, same lots (2590/2574/2536/2488). Direct lane: the tracker organizes Table A by truck/shipment (not by individual tote tag), consistent with the 2026 weekly-batch tracker design where gross mass and tag identity are single-sourced in the Ops Notes IBC ledger; the truck-level tote counts (1+6+18+7+1=33) reconcile exactly to the Ops Notes direct-lane count and to B51=34,113.00 kg. This per-truck (not per-tag) design for the shared-truck direct lane, and the fact that which of 2 trucks carried which Kansas-leg tote was not individually recorded, is explicitly documented and endorsed as immaterial by the VVB Guidance August 1-31: 'Which of the two trucks on the Colorado to Kansas shipment carried which tote was not recorded. This does not affect the result, because four totes out of 34 across two trucks allocates the same mileage as four out of 17 on one truck.' [log:vvb_guidance] [log:shipment_tracker] [log:totes]",
 "Roster vs Ops Notes IBC ledger; VVB Guidance Aug 1-31")
item("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
 "Every computed cell read from the workbook is a live formula, none a typed constant. Table A: E12 '=D12/C12' (batch share), G12 '=E12*F12' (allocated miles), subtotal G18 '=SUM(G12:G16)' = 1,693.3. Table B: leg-1 mileage F26 '=$B$21*H26' (one-way distance x truck count = 537x2 = 1,074.0), subtotal G28 '=SUM(G26:G27)' = 582.4. Grand total row = 2,275.7, matching Ops Notes' own displayed formula-driven cell. Batch-level totals B50/B51/B52 also confirmed as SUM formulas (item 2.1). [log:shipment_tracker]",
 "Auditability; FC-C3")
item("3.4", "Are computed outputs computed correctly per the allocation formulas?", "Pass",
 "Table A reproduces independently: e.g. COLA29 18/21=85.7% x 1,201 mi = 1,029.4 mi, matching the sheet; subtotal across 5 trucks = 1,693.3 mi. Table B Leg 1 (Colorado->Kansas): 4 batch totes / 34 totes aboard 2 trucks = 0.1176470588 share x (537 mi one-way x 2 trucks = 1,074.0 truck-miles) = 126.4 allocated mi. Leg 2 (Kansas->Basco): 4/6 = 0.6666666667 share x 684 mi = 456.0 allocated mi. Grand total 1,693.3 + 582.4 = 2,275.7 mi. Every one of these figures is independently confirmed against the VVB Guidance August 1-31 leg table, which states the identical leg-by-leg allocation and the identical 1,693.3 -> 2,275.7 progression. The Process (fuel-use, mass-based) term correctly uses actual one-way route distance (1,201 mi direct; 537+684=1,221 mi via Kansas) with NO doubling, while the Embodied (per-mile, truck-based) term correctly apportions truck-miles by tote share, per the VVB Guidance's explicit method statement: 'Vehicle embodied emissions are expressed per mile driven ... apportioned between the batches sharing it ... Fuel use is expressed per tonne-mile and therefore needs no apportionment.' [log:shipment_tracker] [log:vvb_guidance] [log:_derived_values]",
 "Shipment tracker EE Allocation tables; VVB Guidance Aug 1-31")
item("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag number, (b) fraction, (c) gross mass, (d) production period?", "Pass",
 "Kansas lane (4 totes): tag, fraction (QOWV), production period (PP#7) all match exactly between the tracker header and the Ops Notes highlighted block; gross mass ties via B52=4,039.00 kg matching the Certify 'Mass of load' on the KS-lane Process component exactly. Direct lane (33 totes): fraction and gross mass (B51=34,113.00 kg) match Certify exactly; the tracker's per-truck design (see 3.2) does not carry an individual tag list for this lane, so tag-level cross-check for the direct 33 rests on the Ops Notes IBC ledger as the single source, consistent with the same convention used and accepted on prior QOWV batches (INJ-07-2026-W1-QOWV: 'Gross mass is not a column on the roster ... single-sourced'). Zero mismatches found on any attribute that IS cross-referenced between the two documents. [log:shipment_tracker] [log:totes]",
 "Per-attribute roster comparison; FC-C5")

# ---------------------------------------------------------------- SECTION 4
section("Section 4 - Certify: Injection Sequestration (9.722 tCO2e)")
item("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
 "Sequestration modal INPUTS read carbon content of product = 8.2 %. Lab certificate SR26-05021.002 (client id 08-2026-W3 QOWV) reports Carbon 8.2% (m/m). Exact match. Recomputed: 32.3335 t x 8.2% x 3.667 = 9.7217 tCO2e against Certify's 9.722 t. [log:testing.qowv_certificate] [log:certify] [log:_derived_values]",
 "Certify Injection sequestration cmp_1M0ZD6K9J1S0RVSE")
item("4.2", "Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?", "Pass",
 "Carbon Content datapoint carries 2 sources: the lab PDF (CHARM INDUSTRIAL - 08-2026-W3 AECN + QOWV + Kerry) and the Ops Notes workbook, confirmed via the Sources tab '+6 more' expansion showing Ops Notes linked to Carbon Content of Bio-oil Injected among 7 datapoints. Both evidence types present and linked to the specific datapoint, not merely at component level. [log:certify.attachment_map]",
 "Certify Sources tab (23 sources enumerated)")
item("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
 "Modal INPUTS read mass of product = 32,333.5 ±41.95726 kg. Ops Notes J50 = 41.95726 kg. Exact match, entered as an absolute mass. The mass itself (32,333.5 kg) equals Ops Notes F50 (Total Oil Injected / MOBI) exactly, so sequestration is built on the injected mass. [log:certify] [log:ops_notes.totals_row_50]",
 "Certify Injection sequestration INPUTS")
item("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty?", "Pass",
 "Modal INPUTS read carbon content 8.2 ±0.032799999999999996 %. Expected 0.004 x 8.2 = 0.0328 percentage points; exact match, entered as an absolute percentage-point value rather than a flat '0.4'. [log:certify]",
 "Isometric Standard S3.7.3")

# ---------------------------------------------------------------- SECTION 5A (DIRECT LANE)
section("Section 5A - Certify: Transport Process Emissions, Direct Lane CO->Basco (5.670 tCO2e, 33 totes)")
item("5A.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
 "Modal INPUTS read 'Flatbed, Northern America, WTW' = 0.086 kgCO2e/(km*t), 1 source (GLEC V3.2). Live 2026 Standard EFs tab row 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck' = 0.0001384 MT CO2e/t-mi, marked Updated, source GLEC V3.2 2025 ISOMETRIC; converted 0.1384/1.60934 = 0.0859984 kgCO2e/(km*t), matching Certify's displayed 0.086 to full precision. This is a documented correction for this exact reporting period: VVB Guidance August 1-31 states QOWV totes travel flatbed not tanker, and the fuel-use factor was corrected from 0.1143 to 0.1384 kg CO2e/tonne-mile this period - exactly the value applied here. [log:standard_efs] [log:vvb_guidance] [log:certify] [log:_derived_values]",
 "Standard EFs sheet, 2026 tab; GLEC V3.2 2025; VVB Guidance Aug 1-31")
item("5A.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
 "'CO to Basco Routing Map.png' attached to the distance datapoint; downloaded at full resolution (1842x863) and read as pixels rather than relying on a thumbnail. It shows 3 route options to destination '4675 LA-115, St Landry, LA 71367': via US-287 S and US-287 S (fastest, avoids road closures), 17 hr 22 min, 1,132 mi; via US-287 S, US-287 S and I-20 E, 17 hr, 1,129 mi; via I-70 E (has tolls, different time zone), 17 hr 36 min, 1,201 mi. Certify's 'Distance from Miniforge CO to Basco' = 1,201 mi - the longest of the three, correctly not the fastest/default option. [log:routing_map_evidence]",
 "Certify Transport Process INPUTS; FC-C6")
item("5A.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
 "Modal INPUTS read mass of load = 'QOWV Transport Mass (CO to B6)' 34,113 ±37.42 kg. Ops Notes lane subtotal B51 (Total Mass Transported, direct lane) = 34,113.00 kg. Exact match - the correct gross basis including tote tares for this lane, not Total Oil Produced or Total Oil in Batch. Together with the Kansas-lane Process component's 4,039 kg, the two Process components' masses sum to 38,152 kg = Ops Notes batch-wide Total Mass Transported (B50) exactly, confirming the two-lane split fully covers the batch with no double-count or gap. [log:certify] [log:ops_notes]",
 "Certify Transport Process INPUTS; FC-C7")
item("5A.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
 "'INJ-08-2026-W3 Ops Notes.xlsx' attached in Certify and linked to 'QOWV Transport Mass (CO to B6)' specifically (confirmed among the 7 datapoints the Ops Notes source row covers). [log:certify.attachment_map]",
 "Certify Sources tab")
item("5A.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
 "Modal INPUTS read mass of load uncertainty ±37.42 kg. Expected 33 direct-lane totes x 1.13398 kg = 37.42 kg. Exact match. [log:certify] [log:_derived_values]",
 "Certify Transport Process INPUTS")

# ---------------------------------------------------------------- SECTION 5B (KANSAS LANE)
section("Section 5B - Certify: Transport Process Emissions, Kansas-Routed Lane CO->KS->Basco (0.683 tCO2e, 4 totes)")
item("5B.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
 "Identical EF to the direct lane: 0.086 kgCO2e/(km*t), 1 source, same live 2026 Flatbed Truck row. Consistent application across both lanes. [log:certify] [log:standard_efs]",
 "Standard EFs sheet, 2026 tab; GLEC V3.2 2025")
item("5B.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
 "Modal INPUTS read distance traveled = 1,221 mi, matching the Shipment Tracker's Via-KS route total (Charm CO->Charm KS 537 mi + Charm KS->Basco LA 684 mi = 1,221 mi one-way), which is also the exact figure documented in VVB Guidance August 1-31 ('the via-Kansas route totals 1,221 miles against 1,201 miles for the direct route, 1.7 per cent longer ... charging the route actually travelled both reflects the physical movement and is the conservative treatment'). This is the correct treatment for the actual physical route travelled by these 4 totes, not the standard direct-route distance. [log:shipment_tracker] [log:vvb_guidance]",
 "Certify Transport Process INPUTS; VVB Guidance Aug 1-31")
item("5B.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
 "Modal INPUTS read mass of load = 4,039 ±4.54 kg. Ops Notes lane subtotal B52 (Total Mass Transported, Kansas lane) = 4,039.00 kg. Exact match. [log:certify] [log:ops_notes]",
 "Certify Transport Process INPUTS; FC-C7")
item("5B.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
 "1 source on the Mass of load datapoint; consistent with the Ops Notes attachment pattern confirmed for the sibling direct-lane component and the batch's other Ops-Notes-sourced datapoints. [log:certify]",
 "Certify Sources tab")
item("5B.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
 "Modal INPUTS read mass of load uncertainty ±4.54 kg. Expected 4 Kansas-lane totes x 1.13398 kg = 4.54 kg. Exact match. [log:certify] [log:_derived_values]",
 "Certify Transport Process INPUTS")

# ---------------------------------------------------------------- SECTION 6 (BATCH-LEVEL EMBODIED)
section("Section 6 - Certify: Transport Embodied Emissions, Batch-Wide (0.439 tCO2e, single component covering both lanes)")
item("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Pass",
 "Modal INPUTS read 'Distance emission factor' = 0.119794 kgCO2e/km, 1 source (Standard Emission Factors + Calculations (8).xlsx). Live 2026 tab row 'Vehicle Embodied Emissions --Non-Tanker Truck' = 0.00019279082556 MT CO2e/mi, marked Updated, source GLEC V3.2 2025; converted 0.19279/1.60934 = 0.119794 kgCO2e/km, exact match. This is a documented correction for this exact reporting period: VVB Guidance August 1-31 states the embodied factor was corrected from 0.23756 to 0.19279 kg CO2e/mile (non-tanker truck) this period, replacing the tanker factor previously applied. [log:standard_efs] [log:vvb_guidance] [log:certify]",
 "Standard EFs sheet, 2026 tab; GLEC V3.2 2025; VVB Guidance Aug 1-31")
item("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Flag",
 "Modal INPUTS read distance traveled = 'QOWV Embodied Distance (CO->KS->B6)' 2,275.7 mi. This is the Shipment Tracker's GRAND TOTAL ALLOCATED MILES cell (A+B) = 2,275.7 mi, i.e. the WHOLE batch's allocated embodied mileage: Direct-lane Subtotal A (1,693.3 mi, 33 totes across 5 trucks) PLUS Kansas-lane Subtotal B (582.4 mi, 4 totes across 3 truck-legs). Independently confirmed against VVB Guidance August 1-31's leg table, which states the identical progression: 'Total allocated miles for the week therefore rise from 1,693.3 ... to 2,275.7.' The value is exactly correct and fully evidenced. "
 "The finding is a naming/scope-clarity issue only: the component and datapoint are titled 'CO->KS-> LA ... Embodied Emissions', which reads as covering only the 4-tote Kansas leg, when the figure it actually carries is the AGGREGATE embodied allocation for the entire 37-tote batch (both lanes). A verifier reading the component name alongside its 2,275.7 mi value without cross-referencing the Shipment Tracker could reasonably (and wrongly) conclude the number is Kansas-leg-only or double-counted against the direct lane's Process components. Recommend renaming to something scope-neutral, e.g. 'QOWV Flatbed Truck Transport Embodied Emissions' (dropping the CO->KS->LA lane-specific prefix), to match its true batch-wide scope - no change to the number is needed. [log:shipment_tracker] [log:vvb_guidance] [log:certify]",
 "Certify Transport Embodied INPUTS; Shipment Tracker Grand Total row")
item("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Pass",
 "2 sources on the Embodied Distance datapoint: 'INJ-08-2026-W3 Ops Notes.xlsx' (which carries the QOWV Shipments & EE Allocation tab, i.e. the RP Bio-Oil Shipment Tracker) and 'CO to Basco Routing Map.png' (the applicable route Google Map, also evidencing the underlying 1,201 mi and 537/684 mi leg distances). "
 "The Charm Contents limb is not achievable and is not held against the batch: no Charm Contents sheet exists in the Drive batch folder or the Certify Sources tab (23 sources enumerated, none titled Charm Contents), consistent with the established precedent on prior 2026 weekly-batch QOWV/WODO removals (e.g. INJ-07-2026-W1-QOWV) that this artifact no longer exists for any 2026 weekly time-block batch - its function, the per-Production-Period mass breakdown, is carried in the Ops Notes IBC ledger's Production Period column, which IS attached and linked. [log:certify.attachment_map] [log:batch_folder_inventory]",
 "Certify Sources tab; VR Appendix 1")

# ---------------------------------------------------------------- SECTION 7
section("Section 7 - Certify: Production Emissions (4.574 tCO2e, one aggregated component across 6 PPs)")
item("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", "Pass",
 "All Production Periods that contributed mass are accounted for in one aggregated component, 'Pyrolysis - Charm QOWV PP Emissions', carrying a production-mass-weighted blended carbon intensity (0.12697098348438993 tCO2e/t) drawn from Ops Notes' own weighted-average formula (H50). The aggregation reconciles exactly: 36,020.8 kg x 0.12697098348438993 = 4,573.60 kg = Ops Notes I50 (per-tote emissions total) = Certify's 4.574 tCO2e. Totes span 6 distinct production periods (PP#8, November 2025, February 2026, March 2026, April 2026 on the direct lane; PP#7 on the Kansas lane) with no period omitted and none double-counted. VVB Guidance August 1-31 independently confirms the Kansas-lane totes' pyrolysis emissions are correctly keyed to production month, not to route or injection week: 'Pyrolysis emissions for these totes remain keyed to the month in which the oil was produced, not to the route taken or to the week of injection.' Aggregating periods into one mass-weighted component is not a deviation - no primary source requires one component per production period. [log:ops_notes] [log:vvb_guidance] [log:certify] [log:_derived_values]",
 "Certify Components tab; FC-C2, FC-C11; VVB Guidance Aug 1-31")
item("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Pass",
 "Modal INPUTS read carbon emission factor = 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' 0.12697098348438993 tCO2e/t. Ops Notes H50 is the formula '=IFERROR(SUMPRODUCT(D11:D48,H11:H48)/SUMIF(H11:H48,\"<>\",D11:D48),\"\")' and returns 0.1269709835. Match to 9 decimal places (display precision limit). All 37 totes predate the Jul-Dec 2026 H1-2026-blended-CI window (per corrected workspace policy, the blended CI 0.120947 applies only to oil produced Jul-Dec 2026), so individual monthly/PP CIs are correctly applied throughout rather than the blended figure - no cross-wiring with WODO (this week's Ops Notes Charm WODO tab is all-zero, no WODO fraction to cross-wire against). [log:ops_notes] [log:certify]",
 "Certify Pyrolysis INPUTS; FC-C10")
item("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Pass",
 "'INJ-08-2026-W3 Ops Notes.xlsx' is among the 18 sources attached to the 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' datapoint (confirmed via the Sources tab '+6 more' expansion). That is the required evidence standard for production carbon intensity - the Ops Notes weighted average across all totes in the injection; a standalone Production Period Summary is not required. The remaining 17 sources are the underlying November 2025 PP calculation-chain documents (Production Period Summary, Up-Time Reporting, Waste Disposal Calc, Water Usage Log, Propane/Diesel Consumption Calcs, route maps, invoice, CSVs), corroborating rather than substituting the Ops Notes weighted average. [log:certify.attachment_map]",
 "Certify Sources tab")
item("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", "Pass",
 "Modal INPUTS read mass = 'QOWV Pyrolysis Mass [Certify input]' 36,020.8 kg. Ops Notes Total Oil Produced (D50) = 36,020.80 kg. Exact match - the correct basis (net oil in tote, i.e. actually produced at the pyrolyser), covering both lanes' totes, not Net Oil Injected (32,333.50 kg) which would understate production emissions by excluding measured post-unload residue. [log:certify] [log:ops_notes]",
 "Certify Pyrolysis INPUTS")
item("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", "Pass",
 "Modal INPUTS read mass 36,020.8 ±41.96 kg. Ops Notes J50 = 41.95726 kg, displayed to two decimals as 41.96. Match. Uncertainty is present and correctly sized (37 totes x 1.13398 kg) on this dominant input - pyrolysis is 97.94% of Activities and 4.574 t against a net of 4.669 t (~98%), so it does not qualify for the <1% omission carve-out and its uncertainty is correctly required and present, avoiding the FC-C12 failure pattern seen on a prior WODO batch. [log:certify] [log:ops_notes] [log:_derived_values]",
 "Isometric Standard S3.7.3; FC-C12")
item("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
 "Charm Contents does not exist as an artifact for this or any 2026 weekly time-block batch - confirmed absent from both the Drive batch folder (4-item enumeration: Ops Notes workbook, Kerry Scale Tickets, Scale Tickets, Testing, Completed QA Checklists folders - no Charm Contents) and the Certify Sources tab (23 sources enumerated, none so titled), consistent with the precedent established on INJ-07-2026-W1-QOWV. Its function - the per-Production-Period mass breakdown - is carried by the Ops Notes QOWV IBC ledger, where column G gives each tote's production period against column D's net oil produced; that workbook is attached in Certify and linked to the 'QOWV Pyrolysis Mass [Certify input]' datapoint, so the mass is evidenced by the document that now holds the content. [log:batch_folder_inventory] [log:certify.attachment_map]",
 "Certify Sources tab; Document Location Rule")

# ---------------------------------------------------------------- SECTION 8
section("Section 8 - Other")
item("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total >= the transport-process sum?", "Pass",
 "'BCU - Transport Process' applies a constant reduction of 6,353 kgCO2e (6.353 t), evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf'. The batch's two diesel Transport Process emissions - direct lane 5.670 t and Kansas lane 0.683 t - sum to exactly 6.353 tCO2e. The BCU offsets this combined sum exactly (neither under- nor over-covering), satisfying both the Max-stated 'all diesel transport-process emissions must be BCU-offset' rule and the workspace policy against BCU over-coverage. Transport Embodied emissions (0.439 t, not diesel-process) correctly carry no BCU. [log:certify] [log:bcu_check]",
 "Charm methodology - all diesel transport-process emissions must be BCU-offset; project_bcu_reduction_cap_policy")

# ---------------------------------------------------------------- SECTION 9
section("Section 9 - Aqueous Buffering (LCS)")
item("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist (correct mass, correct EF, evidenced)?", "N/A",
 "No LCS use is reported for this batch. A full visual review of the QOWV tab's complete column set (Tag, Gross Mass, Tote Mass, Net Oil Produced, Empty Tote Weight, Net Oil Injected, Production Period, Carbon Intensity, Production Emissions, Scale Uncertainty, plus the Constants block covering Lbs/Kg, Kg/Lbs, Sparging Mass Loss, pH range, QOWV 6-Mo CI) found no LCS / Liquid Calcium Sulfate / buffer column of any kind across all 37 tote rows. The VVB Guidance August 1-31 document, read in full, contains no LCS section for this reporting period. [log:lcs_check] [log:vvb_guidance]",
 "Ops Notes; FC-C4")

# ---------------------------------------------------------------- SIDEBAR
r += 1
c = ws.cell(row=r, column=1, value="Sidebar Observations (no Pass/Fail status - flagged for attention)")
c.font = BOLD; c.fill = HDR
for col in range(2, 6):
    ws.cell(row=r, column=col).fill = HDR
r += 1

sidebar = [
 "Two-lane transport structure. This is the first QOWV batch reviewed with a genuine two-lane transport split within a single injection batch: 33 totes travelled Colorado direct to Basco (1,201 mi), while 4 totes (tags 118811/118837/118872/118886) were trucked Colorado to Charm's Kansas site on 2025-10-21, stored, and later repositioned Kansas to Louisiana (1,221 mi via-route). Certify correctly carries this as TWO separate Transport Process components (one per lane, each with its own mass and distance) but only ONE Transport Embodied component (aggregating both lanes' allocated truck-miles, since embodied cost is per-mile/truck-based rather than per-shipment). This structure, and every distance and mileage-allocation figure used, is independently confirmed by the VVB Guidance August 1-31 document, which devotes a full section to explaining exactly this routing and the reasoning behind it - an unusually well-documented case.",
 "QOWV emission-factor correction, disclosed. This reporting period, Charm corrected the QOWV tote-transport emission factors from tanker to flatbed/non-tanker values (fuel-use 0.1143->0.1384 kg CO2e/tonne-mile; embodied 0.23756->0.19279 kg CO2e/mile), per VVB Guidance August 1-31: 'QOWV totes travel on a flatbed trailer, not in a tanker... Until this period the calculation applied tanker emission factors to both QOWV transport terms.' Both new factors were independently re-derived from the live 2026 Standard EFs sheet during this QA and matched exactly. The correction is conservative (increases reported transport emissions, reduces net removal by ~0.9 tCO2e this week per the guidance) and fully disclosed to the verifier ahead of review.",
 "Embodied component naming (see Flag 6.2). The single Transport Embodied component's title names only the Kansas leg ('CO->KS-> LA') while its value is the whole-batch aggregate. Recommend a scope-neutral rename; no numeric change needed.",
 "AECN railcar Trailer Standard Empty Weight substitutions this RP (GPRX5139 offload 1, Week 3) are unrelated to this QOWV removal - they concern AECN rail offloads in the same weekly workbook, not QOWV tote transport. Noted only to confirm the VVB Guidance section was read in full and correctly scoped out as not applicable to this checklist.",
]
for s in sidebar:
    ws.cell(row=r, column=1, value="-").font = BODY
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
summary = ("STATUS SUMMARY: %d Pass - %d Flag - %d Fail - %d N/A  (%d items)  |  ZERO FAILS. "
 "Every Certify component independently recomputed from primary sources and reconciles: sequestration 32.3335 t x 8.2%% x 3.667 = 9.7217 t vs 9.722 t; direct-lane process 34.113 t x 1,201 mi x 0.086 = 5.670 t; Kansas-lane process 4.039 t x 1,221 mi x 0.086 = 0.683 t; batch-wide embodied 2,275.7 mi x 0.119794 = 0.439 t; pyrolysis 36.0208 t x 0.126971 = 4.574 t; BCU 6.353 t offsets the two process emissions (5.670+0.683) exactly. Net 9.722 + 6.353 - 11.366 - 0.042 = 4.669 t, matching Certify's displayed Net CO2e Removed. "
 "Mass chain is clean: all Ops Notes totals (Total Mass Transported, Total Oil Produced, Total Oil in Batch/MOBI, uncertainty) reconcile to zero delta across 37 totes; Aqueous measured-loss method correctly applied with no Standard Loss; every allocation cell in the Shipment Tracker is a live formula; all Production Periods captured in one reconciling aggregated component. "
 "This batch is unusual for its genuine two-lane transport split (33 direct + 4 Kansas-routed totes) and a QOWV-specific tanker-to-flatbed emission-factor correction, both of which are explicitly documented and explained in the VVB Guidance August 1-31 document, read in full before any other source per Gate 1 step 0. Every figure independently derived from Certify, Ops Notes, and the Standard EFs sheet matches the guidance's own stated numbers exactly, with no unexplained anomalies. "
 "One Flag: 6.2, the single Transport Embodied component's title names only the Kansas leg while its value is the whole-batch aggregate - a naming/scope-clarity issue, not a value error; recommend a scope-neutral rename." % (
 counts.get("Pass", 0), counts.get("Flag", 0), counts.get("Fail", 0), counts.get("N/A", 0), total))
c = ws.cell(row=r, column=1, value=summary); c.font = BOLD
c.alignment = Alignment(vertical="top", wrap_text=True)

ws.column_dimensions["A"].width = 9
ws.column_dimensions["B"].width = 52
ws.column_dimensions["C"].width = 9
ws.column_dimensions["D"].width = 100
ws.column_dimensions["E"].width = 32
ws.freeze_panes = ws.cell(row=HEADER_ROW + 1, column=1)

out = "Charm_Aqueous_QOWV_QA_Checklist_INJ-08-2026-W3.xlsx"
wb.save(out)
print("saved", out)
print("counts", counts, "total", total)
