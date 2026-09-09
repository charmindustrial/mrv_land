import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
FAIL_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
FLAG_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
FLAG_FONT = Font(color="996600")
NA_FONT = Font(italic=True, color="808080")
BOLD = Font(bold=True)

# ROWS: tuples of (item_no, description, status, evidence, verifier_ref)
# status in {"HEADER","SUBHEADER","Pass","Fail","Flag","N/A"}
ROWS = []

def hdr(text):
    ROWS.append(("", text, "HEADER", "", ""))

def sub(text):
    ROWS.append(("", text, "SUBHEADER", "", ""))

def row(item, desc, status, evidence, ref):
    ROWS.append((item, desc, status, evidence, ref))

# ===== Header info rows handled separately in header block =====

hdr("1. Batch Folder Completeness")
row("1.1", "Batch folder exists with correct naming", "Pass",
    "Drive folder title 'INJ-08-2026-W2' (weekly time-block naming convention) contains Completed QA Checklists, Scale Tickets, Testing subfolders, and Ops Notes. [log:ops_notes.file]",
    "VR Appendix 1")
row("1.2", "Scale Tickets subfolder present and populated", "Pass",
    "11 full+empty CAT scale ticket pairs (22 PDFs) opened directly via Drive fileIds embedded in Ops Notes hyperlink formulas -- all readable, all values legible. [log:scale_tickets.pairs]",
    "VR Appendix 1")
row("1.3", "Testing subfolder present with all required lab results", "Pass",
    "Testing subfolder contains '08-2026-W2 AECN - 08-2026 W2 QOWV.pdf' (SGS CoA SR26-04824.001/.002) and '8-2026-W2 WODO - SR26-04856.001.pdf'. AECN CoA opened and read in full. [log:lab_results]",
    "VR Appendix 1")
row("1.4", "Ops Notes spreadsheet present and complete", "Pass",
    "'INJ-08-2026-W2 Ops Notes.xlsx' present with Summary, AECN Rail, WODO, AECN Truck, QOWV, Kerry tabs all populated for the week; AECN Rail tab fully read incl. formulas and cell comments. [log:ops_notes.aecn_rail_tab]",
    "VR Appendix 1")
row("1.5", "Injection site confirmed as Basco 6 -- no references to deprecated Vaulted", "Pass",
    "All 12 BOLs route AECN Port-Cartier QC -> SOPOR (Baie-Comeau); Ops Notes 'Opel->Basco' legs and Certify components consistently name Basco/Opelousas; no Vaulted references found in any opened document (Ops Notes all 8 tabs, all 12 BOLs, lab CoA -- searched and documented). [log:bols.all_destinations_confirmed_sopor, global_evidence]",
    "verify BOLs, Ops Notes, Certify")

hdr("2. Scale Tickets & Mass Determination")
row("2.1", "Empty and full scale ticket images present for each truckload (11 offload pairs this week)", "Flag",
    "All 22 tickets opened and legible via the Drive fileIds embedded in Ops Notes' hyperlink formulas (Document Location Rule satisfied: present in Drive, reachable through the attached Ops Notes). Two labeling issues found on otherwise-correct tickets: SHPX215070 offload_3 empty ticket prints commodity field 'GPRX5240 LOAD 2' instead of a SHPX215070 label (rig matches, mass ties exactly); TILX200228 offload_4 both tickets print railcar as 'TXLI 200228' (letter transposition of TILX200228, internally consistent between the pair). Content correct in both cases -- hygiene only. Separately: none of the 22 scale-ticket PDFs is uploaded as its own standalone file in Certify Sources (13 sources enumerated, none matches a ticket/weigh filename pattern) -- only Ops Notes carries them, via hyperlink. A verifier can still reach every ticket through the attached Ops Notes, but the AECN evidence matrix (validated on INJ-06-2026-W1) expects scale-ticket files directly attached to Mass of Injectant alongside Ops Notes. FLAG for Garrett to direct-attach the ticket PDFs to Certify for a cleaner evidence chain. [log:scale_tickets.pairs, certify.attachment_map]",
    "VR Sec 5.1")
row("2.2", "Dates within 2 weeks of injection", "Pass",
    "All 22 ticket dates fall 2026-07-29 through 2026-08-06, within 2 weeks of the 2026-08-08 injection completion date. [log:scale_tickets.all_dates_within_2_weeks_of_injection]",
    "VR Sec 3.5")
row("2.3", "Tractor and trailer numbers match between empty and full tickets (all 11 pairs)", "Fail",
    "10 of 11 pairs match cleanly. SHPX215090 offload_2: full ticket (1124426216328) prints trailer 'RL192'; empty ticket (1312226217833) prints trailer 'KL 192'. Tractor CH2 matches both, but trailer IDs differ. No VVB Guidance (August 1-31 RP) documents a substitution or known-variant covering this pairing -- guidance only lists a Week-1 GPRX5240 substitution. Cannot be confirmed as OCR/print variant vs a genuine rig swap from the images alone. [log:scale_tickets.pairs]",
    "VR Sec 5.1")
row("2.4", "Net mass (full minus empty) correctly calculated in Ops Notes", "Pass",
    "All 11 offloads' independently recalculated net mass ((Full-Empty)x0.453592) match Ops Notes F-column to the cent, e.g. offload_1: (72,180-28,600)x0.453592=19,767.53kg vs Ops Notes 19,767.54kg. [log:scale_tickets.pairs, ops_notes.aecn_rail_tab.section3_offload_table]",
    "VR Sec 5.1")
row("2.5", "Injectate mass uses conservative value per rail last-offload conservatism policy", "Pass",
    "SHPX215090 (FULL railcar, last offload=offload_4 this week): raw scale-ticket sum (78,344.41kg) exceeds BOL aggregate (78,140.00kg) by 204.41kg; back-calc correctly deducts exactly this excess via the J-column formula on the last (highest-row) offload for that railcar. Verified: MAX(0, 78,344.41-78,140.00)=204.41kg matches Ops Notes J39 exactly. Other 3 railcars' raw sums do not exceed their BOL aggregates -- no back-calc triggered, correctly left at 0. [log:ops_notes.aecn_rail_tab.section3_offload_table]",
    "GHG Stmt Sec C")
row("2.6", "1.29% sparging deduction applied to AECN input mass", "Pass",
    "Ops Notes constant O5=0.0129; per-row Sparging Loss = (NetMass-UncertaintyAdj)x0.0129 for all 11 rows. Independently summed the 11 row-level values: 255.00+245.87+251.37+246.46+263.08+250.91+260.97+233.05+246.69+254.53+241.66 = 2,749.59kg, matching the Ops Notes aggregate 2,749.60kg to the cent (1-cent rounding). [log:ops_notes.aecn_rail_tab.constants, ops_notes.aecn_rail_tab.section4_rollup_row52, ops_notes.aecn_rail_tab.section3_offload_table, _derived_values.sparging_loss_recalc_detail]",
    "GHG Stmt Sec C")
row("2.7", "All mass values consistent across scale tickets, Ops Notes, COBB, and Certify", "Pass",
    "Pyrolysis/transport basis: SUM of 11 offloads' raw net mass = 213,351.53kg = Certify 'Bio-Oil Mass - AECN via Rail' 213.352t EXACT. Injectate (MOBI) basis: 209,987.25kg = Certify 'Mass of Injectant' 209.987t EXACT. COBB matches Ops Notes on 10 of 11 rows exactly; 1 row (SHPX215090 offload_4) diverges by exactly the 204.41kg back-calc adjustment -- a documented COBB-side provenance nuance that does not affect the Certify-reported figures (verified Certify uses the raw unadjusted sum for pyrolysis/transport basis). [log:ops_notes.aecn_rail_tab.section4_rollup_row52, cobb.rows, certify.component_modals_opened]",
    "VR Sec 5.1")

hdr("3. Bills of Lading & Transportation")
row("3.1", "Truck BOL(s) present for each shipment (3 BOLs per railcar x 4 railcars = 12)", "Pass",
    "All 12 loading BOLs (2418-R,2419-R,2423-R,2421-R,2422-R,2420-R,2412-R,2413-R,2414-R,2424-R,2425-R,2426-R) opened and read in full -- all present in Drive. [log:bols.records]",
    "VR Appendix 1")
row("3.2", "Truck BOLs from AECN present, destination = SOPOR railyard", "Pass",
    "All 12 BOLs' 'Ship To' field reads 'CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau QC' -- confirmed SOPOR railyard, not Basco. [log:bols.all_destinations_confirmed_sopor]",
    "VR Appendix 1")
row("3.3", "BOL mass (railcar-level aggregate) >= railcar received mass", "Pass",
    "Per-railcar BOL sums tie exactly to Ops Notes Total Loaded: SHPX215082 26.07+26.01+26.05=78.13MT; SHPX215090 26.09+26.05+26.00=78.14MT; TILX200228 26.06+25.81+26.11=77.98MT; SHPX215070 25.83+25.86+25.80=77.49MT -- all EXACT matches. [log:bols.bol_aggregate_check]",
    "VR Sec 3.5")
row("3.4", "Origin and destination correct on BOL (AECN Port-Cartier -> SOPOR Baie-Comeau)", "Pass",
    "All 12 BOLs 'From' field reads 'BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec' -- confirmed AECN origin. [log:bols.all_origins_confirmed_aecn_port_cartier]",
    "PDD Sec A")
row("3.5", "Transportation distance consistent with known AECN rail route (3 legs, allocated where required)", "Fail",
    "Math and methodology are correct: AECN->SOPOR Aggregate Distance 883mi (Ops Notes EE Totals sum 882.56mi) via mass-fraction allocation, single-leg basis 107.5mi x3 trucks. SOPOR->Opelousas: PROCESS component uses full 2,199mi single-leg distance x total mass (mathematically equivalent to per-railcar allocation since every railcar traverses the complete leg); EMBODIED component uses the allocated/fractional 6,019.85mi (Ops Notes sum) x per-mile EF. Both independently recalculated to Certify's exact displayed values (12.156t process, 0.187t embodied). Opelousas->Basco: non-allocated 43mi ties to 'Distance from Opelousas to B6' and 'Allocated Distance Opelousas to B6' (944mi, Ops Notes sum 943.80mi). HOWEVER: opened every '+N more' popover on the 3 route-map PNGs in Certify Sources and confirmed none of the 3 Allocated/Aggregate Distance datapoints (Aggregate Distance AECN to Sopor, Allocated Distance Opelousas to B6, Allocated Distance Sopor Quebec to Opelousas) is linked to Ops Notes -- only to the static route-map image. Ops Notes contains the allocation-fraction math (mass shares across railcars/offloads) that actually produces these figures, and per the required-evidence matrix (Allocated distances -> Ops Notes + Maps) that linkage is missing. Same gap already registered as a FAIL on sister batches INJ-08-2026-W1 and INJ-07-2026-W4 ('Allocated distance datapoints linked only to route-map images, not Ops Notes'). Values are correct; the verifier-facing evidence chain for the allocation math itself is incomplete. [log:certify.component_modals_opened, ops_notes.aecn_rail_tab.ee_totals_row48, certify.attachment_map_note]",
    "Transport Emissions Acctg v1.1")
row("3.6", "Transport mode = tanker truck (AECN->SOPOR, Opel->Basco) and railcar (SOPOR->Opelousas)", "Pass",
    "Certify Components confirms 6 transport components: AECN->SOPOR Tanker Truck (process+embodied), SOPOR->Opelousas Rail (process+embodied), Opelousas->Basco Tanker Truck (process+embodied) -- correct mode per leg. [log:certify.components_breakdown.removal_activities_transport]",
    "Certify Datapoints")
row("3.7", "Billing documents present and consistent with BOL shipment details", "Flag",
    "11 of 12 BOLs print a clean, internally-consistent 'Invoice / BOL /' number. BOL loaded into TILX200228 on 2026-07-06 for 26.11 MT is printed on the physical document as '2314-R' -- a digit transposition of the correct '2414-R' referenced everywhere else (Ops Notes Origins Ledger, COBB BOL_number field). Content (mass, dates, routing) fully consistent with the 2414-R entry; only the printed reference number has a typo. Same typo pattern was previously flagged on the INJ-08-2026-W1 registry entry, suggesting a recurring vendor-side documentation quirk rather than a new error. [log:bols.records]",
    "VR Appendix 1")

hdr("4. Bio-Oil Composition & Testing")
row("4.1", "CHN analysis PDF(s) present in Testing subfolder, correct batch/sample ID", "Pass",
    "SGS Certificate of Analysis SR26-04824.001, Client ID '08-2026-W2 AECN', Location 'BASCO LOUISIANA', opened and read in full. [log:lab_results]",
    "VR Appendix 1, Biomass Feedstock Acctg v1.2")
row("4.2", "Carbon content within expected AECN range", "Pass",
    "Lab result 39.5% vs population mean 39.42% (SD 6.09%, n=285) -- 0.08 points / 0.013 SD above mean, well inside the +/-2SD (~27.2%-51.6%) flag threshold. Matches Ops Notes composite C% (39.50%) and Certify's applied Carbon Content datapoint exactly. [log:lab_results.aecn_carbon_range_check]",
    "Biomass Feedstock Acctg v1.2")
row("4.3", "Hydrogen and nitrogen values reported and reasonable", "Pass",
    "Hydrogen 7.5%, Nitrogen <0.75% -- both present and within normal ranges for AECN pyrolysis oil per lab report. [log:lab_results]",
    "Biomass Feedstock Acctg v1.2")
row("4.4", "Lab report references correct batch/sample ID", "Pass",
    "Client ID field reads '08-2026-W2 AECN', matching this batch. Sampled 2026-08-08 (within the removal window), received 2026-08-12. [log:lab_results]",
    "VR Sec 5.1")
row("4.5", "pH/conductivity (aqueous phase)", "N/A",
    "AECN is not an aqueous phase oil type. pH is tracked separately in Ops Notes (see item 5.5), not as an aqueous-phase composition check.",
    "N/A for AECN")
row("4.6", "Density above formation fluid threshold for safe injection", "Pass",
    "Lab-reported density 1.209 g/cm3, above the 1.01 g/cm3 formation-fluid floor. [log:lab_results]",
    "VR Appendix 1")

hdr("5. Ops Notes Accuracy & Internal Consistency")
row("5.1", "Correct batch ID and injection date", "Pass",
    "Ops Notes header B2='INJ-08-2026-W2', Week Start 2026-08-01, Week End 2026-08-08 -- matches the QA target and the Certify removal window (02-08 Aug 2026). [log:ops_notes.aecn_rail_tab]",
    "Ops Notes")
row("5.2", "All scale ticket values correctly transcribed into Ops Notes", "Pass",
    "All 11 rows' Full/Empty scale-ticket lb values in Ops Notes match the physical CAT tickets exactly (e.g. offload_1: Ops Notes 72,180/28,600 lb = ticket 72,180/28,600 lb). [log:scale_tickets.pairs, ops_notes.aecn_rail_tab.section3_offload_table]",
    "Ops Notes vs scale tickets")
row("5.3", "Oil and aqueous phase mass reconciliation", "N/A",
    "AECN-only removal -- no aqueous phase in this component set.",
    "N/A for AECN-only")
row("5.4", "COBB values present and match (11 offload rows, weekly time-block batch)", "Flag",
    "10 of 11 COBB rows match Ops Notes offloaded_quantity_kg exactly. One row (SHPX215090 offload_4) diverges by exactly 204.41kg, matching the documented uncertainty back-calc -- a COBB-side provenance nuance, not a reporting error affecting Certify. COBB's injection_batch column uses per-completion-date tags ('INJ-20260802_bio_oil') rather than the weekly ID 'INJ-08-2026-W2' -- an established, previously-documented naming convention, not an error. [log:cobb.rows, cobb.batch_id_col_a_note]",
    "COBB tracker vs Ops Notes")
row("5.5", "pH measurement noted", "Pass",
    "pH=2.89 recorded on all 11 offload rows, within the target range 2.0-4.0. [log:ops_notes.aecn_rail_tab.ph_values_all_11_offloads]",
    "Ops Notes > Batch Consumables")
row("5.6", "Completion date present and matches COBB", "Pass",
    "All 11 COBB rows show order_line_completed_on / injection_completion_date = 2026-08-08, matching Ops Notes Week End. [log:cobb.rows]",
    "Ops Notes vs COBB")
row("5.7", "No erroneous density measurements", "N/A",
    "Density field is expected to be blank for AECN in Ops Notes Batch Composition -- confirmed blank, expected behavior.",
    "N/A -- expected blank for AECN")

hdr("6. AECN Feedstock Emissions & Allocation")
row("6.1", "AECN process emissions LCA CI spreadsheet present", "Flag",
    "Present in Certify Sources: 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jan2026.xlsx'. Filename says 'to 30Jan2026' but the file's own internal content (opened directly) states Period start 1-Jan-26, Period end 30-Jun-26 -- correct H1 2026 period. Filename typo only ('Jan' should read 'Jun'); content is correct. [log:certify.lca_ci_file_content]",
    "VR Appendix 1")
row("6.2", "LCA with stack emissions file present", "Pass",
    "'FH 2026 LCA w Stack Emissions.xlsx' present in Certify Sources, linked to the Pyrolysis Process CI datapoint. [log:certify.sources_enumeration]",
    "VR Appendix 1")
row("6.3", "Supporting GHG data file present for AECN production period", "Pass",
    "'Supporting GHG data 30Jun2026 S.xlsx' present in Certify Sources -- matches VVB Guidance's description of the three evidence documents supporting the H2 2026 factor. [log:certify.sources_enumeration, vvb_guidance.aecn_pyrolysis_process_ef_section]",
    "VR Appendix 1")
row("6.4", "AECN pyrolysis process EF matches current value", "Pass",
    "Certify component modal shows Carbon Intensity = 0.13711712584901084 tCO2e/t, matching the VVB Guidance's stated H2-2026 total process CI (0.1371171) to full precision. This is a mid-period EF UPDATE from the prior 0.104(rail)/0.12704(truck) split -- correctly applied to this removal. Independently recalculated: 213.35153t x 0.13711712584901084 = 29.254tCO2e = Certify's displayed value exactly. [log:certify.component_modals_opened, vvb_guidance.aecn_pyrolysis_process_ef_section]",
    "Certify Datapoints")
row("6.5", "AECN pyrolysis embodied EF applied", "Pass",
    "Certify component modal shows Carbon Intensity = 0.02116 tCO2e/t, matching VVB Guidance's stated unchanged embodied factor exactly. [log:certify.component_modals_opened]",
    "Certify Datapoints")
row("6.6", "Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)", "Pass",
    "Both pyrolysis process and embodied components use 'Bio-Oil Mass - AECN via Rail' = 213,351.53kg (the pre-sparging raw offload sum, Ops Notes Section 4 row A52), not the post-sparging 209,987.25kg MOBI figure. Correct basis. [log:ops_notes.aecn_rail_tab.section4_rollup_row52, certify.component_modals_opened]",
    "Certify Components")

hdr("7. Gross-to-Net Calculation")
row("7.1", "Gross CO2e = injectate mass x carbon wt% x 3.667", "Pass",
    "Injection Sequestration component = 304.159 tCO2e. Independent recalculation: 209.98725t x 0.395 x 3.667 = 304.160t (209.98725x0.395=82.9450875; 82.9450875x3.667=304.1596), a 0.001t difference from Certify's 304.159t attributable to Certify's carbon content input carrying more decimal precision than the displayed 39.50%. [log:certify.calculation_view, ops_notes.aecn_rail_tab.section4_rollup_row52, lab_results.carbon_pct, _derived_values.gross_co2e_recalc_detail]",
    "GHG Stmt Sec E")
row("7.2", "Process emissions correctly deducted from gross", "Pass",
    "Certify Calculation View: Activities = 50.213 tCO2e = pyrolysis (33.769) + transport (16.444), matching the sum of all 8 Emitted components read from the Components tree. [log:certify.calculation_view, certify.components_breakdown]",
    "GHG Stmt Sec E")
row("7.3", "Uncertainty discount correctly applied", "Pass",
    "Certify Calculation View shows Uncertainty Discount = 1.689t, present in the net formula. Per-component uncertainty inputs independently verified as Layer-2-correct on Injection Sequestration, both Pyrolysis components, and the SOPOR->Opelousas Rail Process leg (see Section 7a). [log:certify.calculation_view]",
    "Isometric Standard v2.0 S3.7")
row("7.4", "Net removals consistent with independent gross-to-net recalculation", "Pass",
    "304.159 - 50.213 - 1.689 = 252.257t = Certify's displayed Net CO2e Removed exactly. BCU Quant spreadsheet and GHG Statement cross-check deferred as an RP-close artifact (current RP still open); internal Certify consistency is clean. [log:certify.calculation_view]",
    "GHG Stmt Sec E")

hdr("7a. Per-Component Uncertainty Verification")
row("7a.1", "Layer 1 -- Completeness: every AECN component has uncertainty on the correct datapoint", "Pass",
    "Injection Sequestration (Carbon Content + Mass of Product), AECN Pyrolysis Process (Mass), AECN Pyrolysis Embodied (Mass), and SOPOR->Opelousas Rail Process (Mass of Load) all carry +/- uncertainty inputs, opened and confirmed directly in each component's INPUTS section. Embodied transport components correctly carry NO mass uncertainty (per-mile basis, no Mass of Load datapoint expected). [log:certify.component_modals_opened]",
    "MRV Uncertainty Cheat Sheet")
row("7a.2", "Layer 2 -- Correctness: reported +/- matches expected value", "Pass",
    "Carbon Content: 39.5 ±0.158% = 0.004x39.5 EXACT, matching the MRV Uncertainty+ Evidence Cheat Sheet's stated '.004*Measured Value' rule. Mass of Product / Mass of Load (all mass-bearing components): 209,987.25kg / 213,351.53kg both ±798.27kg = 72.57kg x 11 discrete weighings this week -- the Cheat Sheet's stated '72.57kg per discrete weight (one vehicle with one load)' rule, stacked linearly across the week's 11 offload weighings per established precedent (INJ-06-2026-W1's 653.13kg=9x72.57). This differs from the classic single-offload rule (±72.57kg per removal) because a weekly-aggregate batch pools 11 discrete truck-out weighings into one removal, so the stacked uncertainty scales with N=11. [log:certify.component_modals_opened, global_evidence]",
    "MRV Uncertainty+ Evidence Cheat Sheet")
row("7a.3", "Layer 3 -- Discount presence and consistency", "Pass",
    "Aggregate Uncertainty Discount = 1.689t present and included in the Net CO2e Removed formula (verified in item 7.4). [log:certify.calculation_view]",
    "Certify Calculation View vs GHG Statement")

hdr("8. Data Integrity & Anomaly Check")
row("8.1", "No unexplained outliers in mass, carbon content, or calculated values", "Flag",
    "TILX200228 shows a 1,377.39kg (1.77%) railcar-level loss (Total Loaded 77,980kg vs Total Offloaded 76,602.61kg across its full 4-offload lifecycle spanning W1+W2) -- notably higher than SHPX215070's 70.92kg (0.09%) loss. This railcar's offloads 1 and 2 (both claimed in W1, out of this week's scope) are annotated 'COBB derived - no usable CAT ticket pair' (MIXED BASIS per the Ops Notes cell comment on H12), so the elevated loss figure most plausibly reflects estimation imprecision in those two W1 offloads rather than a genuine physical spill this week. This week's own offload (offload_4) has a full scale-ticket pair and ties exactly. Text search across all opened Ops Notes/BOL/lab documents found no incident report and no spill/incident language of any kind -- the loss is purely a railcar-level accounting residual, not deducted from credited mass, and does not affect this removal's reported figures. Carbon content (39.5%) is not an outlier (see 4.2). [log:ops_notes.aecn_rail_tab.section1_railcars_received, global_evidence]",
    "GHG Stmt Sec C")
row("8.2", "Any spills/losses documented, unrecovered mass deducted, incident report filed", "N/A",
    "No spill events identified in any opened source (scale tickets, BOLs, Ops Notes, COBB). The TILX200228 railcar-level loss discussed in 8.1 is an accounting residual across the railcar's lifecycle, not a reported spill/incident.",
    "GHG Stmt Sec C")
row("8.3", "Inventory reconciliation / carryover documentation", "N/A",
    "No cross-RP inventory reconciliation applies to this removal; all 4 railcars' offloads claimed this week are either fully-drawn-down in-week (SHPX215070, SHPX215090) or have their remaining offloads correctly deferred to a documented future week (SHPX215082 -> W3B; TILX200228 completed its lifecycle this week, W1+W2).",
    "VR Sec 3.5")
row("8.4 (Rail)", "Sister-batch/railcar sanity checks", "Pass",
    "Railcar-level BOL aggregates tie exactly to Ops Notes Total Loaded for all 4 railcars (see item 3.3). No offload-number collisions found across the 11 rows read. SHPX215082's still-open status (offloads 1+2 deferred to W3B) is correctly reflected in the Ops Notes M10 cell comment and not treated as a gap. [log:bols.bol_aggregate_check, ops_notes.aecn_rail_tab.section1_railcars_received]",
    "GHG Stmt Sec C")
row("8.5 (Rail)", "N_offloads >= N_inbound_BOLs check on last batch of each fully-drawn railcar", "Pass",
    "SHPX215070: 4 offloads (all this week) vs 3 BOLs, 4>=3 satisfied. SHPX215090: 4 offloads (all this week) vs 3 BOLs, 4>=3 satisfied. TILX200228: 4 offloads total (3 in W1 + 1 in W2, this week's offload_4 completes the railcar) vs 3 BOLs, 4>=3 satisfied. SHPX215082: not yet fully drawn down (2 of 4 offloads remain, deferred to W3B) -- check correctly deferred, not applicable this week. [log:cobb.fc9_last_offload_check]",
    "Failure Category 9")

hdr("9. Isometric Certify -- Removal Component Mapping")
row("9.1", "SEQUESTRATIONS: Gross injection sequestration matches internal gross", "Pass",
    "Injection sequestration = 304.159 tCO2e, single entry, ties to independent recalculation (209.98725t x 39.5% x 3.667, see item 7.1). [log:certify.components_breakdown.sequestrations]",
    "Certify Components")
row("9.2", "ACTIVITIES -- Transport: Process + embodied correct for all 3 legs (6 components)", "Pass",
    "All 6 expected transport components present: AECN->SOPOR Tanker Truck (Process 2.621t + Embodied 0.210t), SOPOR->Opelousas Rail (Process 12.156t + Embodied 0.187t), Opelousas->Basco Tanker Truck (Process 1.046t + Embodied 0.224t). Bio-oil transport total = 2.621+0.210+12.156+0.187+1.046+0.224 = 16.444t, matching Certify's 'Bio-oil transport' subtotal exactly. Process leg recalculations independently verified for the rail leg (see Section 3.5 and 7a.2). [log:certify.components_breakdown.removal_activities_transport, _derived_values.transport_total_calc]",
    "Certify Components")
row("9.3", "ACTIVITIES -- Injection: LCS and sample transport correct", "N/A",
    "AECN oil does not require LCS pre-treatment (that applies to Aqueous only). No dedicated sample-transport line item appears in this removal's 9-component set.",
    "N/A for AECN")
row("9.4", "ACTIVITIES -- Pyrolysis: AECN production process + embodied entries present", "Pass",
    "'AECN pyrolysis (from rail loads) - process emissions' (29.254t) and '...embodied emissions' (4.515t) both present, naming consistent with the rail-batch convention. Sum = 33.769t matches Certify's 'Pyrolysis or other process' subtotal exactly. [log:certify.components_breakdown.removal_activities_pyrolysis, _derived_values.pyrolysis_total_calc]",
    "Certify Components")
row("9.5", "REDUCTIONS: All applicable BCU categories populated", "Fail",
    "Zero Reductions/BCU components present anywhere on this removal (9 total components: 1 Sequestration + 8 Removal Activities, 0 Reductions). No BCU certificate appears in the 13-source Sources tab enumeration. Same finding pattern already registered as a FAIL on sister batch INJ-08-2026-W1 ('Zero BCU reductions; comparable batches all carry one'). [log:certify.components_breakdown.reductions_bcu_finding]",
    "Certify Components")
row("9.6", "REDUCTIONS -- BCU quantity vs transport process activity", "Fail",
    "BCU = 0t vs transport process activity sum = 2.621(AECN->SOPOR) + 12.156(SOPOR->Opelousas rail) + 1.046(Opelousas->Basco) = 15.823 tCO2e. Full transport-process coverage is the target per protocol; here coverage is 0%, a material completeness gap under the BCU QA rule (under-coverage = FLAG-or-FAIL by materiality; total absence of any offset against 15.823t is material). No BCU certificate of any kind appears among the 13 sources on this removal (Sources tab exhaustively enumerated). [log:certify.components_breakdown.reductions_bcu_finding, _derived_values.transport_process_sum_calc, global_evidence]",
    "Certify Components / Calculation View")
row("9.7", "COUNTERFACTUALS: Zero per protocol", "Pass",
    "No counterfactual components appear in the 9-component tree, consistent with bio-oil geological storage protocol (counterfactuals = 0). [log:certify.components_breakdown]",
    "Certify Components")
row("9.8", "Net removal matches internal calculation", "Pass",
    "304.159 - 50.213 - 1.689 = 252.257t = Certify's displayed Net CO2e Removed exactly (see item 7.4). [log:certify.calculation_view]",
    "Certify Calculation View")
row("9.9", "All Datapoints have descriptive source names", "Flag",
    "13 of 13 Sources reviewed. One generic filename: 'image (44).png' (linked to the SOPOR->Opelousas rail distance datapoints). One filename typo (content correct): the LCA CI calculation file says '30Jan2026' instead of '30Jun2026' (see item 6.1). All other filenames are descriptive. [log:certify.sources_enumeration]",
    "Certify Datapoints")
row("9.10", "All Sources match files referenced in Drive/Ops Notes", "Pass",
    "Ops Notes.xlsx, the AECN CoA PDF, and all EF/route-map source documents referenced in Certify Sources correspond to files independently located and opened via Drive during this session (Ops Notes, BOLs, lab CoA, LCA CI files). [log:certify.sources_enumeration, ops_notes.file, lab_results.file]",
    "Certify Sources vs Drive")

# ==================== WRITE WORKBOOK ====================
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "QA Checklist"

ws.column_dimensions['A'].width = 10
ws.column_dimensions['B'].width = 70
ws.column_dimensions['C'].width = 10
ws.column_dimensions['D'].width = 110
ws.column_dimensions['E'].width = 30

# Header block
ws['A1'] = "Batch ID"; ws['B1'] = "INJ-08-2026-W2"
ws['A2'] = "Reporting Period"; ws['B2'] = "02 Aug 2026 to 08 Aug 2026"
ws['A3'] = "Reviewer"; ws['B3'] = "Claude QA Agent"
ws['A4'] = "Date"; ws['B4'] = "2026-08-27"
ws['A5'] = "Injection Site"; ws['B5'] = "Basco 6"
ws['A6'] = "Oil Type"; ws['B6'] = "AECN"
ws['A7'] = "Certify Removal"; ws['B7'] = "rmv_1M0DGH9RA1S0HRTQ (252.257 tCO2e net)"
for r in range(1, 8):
    ws.cell(row=r, column=1).font = BOLD

r = 9
ws.cell(row=r, column=1, value="Item"); ws.cell(row=r, column=2, value="Check")
ws.cell(row=r, column=3, value="Status"); ws.cell(row=r, column=4, value="Notes / Evidence")
ws.cell(row=r, column=5, value="Verifier Reference")
for c in range(1, 6):
    ws.cell(row=r, column=c).font = BOLD
    ws.cell(row=r, column=c).fill = HEADER_FILL
r += 1

status_counts = {"Pass": 0, "Fail": 0, "Flag": 0, "N/A": 0}

for item, desc, status, evidence, ref in ROWS:
    if status == "HEADER":
        ws.cell(row=r, column=1, value="")
        c2 = ws.cell(row=r, column=2, value=desc)
        c2.font = BOLD
        for c in range(1, 6):
            ws.cell(row=r, column=c).fill = HEADER_FILL
        r += 1
        continue
    c1 = ws.cell(row=r, column=1, value=item)
    c2 = ws.cell(row=r, column=2, value=desc)
    c3 = ws.cell(row=r, column=3, value=status)
    c4 = ws.cell(row=r, column=4, value=evidence)
    c5 = ws.cell(row=r, column=5, value=ref)
    for cell in (c1, c2, c3, c4, c5):
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if status == "Fail":
        for cell in (c1, c2, c3, c4, c5):
            cell.fill = FAIL_FILL
        status_counts["Fail"] += 1
    elif status == "Flag":
        for cell in (c1, c2, c3, c4, c5):
            cell.fill = FLAG_FILL
            cell.font = FLAG_FONT
        status_counts["Flag"] += 1
    elif status == "N/A":
        for cell in (c1, c2, c3, c4, c5):
            cell.font = NA_FONT
        status_counts["N/A"] += 1
    else:
        status_counts["Pass"] += 1
    r += 1

# Summary
r += 1
ws.cell(row=r, column=1, value="Summary").font = BOLD
r += 1
ws.cell(row=r, column=1, value="Pass"); ws.cell(row=r, column=2, value=status_counts["Pass"])
r += 1
ws.cell(row=r, column=1, value="Fail"); ws.cell(row=r, column=2, value=status_counts["Fail"])
r += 1
ws.cell(row=r, column=1, value="Flag"); ws.cell(row=r, column=2, value=status_counts["Flag"])
r += 1
ws.cell(row=r, column=1, value="N/A"); ws.cell(row=r, column=2, value=status_counts["N/A"])

outpath = "outputs/qa/batch-INJ-08-2026-W2-AECN/Batch_INJ-08-2026-W2_QA_Checklist.xlsx"
wb.save(outpath)
print("Saved:", outpath)
print("Counts:", status_counts)
