#!/usr/bin/env python3
"""Adds certify_components (14 component detail views opened 2026-09-22), cobb and standard_efs to the source-read log. Run after build_source_reads.py."""
import json
from pathlib import Path

HERE = Path(__file__).parent
LOG = HERE / "batch_INJ-09-2026-W2-AECN_source_reads.json"
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M2RKR58N1S0F02M/edit"
EF_URL = "https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705"
COBB_URL = "https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350#gid=1627433350"

def opened(name, artifact, evidence, cmp_id):
    return {"file": f"Certify component detail view: {name}", "action": "modal_opened",
            "live_source_url": f"{CERTIFY_URL}?component={cmp_id}", "artifact_path": artifact, "evidence": evidence}

RAIL = 155863.28
TRUCK = 58570
certify_components = {
    "injection_sequestration": {
        "component_id": "cmp_1M2RKR58N1S0B5EY", "value_tCO2e": 312.963,
        "carbon_content_input": {"datapoint": "Carbon Content of Bio-oil Injected (per injection)", "value_pct": 40.4, "uncertainty_pct": 0.16164, "sources": 2},
        "mass_input": {"datapoint": "Mass of Injectant (per injection)", "value_kg": 211252.2262, "uncertainty_kg": 798.3225712, "sources": 1},
        "blueprint": "carbon_rich_substance_sequestration: output = product_mass * carbon_content * {co2e_of_carbon}",
        "recalc": "211.2522262 t x 0.404 x 3.667 = 312.963 tCO2e",
        "carbon_uncertainty_check": "0.004 x 40.4 = 0.1616 = displayed 0.16164",
        "mass_uncertainty_check": "798.3225712 / 72.5747792 = 11.0 discrete weighings (72.5747792 kg = 160 lb x 0.45359237); batch has 8 rail offload weighings + 3 truck BOL weighings = 11. The rail and truck mass inputs use 72.57 per weighing (580.56 = 8 x 72.57; 217.71 = 3 x 72.57), so 8 x 72.57 + 3 x 72.57 = 798.27 kg would be the like-for-like figure; the 0.05 kg difference is the 72.57 rounding.",
        "_primary_source_opened": [opened("Injection sequestration", "certify_modal_injection_sequestration.yml", "Carbon 40.4 ±0.16164 %; Mass 211,252.2262 ±798.3225712 kg (1 source)", "cmp_1M2RKR58N1S0B5EY")],
    },
    "pyrolysis_process_rail": {
        "component_id": "cmp_1M2RKR58N1S0PF2B", "value_tCO2e": 21.372, "share_pct": 7.77,
        "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)", "value_tCO2e_per_t": 0.13712, "sources": 1},
        "mass_input": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": RAIL, "uncertainty_kg": 580.56, "sources": 9},
        "recalc": "155.86328 t x 0.1371171258 = 21.372 tCO2e", "mass_uncertainty_check": "580.56 / 72.57 = 8.0 = 8 rail offload weighings",
        "_primary_source_opened": [opened("AECN pyrolysis (from rail loads) - process emissions", "certify_modal_pyro_rail_process.yml", "CI 0.13712 tCO2e/t; Mass 155,863.28 ±580.56 kg (9 sources)", "cmp_1M2RKR58N1S0PF2B")],
    },
    "pyrolysis_process_truck": {
        "component_id": "cmp_1M2RKR58N1S0SRXJ", "value_tCO2e": 8.031, "share_pct": 2.92,
        "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Process Emissions (direct to B6)", "value_tCO2e_per_t": 0.13712, "sources": 1},
        "mass_input": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": TRUCK, "uncertainty_kg": 217.71, "sources": 3},
        "recalc": "58.570 t x 0.1371171258 = 8.031 tCO2e", "mass_uncertainty_check": "217.71 / 72.57 = 3.0 = 3 truck BOL weighings",
        "_primary_source_opened": [opened("AECN pyrolysis (from truck loads) - process emissions", "certify_modal_pyro_truck_process.yml", "CI 0.13712 tCO2e/t; Mass 58,570 ±217.71 kg (3 sources)", "cmp_1M2RKR58N1S0SRXJ")],
    },
    "pyrolysis_embodied_rail": {"component_id": "cmp_1M2RKR58N1S0A3Y0", "value_tCO2e": 3.298, "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)", "value_tCO2e_per_t": 0.02116, "sources": 1}, "mass_input": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": RAIL, "uncertainty_kg": 580.56}, "recalc": "155.86328 t x 0.02116 = 3.298 t",
                                "_primary_source_opened": [opened("AECN pyrolysis (from rail loads) - embodied emissions", "certify_modal_pyro_rail_embodied.yml", "CI 0.02116 tCO2e/t; mass 155,863.28 ±580.56 kg", "cmp_1M2RKR58N1S0A3Y0")]},
    "pyrolysis_embodied_truck": {"component_id": "cmp_1M2RKR58N1S0DDS7", "value_tCO2e": 1.239, "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Embodied Emissions (direct to B6)", "value_tCO2e_per_t": 0.02116, "sources": 1}, "mass_input": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": TRUCK, "uncertainty_kg": 217.71}, "recalc": "58.570 t x 0.02116 = 1.239 t",
                                 "_primary_source_opened": [opened("AECN pyrolysis (from truck loads) - embodied emissions", "certify_modal_pyro_truck_embodied.yml", "CI 0.02116 tCO2e/t; mass 58,570 ±217.71 kg", "cmp_1M2RKR58N1S0DDS7")]},
    "transport_process": {
        "AECN_to_LA_direct_truck": {"component_id": "cmp_1M2RKR58N1S0CX0R", "value_tCO2e": 14.708, "ef": {"datapoint": "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from AECN to Basco", "value_mi": 2197}, "mass": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": TRUCK, "uncertainty_kg": 217.71}, "recalc": "58.570 t x 2,197 mi x 0.1143 kg/(t*mi) = 14,707.6 kg = 14.708 t", "precise_t": 14.70793,
                                    "_primary_source_opened": [opened("AECN to LA Tanker Truck Transport Process Emissions - AECN", "certify_modal_aecn_la_truck_process.yml", "EF 0.1143 kgCO2e/(t*mi); distance 2,197 mi; mass 58,570 ±217.71 kg", "cmp_1M2RKR58N1S0CX0R")]},
        "AECN_to_SOPOR_truck": {"component_id": "cmp_1M2RKR58N1S00HWD", "value_tCO2e": 1.915, "ef": {"value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from AECN to Sopor Quebec (truck)", "value_mi": 107.49722}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": RAIL, "uncertainty_kg": 580.56}, "recalc": "155.86328 t x 107.49722 mi x 0.1143 = 1,915.1 kg = 1.915 t", "precise_t": 1.91508,
                                "_primary_source_opened": [opened("AECN to SOPOR Tanker Truck Transport Process Emissions", "certify_modal_aecn_sopor_truck_process.yml", "EF 0.1143; distance 107.49722 mi; mass 155,863.28 ±580.56 kg", "cmp_1M2RKR58N1S00HWD")]},
        "SOPOR_to_Opelousas_rail": {"component_id": "cmp_1M2RKR58N1S0M6R2", "value_tCO2e": 8.880, "ef": {"datapoint": "Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "value": 0.02591, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from Sopor Quebec to Opelousas (rail)", "value_mi": 2199}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": RAIL, "uncertainty_kg": 580.56}, "recalc": "155.86328 t x 2,199 mi x 0.025910374 = 8,880.6 kg = 8.880 t", "precise_t": 8.88061,
                                    "_primary_source_opened": [opened("SOPOR to Opelousas Rail Transport Process Emissions", "certify_modal_rail_process.yml", "EF 0.02591 kgCO2e/(t*mi); distance 2,199 mi; mass 155,863.28 ±580.56 kg", "cmp_1M2RKR58N1S0M6R2")]},
        "Opelousas_to_Basco_truck": {"component_id": "cmp_1M2RKR58N1S07VKQ", "value_tCO2e": 0.764, "ef": {"value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from Opelousas to B6 (truck)", "value_mi": 42.9}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": RAIL, "uncertainty_kg": 580.56}, "recalc": "155.86328 t x 42.9 mi x 0.1143 = 764.3 kg = 0.764 t", "precise_t": 0.76427,
                                     "_primary_source_opened": [opened("Opelousas to Basco - Tanker Truck Transport Process Emissions", "certify_modal_opel_basco_truck_process.yml", "EF 0.1143; distance 42.9 mi; mass 155,863.28 ±580.56 kg", "cmp_1M2RKR58N1S07VKQ")]},
        "sum_tCO2e": round(14.708 + 1.915 + 8.880 + 0.764, 3), "sum_calc": "14.708 + 1.915 + 8.880 + 0.764 = 26.267",
        "sum_precise_t": round(14.70793 + 1.91508 + 8.88061 + 0.76427, 5), "sum_precise_calc": "14.70793 + 1.91508 + 8.88061 + 0.76427 = 26.26789",
        "distance_uncertainty": "none shown on any of the 4 legs (expected)",
    },
    "transport_embodied": {
        "AECN_to_LA_direct_truck": {"component_id": "cmp_1M2RKR58N1S0S853", "value_tCO2e": 1.566, "ef": {"datapoint": "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Aggregate Distance Transported AECN to Basco", "value_mi": 6591, "sources": 1}, "recalc": "6,591 mi x 0.2375605888 kg/mi = 1,565.8 kg = 1.566 t", "mass_input": "none (per-mile blueprint)",
                                    "_primary_source_opened": [opened("AECN to LA Tanker Truck Transport Embodied Emissions - AECN", "certify_modal_aecn_la_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; distance 6,591 mi", "cmp_1M2RKR58N1S0S853")]},
        "AECN_to_SOPOR_truck": {"component_id": "cmp_1M2RKR58N1S02T6P", "value_tCO2e": 0.153, "ef": {"value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance AECN to Sopor Quebec (truck)", "value_mi": 644.74168, "sources": 13}, "recalc": "644.74168 mi x 0.2375605888 = 153.2 kg = 0.153 t", "ops_notes_L36_mi": 644.7583867, "delta_vs_ops_mi": round(644.7583867 - 644.74168, 5), "basis_note": "Certify allocation built on the map distance 107.49722 mi; Ops L uses the rounded 107.5",
                                "_primary_source_opened": [opened("AECN to SOPOR Tanker Truck Transport Embodied Emissions", "certify_modal_aecn_sopor_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; allocated distance 644.74168 mi (13 sources)", "cmp_1M2RKR58N1S02T6P")]},
        "SOPOR_to_Opelousas_rail": {"component_id": "cmp_1M2RKR58N1S0F5B1", "value_tCO2e": 0.137, "ef": {"datapoint": "Emissions Factor - Vehicle Embodied Emissions -- Railcar", "value": 0.03113, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance Sopor Quebec to Opelousas (rail)", "value_mi": 4396.35245, "sources": 13}, "recalc": "4,396.35245 mi x 0.03113066508 = 136.9 kg = 0.137 t", "ops_notes_M36_mi": 4405.917936, "delta_vs_ops_mi": round(4405.917936 - 4396.35245, 5),
                                    "basis_note": "Certify = mass-fraction allocation on all three railcars: 2199 x 77800.09984/78140 = 2189.4345 (TIMX201060) + 589.1214 + 420.1406 (SHPX215046) + 615.6079 + 582.0479 (SHPX215079) = 4396.3524 mi. Ops M32 books the full 2199 mi for the FULL railcar TIMX201060, giving M36 4405.917936. Ops basis x 0.03113066508 kg/mi = 137.16 kg; both round to 0.137 t.",
                                    "_primary_source_opened": [opened("SOPOR to Opelousas Rail Transport Embodied Emissions", "certify_modal_rail_embodied.yml", "EF 0.03113 kgCO2e/mi; allocated distance 4,396.35245 mi (13 sources)", "cmp_1M2RKR58N1S0F5B1")]},
        "Opelousas_to_Basco_truck": {"component_id": "cmp_1M2RKR58N1S0VGFC", "value_tCO2e": 0.163, "ef": {"value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Allocated Distance Opelousas to B6 (truck)", "value_mi": 686.4, "sources": 1}, "recalc": "686.4 mi x 0.2375605888 = 163.1 kg = 0.163 t", "ops_notes_N36_mi": 686.4,
                                     "_primary_source_opened": [opened("Opelousas to Basco Tanker Truck Transport Embodied Emissions", "certify_modal_opel_basco_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; allocated distance 686.4 mi", "cmp_1M2RKR58N1S0VGFC")]},
        "sum_tCO2e": round(1.566 + 0.153 + 0.137 + 0.163, 3), "sum_calc": "1.566 + 0.153 + 0.137 + 0.163 = 2.019",
        "bio_oil_transport_total_tCO2e": round(26.267 + 2.019, 3), "bio_oil_transport_total_calc": "26.267 (process) + 2.019 (embodied) = 28.286 = Components tab 'Bio-oil transport' subtotal 28.286",
    },
    "bcu_transport": {"component_id": "cmp_1M2RKR58N1S0BP7D", "value_tCO2e": 26.187, "share_pct": 9.52, "input": {"datapoint": "BCUs Applied - Bio-Oil Transport Process [Certify input]", "value_kgCO2e": 26187, "sources": 1, "source_file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf"},
                      "transport_process_sum_tCO2e_displayed": 26.267, "transport_process_sum_precise_t": 26.26789,
                      "delta_t": round(26.187 - 26.26789, 5), "assessment": "BCU 26.187 t is 0.08089 t (80.9 kg, 0.31%) BELOW the transport-process sum 26.26789 t: under-coverage, conservative direction. 26,267 kg would give full coverage without exceeding it.",
                      "certificate": {"file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "local_copy": "../batch-INJ-09-2026-W1-AECN/Charm-RetirementCertificate-RD-EACs-20251218_priorcopy.pdf (read this session)",
                                      "retiring_org": "Amazon.com Services LLC", "on_behalf_of": "Charm Industrial, Inc", "date_of_retirement": "Dec 18, 2025", "vintage": 2024, "commodity": "Renewable Diesel TERCS", "number_retired_tCO2e": 2795, "verification_body": "Turner, Mason & Company", "certificate_number": "TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000",
                                      "note": "Certificate is a pooled 2,795 tCO2e retirement; per-removal draw-down is tracked in Charm's EAC inventory tracker, not on the certificate."},
                      "_primary_source_opened": [opened("BCUs - Applied to Bio-Oil Transport Process Emissions", "certify_modal_bcu.yml", "Constant CO2 reduction input 26,187 kgCO2e, 1 source", "cmp_1M2RKR58N1S0BP7D"),
                                                 {"file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "action": "pdf_read", "artifact_path": "../batch-INJ-09-2026-W1-AECN/Charm-RetirementCertificate-RD-EACs-20251218_priorcopy.pdf", "evidence": "Page read: 2,795 Renewable Diesel TERCs retired Dec 18 2025 on behalf of Charm Industrial, Inc, verifier Turner, Mason & Company"}]},
}

standard_efs = {
    "file": "Standard Emission Factors + Calculations (Google Sheet 1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4), exported to xlsx 2026-09-22 and read with openpyxl", "tab": "2026", "live_source_url": EF_URL, "artifact_path": "source_exports/Standard_Emission_Factors_export_2026-09-22.xlsx",
    "rows": {
        "B3": {"name": "Production Emissions for AECN Oil--H1 2026", "unit_C": "MTCO2e/MT Oil", "final_F": 0.1040167408, "source_G": "AECN LCA"},
        "B4": {"name": "Production Emissions for AECN Oil--H2 2026", "unit_C": "MTCO2e/MT Oil", "baseline_D": 0.1371171258, "final_F": 0.1371171258, "source_G": "FH 2026 LCA w Stack Emissions", "certify_display": 0.13712, "match": True},
        "B5": {"name": "Embodied Emissions for AECN Oil", "unit_C": "MTCO2e/MT Oil", "final_F": 0.02116, "source_G": "AECN Information, NAICS Supply Chain Emissions Factors", "certify_display": 0.02116, "match": True},
        "B6": {"name": "Truck Transport Fuel Use (Well to Wheel) -- Tanker Truck", "unit_C": "MT CO2e/t-mi", "final_F": 0.0001143, "source_G": "GLEC V3.2 2025", "certify_display": "0.1143 kgCO2e/(t*mi)", "match": True},
        "B10": {"name": "Rail Transport Fuel Use (Well to Wheel)", "unit_C": "MTCO2e/T-mi", "final_F": 2.5910374e-05, "source_G": "GLEC V3.2 2025", "certify_display": "0.02591 kgCO2e/(t*mi)", "match": True},
        "B11": {"name": "Vehicle Embodied Emissions --Tanker Truck", "unit_C": "MT CO2e/mi", "final_F": 0.0002375605888, "source_G": "GLEC V3.2 2025", "certify_display": "0.23756 kgCO2e/mi (= 0.1476 kgCO2e/km on Datapoints tab)", "match": True},
        "B13": {"name": "Vehicle Embodied Emissions --Railcar", "unit_C": "MTCO2e/mi", "final_F": 3.113066508e-05, "source_G": "GLEC V3.2 2025", "certify_display": "0.03113 kgCO2e/mi (= 0.0193 kgCO2e/km on Datapoints tab)", "match": True},
    },
    "h2_2026_aecn_tab": {"tab": "H2 2026 AECN Process Emissions", "B1_quote": "Inputs from LCA — 'FH 2026 LCA w Stack Emissions' (H1 2026 operating data), applies to H2 2026 reporting periods from the Aug 1–31 2026 RP onward", "B24_note": "I12 is the AECN pyrolysis PROCESS carbon intensity pushed to Isometric Certify (tCO2e/MT == kgCO2e/kg). Embodied CI is unchanged at 0.02116 tCO2e/MT."},
    "railcar_ee_tab": {"tab": "2026 Railcar Embodied Emissions", "B1_manufacture_MTCO2e": 65.37439668, "B4_lifetime_mi": 2100000, "B5_per_mile": 3.113066508e-05},
    "fh_2026_lca_file": {"file": "FH 2026 LCA w Stack Emissions.xlsx (Certify source #19; local copy source_exports/FH_2026_LCA_w_Stack_Emissions.xlsx read this session)", "Sheet1_I12": None, "Sheet1_I10": None, "Sheet1_I11": None},
    "_primary_source_opened": [
        {"file": "Standard Emission Factors + Calculations - 2026 tab", "action": "sheet_grid_read", "live_source_url": EF_URL, "artifact_path": "source_exports/Standard_Emission_Factors_export_2026-09-22.xlsx", "evidence": "Rows 3-13 read: F4=0.1371171258, F5=0.02116, F6=0.0001143, F10=2.5910374e-05, F11=0.0002375605888, F13=3.113066508e-05"},
        {"file": "FH 2026 LCA w Stack Emissions.xlsx", "action": "sheet_grid_read", "live_source_url": CERTIFY_URL + "?tab=sources", "artifact_path": "source_exports/FH_2026_LCA_w_Stack_Emissions.xlsx", "evidence": "Sheet1 I12 read this session (see fh_2026_lca_file)"},
    ],
}

# COBB: 'Basco Injection -- COBB' tab, export 2026-09-22; header in row 2, data rows found by scanning col A for the batch id
COBB_ROWS = [  # row, consumed_lot, bols, F=qty_consumed, G=offloaded, H=origin, I=order_line_completed_on
    (798, "2503-T_offload_1", "2503-T", 18956.06327, 18956.06327, 19190.0, "2026-09-09 11:45:58"),
    (799, "2505-T_offload_1", "2505-T", 19670.0, 19670.0, 19670.0, "2026-09-08 11:36:21"),
    (800, "2499-T_offload_1", "2499-T", 19593.81362, 19593.81362, 19710.0, "2026-09-09 11:35:43"),
    (801, "Rail_SHPX215046_8.7.2026_offload_3", "2462-R, 2463-R, 2464-R", 20810.80096, 20810.80096, 77680.0, "2026-09-05 20:02:03"),
    (802, "Rail_SHPX215046_8.7.2026_offload_4", "2462-R, 2463-R, 2464-R", 14821.22064, 14821.22064, 77680.0, "2026-09-05 20:02:03"),
    (803, "Rail_SHPX215079_8.4.2026_offload_1", "2453-R, 2454-R, 2455-R", 21799.63152, 21799.63152, 77870.0, "2026-09-04 17:30:19"),
    (804, "Rail_SHPX215079_8.4.2026_offload_2", "2453-R, 2454-R, 2455-R", 20611.22048, 20611.22048, 77870.0, "2026-09-04 17:30:19"),
    (805, "Rail_TIMX201060_7.31.2026_offload_1", "2450-R, 2451-R, 2452-R", 25228.78704, 25228.78704, 78140.0, "2026-08-27 20:02:19"),
    (806, "Rail_TIMX201060_7.31.2026_offload_2", "2450-R, 2451-R, 2452-R", 20711.01072, 20711.01072, 78140.0, "2026-08-27 20:02:19"),
    (807, "Rail_TIMX201060_7.31.2026_offload_3", "2450-R, 2451-R, 2452-R", 19667.74912, 19667.74912, 78140.0, "2026-08-27 20:02:19"),
    (808, "Rail_TIMX201060_7.31.2026_offload_4", "2450-R, 2451-R, 2452-R", 12192.55296, 12192.55296, 78140.0, "2026-08-27 20:02:19"),
]
OPS_KG = {"2499-T": 19710, "2503-T": 19190, "2505-T": 19670,
          "Rail_SHPX215046_8.7.2026_offload_3": 20810.80096, "Rail_SHPX215046_8.7.2026_offload_4": 14841.53024,
          "Rail_SHPX215079_8.4.2026_offload_1": 21799.63152, "Rail_SHPX215079_8.4.2026_offload_2": 20611.22048,
          "Rail_TIMX201060_7.31.2026_offload_1": 25228.78704, "Rail_TIMX201060_7.31.2026_offload_2": 20711.01072,
          "Rail_TIMX201060_7.31.2026_offload_3": 19667.74912, "Rail_TIMX201060_7.31.2026_offload_4": 12192.55296}

def cobb_row(r, lot, bols, f, g, h, i):
    key = lot if lot.startswith("Rail_") else bols
    ops = OPS_KG[key]
    return {"row": r, "consumed_lot_C": lot, "BOL_number_E": bols, "quantity_consumed_F": f, "offloaded_quantity_kg_G": g, "origin_quantity_kg_H": h, "order_line_completed_on_I": i,
            "ops_notes_kg": ops, "delta_G_minus_ops_kg": round(g - ops, 5), "delta_H_minus_ops_kg": (round(h - ops, 3) if not lot.startswith("Rail_") else None),
            "injection_completion_date_L": "2026-09-11", "injection_ph_M": None}

cobb = {
    "tab": "Basco Injection -- COBB", "tracker_url": COBB_URL,
    "method": "Google Sheet exported to xlsx via the Drive connector 2026-09-22 and read with openpyxl (every row scanned for the batch id, the three railcars and the three truck BOLs in any column)",
    "artifact_path": "source_exports/COBB_Bio-oil_Injection_Tracker_export_2026-09-22.xlsx",
    "row_id_at_qa": "INJ-09-2026-W2", "batch_id_col_a": "INJ-09-2026-W2_bio_oil", "rows_found_at": "798-808 (bio_oil, 11 rows); 760-797 are INJ-09-2026-W2_aqueous_fraction (out of scope)", "row_count_bio_oil": 11,
    "offloaded_quantity_kg": 20810.80096,
    "rows": [cobb_row(*r) for r in COBB_ROWS],
    "shpx215046_offloads_1_2": [{"row": 850, "batch_A": "INJ-09-2026-W3_bio_oil", "consumed_lot": "Rail_SHPX215046_8.7.2026_offload_1", "offloaded_kg": 21055.74064, "completion_L": "2026-09-18"},
                               {"row": 851, "batch_A": "INJ-09-2026-W3_bio_oil", "consumed_lot": "Rail_SHPX215046_8.7.2026_offload_2", "offloaded_kg": 20992.23776, "completion_L": "2026-09-18"}],
    "shpx215046_four_offload_sum_kg": round(21055.74064 + 20992.23776 + 20810.80096 + 14821.22064, 5),
    "shpx215046_cobb_overage_vs_bol_kg": round(21055.74064 + 20992.23776 + 20810.80096 + 14821.22064 - 77680, 5),
    "loads_tab": {"TIMX201060": {"rows": "397-399", "carrier": "Watco", "pickup": "2026-07-31", "work_order": "Rail_TIMX201060_7.31.2026", "bol_MT": [26.06, 26.02, 26.06], "railcar_total_MT": 78.14},
                  "SHPX215079": {"rows": "400-402", "carrier": "Watco", "pickup": "2026-08-04", "work_order": "Rail_SHPX215079_8.4.2026", "bol_MT": [25.99, 25.91, 25.97], "railcar_total_MT": 77.87},
                  "SHPX215046": {"rows": "409-411", "carrier": "Watco", "pickup": "2026-08-07", "work_order": "Rail_SHPX215046_8.7.2026", "bol_MT": [25.94, 25.90, 25.84], "railcar_total_MT": 77.68}},
    "findings": {
        "rail_rows": "All 8 rail rows equal the Ops Notes net to five decimals except SHPX215046 offload 4: COBB 14,821.22064 kg vs Ops/ticket 14,841.53024 kg (-20.3096 kg).",
        "truck_rows": "2503-T G/F 18,956.06327 kg vs BOL/Ops 19,190 kg (-233.937); 2499-T 19,593.81362 vs 19,710 (-116.186); 2505-T 19,670 = 19,670. Origin (H) equals the BOL on all three.",
        "completion_date": "injection_completion_date (L) = 2026-09-11 on all 11 rows = Ops Notes offload-table date (A28:A35) = Certify period end 11 Sep 2026.",
        "ph": "injection_ph (M) blank on all 11 rows; Ops Notes pH columns (Rail G28:G35, Truck H10:H12) also blank.",
        "shpx215046_offloads_1_2": "Booked under INJ-09-2026-W3_bio_oil (rows 850-851, completion 2026-09-18), so Ops M12's statement that they 'do not exist in COBB' is out of date; the four COBB offloads sum to 77,700.00 kg against 77,680 kg loaded (+20.0 kg).",
    },
    "_primary_source_opened": [{"file": "Bio-oil Injection Tracker, tab 'Basco Injection -- COBB'", "action": "sheet_grid_read", "live_source_url": COBB_URL, "artifact_path": "source_exports/COBB_Bio-oil_Injection_Tracker_export_2026-09-22.xlsx", "evidence": "rows 798-808 col A = 'INJ-09-2026-W2_bio_oil'; 3 truck + 8 rail rows read with all columns; rows 850-851 (W3) and Loads tab rows 397-411 also read"}],
}

if __name__ == "__main__":
    import openpyxl
    log = json.loads(LOG.read_text())
    lca = HERE / "source_exports" / "FH_2026_LCA_w_Stack_Emissions.xlsx"
    if lca.exists():
        ws = openpyxl.load_workbook(lca, data_only=True)["Sheet1"]
        standard_efs["fh_2026_lca_file"].update({"Sheet1_I12": ws["I12"].value, "Sheet1_I10": ws["I10"].value, "Sheet1_I11": ws["I11"].value, "Sheet1_H12": ws["H12"].value})
    log["certify_components"] = certify_components
    log["standard_efs"] = standard_efs
    log["cobb"] = cobb
    LOG.write_text(json.dumps(log, indent=2, default=str))
    print("patched certify_components, standard_efs, cobb; LCA I12 =", standard_efs["fh_2026_lca_file"]["Sheet1_I12"])
