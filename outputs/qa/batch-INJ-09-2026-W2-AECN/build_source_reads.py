#!/usr/bin/env python3
"""Builds batch_INJ-09-2026-W2-AECN_source_reads.json from values read this session (2026-09-22).
Every number here was read from a primary source opened in-session; see _primary_source_opened blocks."""
import json
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "batch_INJ-09-2026-W2-AECN_source_reads.json"
KG_PER_LB = 0.453592

OPS_URL = "https://docs.google.com/spreadsheets/d/1OEJvgN5KMPKseQrn--RH9QmqDh68zERpf1IMOZN7tvY/edit"
VVB_URL = "https://docs.google.com/document/d/1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc/edit"
VVB_AUG_URL = "https://docs.google.com/document/d/1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y/edit"
EF_URL = "https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705"
COBB_URL = "https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350"
FILT_URL = "https://docs.google.com/spreadsheets/d/1XhIwfVwGTl2T04CAlA-qee03gfqxNWwBmSCAeiSW548/edit"
CERTIFY_URL = "https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M2RKR58N1S0F02M/edit"
DRIVE_URL = "https://drive.google.com/drive/folders/1Oz-oUtmLMxrMQe7cfyzcLEE5ZUg8qzRh"

# ---------------- scale tickets (14 CAT Scale files read as images: 10 PDFs + 4 phone photos) ----------------
# (railcar, offload, kind, ticket#, gross_lb, date, time, scale#, location, tractor, trailer, commodity label, file, format)
TICKETS = [
    ("SHPX215046", 3, "FULL",  "1124426250545", 74320, "2026-09-07", "10:52", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "SHPX215046OFFLOAD3", "Full_Ticket_Rail_SHPX215046_8.7.2026_offload_3.jpg", "phone photo of a PDF viewer"),
    ("SHPX215046", 3, "EMPTY", "1312226250439", 28440, "2026-09-07", "13:48", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "SHPX215046 3",       "Empty_Ticket_Rail_SHPX215046_8.7.2026_offload_3.jpg", "phone photo of a PDF viewer"),
    ("SHPX215046", 4, "FULL",  "1124426250546", 61980, "2026-09-07", "10:55", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL192", "SHPX215046 4",       "Full_Ticket_Rail_SHPX215046_8.7.2026_offload_4.jpg", "phone photo of a PDF viewer"),
    ("SHPX215046", 4, "EMPTY", "1312226251445", 29260, "2026-09-08", "07:07", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL192", "SHPX215046 O4",      "Empty_Ticket_Rail_SHPX215046_8.7.2026_offload_4.jpg", "phone photo of a PDF viewer"),
    ("SHPX215079", 1, "FULL",  "1124426247525", 76720, "2026-09-04", "14:07", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "SHPX215079 1",       "Full_Ticket_Rail_SHPX215079_8.4.2026_offload_1.pdf", "CAT Scale PDF"),
    ("SHPX215079", 1, "EMPTY", "1124426248527", 28660, "2026-09-05", "07:23", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "SHPX215079 OFFLOAD 1", "Empty_Ticket_Rail_SHPX215079_8.4.2026_offload_1.pdf", "CAT Scale PDF"),
    ("SHPX215079", 2, "FULL",  "1124426248528", 73860, "2026-09-05", "09:24", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "SHPX215079 OFFLOAD 2", "Full_Ticket_Rail_SHPX215079_8.4.2026_offload_2.pdf", "CAT Scale PDF"),
    ("SHPX215079", 2, "EMPTY", "1124426248531", 28420, "2026-09-05", "12:03", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH2", "KL188", "SHPX215079 OFFLOAD 2", "Empty_Ticket_Rail_SHPX215079_8.4.2026_offload_2.pdf", "CAT Scale PDF (reweigh, fee $5.25, 'TICKET # OF FULL $ WEIGH 1124426248528')"),
    ("TIMX201060", 1, "FULL",  "1124426246512", 85100, "2026-09-03", "10:02", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "TIMX201060 O1",      "Full_Ticket_Rail_TIMX201060_7.31.2026_offload_1.pdf", "CAT Scale PDF (axles 10,320 / 24,700 / 50,080 lb)"),
    ("TIMX201060", 1, "EMPTY", "1312226246373", 29480, "2026-09-03", "12:21", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL720", "TIMX201060 O1",      "Empty_Ticket_Rail_TIMX201060_7.31.2026_offload_1.pdf", "CAT Scale PDF"),
    ("TIMX201060", 3, "FULL",  "1124426246520", 73220, "2026-09-03", "14:09", "1244", "THE QUARTERS TS, I-49 EXIT 23, OPELOUSAS LA", "CH1", "KL720", "TIMX201060 O3",      "Full_Ticket_Rail_TIMX201060_7.31.2026_offload_3.pdf", "CAT Scale PDF"),
    ("TIMX201060", 3, "EMPTY", "1312226247383", 29860, "2026-09-04", "08:12", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH1", "KL720", "TIMX201060 3",       "Empty_Ticket_Rail_TIMX201060_7.31.2026_offload_3.pdf", "CAT Scale PDF"),
    ("TIMX201060", 4, "FULL",  "1312226246377", 55660, "2026-09-03", "15:06", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "TIMX201060 O4",      "Full_Ticket_Rail_TIMX201060_7.31.2026_offload_4.pdf", "CAT Scale PDF"),
    ("TIMX201060", 4, "EMPTY", "1312226247385", 28780, "2026-09-04", "09:24", "3122", "PILOT TRAVEL CENTER, I 49 EXIT 40, BUNKIE LA",  "CH2", "KL188", "TIMX201060 4",       "Empty_Ticket_Rail_TIMX201060_7.31.2026_offload_4.pdf", "CAT Scale PDF"),
]

# Ops Notes 'AECN Rail' Section 3 rows 28-35 (values read from the exported xlsx; formulas + comments dumped to ops_notes_dump.txt)
OPS_OFFLOADS = [
    # row, consumed_lot, railcar, full_lb(D), empty_lb(E), net_kg(F), sparging(H), filtration(I), unc_adj(J), MOBI(K), alloc_truck_mi(L), rail_mi(M), opel_mi(N), D_has_link, E_has_link
    (28, "Rail_SHPX215046_8.7.2026_offload_3", "SHPX215046", 74320, 28440, 20810.80096, 268.4593324, 40.26298959, 0, 20502.07864, 86.39911573, 589.1214123, 85.8, True, True),
    (29, "Rail_SHPX215046_8.7.2026_offload_4", "SHPX215046", 61980, 29260, 14841.53024, 191.4557401, 28.71414602, 0, 14621.36035, 61.61680616, 420.1406411, 85.8, True, True),
    (30, "Rail_SHPX215079_8.4.2026_offload_1", "SHPX215079", 76720, 28660, 21799.63152, 281.2152466, 42.1760959,  0, 21476.24018, 90.28356447, 615.6079326, 85.8, True, True),
    (31, "Rail_SHPX215079_8.4.2026_offload_2", "SHPX215079", 73860, 28420, 20611.22048, 265.8847442, 39.87685804, 0, 20305.45888, 85.36173886, 582.0479496, 85.8, True, True),
    (32, "Rail_TIMX201060_7.31.2026_offload_1", "TIMX201060", 85100, 29480, 25228.78704, 325.4513528, 48.81053795, 0, 24854.52515, 104.124441,  2199,        85.8, True, True),
    (33, "Rail_TIMX201060_7.31.2026_offload_2", "TIMX201060", 74140, 28480, 20711.01072, 267.1720383, 40.06992382, 0, 20403.76876, 85.47864035, 0,           85.8, False, False),
    (34, "Rail_TIMX201060_7.31.2026_offload_3", "TIMX201060", 73220, 29860, 19667.74912, 253.7139636, 38.05150891, 0, 19375.98365, 81.17288317, 0,           85.8, True, True),
    (35, "Rail_TIMX201060_7.31.2026_offload_4", "TIMX201060", 55660, 28780, 12192.55296, 157.2839332, 23.58912729, 0, 12011.6799,  50.32119695, 0,           85.8, True, True),
]

def ticket_pairs():
    out = {}
    for rc in ("SHPX215046", "SHPX215079", "TIMX201060"):
        out[rc] = {}
        for ops in [o for o in OPS_OFFLOADS if o[2] == rc]:
            n = int(ops[1][-1])
            full = next((t for t in TICKETS if t[0] == rc and t[1] == n and t[2] == "FULL"), None)
            empty = next((t for t in TICKETS if t[0] == rc and t[1] == n and t[2] == "EMPTY"), None)
            entry = {"ops_notes_row": ops[0], "ops_notes_full_lb": ops[3], "ops_notes_empty_lb": ops[4], "ops_notes_net_kg": ops[5],
                     "ops_notes_D_hyperlinked": ops[13], "ops_notes_E_hyperlinked": ops[14]}
            if full and empty:
                net_lb = full[4] - empty[4]
                net_kg = round(net_lb * KG_PER_LB, 5)
                entry.update({
                    "full_ticket": {"filename": full[12], "format": full[13], "ticket_number": full[3], "gross_weight_lb": full[4], "date": full[5], "time": full[6], "scale_number": full[7], "scale_location": full[8], "tractor": full[9], "trailer": full[10], "commodity_label_on_ticket": full[11]},
                    "empty_ticket": {"filename": empty[12], "format": empty[13], "ticket_number": empty[3], "gross_weight_lb": empty[4], "date": empty[5], "time": empty[6], "scale_number": empty[7], "scale_location": empty[8], "tractor": empty[9], "trailer": empty[10], "commodity_label_on_ticket": empty[11]},
                    "tractor_match": full[9] == empty[9], "trailer_match": full[10] == empty[10],
                    "computed_net_lb": net_lb, "computed_net_kg": net_kg,
                    "ops_full_matches_ticket": ops[3] == full[4], "ops_empty_matches_ticket": ops[4] == empty[4],
                    "net_kg_delta_vs_ops": round(net_kg - ops[5], 5)})
            else:
                entry.update({"full_ticket": None, "empty_ticket": None, "tickets_found": False,
                              "search": "Drive Scale Tickets/TIMX201060 has subfolders Offload 1, Offload 3, Offload 4 only (no Offload 2); Ops D33/E33 are plain numbers with no hyperlink (every other offload cell is a HYPERLINK to a Drive file); Certify Sources tab (28 sources) holds no scale ticket for any offload."})
            out[rc][f"offload_{n}"] = entry
    return out

scale_tickets = ticket_pairs()
scale_tickets["_primary_source_opened"] = [
    {"file": t[12], "action": "image_read", "artifact_path": f"tickets/{t[12]}",
     "evidence": f"CAT Scale ticket {t[3]} ({t[13]}): GROSS {t[4]} LB, {t[5]} {t[6]}, scale {t[7]} {t[8]}, tractor {t[9]}, trailer {t[10]}, commodity '{t[11]}'"}
    for t in TICKETS
] + [
    {"file": "Drive folder Scale Tickets/TIMX201060 (id 1as1JEt0ATZ2G3uZ7Lc7CodCMWFpQX6gy)", "action": "csv_exported", "live_source_url": "https://drive.google.com/drive/folders/1as1JEt0ATZ2G3uZ7Lc7CodCMWFpQX6gy",
     "artifact_path": "drive_folder_listing.json", "items_found": ["Offload 1", "Offload 3", "Offload 4"],
     "evidence": "Drive API parentId listing returned subfolders Offload 1, Offload 3, Offload 4; no Offload 2 subfolder and no file for offload 2 anywhere under Scale Tickets/"},
]
scale_tickets["_summary"] = {
    "pairs_read": 7, "tickets_read": 14, "offloads_in_ops_notes": 8, "offloads_without_tickets": ["TIMX201060 offload_2 (Ops row 33: 74,140 / 28,480 lb, no hyperlink, no Drive file, no Certify source)"],
    "rig_mismatches": [],
    "note_formats": "SHPX215046 offloads 3 and 4 are filed as 4 JPG phone photographs of a PDF viewer on a cracked phone screen (all fields legible); the other 10 are CAT Scale PDF exports.",
    "note_dates": "TIMX201060 offloads 1, 3, 4 were weighed 2026-09-03/04 and SHPX215079 offload 1 full weigh is 2026-09-04, i.e. inside the prior removal's Certify period (30 Aug - 04 Sep) but booked in this week's Ops Notes (offload date 2026-09-11) and COBB (completion 2026-09-11); the prior removal INJ-09-2026-W1 carried only GRPX5254 and GPRX5107, so there is no double booking.",
    "note_timx_o1_gross": "TIMX201060 offload 1 full ticket prints GROSS 85,100 LB with trailer axle 50,080 LB; net 55,620 lb = 25,228.79 kg against 42,860-48,540 lb nets on the other six evidenced offloads.",
    "empty_after_full_all_pairs": True,
}

# ---------------- BOLs (12 PDFs, pages 1-3 read as images) ----------------
RAIL_BOLS = [
    # bol, date_p1, railcar, p1_MT, p1_kg, p2_qty_shipped_MT, p2_delivered_kg, p2_tare_kg, p2_full_kg, truck, tanker, weigh_slip_no, slip_net_kg, prod_period, file
    ("2450-R", "2026-07-29", "TIMX201060", 25.60, 25602, 26.06, 26060, 19200, 45260, "2623", "21607", "PC0039357", 26060, "#07-2026", "Documents camion 2450-R.pdf"),
    ("2451-R", "2026-07-29", "TIMX201060", 25.64, 25641, 26.02, 26020, 19600, 45620, "2416", "22095", "PC0039361", 26020, "#07-2026", "Documents Camion 2451-R CHARM PO Q42025.pdf"),
    ("2452-R", "2026-07-30", "TIMX201060", 25.71, 25711, 26.06, 26060, 19270, 45330, "2623", "21607", "PC0039364", 26060, "#07-2026", "Envoi des documents 2452-R.pdf"),
    ("2453-R", "2026-07-30", "SHPX215079", 25.75, 25746, 25.99, 25990, 19440, 45430, "2416", "22095", "PC0039365", 25990, "#0X-2026", "Envoi des documents 2453-R.pdf"),
    ("2454-R", "2026-08-03", "SHPX215079", 25.68, 25678, 25.91, 25910, 19280, 45190, "2114", "22095", "PC0039377", 25910, "#08-2026", "Documents camion 2454-R.pdf"),
    ("2455-R", "2026-08-03", "SHPX215079", 25.73, 25729, 25.97, 25970, 19130, 45100, "2416", "21607", "PC0039384", 25970, "#08-2026", "Document Camion 2455-R.pdf"),
    ("2462-R", "2026-08-05", "SHPX215046", 25.56, 25560, 25.94, 25940, 19340, 45280, "2416", "21607", "PC0039406", 25940, "#08-2026", "Envoi des documents Camion 2462-R.pdf"),
    ("2463-R", "2026-08-06", "SHPX215046", 26.18, 26184, 25.90, 25900, 19590, 45490, "2416", "22095", "PC0039409", 25900, "#08-2026", "Envoi des documents Camion 2463-R.pdf"),
    ("2464-R", "2026-08-06", "SHPX215046", 25.48, 25480, 25.84, 25840, 18980, 44820, "921",  "22095", "PC0039413", 25840, "#08-2026", "Documents camion 2464-R.pdf"),
]
TRUCK_BOLS = [
    # bol, date_p1, p1_MT, p3_qty_shipped_MT, p3_delivered_kg, p3_tare_kg, p3_full_kg, truck, tanker, carrier, prod_period, ops_date, ops_MT, file
    ("2499-T", "2026-08-31", 19.59, 19.71, 19710, 16140, 35850, "33731", "36658", "Tandet Logistics", "#08-2026", "2026-08-31", 19.71, "Billing Documents 2499-T.pdf"),
    ("2503-T", "2026-09-01", 18.95, 19.19, 19190, 16660, 35850, "2214",  "36469", "Tandet Logistics", "#9-2026",  "2026-09-01", 19.19, "Billing Documents 2503-T.pdf"),
    ("2505-T", "2026-09-02", 19.72, 19.67, 19670, 16090, 35760, "2216",  "36677", "Tandet Logistics", "#8-2026",  "2026-09-02", 19.67, "Billing documents 2505-T.pdf"),
]
OPS_RAIL_BOL_MT = {"2450-R": 26.06, "2451-R": 26.02, "2452-R": 26.06, "2453-R": 25.99, "2454-R": 25.91, "2455-R": 25.97, "2462-R": 25.94, "2463-R": 25.90, "2464-R": 25.84}

bols = {
    "rail": {b[0]: {"date_page1": b[1], "railcar_per_ops_notes": b[2], "page1_estimated_MT": b[3], "page1_estimated_kg": b[4],
                    "page2_qty_shipped_MT": b[5], "page2_product_delivered_kg": b[6], "page2_tanker_tare_kg": b[7], "page2_tanker_full_kg": b[8],
                    "truck_id": b[9], "tanker_id": b[10], "carrier": "Transport Baie-Comeau", "aecn_weigh_slip_no": b[11], "aecn_weigh_slip_masse_nette_kg": b[12], "prod_period_printed": b[13], "file": b[14],
                    "ship_to": "CHARM Industrial Inc. /WATCO, Societe du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau, Quebec G4Z 2L6",
                    "from": "BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9",
                    "customer_po": "Q42025", "ops_notes_mass_MT": OPS_RAIL_BOL_MT[b[0]], "matches_ops_notes": OPS_RAIL_BOL_MT[b[0]] == b[5]} for b in RAIL_BOLS},
    "rail_sum_check": {
        "TIMX201060_bol_sum_kg": 26060 + 26020 + 26060, "TIMX201060_ops_total_loaded_kg": 78140,
        "SHPX215079_bol_sum_kg": 25990 + 25910 + 25970, "SHPX215079_ops_total_loaded_kg": 77870,
        "SHPX215046_bol_sum_kg": 25940 + 25900 + 25840, "SHPX215046_ops_total_loaded_kg": 77680,
        "match": True, "calc": "26060 + 26020 = 52080; 52080 + 26060 = 78140; 25990 + 25910 = 51900; 51900 + 25970 = 77870; 25940 + 25900 = 51840; 51840 + 25840 = 77680"},
    "truck": {b[0]: {"date_page1": b[1], "page1_estimated_MT": b[2], "page3_qty_shipped_MT": b[3], "page3_product_delivered_kg": b[4],
                     "page3_tanker_tare_kg": b[5], "page3_tanker_full_kg": b[6], "truck_id": b[7], "tanker_id": b[8], "carrier": b[9], "prod_period_printed": b[10],
                     "ops_notes_date": b[11], "ops_notes_bol_mass_MT": b[12], "file": b[13], "page2": "Charm Purchase Order Q42025 (6,000 MT RFO at $290)",
                     "ship_to": "CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA",
                     "from": "BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9",
                     "customer_po": "Q4-2025", "matches_ops_notes": b[3] == b[12]} for b in TRUCK_BOLS},
    "truck_sum_check": {"ops_notes_sum_bol_kg": 58570, "sum_of_bol_page3_delivered_kg": sum(b[4] for b in TRUCK_BOLS), "certify_bio_oil_mass_AECN_kg": 58570, "match": True, "calc": "19710 + 19190 = 38900; 38900 + 19670 = 58570 kg"},
    "destination_check": {"rail_bols_ship_to_SOPOR_confirmed_on_page1": [b[0] for b in RAIL_BOLS],
                          "truck_bols_ship_to_St_Landry_LA_confirmed_on_page1": [b[0] for b in TRUCK_BOLS],
                          "vaulted_references_found": []},
    "print_oddities": {"2453-R": "page 1 and page 2 print Prod.period / Run # as '#0X-2026' (the sister BOLs print '#07-2026' or '#08-2026')",
                       "2503-T": "Prod.period printed '#9-2026' (September production) while 2499-T and 2505-T print '#08-2026' / '#8-2026'"},
    "_primary_source_opened": [
        {"file": b[14], "action": "pdf_read", "artifact_path": f"bols/{b[14]}", "evidence": f"Pages 1-3 read as images: BOL {b[0]} dated {b[1]}, ship to CHARM/WATCO SOPOR Baie-Comeau, page 2 Qty shipped {b[5]} M.Tons / delivered {b[6]} kg, page 3 weigh slip {b[11]} Masse nette {b[12]} kg"} for b in RAIL_BOLS
    ] + [
        {"file": b[13], "action": "pdf_read", "artifact_path": f"bols/{b[13]}", "evidence": f"Pages 1-3 read as images: BOL {b[0]} dated {b[1]}, ship to CHARM St Landry LA, page 3 Qty shipped {b[3]} M.Tons / delivered {b[4]} kg"} for b in TRUCK_BOLS
    ],
}

# ---------------- Ops Notes ----------------
ops_notes = {
    "file": "INJ-09-2026-W2 Ops Notes (Google Sheet, owner garrett.lutz@; exported to xlsx 2026-09-22 and read with openpyxl WITHOUT data_only so comments were captured, plus a data_only pass for cached values)",
    "sheet_id": "1OEJvgN5KMPKseQrn--RH9QmqDh68zERpf1IMOZN7tvY",
    "live_source_url": OPS_URL,
    "artifact_path": "source_exports/INJ-09-2026-W2_Ops_Notes.xlsx",
    "sheets": ["Summary", "AECN Rail", "AECN Truck", "WODO", "Kerry", "QOWV", "Whole Oil", "QOWV Shipments & EE Allocation", "WODO Shipments & EE Allocation", "Whole Oil Shipments & EE Alloca"],
    "batch_id_B2": "INJ-09-2026-W2", "week_start_B3": "2026-09-05", "week_end_B4": "2026-09-12",
    "_primary_source_opened": [
        {"file": "INJ-09-2026-W2_Ops_Notes.xlsx", "action": "sheet_grid_read", "live_source_url": OPS_URL, "artifact_path": "ops_notes_dump.txt",
         "evidence": "Every non-empty cell of Summary, AECN Rail, AECN Truck dumped with formulas, cached values and cell comments (ops_notes_dump.txt); no cell comments exist on any of the three tabs."}],
    "cell_comments": "none on Summary, AECN Rail or AECN Truck (openpyxl comment scan)",
    "aecn_rail_tab": {
        "constants": {"O3_lbs_per_kg": 2.20462, "O4_kg_per_lb": 0.453592, "O5_sparging": 0.0129, "O6_pH_target": "2.0 - 4.0", "O7_filtration_solids": 0.00196, "O7_hyperlink": FILT_URL, "O8_bol_trips_AECN_SOPOR": 3, "O9_round_trip_opel_basco": 2},
        "railcars_received": {
            "TIMX201060": {"row": 10, "arrival_opelousas": "2026-07-31", "bols": "2450-R, 2451-R, 2452-R", "total_loaded_MT": 78.14, "total_loaded_kg": 78140, "total_offloaded_kg_F": 77800.09984, "loss_kg_G": 339.90016, "prev_claimed_kg": 0, "prior_rp_claimed_kg": 0, "aecn_sopor_mi": 107.5, "rail_mi": 2199, "opel_basco_mi": 42.9, "full_flag_P": "FULL",
                           "notes_M": "New arrival this RP (7.31.2026 load). Loaded 7/29-7/30/2026 at SOPOR (BOLs 2450-R/2451-R/2452-R, 78,140 kg). All 4 offloads logged this week, CAT scale-ticket confirmed (delta 0.00 kg vs COBB on all 4). Prior-RP claimed: 0 kg."},
            "SHPX215079": {"row": 11, "arrival_opelousas": "2026-08-04", "bols": "2453-R, 2454-R, 2455-R", "total_loaded_MT": 77.87, "total_loaded_kg": 77870, "total_offloaded_kg_F": 42410.852, "loss_kg_G": None, "prev_claimed_kg": 0, "prior_rp_claimed_kg": 0, "aecn_sopor_mi": 107.5, "rail_mi": 2199, "opel_basco_mi": 42.9, "full_flag_P": "PARTIAL",
                           "notes_M": "New arrival this RP (8.4.2026 load). Loaded 7/30 and 8/3/2026 at SOPOR (BOLs 2453-R/2454-R/2455-R, 77,870 kg). Offloads 1-2 logged this week, CAT scale-ticket confirmed (delta 0.00 kg vs COBB on both). Prior-RP claimed: 0 kg. Note: this physical railcar had an earlier, separate 6.18.2026 loading/offload cycle already closed in a prior RP -- not part of this arrival mass balance."},
            "SHPX215046": {"row": 12, "arrival_opelousas": "2026-08-07", "bols": "2462-R, 2463-R, 2464-R", "total_loaded_MT": 77.68, "total_loaded_kg": 77680, "total_offloaded_kg_F": 35652.3312, "loss_kg_G": None, "prev_claimed_kg": 0, "prior_rp_claimed_kg": 0, "aecn_sopor_mi": 107.5, "rail_mi": 2199, "opel_basco_mi": 42.9, "full_flag_P": "PARTIAL",
                           "notes_M": "Loaded 8/5-8/6/2026 at SOPOR (BOLs 2462-R/2463-R/2464-R, 77,680 kg). COBB contains ONLY offload_3 (20,810.80 kg) and offload_4 (14,821.22 kg) for this arrival -- offload_1 and offload_2 do not exist in COBB; status pending confirmation, not assumed lost. LD3 only candidate CAT ticket (1124426250545, 74,320 lb, 9-07-26) is confirmed mislabeled (printed SHPX215046OFFLOAD3, actually belongs to another car per Garrett); its next-best mass-fit alternative is itself a ticket labeled GPRX5107 (a different, W1 railcar) -- not treated as genuine. LD4 has no resolvable ticket after a wide Gmail harvest. Both LD3 and LD4 Full/Empty left blank pending real tickets. 45.9 pct of loaded mass currently documented (35,632.02 / 77,680 kg) -- Loss suppressed by design (>=95pct closure guard) until resolved. Prior-RP claimed: 0 kg.",
                           "notes_M_contradictions": "Row 28 (offload 3) IS populated with ticket 1124426250545 (74,320 lb), the very ticket M12 calls 'confirmed mislabeled ... not treated as genuine', and row 29 (offload 4) is populated with 61,980 / 29,260 lb although M12 says 'LD4 has no resolvable ticket' and 'Both LD3 and LD4 Full/Empty left blank'. M12's 35,632.02 kg documented figure also differs from F12 35,652.3312 kg. COBB now holds offload_1 (21,055.74064 kg) and offload_2 (20,992.23776 kg) under INJ-09-2026-W3_bio_oil (rows 850-851), so 'do not exist in COBB' is also out of date."}},
        "origins_ledger": [{"row": r, "date": d, "bol": b, "railcar": rc, "MT": mt, "kg": kg} for r, d, b, rc, mt, kg in [
            (17, "2026-07-29", "2450-R", "TIMX201060", 26.06, 26060), (18, "2026-07-29", "2451-R", "TIMX201060", 26.02, 26020), (19, "2026-07-30", "2452-R", "TIMX201060", 26.06, 26060),
            (20, "2026-07-30", "2453-R", "SHPX215079", 25.99, 25990), (21, "2026-08-03", "2454-R", "SHPX215079", 25.91, 25910), (22, "2026-08-03", "2455-R", "SHPX215079", 25.97, 25970),
            (23, "2026-08-05", "2462-R", "SHPX215046", 25.94, 25940), (24, "2026-08-06", "2463-R", "SHPX215046", 25.90, 25900), (25, "2026-08-06", "2464-R", "SHPX215046", 25.84, 25840)]],
        "offload_table": [{"row": o[0], "id": o[1], "railcar": o[2], "date_A": "2026-09-11", "full_lb_D": o[3], "empty_lb_E": o[4], "net_kg_F": o[5], "pH_G": None, "sparging_kg_H": o[6], "filtration_kg_I": o[7], "uncertainty_adj_kg_J": o[8], "MOBI_kg_K": o[9], "alloc_aecn_sopor_mi_L": o[10], "rail_mi_M": o[11], "opel_basco_mi_N": o[12], "D_hyperlinked": o[13], "E_hyperlinked": o[14]} for o in OPS_OFFLOADS],
        "offload_table_formulas": {"F": "(D-E)*$O$4", "H": "(F-J)*$O$5", "I": "(F-J)*(1-$O$5)*$O$7", "K": "F-H-I-J", "L": "(F-J)/E_railcar*J_railcar*$O$8", "M": "array formula: 2199 (full leg) on the first offload row of a FULL railcar, mass-fraction allocation (F/E_railcar x 2199) on PARTIAL railcars", "N": "L_railcar*$O$9 (42.9 x 2 = 85.8 per offload)"},
        "distance_rollup_row36": {"L36_alloc_aecn_sopor_mi": 644.7583867, "M36_rail_mi": 4405.917936, "N36_opel_basco_mi": 686.4},
        "rail_M_column_note": "M32 = 2199 for TIMX201060 (FULL) while its offloaded fraction is 77800.09984 / 78140 = 0.99565; the four PARTIAL-railcar rows carry mass-fraction allocations (589.1214123 + 420.1406411 + 615.6079326 + 582.0479496 = 2206.917936). M36 = 2199 + 2206.917936 = 4405.917936 mi.",
        "rollup_row44": {"A44_sum_deliveries_raw_kg": 155863.283, "A44_formula": "=SUM(F28:F40)", "B44_sum_uncertainty_adj_kg": 0, "C44_mass_used_post_adj_kg": 155863.283, "D44_sparging_kg": 2010.636351, "E44_filtration_kg": 301.5511875, "F44_MOBI_kg": 153551.0955, "G44_pH": None, "H44_C_content": 0.404, "M44_origins": "2450-R, 2451-R, 2452-R, 2453-R, 2454-R, 2455-R, 2462-R, 2463-R, 2464-R"},
        "rollup_note": "A44 = SUM(F28:F40) = sum of the eight scale-ticket nets (155,863.283 kg). Mass Used is on the scale-ticket basis this week (the prior week's A44 summed the loading BOLs instead). F44 153,551.0955 = sum of K28:K35.",
    },
    "aecn_truck_tab": {
        "constants": {"L3": 2.20462, "L4": 0.453592, "L5_sparging": 0.0129, "L6_pH_target": "2.0 - 4.0", "L7_filtration": 0.00196},
        "methodology_header_A26": "SECTION 2 - ROLLUP  (Mass Used = Σ BOL kg; scale tickets no longer required for direct trucks per 2026-05-26)",
        "deliveries": [{"row": 10 + i, "date": b[11], "bol": b[0], "bol_MT": b[12], "bol_kg": int(round(b[12] * 1000)), "scale_full_lb": None, "scale_empty_lb": None, "cargo_kg_G": None, "pH_H": None, "sparging_J": [254.259, 247.551, 253.743][i], "filtration_K": [38.13325236, 37.12720004, 38.05586372][i], "MOBI_L": [19417.60775, 18905.3218, 19378.20114][i], "EE_miles_N": 2197} for i, b in enumerate(TRUCK_BOLS)],
        "N25_sum_EE_miles": 6591,
        "rollup_row28": {"A28_sum_bol_kg": 58570, "B28_sum_cargo_kg": 0, "C28_mass_used_kg": 58570, "D28_sparging_kg": 755.553, "E28_filtration_kg": 113.3163161, "F28_uncertainty_adj_kg": 0.0, "G28_MOBI_kg": 57701.13068, "H28_pH": None, "K28_origins": "2499-T, 2503-T, 2505-T"},
        "pH_blank_all_rows": True,
    },
    "summary_tab": {"A2_batch": "INJ-09-2026-W2", "B3_week_start": "2026-09-05", "B4_week_end": "2026-09-12",
                    "row8_aecn_rail": {"B8": 155863.283, "C8": 0, "D8": 155863.283, "E8": 2010.636351, "F8": 301.5511875, "G8": 153551.0955, "H8": 644.7583867, "I8": 4405.917936, "J8": 686.4},
                    "row9_aecn_truck": {"B9": 58570, "D9": 58570, "E9": 755.553, "F9": 113.3163161, "G9": 57701.13068},
                    "row18_aecn": {"B18_MOBI_kg": 211252.2262, "C18_composite": "SR26-05494.002", "D18_date_composited": "2026-09-12", "E18_C_pct": 0.404, "F18_link": "COA SR26-05494.002 -> https://drive.google.com/file/d/1E1uy1rtPtWOVK39JiIoe8RyE38Ob0NQo/view", "G18_C_uncertainty": 0.001616, "H18_testing_uncertainty": 0.004},
                    "other_oil_rows": "Kerry (B11 18,007.60 kg), QOWV (B12 38,830.4 kg) and Whole Oil (B13 3,457 kg) are separate removals, not part of rmv_1M2RKR58N1S0F02M"},
}

# ---------------- VVB guidance ----------------
vvb_guidance = {
    "search_performed": [
        "Drive search title contains 'VVB Guidance' (first page of results) -- returned 'VVB Guidance September 1 - September 30' (id 1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc, created 2026-09-21T15:13Z, modified 2026-09-21T15:32Z, owner garrett.lutz@) and 'VVB Guidance August 1 - August 31' (1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y)",
    ],
    "september_2026_guidance_doc_exists": True,
    "doc_id": "1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc",
    "live_source_url": VVB_URL,
    "owner": "garrett.lutz@charmindustrial.com",
    "artifact_path": "VVB_Guidance_September_1-30_fetched_2026-09-22.txt",
    "_primary_source_opened": [{"file": "VVB Guidance September 1 - September 30", "action": "pdf_read", "live_source_url": VVB_URL, "artifact_path": "VVB_Guidance_September_1-30_fetched_2026-09-22.txt", "evidence": "Exported as text via the Drive connector 2026-09-22 and read end to end (one section, 5 paragraphs)."},
                               {"file": "VVB Guidance August 1 - August 31 (prior period)", "action": "pdf_read", "live_source_url": VVB_AUG_URL, "artifact_path": "../batch-INJ-09-2026-W1-AECN/VVB_Guidance_August_1-31_fetched_2026-09-17.txt", "evidence": "Standard-tare table and railcar-loss band re-read from the text fetched 2026-09-17 (file 1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y, unchanged modified time 2026-09-11T01:39Z)."}],
    "sections": ["AECN Rail — Basis for Loaded Mass (Week 3, INJ-09-2026-W3)"],
    "scope_quote": "The basis described here applies to Week 3 of this Reporting Period, INJ-09-2026-W3, covering 11 – 18 September 2026, and to that week alone. For all other weeks in this Reporting Period, the mass loaded at origin is taken from the metric-tons figure stated on the Bill of Lading.",
    "offloaded_mass_quote": "Mass offloaded at the injection site is measured independently, by certified truck scale, as the difference between full and empty weights for each offload. Sparging and filtration losses are deducted from the offloaded mass to give the Mass of Bio-Oil Injected, which is subtracted directly from the railcar's loaded mass.",
    "multi_week_quote": "Where a railcar is offloaded across more than one reporting week, the loaded mass is recorded once, in the week the railcar's first offload occurs, and subsequent weeks draw against the same shipment.",
    "w2_coverage_check": "The document names no INJ-09-2026-W2 offload, railcar TIMX201060 / SHPX215079 / SHPX215046 or truck BOL 2499-T / 2503-T / 2505-T, and contains no standard-tare, missing-ticket or mislabeled-ticket statement. It offers no coverage for the TIMX201060 offload 2 ticket gap or the SHPX215046 M12 note.",
    "august_standard_tare_table": {"KL192": 29510, "KL188": 29307, "KL720": 29645, "KL510": 29478},
    "august_standard_tare_trigger_quote": "substitute the standard empty weight for the trailer recorded on the Full ticket when either (a) the empty scale ticket is missing, or (b) the empty ticket's tractor and/or trailer do not match the Full ticket. Substituted values are annotated in the ops-notes Empty Scale Ticket cell.",
    "august_railcar_loss_band_quote": "Every other railcar offloaded in the same week falls between -101.75 kg and +480.59 kg.",
    "spill_check": "Neither guidance document discloses a spill involving TIMX201060, SHPX215079 or SHPX215046.",
}

# ---------------- lab ----------------
lab_results = {
    "file": "SR26-05494 W2 QOWV AECN COA.pdf (Drive batch-folder root, id 1E1uy1rtPtWOVK39JiIoe8RyE38Ob0NQo; also Certify source #1). Two-page SGS report: page 1 = SR26-05494.001 (QOWV, Carbon 8.3 %), page 2 = SR26-05494.002 (AECN, this removal).",
    "artifact_path": "SR26-05494_W2_QOWV_AECN_COA.pdf",
    "download_path": "Certify Sources tab -> source detail view -> signed storage.googleapis.com embed URL (src_1M30QPPDW1S0ZB4E), md5 76d0657f0d969e4ec2397cf71ed83434",
    "certificate_number": "SR26-05494.002", "sgs_order_no": "5494492", "client_id": "9-2026-W2-AECN", "location_printed": "FORT LUPTON, CO", "product_description": "Oil - AECN",
    "sampled": "2026-09-12 07:00", "received": "2026-09-16 09:50", "analysed": "2026-09-17 04:58 - 11:02", "report_date": "2026-09-17",
    "carbon_pct": 40.4, "carbon_method": "ASTM D5291 (Method C)", "carbon_flag_hash": "# - Result is outside of test method limits and/or analytical range used in method precision study",
    "hydrogen_pct": 7.0, "hydrogen_flag_hash": True, "nitrogen_pct": "<0.75",
    "kinematic_viscosity_cSt_40C": 14.69, "acid_number_mgKOHg": 61, "density_g_cm3_at_15C": 1.208,
    "location_note": "Page 2 prints LOCATION 'FORT LUPTON, CO' for the AECN composite; AECN oil is offloaded and sampled at Basco, Louisiana (the prior week's certificate SR26-05371.001 printed 'BASCO LOUISIANA'). Page 1 (QOWV, Fort Lupton product) prints the same location.",
    "aecn_stats": {"source_file": "MRV_AECN_Analysis.xlsx (Drive id 1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi, downloaded and read with openpyxl this session)", "artifact_path": "source_exports/MRV_AECN_Analysis.xlsx", "live_source_url": "https://drive.google.com/file/d/1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi/view",
                   "tab": "Summary Statistics", "filter_A2": "Filtered to Function = MRV, Offtake = AECN (439 samples)",
                   "carbon_mean_B5": 39.420350877193, "carbon_sd_B6": 6.09332409018271, "carbon_n_B7": 285,
                   "hydrogen_mean_C5": 6.87438596491228, "hydrogen_sd_C6": 0.562848694875852, "nitrogen_n_D7": 9,
                   "two_sd_low": 27.2337, "two_sd_high": 51.607, "batch_carbon_within_2sd": True, "batch_carbon_z": round((40.4 - 39.420350877193) / 6.09332409018271, 3)},
    "formation_fluid": {"file": "Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf (Waypoint Analytical report 24-200-0020, Lab No 98021, page 5, read this session)", "artifact_path": "../batch-INJ-09-2026-W1-AECN/Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf", "specific_gravity_g_mL": 1.01, "method": "ASTM D-1298-85", "sampled": "7/17/2024 8:00"},
    "prior_week_certificate": {"file": "SR26-05371.001 (INJ-09-2026-W1 AECN, values from the prior week's build_source_reads.py read this session)", "carbon_pct": 50.4, "kinematic_viscosity_cSt_40C": 269.4, "density": 1.219, "location": "BASCO LOUISIANA"},
    "_primary_source_opened": [
        {"file": "SR26-05494_W2_QOWV_AECN_COA.pdf", "action": "pdf_read", "artifact_path": "SR26-05494_W2_QOWV_AECN_COA.pdf", "evidence": "Pages 1-2 read: page 2 CLIENT ID 9-2026-W2-AECN, LOCATION FORT LUPTON, CO, SAMPLED 12-Sep-2026 07:00, Carbon 40.4 % (m/m) #, Hydrogen 7.0 #, Nitrogen <0.75, viscosity 14.69 cSt, acid number 61, density 1.208 g/cm3"},
        {"file": "MRV_AECN_Analysis.xlsx", "action": "sheet_grid_read", "live_source_url": "https://drive.google.com/file/d/1bDw821dD2Dq-qz7amEql5qBZBSGPlnEi/view", "artifact_path": "source_exports/MRV_AECN_Analysis.xlsx", "evidence": "Summary Statistics B5=39.420350877193, B6=6.09332409018271, B7=285"},
        {"file": "Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf", "action": "pdf_read", "artifact_path": "../batch-INJ-09-2026-W1-AECN/Formation_Fluid_Characterization_Basco6_SWD_MRV.pdf", "evidence": "Page 5: Specific Gravity 1.01 g/mL, ASTM D-1298-85, sampled 7/17/2024"}],
}

# ---------------- filtration constant source ----------------
filtration_constant_source = {
    "file": "AECN COA Solids Content Dataset (May 2025 - May 2026) (Google Sheet 1XhIwfVwGTl2T04CAlA-qee03gfqxNWwBmSCAeiSW548, hyperlinked from Ops O7; exported as CSV 2026-09-22)",
    "live_source_url": FILT_URL, "artifact_path": "source_exports/AECN_COA_Solids_Content_Dataset_summary_2026-09-22.csv",
    "summary_tab_rows": {"Mean (per unique COA)": "0.195%", "Mean (per load)": "0.196%", "Min": "0.120%", "Max": "0.300%", "Std dev (per load, population)": "0.039%", "Recommended value for filtration loss": "0.196% -- per-load mean; best represents what is actually delivered", "Loads in window": 136, "Unique COA PDFs": 71},
    "ops_constant": 0.00196, "prior_week_constant": 0.00196,
    "_primary_source_opened": [{"file": "AECN COA Solids Content Dataset summary tab", "action": "csv_exported", "live_source_url": FILT_URL, "artifact_path": "source_exports/AECN_COA_Solids_Content_Dataset_summary_2026-09-22.csv", "evidence": "CSV export read: 'Recommended value for filtration loss,0.196%'"}],
}

# ---------------- Certify (tabs read this session; component modals in patch script) ----------------
SOURCES = [
    (1, "SR26-05494 W2 QOWV AECN COA.pdf", "Carbon Content of Bio-oil Injected (per injection)", "Private"),
    (2, "INJ-09-2026-W2 Ops Notes.xlsx", "Mass of Injectant (per injection) + 1 more", "Private"),
    (3, "BOL_2463-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (4, "BOL_2464-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (5, "BOL_2462-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (6, "Aug-08-2026-distance-route_map.png", "Allocated Distance AECN to Sopor Quebec (truck) + 1 more", "Public"),
    (7, "BOL_2455-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (8, "BOL_2454-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (9, "BOL_2453-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (10, "Aug-05-2026-distance-route_map.png", "Allocated Distance AECN to Sopor Quebec (truck) + 1 more", "Public"),
    (11, "BOL_2452-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (12, "BOL_2451-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (13, "BOL_2450-R.pdf", "Allocated Distance AECN to Sopor Quebec (truck) + 2 more", "Public"),
    (14, "Aug-01-2026-distance-route_map.png", "Allocated Distance AECN to Sopor Quebec (truck) + 1 more", "Public"),
    (15, "BOL_2505-T.pdf", "Bio-Oil Mass - AECN", "Public"),
    (16, "BOL_2503-T.pdf", "Bio-Oil Mass - AECN", "Public"),
    (17, "BOL_2499-T.pdf", "Bio-Oil Mass - AECN", "Public"),
    (18, "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "BCUs Applied - Bio-Oil Transport Process [Certify input]", "Public"),
    (19, "FH 2026 LCA w Stack Emissions.xlsx", "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) + 1 more", "Public"),
    (20, "Standard Emission Factors + Calculations (8).xlsx", "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "Public"),
    (21, "Standard Emission Factors + Calculations (8).xlsx", "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "Public"),
    (22, "AECN Embodied Emissions Calc Sheet (1).pdf", "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail) + 1 more", "Public"),
    (23, "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf", "Emissions Factor - Vehicle Embodied Emissions -- Railcar", "Public"),
    (24, "Opelousas Railyard to Basco.png", "Allocated Distance Opelousas to B6 (truck) + 1 more", "Public"),
    (25, "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf", "Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "Public"),
    (26, "AECN to SOPOR (Baie Comeau) (2).png", "Allocated Distance AECN to Sopor Quebec (truck) + 1 more", "Public"),
    (27, "image (44).png", "Allocated Distance Sopor Quebec to Opelousas (rail) + 1 more", "Public"),
    (28, "AECN to Basco.png", "Aggregate Distance Transported AECN to Basco + 1 more", "Public"),
]

DATAPOINTS = [  # name, value shown, method, first source, extra sources count
    ("Allocated Distance AECN to Sopor Quebec (truck)", "645 mi", "Derived", "AECN to SOPOR (Baie Comeau) (2).png", 12),
    ("Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "0.1476 kgCO2e/km", "Derived", "Standard Emission Factors + Calculations (8).xlsx", 0),
    ("Allocated Distance Sopor Quebec to Opelousas (rail)", "4,396 mi", "Derived", "Aug-05-2026-distance-route_map.png", 12),
    ("Emissions Factor - Vehicle Embodied Emissions -- Railcar", "0.0193 kgCO2e/km", "Derived", "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf", 0),
    ("Allocated Distance Opelousas to B6 (truck)", "686 mi", "Reported", "Opelousas Railyard to Basco.png", 0),
    ("Aggregate Distance Transported AECN to Basco", "6,591 mi", "Reported", "AECN to Basco.png", 0),
    ("Bio-Oil Mass - AECN via Rail", "155.863 t", "Reported", "BOL_2462-R.pdf", 8),
    ("Distance from Opelousas to B6 (truck)", "43 mi", "Derived", "Opelousas Railyard to Basco.png", 0),
    ("Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "0.07 kgCO2e/(km*t)", "Derived", "Standard Emission Factors + Calculations (8).xlsx", 0),
    ("Distance from Sopor Quebec to Opelousas (rail)", "2,199 mi", "Derived", "image (44).png", 0),
    ("Emission Factors - Rail Transport Fuel Use (Well to Wheel)", "0.02 kgCO2e/(km*t)", "Derived", "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf", 0),
    ("Distance from AECN to Sopor Quebec (truck)", "107 mi", "Derived", "AECN to SOPOR (Baie Comeau) (2).png", 0),
    ("Bio-Oil Mass - AECN", "58.570 t", "Reported", "BOL_2503-T.pdf", 2),
    ("Distance from AECN to Basco", "2,197 mi", "Derived", "AECN to Basco.png", 0),
    ("Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)", "0.02 tCO2e/t", "Derived", "AECN Embodied Emissions Calc Sheet (1).pdf", 0),
    ("Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)", "0.14 tCO2e/t", "Derived", "FH 2026 LCA w Stack Emissions.xlsx", 0),
    ("Carbon Intensity - AECN Pyrolysis Embodied Emissions (direct to B6)", "0.02 tCO2e/t", "Reported", "AECN Embodied Emissions Calc Sheet (1).pdf", 0),
    ("Carbon Intensity - AECN Pyrolysis Process Emissions (direct to B6)", "0.14 tCO2e/t", "Derived", "FH 2026 LCA w Stack Emissions.xlsx", 0),
    ("Mass of Injectant (per injection)", "211.252 t", "Reported", "INJ-09-2026-W2 Ops Notes.xlsx", 0),
    ("Carbon Content of Bio-oil Injected (per injection)", "40.40 %", "Derived", "SR26-05494 W2 QOWV AECN COA.pdf", 1),
    ("BCUs Applied - Bio-Oil Transport Process [Certify input]", "26.187 tCO2e", "Reported", "Charm-RetirementCertificate-RD-EACs-20251218.pdf", 0),
]

COMPONENTS = {  # Components tab, 14 components, read 2026-09-22
    "Mitigated_total_t": 339.150,
    "BCUs - Applied to Bio-Oil Transport Process Emissions": 26.187,
    "Injection sequestration": 312.963,
    "Emitted_total_t": 62.226,
    "AECN pyrolysis (from rail loads) - embodied emissions": 3.298,
    "AECN pyrolysis (from rail loads) - process emissions": 21.372,
    "AECN pyrolysis (from truck loads) - embodied emissions": 1.239,
    "AECN pyrolysis (from truck loads) - process emissions": 8.031,
    "AECN to LA Tanker Truck Transport Embodied Emissions - AECN": 1.566,
    "AECN to LA Tanker Truck Transport Process Emissions - AECN": 14.708,
    "AECN to SOPOR Tanker Truck Transport Embodied Emissions": 0.153,
    "AECN to SOPOR Tanker Truck Transport Process Emissions": 1.915,
    "Opelousas to Basco - Tanker Truck Transport Process Emissions": 0.764,
    "Opelousas to Basco Tanker Truck Transport Embodied Emissions": 0.163,
    "SOPOR to Opelousas Rail Transport Embodied Emissions": 0.137,
    "SOPOR to Opelousas Rail Transport Process Emissions": 8.880,
    "Pyrolysis_subtotal_t": 33.940, "Bio-oil_transport_activities_subtotal_t": 28.286,
    "injection_side_activity_components": [],
}

attachment_map = {}
for _, name, dp, _vis in SOURCES:
    attachment_map.setdefault(dp.split(" + ")[0], []).append(name)
# The Ops Notes' "+ 1 more" and the COA's "+ 1 more" are each other's datapoint (Carbon Content shows 2 sources in the
# Injection sequestration detail view: the COA and the Ops Notes; Mass of Injectant shows 1 source: the Ops Notes).
attachment_map["Carbon Content of Bio-oil Injected (per injection)"].append("INJ-09-2026-W2 Ops Notes.xlsx")

ops_notes_linked = ["Mass of Injectant (per injection)", "Carbon Content of Bio-oil Injected (per injection)"]
ops_notes_not_linked = ["Bio-Oil Mass - AECN via Rail (9 BOLs only)", "Bio-Oil Mass - AECN (3 BOLs only)", "Allocated Distance AECN to Sopor Quebec (truck) (13 sources: 9 BOLs, 3 dated route maps, AECN to SOPOR png)", "Allocated Distance Sopor Quebec to Opelousas (rail) (13 sources: 9 BOLs, 3 dated route maps, image (44).png)", "Allocated Distance Opelousas to B6 (truck) (Opelousas Railyard to Basco.png only)", "Aggregate Distance Transported AECN to Basco (AECN to Basco.png only)"]

certify = {
    "removal_id": "rmv_1M2RKR58N1S0F02M", "url": CERTIFY_URL, "project": "Charm Bio-oil Geologic Storage (prj_1HZSSWBQM1S08H83)",
    "header": {"type": "Removal", "net_tCO2e_displayed": 275.19, "period": "05 Sep 2026 to 11 Sep 2026"},
    "components_tab": COMPONENTS,
    "calculation_view": {"net_co2e_removed_t": 275.193, "sequestrations_t": 312.963, "adjustments_tCO2e": 26.187, "activities_tCO2e": 62.227, "uncertainty_discount_t": 1.730,
                         "recalc": "312.963 + 26.187 - 62.227 - 1.730 = 275.193", "components_tab_emitted_total_t": 62.226, "cross_tab_rounding_gap_t": 0.001},
    "datapoints_count": 21,
    "datapoints": [{"name": n, "value": v, "method": m, "first_source_shown": s, "additional_sources": k} for n, v, m, s, k in DATAPOINTS],
    "sources_tab_total": 28,
    "sources": [{"n": n, "filename": f, "datapoints": dp, "visibility": vis} for n, f, dp, vis in SOURCES],
    "attachment_map": attachment_map,
    "ops_notes_source_linked_datapoints": {"linked": ops_notes_linked, "not_linked": ops_notes_not_linked},
    "scale_tickets_in_sources": [],
    "lca_supporting_files_in_sources": {"present": ["FH 2026 LCA w Stack Emissions.xlsx", "AECN Embodied Emissions Calc Sheet (1).pdf"], "absent": ["Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jun2026.xlsx", "Supporting GHG data 30Jun2026 S.xlsx"], "prior_week_had_all_four": True},
    "generic_filenames": ["image (44).png (a screenshot of the Watco 'total milage for this move was 2199' email; the content is the rail-distance evidence)"],
    "_primary_source_opened": [
        {"file": "Certify Components tab", "action": "modal_opened", "live_source_url": CERTIFY_URL, "artifact_path": "certify_ghg_entry_page.yml", "evidence": "14 components enumerated with tCO2e values; header 275.19 tCO2e, 05 Sep 2026 to 11 Sep 2026"},
        {"file": "Certify Sources tab", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=sources", "artifact_path": "certify_sources_tab.yml", "evidence": "heading 'Sources (28)'; all 28 filenames + linked datapoints enumerated; no scale ticket among them", "items_found": [f for _, f, _, _ in SOURCES]},
        {"file": "Certify Calculation view", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=calculation-view", "artifact_path": "certify_calculation_view.yml", "evidence": "Net 275.193 t = 312.963 + 26.187 - 62.227 - 1.730"},
        {"file": "Certify Datapoints tab", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=data-points", "artifact_path": "certify_datapoints_tab.yml", "evidence": "21 datapoints with values and first-listed source"},
        {"file": "Certify source detail views: COA, AECN to SOPOR (Baie Comeau) (2).png, image (44).png, Opelousas Railyard to Basco.png, AECN to Basco.png", "action": "modal_opened", "live_source_url": CERTIFY_URL + "?tab=sources", "artifact_path": "certify_source_coa_dialog.yml", "evidence": "Each opened; the signed storage URL captured and the file downloaded (COA md5 76d0657f0d969e4ec2397cf71ed83434; four route images saved under screenshots/)"},
    ],
}

route_evidence = {
    "AECN_to_SOPOR_png": {"file": "AECN to SOPOR (Baie Comeau) (2).png (Certify source #26)", "artifact_path": "screenshots/AECN_to_SOPOR_Baie_Comeau_2.png", "content": "Google Maps: 175 Bd du Portage des Mousses, Port-Cartier -> Societe du port ferroviaire de Baie-Comeau, via QC-138 O, 1 hr 54 min, 173 km", "km": 173, "mi_equiv": round(173 / 1.609344, 2)},
    "image_44_png": {"file": "image (44).png (Certify source #27)", "artifact_path": "screenshots/image_44.png", "content": "Gmail screenshot: Matt P. Bergeland, Rail Logistics Specialist, Watco, Fort Worth TX: 'Hi Antoinette, The total milage for this move was 2199.'", "mi": 2199},
    "Opelousas_Railyard_to_Basco_png": {"file": "Opelousas Railyard to Basco.png (Certify source #24)", "artifact_path": "screenshots/Opelousas_Railyard_to_Basco.png", "content": "Google Maps: 4687 LA-115, St Landry, LA 71367 -> Acadiana Railway, 1224 Cortez St, Opelousas; via I-49 S 44 min 42.9 miles (alternatives 42.9 and 40.9 miles)", "mi": 42.9},
    "AECN_to_Basco_png": {"file": "AECN to Basco.png (Certify source #28)", "artifact_path": "screenshots/AECN_to_Basco.png", "content": "Google Maps: 175 Bd du Portage des Mousses, Port-Cartier -> 4687 LA-115, St Landry, LA 71367; via ON-401 W 35 hr 2,197 miles (alternatives 2,193 miles)", "mi": 2197},
    "_primary_source_opened": [
        {"file": "AECN to SOPOR (Baie Comeau) (2).png", "action": "image_read", "artifact_path": "screenshots/AECN_to_SOPOR_Baie_Comeau_2.png", "evidence": "173 km via QC-138 O"},
        {"file": "image (44).png", "action": "image_read", "artifact_path": "screenshots/image_44.png", "evidence": "Watco email: total milage 2199"},
        {"file": "Opelousas Railyard to Basco.png", "action": "image_read", "artifact_path": "screenshots/Opelousas_Railyard_to_Basco.png", "evidence": "42.9 miles via I-49 S"},
        {"file": "AECN to Basco.png", "action": "image_read", "artifact_path": "screenshots/AECN_to_Basco.png", "evidence": "2,197 miles via ON-401 W"},
    ],
}

drive_folder = {
    "folder_id": "1Oz-oUtmLMxrMQe7cfyzcLEE5ZUg8qzRh", "live_source_url": DRIVE_URL,
    "root_items": ["INJ-09-2026-W2 Ops Notes (Google Sheet, modified 2026-09-21T20:17Z)", "Scale Tickets/", "SR26-05494 W2 QOWV AECN COA.pdf (in the root, no Testing/ subfolder)", "Kerry Oil/ (2 Kerry scale-ticket JPGs: Sept_W2_Full/Empty_Scale_Ticket_Kerry.jpg -- a separate Kerry removal, out of scope)"],
    "testing_subfolder_present": False,
    "scale_tickets_subfolders": {"SHPX215079": ["Offload 1", "Offload 2"], "TIMX201060": ["Offload 1", "Offload 3", "Offload 4"], "SHPX215046": ["Offload 3", "Offload 4"]},
    "scale_ticket_files": [t[12] for t in TICKETS],
    "bols_in_drive_folder": "none -- the 12 BOLs live outside the batch folder and are hyperlinked from the Ops Notes (all 12 downloaded via those links) and uploaded to Certify Sources as BOL_XXXX-R/T.pdf",
    "_primary_source_opened": [{"file": "Drive folder 1Oz-oUtmLMxrMQe7cfyzcLEE5ZUg8qzRh and subfolders", "action": "csv_exported", "live_source_url": DRIVE_URL, "artifact_path": "drive_folder_listing.json", "evidence": "Drive API parentId listings of root, Scale Tickets, Kerry Oil, the three railcar folders and all 7 Offload subfolders", "items_found": ["INJ-09-2026-W2 Ops Notes", "Scale Tickets", "SR26-05494 W2 QOWV AECN COA.pdf", "Kerry Oil"]}],
}

log = {
    "_schema_version": "1.0",
    "batch_id": "INJ-09-2026-W2",
    "oil_type": "AECN",
    "delivery_mode": "rail + direct truck (combined weekly removal)",
    "injection_site": "Basco 6 LA",
    "reporting_period": "Sep 2026 (Certify entry period 05 Sep 2026 to 11 Sep 2026; Ops week 2026-09-05 to 2026-09-12)",
    "completion_date": "2026-09-11",
    "qa_session_T0_utc": "2026-09-22T16:21:38Z",
    "certify_removal_url": CERTIFY_URL,
    "drive_folder_url": DRIVE_URL,
    "drive_folder": drive_folder,
    "vvb_guidance": vvb_guidance,
    "lab_results": lab_results,
    "filtration_constant_source": filtration_constant_source,
    "ops_notes": ops_notes,
    "scale_tickets": scale_tickets,
    "bols": bols,
    "route_evidence": route_evidence,
    "certify": certify,
    "certify_sources_tab_total": 28,
    "certify_sources_enumeration": [f for _, f, _, _ in SOURCES],
    "rp_status": {"september_2026_rp_open": True, "bcu_quant_sheet": "not yet produced (RP open)", "ghg_statement": "not yet produced (RP open)"},
    "rail_uncertainty_precondition": {"TIMX201060": {"full": True, "n_offloads": 4, "n_bols": 3, "conservative": True}, "SHPX215079": {"full": False, "n_offloads_this_week": 2, "n_bols": 3, "check": "deferred to the railcar's final week"}, "SHPX215046": {"full": False, "n_offloads_this_week": 2, "n_offloads_booked_w3_in_cobb": 2, "n_bols": 3, "check": "deferred to INJ-09-2026-W3 (offloads 1-2 booked there)"}},
}

if __name__ == "__main__":
    existing = {}
    if OUT.exists():
        existing = json.loads(OUT.read_text())
    for k in ("cobb", "certify_components", "standard_efs", "_derived_values"):
        if k in existing:
            log[k] = existing[k]
    OUT.write_text(json.dumps(log, indent=2, default=str))
    print("wrote", OUT, "keys:", list(log.keys()))
