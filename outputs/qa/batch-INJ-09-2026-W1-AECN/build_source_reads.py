#!/usr/bin/env python3
"""Builds batch_INJ-09-2026-W1-AECN_source_reads.json from values read this session (2026-09-17).
Every number here was read from a primary source opened in-session; see _primary_source_opened blocks."""
import json
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "batch_INJ-09-2026-W1-AECN_source_reads.json"
KG_PER_LB = 0.453592

OPS_URL = "https://docs.google.com/spreadsheets/d/1_nXYsz50d2ZLQSE2Zkj_CTN2WzZciFc0XnNUEPJxIjo/edit"
VVB_URL = "https://docs.google.com/document/d/1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y/edit"
EF_URL = "https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705"
COBB_URL = "https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350"
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M2GBNMY91S0H2MB/edit"

# ---------------- scale tickets (16 CAT Scale PDFs, each read as an image with the Read tool) ----------------
# (railcar_ops_label, offload, kind, ticket#, gross_lb, date, time, scale#, location, tractor, trailer, commodity label, file)
TICKETS = [
    ("GRPX5254", 1, "FULL",  "1124426245496", 71660, "2026-09-02", "11:27", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "GPRX5254 O1",  "GRPX5254_LD1_FULL_1124426245496.pdf"),
    ("GRPX5254", 1, "EMPTY", "1124426245501", 28800, "2026-09-02", "14:14", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "GPRX5254 O1",  "GRPX5254_LD1_EMPTY_1124426245501.pdf"),
    ("GRPX5254", 2, "FULL",  "1124426245497", 73380, "2026-09-02", "12:33", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "GPRX5254 LD2", "GRPX5254_LD2_FULL_1124426245497.pdf"),
    ("GRPX5254", 2, "EMPTY", "1312226245354", 29620, "2026-09-02", "14:40", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL720", "GPRX5254 LD2", "GRPX5254_LD2_EMPTY_1312226245354.pdf"),
    ("GRPX5254", 3, "FULL",  "1312226245358", 74260, "2026-09-02", "16:30", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "GPRX5254 O3",  "GRPX5254_LD3_FULL_1312226245358.pdf"),
    ("GRPX5254", 3, "EMPTY", "1124426246510", 28400, "2026-09-03", "07:17", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "GPRX5254 O3",  "GRPX5254_LD3_EMPTY_1124426246510.pdf"),
    ("GRPX5254", 4, "FULL",  "1124426245504", 68140, "2026-09-02", "17:25", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "GPRX5254 LD4", "GRPX5254_LD4_FULL_1124426245504.pdf"),
    ("GRPX5254", 4, "EMPTY", "1312226246364", 29420, "2026-09-03", "07:03", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL720", "GPRX5254 O4",  "GRPX5254_LD4_EMPTY_1312226246364.pdf"),
    ("GPRX5107", 1, "FULL",  "1124426243469", 78360, "2026-08-31", "11:20", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "GPRX5107 LD1", "GPRX5107_LD1_FULL_1124426243469.pdf"),
    ("GPRX5107", 1, "EMPTY", "1124426244483", 29440, "2026-09-01", "10:27", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "GPRX5107 LD1", "GPRX5107_LD1_EMPTY_1124426244483.pdf"),
    ("GPRX5107", 2, "FULL",  "1124426243470", 74140, "2026-08-31", "11:22", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "GPRX5107 O2",  "GPRX5107_LD2_FULL_1124426243470.pdf"),
    ("GPRX5107", 2, "EMPTY", "1312226244331", 28640, "2026-09-01", "08:46", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "GPRX5107 O2",  "GPRX5107_LD2_EMPTY_1312226244331.pdf"),
    ("GPRX5107", 3, "FULL",  "1124426244484", 72600, "2026-09-01", "10:51", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "GPRX5107 O3",  "GPRX5107_LD3_FULL_1124426244484.pdf"),
    ("GPRX5107", 3, "EMPTY", "1312226244341", 28480, "2026-09-01", "15:35", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "GPRX5107 O3",  "GPRX5107_LD3_EMPTY_1312226244341.pdf"),
    ("GPRX5107", 4, "FULL",  "1124426244487", 62780, "2026-09-01", "13:02", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "GPRX5107 LD4", "GPRX5107_LD4_FULL_1124426244487.pdf"),
    ("GPRX5107", 4, "EMPTY", "1312226244340", 29300, "2026-09-01", "15:33", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL720", "GPRX5107 LD4", "GPRX5107_LD4_EMPTY_1312226244340.pdf"),
]

# Ops Notes 'AECN Rail' Section 3 rows 28-35 (values read from the downloaded xlsx, formulas + comments dumped)
OPS_OFFLOADS = [
    # row, consumed_lot, railcar, full_lb, empty_lb, net_kg(F), sparging(H), filtration(I), unc_adj(J), MOBI(K), alloc_truck_mi(L), rail_mi(M), opel_mi(N), C(O)
    (28, "Rail_GRPX5254_7.17.2026_offload_1", "GRPX5254", 71660, 28800, 19440.95312, 250.7882952, 37.61272306, 0,        19152.5521,  80.51505562, 2199, 85.8, 0.504),
    (29, "Rail_GRPX5254_7.17.2026_offload_2", "GRPX5254", 73380, 29620, 19849.18592, 256.0544984, 38.40253759, 0,        19554.72888, 82.20575908, 0,    85.8, 0.504),
    (30, "Rail_GRPX5254_7.17.2026_offload_3", "GRPX5254", 74260, 28400, 20801.72912, 268.3423056, 40.24543816, 0,        20493.14138, 86.1507338,  0,    85.8, 0.504),
    (31, "Rail_GRPX5254_7.17.2026_offload_4", "GRPX5254", 68140, 29420, 17563.08224, 226.5637609, 33.97957622, 0,        17302.5389,  72.73781973, 0,    85.8, 0.504),
    (32, "Rail_GPRX5107_7.29.2026_offload_1", "GPRX5107", 78360, 29440, 22189.72064, 286.2473963, 42.93080756, 0,        21860.54244, 91.73419954, 2199, 85.8, 0.504),
    (33, "Rail_GPRX5107_7.29.2026_offload_2", "GPRX5107", 74140, 28640, 20638.436,   266.2358244, 39.92951234, 0,        20332.27066, 85.3210564,  0,    85.8, 0.504),
    (34, "Rail_GPRX5107_7.29.2026_offload_3", "GPRX5107", 72600, 28480, 20012.47904, 258.1609796, 38.7184634,  0,        19715.5996,  82.73329689, 0,    85.8, 0.504),
    (35, "Rail_GPRX5107_7.29.2026_offload_4", "GPRX5107", 62780, 29300, 15186.26016, 195.6847997, 29.34841186, 16.89584, 14944.33111, 62.71144716, 0,    85.8, 0.504),
]

def ticket_pairs():
    out = {}
    for rc in ("GRPX5254", "GPRX5107"):
        out[rc] = {}
        for n in range(1, 5):
            full = next(t for t in TICKETS if t[0] == rc and t[1] == n and t[2] == "FULL")
            empty = next(t for t in TICKETS if t[0] == rc and t[1] == n and t[2] == "EMPTY")
            ops = next(o for o in OPS_OFFLOADS if o[2] == rc and o[0] == 27 + n + (0 if rc == "GRPX5254" else 4))
            net_lb = full[4] - empty[4]
            net_kg = round(net_lb * KG_PER_LB, 5)
            out[rc][f"offload_{n}"] = {
                "full_ticket": {"filename": full[12], "ticket_number": full[3], "gross_weight_lb": full[4], "date": full[5], "time": full[6], "scale_number": full[7], "scale_location": full[8], "tractor": full[9], "trailer": full[10], "commodity_label_on_ticket": full[11]},
                "empty_ticket": {"filename": empty[12], "ticket_number": empty[3], "gross_weight_lb": empty[4], "date": empty[5], "time": empty[6], "scale_number": empty[7], "scale_location": empty[8], "tractor": empty[9], "trailer": empty[10], "commodity_label_on_ticket": empty[11]},
                "tractor_match": full[9] == empty[9],
                "trailer_match": full[10] == empty[10],
                "computed_net_lb": net_lb,
                "computed_net_kg": net_kg,
                "ops_notes_row": ops[0],
                "ops_notes_full_lb": ops[3],
                "ops_notes_empty_lb": ops[4],
                "ops_notes_net_kg": ops[5],
                "ops_full_matches_ticket": ops[3] == full[4],
                "ops_empty_matches_ticket": ops[4] == empty[4],
                "net_kg_delta_vs_ops": round(net_kg - ops[5], 5),
            }
    return out

scale_tickets = ticket_pairs()
scale_tickets["_primary_source_opened"] = [
    {"file": t[12], "action": "image_read", "artifact_path": f"tickets/{t[12]}",
     "evidence": f"CAT Scale ticket {t[3]}: GROSS {t[4]} LB, {t[5]} {t[6]}, scale {t[7]} {t[8]}, tractor {t[9]}, trailer {t[10]}, commodity '{t[11]}'"}
    for t in TICKETS
]
scale_tickets["_summary"] = {
    "pairs_read": 8, "tickets_read": 16,
    "rig_mismatches": [],
    "note_railcar_spelling": "All 16 tickets print the railcar as 'GPRX5254' / 'GPRX5107'. Ops Notes, the Drive folder, the consumed_lot labels and the 8 Certify source filenames spell the first railcar 'GRPX5254' (R and P transposed). The rail BOLs do not name the railcar. Same physical car, different spelling.",
    "note_ld_vs_o_labels": "Tickets label offloads inconsistently ('LD2'/'LD4' on CH1/KL720 rig, 'O1'/'O3' on CH2/KL188 rig). GPRX5107 LD1 pair uses 'LD1' on both tickets; GPRX5107 O2/O3 use 'O' form.",
    "empty_after_full_all_pairs": True,
}

# ---------------- BOLs (20 PDFs, pages 1-3 read as images) ----------------
RAIL_BOLS = [
    # bol, date_p1, railcar(ops), p1_MT, p1_kg_est, p3_qty_shipped_MT, p3_delivered_kg, p3_tare_kg, p3_full_kg, truck, tanker, carrier, weigh_slip_net_kg, file
    ("2430-R", "2026-07-15", "GRPX5254", 25.55, 25552, 25.98, 25980, 19610, 45590, "921",  "21607",  "Transport Baie-Comeau", 25980, "Documents Camion 2430-R CHARM PO Q42025.pdf"),
    ("2431-R", "2026-07-15", "GRPX5254", 25.45, 25450, 25.84, 25840, 19330, 45170, "2114", "22095",  "Transport Baie-Comeau", 25840, "Envoi des documents 2431-R.pdf"),
    ("2432-R", "2026-07-15", "GRPX5254", 25.76, 25764, 26.05, 26050, 19690, 45740, "921",  "21607",  "Transport Baie-Comeau", 26050, "Documents Camion 2432-R CHARM PO Q42025.pdf"),
    ("2444-R", "2026-07-27", "GPRX5107", 25.59, 25594, 25.86, 25860, 18920, 44780, "2623", "21607",  "Transport Baie-Comeau", 25860, "documents 2444-R.pdf"),
    ("2445-R", "2026-07-28", "GPRX5107", 25.81, 25814, 26.06, 26060, 19030, 45090, "2416", "22095",  "Transport Baie-Comeau", 26060, "Documents camion 2445-R.pdf"),
    ("2446-R", "2026-07-28", "GPRX5107", 25.91, 25914, 26.09, 26090, 19170, 45260, "2623", "21-607", "Transport Baie-Comeau", 26090, "Documents camion 2446-R.pdf"),
]
TRUCK_BOLS = [
    # bol, date_p1, p1_MT_est, p3_qty_shipped_MT, p3_delivered_kg, p3_tare_kg, p3_full_kg, truck, tanker, carrier, ops_date, ops_MT, file, note
    ("2481-T", "2026-08-21", 21.00, 19.98, 19980, 16060, 36040, "1291",   "36418",  "SVB Solutions",   "2026-08-28", 19.98, "Billing Documents 2481-T.pdf", ""),
    ("2484-T", "2026-08-23", 20.03, 20.03, 20030, 15900, 35930, "2362",   "7217",   "Blue Tanker",     "2026-08-31", 20.03, "Billing Documents 2484-T.pdf", ""),
    ("2485-T", "2026-08-23", 20.33, 20.04, 20040, 14590, 34630, "815",    "1009",   "Shram",           "2026-08-28", 20.04, "Billing Documents 2485-T.pdf", ""),
    ("2486-T", "2026-08-24", 20.48, 19.92, 19920, 15960, 35880, "2207",   "36626",  "Tandet Logistics","2026-09-02", 19.92, "Billing Documents 2486-T.pdf", ""),
    ("2487-T", "2026-08-24", 20.34, 19.82, 19820, 15460, 35280, "387",    "3426",   "Shram",           "2026-08-29", 19.82, "Billing Documents 2487-T.pdf", ""),
    ("2488-T", "2026-08-25", 20.26, 19.22, 19220, 15870, 35090, "2213",   "36654",  "SVB Solutions",   "2026-09-02", 19.22, "Billing documents 2488-T.pdf", ""),
    ("2489-T", "2026-08-25", 20.94, 19.87, 19870, 15420, 35290, "33639",  "36675",  "SVB Solutions",   "2026-09-02", 19.87, "Billing Documents 2489-T.pdf", ""),
    ("2490-T", "2026-08-25", 20.02, 19.86, 19860, 15470, 35330, "33690",  "36574",  "SVB Solutions",   "2026-09-02", 19.86, "Billing Documents 2490-T.pdf", ""),
    ("2491-T", "2026-08-25", 19.66, 19.92, 19920, 14140, 34060, "818",    "1018",   "Shram",           "2026-09-02", 19.92, "Billing documents 2491-T.pdf", ""),
    ("2492-T", "2026-08-26", 20.17, 27.01, 27010, 15860, 42870, "2208",   "36657",  "Shram",           "2026-08-31", 20.17, "Billing Documents 2492-T.pdf",
        "SELF-CONTRADICTING BOL. Page 1: 17,024 L / 20,173 kg / 20.17 M.Ton (tank 3 level change 148,041 -> 131,017 L = 17,024 L; x1.185 = 20,173 kg). Page 3 'Analytical Details': 'Quantity sent in litres at 60F' 22,523, 'Quantity send in M.Tons at 60F' 27.01, 'Tanker Full wt (Kg) 42,870' minus 'Tanker Tare wt(empty) (Kg) 15,860' = 27,010 kg. The page-3 figure is physically implausible: truck capacity printed on the same page is 20,500 kg and 42,870 kg gross = 94,511 lb, above US road limits; page-3 'Quantity sent in litres' 22,523 L exceeds the 17,024 L level change on page 1. Ops Notes uses 20.17 MT (cell comment C19 documents the choice). Certify Bio-Oil Mass - AECN 277.790 t includes 20,170 kg for this BOL."),
    ("2493-T", "2026-08-26", 20.69, 19.32, 19320, 15540, 34860, "418",    "3414",   "Shram (handwritten 'CH Robinson' over carrier field)", "2026-08-31", 19.32, "BOL 2493-T (corrige).pdf", "Page 3 is the AECN weigh slip (Masse nette 19 320 kg); page 2 is the Analytical Details."),
    ("2494-T", "2026-08-27", 21.34, None, 19880, 15300, 35180, "102114", "607606", "Shram",           "2026-09-01", 19.88, "Billing documents 2494-T - Corr.pdf",
        "Header '***Corrections : density and final liters'. Page 1 = 21.34 M.Ton estimate; page 2 = Commercial Invoice (21.34 MT, US$6,990.27); page 3 = AECN weigh slip PC0039568: Masse brute 35 180 kg, tare 15 300 kg, Masse nette 19 880 kg. No Analytical Details page in the first 3 pages; Ops 19.88 MT = weigh-slip net."),
    ("2495-T", "2026-08-29", 20.83, 19.99, 19990, 15350, 35340, "102295", "603308", "Shram",           "2026-09-03", 19.99, "Billing Documents 2495-T.pdf",
        "Ops cell comment C22: COBB quantity for 2495-T reads 19,510 kg vs BOL 19,990 kg (480 kg / 2.4%); BOL used per policy; flagged to Garrett in the comment."),
    ("2496-T", "2026-08-29", 19.51, 19.77, 19770, 16090, 35860, "2216",   "36585",  "Tandet Logistics","2026-09-04", 19.77, "Billing Documents 2496-T.pdf", ""),
]

bols = {
    "rail": {b[0]: {"date_page1": b[1], "railcar_per_ops_notes": b[2], "page1_estimated_MT": b[3], "page1_estimated_kg": b[4],
                    "page3_qty_shipped_MT": b[5], "page3_product_delivered_kg": b[6], "page3_tanker_tare_kg": b[7], "page3_tanker_full_kg": b[8],
                    "truck_id": b[9], "tanker_id": b[10], "carrier": b[11], "aecn_weigh_slip_masse_nette_kg": b[12], "file": b[13],
                    "ship_to": "CHARM Industrial Inc. /WATCO, Societe du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau, Quebec G4Z 2L6",
                    "from": "BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9",
                    "prod_period": "#07-2026", "customer_po": "Q42025",
                    "ops_notes_mass_MT": b[5], "matches_ops_notes": True} for b in RAIL_BOLS},
    "rail_sum_check": {
        "GRPX5254_bol_sum_kg": 25980 + 25840 + 26050, "GRPX5254_ops_total_loaded_kg": 77870,
        "GPRX5107_bol_sum_kg": 25860 + 26060 + 26090, "GPRX5107_ops_total_loaded_kg": 78010,
        "match": True},
    "truck": {b[0]: {"date_page1": b[1], "page1_estimated_MT": b[2], "page3_qty_shipped_MT": b[3], "page3_product_delivered_kg": b[4],
                     "page3_tanker_tare_kg": b[5], "page3_tanker_full_kg": b[6], "truck_id": b[7], "tanker_id": b[8], "carrier": b[9],
                     "ops_notes_date": b[10], "ops_notes_bol_mass_MT": b[11], "file": b[12], "note": b[13],
                     "ship_to": "CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA",
                     "from": "BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9",
                     "prod_period": "#08-2026", "customer_po": "Q4-2025",
                     "matches_ops_notes": (b[3] == b[11]) if b[3] is not None else (b[4] == round(b[11] * 1000))} for b in TRUCK_BOLS},
    "truck_sum_check": {"ops_notes_sum_bol_kg": 277790, "sum_of_ops_masses_kg": int(round(sum(b[11] for b in TRUCK_BOLS) * 1000)),
                        "sum_of_bol_page3_delivered_kg_as_printed": sum(b[4] for b in TRUCK_BOLS),
                        "delta_if_2492T_page3_used_kg": 27010 - 20170,
                        "certify_bio_oil_mass_AECN_t": 277.790, "match_to_ops": True},
    "destination_check": {"rail_bols_ship_to_SOPOR_confirmed_on_page1": ["2430-R", "2431-R", "2432-R", "2444-R", "2445-R", "2446-R"],
                          "truck_bols_ship_to_St_Landry_LA_confirmed_on_page1": [b[0] for b in TRUCK_BOLS],
                          "vaulted_references_found": []},
    "_primary_source_opened": [
        {"file": b[13], "action": "pdf_read", "artifact_path": f"bols/{b[13]}", "evidence": f"Pages 1-3 read as images: BOL {b[0]} dated {b[1]}, ship to SOPOR Baie-Comeau, page 3 Qty shipped {b[5]} M.Tons, weigh slip Masse nette {b[12]} kg"} for b in RAIL_BOLS
    ] + [
        {"file": b[12], "action": "pdf_read", "artifact_path": f"bols/{b[12]}", "evidence": f"Pages 1-3 read as images: BOL {b[0]} dated {b[1]}, ship to CHARM St Landry LA, page-3 qty {b[3]} M.Tons / delivered {b[4]} kg"} for b in TRUCK_BOLS
    ],
}

# ---------------- Ops Notes ----------------
ops_notes = {
    "file": "INJ-09-2026-W1 Ops Notes (Google Sheet, owner garrett.lutz@; exported to xlsx 2026-09-17 and read with openpyxl WITHOUT data_only so comments were captured)",
    "sheet_id": "1_nXYsz50d2ZLQSE2Zkj_CTN2WzZciFc0XnNUEPJxIjo",
    "live_source_url": OPS_URL,
    "artifact_path": "INJ-09-2026-W1_Ops_Notes.xlsx",
    "sheets": ["Summary", "AECN Rail", "AECN Truck", "WODO", "Kerry", "QOWV", "Whole Oil", "QOWV Shipments & EE Allocation", "WODO Shipments & EE Allocation", "Whole Oil Shipments & EE Alloca"],
    "batch_id_B2": "INJ-09-2026-W1", "week_start_B3": "2026-08-29", "week_end_B4": "2026-09-05",
    "_primary_source_opened": [
        {"file": "INJ-09-2026-W1_Ops_Notes.xlsx", "action": "sheet_grid_read", "live_source_url": OPS_URL, "artifact_path": "ops_notes_dump.txt",
         "evidence": "Every non-empty cell of Summary, AECN Rail, AECN Truck dumped with formulas, cached values and cell comments (ops_notes_dump.txt)."}],
    "aecn_rail_tab": {
        "constants": {"O3_lbs_per_kg": 2.20462, "O4_kg_per_lb": 0.453592, "O5_sparging": 0.0129, "O6_pH_target": "2.0 - 4.0", "O7_filtration_solids": 0.00196, "O8_bol_trips_AECN_SOPOR": 3, "O9_round_trip_opel_basco": 2},
        "railcars_received": {
            "GRPX5254": {"row": 10, "arrival_opelousas": "2026-09-02", "bols": "2430-R, 2431-R, 2432-R", "total_loaded_MT": 77.87, "total_loaded_kg": 77870, "total_offloaded_kg_F": 77654.9504, "loss_kg_G": 215.0496, "prev_claimed_kg": 0, "prior_rp_claimed_kg": 0, "aecn_sopor_mi": 107.5, "rail_mi": 2199, "opel_basco_mi": 42.9, "full_flag_P": "FULL",
                         "notes_M": "New railcar this RP. Loaded 7/15/2026 at SOPOR (BOLs 2430-R/2431-R/2432-R, 77,870 kg). All 4 offloads logged this week, scale-ticket confirmed (delta <1 kg vs COBB on all 4). Prior-RP claimed: 0 kg."},
            "GPRX5107": {"row": 11, "arrival_opelousas": "2026-08-27", "bols": "2444-R, 2445-R, 2446-R", "total_loaded_MT": 78.01, "total_loaded_kg": 78010, "total_offloaded_kg_F": 78026.89584, "loss_kg_G": -16.89584, "prev_claimed_kg": 0, "prior_rp_claimed_kg": 0, "aecn_sopor_mi": 107.5, "rail_mi": 2199, "opel_basco_mi": 42.9, "full_flag_P": "FULL",
                         "notes_M": "New railcar this RP. Loaded 7/27-7/29/2026 at SOPOR (BOLs 2444-R/2445-R/2446-R, 78,010 kg). FLAG: offload 3 (LD3, COBB target 19,995.58 kg) has NO resolvable CAT scale-ticket pair after a wide Gmail harvest (2026-08-15 to 2026-09-15) -- Full/Empty left BLANK per policy; Loss suppressed (58,014.42 / 78,010 kg = 74% < 95% closure threshold) until ticket located. Prior-RP claimed: 0 kg.",
                         "notes_M_is_stale": "Row 34 (offload_3) is populated (72,600 / 28,480 lb) and its D34 comment says the pair was 'Recovered 2026-09-11'; M11 still carries the pre-recovery FLAG text."}},
        "origins_ledger": [{"row": r, "date": d, "bol": b, "railcar": rc, "MT": mt, "kg": kg} for r, d, b, rc, mt, kg in [
            (17, "2026-07-15", "2430-R", "GRPX5254", 25.98, 25980), (18, "2026-07-15", "2431-R", "GRPX5254", 25.84, 25840), (19, "2026-07-15", "2432-R", "GRPX5254", 26.05, 26050),
            (21, "2026-07-27", "2444-R", "GPRX5107", 25.86, 25860), (22, "2026-07-28", "2445-R", "GPRX5107", 26.06, 26060), (23, "2026-07-28", "2446-R", "GPRX5107", 26.09, 26090)]],
        "offload_table": [{"row": o[0], "id": o[1], "railcar": o[2], "date_A": "2026-09-04", "full_lb_D": o[3], "empty_lb_E": o[4], "net_kg_F": o[5], "pH_G": None, "sparging_kg_H": o[6], "filtration_kg_I": o[7], "uncertainty_adj_kg_J": o[8], "MOBI_kg_K": o[9], "alloc_aecn_sopor_mi_L": o[10], "rail_mi_M": o[11], "opel_basco_mi_N": o[12], "C_content_O": o[13]} for o in OPS_OFFLOADS],
        "offload_table_formulas": {"F": "(D-E)*$O$4", "H": "(F-J)*$O$5", "I": "(F-J)*(1-$O$5)*$O$7", "K": "F-H-I-J", "L": "(F-J)/E_railcar*J_railcar*$O$8", "M": "2199 entered on first offload row of each railcar only (2199 x 2 railcars = 4398)", "N": "L_railcar*$O$9 (42.9 x 2 = 85.8 per offload)"},
        "distance_rollup_row36": {"L36_alloc_aecn_sopor_mi": 644.1093682, "M36_rail_mi": 4398, "N36_opel_basco_mi": 686.4},
        "rollup_row44": {"A44_sum_deliveries_raw_kg": 155880, "B44_sum_uncertainty_adj_kg": 16.89584, "C44_mass_used_post_adj_kg": 155863.1042, "D44_sparging_kg": 2008.07786, "E44_filtration_kg": 301.1674702, "F44_MOBI_kg": 153553.8588, "G44_pH": None, "H44_C_content": 0.504, "M44_origins": "2430-R, 2431-R, 2432-R, 2444-R, 2445-R, 2446-R"},
        "rollup_note": "A44 = SUM(E17:E23) = sum of the 6 loading BOLs (155,880 kg) -- i.e. the rail 'deliveries' basis is the BOL aggregate, not the scale-ticket sum (155,681.85 kg). C44 = 155,880 - 16.89584 = 155,863.1042 kg = Certify 'Bio-Oil Mass - AECN via Rail' 155.863 t.",
        "_primary_source_opened_cell_comments": [
            {"cell": "D29", "text": "Provenance corrected 2026-09-11. This offload previously cited full ticket 1124426237444, which is labelled GPRX5236 LD2 and dated 8-25-26 -- a different railcar, from the August week -- paired with an unlabelled 9-03 empty (1312226246373). Both pairs give an identical 43,760 lb delta, so the MASS was always right; only the evidence was wrong. Now cites the correctly labelled GPRX5254 LD2 pair: FULL 1124426245497 (73,380 lb) / EMPTY 1312226245354 (29,620 lb), both 9-02. Reminder: a +0.00 reconciliation proves the mass, never the ticket."},
            {"cell": "D34", "text": "Recovered 2026-09-11. Both tickets ARE labelled GPRX5107 but carry no LD number (a documented label variant), which is why an earlier label search reported no pair. LD assigned by trailer + chronology: CH2 ran LD2 and LD3, CH1 ran LD1 and LD4. FULL 1124426244484 (72,600 lb, 9-01 10:51, CH2); EMPTY 1312226244341 (28,480 lb, 9-01 15:35, CH2). Net 20,012.48 kg vs COBB 19,995.58 (+16.90) -- scale ticket is authoritative over COBB per rig-QC rule. Corroboration: with LD3 included the four offloads sum to 78,026.90 kg against a BOL of 78,010, a 16.90 kg overage now trued up by the col-J uncertainty adjustment."},
            {"cell": "(all other offload cells)", "text": "no comment"}],
    },
    "aecn_truck_tab": {
        "constants": {"L3": 2.20462, "L4": 0.453592, "L5_sparging": 0.0129, "L6_pH_target": "2.0 - 4.0", "L7_filtration": 0.00196},
        "methodology_header_A26": "SECTION 2 - ROLLUP  (Mass Used = Σ BOL kg; scale tickets no longer required for direct trucks per 2026-05-26)",
        "deliveries": [{"row": 10 + i, "date": b[10], "bol": b[0], "bol_MT": b[11], "bol_kg": int(round(b[11] * 1000)), "scale_full_lb": None, "scale_empty_lb": None, "cargo_kg_G": None, "pH_H": None, "C_content_M": 0.504, "EE_miles_N": 2197} for i, b in enumerate(TRUCK_BOLS)],
        "N25_sum_EE_miles": 30758,
        "rollup_row28": {"A28_sum_bol_kg": 277790, "B28_sum_cargo_kg": 0, "C28_mass_used_kg": 277790, "D28_sparging_kg": 3583.491, "E28_filtration_kg": 537.4447576, "F28_uncertainty_adj_kg": 0.0, "G28_MOBI_kg": 273669.0642, "H28_pH": None, "I28_C_content": 0.504, "K28_origins": "2481-T, 2484-T, 2485-T, 2486-T, 2487-T, 2488-T, 2489-T, 2490-T, 2491-T, 2492-T, 2493-T, 2494-T, 2495-T, 2496-T"},
        "cell_comments": [
            {"cell": "C19 (2492-T BOL Mass MT = 20.17)", "text": "Corrected 2026-09-11 from 27.01 to 20.17 MT per Garrett. The BOL scan states Qty shipped 27.01 M.Tons and is internally consistent with tanker full 42,870 - tare 15,860 = 27,010 kg and with 22,523 L x 1.1992 density. BUT the same BOL also reports Volume loaded with level change = 17,024 L / 4,498 Usgal, and 17,024 x 1.1992 = 20,415 kg - i.e. the BOL contradicts itself across two volume bases, 6,840 kg apart. Loads tab col Q (the canonical BOL-mass-at-60F source) reads 20.17 MT and its col R gallons (4,498) matches the BOL level-change volume exactly. 27.01 t would also be a 33 percent outlier against the other 13 loads this week (19.22-20.04 t). Adopted the Loads value. Raise with AECN/Samah if the BOL is meant to be authoritative."},
            {"cell": "C22 (2495-T BOL Mass MT = 19.99)", "text": "COBB quantity_consumed_in_injection / offloaded_quantity_kg for 2495-T reads 19,510 kg, but the AECN Analytical Details BOL (2495-T, RS2-280829-1) shows 'Quantity send in M.Tons at 60F' = 19.99 MT = 19,990 kg -- a 480 kg / 2.4% discrepancy. Per COBB-validation policy the BOL is authoritative; 19,990 kg is used here. Flag to Garrett / upstream COBB owner for correction."}],
        "pH_blank_all_rows": True,
    },
    "summary_tab": {"A2_batch": "INJ-09-2026-W1", "B3_week_start": "2026-08-29", "B4_week_end": "2026-09-05"},
}

# ---------------- VVB guidance ----------------
vvb_guidance = {
    "search_performed": [
        "Drive search title contains 'VVB Guidance' (20 results, 2 pages) -- newest period doc is 'VVB Guidance August 1 - August 31' (id 1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y, modified 2026-09-11T01:39Z)",
        "Drive search title contains 'VVB Guidance' and title contains 'September' -- only 2025 documents ('August/September VVB Guidance', Sep 2025)",
        "Drive search (title contains 'Guidance') and (fullText contains 'INJ-09-2026' or fullText contains 'September 1') -- no 2026 September document",
        "Listing of the August guidance doc's parent folder 1bhqYLfG7Cbc70oOyKOHK7GR_YO-g8jCK -- August items only",
    ],
    "september_2026_guidance_doc_exists": False,
    "doc_read_instead": "VVB Guidance August 1 - August 31 (the most recent period doc), read in full",
    "doc_id": "1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y",
    "live_source_url": VVB_URL,
    "owner": "garrett.lutz@charmindustrial.com",
    "artifact_path": "VVB_Guidance_August_1-31_fetched_2026-09-17.txt",
    "_primary_source_opened": [{"file": "VVB Guidance August 1 - August 31", "action": "pdf_read", "live_source_url": VVB_URL, "artifact_path": "VVB_Guidance_August_1-31_fetched_2026-09-17.txt", "evidence": "Fetched as text via docs export URL 2026-09-17 and read end to end (101 lines)."}],
    "sections": ["Trailer Standard Empty Weight (AECN Rail Offloads)", "QOWV Tote Transport -- Totes Routed via Kansas (Weeks 3 and 4)", "AECN Pyrolysis Process Emissions -- Updated H2 2026 Emission Factor", "Bio-Oil Spill at the SOPOR Rail Transload, Baie-Comeau -- GPRX5139", "Spare Parts and Consumables -- Day-Based Scaling and a July 2026 True-Up", "Annual Well Work at Basco 6 -- Workover and Tracer Survey", "Inspection Reporting", "Oxidizer Sensor Signal Interruptions"],
    "standard_tare_table": {"KL192": 29510, "KL188": 29307, "KL720": 29645, "KL510": 29478},
    "standard_tare_trigger_quote": "substitute the standard empty weight for the trailer recorded on the Full ticket when either (a) the empty scale ticket is missing, or (b) the empty ticket's tractor and/or trailer do not match the Full ticket. Substituted values are annotated in the ops-notes Empty Scale Ticket cell.",
    "w1_sept_coverage_check": "Document names no INJ-09-2026 offload, railcar GPRX5107/GRPX5254 or truck BOL 2481-T..2496-T. No standard-tare substitution is needed this week (all 8 pairs match), so no coverage was required for the tare method.",
    "pyrolysis_ef_update_quote": "The assessment built on January to June 2026 operating data became available during this reporting period and supersedes the one applied through the July 1 - July 31 RP. It governs every AECN removal in this period and in subsequent H2 2026 periods.",
    "spill_check": "The only disclosed spill (GPRX5139, August W3) involves neither of this batch's railcars.",
}

# ---------------- lab ----------------
lab_results = {
    "file": "SR26-05371 09-2026-W1 AECN.pdf (Drive Testing subfolder id 1uEG4UNe5gCHo4M55OWK4Hd1w62Hca-nu; also Certify source #4)",
    "artifact_path": "SR26-05371_09-2026-W1_AECN.pdf",
    "certificate_number": "SR26-05371.001", "sgs_order_no": "5494492", "client_id": "09-2026-W1 AECN", "location": "BASCO LOUISIANA",
    "sampled": "2026-09-05 07:00", "received": "2026-09-09 12:00", "analysed": "2026-09-09 15:04 - 16:57", "report_date": "2026-09-09",
    "carbon_pct": 50.4, "carbon_method": "ASTM D5291 (Method C)", "carbon_flag_hash": "# - Result is outside of test method limits and/or analytical range used in method precision study",
    "hydrogen_pct": 7.1, "hydrogen_flag_hash": True, "nitrogen_pct": "<0.75",
    "kinematic_viscosity_cSt_40C": 269.4, "acid_number_mgKOHg": 46, "density_g_cm3_at_15C": 1.219,
    "aecn_stats": {"source_file": "MRV_AECN_Analysis.xlsx (Drive id 1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi, downloaded and read with openpyxl this session)", "artifact_path": "MRV_AECN_Analysis.xlsx", "live_source_url": "https://drive.google.com/file/d/1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi/view",
                   "tab": "Summary Statistics", "filter_A2": "Filtered to Function = MRV, Offtake = AECN (439 samples)",
                   "carbon_mean_B5": 39.420350877193, "carbon_sd_B6": 6.09332409018271, "carbon_n_B7": 285,
                   "hydrogen_mean_C5": 6.87438596491228, "hydrogen_sd_C6": 0.562848694875852,
                   "two_sd_low": 27.2337, "two_sd_high": 51.607, "batch_carbon_within_2sd": True, "batch_carbon_z": round((50.4 - 39.420350877193) / 6.09332409018271, 3)},
    "second_lab_file_in_testing_folder": "SR26-05444 09-2026-W1 WODO.pdf (WODO, not this removal)",
    "_primary_source_opened": [
        {"file": "SR26-05371_09-2026-W1_AECN.pdf", "action": "pdf_read", "artifact_path": "SR26-05371_09-2026-W1_AECN.pdf", "evidence": "Page 1 of 1 read: Carbon 50.4 % (m/m) #, Hydrogen 7.1 #, Nitrogen <0.75, viscosity 269.4 cSt, acid number 46, density 1.219 g/cm3, CLIENT ID 09-2026-W1 AECN, SAMPLED 05-Sep-2026 07:00"},
        {"file": "MRV_AECN_Analysis.xlsx", "action": "sheet_grid_read", "live_source_url": "https://drive.google.com/file/d/1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi/view", "artifact_path": "MRV_AECN_Analysis.xlsx", "evidence": "Summary Statistics B5=39.420350877193, B6=6.09332409018271, B7=285"}],
}

# ---------------- Certify (tabs read this session; component modals appended by patch script) ----------------
SOURCES = [
    (1, "INJ-09-2026-W1 Ops Notes - 2026-09-17", "Allocated Distance Sopor Quebec to Opelousas (rail) + 6 more", "Private"),
    (2, "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jun2026.xlsx", "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) + 1 more", "Private"),
    (3, "Supporting GHG data 30Jun2026 S.xlsx", "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) + 1 more", "Private"),
    (4, "SR26-05371 09-2026-W1 AECN.pdf", "Carbon Content of Bio-oil Injected (per injection)", "Private"),
] + [(5 + i, n, "Bio-Oil Mass - AECN via Rail + 1 more", "Private") for i, n in enumerate([
    "Full_GPRX5107_offload_4.pdf", "Empty_GPRX5107_offload_4.pdf", "Full_GPRX5107_offload_3.pdf", "Empty_GPRX5107_offload_3.pdf",
    "Full_GPRX5107_offload_2.pdf", "Empty_GPRX5107_offload_2.pdf", "Full_GPRX5107_offload_1.pdf", "Empty_GPRX5107_offload_1.pdf",
    "Full_GRPX5254_offload_4.pdf", "Empty_GRPX5254_offload_4.pdf", "Full_GRPX5254_offload_3.pdf", "Empty_GRPX5254_offload_3.pdf",
    "Full_GRPX5254_offload_2.pdf", "Empty_GRPX5254_offload_2.pdf", "Full_GRPX5254_offload_1.pdf", "Empty_GRPX5254_offload_1.pdf"])
] + [(21 + i, f"BOL_{b}.pdf", "Bio-Oil Mass - AECN via Rail", "Private") for i, b in enumerate(["2446-R", "2445-R", "2444-R", "2432-R", "2431-R", "2430-R"])
] + [(27 + i, f"BOL_{b}.pdf", "Bio-Oil Mass - AECN + 1 more", "Private") for i, b in enumerate(["2496-T", "2495-T", "2494-T", "2493-T", "2492-T", "2491-T", "2490-T", "2489-T", "2488-T", "2487-T", "2486-T", "2485-T", "2484-T", "2481-T"])
] + [
    (41, "Aug-28-2026-distance-route_map.png", "Allocated Distance AECN to Sopor Quebec (truck)", "Public"),
    (42, "Sep-03-2026-distance-route_map.png", "Allocated Distance AECN to Sopor Quebec (truck)", "Public"),
    (43, "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "BCUs Applied - Bio-Oil Transport Process [Certify input]", "Public"),
    (44, "FH 2026 LCA w Stack Emissions.xlsx", "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) + 1 more", "Public"),
    (45, "Standard Emission Factors + Calculations (8).xlsx", "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "Public"),
    (46, "Standard Emission Factors + Calculations (8).xlsx", "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "Public"),
    (47, "AECN Embodied Emissions Calc Sheet (1).pdf", "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail) + 1 more", "Public"),
    (48, "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf", "Emissions Factor - Vehicle Embodied Emissions -- Railcar", "Public"),
    (49, "Opelousas Railyard to Basco.png", "Allocated Distance Opelousas to B6 (truck) + 1 more", "Public"),
    (50, "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf", "Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "Public"),
    (51, "AECN to SOPOR (Baie Comeau) (2).png", "Allocated Distance AECN to Sopor Quebec (truck) + 1 more", "Public"),
    (52, "image (44).png", "Allocated Distance Sopor Quebec to Opelousas (rail) + 1 more", "Public"),
    (53, "AECN to Basco.png", "Aggregate Distance Transported AECN to Basco + 1 more", "Public"),
]

DATAPOINTS = [
    ("Mass of Injectant (per injection)", "427.223 t", "Reported", ["Empty_GRPX5254_offload_1.pdf", "+ 30 more"]),
    ("Carbon Content of Bio-oil Injected (per injection)", "50.40 %", "Derived", ["SR26-05371 09-2026-W1 AECN.pdf", "+ 1 more"]),
    ("BCUs Applied - Bio-Oil Transport Process [Certify input]", "81.318 tCO2e", "Reported", ["Charm-RetirementCertificate-RD-EACs-20251218.pdf"]),
    ("Bio-Oil Mass - AECN", "277.790 t", "Reported", ["BOL_2486-T.pdf", "+ 14 more"]),
    ("Carbon Intensity - AECN Pyrolysis Process Emissions (direct to B6)", "0.14 tCO2e/t", "Derived", ["FH 2026 LCA w Stack Emissions.xlsx", "+ 2 more"]),
    ("Carbon Intensity - AECN Pyrolysis Embodied Emissions (direct to B6)", "0.02 tCO2e/t", "Reported", ["AECN Embodied Emissions Calc Sheet (1).pdf"]),
    ("Bio-Oil Mass - AECN via Rail", "155.863 t", "Reported", ["Empty_GRPX5254_offload_1.pdf", "+ 22 more"]),
    ("Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)", "0.14 tCO2e/t", "Derived", ["FH 2026 LCA w Stack Emissions.xlsx", "+ 2 more"]),
    ("Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)", "0.02 tCO2e/t", "Derived", ["AECN Embodied Emissions Calc Sheet (1).pdf"]),
    ("Aggregate Distance Transported AECN to Basco", "30,758 mi", "Reported", ["AECN to Basco.png", "+ 1 more"]),
    ("Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "0.1476 kgCO2e/km", "Derived", ["Standard Emission Factors + Calculations (8).xlsx"]),
    ("Distance from AECN to Basco", "2,197 mi", "Derived", ["AECN to Basco.png"]),
    ("Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "0.07 kgCO2e/(km*t)", "Derived", ["Standard Emission Factors + Calculations (8).xlsx"]),
    ("Distance from AECN to Sopor Quebec (truck)", "107 mi", "Derived", ["AECN to SOPOR (Baie Comeau) (2).png"]),
    ("Distance from Sopor Quebec to Opelousas (rail)", "2,199 mi", "Derived", ["image (44).png"]),
    ("Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "0.02 kgCO2e/(km*t)", "Derived", ["GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf"]),
    ("Distance from Opelousas to B6 (truck)", "43 mi", "Derived", ["Opelousas Railyard to Basco.png"]),
    ("Allocated Distance Opelousas to B6 (truck)", "686 mi", "Reported", ["Opelousas Railyard to Basco.png", "+ 1 more"]),
    ("Allocated Distance Sopor Quebec to Opelousas (rail)", "4,398 mi", "Reported", ["image (44).png", "+ 1 more"]),
    ("Emissions Factor - Vehicle Embodied Emissions -- Railcar", "0.0193 kgCO2e/km", "Derived", ["Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf"]),
    ("Allocated Distance AECN to Sopor Quebec (truck)", "644 mi", "Derived", ["Aug-28-2026-distance-route_map.png", "+ 2 more"]),
]

COMPONENTS = {  # Components tab, 14 components, read 2026-09-17
    "Mitigated_total_t": 870.898,
    "BCUs - Applied to Bio-Oil Transport Process Emissions": 81.318,
    "Injection sequestration": 789.580,
    "Emitted_total_t": 157.716,
    "AECN pyrolysis (from rail loads) - embodied emissions": 3.298,
    "AECN pyrolysis (from rail loads) - process emissions": 21.372,
    "AECN pyrolysis (from truck loads) - embodied emissions": 5.878,
    "AECN pyrolysis (from truck loads) - process emissions": 38.091,
    "AECN to LA Tanker Truck Transport Embodied Emissions - AECN": 7.307,
    "AECN to LA Tanker Truck Transport Process Emissions - AECN": 69.758,
    "AECN to SOPOR Tanker Truck Transport Embodied Emissions": 0.153,
    "AECN to SOPOR Tanker Truck Transport Process Emissions": 1.915,
    "Opelousas to Basco - Tanker Truck Transport Process Emissions": 0.764,
    "Opelousas to Basco Tanker Truck Transport Embodied Emissions": 0.163,
    "SOPOR to Opelousas Rail Transport Embodied Emissions": 0.137,
    "SOPOR to Opelousas Rail Transport Process Emissions": 8.880,
    "Pyrolysis_subtotal_t": 68.639, "Bio-oil_transport_activities_subtotal_t": 89.077,
}

attachment_map = {}
for _, name, dp, _vis in SOURCES:
    attachment_map.setdefault(dp.split(" + ")[0], []).append(name)

certify = {
    "removal_id": "rmv_1M2GBNMY91S0H2MB", "url": CERTIFY_URL, "project": "Charm Bio-oil Geologic Storage (prj_1HZSSWBQM1S08H83)",
    "header": {"type": "Removal", "net_tCO2e_displayed": 708.74, "period": "30 Aug 2026 to 04 Sep 2026"},
    "components_tab": COMPONENTS,
    "calculation_view": {"net_co2e_removed_t": 708.742, "sequestrations_t": 789.580, "adjustments_tCO2e": 81.318, "activities_tCO2e": 157.716, "uncertainty_discount_t": 4.440,
                         "recalc": "789.580 + 81.318 - 157.716 - 4.440 = 708.742"},
    "datapoints_count": 21,
    "datapoints": [{"name": n, "value": v, "method": m, "sources_shown": s} for n, v, m, s in DATAPOINTS],
    "sources_tab_total": 53,
    "sources": [{"n": n, "filename": f, "datapoints": dp, "visibility": vis} for n, f, dp, vis in SOURCES],
    "attachment_map": attachment_map,
    "_primary_source_opened": [
        {"file": "Certify Components tab", "action": "modal_opened", "live_source_url": CERTIFY_URL, "artifact_path": "certify_ghg_entry_page.yml", "evidence": "14 components enumerated with tCO2e values"},
        {"file": "Certify Sources tab", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=sources", "artifact_path": "certify_sources_tab.yml", "evidence": "heading 'Sources (53)'; all 53 filenames + linked datapoints enumerated"},
        {"file": "Certify Calculation view + Datapoints", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=calculation-view", "artifact_path": "certify_calculation_view.yml", "evidence": "Net 708.742 t = 789.580 + 81.318 - 157.716 - 4.440; 21 datapoints"},
        {"file": "Certify Datapoints tab", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=datapoints", "artifact_path": "certify_datapoints_tab.yml", "evidence": "21 datapoints with values and first-listed source"},
    ],
}

log = {
    "_schema_version": "1.0",
    "batch_id": "INJ-09-2026-W1",
    "oil_type": "AECN",
    "delivery_mode": "rail + direct truck (combined weekly removal)",
    "injection_site": "Basco 6 LA",
    "reporting_period": "Sep 2026 (Certify entry period 30 Aug 2026 to 04 Sep 2026; Ops week 2026-08-29 to 2026-09-05)",
    "completion_date": "2026-09-04",
    "qa_session_T0_utc": "2026-09-17T23:07:11Z",
    "certify_removal_url": CERTIFY_URL,
    "drive_folder_url": "https://drive.google.com/drive/folders/10r703ReVy1mYtwljJ_uT0lya80r7H5yw",
    "drive_folder": {
        "root_items": ["INJ-09-2026-W1 Ops Notes (Google Sheet)", "Testing/", "Completed QA Checklists/ (empty)", "Scale Tickets/"],
        "scale_tickets_subfolders": {"GPRX5107": ["Offload 1", "Offload 2", "Offload 3", "Offload 4"], "GRPX5254": ["Offload 1", "Offload 2", "Offload 3", "Offload 4"]},
        "scale_ticket_files": [t[12] for t in TICKETS],
        "testing_files": ["SR26-05371 09-2026-W1 AECN.pdf", "SR26-05444 09-2026-W1 WODO.pdf"],
        "bols_in_drive_folder": "none -- BOLs live outside the batch folder and are hyperlinked from the Ops Notes (all 20 downloaded via those links) and uploaded to Certify Sources",
        "_primary_source_opened": [{"file": "Drive folder 10r703ReVy1mYtwljJ_uT0lya80r7H5yw and subfolders", "action": "csv_exported", "live_source_url": "https://drive.google.com/drive/folders/10r703ReVy1mYtwljJ_uT0lya80r7H5yw", "artifact_path": "drive_folder_listing.json", "evidence": "Drive API folder listings (parentId queries) of root, Testing, Scale Tickets, Completed QA Checklists and all 8 Offload subfolders"}],
    },
    "vvb_guidance": vvb_guidance,
    "lab_results": lab_results,
    "ops_notes": ops_notes,
    "scale_tickets": scale_tickets,
    "bols": bols,
    "certify": certify,
    "certify_sources_tab_total": 53,
    "certify_sources_enumeration": [f for _, f, _, _ in SOURCES],
}

if __name__ == "__main__":
    existing = {}
    if OUT.exists():
        existing = json.loads(OUT.read_text())
    # preserve sections filled by later patch steps
    for k in ("cobb", "certify_components", "standard_efs", "_derived_values", "certify_source_file_checks"):
        if k in existing:
            log[k] = existing[k]
    OUT.write_text(json.dumps(log, indent=2, default=str))
    print("wrote", OUT, "keys:", list(log.keys()))
