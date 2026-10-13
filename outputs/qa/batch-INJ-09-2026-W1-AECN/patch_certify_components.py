#!/usr/bin/env python3
"""Adds certify_components (per-component modal reads) to the source-read log. Run after build_source_reads.py.
Every value below was read from a Certify component detail view opened in-session (snapshot yml / innerText txt saved alongside)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
LOG = HERE / "batch_INJ-09-2026-W1-AECN_source_reads.json"
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M2GBNMY91S0H2MB/edit?tab=components"

def opened(name, artifact, evidence, cmp_id):
    return {"file": f"Certify component detail view: {name}", "action": "modal_opened",
            "live_source_url": f"{CERTIFY_URL}&component={cmp_id}", "artifact_path": artifact, "evidence": evidence}

RAIL_MASS_KG = 155863.1042
TRUCK_MASS_KG = 277790
certify_components = {
    "injection_sequestration": {
        "component_id": "cmp_1M2GBNMY91S0D80N", "value_tCO2e": 789.580,
        "carbon_content_input": {"datapoint": "Carbon Content of Bio-oil Injected (per injection)", "value_pct": 50.4, "uncertainty_pct": 0.20164, "sources": 2},
        "mass_input": {"datapoint": "Mass of Injectant (per injection)", "value_kg": 427222.92, "uncertainty_kg": 1669.11, "sources": 31},
        "blueprint": "carbon_rich_substance_sequestration: output = product_mass * carbon_content * {co2e_of_carbon}",
        "recalc": "427.22292 t x 0.504 x 3.667 = 789.580 tCO2e",
        "carbon_uncertainty_check": "0.004 x 50.4 = 0.2016 = displayed 0.20164 (Certify shows 5 s.f.)",
        "mass_uncertainty_check": "1,669.11 / 72.57 = 23.0 discrete weighings booked; batch has 8 rail offload weighings + 14 truck BOL weighings = 22 (expected 1,596.54 kg). One extra weighing booked (conservative direction).",
        "_primary_source_opened": [opened("Injection sequestration", "certify_modal_injection_sequestration.yml", "Carbon 50.4 ±0.20164 %; Mass 427,222.92 ±1,669.11 kg", "cmp_1M2GBNMY91S0D80N")],
    },
    "pyrolysis_process_rail": {
        "component_id": "cmp_1M2GBNMY91S0RHM2", "value_tCO2e": 21.372, "share_pct": 3.02,
        "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)", "value_tCO2e_per_t": 0.13712, "sources": 3},
        "mass_input": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": 155863.1, "uncertainty_kg": 580.56, "sources": 23},
        "recalc": "155.8631042 t x 0.13712 = 21.372 tCO2e", "exact_ci_implied": round(21.372 / (RAIL_MASS_KG / 1000), 8),
        "mass_uncertainty_check": "580.56 / 72.57 = 8.0 = 8 rail offload weighings",
        "_primary_source_opened": [opened("AECN pyrolysis (from rail loads) - process emissions", "certify_modal_pyro_rail_process.txt", "CI 0.13712 tCO2e/t; Mass 155,863.1 ±580.56 kg", "cmp_1M2GBNMY91S0RHM2")],
    },
    "pyrolysis_process_truck": {
        "component_id": "cmp_1M2GBNMY91S0VVF9", "value_tCO2e": 38.091, "share_pct": 5.37,
        "ci_input": {"datapoint": "Carbon Intensity - AECN Pyrolysis Process Emissions (direct to B6)", "value_tCO2e_per_t": 0.13712, "sources": 3},
        "mass_input": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": 277790, "uncertainty_kg": 1088.55, "sources": 15},
        "recalc": "277.790 t x 0.13712 = 38.091 tCO2e", "exact_ci_implied": round(38.091 / 277.790, 8),
        "mass_uncertainty_check": "1,088.55 / 72.57 = 15.0 weighings booked; 14 truck BOL weighings expected (1,015.98 kg). One extra weighing booked (conservative direction); this is the source of the 23-vs-22 count on Mass of Injectant.",
        "_primary_source_opened": [opened("AECN pyrolysis (from truck loads) - process emissions", "certify_modal_pyro_truck_process.txt", "CI 0.13712 tCO2e/t; Mass 277,790 ±1,088.55 kg", "cmp_1M2GBNMY91S0VVF9")],
    },
    "transport_process": {
        "AECN_to_LA_direct_truck": {"component_id": "cmp_1M2GBNMY91S0EZJF", "value_tCO2e": 69.758, "ef": {"datapoint": "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from AECN to Basco", "value_mi": 2197}, "mass": {"datapoint": "Bio-Oil Mass - AECN", "value_kg": 277790, "uncertainty_kg": 1088.55}, "recalc": "277.790 t x 2,197 mi x 0.1143 kg/(t*mi) = 69,758 kg = 69.758 t",
                                    "_primary_source_opened": [opened("AECN to LA Tanker Truck Transport Process Emissions - AECN", "certify_modal_aecn_la_truck_process.yml", "EF 0.1143 kgCO2e/(t*mi); distance 2,197 mi; mass 277,790 ±1,088.55 kg", "cmp_1M2GBNMY91S0EZJF")]},
        "AECN_to_SOPOR_truck": {"component_id": "cmp_1M2GBNMY91S02ME4", "value_tCO2e": 1.915, "ef": {"value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from AECN to Sopor Quebec (truck)", "value_mi": 107.49722}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": 155863.1, "uncertainty_kg": 580.56}, "recalc": "155.8631 t x 107.49722 mi x 0.1143 = 1,915.1 kg = 1.915 t",
                                "_primary_source_opened": [opened("AECN to SOPOR Tanker Truck Transport Process Emissions", "certify_modal_aecn_sopor_truck_process.yml", "EF 0.1143; distance 107.49722 mi; mass 155,863.1 ±580.56 kg", "cmp_1M2GBNMY91S02ME4")]},
        "SOPOR_to_Opelousas_rail": {"component_id": "cmp_1M2GBNMY91S0P99S", "value_tCO2e": 8.880, "ef": {"datapoint": "Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "value": 0.02591, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from Sopor Quebec to Opelousas (rail)", "value_mi": 2199}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": 155863.1, "uncertainty_kg": 580.56}, "recalc": "155.8631 t x 2,199 mi x 0.02591 = 8,880.5 kg = 8.880 t",
                                    "_primary_source_opened": [opened("SOPOR to Opelousas Rail Transport Process Emissions", "certify_modal_rail_process.yml", "EF 0.02591 kgCO2e/(t*mi); distance 2,199 mi; mass 155,863.1 ±580.56 kg", "cmp_1M2GBNMY91S0P99S")]},
        "Opelousas_to_Basco_truck": {"component_id": "cmp_1M2GBNMY91S09Y5E", "value_tCO2e": 0.764, "ef": {"value": 0.1143, "unit": "kgCO2e/(t*mi)"}, "distance": {"datapoint": "Distance from Opelousas to B6 (truck)", "value_mi": 42.9}, "mass": {"datapoint": "Bio-Oil Mass - AECN via Rail", "value_kg": 155863.1, "uncertainty_kg": 580.56}, "recalc": "155.8631 t x 42.9 mi x 0.1143 = 764.3 kg = 0.764 t",
                                     "_primary_source_opened": [opened("Opelousas to Basco - Tanker Truck Transport Process Emissions", "certify_modal_opel_basco_truck_process.yml", "EF 0.1143; distance 42.9 mi; mass 155,863.1 ±580.56 kg", "cmp_1M2GBNMY91S09Y5E")]},
        "sum_tCO2e": round(69.758 + 1.915 + 8.880 + 0.764, 3),
        "sum_calc": "69.758 + 1.915 + 8.880 + 0.764 = 81.317",
        "distance_uncertainty": "none shown on any of the 4 legs (expected)",
    },
    "transport_embodied": {
        "AECN_to_LA_direct_truck": {"component_id": "cmp_1M2GBNMY91S0VAPT", "value_tCO2e": 7.307, "ef": {"datapoint": "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "value": 0.23756, "unit": "kgCO2e/mi"}, "distance": {"datapoint": "Aggregate Distance Transported AECN to Basco", "value_mi": 30758, "sources": 2}, "recalc": "30,758 mi x 0.23756 kg/mi = 7,306.9 kg = 7.307 t", "mass_input": "none (per-mile blueprint distance_based_ci_emissions)",
                                    "_primary_source_opened": [opened("AECN to LA Tanker Truck Transport Embodied Emissions - AECN", "certify_modal_aecn_la_truck_embodied.yml", "EF 0.23756 kgCO2e/mi; distance 30,758 mi", "cmp_1M2GBNMY91S0VAPT")]},
    },
}

if __name__ == "__main__":
    log = json.loads(LOG.read_text())
    cc = log.get("certify_components", {})
    cc.update(certify_components)
    log["certify_components"] = cc
    LOG.write_text(json.dumps(log, indent=2, default=str))
    print("patched certify_components:", list(cc.keys()))
