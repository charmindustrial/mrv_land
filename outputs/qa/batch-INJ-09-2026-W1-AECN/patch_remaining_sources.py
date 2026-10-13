#!/usr/bin/env python3
"""Second patch: remaining component modals, COBB, Standard EF sheet, Certify source-file identity checks. Run after patch_certify_components.py."""
import json
from pathlib import Path

HERE = Path(__file__).parent
LOG = HERE / "batch_INJ-09-2026-W1-AECN_source_reads.json"
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M2GBNMY91S0H2MB/edit?tab=components"
EF_URL = "https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705"
COBB_URL = "https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350#gid=1627433350"

def opened(name, artifact, evidence, cmp_id):
    return {"file": f"Certify component detail view: {name}", "action": "modal_opened",
            "live_source_url": f"{CERTIFY_URL}&component={cmp_id}", "artifact_path": artifact, "evidence": evidence}

log = json.loads(LOG.read_text())
cc = log.setdefault("certify_components", {})

cc["transport_embodied"].update({
    "AECN_to_SOPOR_truck": {"component_id": "cmp_1M2GBNMY91S04WRD", "value_tCO2e": 0.153, "ef": {"datapoint": "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance AECN to Sopor Quebec (truck)", "value_mi": 644.09429, "sources": 3}, "recalc": "644.09429 mi x 0.23756 = 153.0 kg = 0.153 t", "ops_notes_L36_mi": 644.1093682, "delta_vs_ops_mi": round(644.1093682 - 644.09429, 5),
                             "_primary_source_opened": [opened("AECN to SOPOR Tanker Truck Transport Embodied Emissions", "certify_modal_aecn_sopor_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; allocated distance 644.09429 mi", "cmp_1M2GBNMY91S04WRD")]},
    "SOPOR_to_Opelousas_rail": {"component_id": "cmp_1M2GBNMY91S0H7WR", "value_tCO2e": 0.137, "ef": {"datapoint": "Emissions Factor - Vehicle Embodied Emissions -- Railcar", "value": 0.03113, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance Sopor Quebec to Opelousas (rail)", "value_mi": 4398, "sources": 2}, "recalc": "4,398 mi x 0.03113 = 136.9 kg = 0.137 t", "ops_notes_M36_mi": 4398,
                                "_primary_source_opened": [opened("SOPOR to Opelousas Rail Transport Embodied Emissions", "certify_modal_rail_embodied.yml", "EF 0.03113 kgCO2e/mi; allocated distance 4,398 mi", "cmp_1M2GBNMY91S0H7WR")]},
    "Opelousas_to_Basco_truck": {"component_id": "cmp_1M2GBNMY91S0XK13", "value_tCO2e": 0.163, "ef": {"value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance Opelousas to B6 (truck)", "value_mi": 686.4, "sources": 2}, "recalc": "686.4 mi x 0.23756 = 163.1 kg = 0.163 t", "ops_notes_N36_mi": 686.4,
                                 "_primary_source_opened": [opened("Opelousas to Basco Tanker Truck Transport Embodied Emissions", "certify_modal_opel_basco_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; allocated distance 686.4 mi", "cmp_1M2GBNMY91S0XK13")]},
    "sum_tCO2e": round(7.307 + 0.153 + 0.137 + 0.163, 3), "sum_calc": "7.307 + 0.153 + 0.137 + 0.163 = 7.760",
    "bio_oil_transport_total_tCO2e": round(81.317 + 7.760, 3), "bio_oil_transport_total_calc": "81.317 (process) + 7.760 (embodied) = 89.077 = Components tab 'Bio-oil transport' subtotal 89.077",
})
cc["pyrolysis_embodied_rail"] = {"component_id": "cmp_1M2GBNMY91S0C6FQ", "value_tCO2e": 3.298, "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)", "value_tCO2e_per_t": 0.02116, "sources": 1}, "mass_input": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": 155863.1, "uncertainty_kg": 580.56}, "recalc": "155.8631 t x 0.02116 = 3.298 t",
                                 "_primary_source_opened": [opened("AECN pyrolysis (from rail loads) - embodied emissions", "certify_modal_pyro_rail_embodied.yml", "CI 0.02116 tCO2e/t; mass 155,863.1 ±580.56 kg", "cmp_1M2GBNMY91S0C6FQ")]}
cc["pyrolysis_embodied_truck"] = {"component_id": "cmp_1M2GBNMY91S0FGAY", "value_tCO2e": 5.878, "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Embodied Emissions (direct to B6)", "value_tCO2e_per_t": 0.02116, "sources": 1}, "mass_input": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": 277790, "uncertainty_kg": 1088.55}, "recalc": "277.790 t x 0.02116 = 5.878 t",
                                  "_primary_source_opened": [opened("AECN pyrolysis (from truck loads) - embodied emissions", "certify_modal_pyro_truck_embodied.yml", "CI 0.02116 tCO2e/t; mass 277,790 ±1,088.55 kg", "cmp_1M2GBNMY91S0FGAY")]}
cc["bcu_transport"] = {"component_id": "cmp_1M2GBNMY91S0DRS4", "value_tCO2e": 81.318, "input": {"datapoint": "BCUs Applied - Bio-Oil Transport Process [Certify input]", "value_kgCO2e": 81318, "sources": 1, "source_file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf"},
                       "transport_process_sum_tCO2e_displayed": 81.317, "transport_process_sum_precise_t": round(69.75781921 + 1.91507940 + 8.88047025 + 0.76427006, 5),
                       "delta_t": round(81.318 - 81.31764, 5), "assessment": "BCU 81.318 t vs precise transport-process sum 81.31764 t: delta +0.00036 t (0.36 kg, 0.0004%), i.e. equal at the kg-rounding level; no meaningful over-coverage.",
                       "certificate": {"file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "certify_etag_md5": "80cd7978cce9296e57c6af7d7d71e416", "local_copy": "Charm-RetirementCertificate-RD-EACs-20251218_priorcopy.pdf (byte-identical, md5 80cd7978cce9296e57c6af7d7d71e416)",
                                       "retiring_org": "Amazon.com Services LLC", "on_behalf_of": "Charm Industrial, Inc", "date_of_retirement": "Dec 18, 2025", "vintage": 2024, "commodity": "Renewable Diesel TERCS", "number_retired_tCO2e": 2795, "verification_body": "Turner, Mason & Company", "certificate_number": "TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000",
                                       "note": "Certificate is a pooled 2,795 tCO2e retirement; per-removal draw-down is tracked in Charm's EAC inventory tracker, not on the certificate."},
                       "_primary_source_opened": [opened("BCUs - Applied to Bio-Oil Transport Process Emissions", "certify_modal_bcu.yml", "Constant CO2 reduction input 81,318 kgCO2e, 1 source", "cmp_1M2GBNMY91S0DRS4"),
                                                  {"file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "action": "pdf_read", "artifact_path": "Charm-RetirementCertificate-RD-EACs-20251218_priorcopy.pdf", "evidence": "Certify copy etag md5 80cd7978cce9296e57c6af7d7d71e416 == local file md5; page read: 2,795 TERCs retired Dec 18 2025 on behalf of Charm Industrial, Inc"}]}

log["standard_efs"] = {
    "file": "Standard Emission Factors + Calculations (Google Sheet 1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4), exported to xlsx 2026-09-17 and read with openpyxl", "tab": "2026", "live_source_url": EF_URL, "artifact_path": "Standard_Emission_Factors_export_2026-09-17.xlsx",
    "rows": {
        "B3": {"name": "Production Emissions for AECN Oil--H1 2026", "unit_C": "MTCO2e/MT Oil", "final_F": 0.1040167408, "source_G": "AECN LCA"},
        "B4": {"name": "Production Emissions for AECN Oil--H2 2026", "unit_C": "MTCO2e/MT Oil", "baseline_D": 0.1371171258, "final_F": 0.1371171258, "source_G": "FH 2026 LCA w Stack Emissions", "certify_display": 0.13712, "match": True},
        "B5": {"name": "Embodied Emissions for AECN Oil", "unit_C": "MTCO2e/MT Oil", "final_F": 0.02116, "source_G": "AECN Information, NAICS Supply Chain Emissions Factors", "certify_display": 0.02116, "match": True},
        "B6": {"name": "Truck Transport Fuel Use (Well to Wheel) -- Tanker Truck", "unit_C": "MT CO2e/t-mi", "final_F": 0.0001143, "source_G": "GLEC V3.2 2025", "certify_display": "0.1143 kgCO2e/(t*mi)", "match": True},
        "B10": {"name": "Rail Transport Fuel Use (Well to Wheel)", "unit_C": "MTCO2e/T-mi", "final_F": 2.5910374e-05, "source_G": "GLEC V3.2 2025", "certify_display": "0.02591 kgCO2e/(t*mi)", "match": True},
        "B11": {"name": "Vehicle Embodied Emissions --Tanker Truck", "unit_C": "MT CO2e/mi", "final_F": 0.0002375605888, "source_G": "GLEC V3.2 2025", "certify_display": "0.23756 kgCO2e/mi (= 0.1476 kgCO2e/km on Datapoints tab)", "match": True},
        "B13": {"name": "Vehicle Embodied Emissions --Railcar", "unit_C": "MTCO2e/mi", "final_F": 3.113066508e-05, "source_G": "GLEC V3.2 2025", "certify_display": "0.03113 kgCO2e/mi (= 0.0193 kgCO2e/km on Datapoints tab)", "match": True},
    },
    "h2_2026_aecn_tab": {"tab": "H2 2026 AECN Process Emissions", "I10_stack": 0.004065098048, "I11_vendor_lca": 0.133052027800741, "I12_total": 0.1371171258},
    "railcar_ee_tab": {"tab": "2026 Railcar Embodied Emissions", "B1_manufacture_MTCO2e": 65.37439668, "B4_lifetime_mi": 2100000, "B5_per_mile": 3.113066508e-05},
    "fh_2026_lca_file": {"file": "FH 2026 LCA w Stack Emissions.xlsx (Certify source #44)", "certify_etag_md5": "d648deb28f36628c4bf06e1c21e12804", "local_copy": "FH_2026_LCA_w_Stack_Emissions.xlsx (md5 d648deb28f36628c4bf06e1c21e12804, byte-identical)", "Sheet1_I12": 0.1371171258, "Sheet1_I10": 0.004065098048, "Sheet1_I11": 0.133052027800741},
    "_primary_source_opened": [
        {"file": "Standard Emission Factors + Calculations - 2026 tab", "action": "sheet_grid_read", "live_source_url": EF_URL, "artifact_path": "Standard_Emission_Factors_export_2026-09-17.xlsx", "evidence": "Rows 3-13 read: F4=0.1371171258, F5=0.02116, F6=0.0001143, F10=2.5910374e-05, F11=0.0002375605888, F13=3.113066508e-05"},
        {"file": "FH 2026 LCA w Stack Emissions.xlsx", "action": "sheet_grid_read", "live_source_url": CERTIFY_URL.replace("tab=components", "tab=sources"), "artifact_path": "FH_2026_LCA_w_Stack_Emissions.xlsx", "evidence": "Sheet1 I12 = 0.1371171258 MT CO2e/MT Bio Oil; Certify upload etag md5 d648deb28f36628c4bf06e1c21e12804 equals this file"},
    ],
}

TRUCK_ROWS = [  # row, bol, qty_consumed(F), offloaded(G), origin(H), completed_on(I)
    (725, "2488-T", 19220.0, 19220.0, 19220.0, "2026-09-02 11:45:46"), (726, "2493-T", 19320.0, 19320.0, 19320.0, "2026-08-31 17:09:07"),
    (727, "2495-T", 19510.0, 19510.0, 19510.0, "2026-09-03 19:50:26"), (728, "2496-T", 19507.17755, 19507.17755, 19770.0, "2026-09-04 13:24:00"),
    (729, "2487-T", 19820.0, 19820.0, 19820.0, "2026-08-29 02:02:39"), (730, "2490-T", 19860.0, 19860.0, 19860.0, "2026-09-02 11:47:59"),
    (731, "2489-T", 19870.0, 19870.0, 19870.0, "2026-09-02 11:47:10"), (732, "2494-T", 19880.0, 19880.0, 19880.0, "2026-09-01 22:09:38"),
    (733, "2486-T", 19920.0, 19920.0, 19920.0, "2026-09-02 11:44:48"), (734, "2491-T", 19657.77009, 19657.77009, 19920.0, "2026-09-02 11:48:34"),
    (735, "2481-T", 19980.0, 19980.0, 19980.0, "2026-08-28 01:02:20"), (736, "2484-T", 20027.44757, 20027.44757, 20030.0, "2026-08-31 17:10:14"),
    (737, "2485-T", 20040.0, 20040.0, 20040.0, "2026-08-28 18:16:57"), (738, "2492-T", 20175.77216, 20175.77216, 27010.0, "2026-08-31 20:32:18"),
]
OPS_TRUCK = {"2481-T": 19980, "2484-T": 20030, "2485-T": 20040, "2486-T": 19920, "2487-T": 19820, "2488-T": 19220, "2489-T": 19870, "2490-T": 19860, "2491-T": 19920, "2492-T": 20170, "2493-T": 19320, "2494-T": 19880, "2495-T": 19990, "2496-T": 19770}
RAIL_ROWS = [  # row, consumed_lot, bols, qty(F=G), origin(H), completed_on
    (739, "Rail_GRPX5254_7.17.2026_offload_1", "2430-R, 2431-R, 2432-R", 19440.95312, 77870.0, "2026-09-02 13:54:30"),
    (740, "Rail_GRPX5254_7.17.2026_offload_2", "2430-R, 2431-R, 2432-R", 19849.18592, 77870.0, "2026-09-02 13:54:30"),
    (741, "Rail_GRPX5254_7.17.2026_offload_3", "2430-R, 2431-R, 2432-R", 20801.72912, 77870.0, "2026-09-02 13:54:30"),
    (742, "Rail_GRPX5254_7.17.2026_offload_4", "2430-R, 2431-R, 2432-R", 17563.08224, 77870.0, "2026-09-02 13:54:30"),
    (743, "Rail_GPRX5107_7.29.2026_offload_1", "2444-R, 2445-R, 2446-R", 22189.72064, 78010.0, "2026-08-27 20:01:46"),
    (744, "Rail_GPRX5107_7.29.2026_offload_2", "2444-R, 2445-R, 2446-R", 20638.436, 78010.0, "2026-08-27 20:01:46"),
    (745, "Rail_GPRX5107_7.29.2026_offload_3", "2444-R, 2445-R, 2446-R", 19995.5832, 78010.0, "2026-08-27 20:01:46"),
    (746, "Rail_GPRX5107_7.29.2026_offload_4", "2444-R, 2445-R, 2446-R", 15186.26016, 78010.0, "2026-08-27 20:01:46"),
]
OPS_RAIL_NET = {"offload_1_GRPX5254": 19440.95312, "offload_2_GRPX5254": 19849.18592, "offload_3_GRPX5254": 20801.72912, "offload_4_GRPX5254": 17563.08224,
                "offload_1_GPRX5107": 22189.72064, "offload_2_GPRX5107": 20638.436, "offload_3_GPRX5107": 20012.47904, "offload_4_GPRX5107": 15186.26016}

log["cobb"] = {
    "tab": "Basco Injection -- COBB", "tracker_url": COBB_URL,
    "method": "Google Sheet exported to xlsx via Drive API 2026-09-17 and read with openpyxl (all 3000 rows scanned for the batch id in column A)",
    "artifact_path": "COBB_Bio-oil_Injection_Tracker_export_2026-09-17.xlsx",
    "header_row_2": {"A": "injection_batch", "B": "injected_product", "C": "consumed_lot", "D": "security_tag", "E": "BOL_number", "F": "quantity_consumed_in_injection", "G": "offloaded_quantity_kg", "H": "origin_quantity_kg", "I": "order_line_completed_on", "J": "purchase_order_link", "K": "offload_order_link", "L": "injection_completion_date", "M": "injection_ph", "N": "Proportion of Origin Consumed", "O": "Origin Mass", "P": "Consumed Origin Mass", "Q": "week_of_year", "R": "ISO_week_starting", "S": "week_starting_injected"},
    "rows_found_at": "725-746 (bio_oil); 747-759 are INJ-09-2026-W1_oily_fraction (WODO, out of scope)",
    "row_id_at_qa": "INJ-09-2026-W1", "batch_id_col_a": "INJ-09-2026-W1_bio_oil", "row_count_bio_oil": 22,
    "truck_rows": [{"row": r, "bol": b, "quantity_consumed_in_injection_F": f, "offloaded_quantity_kg_G": g, "origin_quantity_kg_H": h, "order_line_completed_on_I": i, "ops_notes_bol_kg": OPS_TRUCK[b], "origin_minus_ops_kg": round(h - OPS_TRUCK[b], 3), "injection_completion_date_L": "2026-09-04", "injection_ph_M": None} for r, b, f, g, h, i in TRUCK_ROWS],
    "rail_rows": [{"row": r, "consumed_lot": c, "BOL_number_E": b, "quantity_consumed_F_and_offloaded_G_kg": q, "origin_quantity_kg_H": h, "order_line_completed_on_I": i, "ops_notes_net_kg": OPS_RAIL_NET[c.split("_")[-2] + "_" + c.split("_")[-1] + "_" + c.split("_")[1]] if False else OPS_RAIL_NET[f"offload_{c[-1]}_{c.split('_')[1]}"], "delta_cobb_minus_ops_kg": round(q - OPS_RAIL_NET[f"offload_{c[-1]}_{c.split('_')[1]}"], 5), "injection_completion_date_L": "2026-09-04", "injection_ph_M": None} for r, c, b, q, h, i in RAIL_ROWS],
    "findings": {
        "origin_2492T": "COBB origin_quantity_kg for 2492-T = 27,010 kg (the BOL page-3 figure) vs Ops Notes/Certify 20,170 kg; F/G columns carry 20,175.77 kg.",
        "origin_2495T": "COBB origin_quantity_kg for 2495-T = 19,510 kg vs BOL page-3 / Ops Notes 19,990 kg (-480 kg); Ops Notes cell comment C22 already flags this.",
        "rail_offload3_GPRX5107": "COBB 19,995.5832 kg vs Ops Notes / ticket-derived 20,012.47904 kg (-16.896 kg); documented in Ops Notes D34 comment (scale ticket authoritative).",
        "other_rail_rows": "7 of 8 rail rows equal the Ops Notes ticket-derived net exactly.",
        "railcar_spelling": "consumed_lot uses 'GRPX5254' (matches Ops Notes/Certify); the CAT tickets and the April 2026 COBB rows (127-130, 'Rail_GPRX5254_4.10.2026_offload_N') spell the same car 'GPRX5254'.",
        "completion_date": "injection_completion_date (L) = 2026-09-04 on all 22 rows = Ops Notes offload-table date (A28:A35) = Certify period end 04 Sep 2026.",
        "ph": "injection_ph (M) blank on all 22 rows; Ops Notes pH columns (Rail G28:G35, Truck H10:H23) also blank.",
    },
    "_primary_source_opened": [{"file": "Bio-oil Injection Tracker, tab 'Basco Injection -- COBB'", "action": "sheet_grid_read", "live_source_url": COBB_URL, "artifact_path": "COBB_Bio-oil_Injection_Tracker_export_2026-09-17.xlsx", "evidence": "rows 725-746 col A = 'INJ-09-2026-W1_bio_oil'; 14 truck + 8 rail rows read with all columns"}],
}

log["certify_source_file_checks"] = {
    "method": "For each Certify source: opened the source detail view, captured the signed storage.googleapis.com request from the browser network log, read the response headers; GCS etag = file md5. Compared with md5 of the files downloaded from the Drive hyperlinks in the Ops Notes.",
    "ledger_artifact": "certify_upload_etags.txt", "drive_md5_artifact": "drive_file_md5.txt",
    "result": "36 of 36 Certify ticket/BOL uploads are byte-identical (md5 + content-length) to the Drive files read in this session: 16 scale tickets, 6 rail BOLs, 14 truck BOLs.",
    "other_sources": {"FH 2026 LCA w Stack Emissions.xlsx": "etag d648deb28f36628c4bf06e1c21e12804 = local FH_2026_LCA_w_Stack_Emissions.xlsx (read: I12 = 0.1371171258)",
                      "Charm-RetirementCertificate-RD-EACs-20251218.pdf": "etag 80cd7978cce9296e57c6af7d7d71e416 = local copy read this session (2,795 TERCs, Dec 18 2025)",
                      "AECN Embodied Emissions Calc Sheet (1).pdf": "see certify_components.pyrolysis_embodied_calc_sheet"},
    "_primary_source_opened": [{"file": "Certify Sources tab detail views (36 ticket/BOL sources + LCA + BCU cert + embodied calc sheet)", "action": "modal_opened", "live_source_url": CERTIFY_URL.replace("tab=components", "tab=sources"), "artifact_path": "certify_upload_etags.txt", "evidence": "36/36 md5 matches recorded in certify_upload_etags.txt vs drive_file_md5.txt"}],
}

LOG.write_text(json.dumps(log, indent=2, default=str))
print("patched: standard_efs, cobb, certify_source_file_checks, remaining components")
