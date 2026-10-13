#!/usr/bin/env python3
"""Builds batch_INJ-09-2026-W4-AECN_source_reads.json.

Machine-readable sources (Ops Notes xlsx, COBB xlsx, Certify GraphQL pull, Standard EF
sheet, AECN analysis workbook, FH 2026 LCA) are parsed here directly. Values that were
read by eye from images and PDFs this session (28 scale tickets, 12 BOLs, the SGS
certificate, route maps, the Watco email, the loss example, the BCU certificate, the
EAC tracker PDF, the solids dataset PDF, the formation fluid report, the protocol) are
entered below exactly as read, each tied to the file it came from."""
import json, re, hashlib, datetime
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
OUT = HERE / "batch_INJ-09-2026-W4-AECN_source_reads.json"
SE = HERE / "source_exports"
CS = HERE / "certify_run3" / "files"
DF = HERE / "drive_w4"
import glob as _glob
def _latest_file(pat):
    return Path(sorted(_glob.glob(str(HERE / pat)))[-1])

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---------------------------------------------------------------- Ops Notes (live export)
OPS = _latest_file("source_exports/INJ-09-2026-W4_Ops_Notes_live_export_run3b_*.xlsx")
wf = openpyxl.load_workbook(OPS)
wv = openpyxl.load_workbook(OPS, data_only=True)
ar_v, ar_f = wv["AECN Rail"], wf["AECN Rail"]

def cell(ref, ws_v=ar_v, ws_f=ar_f, tab="AECN Rail"):
    v = ws_v[ref].value
    f = ws_f[ref].value
    d = {"cell": f"'{tab}'!{ref}", "value": v.isoformat() if isinstance(v, datetime.datetime) else v}
    if isinstance(f, str) and f.startswith("="):
        d["formula"] = f
    return d

railcars = []
for r in range(10, 14):
    railcars.append({
        "row": r, "railcar": ar_v[f"A{r}"].value,
        "arrival_col_B": ar_v[f"B{r}"].value.date().isoformat(),
        "bols": ar_v[f"C{r}"].value,
        "total_loaded_mt": cell(f"D{r}"), "total_loaded_kg": cell(f"E{r}"),
        "total_offloaded_kg": cell(f"F{r}"), "loss_kg": cell(f"G{r}"),
        "previously_claimed_kg": cell(f"H{r}"), "prior_rp_claimed_kg": cell(f"I{r}"),
        "aecn_sopor_mi": ar_v[f"J{r}"].value, "rail_mi": ar_v[f"K{r}"].value,
        "opel_basco_mi": cell(f"L{r}"), "notes_M": ar_v[f"M{r}"].value,
        "full_flag_P": cell(f"P{r}"), "completes_this_week_Q": ar_v[f"Q{r}"].value,
    })
bols_loaded = []
for r in range(17, 26):
    bols_loaded.append({"row": r, "date": ar_v[f"A{r}"].value.date().isoformat(), "bol": ar_v[f"B{r}"].value,
                        "bol_link_formula": ar_f[f"B{r}"].value, "railcar": ar_v[f"C{r}"].value,
                        "mass_MT": ar_v[f"D{r}"].value, "mass_kg": cell(f"E{r}")})
offload_table = []
for r in range(28, 42):
    offload_table.append({
        "row": r, "id": ar_v[f"B{r}"].value, "railcar": ar_v[f"C{r}"].value,
        "date_col_A": ar_v[f"A{r}"].value.date().isoformat(),
        "full_lb": ar_v[f"D{r}"].value, "empty_lb": ar_v[f"E{r}"].value,
        "full_link": ar_f[f"D{r}"].value, "empty_link": ar_f[f"E{r}"].value,
        "net_scaled_kg_F": ar_v[f"F{r}"].value, "pH_G": ar_v[f"G{r}"].value,
        "sparging_kg_H": ar_v[f"H{r}"].value, "filtration_kg_I": ar_v[f"I{r}"].value,
        "uncertainty_adj_kg_J": ar_v[f"J{r}"].value, "mobi_kg_K": ar_v[f"K{r}"].value,
        "alloc_aecn_sopor_mi_L": ar_v[f"L{r}"].value, "rail_alloc_mi_M": ar_v[f"M{r}"].value,
        "rail_alloc_mi_M_formula": ar_f[f"M{r}"].value if isinstance(ar_f[f"M{r}"].value, str) else "hard-coded number",
        "truck_ee_mi_N": ar_v[f"N{r}"].value, "note_O": ar_v[f"O{r}"].value,
        # cargo_kg = the mass that flows on (net less Uncertainty Adjustment), the schema field the
        # mass-chain script reads
        "cargo_kg": ar_v[f"F{r}"].value - (ar_v[f"J{r}"].value or 0),
    })
rollup = {k: cell(ref) for k, ref in [("sum_deliveries_raw_kg", "A46"), ("sum_uncertainty_adj_kg", "B46"),
          ("mass_used_kg", "C46"), ("sparging_kg", "D46"), ("filtration_kg", "E46"), ("mobi_kg", "F46"),
          ("pH", "G46"), ("aecn_sopor_alloc_mi_sum", "L42"), ("rail_alloc_mi_sum", "M42"),
          ("truck_ee_mi_sum", "N42"), ("origins_list", "M46")]}
rollup["mass_removed_rnd_K46"] = {"cell": "'AECN Rail'!K46", "value": ar_v["K46"].value,
                                  "note": "F46 formula subtracts K46; K46 is blank, so no R&D deduction this week"}
railyard_split = {"header_row_48": [ar_v["A48"].value, ar_v["B48"].value, ar_v["C48"].value],
                  "raillogix_baton_rouge": cell("C49"), "opelousas": cell("C50")}
constants = {"lb_per_kg_O3": ar_v["O3"].value, "kg_per_lb_O4": ar_v["O4"].value, "sparging_O5": ar_v["O5"].value,
             "pH_target_O6": ar_v["O6"].value, "filtration_solids_O7": cell("O7"), "bol_trips_O8": ar_v["O8"].value,
             "round_trip_O9": ar_v["O9"].value}
summ_v = wv["Summary"]
summary_aecn = {"B17_mobi": summ_v["B17"].value, "C17_sample": summ_v["C17"].value,
                "D17_date": summ_v["D17"].value.date().isoformat(), "E17_c": summ_v["E17"].value,
                "G17_c_unc": summ_v["G17"].value, "H17_testing_unc": summ_v["H17"].value,
                "I8_rail_ee_mi": summ_v["I8"].value, "J8_truck_ee_mi": summ_v["J8"].value}
truck_tab = {"A28_sum_bol_kg": wv["AECN Truck"]["A28"].value, "G28_mobi": wv["AECN Truck"]["G28"].value,
             "B10_B24_blank": all(wv["AECN Truck"][f"B{r}"].value in (None, "") for r in range(10, 25)),
             "H28_pH": wv["AECN Truck"]["H28"].value}
comments = [{"tab": ws.title, "cell": c.coordinate, "text": c.comment.text}
            for ws in wf for row in ws.iter_rows() for c in row if c.comment]

# ---------------------------------------------------------------- Certify (GraphQL full precision)
arr = json.load(open(_latest_file("source_exports/certify_graphql_GetGhgEntryQAData_run3_*.json")))
ge = json.loads([a["text"] for a in arr if a["text"].startswith("{")][0])["ghgEntry"]
components, attachment_map, site_map = {}, {}, {}
AECN_SCOPE = {"Injection sequestration", "AECN Bio-oil Loss", "AECN pyrolysis (from rail loads) - process emissions",
              "AECN pyrolysis (from rail loads) - embodied emissions",
              "AECN to SOPOR Tanker Truck Transport Process Emissions",
              "SOPOR to Opelousas Rail Transport Process Emissions",
              "Opelousas to Basco - Tanker Truck Transport Process Emissions",
              "Opelousas/Baton Rouge to Basco Tanker Truck Transport Embodied Emissions",
              "SOPOR to Opelousas/Baton Rouge Rail Transport Embodied Emissions",
              "AECN to SOPOR Tanker Truck Transport Embodied Emissions",
              "SOPOR to Baton Rouge Rail Process Emissions", "Baton Rouge to Basco Tanker Truck Process Emissions",
              "BCU - Transport Process"}
for cg in ge["componentGroups"]:
    for ca in cg["componentAttributions"]:
        c = ca["component"]
        q = ca["carbonFlux"]["co2eTransferred"]
        val_t = q["magnitude"] / (1000 if q["unit"].startswith("kg") else 1)
        inputs = {}
        for s in c["inputData"]["scalarInputs"]:
            dp = s["dataPoint"]
            files = [r["source"]["originalFilename"] or r["source"]["displayName"] for r in dp["references"]]
            inputs[s["blueprintInput"]["inputKey"]] = {
                "datapoint": dp["displayName"], "datapoint_id": dp["id"], "value": dp["quantity"]["magnitude"],
                "unit": dp["quantity"]["unit"], "sd": dp["quantity"]["standardDeviation"], "sources": files}
            key = dp["displayName"]
            if key in ("Mass of load", "Distance traveled", "Constant CO₂ reduction", "Constant emissions"):
                key = f"{key} [{c['displayName']}]"
            (attachment_map if c["displayName"] in AECN_SCOPE else site_map)[key] = files
        components[c["displayName"]] = {"id": c["id"], "group": cg["displayName"], "type": c["componentType"],
                                        "blueprint": c["componentBlueprint"]["key"], "direction": ca["carbonFlux"]["direction"],
                                        "value_t": val_t, "inputs": inputs, "in_batch_scope": c["displayName"] in AECN_SCOPE}
acts_all = sum(v["value_t"] for v in components.values() if v["type"] == "ACTIVITY")
acts_aecn = sum(v["value_t"] for v in components.values() if v["type"] == "ACTIVITY" and v["in_batch_scope"])
adj_all = sum(v["value_t"] for v in components.values() if v["type"] == "ADJUSTMENT")
seq = components["Injection sequestration"]["value_t"]
enum = json.load(open(HERE / "certify_run3" / "certify_sources_enumeration_run3.json"))

# ---------------------------------------------------------------- COBB
cw = openpyxl.load_workbook(_latest_file("source_exports/COBB_Bio-oil_Injection_Tracker_export_run3_*.xlsx"), read_only=True, data_only=True)
crow = list(cw["Basco Injection -- COBB"].iter_rows(values_only=True))
hdr = crow[1]
def cobb_rows(pred):
    out = []
    for i, r in enumerate(crow, 1):
        if i > 2 and pred(r):
            d = {"row": i}
            for j, h in enumerate(hdr):
                if h and j < len(r) and r[j] not in (None, "") and h not in ("purchase_order_link", "offload_order_link", "weighing_order_link"):
                    v = r[j]
                    d[h] = v.isoformat() if isinstance(v, datetime.datetime) else v
            out.append(d)
    return out
w4_all = cobb_rows(lambda r: r[0] == "INJ-09-2026-W4_bio_oil")
blocks = {}
for d in w4_all:
    blocks.setdefault(d.get("Import Time"), []).append(d["row"])
latest_import = max(blocks)
latest = [d for d in w4_all if d.get("Import Time") == latest_import]
w2_215079 = cobb_rows(lambda r: r[0] == "INJ-09-2026-W2_bio_oil" and "SHPX215079" in str(r[2]))
loads = list(cw["Loads"].iter_rows(values_only=True))
lh = loads[0]
load_rows = []
for i, r in enumerate(loads, 1):
    if r[2] in ("2497-R", "2498-R", "2500-R", "2459-R", "2460-R", "2461-R", "2465-R", "2466-R", "2467-R", "2453-R", "2454-R", "2455-R"):
        load_rows.append({"row": i, "BOL": r[2], "COA": r[3], "carrier": r[10], "asset": r[11],
                          "pickup": r[13].date().isoformat() if r[13] else None, "work_order": r[15],
                          "actual_loaded_mt": r[16], "railcar_total_mt": r[18], "delivery_location": r[9]})

# ---------------------------------------------------------------- Standard EF sheet (live export)
sv = openpyxl.load_workbook(_latest_file("source_exports/Standard_Emission_Factors_export_run3_*.xlsx"), data_only=True)["2026"]
def efrow(r):
    return {"row": r, "name": sv[f"B{r}"].value, "unit": sv[f"C{r}"].value, "baseline_D": sv[f"D{r}"].value,
            "final_F": sv[f"F{r}"].value, "source_G": sv[f"G{r}"].value}

# ---------------------------------------------------------------- MRV AECN analysis
mw = openpyxl.load_workbook(SE / "MRV_AECN_Analysis.xlsx_run3.xlsx", read_only=True, data_only=True)
stats = {r[0]: r for r in mw["Summary Statistics"].iter_rows(values_only=True) if r and r[0]}
mean_c, sd_c, n_c = stats["Mean"][1], stats["Std Dev"][1], stats["Count"][1]

# ---------------------------------------------------------------- FH 2026 LCA (Certify copy)
fh = openpyxl.load_workbook(CS / "src_1M1MFJCSF1S0P0KB_FH_2026_LCA_w_Stack_Emissions.xlsx", data_only=True)["Sheet1"]

# ---------------------------------------------------------------- scale tickets (read as page images)
T = {
 "SHPX215053_offload_1": [("1186426265990", "2026-09-22", "16:19", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH1", "KL720", 10240, 31840, 31720, 73800, "SHPX215053 01", "LA01"),
                          ("1124426266608", "2026-09-23", "07:00", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720 RL", 9500, 11320, 8580, 29400, "SHPX215053 01", "LA02")],
 "SHPX215053_offload_2": [("1186426265989", "2026-09-22", "16:16", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH2", "KL188 RL", 11900, 28480, 33060, 73440, "SHPX 215053 OFF 2", "LA01"),
                          ("1186426266998", "2026-09-23", "07:08", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH2", "KL188 RL", 10480, 9740, 8420, 28640, "SHPX 215053 OFF 2 (reweigh of 1186426265989, fee $5.25)", "LA01")],
 "SHPX215053_offload_3": [("1124426266610", "2026-09-23", "11:43", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188 RL", 12100, 29460, 33640, 75200, "SHPX 215053 OFF 3", "LA01"),
                          ("1186426267015", "2026-09-24", "05:08", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH2", "KL188", 9580, 11260, 7840, 28680, "SHPX215053 O3", "LA02")],
 "SHPX215053_offload_4": [("1186426266003", "2026-09-23", "12:18", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH1", "KL720 RL", 10120, 27220, 26840, 64180, "SHPX215053 04", "LA02"),
                          ("1186426267016", "2026-09-24", "05:09", "1864", "LOVES, US HWY 190, PORT BARRE LA", "CH1", "KL720", 0, 21140, 8500, 29640, "SHPX215053", "LA O2")],
 "SHPX215039_offload_1": [("1124426261599", "2026-09-18", "13:18", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", 9940, 32360, 32200, 74500, "SHPX215039 O1", "LA01"),
                          ("1312226261666", "2026-09-18", "16:37", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 9360, 11300, 8020, 28680, "SHPX215039 O1", "LA01")],
 "SHPX215039_offload_2": [("1124426261598", "2026-09-18", "13:16", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", 0, 23800, 54820, 78620, "SHPX215039 O1", "LA O1"),
                          ("1312226261663", "2026-09-18", "16:00", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH1", "KL720", 0, 20900, 8580, 29480, "SHPX215039 O1", "LA O1")],
 "SHPX215039_offload_3": [("1124426262601", "2026-09-19", "12:34", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", 0, 10040, 60580, 70620, "SHPX215039 O3", "LA O1"),
                          ("1312226262682", "2026-09-19", "16:17", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH1", "KL720", 0, 17920, 11360, 29280, "SHPX215039 O3", "LA O1")],
 "SHPX215039_offload_4": [("1124426262600", "2026-09-19", "12:30", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", 9940, 27040, 26360, 63340, "SHPX215039 O4", "LA01"),
                          ("1312226262679", "2026-09-19", "15:39", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 9440, 11320, 7860, 28620, "SHPX215039 O4", "LA01")],
 "SHPX215091_offload_1": [("1312226260630", "2026-09-17", "11:22", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 10000, 32280, 31920, 74200, "SHPX215091 O1", "LA01"),
                          ("1312226260636", "2026-09-17", "13:23", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 9420, 11380, 7880, 28680, "SHPX215091 O1 (reweigh of 1312226260630, fee $5.25)", "LA01")],
 "SHPX215091_offload_2": [("1124426260591", "2026-09-17", "11:57", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", 0, 23780, 48420, 72200, "SHPX215091 O2", "LA O1"),
                          ("1312226260638", "2026-09-17", "14:00", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH1", "KL720", 0, 18300, 10940, 29240, "SHPX215091 O2", "LA O1")],
 "SHPX215091_offload_3": [("1312226260641", "2026-09-17", "16:25", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 9940, 33060, 33060, 76060, "SHPX215091 O3", "LA01"),
                          ("1312226261651", "2026-09-18", "06:44", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH2", "KL188", 9400, 11280, 7880, 28560, "SHPX215091 O3 (reweigh of 1312226260641, fee $5.25)", "LA01")],
 "SHPX215091_offload_4": [("1124426260594", "2026-09-17", "16:11", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", 0, 9940, 54620, 64560, "SHPX215091 O4", "LA O1"),
                          ("1312226261653", "2026-09-18", "07:02", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH1", "KL720", 9680, 11400, 8500, 29580, "SHPX215091 O4", "LA O1")],
 "SHPX215079_offload_3": [("1124426248529", "2026-09-05", "09:29", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL192", 10320, 32960, 32520, 75800, "SHPX215079 3", None),
                          ("1312226248408", "2026-09-05", "12:35", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA", "CH1", "KL192", 9580, 11420, 8200, 29200, "SHPX215079 3", None)],
 "SHPX215079_offload_4": [("1124426248533", "2026-09-05", "14:20", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", 12480, 21420, 26800, 60700, "SHPX215079 OFFLOAD 4", None),
                          ("1124426249537", "2026-09-06", "07:50", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", 9340, 11060, 7860, 28260, "SHPX215079 4", None)],
}
CERT_TICKET_FILE = {p.name.split("_", 2)[2]: p.name for p in CS.glob("src_*Ticket*.pdf")}
DATE_TAG = {"SHPX215053": "9.1.2026", "SHPX215039": "8.6.2026", "SHPX215091": "8.11.2026", "SHPX215079": "8.4.2026"}
offloads, primary_tix, pairs = {}, [], []
for k, (full, empty) in T.items():
    car, n = k.split("_offload_")
    def tk(t, kind):
        fname = f"{kind}_Ticket_Rail_{car}_{DATE_TAG[car]}_offload_{n}.pdf"
        return {"ticket_no": t[0], "date": t[1], "time": t[2], "scale": t[3], "location": t[4], "tractor": t[5],
                "trailer": t[6], "steer_lb": t[7], "drive_lb": t[8], "trailer_axle_lb": t[9], "gross_weight_lb": t[10],
                "axle_sum_lb": t[7] + t[8] + t[9], "commodity_label": t[11], "delivery_site": t[12],
                "certify_file": "certify_run3/files/" + CERT_TICKET_FILE[fname], "drive_file": f"drive_w4/Scale Tickets/{car}/Offload {n}/{fname}"}
    f, e = tk(full, "Full"), tk(empty, "Empty")
    net_lb = f["gross_weight_lb"] - e["gross_weight_lb"]
    offloads[k] = {"railcar": car, "offload": int(n), "full_ticket": f, "empty_ticket": e,
                   "computed_net_lb": net_lb, "computed_net_kg": round(net_lb * 0.453592, 6)}
    same_trailer = f["trailer"].split()[0] == e["trailer"].split()[0]
    pairs.append({"offload": k, "tractor_full": f["tractor"], "tractor_empty": e["tractor"], "trailer_full": f["trailer"],
                  "trailer_empty": e["trailer"], "tractor_match": f["tractor"] == e["tractor"], "trailer_match": same_trailer})
    for t, kind in ((f, "Full"), (e, "Empty")):
        primary_tix.append({"file": t["drive_file"], "action": "image_read", "artifact_path": t["drive_file"],
                            "evidence": f"{kind} ticket {t['ticket_no']} {t['date']} {t['time']} scale {t['scale']} {t['location']}; "
                                        f"tractor {t['tractor']} trailer {t['trailer']}; steer {t['steer_lb']} drive {t['drive_lb']} trailer {t['trailer_axle_lb']}; GROSS {t['gross_weight_lb']} LB; '{t['commodity_label']}'"})
_c3 = json.load(open(HERE / "certify_run3" / "certify_vs_drive_compare_run3.json"))
cmp = {"compared": len(_c3["tickets"]), "identical": sum(v["identical"] for v in _c3["tickets"].values())}
_t3 = json.load(open(HERE / "run3_reads" / "scale_tickets_run3.json"))["offloads"]
offloads_w2 = {k: v for k, v in _t3.items() if k.startswith("W2_")}
# the run-3 typed reads and the T table above must agree field by field
for _k, _v in offloads.items():
    for _side in ("full_ticket", "empty_ticket"):
        for _f in ("ticket_no", "date", "time", "scale", "tractor", "trailer", "steer_lb", "drive_lb", "trailer_axle_lb", "gross_weight_lb"):
            assert _v[_side][_f] == _t3[_k][_side][_f], (_k, _side, _f)

# ---------------------------------------------------------------- BOLs (all pages read as images)
B = {
 "2497-R": dict(file="bols/BOL_2497-R.pdf", drive_title="Documents camion 2497-R.pdf", railcar="SHPX215053", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-31", truck_id="927", tanker_id="21607", coa_p1="RS2-260828-1", coa_shipping="RS2-260828-1", prod_period="#08-2026", driver="Dany Michaud", p1_gal=5700, p1_lb=56365, p1_l=21573, p1_kg_est=25564, p1_mt_est=25.56, tare_kg=19210, full_kg=45120, delivered_kg=25910, delivered_mt=25.91, litres_60F=21648, qty_shipped_mt=25.91, density_60F=1.1969, weigh_ticket="PC0039580", weigh_in_out="2026/08/31 04:59-06:06", masse_brute=45120, masse_tare=19210, masse_nette=25910, page_order="p1 BOL, p2 weighbridge, p3 Shipping Details, p4 TSCA (31/08/2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2498-R": dict(file="bols/BOL_2498-R.pdf", drive_title="Documents camion 2498-R.pdf", railcar="SHPX215053", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-31", truck_id="2416", tanker_id="22095", coa_p1="RS2-260825-1", coa_shipping="RS2-260828-1", prod_period="#08-2026", driver="Jean-Sebastien Gasse", p1_gal=5731, p1_lb=56674, p1_l=21691, p1_kg_est=25704, p1_mt_est=25.70, tare_kg=19280, full_kg=45010, delivered_kg=25730, delivered_mt=25.73, litres_60F=21497, qty_shipped_mt=25.73, density_60F=1.1969, weigh_ticket="PC0039581", weigh_in_out="2026/08/31 07:43-09:03", masse_brute=45010, masse_tare=19280, masse_nette=25730, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (08-31-2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2500-R": dict(file="bols/BOL_2500-R.pdf", drive_title="Documents camion 2500-R.pdf", railcar="SHPX215053", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-31", truck_id="927", tanker_id="21607", coa_p1="RS2-260828-1", coa_shipping="RS2-260828-1", prod_period="#08-2026", driver="Dany Michaud", p1_gal=5759, p1_lb=56953, p1_l=21798, p1_kg_est=25831, p1_mt_est=25.83, tare_kg=19050, full_kg=44980, delivered_kg=25930, delivered_mt=25.93, litres_60F=21664, qty_shipped_mt=25.93, density_60F=1.1969, weigh_ticket="PC0039585", weigh_in_out="2026/08/31 11:18-12:24", masse_brute=44980, masse_tare=19050, masse_nette=25930, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (08-31-2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2459-R": dict(file="bols/BOL_2459-R.pdf", railcar="SHPX215039", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-04", truck_id="2114", tanker_id="22095", coa_p1="RS1-260803-1", coa_shipping="RS1-260803-1", prod_period="#08-2026", driver="R. J. Desterres", p1_gal=5791, p1_lb=57272, p1_l=21920, p1_kg_est=25975, p1_mt_est=25.98, tare_kg=19120, full_kg=44980, delivered_kg=25860, delivered_mt=25.86, litres_60F=21566, qty_shipped_mt=25.86, density_60F=1.1991, weigh_ticket="PC0039394", weigh_in_out="2026/08/04 17:51-18:53", masse_brute=44980, masse_tare=19120, masse_nette=25860, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (08/04/2026), p5 Charm PO", po_seller_signed=True, in_certify=False),
 "2460-R": dict(file="bols/BOL_2460-R.pdf", railcar="SHPX215039", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-04", truck_id="2416", tanker_id="21607", coa_p1="RS3-260804-1", coa_shipping="RS3-260804-1", prod_period="#08-2026", driver="J.S.Gasse", p1_gal=5703, p1_lb=56394, p1_l=21584, p1_kg_est=25577, p1_mt_est=25.58, tare_kg=19540, full_kg=45460, delivered_kg=25920, delivered_mt=25.92, litres_60F=21652, qty_shipped_mt=25.92, density_60F=1.1971, weigh_ticket="PC0039396", weigh_in_out="2026/08/04 21:43-22:50", masse_brute=45460, masse_tare=19540, masse_nette=25920, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (August 4th 2026), p5 Charm PO", po_seller_signed=True, in_certify=False),
 "2461-R": dict(file="bols/BOL_2461-R.pdf", railcar="SHPX215039", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-05", truck_id="356", tanker_id="22095", coa_p1="RS3-260804-1", coa_shipping="RS3-260804-1", prod_period="#08-2026", driver="Alex Langevin", p1_gal=5760, p1_lb=56964, p1_l=21802, p1_kg_est=25835, p1_mt_est=25.84, tare_kg=19270, full_kg=45130, delivered_kg=25860, delivered_mt=25.86, litres_60F=21602, qty_shipped_mt=25.86, density_60F=1.1971, weigh_ticket="PC0039405", weigh_in_out="2026/08/05 16:50-18:05", masse_brute=45130, masse_tare=19270, masse_nette=25860, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (05-08-2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2465-R": dict(file="bols/BOL_2465-R.pdf", railcar="SHPX215091", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-06", truck_id="2416", tanker_id="22095", coa_p1="RS1-260806-1", coa_shipping="RS1-260806-1", prod_period="#08-2026", driver="Jean Sebastien Gasse", p1_gal=5838, p1_lb=57737, p1_l=22098, p1_kg_est=26186, p1_mt_est=26.19, tare_kg=19370, full_kg=45390, delivered_kg=26020, delivered_mt=26.02, litres_60F=21720, qty_shipped_mt=26.02, density_60F=1.1980, weigh_ticket="PC0039418", weigh_in_out="2026/08/06 20:22-21:35", masse_brute=45390, masse_tare=19370, masse_nette=26020, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (06/08/2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2466-R": dict(file="bols/BOL_2466-R.pdf", drive_title="Document Camion 2466-R - Corr.pdf", railcar="SHPX215091", form="TR95-012-R00 (old five-page package, corrected)", pages=5, date="2026-08-07", truck_id="2416", tanker_id="22095", coa_p1="RS1-260806-1", coa_shipping="RS1-260806-1", prod_period="#08-2026", driver="J.S. Gasse", p1_gal=5794, p1_lb=57301, p1_l=21931, p1_kg_est=25988, p1_mt_est=25.99, tare_kg=19290, full_kg=45150, delivered_kg=25860, delivered_mt=25.86, litres_60F=21586, qty_shipped_mt=25.86, density_60F=1.1980, weigh_ticket="PC0039421", weigh_in_out="2026/08/07 12:53-14:04", masse_brute=45150, masse_tare=19290, masse_nette=25860, page_order="p1 BOL headed '***Correction densité et litres finaux / ***Correction of density and final liters', p2 Shipping Details with density hand-corrected to 1.1980 and litres at 60F to 21 586 (struck values circled), p3 weighbridge, p4 TSCA (August 7 2026), p5 Charm PO (seller signature blank); all 5 pages read 2026-10-07 (run 3)", po_seller_signed=False, in_certify=False),
 "2467-R": dict(file="bols/BOL_2467-R.pdf", railcar="SHPX215091", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-10", truck_id="2114", tanker_id="22095", coa_p1="RS1-260810-1", coa_shipping="RS1-260810-1", prod_period="#08-2026", driver="René Jr. Desterre", p1_gal=5753, p1_lb=56896, p1_l=21776, p1_kg_est=25805, p1_mt_est=25.80, tare_kg=19330, full_kg=45220, delivered_kg=25890, delivered_mt=25.89, litres_60F=21634, qty_shipped_mt=25.89, density_60F=1.1967, weigh_ticket="PC0039436", weigh_in_out="2026/08/10 19:03-20:11", masse_brute=45220, masse_tare=19330, masse_nette=25890, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (10-08-2026), p5 Charm PO", po_seller_signed=False, in_certify=False),
 "2453-R": dict(file="bols/BOL_2453-R.pdf", railcar="SHPX215079", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-07-30", truck_id="2416", tanker_id="22095", coa_p1="RS1-260728-1", coa_shipping="RS1-260728-1", prod_period="#0X-2026", driver="J.S. Gasse", p1_gal=5740, p1_lb=56768, p1_l=21727, p1_kg_est=25746, p1_mt_est=25.75, tare_kg=19440, full_kg=45430, delivered_kg=25990, delivered_mt=25.99, litres_60F=21595, qty_shipped_mt=25.99, density_60F=1.2035, weigh_ticket="PC0039365", weigh_in_out="2026/07/30 15:01-16:08", masse_brute=45430, masse_tare=19440, masse_nette=25990, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (30 juillet 2026), p5 Charm PO", po_seller_signed=False, in_certify=True),
 "2454-R": dict(file="bols/BOL_2454-R.pdf", railcar="SHPX215079", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-03", truck_id="2114", tanker_id="22095", coa_p1="RS1-260803-1", coa_shipping="RS1-260803-1", prod_period="#08-2026", driver="René Jr.Desterres", p1_gal=5725, p1_lb=56616, p1_l=21669, p1_kg_est=25678, p1_mt_est=25.68, tare_kg=19280, full_kg=45190, delivered_kg=25910, delivered_mt=25.91, litres_60F=21608, qty_shipped_mt=25.91, density_60F=1.1991, weigh_ticket="PC0039377", weigh_in_out="2026/08/03 10:39-11:45", masse_brute=45190, masse_tare=19280, masse_nette=25910, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (08/03/2026), p5 Charm PO", po_seller_signed=True, in_certify=True),
 "2455-R": dict(file="bols/BOL_2455-R.pdf", railcar="SHPX215079", form="TR95-012-R00 (old five-page package)", pages=5, date="2026-08-03", truck_id="2416", tanker_id="21607", coa_p1="RS1-260803-1", coa_shipping="RS1-260803-1", prod_period="#08-2026", driver="J.S. Gasse", p1_gal=5736, p1_lb=56729, p1_l=21712, p1_kg_est=25729, p1_mt_est=25.73, tare_kg=19130, full_kg=45100, delivered_kg=25970, delivered_mt=25.97, litres_60F=21658, qty_shipped_mt=25.97, density_60F=1.1991, weigh_ticket="PC0039384", weigh_in_out="2026/08/03 17:32-19:03", masse_brute=45100, masse_tare=19130, masse_nette=25970, page_order="p1 BOL, p2 Shipping Details, p3 weighbridge, p4 TSCA (08/03/2026), p5 Charm PO", po_seller_signed=True, in_certify=True),
}
SHIP_TO = "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau, Québec G4Z 2L6"
SHIP_FROM = "BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec G5B 2V9"
per_bol, primary_bols, ties = {}, [], {}
for b, d in B.items():
    d = dict(d); d["bol"] = b; d["ship_to"] = SHIP_TO; d["ship_from"] = SHIP_FROM; d["carrier"] = "Transport Baie-Comeau"; d["customer_po"] = "Q42025"
    d["sha256"] = sha(HERE / d["file"])
    per_bol[b] = d
    ties[b] = {"full_minus_tare_eq_delivered": d["full_kg"] - d["tare_kg"] == d["delivered_kg"],
               "delivered_div_1000_eq_qty_shipped": round(d["delivered_kg"] / 1000, 2) == d["qty_shipped_mt"],
               "masse_nette_eq_delivered": d["masse_nette"] == d["delivered_kg"],
               "litres_x_density_kg": round(d["litres_60F"] * d["density_60F"], 2),
               "litres_x_density_minus_delivered_kg": round(d["litres_60F"] * d["density_60F"] - d["delivered_kg"], 2),
               "rounding_allowance_kg": round(d["litres_60F"] * 0.00005, 2)}
    primary_bols.append({"file": d["file"], "action": "pdf_read", "artifact_path": d["file"],
                         "evidence": f"all {d['pages']} pages read as images; Qty shipped {d['qty_shipped_mt']} MT; tare {d['tare_kg']} full {d['full_kg']} delivered {d['delivered_kg']} kg; weighbridge {d['weigh_ticket']} nette {d['masse_nette']}"})
per_railcar = {}
for car in ("SHPX215053", "SHPX215039", "SHPX215091", "SHPX215079"):
    bs = [b for b, d in per_bol.items() if d["railcar"] == car]
    per_railcar[car] = {"bols": bs, "sum_qty_shipped_mt": round(sum(per_bol[b]["qty_shipped_mt"] for b in bs), 2),
                        "sum_delivered_kg": sum(per_bol[b]["delivered_kg"] for b in bs)}

def _copy_summary(p):
    v = openpyxl.load_workbook(p, data_only=True)["AECN Rail"]
    fm = openpyxl.load_workbook(p)
    return {"K10_rail_mi": v["K10"].value, "L10_truck_mi": v["L10"].value, "M28_rail_alloc": v["M28"].value, "M42_rail_alloc_sum": v["M42"].value,
            "N42_truck_ee_sum": v["N42"].value, "rows_48_50_railyard_split": "present" if v["A48"].value else "absent",
            "comments": [{"tab": ws.title, "cell": c.coordinate, "text": c.comment.text} for ws in fm for row in ws.iter_rows() for c in row if c.comment]}

# ---------------------------------------------------------------- assemble
log = {
 "_schema_version": "1.0",
 "batch_id": "INJ-09-2026-W4-AECN",
 "oil_type": "AECN",
 "injection_site": "Basco 6",
 "certify_removal_url": "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M3Z5YJN51S0SN1Q/edit",
 "certify_removal_id": "rmv_1M3Z5YJN51S0SN1Q",
 "drive_folder_url": "https://drive.google.com/drive/u/0/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0",
 "qa_session_T0_utc": "2026-10-07T01:10:10Z",
 "qa_run": {"run": 3, "run1": "2026-10-06T18:20:56Z (files in run1_2026-10-06_superseded/)", "run2": "2026-10-06T22:46:58Z (files in run2_2026-10-07_superseded/)",
            "why_run3": "run 2's pre-flight did not open qa_active_batches.json before Gate 1 (skill pre-flight step 5); run 3 restarted from kickoff"},
 "preflight": {
   "knowledge_base": {"file": "knowledge-base/Charm_Isometric_Knowledge_Base.md", "lines": 1300, "read": "in full, two reads (01:10:32Z and 01:10:38Z), before Gate 1", "read_utc": "2026-10-07T01:10:38Z"},
   "lessons_learned": {"file": "skills/qa/batch-qa-aecn/references/lessons_learned.md", "read": "in full, Failure Categories 1-14", "read_utc": "2026-10-07T01:10:33Z"},
   "checklist_structure": {"file": "skills/qa/batch-qa-aecn/references/checklist_structure.md", "read": "in full", "read_utc": "2026-10-07T01:10:34Z"},
   "failure_categories_printed": ["FC1 primary sources: full Certify Sources list, column A of every COBB row, all 28 tickets, every component window",
     "FC2 missing evidence is a Fail; a generic file name such as 'image (44).png' is a Flag", "FC3 every evidence note quotes the values read",
     "FC4 no process notes and no quotes from Max in the checklist", "FC5 every correction applies to its whole class",
     "FC6 2026 tab of the emission-factor sheet at full precision, never Certify's rounded display", "FC7 no statuses until the source-read log is complete",
     "FC8 embodied per mile, process per tonne-mile", "FC9 each removal counts only its own oil, ±72.57 kg per weighing; offloads outnumber BOLs on each closing railcar",
     "FC10 every finding cites a log key; 'blocked' needs three tried routes; the audit script runs",
     "FC11 on a railcar's last offload, run the balance check before calling a mass gap an error (SHPX215079)",
     "FC12 follow every finding through every row it touches", "FC13 a difference from sister weeks in the same period is at least a Flag",
     "FC14 read the September VVB guidance first, and read Ops Notes cell comments"],
   "failure_categories_printed_utc": "2026-10-07T01:11:11Z",
   "failure_categories_printed_note": "printed as a turn-final chat message at 01:11:11Z and re-sent whole at 01:11:27Z (citation-hook re-delivery), before any batch source was opened; confirmed present in the session record at 01:11:47Z"},
 "registry_check": {"file": "skills/qa/batch-qa-aecn/qa_active_batches.json", "read_utc": "2026-10-07T01:10:43Z", "entry_pulled_utc": "2026-10-07T01:10:50Z",
                    "INJ-09-2026-W4_entry": "present: run-1 entry, status 'gates_blocked_pending_max_step_exceptions', T0 2026-10-06T18:20:56Z",
                    "decision": "run 3 starts fresh rather than resuming run 1's entry; prior sessions are navigation aids, not verification",
                    "sister_context": "re-read 2026-10-07T02:21:35Z: INJ-09-2026-W1 (rmv_1M2GBNMY91S0H2MB) closed; INJ-09-2026-W2 (rmv_1M2RKR58N1S0F02M) awaiting_garrett; INJ-09-2026-W3 (rmv_1M3MMSA7X1S0R377) awaiting_garrett"},
 "inputs_confirmed": {
   "batch_id": "INJ-09-2026-W4-AECN",
   "inputs_given": "'Certify:' and 'Folder:' lines both carry Drive folder 1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0 ('W4'); no Certify link was given",
   "certify_removal_url": "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M3Z5YJN51S0SN1Q/edit",
   "certify_identification": "removal id taken from the registry entry read at 01:10:50Z; re-confirmed at 01:22:52Z by Isometric ListProjectGhgEntries (project prj_1HZSSWBQM1S08H83, 12 newest): three entries dated 2026-09-19 to 2026-09-25 - rmv_1M3Z5YJN51S0SN1Q (AECN rail components + site emissions, 362.07 t), rmv_1M3T2J3V51S0NCHH (Kerry, 37.73 t), rmv_1M3SG7D701S0HZ1Z (QOWV, 4.08 t); the AECN one is in scope",
   "drive_folder_url": "https://drive.google.com/drive/u/0/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0",
   "reporting_period_certify": f"{ge['started']} to {ge['completed']}",
   "ops_week": "2026-09-18 to 2026-09-25 ('AECN Rail'!B3:B4)",
   "vvb_week_window": "18 – 25 September 2026",
   "aecn_only": True,
   "aecn_only_basis": "Every oil-related component on rmv_1M3Z5YJN51S0SN1Q is AECN (pyrolysis from rail loads, AECN Bio-oil Loss, AECN rail/truck transport legs, Injection sequestration on Bio-Oil Mass - AECN via Rail); Kerry and QOWV have their own removals. The removal also carries the September site emissions (electricity, argon electricity, diesel, gasoline, E-85, additional transport, support travel, embodied, methanol, spare parts) and their BCUs, which the site-emissions QA covers, not this batch QA.",
   "confirmed_utc": "2026-10-07T01:11:11Z"},
 "vvb_guidance": {
   "_primary_source_opened": [{"file": "VVB Guidance September 1 - September 30 (Google Doc 1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc, owner garrett.lutz@, modified 2026-10-05T07:16:43Z)",
       "action": "csv_exported", "live_source_url": "https://docs.google.com/document/d/1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc/edit",
       "artifact_path": "source_exports/VVB_Guidance_September_1-30_run3.txt",
       "evidence": "plain-text export (Drive connector 01:11:58Z) read in full at 01:12:12Z, before any other batch source: the W4 folder copy began 01:12:23Z, Ops Notes 01:20:47Z, COBB 01:21:43Z, Certify 01:22:52Z; 11,181 bytes, sha256 9bcc4e72ae019f4e..., identical to the 2026-10-06 export"}],
   "search": "Drive title contains 'VVB Guidance' (01:11:53Z); the September 1 - September 30 doc covers the 2026-09-19 to 2026-09-25 removal",
   "sections": ["AECN Rail — Oil Withdrawn for Research and Development (Week 3, INJ-09-2026-W3)",
                "AECN Rail — New Rail Destination at Baton Rouge (Railcar SHPX215053, Week 4, INJ-09-2026-W4)",
                "AECN Rail — Bio-oil Loss", "Site Gasoline — E-85 Fills Quantified at an E-85 Emission Factor",
                "Site Diesel — Rail-Yard Air Compressor Fuel", "Immateriality of Argon Transport and removal from calculations"],
   "quote_br_change": "Beginning in late September 2026, AECN railcars are routed to a transload rail spur in Baton Rouge, Louisiana, instead of the rail yard at Opelousas, Louisiana. At Baton Rouge the oil is transferred from the railcar to tanker trucks and hauled by road to the injection site. The first transload at Baton Rouge took place on 22 September 2026.",
   "quote_br_scope": "In this Reporting Period, one railcar used the new route: SHPX215053, offloaded in Week 4 (INJ-09-2026-W4, 18 – 25 September 2026). Every other railcar in this Reporting Period was received at Opelousas under the existing routing.",
   "quote_br_method": "Each leg uses this railcar’s own mass and its own route distance, so the Opelousas distances are not applied to SHPX215053 and the Baton Rouge distances are not applied to any other railcar. The tanker leg is counted as a round trip, consistent with the treatment of the Opelousas leg.",
   "quote_br_values": "Rail distance from the loading origin to Baton Rouge: 2,152 (map evidence is added in drive). Tanker distance from Baton Rouge to the injection site: 136 mi one way, doubled for the round trip. Mass basis: the same scale-ticket net masses and loading Bill of Lading masses used for every other railcar.",
   "quote_br_evidence": "Week 4 ops notes, AECN Rail tab (Section 1 for the railcar’s route distances, Section 3 for the four offloads); certified truck scale tickets for each offload; loading Bills of Lading.",
   "quote_loss_purpose": "The difference is bio-oil that Charm received and transported but did not inject. Its upstream emissions, pyrolysis and transport from the loading origin to the rail yard, remain attributable to Charm and are reported on each AECN rail removal as a separate component, AECN Bio-oil Loss.",
   "quote_loss_method": "Pyrolysis and all transport components on the removal are calculated on the delivered mass: scale-ticket net mass, less any Uncertainty Adjustment. The lost mass, loaded mass minus delivered mass, is quantified per railcar and recognised in the week in which the railcar’s final offload is completed; a railcar that is still being offloaded carries no loss until it closes. Where a railcar’s scale tickets exceed its Bills of Lading, the excess is removed from the final offload through the Uncertainty Adjustment and the railcar’s loss is zero.",
   "quote_loss_factor": "Loss emissions apply the same AECN pyrolysis carbon intensities (process and embodied) and the same loading-origin-to-rail-yard transport emissions used for the delivered oil, pro-rated to the lost mass, which equates to approximately 0.229 t CO₂e per tonne of oil lost.",
   "quote_loss_evidence": "A platform-generated calculation record cannot yet be attached to each specific Certify datapoint; until it can, we have an example calculation attached to show the method.",
   "quote_compressor": "Rail offloads (Weeks 1 – 4; ten railcars, four offloads each)        40",
   "no_tare_substitution_section": "the doc holds no standard-empty-weight or ticket-substitution section; no W4 cell comment cites one",
   "no_SHPX215079_timing_note": "the doc does not mention SHPX215079 or the 2026-09-05/06 weighing of its offloads 3-4",
   "out_of_scope_sections": "E-85, compressor diesel and argon sections concern site emissions (site-emissions QA)"},
 "drive_folder": dict(json.load(open(HERE / "drive_folder_listing_run3.json")),
     folder={"id": "1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0", "title": "W4", "owner": "garrett.lutz@charmindustrial.com", "parent": "1Hss0-tuVGdGzfCb6bGnn9v3857Of7DGZ", "created": "2026-09-27T15:48:55Z", "metadata_read_utc": "2026-10-07T08:25:17Z"},
     root_items=["Kerry Oil/ (folder, 18gYRjmBMcScctEFU3DkrNNiuk_9v8pR2)", "Testing/ (folder, 1sbuy0NI_yqQmXd4e326PCZ5VmaSUHnsM)", "Scale Tickets/ (folder, 1g6Ii4OOanrIiM36ges-mDnBeNfMau0gA)",
                 "INJ-09-2026-W4 Ops Notes (Google Sheet 1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ, modified 2026-10-07T07:26:58Z)", "RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png (172SPmOAomsORH6vxAStJEVwo8N2K5fIs, created 2026-10-02T00:30:42Z)"],
     completed_qa_checklists_folder="none in W4 (Drive listing of the folder's children shows 5 items)",
     scale_tickets_tree={c: sorted({p["path"].split("/")[2] for p in json.load(open(HERE / "drive_folder_listing_run3.json"))["files"] if p["path"].startswith("Scale Tickets/" + c + "/")}) for c in ("SHPX215053", "SHPX215039", "SHPX215091", "SHPX215079")},
     scale_ticket_files=sum(1 for p in json.load(open(HERE / "drive_folder_listing_run3.json"))["files"] if p["path"].startswith("Scale Tickets/")),
     testing=["SR26-05719 W4 Kerry AECN QOWV COA.pdf (1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ)"],
     kerry_oil=["Sept_W4_Full_Scale_Ticket_Kerry", "Sept_W4_Empty_Scale_Ticket_Kerry (separate Kerry removal, out of scope; replaced in Drive after 01:00Z on 2026-10-07)"],
     bols_location="Not in the W4 folder. The 9 BOLs for SHPX215053, SHPX215039 and SHPX215091 are hyperlinked from Ops Notes 'AECN Rail'!B17:B25 to separate Drive files (local copy: 'AECN BOLs' folder); SHPX215079's BOLs 2453-R/2454-R/2455-R are not listed in W4 Section 2 (W2 holds them) and are uploaded to Certify.",
     _primary_source_opened=[
     {"file": "Drive folder W4 (1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0) and every subfolder", "action": "csv_exported",
      "live_source_url": "https://drive.google.com/drive/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0",
      "artifact_path": "drive_folder_listing_run3.json", "evidence": "local Google Drive copy of the W4 folder (drive_w4/, 01:12:23Z): 33 files with bytes, modified time and sha256 - root, Testing, Kerry Oil, Scale Tickets, 4 railcar and 14 offload folders",
      "items_found": ["INJ-09-2026-W4 Ops Notes", "RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png", "SR26-05719 W4 Kerry AECN QOWV COA.pdf", "28 ticket PDFs"]}]),
 "scale_tickets": {
   "_primary_source_opened": primary_tix,
   "_how_obtained": "Drive copies (drive_w4/, local Google Drive copy 01:12:23Z) read page by page as images with the Read tool 01:12:51Z-01:15:31Z; values recorded in run3_reads/scale_tickets_run3.json; Certify copies downloaded through each source's signed storage link 02:07Z-02:09Z; 28 of 28 byte-identical (sha256, certify_run3/certify_vs_drive_compare_run3.json)",
   "lb_to_kg_used": 0.453592,
   "count_files": 28, "offloads": offloads, "pair_comparison": pairs,
   "pairs_all_match": all(p["tractor_match"] and p["trailer_match"] for p in pairs),
   "date_range": {"earliest": "2026-09-05 09:29 (SHPX215079 offload 3 full)", "latest": "2026-09-24 05:09 (SHPX215053 offload 4 empty)"},
   "certify_vs_drive": {"compared": cmp["compared"], "identical": cmp["identical"], "artifact": "certify_run3/certify_vs_drive_compare_run3.json"},
   "label_notes": ["SHPX215039 offload 2 full (1124426261598) and empty (1312226261663) both carry commodity 'SHPX215039 O1'",
                   "SHPX215053 offload 4 empty (1186426267016) commodity 'SHPX215053' with no offload number",
                   "SHPX215079 offload 3/4 tickets carry no 'DELIVERY SITE' line; all others print LA01/LA02/LA O1/LA O2",
                   "SHPX215053 offload 1 full prints trailer 'KL720', empty 'KL720 RL' (same trailer number)"],
   "zero_steer_tickets": ["SHPX215053 o4 empty 1186426267016 (0/21140/8500 = 29640)", "SHPX215039 o2 full 1124426261598 (0/23800/54820 = 78620)",
                          "SHPX215039 o2 empty 1312226261663 (0/20900/8580 = 29480)", "SHPX215039 o3 full 1124426262601 (0/10040/60580 = 70620)",
                          "SHPX215039 o3 empty 1312226262682 (0/17920/11360 = 29280)", "SHPX215091 o2 full 1124426260591 (0/23780/48420 = 72200)",
                          "SHPX215091 o2 empty 1312226260638 (0/18300/10940 = 29240)", "SHPX215091 o4 full 1124426260594 (0/9940/54620 = 64560)"],
   "zero_steer_rig": "all eight are tractor CH1 / trailer KL720",
   "ch1_kl720_empties_lb": {"with_steer_reading": [29400, 29580], "with_zero_steer": [29640, 29480, 29280, 29240]},
   "reweighs": ["1186426266998 reweigh of 1186426265989", "1312226260636 reweigh of 1312226260630", "1312226261651 reweigh of 1312226260641"]},
 "bols": {"_primary_source_opened": primary_bols,
   "_how_obtained": "12 BOLs copied from the local Google Drive 'AECN BOLs' folder (bols/, 01:17Z; byte-identical to the run-1 copies and, for 2453-R/2454-R/2455-R, to the Certify Sources copies downloaded 02:10Z); every page of each read as an image 01:17Z-01:19Z; values in run3_reads/bol_reads_run3.json",
   "per_bol": per_bol, "per_railcar": per_railcar, "internal_ties": ties,
   "all_ties_hold": all(t["full_minus_tare_eq_delivered"] and t["delivered_div_1000_eq_qty_shipped"] and t["masse_nette_eq_delivered"] and abs(t["litres_x_density_minus_delivered_kg"]) <= t["rounding_allowance_kg"] + 0.6 for t in ties.values()),
   "in_certify_sources": [b for b, d in per_bol.items() if d["in_certify"]],
   "not_in_certify_sources": [b for b, d in per_bol.items() if not d["in_certify"]],
   "po_page": {"po": "Q42025", "line_po": "Q32025", "date": "10/2/2025", "ship_to": "Charm Industrial, 838 SW Purity Springs Road, El Dorado, KS 67042",
               "description": "Renewable Fuel Oil (RFO) Metric Tons 6,000.0 at $290.00, total $1,740,000.00",
               "seller_signature_blank_on": [b for b, d in per_bol.items() if d.get("po_seller_signed") is False],
               "carried_by": "all 12 packages (page 5 of each read 2026-10-07)"},
   "hygiene": {"2466-R": "corrected package: header '***Correction densité et litres finaux / ***Correction of density and final liters'; density and litres hand-corrected; masses unchanged; 5 pages with TSCA (August 7 2026) and PO Q42025 (seller signature blank)",
               "2453-R": "Production period printed '#0X-2026' on page 1 and Run # on Shipping Details",
               "2498-R": "C of A Number on page 1 'RS2-260825-1', Shipping Details '# of the CofA' 'RS2-260828-1'"}},
 "lab_results": {
   "_primary_source_opened": [{"file": "drive_w4/Testing/SR26-05719 W4 Kerry AECN QOWV COA.pdf", "action": "pdf_read", "artifact_path": "drive_w4/Testing/SR26-05719 W4 Kerry AECN QOWV COA.pdf",
        "live_source_url": "https://drive.google.com/file/d/1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ/view", "evidence": "3 pages read 2026-10-07T01:20:22Z; page 2 is SR26-05719.002, client ID 9-2026-W4-AECN"}],
   "drive_file": "Testing/SR26-05719 W4 Kerry AECN QOWV COA.pdf (1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ)",
   "certificate": "SR26-05719.002", "sgs_order": "5506143", "client_id": "9-2026-W4-AECN", "location_on_certificate": "FORT LUPTON, CO",
   "sampled": "2026-09-25 14:00", "received": "2026-09-28 11:00", "analysed": "2026-09-28 14:29-23:23", "report_date": "2026-09-28",
   "carbon_pct": 44.0, "carbon_flag_hash": True, "hydrogen_pct": 6.6, "hydrogen_flag_hash": True, "nitrogen_pct": "<0.75",
   "viscosity_40C_cSt": 13.38, "titration_solvent_mL": 60, "acid_number_mgKOH_g": 156, "acid_number_flag_hash": True, "density_15C_g_cm3": 1.203,
   "hash_footnote": "# - Result is outside of test method limits and/or analytical range used in method precision study",
   "other_pages": "SR26-05719.001 client ID 9-2026-W4-KERRY (C 57.9 %, acid number 154, viscosity 545.2 cSt, density 1.201); SR26-05719.003 client ID 9-2026-W4-QOWV (C 7.9 %) - separate removals",
   "in_certify_sources": False,
   "w3_comparison": "W3 certificate SR26-05599.002: C 39.7 %, H 7.0 %, acid number 47, viscosity 11.73 cSt, density 1.192 (W3 log)",
   "formation_fluid": {"_primary_source_opened": [{"file": "source_exports/Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf (Drive 193vgnGNkDwxYCzYKt8_lM6Y25iKc-kZv)", "action": "pdf_read",
        "artifact_path": "source_exports/Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf", "evidence": "page 5 read: Waypoint Analytical report 24-200-0020, Lab No 98021, Sample ID Formation Fluid, sampled 7/17/2024 8:00, Specific Gravity 1.01 g/mL, ASTM D-1298-85"}],
        "specific_gravity_g_mL": 1.01, "method": "ASTM D-1298-85", "report": "24-200-0020", "lab_no": "98021", "project": "Basco 6 SWD MRV"}},
 "ops_notes": {
   "_primary_source_opened": [{"file": "INJ-09-2026-W4 Ops Notes (Google Sheet 1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ)", "action": "sheet_grid_read",
        "live_source_url": "https://docs.google.com/spreadsheets/d/1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ/edit",
        "artifact_path": "source_exports/INJ-09-2026-W4_Ops_Notes_live_export_run3b_2026-10-07T0825Z.xlsx",
        "evidence": "xlsx export through the Drive connector 2026-10-07T01:20:47Z; all 10 tabs dumped cell by cell with values, formulas and comments (run3_reads/ops_notes_dump_run3_all_tabs.txt, 269 lines) and read 01:21:25Z-01:21:33Z; comments read without data_only (2 comments: AECN Truck H28, Kerry D18); all 4,578 cells identical to the run-2 export. Re-exported 08:25Z after the sheet was edited at 07:26:58Z: 17 cells changed, all on the Kerry tab and the Summary's Kerry rows, none on AECN Rail (run3_reads/ops_notes_change_0726Z_run3.json, read 08:25Z)"}],
   "drive_modified": "2026-10-07T07:26:58Z",
   "change_since_first_read": {"first_export": "2026-10-07T01:20:47Z (sheet modified 2026-10-05T15:09:43Z)", "re_export": "2026-10-07T08:25Z (sheet modified 2026-10-07T07:26:58Z)",
       "cells_changed": 17, "where": "Kerry tab C10/D10 (new gross 76,680 and empty 34,420 lb tickets, re-linked), E10, F10, A18:C18, and the Summary's Kerry rows B11/D11/F11/G11/B19 and totals B13/D13/F13/G13/B21",
       "aecn_cells_changed": 0, "artifact": "run3_reads/ops_notes_change_0726Z_run3.json"},
   "tabs": wf.sheetnames,
   "batch_id_cell": cell("B2"), "week_start": cell("B3"), "week_end": cell("B4"),
   "week_labels": {"A3": ar_v["A3"].value, "A4": ar_v["A4"].value, "B3_weekday": "Friday", "B4_weekday": "Friday"},
   "section1_header_B9": ar_v["B9"].value,
   "constants": constants, "railcars": railcars, "bols_loaded": bols_loaded, "offload_table": offload_table,
   "rollup": rollup, "railyard_split": railyard_split, "summary_aecn": summary_aecn, "aecn_truck_tab": truck_tab,
   "cell_comments": comments,
   "cell_comments_check": {"method": "openpyxl.load_workbook without data_only, every cell on all 10 tabs", "aecn_rail_comments": [c for c in comments if c["tab"] == "AECN Rail"],
                           "all_comments": len(comments)},
   "SHPX215079_note": "Section 2 lists only the 9 BOLs of the three new railcars; SHPX215079's E13 77,870 is typed in (no SUMIF) and its BOLs 2453-R/2454-R/2455-R sit in W2's Section 2"},
 "cobb": {
   "_primary_source_opened": [{"file": "Bio-oil Injection Tracker (Google Sheet 116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q), tabs 'Basco Injection -- COBB' and 'Loads'", "action": "sheet_grid_read",
        "live_source_url": "https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350",
        "artifact_path": "source_exports/COBB_Bio-oil_Injection_Tracker_export_run3_2026-10-07T0122Z.xlsx",
        "evidence": "xlsx export through the Drive connector 2026-10-07T01:21:43Z (tracker modified 2026-10-06T22:40:21Z); header row 2; every row scanned for INJ-09-2026-W4 and the four railcars (run3_reads/cobb_rows_run3.json); 3,805 rows, identical to the run-2 export"}],
   "tab": "Basco Injection -- COBB", "header_row": 2, "A1": "Microsoft SQL Server Import / Last updated 23 hours ago",
   "import_blocks": {str(k): v for k, v in blocks.items()},
   "latest_import": str(latest_import),
   "row_id_at_qa": f"{min(d['row'] for d in latest)}-{max(d['row'] for d in latest)} (latest import {latest_import})",
   "batch_id_col_a": "INJ-09-2026-W4_bio_oil",
   "batch_id_col_a_matches_target": True,
   "rows_latest": latest,
   "injection_completion_date": sorted({d["injection_completion_date"] for d in w4_all}),
   "injection_ph_by_block": {str(k): sorted({str(d.get("injection_ph")) for d in w4_all if d.get("Import Time") == k}) for k in blocks},
   "offloaded_quantity_kg": {d["consumed_lot"]: d["offloaded_quantity_kg"] for d in latest},
   "origin_quantity_kg": {d["consumed_lot"]: d["origin_quantity_kg"] for d in latest},
   "order_line_completed_on": {d["consumed_lot"]: d["order_line_completed_on"] for d in latest},
   "w2_rows_SHPX215079": w2_215079,
   "loads_tab": load_rows,
   "loads_tab_notes": "SHPX215053 rows: 2497-R Actual Loaded 25.73 / COA 'RS2-280828-1' and 2498-R 25.91 / 'RS2-280825-1', against BOL Qty shipped 25.91 (2497-R) and 25.73 (2498-R); railcar total 77.57 MT agrees"},
 "certify": {
   "_primary_source_opened": [
     {"file": "Certify removal rmv_1M3Z5YJN51S0SN1Q - Components, Calculation view, Datapoints, Sources tabs", "action": "modal_opened",
      "live_source_url": "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M3Z5YJN51S0SN1Q/edit",
      "artifact_path": "certify_run3/components_tab.yml", "evidence": "four tabs opened 2026-10-07T01:24:40Z-01:26:16Z and saved: certify_run3/components_tab.yml, calculation_view.yml, datapoints_tab.yml, sources_tab.yml; Components and Datapoints identical to run 2"},
     {"file": "Isometric GraphQL GetGhgEntryQAData (read-only, unrounded)", "action": "csv_exported",
      "artifact_path": "source_exports/certify_graphql_GetGhgEntryQAData_run3_2026-10-07T0123Z.json", "evidence": "pulled 01:22:53Z; full-precision components, inputs, uncertainties and 72 linked sources; read through run3_reads/certify_qa_parsed_run3.txt and certify_fluxes_and_details_run3.txt; data identical to run 2"},
     {"file": "Isometric GraphQL ListProjectGhgEntries", "action": "csv_exported", "artifact_path": "source_exports/certify_graphql_ListProjectGhgEntries_run3_2026-10-07T0123Z.json", "evidence": "pulled 01:22:52Z; 12 newest of 265 entries (run3_reads/certify_project_entries_run3.txt)"},
     {"file": "Isometric GraphQL GetGhgEntryDetails", "action": "csv_exported", "artifact_path": "source_exports/certify_graphql_GetGhgEntryDetails_run3_2026-10-07T0123Z.json", "evidence": "pulled 01:22:53Z; credit allocation 343.966 supplier / 18.104 buffer, risk of reversal 5.0 %"}],
   "removal_period": f"{ge['started']} to {ge['completed']}",
   "net_co2e_removed_t": ge["co2eRemoved"]["magnitude"], "net_displayed_calc_view": "362.068 t",
   "uncertainty_discount_t": ge["uncertaintyDiscount"]["magnitude"],
   "calc_view": "Net CO₂e Removed 362.068 t = Sequestrations 425.691 t + Adjustments 22.439 tCO₂e - Activities 83.620 tCO₂e - Uncertainty Discount 2.443 t",
   "sequestrations_t": seq, "adjustments_t": adj_all, "activities_t": acts_all, "activities_batch_scope_t": acts_aecn,
   "activities_site_t": acts_all - acts_aecn,
   "adjustments_site_t": adj_all - components["BCU - Transport Process"]["value_t"],
   "component_count": len(components), "components": components,
   "datapoints_tab_count": 43, "calculation_view_datapoint_rows": 42, "calculation_view_omits": "E-85 Emissions (196 kgCO2e) is listed on the Datapoints tab but not in the Calculation view grid", "certify_sources_tab_total": 72,
   "certify_sources_enumeration": enum,
   "attachment_map": attachment_map, "attachment_map_site_out_of_scope": site_map,
   "modal_reads": {
     "_primary_source_opened": [{"file": f"component window: {n}", "action": "modal_opened", "artifact_path": a} for n, a in [
        ("Injection sequestration", "certify_run3/modal_injection_sequestration.txt"),
        ("AECN pyrolysis (from rail loads) - process emissions", "certify_run3/modal_pyro_process.txt"),
        ("AECN pyrolysis (from rail loads) - embodied emissions", "certify_run3/modal_pyro_embodied.txt"),
        ("AECN Bio-oil Loss", "certify_run3/modal_bio_oil_loss.txt"),
        ("AECN to SOPOR Tanker Truck Transport Process Emissions", "certify_run3/modal_aecn_sopor_truck_process.txt"),
        ("AECN to SOPOR Tanker Truck Transport Embodied Emissions", "certify_run3/modal_aecn_sopor_truck_embodied.txt"),
        ("SOPOR to Opelousas Rail Transport Process Emissions", "certify_run3/modal_rail_process_opelousas.txt"),
        ("SOPOR to Baton Rouge Rail Process Emissions", "certify_run3/modal_rail_process_baton_rouge.txt"),
        ("SOPOR to Opelousas/Baton Rouge Rail Transport Embodied Emissions", "certify_run3/modal_rail_embodied.txt"),
        ("Opelousas to Basco - Tanker Truck Transport Process Emissions", "certify_run3/modal_opel_basco_truck_process.txt"),
        ("Baton Rouge to Basco Tanker Truck Process Emissions", "certify_run3/modal_baton_rouge_basco_truck_process.txt"),
        ("Opelousas/Baton Rouge to Basco Tanker Truck Transport Embodied Emissions", "certify_run3/modal_opel_br_basco_truck_embodied.txt"),
        ("BCU - Transport Process", "certify_run3/modal_bcu.txt")]],
     "injection_sequestration": "Carbon 44 ±0.176 % (No sources); Mass of Injectant 263,834.2716 ±1,015.98 kg (No sources); output = product_mass * carbon_content * {co2e_of_carbon}",
     "pyrolysis_process": "CI 0.13712 tCO₂e/t (1 source); Bio-Oil Mass - AECN via Rail 267,807.11 ±1,015.98 kg (32 sources)",
     "pyrolysis_embodied": "CI 0.02116 tCO₂e/t (1 source); Bio-Oil Mass - AECN via Rail 267,807.11 ±1,015.98 kg (32 sources)",
     "loss": "AECN Bio-oil Loss - Upstream Emissions 0.145 tCO₂e (2 sources), no ±",
     "aecn_sopor_process": "EF 0.1143 kgCO₂e/(t⋅mi); distance 107.49722 mi (1 source); mass 267,807.11 ±1,015.98 kg (32 sources)",
     "aecn_sopor_embodied": "EF 0.23756 kgCO₂e/mi; Allocated Distance 1,111.70083 mi (8 sources)",
     "rail_process_opelousas": "EF 0.02591 kgCO₂e/(t⋅mi); distance 2,199 mi (1 source); Mass of load 190,578.54 ±725.7 kg (No sources)",
     "rail_process_baton_rouge": "EF 'Rail transport, Northern America, WTW' 0.0161 kgCO₂e/(km⋅t) (1 source); Distance traveled 2,153 km (No sources); Mass of load 77,228.57 kg, no ± (No sources)",
     "rail_embodied": "EF 0.03113 kgCO₂e/mi; Allocated Distance Sopor Quebec to Opelousas (rail) 15,102.69 mi (2 sources)",
     "opel_basco_process": "EF 0.1143 kgCO₂e/(t⋅mi); distance 42.9 mi (1 source); mass Bio-Oil Mass - AECN via Rail 267,807.11 ±1,015.98 kg (32 sources)",
     "br_basco_process": "EF 'Tanker truck, Northern America, WTW' 0.071 kgCO₂e/(km⋅t) (1 source); Distance traveled 136 mi (No sources); Mass of load 77,228.57 ±290.28 kg (No sources)",
     "opel_br_embodied": "EF 0.23756 kgCO₂e/mi; Allocated Distance Opelousas to B6 (truck) 1,946 mi (No sources)",
     "bcu": "Constant CO₂ reduction 19,339 kgCO₂e (No sources)"},
   "sources_downloaded_and_opened": {
     "_primary_source_opened": [
       {"file": "47 Certify source files (tickets, 3 BOLs, 2 Ops Notes copies, maps, EF files, LCA, embodied calc sheet)", "action": "pdf_read",
        "artifact_path": "certify_run3/files/_download_manifest_run3.json", "evidence": "49 files downloaded 2026-10-07T02:08Z-02:11Z through signed storage links read from each /account/certify/source/<id> page (certify_run3/signed/); all 49 byte-identical to run 2; images, PDFs and spreadsheets opened 02:11Z-02:14Z (run3_reads/certify_file_reads_run3.json)"},
       {"file": "_Bio-oil_loss_evidence.png", "action": "image_read", "artifact_path": "certify_run3/files/src_1M3Z64CS81S0R43Q__Bio-oil_loss_evidence.png", "evidence": "Mangrove '3a AECN 3P Bio-oil Loss (v9)': 341.43 kg; transport process 0.0044 x 5.3728 = 0.02365; embodied 0.0044 x 0.14507 = 0.00064; pyrolysis 0.04682 + 0.00722; total 0.07833 tCO₂e"}],
     "loss_example": {"title": "3a AECN 3P Bio-oil Loss (v9)", "mass_kg": 341.43, "label": "AECN 3P Bio-Oil (loss) (Opel to B6)",
                      "upstream_total_t": 0.07833, "transport_process_t": 0.02365, "allocation": 0.0044, "aecn_to_opel_transport_process_t": 5.3728,
                      "transport_embodied_t": 0.00064, "aecn_to_opel_transport_embodied_t": 0.14507, "pyrolysis_process_t": 0.04682, "pyrolysis_embodied_t": 0.00722,
                      "ci_process": 0.13712, "ci_embodied": 0.02116},
     "watco_email": "image (44).png: Gmail screenshot, Matt P. Bergeland (Watco Rail Logistics Specialist) to Antoinette: 'The total milage for this move was 2199.' No railcar, route or date named",
     "aecn_sopor_map": "AECN to SOPOR (Baie Comeau) (2).png: Google Maps 175 Bd du Portage des Mousses, Port-Cartier to Société du port ferroviaire de Baie-Comeau, via QC-138 O, 1 hr 54 min, 173 km (single route)",
     "opel_basco_map": "Opelousas Railyard to Basco.png: Google Maps 4687 LA-115, St Landry LA 71367 to Acadiana Railway, 1224 Cortez St, Opelousas; 42.9 mi (I-49 S), 42.9 mi (I-49 S & US-167 S), 40.9 mi (US-167 S)",
     "mangrove_maps": "Aug-05-, Aug-07-, Aug-12-, Sep-02-2026-distance-route_map.png: Mangrove 'Route Information', origin 'AECN - Produits Forestiers Arbec S.E.N.C.', destination 'Opelousas, LA', 3672.1 km / 2281.7 mi (Aug-05) and 2281.8 mi (others), road routes 2275.0 (not claimed) and 2281.x (claimed); generated 2026-09-16 and 2026-09-29; all four linked to 'Allocated Distance AECN to Sopor Quebec (truck)'",
     "mangrove_maps_identical": "Aug-07 and Sep-02 are both 891,889 bytes",
     "railcar_ee_pdf": "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf: 65.37 MTCO2e / 2,100,000 mi (35 yr x 60,000 mi, Cambridge Systematics) = 0.0000311307 MTCO2e per mile; DOT-111 BOM model, cradle-to-grave 65.37 MT",
     "aecn_ee_calc": "AECN Embodied Emissions Calc Sheet (1).pdf: Total Embodied Emissions (T CO2e)/MT Bio Oil 0.02115941123",
     "glec_pdf": "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf: cover 'V3.1'; page 6 'v3.1 edition, revised and updated (2024)'",
     "glec_library_source": "'GLEC V3.2' library source (src_1KGT9MXXG1S0BWBH) links to https://smart-freight-centre-media.s3.amazonaws.com/documents/GLEC_FRAMEWORK_v3.2_21_10_25_1.pdf; it backs 'Rail transport, Northern America, WTW' 0.0161 kgCO₂e/(km⋅t) and 'Tanker truck, Northern America, WTW' 0.071 kgCO₂e/(km⋅t)",
     "stdef_copies": "Standard Emission Factors + Calculations (8).xlsx uploaded as three source records (src_1KWZ2NN3G1S0QF3R methanol, src_1KWZ2NVQM1S08AWN tanker fuel, src_1KVJRSYT91S09G2E tanker embodied), 336,797 bytes each"},
   "ops_notes_copies": {
     "_primary_source_opened": [{"file": "certify_run3/files/src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx", "action": "sheet_grid_read", "artifact_path": "certify_run3/files/src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx", "evidence": "compared cell by cell with the run-3 live export 2026-10-07T02:11:39Z (certify_run3/certify_vs_drive_compare_run3.json)"},
                                {"file": "certify_run3/files/src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx", "action": "sheet_grid_read", "artifact_path": "certify_run3/files/src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx", "evidence": "compared cell by cell with the run-3 live export 2026-10-07T02:11:39Z (certify_run3/certify_vs_drive_compare_run3.json)"}],
     "copy1_src_1M3VZCDQF1S0FQ0D": dict(_copy_summary(CS / "src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx"), linked_to=["Bio-Oil Mass - AECN via Rail", "Allocated Distance Sopor Quebec to Opelousas (rail)"],
        cells_differing_in_value_from_live=_c3["ops_notes"]["src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx"]["cells_differing_value"]),
     "copy2_src_1M3W1NWED1S0K0MP_2026-10-01": dict(_copy_summary(CS / "src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx"), linked_to=["AECN Bio-oil Loss - Upstream Emissions"],
        cells_differing_in_value_from_live=_c3["ops_notes"]["src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx"]["cells_differing_value"],
        G46_comment=openpyxl.load_workbook(CS / "src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx")["AECN Rail"]["G46"].comment.text),
     "live": {"K10_rail_mi": ar_v["K10"].value, "L10_truck_mi": ar_v["L10"].value, "M28_rail_alloc": ar_v["M28"].value, "M42_rail_alloc_sum": ar_v["M42"].value, "N42_truck_ee_sum": ar_v["N42"].value,
              "C49_raillogix_mass": ar_v["C49"].value, "C50_opelousas_mass": ar_v["C50"].value, "modified": "2026-10-07T07:26:58Z (run3b export; AECN Rail unchanged from the 2026-10-05T15:09:43Z version)"},
     "certify_values_follow": "live sheet (15,102.69 mi, 1,946 mi, 77,228.57 kg, 190,578.54 kg); neither attached copy shows them",
     "compare_method": "every non-empty cell on all 10 tabs, values (data_only); differences include the Whole Oil tab and the AECN Rail rows 48-50 added after the copies were made"}},
 "standard_efs": {
   "_primary_source_opened": [{"file": "Standard Emission Factors + Calculations (Google Sheet 1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4), tab '2026'", "action": "sheet_grid_read",
        "live_source_url": "https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit",
        "artifact_path": "source_exports/Standard_Emission_Factors_export_run3_2026-10-07T0213Z.xlsx", "evidence": "exported through the Drive connector 2026-10-07T02:13:24Z (sheet modified 2026-10-02T15:26:02Z); 2026 tab rows 1-71 dumped (run3_reads/standard_ef_2026_tab_run3.txt) and read 02:13:55Z; identical to the run-2 export"}],
   "row3_aecn_process_H1_2026": efrow(3), "row4_aecn_process_H2_2026": efrow(4), "row5_aecn_embodied": efrow(5),
   "row6_tanker_fuel": efrow(6), "row10_rail_fuel": efrow(10), "row11_tanker_embodied": efrow(11), "row13_railcar_embodied": efrow(13),
   "period_basis": "Removal 2026-09-19 to 2026-09-25 falls in H2 2026, so row 4 (H2 2026) applies",
   "glec_version_cited": "GLEC V3.2 2025",
   "read_utc": "2026-10-07T02:13:55Z"},
 "carbon_range": {
   "_primary_source_opened": [{"file": "MRV_AECN_Analysis.xlsx (Drive 1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi)", "action": "sheet_grid_read",
        "live_source_url": "https://drive.google.com/file/d/1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi/view", "artifact_path": "source_exports/MRV_AECN_Analysis.xlsx_run3.xlsx",
        "evidence": "Summary Statistics tab: 'Filtered to Function = MRV, Offtake = AECN (439 samples)'; Mean, Std Dev, Count rows"}],
   "mean_C_pct": mean_c, "sd_C_pct": sd_c, "n": n_c, "lower_2sd": mean_c - 2 * sd_c, "upper_2sd": mean_c + 2 * sd_c,
   "batch_C_pct": 44.0, "within_2sd": mean_c - 2 * sd_c <= 44.0 <= mean_c + 2 * sd_c,
   "h_mean_pct": stats["Mean"][2], "h_sd_pct": stats["Std Dev"][2], "read_utc": "2026-10-07T02:15:22Z"},
 "lca_files": {
   "_primary_source_opened": [{"file": "FH 2026 LCA w Stack Emissions.xlsx (Certify src_1M1MFJCSF1S0P0KB)", "action": "sheet_grid_read", "artifact_path": "certify_run3/files/src_1M1MFJCSF1S0P0KB_FH_2026_LCA_w_Stack_Emissions.xlsx",
        "evidence": "Sheet1 read: I10 stack 0.004065098048, I11 'Total Other Process Emissions MT COT2e/MT Bio Oil (From Vendor LCA)' 0.133052027800741, I12 total 0.1371171258"},
        {"file": "AECN Embodied Emissions Calc Sheet (1).pdf (Certify src_1KVJRSPDT1S0VY4R)", "action": "pdf_read", "artifact_path": "certify_run3/files/src_1KVJRSPDT1S0VY4R_AECN_Embodied_Emissions_Calc_Sheet__1_.pdf", "evidence": "page 1: Total Embodied Emissions (T CO2e)/MT Bio Oil 0.02115941123"}],
   "fh_2026": {"I10_stack": fh["I10"].value, "I11_vendor": fh["I11"].value, "I12_total": fh["I12"].value, "B6_density": fh["B6"].value, "B4_bio_oil_L": fh["B4"].value},
   "vendor_ci_spreadsheet_in_certify": False, "supporting_ghg_data_in_certify": False,
   "w3_had": "W3 (rmv_1M3MMSA7X1S0R377) Certify Sources carried 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jun2026.xlsx' (Summary!E19 0.13305202780074143) and 'Supporting GHG data 30Jun2026 S.xlsx' linked to the pyrolysis-process CI (W3 log lca_files)",
   "w4_ci_process_sources": components["AECN pyrolysis (from rail loads) - process emissions"]["inputs"]["carbon_intensity"]["sources"],
   "w4_drive_folder": "neither vendor file in the W4 folder (drive_folder_listing.json)"},
 "bcu_sources": {
   "_primary_source_opened": [
     {"file": "Charm-RetirementCertificate-RD-EACs-20251218.pdf (Certify src_1M1MFJPW11S08KY2, attached to W3's BCU, not to W4's)", "action": "pdf_read",
      "live_source_url": "https://registry.isometric.com/account/certify/source/src_1M1MFJPW11S08KY2",
      "artifact_path": "certify_run3/files/src_1M1MFJPW11S08KY2_Charm-RetirementCertificate-RD-EACs-20251218.pdf",
      "evidence": "TERC Certificate of Retirement: Amazon.com Services LLC on behalf of Charm Industrial, Inc; Dec 18, 2025; vintage 2024; Renewable Diesel TERCS; 2,795 TERCs; Turner, Mason & Company; TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000"},
     {"file": "Charm EAC Verification Inventory tracker (Google Sheet 1ZmByYc45FOM2Glk1hF2Wnp-l78v9wAaGmvo42EAbKjw), xlsx export of all 7 tabs", "action": "sheet_grid_read",
      "live_source_url": "https://docs.google.com/spreadsheets/d/1ZmByYc45FOM2Glk1hF2Wnp-l78v9wAaGmvo42EAbKjw/edit",
      "artifact_path": "source_exports/Charm_EAC_Verification_Inventory_tracker_run3.xlsx", "evidence": "exported 2026-10-07T02:14:40Z (identical to run 2); BCU Inventory and GHG Statement BCU Usage tabs dumped (run3_reads/supporting_workbooks_dump_run3.txt) and read 02:15:22Z: row 16 13-47206-50000, row 56 September 2026"},
     {"file": "Transportation Emissions Accounting v1.1 (knowledge-base/isometric-pdfs)", "action": "pdf_read",
      "live_source_url": "https://registry.isometric.com/module/transportation/1.1",
      "artifact_path": "../../../knowledge-base/isometric-pdfs/Transportation Emissions Accounting v1.1 — Isometric.pdf", "evidence": "pages 9-12 read 2026-10-07T02:15:43Z: Section 4.0, 4.1 (EC1-EC5), 4.2, 4.2.1 Equation 5, 4.2.2 Equation 6"}],
   "certificate_terc_count": 2795,
   "certificate_quote": "Each TERC represents one metric ton of carbon dioxide equivalent (“tCO2e”) reduced.",
   "certificate_attached_to_w4_bcu": False,
   "w4_bcu_datapoint_sources": components["BCU - Transport Process"]["inputs"]["constant_reduction"]["sources"],
   "inventory_bcu_row": {"id": "13-47206-50000", "link": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "issued": "12/18/2025", "production": 2024,
                         "ci_gCO2e_MJ": 29.68, "lhv": 44, "total_reduction_mt": 2765.3612, "used": 586.8777, "remaining": 2178.4834},
   "usage_september": {"start": "9/1/2026", "end": "9/30/2026", "co2e_abated_mt": 171.9503, "rd_mass_t": 67.85511902, "cert": "13-47206-50000",
                       "note": "Charm September 2026 RP Oil -- Emissions Reductions from September1-September30_Bio-Oil_GHG_Statement_Results.xlsx as of 2026-10-04 (11 removals, W1-W4); revise if Sept site emissions change."},
   "usage_rows_on_cert_sum": 586.87771,
   "protocol_s4_0": "Under this Module, the use of Book and Claim Units (BCUs) for low-carbon fuels to substitute for some, or all, of project fuel usage is permitted.",
   "protocol_ec1": "BCUs must be purchased and retired by the Project Proponent in a volume equivalent to the volume of fuel substitution claimed.",
   "protocol_ec1_documentation": "Provide proof of BCU purchase and retirement in a volume equivalent to the volume of fuel substitution claimed.",
   "protocol_s4_2_1_eq5": "When applying Equation 4, at maximum, an amount of BCUs may be used for each journey, j, such that: (F_j − F_BCU,j ED_BCU,j/ED_Fuel,Transportation,j) ≥ 0 (Equation 5)",
   "read_utc": "2026-10-07T02:15:43Z"},
 "filtration_constant_source": {
   "_primary_source_opened": [{"file": "AECN COA Solids Content Dataset (May 2025 - May 2026) (Google Sheet 1XhIwfVwGTl2T04CAlA-qee03gfqxNWwBmSCAeiSW548), linked from Ops 'AECN Rail'!O7; xlsx export", "action": "sheet_grid_read",
        "live_source_url": "https://docs.google.com/spreadsheets/d/1XhIwfVwGTl2T04CAlA-qee03gfqxNWwBmSCAeiSW548/edit",
        "artifact_path": "source_exports/AECN_COA_Solids_Content_Dataset_run3.xlsx", "evidence": "exported 2026-10-07T02:14:42Z (identical to run 2); Summary and Materiality tabs read 02:15:22Z"}],
   "window": "2025-05-18 to 2026-05-18", "loads": 136, "unique_coas": 71, "mean_per_unique_coa_pct": 0.195, "mean_per_load_pct": 0.196,
   "summary_A12_B12_C12": ["Recommended value for filtration loss", 0.001959191176, "per-load mean — best represents what is actually delivered"],
   "summary_A7_B7": ["Mean (per load)", 0.001959191176], "summary_A2_B2": ["Window", "2025-05-18 to 2026-05-18"],
   "materiality_C12": "Proposed (fixed 0.196%)",
   "title_source": "Drive download response 2026-10-07T02:14:44Z: title 'AECN COA Solids Content Dataset (May 2025 - May 2026)'",
   "adopted_constant_O7": 0.00196},
 "route_evidence": {
   "_primary_source_opened": [
     {"file": "drive_w4/RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png (Drive 172SPmOAomsORH6vxAStJEVwo8N2K5fIs, W4 root, hyperlinked from Ops L10)", "action": "image_read", "artifact_path": "drive_w4/RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png",
      "evidence": "Google Maps 6045 Point Clair Rd, Carville, LA 70721 to 4675 LA-115, St Landry, LA 71367: via US-190 W 121 miles (2 hr 10 min, fastest), via US-190 W and US-71 N 117 miles, via I-10 W and I-49 N 136 miles (selected)"},
     {"file": "run3_reads/rail_distance_evidence_search_run3.json", "action": "csv_exported", "artifact_path": "run3_reads/rail_distance_evidence_search_run3.json",
      "evidence": "three Drive connector searches 2026-10-07T02:17:50Z-02:17:52Z (titles, full text '2,152' / '2152 mi') and the 72 Certify Sources checked for SOPOR-Baton Rouge rail-distance evidence; none found", "items_found": []}],
   "br_truck_route_mi": [121, 117, 136], "br_truck_selected_mi": 136, "br_truck_origin": "6045 Point Clair Rd, Carville, LA 70721", "br_truck_destination": "4675 LA-115, St Landry, LA 71367",
   "br_truck_map_in_certify": False,
   "br_rail_distance_evidence_found": False,
   "opel_truck_mi": [42.9, 42.9, 40.9], "aecn_sopor_km": 173, "watco_rail_mi": 2199,
   "tickets_route_note": "SHPX215053 full loads were weighed at LOVES, US HWY 190, Port Barre LA (scale 1864) on three of four offloads, i.e. on the US-190 corridor"},
 "rp_status": {
   "_primary_source_opened": [{"file": "Certify project GHG statements list", "action": "sheet_grid_read",
        "live_source_url": "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-statements",
        "artifact_path": "certify_run3/ghg_statements_run3.txt", "evidence": "read 2026-10-07T02:17:01Z: latest row '01 Aug 2026 to 31 Aug 2026 13 GHG entries', Certificates issued, 11 Sep 2026, 1,746.14 tCO₂e; no September 2026 row"}],
   "latest_statement": "01 Aug 2026 to 31 Aug 2026 (Certificates issued, 11 Sep 2026, 1,746.14 tCO₂e)", "september_2026_statement": None, "read_utc": "2026-10-07T02:17:01Z"},
 "prior_weeks": {
   "_primary_source_opened": [{"file": "W1, W2 and W3 AECN source-read logs (outputs/qa/batch-INJ-09-2026-W1/W2/W3-AECN)", "action": "csv_exported",
        "artifact_path": "run3_reads/prior_weeks_run3.json", "evidence": "searched 2026-10-07T02:18:28Z for SHPX215079/215039/215091/215053 (W1 0, W2 49 SHPX215079 hits, W3 0); W2 COBB rows 805-806, 1732-1733, 2660-2661, 3623-3624 re-read in the run-3 COBB export"}],
   "w2_SHPX215079": {"offload_1_net_kg": offloads_w2["W2_SHPX215079_offload_1"]["computed_net_kg"], "offload_2_net_kg": offloads_w2["W2_SHPX215079_offload_2"]["computed_net_kg"],
                     "sum_kg": round(offloads_w2["W2_SHPX215079_offload_1"]["computed_net_kg"] + offloads_w2["W2_SHPX215079_offload_2"]["computed_net_kg"], 6),
                     "w2_completion": json.load(open(HERE / "../batch-INJ-09-2026-W2-AECN/batch_INJ-09-2026-W2-AECN_source_reads.json"))["completion_date"],
                     "w2_rail_alloc_mi": [r["rail_mi_M"] for r in json.load(open(HERE / "../batch-INJ-09-2026-W2-AECN/batch_INJ-09-2026-W2-AECN_source_reads.json"))["ops_notes"]["aecn_rail_tab"]["offload_table"][2:4]],
                     "w2_rail_basis": "one-way 2,199 mi x fraction (W2 log ops_notes.aecn_rail_tab.offload_table[2:4].rail_mi_M)"},
   "w1_hits": 0, "w3_hits": 0},
 "skipped_pending_signin": [],
 "skip_log_note": "No step was skipped in run 3. Every Drive file came through the Drive connector or the local Google Drive copy, and every Certify file through its signed storage link; no sign-in screen was met.",
}
# ---------------------------------------------------------------- artifact paths that must be files
log["certify"]["sources_downloaded_and_opened"]["_primary_source_opened"][0]["artifact_path"] = "certify_run3/files/_download_manifest_run3.json"
log["route_evidence"]["_primary_source_opened"][1]["negative_check_tokens"] = ['"rail_distance_evidence_found": true']

# ---------------------------------------------------------------- presence checks against the 72-record Certify list
ENUM_ART = "certify_run3/certify_sources_enumeration_run3.json"
def presence(label, tokens):
    hits = [t for t in tokens if t in (HERE / ENUM_ART).read_text()]
    return {"_primary_source_opened": [{"file": "Certify Sources tab, all 72 records (certify_run3/certify_sources_enumeration_run3.json, built from certify_run3/sources_tab.yml and GetGhgEntryQAData)",
             "action": "csv_exported", "artifact_path": ENUM_ART, "items_found": hits, "negative_check_tokens": tokens,
             "evidence": f"searched every source filename and display name for {label}"}], "searched_for": tokens, "found": hits}
log["certify"]["presence_checks"] = {
    "w4_new_bols": presence("the nine W4 railcar BOLs", ["2497-R", "2498-R", "2500-R", "2459-R", "2460-R", "2461-R", "2465-R", "2466-R", "2467-R"]),
    "sgs_certificate": presence("the SGS certificate", ["SR26-05719", "COA", "Certificate of Analysis"]),
    "vendor_lca_files": presence("the vendor LCA CI workbook and Supporting GHG data file", ["LCA CI calculation", "Supporting GHG", "Bioenergy AE Cote-Nord"]),
    "bcu_certificate": presence("the BCU retirement certificate", ["RetirementCertificate", "Retirement Certificate", "TERC"]),
    "baton_rouge_route_evidence": presence("the Baton Rouge truck map and any SOPOR-Baton Rouge rail distance record", ["RailLogix", "Carville", "136 mi", "2152", "2,152"]),
}

# ---------------------------------------------------------------- Vaulted / Kansas search across the batch's own records
TERMS = ["Vaulted", "Kansas", "El Dorado", ", KS", "Purity Springs"]
scanned, hits = [], []
for ws in wf:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                scanned.append(f"Ops '{ws.title}'!{c.coordinate}")
                hits += [f"Ops '{ws.title}'!{c.coordinate}: {t}" for t in TERMS if t in c.value]
for n, c in components.items():
    for txt in [n] + [i["datapoint"] for i in c["inputs"].values()] + [f for i in c["inputs"].values() for f in i["sources"]]:
        scanned.append(f"Certify: {txt}")
        hits += [f"Certify '{txt}': {t}" for t in TERMS if t in txt]
for b, d in per_bol.items():
    for fld in ("ship_to", "ship_from", "carrier"):
        scanned.append(f"BOL {b} {fld}")
        hits += [f"BOL {b} {fld}: {t}" for t in TERMS if t in d[fld]]
for d in latest:
    for k, v in d.items():
        if isinstance(v, str):
            scanned.append(f"COBB row {d['row']} {k}")
            hits += [f"COBB row {d['row']} {k}: {t}" for t in TERMS if t in v]
vs = {"terms": TERMS, "fields_scanned": len(scanned), "hits": hits,
      "po_page_note": "BOL page 5 (Charm PO Q42025) Ship To 'Charm Industrial, 838 SW Purity Springs Road, El Dorado, KS 67042' on every five-page package (read from the page images; not a structured field above)"}
(HERE / "vaulted_search.json").write_text(json.dumps(vs, indent=1))
log["vaulted_search"] = dict(vs, _primary_source_opened=[{"file": "Ops Notes all 10 tabs (every text cell), 26 Certify component/datapoint/source names, 12 BOL ship-to/ship-from/carrier fields, 14 COBB rows",
    "action": "csv_exported", "artifact_path": "vaulted_search.json", "negative_check_tokens": ["Vaulted"], "evidence": f"{len(scanned)} text fields scanned for {TERMS}"}])

# ---------------------------------------------------------------- policy (Max's stated rules, recorded in memory)
MEM = Path.home() / ".claude/projects/-Users-maxlavine-Desktop-Claude-Skills-MRV-Expert/memory"
log["policy"] = {
  "_primary_source_opened": [{"file": str(MEM / f), "action": "pdf_read", "artifact_path": str(MEM / f), "evidence": "read 2026-10-07T02:17:41Z"}
                             for f in ("project_custody_upstream_emissions.md", "project_railcar_mass_policy.md", "project_bcu_reduction_cap_policy.md")],
  "custody_rule": "Max, 2026-09-29 (W3 AECN QA): \"THE UPSTREAM EMISSIONS OF ALL OIL IN CHARM CUSTODY MUST BE NETTED AGAINST REMOVALS. THIS IS NOT NEW FUCKING INFORMATION.\"",
  "last_load_rule": "On the last offload of a railcar, MRV applies a conservatism rule: if sum(all offloads at scale-ticket values) exceeds BOL inbound aggregate (= sum of inbound BOLs into the railcar), the last offload's Cargo (kg) is set to BOL_total − sum(prior offloads' raw scale-ticket masses).",
  "bcu_cap_rule": "BCU quantity (tCO2e) applied in Reductions against a specific process/activity emission must be ≤ that emission — full coverage (BCU = emission) is the target, never more.",
  "bcu_fix_rule": "Over-coverage of any size is a FAIL (INJ-09-2026-W3-QOWV: BCU 6,264 kg vs process 6,263.604 kg, 0.396 kg over, Fail; fix = enter the exact process figure, never round down either)."}

# ---------------------------------------------------------------- deterministic outputs (mass chain, recompute)
mc = HERE / "mass_chain" / "summary.json"
if mc.exists():
    s = json.load(open(mc))
    from collections import Counter
    log["mass_chain"] = {
        "_artifact": "mass_chain/summary.json", "script": "skills/qa/_lab/batch-qa-aecn-deterministic/scripts/compute_mass_chain.py",
        "inputs_built_by": "build_mass_chain_inputs.py (one input per offload under mass_chain/<offload>/)",
        "counts": dict(Counter(x["status"] for x in s)),
        "non_pass": [x for x in s if x["status"] not in ("PASS", "SKIP")],
        "last_offload": {x["offload"]: x["note"] for x in s if x["check_id"] == "last_offload_derivation" and x["status"] != "SKIP"},
        "railcar_balance": {x["offload"]: x["note"] for x in s if x["check_id"] == "railcar_inbound_outbound_balance" and x["offload"].endswith("_4")},
        "rail_uncertainty_precondition": {"SHPX215053": "4 offloads vs 3 BOLs", "SHPX215039": "4 offloads vs 3 BOLs", "SHPX215091": "4 offloads vs 3 BOLs", "SHPX215079": "4 offloads (2 in W2, 2 here) vs 3 BOLs"},
        "fc11_flag_explained": "SHPX215079 offload 4: scale ticket 14,714.52448 kg vs Ops cargo 14,321.7608 kg; the 392.76368 kg difference is the last-offload cut (W2 42,410.852 + W4 35,851.91168 = 78,262.76368 kg against 77,870 kg loaded), booked in Ops J41 and COBB (14,321.76)",
    }
ro = HERE / "recompute_output.txt"
if ro.exists():
    lines = ro.read_text().splitlines()
    log["recompute"] = {"script": "recompute_INJ-09-2026-W4-AECN.py", "output": "recompute_output.txt",
                        "mismatch_line": [l for l in lines if "arithmetic mismatch" in l],
                        "lines": [l for l in lines if l.startswith(("OK ", "MISMATCH", "INFO", "   term"))],
                        "findings": [l for l in lines if l.startswith("FINDING")]}

# ---------------------------------------------------------------- run-3 reads of the guidance history, Ops copies, prior weeks, policy and period documents
W3G = "../batch-INJ-09-2026-W3-AECN/source_exports/VVB_Guidance_September_1-30_fetched_2026-09-29.txt"
gt = (HERE / W3G).read_text()
log["vvb_guidance"]["read_order"] = {"guidance_read_utc": "2026-10-07T01:12:12Z",
    "before_it": ["pre-flight reads 01:10:32Z-01:10:38Z (knowledge base, lessons learned, checklist structure)", "registry 01:10:43Z-01:10:50Z",
                  "Failure Categories printed 01:11:11Z / 01:11:27Z", "two memory notes on Gate 1 order and source access 01:11:48Z",
                  "Drive search title contains 'VVB Guidance' 01:11:53Z and the guidance export 01:11:58Z"],
    "first_batch_source_after_it": "W4 Drive folder copy 01:12:23Z",
    "result": "Gate 1 step 0 order met in run 3: the guidance was read in full before any batch source (Drive folder, Ops Notes, COBB, Certify) was opened"}
log["vvb_guidance"]["removed_since_2026_09_29"] = {
    "_primary_source_opened": [{"file": "VVB Guidance September 1 - September 30, fetch of 2026-09-29 (W3 QA)", "action": "csv_exported", "artifact_path": "run3_reads/vvb_guidance_w3_fetch_comparison_run3.json",
                                "evidence": "W3-era fetch searched 2026-10-07T02:18Z for the multi-week clause and the 'Basis for Loaded Mass' section; both present"},
                               {"file": "VVB Guidance September 1 - September 30, run-3 fetch (2026-10-07T01:11:58Z)", "action": "csv_exported", "artifact_path": "source_exports/VVB_Guidance_September_1-30_run3.txt",
                                "evidence": "same search; neither present", "negative_check_tokens": ["more than one reporting week", "Basis for Loaded Mass"], "items_found": []}],
    "quote_multi_week_2026_09_29": [l for l in gt.splitlines() if "more than one reporting week" in l][0],
    "basis_for_loaded_mass_section_2026_09_29": "Basis for Loaded Mass" in gt,
    "in_run3_fetch": "Basis for Loaded Mass" in (HERE / "source_exports/VVB_Guidance_September_1-30_run3.txt").read_text()}
cp1 = openpyxl.load_workbook(CS / "src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx", data_only=True)["AECN Rail"]
cp2 = openpyxl.load_workbook(CS / "src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx", data_only=True)["AECN Rail"]
oc = log["certify"]["ops_notes_copies"]
oc["copy1_src_1M3VZCDQF1S0FQ0D"].update(G13_loss=cp1["G13"].value, M10_note=cp1["M10"].value, M13_note=cp1["M13"].value)
oc["copy2_src_1M3W1NWED1S0K0MP_2026-10-01"].update(G13_loss=cp2["G13"].value)
oc["live"]["G13_loss"] = ar_v["G13"].value
oc["live"]["G13_formula"] = ar_f["G13"].value
oc["live"]["M13_note"] = ar_v["M13"].value
W2L = json.load(open(HERE / "../batch-INJ-09-2026-W2-AECN/batch_INJ-09-2026-W2-AECN_source_reads.json"))
PW3 = json.load(open(HERE / "run3_reads/prior_weeks_run3.json"))
log["prior_weeks"]["w2_SHPX215079"]["tickets"] = PW3["w2_SHPX215079_tickets"]
log["prior_weeks"]["w2_SHPX215079"]["tickets_read_run3"] = {k: offloads_w2[k] for k in offloads_w2}
log["prior_weeks"]["w2_SHPX215079"]["w2_log_matches_run3_ticket_reads"] = PW3["w2_tickets_match_run3_reads"]
log["prior_weeks"]["w2_acid_number_mgKOHg"] = W2L["lab_results"]["acid_number_mgKOHg"]
log["prior_weeks"]["_primary_source_opened"].append({"file": "W2 SHPX215079 offload 1-2 ticket PDFs (local Google Drive W2/Scale Tickets/SHPX215079, copied 01:15:43Z to drive_w2_215079/)", "action": "image_read",
    "artifact_path": "run3_reads/scale_tickets_run3.json", "evidence": "4 tickets read as images 01:16:12Z-01:16:14Z: offload 1 76,720 - 28,660 = 48,060 lb (21,799.63152 kg); offload 2 73,860 - 28,420 = 45,440 lb (20,611.22048 kg); match the W2 log"})
log["lab_results"]["acid_number_by_week"] = {"W1": PW3["logs"]["W1"]["acid_number"], "W2": W2L["lab_results"]["acid_number_mgKOHg"], "W3": 47, "W4": 156}
log["ops_notes"]["railcar_headers_row9"] = {col: ar_v[f"{col}9"].value for col in "ABCDEFGHIJKLMNOPQ"}
KBP = HERE.parents[2] / "knowledge-base/Charm_Isometric_Knowledge_Base.md"
log["policy"]["kb_document_location_rule"] = [l for l in KBP.read_text().splitlines() if "Document Location Rule" in l][0]
log["policy"]["kb_document_location_rule_text"] = [l for l in KBP.read_text().splitlines() if "only FLAG/FAIL if the document is absent from BOTH" in l][0]
log["policy"]["_primary_source_opened"].append({"file": "knowledge-base/Charm_Isometric_Knowledge_Base.md, Document Location Rule (lines 644-645)", "action": "pdf_read", "artifact_path": str(KBP), "evidence": "rule text read 2026-10-07T02:17:43Z"})
_w2txt = json.dumps(W2L)
log["prior_weeks"]["w2_bol_2499T_present"] = "2499-T" in _w2txt
log["certify"]["mangrove_map_hashes"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:12] for p in sorted(CS.glob("*route_map*"))}
SR = "source_exports/September1-September30_Bio-Oil_GHG_Statement_Results_run3b_2026-10-07T0826Z.xlsx"
SRD = "run3_reads/september_results_and_report_run3_dump.txt"
GR = "source_exports/September1-September30_Removals_Isometric_GHG_Statement_Report_v1.7_run3.docx"
_rw = openpyxl.load_workbook(HERE / SR, data_only=True)["Sheet1"]
_rwf = openpyxl.load_workbook(HERE / SR)["Sheet1"]
_rows = [r for r in range(2, 13) if _rw[f"F{r}"].value]
_tot = {k: round(sum(_rw[f"{c}{r}"].value or 0 for r in _rows), 4) for k, c in (("process_t", "J"), ("site_t", "K"), ("reductions_t", "L"), ("discount_t", "M"))}
_gross = round(sum(_rw[f"H{r}"].value * _rw[f"R{r}"].value * 3.667 / 1000 for r in _rows), 4)
log["rp_status"]["results_workbook"] = {
    "_primary_source_opened": [{"file": "September1-September30_Bio-Oil_GHG_Statement_Results.xlsx, local Google Drive copy (My Drive/MRV/Removals Reporting/2026/CURRRENT PERIOD/September 1 - September 30 RP/Additional Documentation)", "action": "sheet_grid_read",
        "live_source_url": "https://drive.google.com/file/d/18JugtY8A2sMk0-jxvkrGwe8f6FMwnM4r/view", "artifact_path": SR,
        "evidence": "first copied 2026-10-07T02:16:20Z (8,985 bytes, identical to run 2) and read 02:16:34Z (" + SRD + "); the workbook was edited 2026-10-07T07:43:32Z and re-copied 08:26Z (8,986 bytes): rows 9 and 12 (W3 and W4 Kerry) swapped their H, J, L and M values; row 10 W4 AECN unchanged: H10 263834.2716, J10 63.069, K10 20.55, L10 22.439, M10 2.4429, R10 0.44; column totals unchanged"}],
    "w4_aecn_row": {"removal": _rw["F10"].value, "date": _rw["G10"].value, "bio_oil_injected_kg": _rw["H10"].value, "process_t": _rw["J10"].value, "site_t": _rw["K10"].value,
                    "reductions_t": _rw["L10"].value, "discount_t": _rw["M10"].value, "carbon_pct": round(_rw["R10"].value * 100, 2),
                    "gross_t": round(_rw["H10"].value * _rw["R10"].value * 3.667 / 1000, 3),
                    "net_t": round(_rw["H10"].value * _rw["R10"].value * 3.667 / 1000 - _rw["J10"].value - _rw["K10"].value + _rw["L10"].value - _rw["M10"].value, 2)},
    "rp_totals_from_rows_2_12": dict(_tot, gross_t=_gross, net_t=round(_gross - _tot["process_t"] - _tot["site_t"] + _tot["reductions_t"] - _tot["discount_t"], 2), rows=len(_rows)),
    "rp_totals": {"process_t": round(_tot["process_t"], 2), "site_t": round(_tot["site_t"], 2), "discount_t": round(_tot["discount_t"], 2), "reductions_t": round(_tot["reductions_t"], 2),
                  "reductions_kg": round(_tot["reductions_t"] * 1000, 2), "net_t": round(_gross - _tot["process_t"] - _tot["site_t"] + _tot["reductions_t"] - _tot["discount_t"], 2)},
    "w4_row10_formulas": {"I10_gross": _rwf["I10"].value, "N10_net": _rwf["N10"].value},
    "reductions_by_removal_t": [_rw[f"L{r}"].value for r in _rows]}
log["rp_status"]["statement_report_v1_7"] = {
    "_primary_source_opened": [{"file": "September1-September30_Removals_Isometric_GHG_Statement_Report_v1.7.docx, local Google Drive copy", "action": "pdf_read",
        "live_source_url": "https://drive.google.com/file/d/1smX6HME33-dGfTFApXNRRCPVvncmFxeB/view", "artifact_path": GR,
        "evidence": "copied 2026-10-07T02:16:20Z (21,245 bytes, byte-identical to the run-2 copy); all 165 paragraphs dumped to " + SRD + " and read 02:16:34Z"}],
    "drive_metadata": {"read_utc": "2026-10-07T08:38Z", "created": "2026-10-03T16:52:22Z", "modified": "2026-10-05T16:07:59Z", "size_bytes": 21245,
                       "owner": "garrett.lutz@charmindustrial.com", "note": "size equals the 02:16:20Z copy, so the copy read is the current file"},
    "date_of_report": "10/3/26", "section_e": {"process_t": 384.65, "site_t": 20.48, "discount_t": 11.00, "reductions_t": 171.95, "net_t": 1744.01},
    "w4_site_t": 20.482, "w4_additional_transport_t": 1.084,
    "quote_br": "Its rail leg (2,152 mi) and tanker leg (136 mi one way, counted as a round trip) are calculated and reported separately from the Opelousas railcars, each on that railcar's own mass and route distance.",
    "quote_no_negative_loss": "Where scale tickets exceed Bills of Lading, the excess is removed through the Uncertainty Adjustment and no negative loss is applied.",
    "quote_loss_total": "In this period 1,373.38 kg was lost across ten railcars, carrying 0.315 t CO2e.",
    "quote_longest_route": "Regardless of the software used, where multiple routing options are given, the longest will be used."}
log["rp_status"]["certify_w4_adjustments_t"] = log["certify"]["adjustments_t"]
log["route_evidence"]["rail_logix_lessons_learned"] = {
    "_primary_source_opened": [{"file": "Rail Logix Lessons Learned (Google Doc 167_fXe69toEPdRvipinM1MYhPSHuf7-0v62dpXVn7u0)", "action": "pdf_read",
        "live_source_url": "https://docs.google.com/document/d/167_fXe69toEPdRvipinM1MYhPSHuf7-0v62dpXVn7u0/edit", "artifact_path": "source_exports/Rail_Logix_Lessons_Learned_run3.txt",
        "evidence": "text export 02:14:44Z (4,721 bytes, identical to run 2), 102 lines read 02:15:23Z; road routes and timings, no rail distance"}],
    "quote_route": "From Basco site take I-49 to 190.Stay on 190 until hit I-10 hang a left on to I-10.",
    "quote_scale": "We stopped at Loves Truck stop in Port Barre topped off trucks and weight ticket."}

# ---------------------------------------------------------------- run-3 Gate 3 follow-up reads (2026-10-07T09:13Z-09:24Z)
G3F = {"reviewer_file": "adversarial_review.md", "reads_utc": "2026-10-07T09:13:13Z-09:24:49Z (first re-read 09:13:13Z, after the review arrived at 09:13:04Z)"}
# loss column of both Certify Ops copies (files opened 09:13Z-09:24Z)
for _k, _f in (("copy1_src_1M3VZCDQF1S0FQ0D", "src_1M3VZCDQF1S0FQ0D_INJ-09-2026-W4_Ops_Notes.xlsx"), ("copy2_src_1M3W1NWED1S0K0MP_2026-10-01", "src_1M3W1NWED1S0K0MP_INJ-09-2026-W4_Ops_Notes.xlsx")):
    _w = openpyxl.load_workbook(CS / _f, data_only=True)["AECN Rail"]
    _wf = openpyxl.load_workbook(CS / _f)["AECN Rail"]
    _g = [_w[f"G{r}"].value for r in range(10, 14)]
    log["certify"]["ops_notes_copies"][_k].update(G10_G13_loss_kg=_g, G_loss_sum_kg=round(sum(_g), 5), G13_formula=_wf["G13"].value)
_g3 = log["certify"]["ops_notes_copies"]["copy2_src_1M3W1NWED1S0K0MP_2026-10-01"]["G10_G13_loss_kg"][:3]
log["certify"]["ops_notes_copies"]["loss_positive_sum_kg"] = round(sum(_g3), 5)
# standard EF sheet: how the tanker and railcar embodied factors are built (read 09:13Z-09:24Z)
_SEF = HERE / "source_exports/Standard_Emission_Factors_export_run3_2026-10-07T0213Z.xlsx"
_sefv = openpyxl.load_workbook(_SEF, data_only=True)
_seff = openpyxl.load_workbook(_SEF)
_tt, _rc = _sefv["Truck and Trailer EE 2026"], _sefv["2026 Railcar Embodied Emissions"]
log["standard_efs"]["tanker_embodied_build"] = {
    "tab": "Truck and Trailer EE 2026", "A12_B12": [_tt["A12"].value, _tt["B12"].value], "A14_B14": [_tt["A14"].value, _tt["B14"].value],
    "A15_B15": [_tt["A15"].value, _tt["B15"].value], "B15_formula": _seff["Truck and Trailer EE 2026"]["B15"].value}
log["standard_efs"]["railcar_embodied_build"] = {"tab": "2026 Railcar Embodied Emissions", "A4_B4": [_rc["A4"].value, _rc["B4"].value], "A5_B5": [_rc["A5"].value, _rc["B5"].value]}
# lab: other oils in the same SGS order (certificate pages 1 and 3 re-read 09:13Z-09:24Z)
log["lab_results"]["same_order_acid_numbers"] = {"sgs_order": "5506143", "SR26-05719.001 9-2026-W4-KERRY": "154 mg KOH/g, marked '#'",
    "SR26-05719.002 9-2026-W4-AECN": "156 mg KOH/g, marked '#'", "SR26-05719.003 9-2026-W4-QOWV": "36 mg KOH/g, no mark",
    "analysed": "28-Sep-2026 14:29 - 28-Sep-2026 23:23 (all three)"}
# COBB: injection-week booking of September offloads (export of 01:22Z, read 09:13Z-09:24Z)
_CBF = HERE / "source_exports/COBB_Bio-oil_Injection_Tracker_export_run3_2026-10-07T0122Z.xlsx"
_cb = list(openpyxl.load_workbook(_CBF, read_only=True, data_only=True)["Basco Injection -- COBB"].iter_rows(values_only=True))
def _cbrow(i):
    r = _cb[i - 1]
    return {"row": i, "injection_batch": r[0], "consumed_lot": r[2], "order_line_completed_on": str(r[8]), "injection_completion_date": str(r[11])}
log["cobb"]["w4_order_line_completed_on"] = {_cbrow(i)["consumed_lot"]: _cbrow(i)["order_line_completed_on"] for i in range(3724, 3738)}
log["cobb"]["late_september_railcars"] = {"rows": "3781-3792", "railcars": ["SHPX215061", "SHPX215067", "SHPX215073"],
    "examples": [_cbrow(3781), _cbrow(3786), _cbrow(3792)],
    "all_rows_batch": sorted({_cb[i - 1][0] for i in range(3781, 3793)}),
    "all_rows_completion": sorted({str(_cb[i - 1][11]) for i in range(3781, 3793)}),
    "order_lines_completed": sorted({str(_cb[i - 1][8]) for i in range(3781, 3793)})}
# W3 Ops week (W3 batch folder export of 2026-09-29, read 09:13Z-09:24Z)
_w3 = openpyxl.load_workbook(HERE.parent / "batch-INJ-09-2026-W3-AECN/source_exports/INJ-09-2026-W3_Ops_Notes.xlsx", data_only=True)["AECN Rail"]
log["prior_weeks"]["w3_ops_week"] = {"file": "../batch-INJ-09-2026-W3-AECN/source_exports/INJ-09-2026-W3_Ops_Notes.xlsx",
    "A3_B3": [_w3["A3"].value, str(_w3["B3"].value)], "A4_B4": [_w3["A4"].value, str(_w3["B4"].value)]}
# Rail Logix notes: loads after SHPX215053 (re-read 09:13Z-09:24Z)
log["route_evidence"]["rail_logix_lessons_learned"].update(
    quote_0923_swap="Rigged down and swapped rail cars", quote_0924="Left yard at 0415 arrived at raillogix at 0645",
    quote_0925="Starting on the 2nd load at 0915", quote_0925_end="Finished loading at 0934. Last load is always light")
# Drive search for Certify's own figure, 2,153 (09:13Z-09:24Z)
_s2153 = json.loads((HERE / "run3_reads/rail_distance_2153_search_run3.json").read_text())
log["route_evidence"]["search_2153"] = {"_primary_source_opened": [{"file": "run3_reads/rail_distance_2153_search_run3.json", "action": "csv_exported",
        "artifact_path": "run3_reads/rail_distance_2153_search_run3.json",
        "evidence": "Drive connector search 2026-10-07 (between 09:13Z and 09:24Z), all 50 results listed; the two spreadsheets among them opened: Bio-oil Injection Tracker (2153 only as BOL '2153-T') and 2026 Basco Planning (run3_reads/2026_Basco_Planning_export_run3.xlsx, 44,429 cells: nearest value 2152.647981, a running tCDR total)",
        "items_found": [], "negative_check_tokens": ["SOPOR to Baton Rouge rail distance 2,153"]}],
    "query": _s2153["query"], "results": _s2153["n"], "rail_distance_record_found": False,
    "tracker_hits": "Loads C154, Temp Reading B22, PCBs B24/B26: '2153-T'; RP Summary AprilMay A68 '2153T'",
    "planning_hit": "'Original Schedule (Apr-Dec)'!P99 2152.647981 under 'Total tCDR Running Total' (2026-04-08)"}
# Ops Notes AECN Truck header (run3b export, read 09:13Z-09:24Z)
_atv = openpyxl.load_workbook(OPS, data_only=True)["AECN Truck"]
log["ops_notes"]["aecn_truck_tab"]["A1_header"] = _atv["A1"].value
log["ops_notes"]["aecn_truck_tab"]["N10_N12_N25"] = [_atv["N10"].value, _atv["N11"].value, _atv["N12"].value, _atv["N25"].value]
# discount column and report figure (results workbook run3b, report v1.7; read 09:13Z-09:24Z)
_RWF = HERE / "source_exports/September1-September30_Bio-Oil_GHG_Statement_Results_run3b_2026-10-07T0826Z.xlsx"
_rwv = openpyxl.load_workbook(_RWF, data_only=True).active
log["rp_status"]["results_workbook"]["discount_column_M2_M12"] = [_rwv[f"M{r}"].value for r in range(2, 13)]
log["rp_status"]["results_workbook"]["discount_column_sum_t"] = round(sum(_rwv[f"M{r}"].value for r in range(2, 13)), 4)
log["rp_status"]["statement_report_v1_7"]["section_e_discount_lines"] = ["Uncertainty Discounts", "10998.10", "11.00"]
# knowledge-base uncertainty rule for electricity (lines 620-621, read 09:13Z-09:24Z)
_KBT = (HERE.parents[2] / "knowledge-base/Charm_Isometric_Knowledge_Base.md").read_text().splitlines()
log["policy"]["kb_electricity_uncertainty"] = [l.strip() for l in _KBT if "Electricity Usage: 0.02" in l]
_SKT = (HERE.parents[2] / "skills/qa/batch-qa-aecn/SKILL.md").read_text().splitlines()
log["policy"]["status_rules"] = {"skill_fail_definition": [l.strip() for l in _SKT if l.startswith("- **Fail** —")][0],
    "skill_tolerance_line": [l.strip() for l in _SKT if "no rounding tolerance beyond" in l][0],
    "lessons_learned_principle_7": "7. **Missing evidence = FAIL.** No exceptions."}
log["gate3_followup"] = G3F

# ---------------------------------------------------------------- per-batch required-evidence matrix + attachment gate
log["certify"]["required_evidence"] = {
    "Mass of Injectant": ["scale_ticket", "ops_notes"],
    "Bio-Oil Mass - AECN via Rail": ["scale_ticket", "bol", "ops_notes"],
    "Mass of load": ["scale_ticket", "bol", "ops_notes"],
    "Carbon Content": ["lab"],
    "Carbon Intensity - AECN Pyrolysis": ["lca"],
    "Allocated Distance": ["ops_notes", "map_or_watco"],
    "Distance from": ["map_or_watco"],
    "Distance traveled": ["map_or_watco"],
    "Emissions Factor": ["ef_sheet"],
    "Emission Factors": ["ef_sheet"],
    "Northern America, WTW": ["ef_sheet"],
    "Constant CO": ["eac_cert"],
    "AECN Bio-oil Loss": ["ops_notes", "bol"],
}
log["certify"]["required_evidence_basis"] = ("Built from this removal's 13 AECN components because the registered AECN matrix keys "
    "('Allocated Bio-Oil Mass') do not match W4's datapoint names ('Bio-Oil Mass - AECN via Rail', 'Mass of load', 'Distance traveled', "
    "GLEC library factors, BCU constant, AECN Bio-oil Loss). Same categories as the registered AECN matrix for the matching roles; "
    "'Mass of load' takes the Bio-Oil Mass rule (tickets + BOLs + Ops Notes); the loss takes Ops Notes (loss per railcar) + BOLs (loaded mass).")
import sys as _s
_s.path.insert(0, str(HERE.parents[2] / "skills/qa/batch-qa-aecn/scripts"))
from audit_attachments import audit_attachments
ok, gaps = audit_attachments(log)
log["certify"]["attachment_gate"] = {"ok": ok, "gaps": gaps, "open_datapoints": [g.split(": required")[0] for g in gaps], "run_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")}

# keep the derived values the checklist build merged in (build_with_validation writes them here)
if OUT.exists():
    _prev = json.loads(OUT.read_text()).get("_derived_values")
    if _prev:
        log["_derived_values"] = _prev
OUT.write_text(json.dumps(log, indent=1, ensure_ascii=False, default=str))
print("wrote", OUT, len(OUT.read_text()), "bytes;", len(components), "components;", len(attachment_map), "batch-scope datapoints mapped")
