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
 ("Batch ID", "INJ-07-2026-W1-QOWV  (Ops Notes QOWV tab records the batch id as INJ-06-2026-W2 - deferred June Week-2 Aqueous batch reported in the July RP)"),
 ("Reporting Period", "July 1 - July 31 2026 RP; batch week per Ops Notes 2026-06-06 to 2026-06-13; Certify removal window 01-04 Jul 2026"),
 ("Reviewer", "Claude (QA agent) - for Max Lavine review"),
 ("Date", "2026-08-06"),
 ("Injection Site", "Basco 6 (Louisiana)"),
 ("Oil Type", "Aqueous / QOWV (Charm-produced, Fort Lupton CO) - 36 IBC totes, shipped 2025-12-09 (18) and 2025-12-10 (18)"),
 ("Production Periods", "PP#7 (14 totes, CI 0.1373671128), PP#8 (3 totes, CI 0.1575553395), October 2025 (19 totes, CI 0.1110176229)"),
 ("Certify Removal ID", "rmv_1KZBTSNE81S0DJT1  |  Net 5.526 tCO2e  |  GHG statement ggs_1KZBX6AX41S029JS"),
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
 "Cleared on the 2026-08-06 re-read. Certify's carbon content was resolved to 8.40 %, which is the value reported by '07-26-W1-QOWV.pdf' - SGS SR26-04323.001, client id '07-26-W1-QOWV', Fort Lupton CO, completed 21-Jul-2026 11:01, Carbon 8.4 % (m/m) ASTM D5291 Method C, Hydrogen 8.8 %, Nitrogen <0.75 %, density 15 C 1.048 g/cm3, viscosity 40 C 1.005 cSt, acid number 33 mg KOH/g. "
 "That certificate is in the batch Testing subfolder and is attached in Certify, so the operative lab report is present in both permitted locations. The folder also holds the QOWV physical-properties certificate for sample 6-2026-W2 (SR26-04323.001, viscosity/TAN/density, no CHN) and SR26-04220.001/.002 (AECN 40.5 %, QOWV 7-2026-W2 8.4 %). "
 "Which sample governs is a question the checklist cannot settle and item 4.2 carries it: the Ops Notes cell note still names 9.20 % from SR26-03726.003 as this batch's carbon and assigns 8.4 % to a different batch. [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "VR Appendix 1; Document Location Rule (Drive OR Certify Sources)")
item("1.2", "Are Ops Notes in the folder and fully completed?", "Flag",
 "'INJ-07-2026-W1 Ops Notes' is present with 8 tabs and the QOWV tab is fully populated for mass: all 36 tote rows carry tag, gross mass, tote mass, net oil produced, measured empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty, with no blanks and no formula errors, and every totals cell on row 53 is a live SUM or SUMPRODUCT formula. "
 "The carbon cells were corrected on 2026-08-06 at 21:21:14Z (version 168): Summary!D20 now reads 8.40 % and F20 recomputed to 0.0336 %, matching Certify and the attached lab certificate. Two documentation gaps remain, neither of which changes a reported number. "
 "First, the cell note on QOWV!B2 was not updated with the cells. It still reads 'C content (9.20%, SGS SR26-03726, sample 6-2026-W2-QOWV) received after the June RP closed' and 'Distinct from the July-W2 QOWV batch (INJ-20260709, C% 8.4%)'. It therefore contradicts the 8.40 % now sitting three cells away, and tells a verifier that the figure the removal actually uses belongs to a different batch. The note is present in the copy attached in Certify as well as the live sheet, so a verifier will read it. "
 "Second, the QOWV tab defines 'pH range (target)' = 2.0 - 4.0 at K6/L6 and records no measured pH anywhere: an every-cell scan of the used range A1:N73 returns that single header hit and no pH column for the 36 totes. The AECN Rail tab in the same workbook records a measured pH of 3.70 against every offload. [log:ops_notes] [log:totes] [log:ph_absence] [log:ph_absence._primary_source_opened] [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z] [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z._primary_source_opened] [log:_derived_values]",
 "VR Appendix 1; UIC permit pH range")
item("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Pass",
 "Under the weekly time-block schema the tracker is carried as the 'QOWV Shipments & EE Allocation' tab inside the batch Ops Notes workbook, which is in the batch folder. No standalone Bio-Oil Shipment Tracker file exists for 2026 weekly batches (a Drive title search for 'Bio-Oil Shipment Tracker' returns only April 2026 copies). The tab is complete: batch summary row (36 totes, injection week 2026-06-06 to 2026-06-13, ship dates 2025-12-09 x18 and 2025-12-10 x18), one-way distance input B8 = 1201, the EE allocation table for both trucks, the batch mileage allocation block, and the full 36-tote roster with tag, fraction, production period, date loaded and batch. [log:shipment_tracker] [log:shipment_tracker_roster] [log:batch_folder_inventory]",
 "VR Appendix 1")

# ---------------------------------------------------------------- SECTION 2
section("Section 2 - Ops Notes")
item("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", "Pass",
 "Reported 37,833.00 kg at QOWV!B53, which is the live formula '=SUM(B11:B46)'. Independent sum of the 36 per-tote gross masses = 37,833.00 kg; delta 0.0000 kg. The SUM range B11:B46 spans exactly the 36 populated tote rows with none omitted and no blank row inside the range. The Summary tab carries the same figure through '=QOWV!B53'. [log:ops_notes] [log:ops_notes_totals] [log:totes] [log:_derived_values]",
 "Ops Notes QOWV tab, Section 1 IBC Ledger")
item("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", "Pass",
 "Reported 35,759.40 kg at QOWV!D53 = '=SUM(D11:D46)'; each per-tote cell is the formula '=B-C', never a typed constant. Independent sum of (gross - tare) across all 36 totes = 35,759.40 kg; delta 0.0000 kg. "
 "The tab carries two tare-like columns and each is correct for its own purpose. Column C is 57.60 kg for every tote - the empty weight of the IBC container itself, uniform because the containers are identical. Column E is the measured post-unload weight of the tote and varies from 111.50 to 270.00 kg because it is the container plus the residual oil left behind. Net Oil Produced therefore subtracts C, capturing all the oil that was in the tote, and Net Oil Injected subtracts the measured E, capturing what actually left it; the difference between the two totals, 4,322.40 kg, is the measured residue. No weighing is substituted or missing. [log:ops_notes] [log:ops_notes_qowv_tab_cells] [log:totes] [log:_derived_values]",
 "Ops Notes QOWV tab, column C/D")
item("2.3", "Is the 'Total Oil in Batch' value correctly computed (Aqueous: measured pre-unload minus measured post-unload per tote, no Standard Loss)?", "Pass",
 "Reported 31,437.00 kg at QOWV!F53 = '=SUM(F11:F46)'; each per-tote cell is the formula '=IF(E=\"\",\"\",B-E)', i.e. gross mass minus the directly measured empty tote weight after unloading. Independent sum across all 36 totes = 31,437.00 kg; delta 0.0000 kg. "
 "The Aqueous method is correctly applied and no Standard Loss deduction appears: a programmatic check of all 36 net-in-batch formulas found zero references to a Standard Loss term, and the per-tote empty weights vary genuinely from 111.50 kg to 270.00 kg, which is measurement rather than a fixed allowance. Measured tote loss = 6,396.00 kg of measured empty weight less 2,073.60 kg of nominal tare = 4,322.40 kg, which equals Net Oil Produced minus Net Oil Injected (35,759.40 - 31,437.00 = 4,322.40 kg) exactly. The WODO-only 'WODO Tote Standard Loss - 2026 Dataset' sheet in the same folder is correctly not applied to this Aqueous batch. [log:ops_notes] [log:totes] [log:computed_crosschecks] [log:_derived_values]",
 "Ops Notes QOWV tab column F; FC-C1")
item("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
 "Reported 40.82328 kg at QOWV!J53 = '=SUM(J11:J46)'; each per-tote cell is '=2.5*$L$4' where L4 is the Kg/Lbs constant 0.453592, giving 1.13398 kg per tote. Expected 2.5 lb / 2.20462 x 36 totes = 40.82336 kg; delta 0.00008 kg, well inside the 0.01 kg tolerance (the sheet multiplies by the kg-per-lb constant rather than dividing by lb-per-kg, which agrees to five decimals). The Charm per-tote precision of 1.134 kg is correctly applied here; this is not the AECN 72.57 kg per-truck spec. [log:ops_notes] [log:totes] [log:_derived_values]",
 "Isometric Standard S3.7.3 Option B; FC-C8")

# ---------------------------------------------------------------- SECTION 3
section("Section 3 - Bio-Oil Shipment Tracker (QOWV Shipments & EE Allocation tab)")
item("3.1", "Are totes for the RP correctly identified?", "Pass",
 "36 totes are listed for the batch across two shipments (18 on 2025-12-09, 18 on 2025-12-10) and all 36 appear in the Ops Notes IBC ledger. The tag sets are identical between the two tabs, verified programmatically rather than sampled: no tote appears in one tab and is absent from the other, and there are no duplicate tags in either. Every roster row carries fraction QOWV and batch INJ-06-2026-W2. [log:shipment_tracker] [log:shipment_tracker_roster] [log:totes]",
 "Shipment tracker tab rows 22-39 and 43-60")
item("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Pass",
 "36 of 36 match with zero mismatches on every attribute the roster carries: tag, fraction (all QOWV on both tabs) and production period. Per-tote production periods agree exactly, and so do the counts - PP#7 x14, PP#8 x3, October 2025 x19, totalling 36. Gross mass is not a column on the roster; it is held once, in IBC ledger column B, which is the cell Certify's mass of load draws from, so there is no divergent second copy to reconcile. [log:shipment_tracker_roster] [log:totes]",
 "Roster vs Ops Notes IBC ledger")
item("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
 "Every computed cell read from the workbook is a live formula and not one is a typed constant. Batch Share of Truck: E12 = '=D12/C12', E13 = '=D13/C13'. Mileage one-way: F12 = '=$B$8', F13 = '=$B$8'. Allocated Miles: G12 = '=E12*F12', G13 = '=E13*F13'. Totals: C14 = '=SUM(C12:C13)', D14 = '=SUM(D12:D13)', G14 = '=SUM(G12:G13)'. Batch Mileage Allocation: C18 = '=G14', tote count D18 = '=D14'. A verifier can rebuild the whole allocation from the tote counts and the single mileage input. [log:shipment_tracker_cells_are_formulas] [log:shipment_tracker._primary_source_opened]",
 "Auditability; FC-C3")
item("3.4", "Are computed outputs computed correctly per the allocation formulas?", "Pass",
 "All three reproduce the specification independently. Shipment 12-09: 18 batch-relevant of 36 on the truck = 50.00 % share; 50.00 % x 1,201 mi one-way = 600.50 mi, matching the sheet. Shipment 12-10: 18 of 35 = 51.4286 %; x 1,201 mi = 617.66 mi, matching the sheet. Batch Mileage Allocation = 600.50 + 617.66 = 1,218.16 mi, matching C18 to within 0.003 mi of the recomputation. The mileage input B8 is labelled 'Charm CO -> Basco LA distance (one-way miles)' and is used one-way with no round-trip doubling, correct for this batch. The allocated total legitimately exceeds the 1,201 mi one-way figure because it sums two separate truck movements. [log:shipment_tracker] [log:shipment_tracker_cells_are_formulas] [log:_derived_values]",
 "Shipment tracker EE Allocation table")
item("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag number, (b) fraction, (c) gross mass, (d) production period?", "Pass",
 "(a) Tag - 36 of 36 identical, no extras either direction, no duplicates. (b) Fraction - 36 of 36 QOWV on both tabs. (c) Gross mass - single-sourced: the roster columns are Metal Tag, Fraction, Production Period, Date Loaded and Batch, with no mass column, so gross mass exists exactly once in IBC ledger column B and is the cell feeding Certify; its sum is verified at 37,833.00 kg in item 2.1. (d) Production period - 36 of 36 identical per tote and in aggregate. Zero mismatches on any attribute. [log:shipment_tracker_roster] [log:totes]",
 "Per-attribute roster comparison; FC-C5")

# ---------------------------------------------------------------- SECTION 4
section("Section 4 - Certify: Injection Sequestration (10.606 tCO2e)")
item("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
 "Cleared on the 2026-08-06 re-read. The Sequestration modal INPUTS now read carbon content of product = 8.4 %, and the lab certificate attached to that datapoint - SR26-04323.001, client id '07-26-W1-QOWV' - reports Carbon 8.4 % (m/m). Delta 0.0 percentage points. "
 "The component recomputes from those inputs: 31.437 t x 8.4 % x 3.667 = 9.6835 tCO2e against Certify's 9.683 t. Adopting 8.4 % in place of the earlier 9.20 % reduced the sequestration claim by 0.922 tCO2e, a conservative movement. [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "Certify Injection sequestration cmp_1KZBTSNE81S09R6B")
item("4.2", "Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?", "Pass",
 "Cleared on the 2026-08-06 21:50Z re-read. Both required evidence types are attached to the Carbon Content datapoint and both now support 8.40 %. The lab certificate '07-26-W1-QOWV.pdf' (SR26-04323.001) reports Carbon 8.4 %. "
 "The Ops Notes copy was re-uploaded after the sheet was corrected, and I verified the attached copy itself rather than only the live sheet: downloaded from Certify and opened, it reads Summary!D20 = 8.40 % and Summary!F20 = 0.0336 %. The workbook was re-linked per datapoint, so the Ops Notes now appears as six separate source rows on this removal, one for each datapoint it evidences, and the removal's source count went from 6 to 11. "
 "One piece of stale text remains and is carried as a Flag at 1.2 rather than here, because it changes no number: the QOWV!B2 cell note still reads 'C content (9.20%, SGS SR26-03726, sample 6-2026-W2-QOWV)' and 'Distinct from the July-W2 QOWV batch (INJ-20260709, C% 8.4%)' in both the live sheet and the attached copy, which now contradicts the sheet's own 8.40 %. [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z] [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z._primary_source_opened] [log:_derived_values]",
 "Certify Sources tab (11 sources enumerated)")
item("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
 "Modal INPUTS read: mass of product = 'Mass of Injectant (per injection)' 31,437 +/-40.82 kg. Ops Notes J53 = 40.82328 kg, which Certify displays to two decimals as 40.82. Match. Entered as an absolute mass, not a percentage. The mass itself, 31,437 kg, equals Ops Notes Net Oil Injected (F53) exactly, so the sequestration is built on the injected mass rather than on produced or transported mass. [log:certify] [log:ops_notes_totals]",
 "Certify Injection sequestration INPUTS")
item("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty?", "Pass",
 "Cleared on the 2026-08-06 21:50Z re-read. The Injection sequestration modal INPUTS now read carbon content 8.4 +/-0.0336 %. Expected 0.004 x 8.4 = 0.0336 percentage points; delta 0.0000, and the relative uncertainty is exactly 0.4 % rather than the 0.438 % the stale figure produced. "
 "Corroborated in the Ops Notes, where Summary!F20 is the formula '=D20*G20' and now returns 0.0336 % off the corrected 8.40 %. Entered as an absolute percentage-point value, not as '0.4'. [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z] [log:w1_opsnotes_attachment_sweep_2026_08_06T2150Z._primary_source_opened] [log:_derived_values]",
 "Isometric Standard S3.7.3")

# ---------------------------------------------------------------- SECTION 5
section("Section 5 - Certify: Transport Process Emissions (5.193 tCO2e)")
item("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
 "Cleared on the 2026-08-06 re-read. The modal INPUTS now read the datapoint 'Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Flatbed Truck' at 0.1384 kgCO2e/(t*mi), which is the live 2026 tab row 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck' = 0.0001384 MT CO2e/t-mi, cited GLEC V3.2 2025 and marked Updated. Exact match in native units, and the datapoint name now matches the sheet row name. "
 "Recomputed from full precision: 37.833 t x 1201 mi = 45,437.433 t-mi; x 0.0001384 = 6.2885 tCO2e against Certify's 6.289 t. The component title was also corrected from 'Tanker Truck' to 'CO to LA Flatbed Truck Transport Process Emissions - QOWV'. [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "Standard EFs sheet, 2026 tab; GLEC V3.2 2025")
item("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
 "'CO to Basco Routing Map.png' is attached to the distance datapoint and was read as pixels (1842x863). It shows three route options to destination '4675 LA-115, St Landry, LA 71367': via US-287 S and US-287 S, 17 hr 22 min, 1,132 miles, labelled 'Fastest route now, avoids road closures'; via US-287 S, US-287 S and I-20 E, 17 hr 32 min, 1,129 miles; and via I-70 E, 17 hr 36 min, 1,201 miles. Certify's 'Distance from Miniforge CO to Basco' reads 1,201 mi - the longest of the three, correctly not the fastest. It also agrees with the Ops Notes allocation input B8 = 1201. The origin field displays 'Your location' with the pin in the Denver-Fort Lupton corridor; origin confirmed as Fort Lupton (Max-stated 2026-08-06). [log:google_maps_options] [log:google_maps_options_artifact] [log:certify]",
 "Certify Transport Process INPUTS; FC-C6")
item("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
 "Modal INPUTS read: mass of load = 'QOWV Transport Mass (CO to B6) [Certify input]' 37,833 kg. Ops Notes Total Mass Transported (QOWV!B53) = 37,833.00 kg. Exact match. This is the correct gross basis including tote tares - not Total Oil Produced (35,759.40 kg) and not Total Oil in Batch (31,437.00 kg), either of which would have understated the load. [log:certify] [log:ops_notes_totals]",
 "Certify Transport Process INPUTS; FC-C7")
item("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
 "'INJ-07-2026-W1 Ops Notes.xlsx' is attached in Certify and linked to the 'QOWV Transport Mass (CO to B6) [Certify input]' datapoint specifically, not merely at removal level - the Sources tab shows that datapoint as the first of five the Ops Notes carries. [log:certify.attachment_map] [log:certify.certify_sources_enumeration]",
 "Certify Sources tab")
item("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
 "Modal INPUTS read: mass of load 37,833 +/-40.82 kg. Ops Notes J53 = 40.82328 kg, displayed to two decimals as 40.82. Match, and identical to the Mass of Product uncertainty on the Sequestration component as it should be - the same 36 totes, weighed once each. [log:certify] [log:ops_notes_totals]",
 "Certify Transport Process INPUTS")

# ---------------------------------------------------------------- SECTION 6
section("Section 6 - Certify: Transport Embodied Emissions (0.289 tCO2e)")
item("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Flag",
 "The value is now right and only the label is wrong. The modal INPUTS read 0.1928 kgCO2e/mi, which is the live 2026 tab row 'Vehicle Embodied Emissions --Non-Tanker Truck' = 0.0001927908255646154 MT CO2e/mi, cited GLEC V3.2 2025. Recomputed: 1,218.16 mi x 0.0001927908255646154 = 0.2349 tCO2e against Certify's 0.235 t. The superseded tanker factor of 0.23756 kgCO2e/mi is gone. "
 "The flag is traceability: the datapoint is titled 'Emissions Factor - Vehicle Embodied Emissions - Flatbed Truck', but there is no Flatbed Truck row on the embodied side of the 2026 tab - the row supplying this value is Non-Tanker Truck. A verifier tracing the name back to the sheet will not find it. Rename the datapoint to Non-Tanker Truck to match its source row; the number needs no change. The sibling WODO removal rmv_1KYWMYBJ51S0HH3N, in this same week and reporting period, names the identical factor correctly as 'Emissions Factor - Vehicle Embodied Emissions - Non-Tanker Truck', so this removal is the outlier of the two. [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "Standard EFs sheet, 2026 tab; GLEC V3.2 2025")
item("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Pass",
 "Modal INPUTS read: distance travelled = 'QOWV Embodied Distance (CO to B6) [Certify input]' 1,218.16 mi. The Shipment tracker's Batch Mileage Allocation (C18 = '=G14') is 1,218.16 mi. Exact match, carried to two decimals rather than rounded to the 1,218 mi shown on the Datapoints list. The allocated figure - not the full 1,201 mi one-way distance - is correctly what the embodied component uses. [log:certify] [log:shipment_tracker_cells_are_formulas] [log:_derived_values]",
 "Certify Transport Embodied INPUTS")
item("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Pass",
 "Cleared on the 2026-08-06 re-read. Certify sources went from 6 to 7 with a new row linking 'INJ-07-2026-W1 Ops Notes.xlsx' to 'QOWV Embodied Distance (CO to B6) [Certify input]', and the embodied modal now shows that datapoint carrying 2 sources rather than 1. The allocation arithmetic behind the 1,218.16 mi figure is therefore evidenced by the workbook that holds it - the QOWV Shipments & EE Allocation tab - alongside the route map that evidences the 1,201 mi leg. "
 "The Charm Contents limb is not achievable and is not held against the batch: no Charm Contents sheet exists for any 2026 weekly time-block batch, confirmed by four independent searches - a Drive title search returning only the pre-weekly sheets 5-07, 5-08, 5-10, 3-55 and 3-56; a title-plus-recency search returning only unrelated CAD drawings; enumeration of the batch folder; and the Certify sources list. Its content, the per-Production-Period mass breakdown, now lives in the Ops Notes IBC ledger. [log:charm_contents_absence] [log:charm_contents_absence._primary_source_opened] [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "Certify Sources tab; VR Appendix 1")

# ---------------------------------------------------------------- SECTION 7
section("Section 7 - Certify: Production Emissions (4.461 tCO2e)")
item("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", "Pass",
 "All three production periods that contributed mass are accounted for. The batch draws on PP#7 (14 totes), PP#8 (3 totes) and October 2025 (19 totes), together 36 totes, and they are captured in one aggregated component, 'Pyrolysis - Charm QOWV PP Emissions', carrying a production-mass-weighted blended carbon intensity. The aggregation reconciles exactly: PP#7 13,507.60 kg x 0.1373671128 = 1,855.50 kg, PP#8 2,896.20 kg x 0.1575553395 = 456.31 kg, October 2025 19,355.60 kg x 0.1110176229 = 2,148.81 kg, summing to 4,460.62 kg, which equals the Ops Notes per-tote emissions total at I53 (4,460.62 kg) and the component's 4.461 tCO2e. No period is omitted and none is double-counted. Aggregating periods into one mass-weighted component is not a deviation - no primary source requires one component per production period. [log:computed_crosschecks] [log:computed_crosschecks.per_pp] [log:certify] [log:_derived_values]",
 "Certify Components tab; FC-C2, FC-C11")
item("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Pass",
 "Modal INPUTS read: carbon emission factor = 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' 0.12474 tCO2e/t. Ops Notes H53 is the formula '=IFERROR(SUMPRODUCT(D11:D46,H11:H46)/SUM(D11:D46),\"\")' and returns 0.124740. Recomputing the weighted average independently from the 36 per-tote net-produced masses and per-tote intensities gives 0.1247399142 - agreement to seven decimal places. "
 "Each period's intensity is also the right one for its own totes and comes from that period's own summary: PP#7 totes carry 0.1373671128, which is the Aqueous row of Production Period 7 Summary (row 4, mass of output 73,495 kg); PP#8 totes carry 0.1575553395, the Aqueous row of Production Period 8 Summary (77,076 kg); October 2025 totes carry 0.1110176229, the Aqueous row of the October 2025 Production Period Summary (42,860 kg). The WODO intensities in those same summaries are quite different - 0.753505596, 0.7128290192 and 0.7448717126 - so the Aqueous column was used throughout and no fraction has been cross-wired. [log:certify] [log:ops_notes_totals] [log:pp_summaries] [log:pp_summaries_meta._primary_source_opened] [log:_derived_values]",
 "Certify Pyrolysis INPUTS; FC-C10")
item("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Pass",
 "'INJ-07-2026-W1 Ops Notes.xlsx' is attached in Certify and linked to the 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' datapoint specifically. That is the required evidence standard for production carbon intensity: the Ops Notes shows the production-mass-weighted average across all totes in the injection, and a standalone Production Period Summary is not required. The per-period summaries do exist and corroborate each period's intensity, as recorded in item 7.2. [log:certify.attachment_map] [log:certify.certify_sources_enumeration] [log:pp_summaries]",
 "Certify Sources tab")
item("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", "Pass",
 "Modal INPUTS read: mass = 'QOWV Pyrolysis Mass [Certify input]' 35,759.4 kg. Ops Notes Net Oil Produced (QOWV!D53) = 35,759.40 kg. Exact match. This is the correct basis - net oil in the tote, the quantity actually produced at the pyrolyser - rather than Net Oil Injected (31,437.00 kg), which would have under-charged production emissions by excluding the 4,322.40 kg of measured tote residue. The Ops Notes column header confirms the intent, grouping column D under 'Pyrolysis Emissions Mass'. [log:certify] [log:ops_notes_totals] [log:ops_notes_qowv_tab_cells]",
 "Certify Pyrolysis INPUTS")
item("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", "Pass",
 "Modal INPUTS read: mass 35,759.4 +/-40.82328000000002 kg. Ops Notes J53 = 40.82328 kg. Match to five decimals. The uncertainty is present on the production mass, which matters because this is a dominant input - 4.461 tCO2e against a net of 5.526 tCO2e, roughly 81 % of net - so it does not qualify for the under-1 % omission allowance and its uncertainty is required rather than optional. It covers all 36 weighing events at 1.13398 kg each, matching the batch total rather than a per-period slice, which is right for a single aggregated component spanning all three periods. [log:certify] [log:ops_notes_totals] [log:_derived_values]",
 "Isometric Standard S3.7.3; FC-C12")
item("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
 "The Charm Contents sheet no longer exists as an artifact. Four independent searches establish that no such sheet is produced for any 2026 weekly time-block batch: a Drive title search for 'Charm Contents' returns only the pre-weekly per-batch sheets 5-07, 5-08, 5-10, 3-55 and 3-56; a title-plus-recency search over everything modified since 2026-06-01 returns only unrelated CAD table-of-contents files; enumeration of the batch folder returns five items with no Charm Contents; and the six Certify sources include none. "
 "Its function - the per-Production-Period mass breakdown for the batch - is carried by the Ops Notes QOWV IBC ledger, where column G gives each tote's production period against column D's net oil produced, and that workbook is attached in Certify and linked to the 'QOWV Pyrolysis Mass [Certify input]' datapoint. The mass is therefore evidenced by the document that now holds the content. [log:charm_contents_absence] [log:charm_contents_absence._primary_source_opened] [log:certify.attachment_map]",
 "Certify Sources tab; Document Location Rule")

# ---------------------------------------------------------------- SECTION 8
section("Section 8 - Other")
item("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total >= the transport-process sum?", "Pass",
 "Cleared on the 2026-08-06 re-read. 'BCU - Transport Process' now applies a constant reduction of 6,289 kgCO2e, up from 4,909, evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf'. The only diesel transport-process emission on the removal is 'CO to LA Flatbed Truck Transport Process Emissions - QOWV' at 6.289 tCO2e, so the offset is exact and complete rather than short. "
 "The BCU was resized in step with the corrected flatbed factor - my recomputation of that emission is 6.2885 tCO2e - so it is now sized on the 37,833 kg actually transported at the flatbed factor, rather than on the net-produced mass at the tanker factor as before. "
 "On the Activities figure: the three emitted components recompute to 6.2885 + 0.2349 + 4.4606 = 10.9840 tCO2e, matching Certify's 10.984 t. [log:certify_recheck_2026_08_06T2054Z] [log:certify_recheck_2026_08_06T2054Z._primary_source_opened] [log:_derived_values]",
 "Charm methodology - all diesel transport-process emissions must be BCU-offset")

# ---------------------------------------------------------------- SECTION 9
section("Section 9 - Aqueous Buffering (LCS)")
item("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist (correct mass, correct EF, evidenced)?", "N/A",
 "No LCS use is reported for this batch, so no matching Certify component is required. An every-cell scan of all eight Ops Notes tabs for LCS, liquid calcium, calcium sulfate and buffer returns zero hits, run twice - once against cell values and once against formulas - and the QOWV tab carries no pre-treatment column of any kind. The Summary tab's QOWV row corroborates it, recording Sparging Loss 0.00 kg and Filtration Loss 0.00 kg. The July reporting-period VVB guidance contains no LCS section either. [log:lcs_absence] [log:lcs_absence._primary_source_opened] [log:ops_notes_summary_tab_qowv_row] [log:vvb_guidance]",
 "Ops Notes; FC-C4")

# ---------------------------------------------------------------- SIDEBAR
r += 1
c = ws.cell(row=r, column=1, value="Sidebar Observations (no Pass/Fail status - flagged for attention)")
c.font = BOLD; c.fill = HDR
for col in range(2, 6):
    ws.cell(row=r, column=col).fill = HDR
r += 1

sidebar = [
 "Batch identity. This is the deferred June Week-2 Aqueous batch reported in the July RP. The Ops Notes QOWV tab records the batch id as INJ-06-2026-W2 with week 2026-06-06 to 2026-06-13, while the Certify removal window reads 01-04 Jul 2026 and the file is the W1 Ops Notes; the totes themselves shipped 2025-12-09 and 2025-12-10. The QOWV!B2 cell note explains the deferral. Worth confirming the removal's date window is what Charm intends a verifier to see for oil injected in the week of 6-13 June.",
 "Production-period naming does not connect between the Ops Notes and the verifier guidance. The document is 'VVB Guidance July 1 - July 31' (docs.google.com/document/d/1IQS3Aeqg3MISVjXqzRtYcYmCvEfRo7LNxQgilqdlF0U), section 'Charm Production-Period Documentation Included in This Reporting Period'. That section is what tells a verifier which production periods feed the reporting period and where each one's documentation sits, and it identifies them by month name: 'The earlier Periods (June, August, and September 2025) correspond to the aqueous-fraction (QOWV) oil injected this period'. This batch's Ops Notes identifies its periods as PP#7, PP#8 and October 2025 - two by number, one by month. Nothing in the package maps the PP numbers to calendar months: Production Period 7 Summary.xlsx and Production Period 8 Summary.xlsx name no month, carrying only 'Days in Production Period 7' = 30 and 'Days in Production Period 8' = 31. So a verifier cannot establish whether PP#7 and PP#8 are among the June/August/September entries, and October 2025 - the one label that is itself a month - does not appear in the list at all, while supplying 19 of the 36 totes and 2,148.81 kg of the 4,460.62 kg of production emissions. The October 2025 Production Period Summary does exist and its Aqueous intensity of 0.1110176229 is exactly what the Ops Notes applies, so every number is sourced; what is missing is the pointer. Ask: state the PP-number-to-month mapping in the guidance and add October 2025 to the list. Separately, the same paragraph assigns November-December 2025 to WODO while the sibling WODO batch runs on January-May 2026 periods, so the section looks carried over from the June guidance.",
 "October 2025 Production Period Summary tab name. The file titled 'October 2025 Production Period Summary' contains a tab named 'September PP Summary'. The data is October's, not September's - its Aqueous intensity is 0.1110176228550779 against the September file's 0.12868956697570233 - so the values are right and only the tab label is stale. Worth renaming so a verifier opening the October file is not met with a September heading.",
 "Certify component naming - resolved 2026-08-06. Both transport component titles were renamed from 'CO to LA Tanker Truck ...' to 'CO to LA Flatbed Truck ...', and the process emission-factor datapoint now reads Flatbed Truck to match its source row. The one naming item still open is the embodied emission-factor datapoint, carried as Flag 6.1: it is titled Flatbed Truck while the 2026 tab row supplying its value is Non-Tanker Truck.",
 "Duplicate SGS certificate number. Two PDFs in the Testing folder both carry certificate number SR26-04323.001 with different client ids and different completion times - '07-26-W1-QOWV' completed 21-Jul-2026 11:01 with CHN, and '6-2026-W2' completed 17-Jul-2026 13:58 with physical properties only. Same number, two documents; worth asking SGS to reissue distinctly so the package has one certificate per number.",
 "Scale Tickets subfolder. It contains only the four AECN railcar sets (GRPX5188, GPRX5236, GPRX5107, GPRX5098) and no QOWV tote weighing records. This is not held against the batch - the Ops Notes IBC ledger is the accepted weighing record for tote deliveries - but it means the 36 gross weights and 36 measured empty weights rest on the ledger alone.",
 "Template remnants. QOWV tab rows 56-73 retain sparging-loss template formulas in columns G and H that evaluate to blank. No data and no effect on any total; worth clearing so the used range ends at the totals row.",
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
 "Re-verified live against Certify at 21:50Z on 2026-08-06 after two rounds of Charm corrections. Net 4.943 tCO2e, down from 5.526 at first read, and every component recomputes to what Certify displays: "
 "sequestration 31.437 t x 8.4 %% x 3.667 = 9.6835 t; transport process 37.833 t x 1,201 mi x 0.0001384 = 6.2885 t; transport embodied 1,218.16 mi x 0.0001927908255646154 = 0.2349 t; pyrolysis 35.7594 t x 0.12474 = 4.4606 t; "
 "activities 10.9840 t; net 9.683 + 6.289 - 10.984 - 0.045 = 4.9435 t. The mass chain was clean from the first read and is unchanged: all four Ops Notes totals reconcile to zero delta across 36 totes, the Aqueous measured-loss method is applied with no Standard Loss, every allocation cell is a live formula, and all three production periods reconcile exactly to 4,460.62 kg. "
 "All seven original Fails are cleared. Flatbed process factor 0.1384 applied (5.1); embodied factor revalued to the Non-Tanker figure 0.1928 (6.1, now a naming-only Flag); Ops Notes linked to the embodied-distance datapoint (6.3); BCU resized to 6,289 kgCO2e, exactly offsetting the process emission (8.1); carbon content resolved to 8.40 %% matching the attached certificate (1.1, 4.1, 4.2); and the carbon uncertainty corrected to +/-0.0336 (4.4). Both transport components were renamed Tanker to Flatbed. "
 "Ops Notes attachment verified across all three Week-1 removals, not just this one, by downloading the copy actually attached to each and comparing: QOWV rmv_1KZBTSNE81S0DJT1 (src_1KZCFCEHX1S0VCPY, 6 datapoints), WODO rmv_1KYWMYBJ51S0HH3N (src_1KZCFJ2S71S04E02, 6 datapoints) and AECN rmv_1KYT7WF6Q1S03R7Q (src_1KZCFQ71B1S0DF96, 7 datapoints) all carry byte-identical files (sha256 114d2f9093346dac) reading D20 = 8.40 %% and F20 = 0.0336 %%. "
 "The other six July removals were also checked and each carries its own week's workbook - three W2 removals on the W2 Ops Notes, one W3 on W3, one W4 on W4, and the W4 Kerry removal on Kerry scale tickets and its own COA - so the W1 file appears on no removal outside Week 1. "
 "Two Flags remain, neither affecting a reported number. 1.2: the QOWV!B2 cell note still names 9.20 %% from SR26-03726 as this batch's carbon and assigns 8.4 %% to batch INJ-20260709, contradicting the corrected 8.40 %% three cells away, and it is present in the attached copy a verifier will read; plus the QOWV tab states a target pH range of 2.0-4.0 while recording no measured pH. "
 "6.1: the embodied emission-factor datapoint is titled Flatbed Truck while the 2026 tab row supplying its value is Non-Tanker Truck - right number, wrong label, and the sibling WODO removal names the same factor correctly. "
 "Adversarial self-review completed on all 32 items with every arithmetic result independently recomputed." % (
 counts.get("Pass", 0), counts.get("Flag", 0), counts.get("Fail", 0), counts.get("N/A", 0), total))
c = ws.cell(row=r, column=1, value=summary); c.font = BOLD
c.alignment = Alignment(vertical="top", wrap_text=True)

ws.column_dimensions["A"].width = 7
ws.column_dimensions["B"].width = 52
ws.column_dimensions["C"].width = 9
ws.column_dimensions["D"].width = 100
ws.column_dimensions["E"].width = 32
ws.freeze_panes = ws.cell(row=HEADER_ROW + 1, column=1)

out = "Charm_Aqueous_QOWV_QA_Checklist_INJ-07-2026-W1.xlsx"
wb.save(out)
print("saved", out)
print("counts", counts, "total", total)
