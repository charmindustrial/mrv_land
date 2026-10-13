#!/usr/bin/env python3
"""Build the Charm WODO QA checklist for batch INJ-08-2026-W5."""
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "skills" / "qa" / "batch-qa-aecn" / "scripts"))
from checklist_lib import build_with_validation, BuildAborted  # noqa: E402

LOG = HERE / "batch_INJ-08-2026-W5-WODO_source_reads.json"
OUT = HERE / "Charm_WODO_QA_Checklist_INJ-08-2026-W5.xlsx"

DERIVED = {
    "sum_gross_kg": 20554.00,
    "sum_net_produced_kg": 19517.20,
    "sum_net_injected_kg": 19376.08,
    "sum_standard_loss_kg": 141.12,
    "delta_gross_kg": 0.0,
    "delta_net_produced_kg": 0.0,
    "delta_net_injected_kg": 0.0,
    "uncertainty_expected_kg": 20.41164,
    "uncertainty_per_tote_kg": 1.13398,
    "uncertainty_delta_kg": 0.0,
    "c_uncertainty_expected_pct": 0.2216,
    "c_uncertainty_reported_pct": 0.23647,
    "c_uncertainty_delta_pct": 0.01487,
    "weighted_ci_recomputed": 0.819811,
    "production_emissions_recomputed_kg": 16000.41,
    "seq_recomputed_t": 39.362,
    "process_recomputed_t": 3.416,
    "embodied_recomputed_t": 0.232,
    "pyrolysis_recomputed_t": 16.000,
    "net_recomputed_t": 22.957,
    "batch_share_of_truck": 1.0,
    "batch_mileage_allocation_mi": 1201.00,
    "bcu_kg": 3416,
    "n_totes": 18,
    "lb_per_weighing_event": 2.5,
}

P, F, FL, NA = "Pass", "Fail", "Flag", "N/A"

ROWS = [
    ("SECTION 1 — BATCH FOLDER",),
    ("1.1", "Is there testing in the testing folder for the batch?", P,
     "The RP-level Testing folder holds 'SR26-05246.001', SGS North America certificate, client ID "
     "'8-2026-W5 WODO', product 'Oil - WODO', sampled at Fort Lupton CO, sampled/analysed 02-Sep-2026 "
     "11:53-15:59. Read from the PDF: carbon 55.4 % (m/m) by ASTM D5291 Method C, hydrogen 7.5 %, "
     "nitrogen <0.75 %, kinematic viscosity at 40 C 145.5 cSt, acid number 69 mg KOH/g, density at 15 C "
     "1.195 g/cm3. Carbon content is present and unambiguous. [log:testing]",
     "VR Appendix 1"),
    ("1.2", "Are Ops Notes in the folder and fully completed?", P,
     "'INJ-08-2026-W5 Ops Notes' is in the batch folder, seven tabs. The WODO tab carries a complete "
     "18-tote ledger with no blank cells in any populated row: tag, gross mass, tote mass, net oil "
     "produced, standard loss, net oil injected, production period, carbon intensity, production "
     "emissions and scale uncertainty are all filled for every tote. Every summary cell resolves to a "
     "number with no formula errors: 20554.00, 19517.20, 19376.08, 0.819811, 16000.41. Header block "
     "carries batch ID INJ-08-2026-W5 and week 2026-08-22 to 2026-08-29. [log:ops_notes_totals, totes]",
     "VR Appendix 1"),
    ("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", P,
     "Under the weekly time-block schema the shipment tracker is the Ops Notes tab 'WODO Shipments & EE "
     "Allocation'. It covers this batch completely: shipping order COLA_33, 18 totes on the truck, 18 "
     "batch-relevant totes (100% batch share), Charm CO to Basco LA one-way distance 1,201 mi, and a full "
     "EE allocation row with batch share, mileage and allocated miles. [log:shipment_allocation]",
     "VR Appendix 1"),

    ("SECTION 2 — OPS NOTES",),
    ("2.1", "Is the 'Total Mass Transported' value correctly computed as the sum of the gross weight of all totes?", P,
     "Ops Notes WODO tab reports 20554.00 kg at the TOTAL row, a live SUM over the 18-tote Gross Mass "
     "column. Summing the 18 ledger rows independently reproduces 20554.00 kg exactly, a delta of 0.0 kg. "
     "This is also the exact value Certify's Transport Process component uses for Mass of Load (see 5.3). "
     "[log:_derived_values.sum_gross_kg, _derived_values.delta_gross_kg, ops_notes_totals, totes]",
     "Ops Notes WODO TOTAL row"),
    ("2.2", "Is the 'Total Oil Produced' value correctly computed as the sum of the net weight of oil in tote for all totes (gross minus tare per tote)?", P,
     "Ops Notes reports 19517.20 kg, each per-tote Net Oil Produced cell equal to Gross minus a uniform "
     "57.60 kg tote tare. Summed independently across all 18 totes: 19517.20 kg against the reported "
     "19517.20, a delta of 0.0 kg. This exact figure is also what Certify's Pyrolysis component uses as "
     "its mass basis (see 7.4). [log:_derived_values.sum_net_produced_kg, "
     "_derived_values.delta_net_produced_kg, totes]",
     "Ops Notes WODO TOTAL row"),
    ("2.3", "Is the 'Total Oil in Batch' value correctly computed (WODO: net-in-tote less Standard Loss per tote)?", P,
     "Reported 19376.08 kg. Each per-tote figure is Net Oil Produced minus a Standard Loss of 7.84 "
     "kg/tote, a cell labelled 'WODO Standard Loss (kg/tote), 2026 = Mean + 1SD', hyperlinked to a 'Tote "
     "Loss Dataset' -- a live, dataset-derived, conservative 2026 figure, distinct from and not the "
     "previously-disapproved fixed 4.73 kg/tote value. Standard Loss IS applied, correctly -- this is the "
     "WODO branch, not Aqueous. Summed independently: 19517.20 - (7.84 x 18) = 19517.20 - 141.12 = "
     "19376.08 kg, a delta of 0.0 kg, and the sheet's own Standard Loss column total is 141.12 kg, "
     "matching. [log:_derived_values.sum_net_injected_kg, _derived_values.delta_net_injected_kg, "
     "_derived_values.sum_standard_loss_kg, ops_notes_totals, standard_loss_methodology]",
     "Ops Notes WODO TOTAL row / v1.2 6.5"),
    ("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", P,
     "Per-tote Scale Uncertainty is 1.13398 kg (2.5 lb x 0.453592 kg/lb), times 18 totes = 20.41164 kg. "
     "This reconciles exactly against Certify's reported Mass of Product / Mass of Load uncertainty of "
     "+/-20.41164 kg on both the Sequestration and Transport Process components. This is the Charm "
     "per-tote weighing precision, not AECN's 72.57 kg per-truck figure. [log:_derived_values.uncertainty_expected_kg, "
     "_derived_values.uncertainty_per_tote_kg, _derived_values.uncertainty_delta_kg, "
     "_derived_values.lb_per_weighing_event, _derived_values.n_totes, ops_notes_totals]",
     "Isometric Standard S3.7.3"),

    ("SECTION 3 — BIO-OIL SHIPMENT TRACKER",),
    ("3.1", "Are totes for the RP correctly identified?", P,
     "All 18 WODO totes for the week are identified on the 'WODO Shipments & EE Allocation' tab as "
     "batch-relevant against shipping order COLA_33 (18 totes on truck, 18 batch-relevant, 100% batch "
     "share) -- the same 18 tags enumerated on the WODO ledger tab. [log:shipment_allocation, totes]",
     "Ops Notes WODO / allocation tab"),
    ("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", P,
     "The allocation tab's batch-relevant-tote count (18) matches the WODO tab's own 18-tote ledger "
     "exactly -- this is a single-shipment batch (COLA_33 = 18 totes, 'Total-on-truck counted from BGN "
     "master Shipment tracker' per the sheet's own note), with no other fraction sharing the truck. "
     "[log:shipment_allocation, totes]",
     "WODO Shipments & EE Allocation tab"),
    ("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", P,
     "Every computed cell was opened and its formula read directly, not inferred from appearance. Batch "
     "Share of Truck = '=IFERROR(D12/C12,\"\")'. Allocated Miles = '=IFERROR(E12*F12,\"\")'. Both formulas "
     "reference the tote-count and mileage input cells; neither is a typed constant. The only hard value "
     "in the chain is the one-way distance itself (1201), an input rather than a computed output, "
     "evidenced by the routing map. [log:shipment_allocation]",
     "Auditability"),
    ("3.4", "Are computed outputs computed correctly?", P,
     "Reproduced independently against the spec. Batch Share of Truck = 18 batch-relevant totes / 18 "
     "totes on truck COLA_33 = 100%, matching the sheet. Allocated Miles = 100% x 1201 = 1201.00 mi, "
     "matching exactly. Distance is one-way throughout with no round-trip doubling, correct for a "
     "per-batch truck-share allocation. [log:_derived_values.batch_share_of_truck, "
     "_derived_values.batch_mileage_allocation_mi, shipment_allocation]",
     "WODO Shipments & EE Allocation tab"),
    ("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", P,
     "The allocation tab's batch-relevant-tote count derives from the same single shipping order "
     "(COLA_33) that carries all 18 WODO-fraction totes on the WODO ledger tab -- there is no second, "
     "independently-maintained tote roster to drift out of sync with, and the WODO tab is the single "
     "source of truth for tag, fraction, gross mass and production period for all 18 totes. "
     "[log:shipment_allocation, totes]",
     "WODO Shipments & EE Allocation tab vs Ops Notes"),

    ("SECTION 4 — CERTIFY: INJECTION SEQUESTRATION",),
    ("4.1", "Does the C content in the testing match the C content in the Sequestration component?", P,
     "Certificate SR26-05246.001 reports carbon 55.4 % (m/m) by ASTM D5291 Method C, read from the PDF. "
     "The Certify sequestration component modal shows Carbon Content of Product 55.4 %. Exact match. "
     "[log:testing, certify.components.0]",
     "Certify cmp_1M1KP21WZ1S0PX2T"),
    ("4.2", "Is the C content in the Sequestration component properly evidenced (test copy plus Ops Notes copy)?", P,
     "The carbon content datapoint shows 2 sources in the component modal, expanded and confirmed as "
     "'INJ-08-2026-W5 Ops Notes.xlsx' and '8-2026-W5 WODO, SR26-05246.pdf' -- both required evidence "
     "types, linked to the specific datapoint rather than only at removal level. Confirmed independently "
     "from the Sources tab (9 sources total). [log:certify.components.0, certify.certify_sources_enumeration]",
     "Certify Sources tab"),
    ("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS: Mass of Product 19,376.08 kg plus or minus 20.41164 kg. "
     "Matches the Ops Notes uncertainty (20.41164 kg = 1.13398 kg x 18 totes) exactly. "
     "[log:certify.components.0, _derived_values.uncertainty_expected_kg, _derived_values.uncertainty_per_tote_kg]",
     "Certify cmp_1M1KP21WZ1S0PX2T INPUTS"),
    ("4.4", "Does the C content have the appropriately computed 0.4 % relative uncertainty?", F,
     "Certify shows Carbon Content 55.4 plus or minus 0.23647 %. Recomputed: 0.004 relative uncertainty "
     "times the 55.4 % carbon content should give 0.2216 percentage points (0.004 x 55.4 = 0.2216). The "
     "reported figure (0.23647) is 0.01487 percentage points higher than expected -- about 6.7% relative "
     "overstatement, well outside the +/-0.001-absolute / +/-0.1%-relative match tolerance. This does not "
     "reconcile to the documented 0.4%-relative convention on any obvious alternate basis (it is not a "
     "simple root-sum-square of 0.4% with another stated Charm uncertainty component either). A verifier "
     "could not confirm this figure ties to the stated methodology as submitted. "
     "[log:certify.components.0, _derived_values.c_uncertainty_expected_pct, "
     "_derived_values.c_uncertainty_reported_pct, _derived_values.c_uncertainty_delta_pct]",
     "Certify cmp_1M1KP21WZ1S0PX2T INPUTS"),

    ("SECTION 5 — CERTIFY: TRANSPORT PROCESS EMISSIONS",),
    ("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", P,
     "The component modal shows 0.1384 kgCO2e per tonne-mile, the current 2026 corrected value (fuel-use "
     "EF updated 0.1143 -> 0.1384 kg/t-mi per the reporting-period VVB guidance and Standard Emission "
     "Factors 2026 tab). Correctly the flatbed row, not tanker. [log:certify.components.1, standard_efs_2026]",
     "Standard EFs 2026 tab"),
    ("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", P,
     "Distance in Certify is 1,201 mi ('Distance from Miniforge CO to Basco'). The attached routing map "
     "shows three Google Maps route options from Fort Lupton CO to Basco LA; 1,201 mi is the longest of "
     "the options displayed (consistent with the 1,201 mi longest-route figure used on every other WODO "
     "batch this year for the same origin/destination pair). [log:certify.components.1, "
     "certify.certify_sources_enumeration]",
     "CO to Basco Routing Map.png"),
    ("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", FL,
     "The value is right and the label is wrong. Mass of Load in Certify is 20,554 kg, exactly the Ops "
     "Notes Total Mass Transported of 20554.00 kg -- the gross basis including tote tare, not Total Oil "
     "Produced (19,517.20) or Total Oil in Batch (19,376.08). But the datapoint carrying it is titled "
     "'WODO Trip Count Source' -- a name that describes a trip count, not a mass. Flag rather than Fail "
     "because the quantity feeding the calculation is correct and the transport-process emission "
     "reproduces exactly (20.554 t x 1,201 mi x 0.1384 kgCO2e/t-mi = 3.416 t, matching Certify). This is "
     "the same recurring mass-of-load naming defect seen on essentially every WODO/QOWV batch this year "
     "(e.g. INJ-08-2026-W2 'QOWV Trip Count Source' on a WODO removal) -- worth fixing at the Mangrove/ops "
     "template level. [log:certify.components.1, _derived_values.process_recomputed_t, ops_notes_totals]",
     "Certify cmp_1M1KP21WZ1S0AHYF"),
    ("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", P,
     "The Mass of Load datapoint shows 1 source: 'INJ-08-2026-W5 Ops Notes.xlsx', linked to the specific "
     "datapoint. [log:certify.components.1, certify.certify_sources_enumeration]",
     "Certify Sources tab"),
    ("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", P,
     "Read from the component modal INPUTS: Mass of Load 20,554 kg plus or minus 20.41164 kg -- identical "
     "to the Mass of Product uncertainty on the Sequestration component, correct since it is the same 18 "
     "totes weighed once each. [log:certify.components.1, _derived_values.uncertainty_expected_kg]",
     "Certify cmp_1M1KP21WZ1S0AHYF INPUTS"),

    ("SECTION 6 — CERTIFY: TRANSPORT EMBODIED EMISSIONS",),
    ("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", P,
     "The component modal shows 0.19279 kgCO2e per mile, the current 2026 corrected value (embodied EF "
     "updated 0.23756 -> 0.19279 kg/mi per the reporting-period VVB guidance and Standard Emission "
     "Factors 2026 tab). Correctly the non-tanker row, and the datapoint label reads 'Emissions Factor - "
     "Vehicle Embodied Emissions - Non-Tanker Truck' -- label and value agree. [log:certify.components.2, standard_efs_2026]",
     "Standard EFs 2026 tab"),
    ("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", P,
     "Certify aggregate distance ('Aggregate Distance Transported CO to LA - WODO') is 1,201 mi. The "
     "allocation tab's Allocated Miles resolves to 1,201.00 mi (100% batch share x 1,201 mi one-way) -- "
     "exact match. This batch takes the whole truck (18 of 18 totes), so the allocated distance equals "
     "the full one-way distance rather than a fractional share. [log:certify.components.2, "
     "_derived_values.batch_mileage_allocation_mi, shipment_allocation]",
     "Certify cmp_1M1KP21WZ1S0Y6T4 INPUTS"),
    ("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", F,
     "The 'Aggregate Distance Transported CO to LA - WODO' datapoint carries exactly ONE source: 'CO to "
     "Basco Routing Map.png'. The Ops Notes -- which under the weekly time-block schema plays the "
     "Shipment Tracker role and is what actually derives the 1,201.00 mi allocation (100% batch share x "
     "1,201 mi one-way, verified live at 3.3/3.4) -- is NOT linked to this specific datapoint, even though "
     "it IS linked to five other datapoints on this same removal (Mass of Injectant, Mass of Load, Carbon "
     "Content, Production CI, Production Mass). This is a real evidence-attachment gap, not a values "
     "problem: the reported number is correct and independently reproduces from the Ops Notes tracker, "
     "but a verifier working only from what is attached in Certify cannot see the tracker computation "
     "behind it, only the raw map. The equivalent datapoint on the prior WODO batch (INJ-08-2026-W2) "
     "carried 2 sources at this same slot (routing map AND Ops Notes) -- this batch is missing the second. "
     "No standalone 'Charm Contents' sheet exists for any 2026 weekly WODO batch (its role is folded into "
     "Ops Notes), so the practical requirement here is Ops Notes + map; only the map is present. "
     "[log:certify.attachment_map, certify.certify_sources_enumeration, shipment_allocation]",
     "Certify Sources tab"),

    ("SECTION 7 — CERTIFY: PRODUCTION EMISSIONS",),
    ("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", P,
     "The batch draws on four production periods: February 2026 (3 totes, CI 0.849896), March 2026 (6 "
     "totes, CI 0.790065), June 2026 (1 tote, CI 1.110536) and the H2 2026 blended/rolling CI (8 totes "
     "produced July 2026, CI 0.795241). All four are captured in a single aggregated component, "
     "'Pyrolysis - Charm WODO PP Emissions' at 16.000 tCO2e, carrying a production-mass-weighted blended "
     "intensity of 0.819811 that reconciles to the per-tote sum: Ops Notes total Production Emissions = "
     "16000.41 kg = 16.000 t against Certify's 16.000 t. No period is omitted; aggregating periods into "
     "one weighted component is not a finding. [log:production_periods, "
     "_derived_values.production_emissions_recomputed_kg, certify.components.3]",
     "Certify Components tab"),
    ("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", P,
     "Certify carries 0.819811 tCO2e per tonne. The Ops Notes weighted average is 0.819811 (= total "
     "Production Emissions / total Net Oil Produced = 16000.41 / 19517.20). Exact match to full displayed "
     "precision. Each production period's CI is applied to the right totes, confirmed by opening the "
     "per-tote CI lookup formulas: March 2026 totes reference the March 2026 lookup row (0.790065), the "
     "single June 2026 tote references the June 2026 row (1.110536), the 8 July-2026-and-later totes "
     "reference the blended H2 2026 row (0.795241), and the 3 February 2026 totes reference the February "
     "2026 row (0.849896) -- no cross-wiring between fractions/periods. [log:_derived_values.weighted_ci_recomputed, "
     "ops_notes_totals, production_periods, certify.components.3]",
     "Ops Notes WODO TOTAL row"),
    ("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", P,
     "The 'WODO Tote - Carbon Intensity' datapoint shows 4 sources: the V2 mass-weighted CI workbook, the "
     "February and March 2026 Production Period Summaries, and 'INJ-08-2026-W5 Ops Notes.xlsx' -- the Ops "
     "Notes weighted average is attached, which is the required evidence standard for Charm production "
     "intensity (a standalone PP Summary is not required for every period). [log:certify.components.3, "
     "certify.certify_sources_enumeration]",
     "Certify Sources tab"),
    ("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?", P,
     "Certify mass is 19,517.2 kg ('WODO Tote - Mass (Gross-Tote) for pyrolysis'). The Ops Notes sum of "
     "Net Oil Produced across all 18 totes is 19517.20 kg, a delta of 0.0 kg. The component correctly "
     "uses net-in-tote (produced mass), not net-in-injection-batch (19,376.08) -- production emissions "
     "attach to what was produced, not to what survived transfer. [log:_derived_values.sum_net_produced_kg, "
     "_derived_values.delta_net_produced_kg, certify.components.3]",
     "Certify cmp_1M1KP21WZ1S0CT8R INPUTS"),
    ("7.5", "Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?", P,
     "Read from the component modal INPUTS: Mass 19,517.2 kg plus or minus 20.41 kg, matching the "
     "expected 1.13398 kg per tote across 18 totes (20.41164, displayed rounded to 20.41). Uncertainty is "
     "present on this dominant input -- pyrolysis is 69.69% of Activities and roughly 40% of gross "
     "sequestration, well above the negligible-input threshold that would qualify for a v1.2 6.5 omission "
     "carve-out. [log:certify.components.3, _derived_values.uncertainty_expected_kg]",
     "v1.2 6.5.1"),
    ("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", P,
     "No Charm Contents sheet exists for this batch or for any WODO batch under the current weekly "
     "time-block schema (confirmed absent from both the Drive batch folder -- top-level contents: "
     "Completed QA Checklists, Scale Tickets, Testing, Ops Notes only -- and Certify's 9 enumerated "
     "Sources this session). The per-period mass breakdown it used to carry now lives directly in the Ops "
     "Notes WODO tab (Production Period column against Net Oil Produced column), and the Ops Notes is "
     "attached to this mass datapoint. Same basis accepted on every prior 2026 weekly WODO/Aqueous batch. "
     "[log:certify.charm_contents_present, certify.charm_contents_note, certify.components.3]",
     "VR Appendix 1"),

    ("SECTION 8 — OTHER",),
    ("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total meet or exceed the transport-process sum?", P,
     "There is one diesel transport-process emission on this removal, the flatbed leg at 3.416 tCO2e, "
     "and it is offset exactly. Reductions carries a 'BCU - Transport Process' Constant CO2 reduction of "
     "3,416 kgCO2e, evidenced by 'Charm-RetirementCertificate-RD-EACs-20251218.pdf' -- opened directly: a "
     "Transport Emission Reduction Certificate (TERC), Certificate of Retirement, Retiring Organization "
     "Amazon.com Services LLC, On Behalf Of Charm Industrial Inc, Date of Retirement Dec 18 2025, Vintage "
     "Year 2024, Commodity Type Renewable Diesel TERCS -- a real, dated retirement certificate drawn down "
     "incrementally across weekly batches (same shared-inventory pattern as every other 2026 WODO/QOWV "
     "batch). Recomputing the process emission from primary sources gives 20.554 t x 1,201 mi x 0.1384 "
     "kgCO2e/t-mi = 3.416 t, so the 3,416 kgCO2e offset equals it exactly. Embodied emissions are "
     "correctly not offset. [log:_derived_values.bcu_kg, _derived_values.process_recomputed_t, "
     "retirement_certificate, certify.components.4]",
     "Certify cmp_1M1KP6QEJ1S01R8D"),

    ("SECTION 9 — AQUEOUS BUFFERING (LCS)",),
    ("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist?", NA,
     "Not applicable to a WODO batch -- LCS is an aqueous pre-treatment. The WODO tab and WODO Shipments "
     "& EE Allocation tab carry no LCS/calcium/buffer column or reference, and all 5 Certify components "
     "were enumerated with no LCS component among them. [log:certify.components]",
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
    ws.title = "WODO QA INJ-08-2026-W5"

    ws.cell(row=1, column=1, value="Charm WODO Injection Batch QA Checklist").font = TITLE
    meta = [
        ("Batch ID", "INJ-08-2026-W5 (WODO)"),
        ("Reporting Period", "Certify removal window 23 Aug 2026 to 29 Aug 2026; Ops Notes injection week 2026-08-22 to 2026-08-29"),
        ("Reviewer", "Claude (MRV QA agent)"),
        ("Date", "2026-09-10"),
        ("Injection Site", "Basco 6, Louisiana (Class V UIC)"),
        ("Oil Type", "WODO (Charm-produced, Fort Lupton CO), 18 IBC totes"),
        ("Production Periods", "February 2026 (3 totes, CI 0.849896); March 2026 (6 totes, CI 0.790065); June 2026 (1 tote, CI 1.110536); H2 2026 blended CI 0.795241 (8 totes produced Jul 2026)"),
        ("Certify Removal ID", "rmv_1M1KP21WZ1S0TQPG"),
        ("Certify Net", "22.957 tCO2e (displayed 22.96) = Sequestrations 39.363 + BCU 3.416 - Activities 19.648 - Uncertainty Discount 0.174"),
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
        "Tote tare mass (57.60 kg) is a uniform hardcoded constant across all 18 totes, not an "
        "individually scale-measured value, per the ledger header 'tote tag mass is authoritative'. This "
        "is the standard IBC-tote convention Charm has used all year for WODO/Aqueous totes, but it was "
        "not independently re-derived against a manufacturer spec or scale reading this session -- worth "
        "a periodic spot-check that 57.60 kg remains the correct tare for the current tote fleet.",

        "The June 2026 tote (301251) carries a notably higher production CI (1.110536 tCO2e/t) than the "
        "surrounding months (0.79-0.85). Verified this is a genuine, independently-linked monthly PP "
        "Summary figure (own 'PP Summary' hyperlink in the Ops Notes lookup table), not a data-entry "
        "error or row-mapping mistake -- confirmed by reading the underlying formula cell references "
        "directly rather than trusting the on-screen row alignment.",

        "The BCU is drawn from a single large Renewable Diesel Transport Emission Reduction Certificate "
        "(TERC) retired by Amazon.com Services LLC on behalf of Charm Industrial, Dec 18 2025, vintage "
        "2024 -- the same shared-inventory certificate pattern used across every other 2026 WODO/QOWV "
        "batch. Consistent with the EAC inventory monitor's drawdown tracking; no new finding.",

        "An unintended edit was made to cell N1 of the live INJ-08-2026-W5 Ops Notes Google Sheet during "
        "this session (a temporary formula typed to cross-check lookup-table row alignment) and was "
        "undone via Ctrl+Z in the same turn; N1 is confirmed empty and no ledger/lookup content was "
        "altered. Flagging for transparency since Drive's file-modification metadata will show this "
        "session touched the file.",
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
        "sequestration 19,376.08 kg x 55.4% x 3.667 = 39.362 t (Certify 39.363 t); transport process "
        "20.554 t x 1,201 mi x 0.1384 kg/t-mi = 3.416 t; transport embodied 1,201 mi x 0.19279 kg/mi = "
        "0.232 t; pyrolysis 19.5172 t x weighted-avg CI 0.819811 = 16.000 t; net closes at 22.957 t "
        "against Certify's 22.96 t displayed (uncertainty discount 174 kg). Both emission factors match "
        "the live 2026 Standard EFs tab and the reporting-period VVB-guidance corrected values. All Ops "
        "Notes totals reconcile to a zero delta across the 18-tote ledger. The BCU offsets the flatbed "
        "transport-process emission exactly (3,416 kg = 3.416 t) via a verified, dated Renewable Diesel "
        "TERC retirement certificate. TWO FAILS: item 4.4 -- the Carbon Content uncertainty in Certify "
        "(+/-0.23647%) does not reconcile to the documented 0.4%-relative convention (expected +/-0.2216%, "
        "a 6.7% relative overstatement) -- needs Garrett to check how that figure was entered. Item 6.3 -- "
        "the Aggregate Distance datapoint carries only the routing map as evidence; the Ops Notes (which "
        "plays the Shipment Tracker role and actually derives the 1,201 mi allocation) is not linked to "
        "this specific datapoint, unlike five other datapoints on this same removal and unlike the "
        "equivalent datapoint on the prior WODO batch. The value itself is correct and independently "
        "reproduces from the Ops Notes tracker -- this is an evidence-attachment gap, not a valuation "
        "error. ONE FLAG: item 5.3, the Transport Process Mass-of-Load datapoint is titled 'WODO Trip "
        "Count Source', a name that describes a trip count rather than a mass -- the value (20,554 kg) is "
        "correct and reproduces exactly; this is the same recurring naming-hygiene defect seen on "
        "essentially every WODO/QOWV batch this year."
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
