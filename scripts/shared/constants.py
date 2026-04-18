"""Folder IDs, sheet IDs, and other constants used across automation jobs.

Update this file when folders move or new sources get added.
"""
from __future__ import annotations

# Google Drive root folder IDs
REMOVALS_REPORTING_ROOT = "17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b"
INVOICES_TRACKING_DOCS_ROOT = "1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi"

# Source sheet IDs (read-only)
BIO_OIL_INJECTION_TRACKER = "116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q"
BGN_PRODUCTION_INVENTORY = "1cD9cd_y_SI8GA1Yv8TFtDPqevKKF1Jh42WFRWSSMJ6g"
STANDARD_EF_SHEET = "1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4"

# Tab names inside the tracker
COBB_TAB = "Basco Injection -- COBB"
COBB_OFFLOAD_TAB = "COBB (with offload info)"
LOADS_TAB = "Loads"
INVENTORY_TAB = "Oil_inventory_data"

# Canonical rail ops notes template (2-192)
CANONICAL_RAIL_TEMPLATE_ID = "1LitV1KLOKHA7pcfQtCpFEyWicNiy9Yn--NDd6Jp5sR8"

# Rail route distances (miles) — always fixed
ROUTE_RAIL_SOPOR_OPELOUSAS = 2199
ROUTE_TRUCK_AECN_SOPOR = 107.5
ROUTE_TRUCK_OPELOUSAS_BASCO = 42.9

# Rail constants
SPARGING_MASS_LOSS = 0.0129  # 1.29% — AECN only
LBS_TO_KG = 0.453592
KG_TO_LBS = 2.20462
TOTE_TARE_KG = 57.6
UNCERTAINTY_LBS_PER_TOTE = 2.5
WODO_STANDARD_LOSS_KG = 5.33

# Row/column conventions for rail ops notes (canonical template)
RAIL_TEMPLATE = {
    "completion_date_cell": "B1",
    "batch_number_cell": "B3",
    "railcar_cell": "B5",
    "constants_col_labels": "E",
    "constants_col_values": "F",
    "lbs_to_kg_row": 5,
    "sparging_mass_loss_row": 6,
    "sopor_opelousas_row": 7,
    "aecn_sopor_row": 8,
    "opelousas_basco_row": 9,
    "bol_header_row": 8,
    "bol_first_row": 9,
    "bol_last_row": 11,
    "total_loaded_mass_cell": "B13",
    "trucks_unloaded_header_row": 16,
    "offload_first_row": 17,
    "offload_last_row": 20,
    "total_unloaded_mass_cell": "D21",
    "oil_left_mt_cell": "B23",
    "oil_left_kg_cell": "B24",
}

# Highlight color for current offload row (RGB, 0-1 range)
HIGHLIGHT_COLOR = {"red": 1.0, "green": 0.949, "blue": 0.8}  # #FFF2CC

# User to impersonate for Gmail (domain-wide delegation)
# Emails are read on behalf of this user
GMAIL_IMPERSONATE_USER = "garrett.lutz@charmindustrial.com"

# Gmail search patterns
SGS_SENDER_QUERIES = [
    "from:sgs.com has:attachment newer_than:2d",
    "SGS Certificate Analysis has:attachment newer_than:2d",
    "from:sampling@charmindustrial.com SGS has:attachment newer_than:2d",
]

# Agfinity + Buckeye invoice senders (for future invoice-harvester port)
AGFINITY_SENDER = "energycsr@agfinityinc.com"
BUCKEYE_SENDER = "ar@buckeyeweldingsupply.com"

# Temp download path inside Cloud Function runtime
# /tmp is the only writable location on Cloud Functions
TEMP_DIR = "/tmp"
