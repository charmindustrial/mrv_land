#!/usr/bin/env python3
"""Builds batch_INJ-09-2026-W4-KERRY_source_reads.json from the primary sources saved in this folder.

Spreadsheet values are read from the downloaded files with openpyxl, so the log carries what the
files say rather than a transcription. Image / PDF / Certify values were read in this session and are
written here verbatim from those reads (artifacts in screenshots/ and source_exports/, Certify modal
text in certify_*.txt).
"""
import hashlib, json, warnings
from pathlib import Path
import openpyxl

warnings.filterwarnings("ignore")
B = Path(__file__).resolve().parent
SX = B / "source_exports"
XC = SX / "w3_kerry_cross_check"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cell(wb, tab, ref):
    return wb[tab][ref].value


DRIVE = "https://drive.google.com/file/d/{}/view"
SHEET = "https://docs.google.com/spreadsheets/d/{}/edit"
DOC = "https://docs.google.com/document/d/{}/edit"
REMOVAL_URL = ("https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/"
               "ghg-entry/rmv_1M3T2J3V51S0NCHH/edit")

# ---------------------------------------------------------------- Ops Notes (live export 18:28Z)
ON = SX / "INJ-09-2026-W4_Ops_Notes_live_20261006T1828Z.xlsx"
onf = openpyxl.load_workbook(ON)
onv = openpyxl.load_workbook(ON, data_only=True)
k = "Kerry"
kerry_row = {
    "A10_date": str(cell(onv, k, "A10"))[:10],
    "B10_uid": cell(onv, k, "B10"),
    "C10_full_ticket_lb": cell(onv, k, "C10"),
    "C10_formula": cell(onf, k, "C10"),
    "D10_empty_ticket_lb": cell(onv, k, "D10"),
    "D10_formula": cell(onf, k, "D10"),
    "E10_net_oil_lb": cell(onv, k, "E10"),
    "F10_net_kg": cell(onv, k, "F10"),
    "F10_formula": cell(onf, k, "F10"),
    "G10_ph": cell(onv, k, "G10"),
    "I10_c_content": cell(onv, k, "I10"),
    "J10_c_uncertainty": cell(onv, k, "J10"),
    "K10_mass_uncertainty": cell(onv, k, "K10"),
}
rollup = {
    "A18_sum_net_kg": cell(onv, k, "A18"),
    "B18_filtration_loss_kg": cell(onv, k, "B18"),
    "B18_formula": cell(onf, k, "B18"),
    "C18_mobi_kg": cell(onv, k, "C18"),
    "C18_formula": cell(onf, k, "C18"),
    "D18_ph": cell(onv, k, "D18"),
    "G18_origins": cell(onv, k, "G18"),
}
constants = {
    "M3_lbs_per_kg": cell(onv, k, "M3"),
    "M4_kg_per_lb": cell(onv, k, "M4"),
    "M5_filtration_solids": cell(onv, k, "M5"),
    "M6_ph_target": cell(onv, k, "M6"),
    "M7_testing_uncertainty": cell(onv, k, "M7"),
}
m5 = onf[k]["M5"]
headers = {c: cell(onv, k, f"{c}9") for c in "ABCDEFGHIJK"}
headers.update({"A8": cell(onv, k, "A8"), "A1": cell(onv, k, "A1"), "A17": cell(onv, k, "A17"),
                "B17": cell(onv, k, "B17"), "C17": cell(onv, k, "C17"), "D17": cell(onv, k, "D17")})
summary = {
    "B11_deliveries_cargo_kg": cell(onv, "Summary", "B11"),
    "D11_mass_used_kg": cell(onv, "Summary", "D11"),
    "E11_sparging_loss_kg": cell(onv, "Summary", "E11"),
    "F11_filtration_loss_kg": cell(onv, "Summary", "F11"),
    "G11_mobi_kg": cell(onv, "Summary", "G11"),
    "B19_kerry_mobi_kg": cell(onv, "Summary", "B19"),
    "C19_composite_sample_id": cell(onv, "Summary", "C19"),
    "D19_date_composited": str(cell(onv, "Summary", "D19"))[:10],
    "E19_c_fraction": cell(onv, "Summary", "E19"),
    "F19_coa_link": cell(onf, "Summary", "F19"),
    "G19_c_uncertainty_fraction": cell(onv, "Summary", "G19"),
    "H19_testing_uncertainty": cell(onv, "Summary", "H19"),
}
comments = []
for ws in onf.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.comment:
                comments.append({"tab": ws.title, "cell": c.coordinate, "text": c.comment.text})

# Certify-attached Ops Notes copy (2026-10-01) vs live
OA = SX / "Certify_attached_Ops_Notes_src_1M3W1NWED1S0K0MP.xlsx"
oav = openpyxl.load_workbook(OA, data_only=True)
attached_vs_live_kerry_value_diffs = []
for r in range(1, 30):
    for c in range(1, 14):
        a, b = oav[k].cell(r, c).value, onv[k].cell(r, c).value
        if a != b:
            attached_vs_live_kerry_value_diffs.append([oav[k].cell(r, c).coordinate, a, b])

# ---------------------------------------------------------------- CAR-474
CAR = SX / "CAR-474_Solids_Loading_Kerry_source_0.071pct.xlsx"
carv = openpyxl.load_workbook(CAR, data_only=True).active
car_rows = [[carv.cell(r, c).value for c in range(1, 4)] for r in range(1, carv.max_row + 1)]
manitowoc = next(r for r in car_rows if r[0] == "MANITOWOC CALCINER PHASE")

# ---------------------------------------------------------------- Standard EFs (live + attached)
EF = SX / "Standard_EFs_live_20261006T1840Z.xlsx"
efv = openpyxl.load_workbook(EF, data_only=True)["2026"]
eff = openpyxl.load_workbook(EF)["2026"]
EFA = SX / "Certify_attached_StdEFs_src_1KWZ2NVQM1S08AWN.xlsx"
efa = openpyxl.load_workbook(EFA, data_only=True)["2026"]

# ---------------------------------------------------------------- cross-week Ops Notes
def kerry_line(path):
    wv = openpyxl.load_workbook(path, data_only=True)
    wf = openpyxl.load_workbook(path)
    if "Kerry" not in wv.sheetnames:
        return {"kerry_tab": False}
    kv, kf = wv["Kerry"], wf["Kerry"]
    rows = []
    for r in range(10, 16):
        if kv.cell(r, 2).value:
            rows.append({"row": r, "date": str(kv.cell(r, 1).value)[:10], "uid": kv.cell(r, 2).value,
                         "full_lb": kv.cell(r, 3).value, "empty_lb": kv.cell(r, 4).value,
                         "net_kg": kv.cell(r, 6).value,
                         "full_link": kf.cell(r, 3).value, "empty_link": kf.cell(r, 4).value})
    return {"kerry_tab": True, "header_A1": kv["A1"].value, "rows": rows}

cross_week = {}
for name in ["INJ-08-2026-W5", "INJ-09-2026-W1", "INJ-09-2026-W2", "INJ-09-2026-W3", "INJ-10-2026-W1"]:
    p = next(XC.glob(f"{name}_Ops_Notes_live_*.xlsx"))
    cross_week[name] = kerry_line(p)
    cross_week[name]["artifact_path"] = str(p.relative_to(B))

# ---------------------------------------------------------------- Certify texts
seq_modal = (B / "certify_modal_injection_sequestration.txt").read_text()
proc_modal = (B / "certify_modal_transport_process.txt").read_text()
emb_modal = (B / "certify_modal_transport_embodied.txt").read_text()
bcu_modal = (B / "certify_modal_bcu.txt").read_text()
calc_view = (B / "certify_calculation_view.txt").read_text()

opened = lambda **kw: kw  # readability helper

log = {
    "batch_id": "INJ-09-2026-W4-KERRY",
    "oil_type": "Kerry",
    "delivery_mode": "tanker",
    "delivery_mode_basis": ("Drive 'Kerry Oil' subfolder holds one Full + one Empty CAT Scale ticket pair "
                            "(Sept_W4_Full_Scale_Ticket_Kerry.jpg, Sept_W4_Empty_Scale_Ticket_Kerry.jpg), commodity "
                            "'TANKER' on both; Ops Notes Kerry tab header 'BATCH HEADER — Kerry (Calciner Waste Oil, "
                            "Tankers)'; no tote ledger and no multi-tote BOL"),
    "reporting_period": "2026-09-01 to 2026-09-30 (Certify removal period 19 Sep 2026 to 25 Sep 2026)",
    "certify_removal_id": "rmv_1M3T2J3V51S0NCHH",
    "certify_project_id": "prj_1HZSSWBQM1S08H83",
    "certify_removal_url": REMOVAL_URL,
    "drive_folder_url": "https://drive.google.com/drive/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0",
    "T0": "2026-10-06T18:23:50Z",
    "preflight": {
        "knowledge_base": ("knowledge-base/Charm_Isometric_Knowledge_Base.md read in full (lines 1-1300) at "
                           "2026-10-06 ~18:24Z: Sections 0-16, incl. BCU QA Rule (never exceed), uncertainty "
                           "Layers 1-3, Document Location Rule, Kerry oil entry"),
        "lessons_learned": ("skills/qa/batch-qa-kerry/references/lessons_learned.md read in full: FC-K1 to FC-K8 "
                            "and cross-skill FC1/FC3/FC8/FC10; AECN FC12-FC14 read in "
                            "skills/qa/batch-qa-aecn/references/lessons_learned.md lines 219-313"),
        "checklist_structure": ("skills/qa/batch-qa-kerry/references/checklist_structure.md read in full: tote vs "
                                "tanker table, Sections 1-8, custody rule (2026-09-29), tanker uncertainty 72.57 kg"),
        "failure_categories_printed": [
            "FC-K2 process transport mass is gross mass hauled; tanker = oil-only ticket net",
            "FC-K4 no 1.29% sparging on Kerry",
            "FC-K5 no upstream Kerry production or biomass component",
            "FC-K6 counterfactual = 0",
            "FC-K7 detect tote vs tanker from the artifacts and record it",
            "FC-K8 follow any changed finding through every dependent row",
            "FC1 Sources tab is the document truth; COBB cell A before values",
            "FC3 open both ticket images; open every component modal",
            "FC8 vehicle embodied EF per mile",
            "FC10 every note cites [log:KEY]; blocked needs 3 attempts",
            "FC14 read VVB guidance and Ops Notes cell comments first",
            "FC12 / FC13 fix every dependent row; no Pass row narrates a cross-batch inconsistency",
            "not applicable (tote only): FC-K1, FC-K3",
        ],
        "failure_categories_printed_when": "21:30:40Z as a chat message (the 18:24Z first-pass list was not shown in chat), before the ordered Gate 1 re-pass",
        "registry_checked": ("skills/qa/batch-qa-kerry/qa_active_kerry_batches.json read in full: entries "
                             "INJ-08-2026-W3-KERRY, K-002, INJ-07-2026-W4-KERRY; no INJ-09-2026-W4 entry, fresh QA"),
    },
    "vvb_guidance": {
        "_primary_source_opened": [
            opened(file="VVB Guidance September 1 - September 30", action="pdf_read",
                   drive_id="1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc",
                   live_source_url=DOC.format("1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc"),
                   artifact_path="source_exports/VVB_Guidance_Sep_2026.txt", modified="2026-10-05T07:16:43Z"),
            opened(file="VVB Guidance August 1 - August 31", action="pdf_read",
                   drive_id="1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y",
                   live_source_url=DOC.format("1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y"),
                   artifact_path="source_exports/VVB_Guidance_Aug_2026.txt"),
            opened(file="VVB Guidance July 1 - July 31", action="pdf_read",
                   drive_id="1IQS3Aeqg3MISVjXqzRtYcYmCvEfRo7LNxQgilqdlF0U",
                   live_source_url=DOC.format("1IQS3Aeqg3MISVjXqzRtYcYmCvEfRo7LNxQgilqdlF0U"),
                   artifact_path="source_exports/VVB_Guidance_Jul_2026.txt"),
        ],
        "read_in_full": True,
        "read_order": ("First pass: Certify Components page (18:24:52Z) and Drive folder listing (18:24:53Z) were opened before the September ""guidance (18:26:00Z); the guidance preceded the Ops Notes, tickets, lab report, COBB and every Certify modal and source. ""Gate 1 was re-run in order at 21:30Z (see gate1_ordered_repass)."),
        "sections_sep": [
            "AECN Rail — Oil Withdrawn for Research and Development (Week 3, INJ-09-2026-W3)",
            "AECN Rail — New Rail Destination at Baton Rouge (Railcar SHPX215053, Week 4, INJ-09-2026-W4)",
            "AECN Rail — Bio-oil Loss",
            "Site Gasoline — E-85 Fills Quantified at an E-85 Emission Factor",
            "Site Diesel — Rail-Yard Air Compressor Fuel",
            "Immateriality of Argon Transport and removal from calculations",
        ],
        "sep_week4_window_verbatim": "SHPX215053, offloaded in Week 4 (INJ-09-2026-W4, 18 – 25 September 2026)",
        "sep_kerry_content": "September and August docs carry no Kerry section; the Kerry tanker method is the July section quoted below",
        "kerry_method_july_verbatim": {
            "delivery_vehicle": ("In this Reporting Period, Kerry calciner oil is delivered to the Basco injection site in bulk "
                                 "tanker trailers rather than in IBC totes as in prior Periods."),
            "delivery_form": ("Delivered mass is therefore established from CAT Scale tickets — the full weight less the "
                              "post-offload empty (tare) weight of the same tractor and trailer — rather than from "
                              "per-tote tag weights. There is no per-tote record for a tanker load; the scale tickets "
                              "are the primary mass evidence."),
            "filtered_mass": ("For Kerry, that subtraction uses the measured solids content of Kerry calciner oil itself, "
                              "not the AECN-derived solids content that Charm applies to its other third-party oil."),
            "testing_location": "Testing is in the Additional Documentation folder.",
            "constants_block_citation": ("The Kerry solids value and its source analysis are cited on the constants block "
                                         "of the Kerry tab in the weekly ops notes"),
            "loss_treatment": ("Kerry takes a filtration deduction only. No sparging loss is applied to Kerry oil (because "
                               "Kerry is not sparged)"),
            "tank_hold": ("The oil that is unloaded from the truck is held in a dedicated tank and progressively injected "
                          "in combination with AECN injections as the high viscosity of the oil precludes independent "
                          "injection."),
            "removal_completion": ("trucked Kerry oil is progressively co-injected with AECN over the course of the month "
                                   "and the associated removal is not considered complete until the tank is empty."),
            "ph": ("we do not have an independent pH value that is specific to Kerry. Rather, the pH measured over the "
                   "course of the month’s AECN injections is net of Kerry oil as well."),
        },
        "bearing_on_this_batch": ("July Kerry section governs: ticket pair is the mass evidence, Kerry-specific filtration "
                                  "only, no sparging, tank hold until empty, pH shared with AECN. No section in any of the "
                                  "three docs addresses holding one Kerry tanker load across weeks while a later load is "
                                  "credited first, or the 14-day ticket-to-injection gap."),
        "ops_notes_cell_comments": comments,
    },
    "batch_folder_inventory": {
        "_primary_source_opened": [opened(file="Drive folder W4 (1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0) listing, all pages + subfolders",
                                          action="csv_exported",
                                          live_source_url="https://drive.google.com/drive/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0",
                                          artifact_path="batch_folder_listing.txt")],
        "items": ["INJ-09-2026-W4 Ops Notes (Google Sheet 1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ, modified 2026-10-05T15:09:43Z)",
                  "Kerry Oil/ (2 files: Sept_W4_Full_Scale_Ticket_Kerry.jpg 1GGBPvhyFDrD6GT-kC86Vx7tbiQ9iTjl4; Sept_W4_Empty_Scale_Ticket_Kerry.jpg 1LwkjfYLg37l7whJyCG5mU5Z7bsKD3IKi)",
                  "Testing/ (1 file: SR26-05719 W4 Kerry AECN QOWV COA.pdf 1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ)",
                  "Scale Tickets/ (AECN railcar subfolders SHPX215079, SHPX215091, SHPX215053, SHPX215039)",
                  "RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png (AECN route map)"],
        "kerry_mass_subfolder": "Kerry Oil/",
        "testing_subfolder_files": 1,
    },
    "scale_tickets": {
        "_primary_source_opened": [
            opened(file="Sept_W4_Full_Scale_Ticket_Kerry.jpg", action="image_read",
                   live_source_url=DRIVE.format("1GGBPvhyFDrD6GT-kC86Vx7tbiQ9iTjl4"),
                   artifact_path="screenshots/Sept_W4_Full_Scale_Ticket_Kerry.jpg",
                   sha256=sha(B / "screenshots/Sept_W4_Full_Scale_Ticket_Kerry.jpg")),
            opened(file="Sept_W4_Empty_Scale_Ticket_Kerry.jpg", action="image_read",
                   live_source_url=DRIVE.format("1LwkjfYLg37l7whJyCG5mU5Z7bsKD3IKi"),
                   artifact_path="screenshots/Sept_W4_Empty_Scale_Ticket_Kerry.jpg",
                   sha256=sha(B / "screenshots/Sept_W4_Empty_Scale_Ticket_Kerry.jpg")),
        ],
        "full_ticket": {"ticket_number": "1189526252027", "date": "9-09-26", "time": "09:27", "scale": "1895",
                        "location": "LOVES COUNTRY STORES, I43 S BUISNESS DR EX 120, WILSON TOWNSHIP WI",
                        "steer_lb": 12280, "drive_lb": 31920, "trailer_axle_lb": 29800, "gross_weight_lb": 74000,
                        "commodity": "TANKER", "company": "FREIBURGER", "tractor": "07", "trailer": "1013",
                        "weigh_number": "2027", "delivery_site": "CHARM", "drive_file_created": "2026-09-30T17:02:38Z"},
        "empty_ticket": {"ticket_number": "1319926254821", "date": "9-11-26", "time": "13:20", "scale": "3199",
                         "location": "LOVES COUNTRY STORE, HWY 82 HWY 65, LAKE VILLAGE AR",
                         "steer_lb": 11780, "drive_lb": 13840, "trailer_axle_lb": 8680, "gross_weight_lb": 34300,
                         "commodity": "TANKER", "company": "FREIBURGER", "tractor": "07", "trailer": "1013",
                         "weigh_number": "4821", "delivery_site": "CHARM", "drive_file_created": "2026-09-14T19:13:59Z"},
        "tractor_trailer_match": True,
        "scale_type": "CAT Scale (Certified Automated Truck Scale) on both tickets — commercial truck scale",
        "net_lb": 74000 - 34300,
        "net_kg": (74000 - 34300) * 0.453592,
        "days_full_ticket_to_ops_row_date_20260925": 16,
        "days_empty_ticket_to_ops_row_date_20260925": 14,
        "days_full_ticket_to_cobb_completion_20260923": 14,
        "certify_copies_identical_to_drive": (sha(B / "screenshots/Sept_W4_Full_Scale_Ticket_Kerry.jpg") ==
                                              sha(SX / "Certify_attached_src_1M3VZ8VKH1S0MRDE_Sept_W4_Full_Scale_Ticket_Kerry.jpg")
                                              and sha(B / "screenshots/Sept_W4_Empty_Scale_Ticket_Kerry.jpg") ==
                                              sha(SX / "Certify_attached_src_1M3VZ8XVN1S0W24R_Sept_W4_Empty_Scale_Ticket_Kerry.jpg")),
    },
    "bol": {
        "status": "absent",
        "_primary_source_opened": [opened(file="Drive W4 folder listing + Certify Sources tab (8 sources)", action="csv_exported",
                                          live_source_url=REMOVAL_URL + "?tab=sources",
                                          artifact_path="certify_sources_tab.txt",
                                          negative_check_tokens=["Bill of Lading", "BOL"], items_found=[])],
        "searched": ["Drive W4 batch folder and all four subfolders", "Certify Sources tab (8 sources)",
                     "COBB BOL_number field holds the tanker UID 'WILA004', not a BOL document"],
    },
    "lab_results": {
        "_primary_source_opened": [opened(file="SR26-05719 W4 Kerry AECN QOWV COA.pdf (page 1 of 3, SR26-05719.001)",
                                          action="pdf_read",
                                          live_source_url=DRIVE.format("1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ"),
                                          artifact_path="source_exports/Drive_Testing_SR26-05719_COA_1Viar0c3xdOh.pdf")],
        "certificate": "SR26-05719.001", "sgs_order": "5506143", "client_id": "9-2026-W4-KERRY",
        "location_on_coa": "FORT LUPTON, CO", "sample_source": "Submitted Sample", "sampled_by": "Client",
        "sampled": "25-Sep-2026 07:00", "received": "28-Sep-2026 11:00",
        "analysed": "28-Sep-2026 14:29 - 28-Sep-2026 23:23", "report_date": "28-Sep-2026",
        "carbon_pct": 57.9, "hydrogen_pct": 6.4, "nitrogen": "<0.75", "kinematic_viscosity_cst_40C": 545.2,
        "acid_number_mgKOH_g": 154, "density_15C_g_cm3": 1.201,
        "lab_flags": "Carbon, Hydrogen and Acid Number marked '#' (outside test method limits / precision study range)",
        "aecn_sample_same_report": {"certificate": "SR26-05719.002", "location_on_coa": "FORT LUPTON, CO", "carbon_pct": 44.0, "hydrogen_pct": 6.6},
        "certify_copy_sha256": sha(SX / "Certify_attached_COA_src_1M3VZ8S8W1S013HS.pdf"),
        "drive_copy_sha256": sha(SX / "Drive_Testing_SR26-05719_COA_1Viar0c3xdOh.pdf"),
    },
    "ops_notes": {
        "_primary_source_opened": [opened(file="INJ-09-2026-W4 Ops Notes (live export 2026-10-06 18:28Z, formulas and values)",
                                          action="sheet_grid_read",
                                          live_source_url=SHEET.format("1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ"),
                                          artifact_path="source_exports/INJ-09-2026-W4_Ops_Notes_live_20261006T1828Z.xlsx")],
        "tabs": onf.sheetnames,
        "kerry_row": kerry_row,
        "rollup": rollup,
        "constants": constants,
        "constants_M5_comment": m5.comment.text if m5.comment else None,
        "constants_M5_hyperlink": m5.hyperlink.target if m5.hyperlink else None,
        "headers": headers,
        "summary": summary,
        "aecn_mass_in_kg_summary_G8": cell(onv, "Summary", "G8"),
        "total_mobi_all_oils_kg_summary_G13": cell(onv, "Summary", "G13"),
        "certify_attached_copy": {"file": "INJ-09-2026-W4 Ops Notes - 2026-10-01 (src_1M3W1NWED1S0K0MP)",
                                  "artifact_path": "source_exports/Certify_attached_Ops_Notes_src_1M3W1NWED1S0K0MP.xlsx",
                                  "kerry_tab_value_diffs_vs_live": attached_vs_live_kerry_value_diffs,
                                  "kerry_tab_formula_diffs_vs_live": ["C10: plain 74000 in the attached copy, HYPERLINK to the Full ticket in live",
                                                                      "D10: plain 34300 in the attached copy, HYPERLINK to the Empty ticket in live"]},
    },
    "filtration_constant_source": {
        "_primary_source_opened": [opened(file="CAR-474 Solids Loading in Kerry-AECN-WODO oils (2026-05-28) - source for Kerry Calciner 0.071%.xlsx",
                                          action="sheet_grid_read",
                                          live_source_url=DRIVE.format("1twIf0H9Ma4crVsPgD0Iq6eFDwxQIC-ni"),
                                          artifact_path="source_exports/CAR-474_Solids_Loading_Kerry_source_0.071pct.xlsx")],
        "rows": car_rows,
        "manitowoc_calciner_pct_solids": manitowoc[1],
        "lab": manitowoc[2],
        "attached_in_certify": False,
    },
    "cobb_row_id_verified": True,
    "cobb_cell_A_value": "INJ-09-2026-W4_calciner",
    "cobb_tracker": {
        "_primary_source_opened": [
            opened(file="Bio-oil Injection Tracker, tab 'Basco Injection -- COBB', live query of every row whose injection_batch contains 'calciner' (gviz HTML view, 2026-10-06 18:42Z)",
                   action="sheet_grid_read", live_source_url=SHEET.format("116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q"),
                   artifact_path="source_exports/COBB_live_calciner_rows_20261006T1842Z.txt"),
            opened(file="Same tracker, full workbook export taken 2026-10-06 18:26:54Z (row numbers)", action="sheet_grid_read",
                   live_source_url=SHEET.format("116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q"),
                   artifact_path="source_exports/COBB_tracker_export_20261006T1826Z_from_QOWV_session.xlsx"),
        ],
        "tab": "Basco Injection -- COBB",
        "cobb_row_id_verified": True,
        "cobb_cell_A_value": "INJ-09-2026-W4_calciner",
        "row_numbers_in_export": [1790, 2718, 3681],
        "row_numbers_note": "The tab repeats its dataset in three blocks; all three W4 calciner rows carry identical values except injection_ph is blank in the third block",
        "w4_row": {"injection_batch": "INJ-09-2026-W4_calciner", "injected_product": "Kerry Calciner",
                   "consumed_lot": "WILA004_offload_1", "BOL_number": "WILA004",
                   "quantity_consumed_in_injection": 18007.6024, "offloaded_quantity_kg": 18007.6024,
                   "origin_quantity_kg": 20000, "order_line_completed_on": "2026-09-24 18:04:36",
                   "injection_completion_date": "2026-09-23", "injection_ph": 2.97},
        "w3_row": {"injection_batch": "INJ-09-2026-W3_calciner", "consumed_lot": "WILA003_offload_1",
                   "quantity_consumed_in_injection": 18007.6024, "origin_quantity_kg": 20000,
                   "order_line_completed_on": "2026-09-12 14:17:56", "injection_completion_date": "2026-09-18",
                   "injection_ph": 2.7},
        "w2_row": {"injection_batch": "INJ-09-2026-W2_calciner", "consumed_lot": "WILA002_offload_1",
                   "quantity_consumed_in_injection": 17000, "origin_quantity_kg": 17000,
                   "order_line_completed_on": "2026-09-02 19:41:31", "injection_completion_date": "2026-09-17",
                   "injection_ph": 2.92},
        "consumed_lot_pattern": "WILA00N_offload_1 (tanker era); the kc_NNNN pattern in the skill reference belongs to the tote batches K-001/K-002",
        "export_matches_live": True,
    },
    "cross_week_kerry": {
        "_primary_source_opened": [
            opened(file="Sept_W3_Full_Scale_Ticket_Kerry.pdf", action="pdf_read", live_source_url=DRIVE.format("1GAqZF0tspn69yxEu9qeh335noEtt4cIH"),
                   artifact_path="source_exports/w3_kerry_cross_check/Sept-W3-Full-Scale-Ticket-Kerry.pdf"),
            opened(file="Sept_W3_Empty_Scale_Ticket_Kerry.pdf", action="pdf_read", live_source_url=DRIVE.format("1yIF3Xk4gf5-KAlQWOgEdsFtLL17r7eJz"),
                   artifact_path="source_exports/w3_kerry_cross_check/Sept-W3-Empty-Scale-Ticket-Kerry.pdf"),
            opened(file="Sept_W2_Full_Scale_Ticket_Kerry.jpg", action="image_read", live_source_url=DRIVE.format("1btCtnc1rbtqxocWXm7n2UE64uul98WHY"),
                   artifact_path="source_exports/w3_kerry_cross_check/Sept_W2_Full_Scale_Ticket_Kerry.jpg"),
            opened(file="Sept_W2_Empty_Scale_Ticket_Kerry.pdf", action="pdf_read", live_source_url=DRIVE.format("1USAs0YoRNzymMk56RZBa70pYdhca1Sbc"),
                   artifact_path="source_exports/w3_kerry_cross_check/Sept-W2-Empty-Scale-Ticket-Kerry.pdf"),
        ],
        "ops_notes_kerry_rows": cross_week,
        "w2_tickets": {"full": {"ticket_number": "1189526243756", "date": "8-31-26", "time": "15:29", "location": "WILSON TOWNSHIP WI", "gross_weight_lb": 75520, "tractor": "07", "trailer": "1013"},
                       "empty": {"ticket_number": "1186426245724", "date": "9-02-26", "time": "10:47", "location": "PORT BARRE LA", "gross_weight_lb": 35320, "tractor": "07", "trailer": "1013"}},
        "w3_tickets": {"full": {"ticket_number": "1189526259282", "date": "9-16-26", "time": "09:59", "location": "WILSON TOWNSHIP WI", "gross_weight_lb": 76680, "tractor": "07", "trailer": "1013"},
                       "empty": {"ticket_number": "1319926261935", "date": "9-18-26", "time": "22:06", "location": "LAKE VILLAGE AR", "gross_weight_lb": 34420, "tractor": "07", "trailer": "1013"}},
        "w4_ticket_pair_reused_elsewhere": False,
        "w3_ops_notes_net_kg": 19168.79792,
        "w2_ops_notes_net_kg": 18234.3984,
        "trip_order_by_ticket_date": ["WILA002: 8-31 full / 9-02 empty (credited W2)",
                                      "WILA004: 9-09 full / 9-11 empty (credited W4, this removal)",
                                      "WILA003: 9-16 full / 9-18 empty (credited W3)"],
        "removal_crossref": {"_primary_source_opened": [opened(file="Removal–Batch Cross-Reference — September 1 - September 30 RP", action="sheet_grid_read",
                                                               live_source_url=SHEET.format("1JcbdFHeAyjeqcCKESwDzJpmUii_FKgK6NH7BWFmi7VI"),
                                                               artifact_path="source_exports/Removal_Batch_CrossRef_Sep2026_live_20261006T1834Z.xlsx")],
                             "w4_kerry": "rmv_1M3T2J3V51S0NCHH, INJ-09-2026-W4-KERRY, 2026-09-25",
                             "w3_kerry": "rmv_1M3SWNGK51S0GH00, INJ-09-2026-W3-KERRY, 2026-09-18",
                             "w2_kerry": "rmv_1M3SW77M41S0RNME, INJ-09-2026-W2-KERRY, 2026-09-11"},
    },
    "standard_efs_2026": {
        "_primary_source_opened": [opened(file="Standard Emission Factors + Calculations, tab 2026 (live export 18:40Z)", action="sheet_grid_read",
                                          live_source_url="https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705",
                                          artifact_path="source_exports/Standard_EFs_live_20261006T1840Z.xlsx")],
        "tab": "2026",
        "row6_label": efv["B6"].value, "row6_tanker_fuel_use_mt_per_t_mi": efv["F6"].value, "row6_source": efv["G6"].value,
        "row11_label": efv["B11"].value, "row11_tanker_embodied_mt_per_mi": efv["F11"].value, "row11_formula_D": eff["D11"].value,
        "row7_flatbed_fuel_use_mt_per_t_mi": efv["F7"].value,
        "certify_attached_copy": {"sources": ["src_1KWZ2NVQM1S08AWN", "src_1KVJRSYT91S09G2E"],
                                  "identical_files": sha(SX / "Certify_attached_StdEFs_src_1KWZ2NVQM1S08AWN.xlsx") == sha(SX / "Certify_attached_StdEFs_src_1KVJRSYT91S09G2E.xlsx"),
                                  "row5_tanker_fuel_use": efa["F5"].value, "row10_tanker_embodied": efa["F10"].value,
                                  "artifact_path": "source_exports/Certify_attached_StdEFs_src_1KWZ2NVQM1S08AWN.xlsx"},
    },
    "route_map": {
        "_primary_source_opened": [opened(file="Kerry to Basco Distance.png (Certify src_1KT1W9XED1S08J0H)", action="image_read",
                                          live_source_url="https://registry.isometric.com/account/certify/source/src_1KT1W9XED1S08J0H",
                                          artifact_path="source_exports/Certify_attached_src_1KT1W9XED1S08J0H_Kerry_to_Basco_Distance.png")],
        "origin": "4343 Expo Dr, Manitowoc, WI 54220", "destination": "4687 LA-115, St Landry, LA 71367",
        "options_mi": [1059, 1071, 1090], "longest_mi": 1090, "longest_route": "via I-55 S (has tolls), 16 hr 49 min",
    },
    "retirement_certificate": {
        "_primary_source_opened": [opened(file="Charm-RetirementCertificate-RD-EACs-20251218.pdf (Certify src_1M1MFJPW11S08KY2)", action="pdf_read",
                                          live_source_url="https://registry.isometric.com/account/certify/source/src_1M1MFJPW11S08KY2",
                                          artifact_path="source_exports/Certify_attached_src_1M1MFJPW11S08KY2_Charm-RetirementCertificate-RD-EACs-20251218.pdf")],
        "retiring_org": "Amazon.com Services LLC", "on_behalf_of": "Charm Industrial, Inc", "date": "Dec 18, 2025",
        "vintage": 2024, "commodity": "Renewable Diesel TERCS", "number_retired": 2795,
        "verification_body": "Turner, Mason & Company", "certificate": "TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000",
    },
    "certify": {
        "_primary_source_opened": [
            opened(file="Certify GHG entry rmv_1M3T2J3V51S0NCHH, Components tab", action="modal_opened", live_source_url=REMOVAL_URL, artifact_path="certify_initial_snapshot.yml"),
            opened(file="Injection sequestration modal", action="modal_opened", live_source_url=REMOVAL_URL + "?component=cmp_1M3T2J3V51S056SG", artifact_path="certify_modal_injection_sequestration.txt"),
            opened(file="Process transport modal", action="modal_opened", live_source_url=REMOVAL_URL + "?component=cmp_1M3T2J3V51S0J2PA", artifact_path="certify_modal_transport_process.txt"),
            opened(file="Embodied transport modal", action="modal_opened", live_source_url=REMOVAL_URL + "?component=cmp_1M3T2J3V51S0YDTN", artifact_path="certify_modal_transport_embodied.txt"),
            opened(file="BCU modal", action="modal_opened", live_source_url=REMOVAL_URL + "?component=cmp_1M3T2J3V51S05QHZ", artifact_path="certify_modal_bcu.txt"),
            opened(file="Calculation view tab", action="modal_opened", live_source_url=REMOVAL_URL + "?tab=calculation-view", artifact_path="certify_calculation_view.txt"),
            opened(file="Datapoints tab", action="modal_opened", live_source_url=REMOVAL_URL + "?tab=data-points", artifact_path="certify_datapoints_tab.txt"),
            opened(file="Sources tab", action="modal_opened", live_source_url=REMOVAL_URL + "?tab=sources", artifact_path="certify_sources_tab.txt"),
        ],
        "removal_header": "Removal 37.73 tCO₂e, 19 Sep 2026 to 25 Sep 2026",
        "components_total": 4,
        "component_by_key": {
            "injection_sequestration": {"value_tCO2e": 38.206, "carbon_content_pct": 57.9, "carbon_content_pm": 0.2316,
                                        "carbon_sources": 2, "mass_of_product_kg": 17994.817, "mass_pm_kg": 72.57, "mass_sources": 3,
                                        "formula": "product_mass * carbon_content * {co2e_of_carbon}"},
            "transport_process": {"name": "Kerry to Basco Tanker Truck Transport Process Emissions", "value_tCO2e": 2.244, "pct": "5.95%",
                                  "ef_kg_per_t_mi": 0.1143, "ef_label": "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck",
                                  "distance_mi": 1090, "mass_of_load_t": 18.0076, "mass_of_load_pm_t": 0.07257, "mass_sources": 3,
                                  "formula": "mass * distance * carbon_intensity"},
            "transport_embodied": {"name": "Kerry to Basco Tanker Truck Transport Embodied Emissions", "value_tCO2e": 0.259, "pct": "0.69%",
                                   "ef_kg_per_mi": 0.23756, "ef_label": "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck",
                                   "ef_sources": 1, "distance_mi": 1090, "distance_sources": 1, "formula": "distance * carbon_intensity"},
            "bcu": {"name": "BCUs - Applied to Bio-Oil Transport Process Emissions", "category": "Mitigated / Bio-oil transport (Adjustments)",
                    "value_tCO2e": 2.244, "constant_reduction_kg": 2243.51, "sources": 1},
        },
        "component_tree": {"Mitigated": 40.450, "Mitigated/Bio-oil transport": 2.244, "Mitigated/CO2 stored": 38.206,
                           "Emitted": 2.503, "Emitted/Bio-oil transport": 2.503},
        "no_upstream_production_component": True,
        "no_counterfactual_component": True,
        "no_sparging_deduction_on_kerry": True,
        "calculation_view": {"net_co2e_removed_t": 37.730, "sequestrations_t": 38.206, "adjustments_tCO2e": 2.244,
                             "activities_tCO2e": 2.502, "uncertainty_discount_kg": 217},
        "datapoints_total": 7,
        "datapoints": [
            {"name": "Route Distance Kerry to Basco", "value": "1,090 mi", "collection": "DERIVED", "sources": ["Kerry to Basco Distance.png"]},
            {"name": "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck", "value": "0.1476 kgCO₂e/km", "collection": "DERIVED", "sources": ["Standard Emission Factors + Calculations (8).xlsx"]},
            {"name": "Allocated Kerry Oil Gross Mass", "value": "18.008 t", "collection": "REPORTED", "sources": ["INJ-09-2026-W4 Ops Notes - 2026-10-01", "Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "Sept_W4_Full_Scale_Ticket_Kerry.jpg"]},
            {"name": "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck", "value": "0.07 kgCO₂e/(km⋅t)", "collection": "DERIVED", "sources": ["Standard Emission Factors + Calculations (8).xlsx"]},
            {"name": "Mass of Injectant (per injection)", "value": "17.995 t", "collection": "REPORTED", "sources": ["INJ-09-2026-W4 Ops Notes - 2026-10-01", "Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "Sept_W4_Full_Scale_Ticket_Kerry.jpg"]},
            {"name": "Carbon Content of Bio-oil Injected (per injection)", "value": "57.90 %", "collection": "REPORTED", "sources": ["SR26-05719 W4 Kerry AECN QOWV COA.pdf", "INJ-09-2026-W4 Ops Notes - 2026-10-01"]},
            {"name": "BCUs Applied - Bio-Oil Transport Process [Certify input]", "value": "2.244 tCO₂e", "collection": "DERIVED", "sources": ["Charm-RetirementCertificate-RD-EACs-20251218.pdf"]},
        ],
        "certify_sources_tab_total": 8,
        "certify_sources_enumeration": [
            {"name": "INJ-09-2026-W4 Ops Notes - 2026-10-01", "source_id": "src_1M3W1NWED1S0K0MP", "linked": ["Allocated Kerry Oil Gross Mass", "Mass of Injectant (per injection)", "Carbon Content of Bio-oil Injected (per injection)"], "visibility": "PRIVATE"},
            {"name": "Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "source_id": "src_1M3VZ8XVN1S0W24R", "linked": ["Allocated Kerry Oil Gross Mass", "Mass of Injectant (per injection)"], "visibility": "PRIVATE"},
            {"name": "Sept_W4_Full_Scale_Ticket_Kerry.jpg", "source_id": "src_1M3VZ8VKH1S0MRDE", "linked": ["Allocated Kerry Oil Gross Mass", "Mass of Injectant (per injection)"], "visibility": "PRIVATE"},
            {"name": "SR26-05719 W4 Kerry AECN QOWV COA.pdf", "source_id": "src_1M3VZ8S8W1S013HS", "linked": ["Carbon Content of Bio-oil Injected (per injection)"], "visibility": "PRIVATE"},
            {"name": "Charm-RetirementCertificate-RD-EACs-20251218.pdf", "source_id": "src_1M1MFJPW11S08KY2", "linked": ["BCUs Applied - Bio-Oil Transport Process [Certify input]"], "visibility": "PUBLIC"},
            {"name": "Standard Emission Factors + Calculations (8).xlsx", "source_id": "src_1KWZ2NVQM1S08AWN", "linked": ["Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck"], "visibility": "PUBLIC"},
            {"name": "Standard Emission Factors + Calculations (8).xlsx", "source_id": "src_1KVJRSYT91S09G2E", "linked": ["Emissions Factor - Vehicle Embodied Emissions - Tanker Truck"], "visibility": "PUBLIC"},
            {"name": "Kerry to Basco Distance.png", "source_id": "src_1KT1W9XED1S08J0H", "linked": ["Route Distance Kerry to Basco"], "visibility": "PUBLIC"},
        ],
        "attachment_map": {
            "Mass of Injectant (per injection)": ["INJ-09-2026-W4 Ops Notes - 2026-10-01", "Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "Sept_W4_Full_Scale_Ticket_Kerry.jpg"],
            "Allocated Kerry Oil Gross Mass": ["INJ-09-2026-W4 Ops Notes - 2026-10-01", "Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "Sept_W4_Full_Scale_Ticket_Kerry.jpg"],
            "Carbon Content of Bio-oil Injected (per injection)": ["SR26-05719 W4 Kerry AECN QOWV COA.pdf", "INJ-09-2026-W4 Ops Notes - 2026-10-01"],
            "Route Distance Kerry to Basco": ["Kerry to Basco Distance.png"],
            "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck": ["Standard Emission Factors + Calculations (8).xlsx"],
            "Emissions Factor - Vehicle Embodied Emissions - Tanker Truck": ["Standard Emission Factors + Calculations (8).xlsx"],
            "BCUs Applied - Bio-Oil Transport Process [Certify input]": ["Charm-RetirementCertificate-RD-EACs-20251218.pdf"],
        },
        "required_evidence": {
            "Mass of Injectant": ["scale_ticket", "ops_notes"],
            "Allocated Kerry Oil Gross Mass": ["scale_ticket"],
            "Carbon Content of Bio-oil Injected": ["lab"],
            "Route Distance": ["map_or_watco"],
            "Emissions Factor - Truck Transport Fuel Use": ["ef_sheet"],
            "Emissions Factor - Vehicle Embodied Emissions": ["ef_sheet"],
            "BCUs Applied": ["eac_cert"],
        },
        "required_evidence_basis": "Built from this removal's seven datapoints as read on the Datapoints and Sources tabs; categories follow MATRICES['KERRY'] (tanker, validated INJ-07-2026-W4) with keys matched to the current datapoint names",
    },
}

# Size of the ticket-attribution question (row 1.7): what this removal would credit if it carried the
# 16-18 Sep pair that the W3 removal credits. Read from the W3 Ops Notes file, computed with the same
# formula as this removal (MOBI x C x 3.667), carbon held at this removal's 57.9%.
w3p = next(XC.glob("INJ-09-2026-W3_Ops_Notes_live_*.xlsx"))
w3v = openpyxl.load_workbook(w3p, data_only=True)["Kerry"]
w3_mobi = w3v["C17"].value
this_seq = rollup["C18_mobi_kg"] / 1000 * 0.579 * 3.667
alt_seq = w3_mobi / 1000 * 0.579 * 3.667
log["cross_week_kerry"]["attribution_sensitivity"] = {
    "w3_ops_notes_C17_mobi_kg": w3_mobi,
    "this_removal_sequestration_t": round(this_seq, 4),
    "sequestration_if_16_18_sep_pair_t": round(alt_seq, 4),
    "difference_t": round(alt_seq - this_seq, 4),
    "difference_pct_of_this_removal": round((alt_seq - this_seq) / this_seq * 100, 2),
}

# ---- added after the Gate 3 review: W3 Certify read, W3 composite date, solids-constant facts
w3sum = openpyxl.load_workbook(w3p, data_only=True)["Summary"]
log["cross_week_kerry"]["w3_summary_row19"] = {"composite_sample_id": w3sum["C19"].value,
                                                "date_composited": str(w3sum["D19"].value)[:10],
                                                "c_fraction": w3sum["E19"].value}
log["cross_week_kerry"]["w3_certify"] = {
    "_primary_source_opened": [
        opened(file="Certify GHG entry rmv_1M3SWNGK51S0GH00 (W3 Kerry), Sources tab", action="modal_opened",
               live_source_url="https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M3SWNGK51S0GH00/edit?tab=sources",
               artifact_path="source_exports/w3_kerry_cross_check/certify_W3_kerry_sources_tab.txt"),
        opened(file="Certify GHG entry rmv_1M3SWNGK51S0GH00 (W3 Kerry), Datapoints tab", action="modal_opened",
               live_source_url="https://registry.isometric.com/account/certify/project/prj_1HZSSWBQM1S08H83/ghg-entry/rmv_1M3SWNGK51S0GH00/edit?tab=data-points",
               artifact_path="source_exports/w3_kerry_cross_check/certify_W3_kerry_datapoints_tab.txt")],
    "header": "Removal 40.19 tCO₂e, 12 Sep 2026 to 18 Sep 2026",
    "ticket_sources": ["Sept_W3_Full_Scale_Ticket_Kerry.pdf", "Sept_W3_Empty_Scale_Ticket_Kerry.pdf"],
    "mass_of_injectant_t": 19.155, "allocated_gross_mass_t": 19.169, "carbon_pct": 57.90,
    "carbon_source": "SR26-05599.003 W3 Kerry COA.pdf", "bcu_t": 2.388,
}
aecn = onf["AECN Rail"]["O7"]
w5p = next(XC.glob("INJ-08-2026-W5_Ops_Notes_live_*.xlsx"))
w5o5 = openpyxl.load_workbook(w5p)["Kerry"]["O5"]
note = w5o5.comment.text if w5o5.comment else ""
mobi_hi = rollup["A18_sum_net_kg"] * (1 - 0.0071)
log["solids_constant_check"] = {
    "_primary_source_opened": [
        opened(file="INJ-09-2026-W4 Ops Notes, AECN Rail tab N7:O7", action="sheet_grid_read",
               live_source_url=SHEET.format("1zgrkVKQsGlzwjiumtn1vkYSaCt5_XTr7UWs3lR3RORQ"),
               artifact_path="source_exports/INJ-09-2026-W4_Ops_Notes_live_20261006T1828Z.xlsx"),
        opened(file="INJ-08-2026-W5 Ops Notes, Kerry tab O5 cell note", action="sheet_grid_read",
               live_source_url=SHEET.format("1o6xz3GjWJSkmMNnjZV30U4-HNzZyJCSAp-XgsCJqbEY"),
               artifact_path=str(w5p.relative_to(B)))],
    "aecn_rail_O7_label": onv["AECN Rail"]["N7"].value,
    "aecn_rail_O7_filtration_solids": openpyxl.load_workbook(ON, data_only=True)["AECN Rail"]["O7"].value,
    "aecn_rail_O7_formula": aecn.value,
    "kerry_M5_filtration_solids": constants["M5_filtration_solids"],
    "july_guidance_verbatim": "Kerry calciner oil measures materially higher in solids than AECN oil",
    "july_guidance_quote_in_source": "Kerry calciner oil measures materially higher in solids than AECN oil" in (SX / "VVB_Guidance_Jul_2026.txt").read_text(),
    "w5_kerry_O5_note_verbatim": note,
    "w5_note_discrepancy_quote": "quotes 'Kerry Manitowoc Calciner Phase Separated Tar - 0.71% solids'",
    "w5_note_confirm_quote": "Confirm with Steven Rowland before this constant is ever changed.",
    "w5_note_resolution_quote": "the data file is authoritative and the Slack text is treated as a transcription slip",
    "w4_M5_note": constants and (m5.comment.text if m5.comment else None),
    "sensitivity_if_0_71_pct": {
        "mobi_kg": round(mobi_hi, 3),
        "sequestration_t": round(mobi_hi / 1000 * 0.579 * 3.667, 4),
        "difference_t": round(mobi_hi / 1000 * 0.579 * 3.667 - this_seq, 4),
        "difference_pct": round((mobi_hi / 1000 * 0.579 * 3.667 - this_seq) / this_seq * 100, 2),
    },
}
assert log["solids_constant_check"]["w5_note_discrepancy_quote"].split("quotes ")[1] in note
assert log["solids_constant_check"]["w5_note_confirm_quote"] in note
assert log["solids_constant_check"]["w5_note_resolution_quote"] in note
# 16-18 Sep pair transport effect (for 1.7)
alt_gross_kg = 19168.79792
log["cross_week_kerry"]["attribution_sensitivity"]["transport_process_if_16_18_sep_pair_t"] = round(alt_gross_kg / 1000 * 1090 * 0.0001143, 5)
log["cross_week_kerry"]["attribution_sensitivity"]["transport_process_difference_t"] = round(
    alt_gross_kg / 1000 * 1090 * 0.0001143 - rollup["A18_sum_net_kg"] / 1000 * 1090 * 0.0001143, 5)
log["reference_rules"] = {
    "kb_ticket_date_rule": "For each pair: dates within 2 weeks of injection [VR Sec 3.5]",
    "kb_ticket_date_rule_in_source": "For each pair: dates within 2 weeks of injection [VR Sec 3.5]" in
        (B.parents[2] / "knowledge-base/Charm_Isometric_Knowledge_Base.md").read_text(),
    "kb_path": "knowledge-base/Charm_Isometric_Knowledge_Base.md (Section 10A, item 2)",
}


log["adversarial_review"] = {
    "file": "adversarial_review_INJ-09-2026-W4-KERRY.md",
    "reviewer": "independent general-purpose agent (adversarial-reviewer skill), files on disk only, no browser",
    "rows_upheld": 27, "rows_challenged": 5,
    "accepted": [
        "1.5 Pass -> Flag: Kerry solids constant 0.00071 below AECN 0.00196 against July 'materially higher'; Aug W5 note's 0.71% discrepancy; M5 uncited (moved from 1.7(e))",
        "1.7 Fail kept; wording fixed: COBB quantity does not separate WILA003/WILA004; W3 claim now read from the W3 Certify removal itself; KB 14-day rule quoted; transport/BCU effect added; dependent rows marked",
        "2A.6: COBB WILA004 quantity removed as support (WILA003 carries the same figure)",
        "3.6: paraphrase replaced by the verbatim July pH sentence",
        "S.4: cell addresses corrected to the value cells (C10, F10, A18, C18)",
    ],
    "reviewer_notes_added": ["W3 composite sample dated 2026-09-16 (W3 Summary D19) added to 1.7", "empty-ticket Drive filing date 2026-09-14 added to 1.7", "COBB WILA004 offload after its own injection completion added to 1.7"],
    "re_checked_by_qa_agent": "AECN Rail O7 and Aug W5 Kerry O5 note opened in the saved workbooks; W3 Kerry Certify removal Sources and Datapoints tabs read live",
}

log["gate1_ordered_repass"] = {
    "_primary_source_opened": [
        opened(file="VVB Guidance September 1 - September 30 (re-read in full)", action="pdf_read",
               live_source_url=DOC.format("1pib26xToLPFxaOla2p3pv4ummq5ekPpAn65FFuqrlPc"), artifact_path="source_exports/repass/VVB_Guidance_Sep_2026.txt"),
        opened(file="All Gate 1 sources re-opened after the guidance", action="sheet_grid_read",
               live_source_url="https://drive.google.com/drive/folders/1Ed6zGEgZO69vZPbvmDo0l4Sw4zzZiZl0", artifact_path="repass_comparison.json")],
    "why": ("The step audit (ledger_audit.json, first run) found that in the first pass the Certify Components page (18:24:52Z) and the "
            "Drive folder listing (18:24:53Z) were opened before the September guidance (18:26:00Z), and that the failure-category list "
            "had not been printed to chat. Every other first-pass read came after the guidance. Gate 1 was re-run in the required order."),
    "order": ["21:30Z failure categories printed to chat as a plain message",
              "21:30:41Z re-pass start; 21:30:48-53Z September, August and July guidance re-read from the live docs and read in full",
              "21:31Z Drive listing, Ops Notes W4 (and W2, W3, Aug W5), Standard EFs, CAR-474, CoA, both ticket images re-downloaded and opened",
              "21:32Z live COBB calciner rows; Certify Components tab, four component modals, Calculation view, Datapoints, Sources; W3 Kerry Datapoints",
              "21:46-21:50Z Certify-attached copies of the Ops Notes, both EF workbooks, CoA and both tickets; route map and retirement certificate (opened); Removal-Batch Cross-Reference; Sep W1 and Oct W1 Ops Notes; W2 and W3 ticket files (opened)"],
    "result": json.loads((B / "repass_comparison.json").read_text()) if (B / "repass_comparison.json").exists() else None,
}
out = B / "batch_INJ-09-2026-W4-KERRY_source_reads.json"
out.write_text(json.dumps(log, indent=1, default=str, ensure_ascii=False))
print("wrote", out.name, out.stat().st_size, "bytes")
print("kerry_row", kerry_row)
print("rollup", rollup)
print("constants", constants, "M5 comment:", log["ops_notes"]["constants_M5_comment"], "M5 link:", log["ops_notes"]["constants_M5_hyperlink"])
print("summary", summary)
print("EF live", log["standard_efs_2026"]["row6_tanker_fuel_use_mt_per_t_mi"], log["standard_efs_2026"]["row11_tanker_embodied_mt_per_mi"])
print("EF attached", log["standard_efs_2026"]["certify_attached_copy"])
print("tickets identical:", log["scale_tickets"]["certify_copies_identical_to_drive"], "CoA identical:", log["lab_results"]["certify_copy_sha256"] == log["lab_results"]["drive_copy_sha256"])
print("attached ops notes Kerry value diffs:", attached_vs_live_kerry_value_diffs)
print("CAR-474", manitowoc)
for kk, v in cross_week.items():
    print(kk, v.get("kerry_tab"), [(r["uid"], r["date"], r["full_lb"], r["empty_lb"]) for r in v.get("rows", [])])
