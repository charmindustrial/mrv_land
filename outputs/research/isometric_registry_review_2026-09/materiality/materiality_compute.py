#!/usr/bin/env python3
"""
Materiality assessment (GHG Accounting Module v1.1 Section 5.0) across the 12
Charm bio-oil GHG statements covered by certify_lines_A_mar-aug2026.csv (Mar-Aug 2026)
and certify_lines_B_aug2025-feb2026.csv (Aug 2025-Feb 2026).

Re-runnable: reads the two CSVs in this folder, writes:
  - line_category_map.csv
  - materiality_assessment.xlsx
  - materiality_assessment.md
"""
import csv
import re
from collections import defaultdict, OrderedDict
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

FOLDER = Path(__file__).parent
FILE_A = FOLDER / "certify_lines_A_mar-aug2026.csv"
FILE_B = FOLDER / "certify_lines_B_aug2025-feb2026.csv"

HEADER_FILL = "D6E4F0"

# ---------------------------------------------------------------------------
# Period ordering (chronological, B file first, then A file)
# ---------------------------------------------------------------------------
PERIOD_ORDER = [
    "01 Aug 2025 to 15 Aug 2025",
    "16 Aug 2025 to 08 Sep 2025",
    "09 Sep 2025 to 30 Sep 2025",
    "01 Oct 2025 to 06 Nov 2025",
    "07 Nov 2025 to 31 Jan 2026",
    "01 Feb 2026 to 02 Mar 2026",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
]
LAST_6 = ["MAR", "APR", "MAY", "JUN", "JUL", "AUG"]

# ---------------------------------------------------------------------------
# Table 1 categories (Bio-oil Geological Storage protocol v1.2)
# ---------------------------------------------------------------------------
ESTABLISHMENT_CATS = [
    "Equipment and materials manufacture",
    "Equipment and materials transport to site",
    "Construction and installation",
    "Initial surveys",
    "Misc. (Establishment)",
    "End-of-life",
]
OPERATIONS_CATS = [
    "Biomass Feedstock Sourcing",
    "Biomass feedstock transport",
    "Biomass feedstock processing",
    "Pyrolysis or other process",
    "Direct emissions",
    "Bio-oil processing",
    "Bio-oil storage",
    "Bio-oil transport",
    "Bio-oil injection",
    "Sampling required for MRV",
    "Staff travel",
    "Surveys",
    "Misc. (Operations)",
]
ALL_CATS = ESTABLISHMENT_CATS + OPERATIONS_CATS

KANSAS_TOKENS = ["KS", "Kansas", "Vaulted", "Hutchinson"]
TRANSIT_LEG_NAMES = {"SOPOR", "Opelousas", "Maize"}


def is_kansas_transit_leg(name: str) -> bool:
    """A KS-substring hit that is really a rail/road leg passing through KS
    en route to LA (same logic the task gives for SOPOR/Opelousas/Maize)."""
    return bool(re.search(r"->\s*KS\s*->|CO->KS-> LA|CO to KS|KS to LA|KS to CO", name, re.I))


def categorize(name: str):
    """Return (category, reason, establishment_flag, subcategory)."""
    n = name.strip()
    nl = n.lower()
    est_flag = ""
    sub = ""

    if nl.startswith("injection sequestration"):
        return ("N/A - Sequestration (not a SSR)",
                "Sequestrations-branch line (gross removal), not an emission SSR; excluded from "
                "materiality sums regardless of this label", est_flag, sub)

    if n in ("Constant CO₂ reduction",) or nl.startswith("bcu") or nl.startswith("bcu's") or nl.startswith("bcus"):
        return ("Adjustment (not a SSR - reduction)",
                "Adjustments-branch line (BCU / constant CO2 reduction); a reduction, not an SSR, "
                "per instruction - excluded from materiality sums, reported on Adjustments sheet",
                est_flag, sub)

    if "sample" in nl:
        return "Sampling required for MRV", 'Contains "sample"', est_flag, sub

    if nl == "lcs usage emissions":
        return ("Bio-oil processing",
                "LCS (pre-treatment consumable) usage emissions, same as \"KS Pre-Treatment LCS "
                "Usage Emissions\" - pre-injection processing consumable",
                est_flag, sub)
    if nl == "ks + b6 embodied emissions":
        return ("Bio-oil processing",
                "Combined KS Pre-Treatment + B6 Injection embodied emissions line; spans both "
                "processing and injection stages, assigned to processing as the KS-side is the "
                "distinguishing component of this combined line",
                est_flag, sub)

    if "argon" in nl or "methanol" in nl:
        return ("Bio-oil processing",
                "Argon/Methanol = process consumable per instruction",
                est_flag, "consumables")

    if "brine" in nl:
        return ("Bio-oil injection", "Brine Transport mapped to injection per instruction",
                est_flag, sub)

    if "waste disposal" in nl or "landfilling" in nl or "incineration" in nl or \
       ("waste" in nl and "disposal" in nl):
        return ("Bio-oil injection",
                "Waste Disposal line mapped to injection (waste processing) per instruction",
                est_flag, "waste disposal")

    if "support travel" in nl:
        return "Staff travel", 'Contains "Support Travel"', est_flag, sub

    if n in ("B6 Injection - Capex Embodied Emissions", "B6 Injection - Capital Embodied Emissions"):
        return ("Bio-oil injection",
                "Capex Embodied line; injection-site capital embodied emissions "
                "(flagged: may belong under Establishment - Equipment and materials manufacture)",
                "yes", sub)
    if n == "Basco Embodied emissions":
        return ("Bio-oil injection",
                "Basco Embodied emissions; site embodied emissions "
                "(flagged: may belong under Establishment - Equipment and materials manufacture)",
                "yes", sub)
    if n in ("Louisiana Sitework", "LA Sitework", "BCU - Louisiana Sitework",
              "BCUs - Louisiana Sitework"):
        return ("Bio-oil injection",
                "Louisiana Sitework; injection-site groundworks "
                "(flagged: may belong under Establishment - Construction and installation)",
                "yes", sub)

    # Oil-route transport (Bio-oil transport): AECN->SOPOR, SOPOR->Opelousas,
    # Opelousas->Basco, CO->LA, Kerry->Basco, Additional Transport, Railcar
    # Movement, Extra Scaling Trip, Bourque Transport, and every named truck/
    # rail/flatbed/tanker leg between named sites.
    transport_patterns = [
        r"AECN\s*->", r"AECN to (KS|LA|SOPOR)", r"AECN\s.*Tanker Truck Transport",
        r"BOL \d+-T", r"\d{4}-T AECN",
        r"SOPOR\s*->|SOPOR to Opelousas|SOPOR->Maize",
        r"Opelousas to Basco|Opelousas Railyard|Opelousas Cleanup",
        r"CO to (KS|LA)|CO->KS|CO to LA",
        r"KS to (LA|CO)",
        r"QC to KS",
        r"Kerry to Basco",
        r"Additional Transport", r"Additional Railcar Movement",
        r"Extra Scaling Trip", r"Bourque Transport",
        r"Railcar (Movement|Cleaning)", r"Eagle Railcar Cleaning",
        r"KS Decommissioning Activity", r"KS Equipment Additional Transport",
        r"Disposed .*(Upstream )?Transport",
        r"Feb-Mar Railcar Loss",
        r"Inventory Reconciliation",
        r"Flatbed Truck Transport",
        r"Tanker Truck (Embodied|Process|Transport)",
        r"Non-Tanker Truck",
    ]
    if any(re.search(p, n, re.I) for p in transport_patterns):
        return ("Bio-oil transport",
                "Named truck/rail/flatbed/tanker transport leg of oil (or upstream/"
                "disposed-oil transport, railcar movement/cleaning, or site "
                "logistics leg) per instruction",
                est_flag, sub)

    # Pyrolysis / production
    if "pyrolysis" in nl or "oily fraction" in nl or \
       n in ("Disposed AECN Production Embodied Emissions",
             "PARTIAL - Disposed AECN Production Process Emissions",
             "Disposed Charm Oil Production Emissions"):
        return ("Pyrolysis or other process",
                'Pyrolysis / production-emissions line ("AECN pyrolysis…", '
                '"Pyrolysis - Charm…", oily-fraction CI, or disposed-oil production) '
                "per instruction",
                est_flag, sub)

    # KS Pre-Treatment (processing stage ahead of injection)
    if "ks pre-treatment" in nl or "ks pre treatment" in nl:
        return ("Bio-oil processing",
                "KS Pre-Treatment line; pre-injection oil processing/characterization "
                "energy, consumables, waste, embodied and vendor-delivery emissions",
                est_flag, sub)

    # B6 / Basco / injection-site utilities & consumables
    injection_patterns = [
        r"B6 (Injection|Diesel Delivery|Grid|Site)", r"B6 Vendor Delivery",
        r"Basco (Site|SP&C|Support Travel)?",  # broad catch, refined below
        r"Annual Well Work", r"Vaulted Embodied Emissions",
        r"February Basco Sitework", r"SP&C", r"Spare Parts and Consumables",
        r"Diesel Site Emissions", r"Charm .* PP Emissions",
    ]
    if any(re.search(p, n, re.I) for p in injection_patterns):
        return ("Bio-oil injection",
                "B6/Basco injection-site energy (diesel/gasoline/electricity/water), "
                "embodied, SP&C, or well-work line",
                est_flag, sub)

    return ("Misc.", "No specific Table 1 activity keyword matched; catch-all", est_flag, sub)


# ---------------------------------------------------------------------------
# Load file A
# ---------------------------------------------------------------------------
def load_A():
    leaves = []
    removal_meta = {}  # (period, removal_id) -> dict of totals
    with open(FILE_A, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            period = row["statement_period"]
            rid = row["removal_id"]
            unit = row["unit"]
            val = float(row["value"])
            val_kg = val * 1000 if unit.lower() == "t" else val  # A units are tCO2e uniformly per file, but guard anyway
            if unit.lower().startswith("t"):
                val_kg = val * 1000
            elif unit.lower() == "kg":
                val_kg = val
            else:
                val_kg = val * 1000  # tCO2e treated as tonnes
            leaves.append({
                "period": period, "statement_id": row["statement_id"], "removal_id": rid,
                "oil_type": row["oil_type"], "branch": row["branch"], "line": row["leaf_line"],
                "value_kg": val_kg, "unit_raw": unit,
            })
            key = (period, rid)
            meta = removal_meta.setdefault(key, {})
            field_map = {
                "net_co2e_removed": "net_co2e_removed_kg",
                "gross_sequestration": "gross_sequestration_kg",
                "total_activities": "total_activities_kg",
                "total_adjustments": "total_adjustments_kg",
                "uncertainty_discount": "uncertainty_discount_kg",
            }
            for src_col, dst_key in field_map.items():
                v = row[src_col]
                if v != "" and dst_key not in meta:
                    meta[dst_key] = float(v) * 1000
    return leaves, removal_meta


# ---------------------------------------------------------------------------
# Load file B (summary rows inline, 5 per removal, branch == "SUMMARY")
# ---------------------------------------------------------------------------
def load_B():
    leaves = []
    removal_meta = {}
    summary_name_map = {
        "Gross sequestration": "gross_sequestration_kg",
        "Net CO2e removed": "net_co2e_removed_kg",
        "Total activities": "total_activities_kg",
        "Total adjustments": "total_adjustments_kg",
        "Uncertainty discount": "uncertainty_discount_kg",
    }
    with open(FILE_B, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            period = row["statement_period"]
            rid = row["removal_id"]
            unit = row["unit"]
            val = float(row["value"])
            if unit.lower() == "kg":
                val_kg = val
            else:  # "t" or "tCO2e"/"tCO₂e"
                val_kg = val * 1000
            key = (period, rid)
            if row["branch"] == "SUMMARY":
                removal_meta.setdefault(key, {})
                field = summary_name_map[row["leaf_line_name"]]
                removal_meta[key][field] = val_kg
            else:
                leaves.append({
                    "period": period, "statement_id": row["statement_id"], "removal_id": rid,
                    "oil_type": row["oil_type"], "branch": row["branch"], "line": row["leaf_line_name"],
                    "value_kg": val_kg, "unit_raw": unit,
                })
    return leaves, removal_meta


leaves_A, meta_A = load_A()
leaves_B, meta_B = load_B()
all_leaves = leaves_A + leaves_B
all_meta = {}
all_meta.update(meta_A)
all_meta.update(meta_B)

# ---------------------------------------------------------------------------
# Reconciliation: per removal, sum of Activities leaf rows == total_activities;
# sum of Adjustments leaf rows == total_adjustments (within 0.5%)
#
# Two removals (MAR rmv_1KMR8D9XN1S0EHVH, APR rmv_1KRH4CXAP1S0M44D) have every
# one of gross_sequestration/total_activities/total_adjustments/uncertainty_
# discount blank in the source export because their Certify calc-view tab
# capture failed. Their raw components-tab captures (raw/rmv_..._components_
# 2026-09-28.txt) DO carry every leaf line plus the removal-level net figure
# ("REMOVAL n.nn tCO2e"), which matches the net_co2e_removed already present
# in the CSV for both (25.77 / 18.98) -- so net is not re-derived. For these
# two only, the missing branch totals are taken as the leaf-row sums
# themselves (status "DERIVED FROM LEAF SUMS"), per Max's all-system-
# sensitivity instruction: no removal is dropped.
# ---------------------------------------------------------------------------
DERIVED_TOTALS_REMOVALS = {
    ("MAR", "rmv_1KMR8D9XN1S0EHVH"),
    ("APR", "rmv_1KRH4CXAP1S0M44D"),
}

recon_rows = []
recon_fail = False
sums_by_removal = defaultdict(lambda: defaultdict(float))
for leaf in all_leaves:
    key = (leaf["period"], leaf["removal_id"])
    sums_by_removal[key][leaf["branch"]] += leaf["value_kg"]

for key, meta in all_meta.items():
    period, rid = key
    act_sum = sums_by_removal[key].get("Activities", 0.0)
    adj_sum = sums_by_removal[key].get("Adjustments", 0.0)
    seq_sum = sums_by_removal[key].get("Sequestrations", 0.0)

    if key in DERIVED_TOTALS_REMOVALS:
        # Fill the blank stated totals from the leaf-row sums (confirmed
        # against the components-tab capture: Mitigated = adjustments + gross
        # sequestration; Emitted = activities; both tie out exactly).
        meta.setdefault("total_activities_kg", act_sum)
        meta.setdefault("total_adjustments_kg", adj_sum)
        meta.setdefault("gross_sequestration_kg", seq_sum)
        act_stated = act_sum
        adj_stated = adj_sum
        recon_rows.append({
            "period": period, "removal_id": rid,
            "activities_sum_kg": round(act_sum, 3), "activities_stated_kg": round(act_stated, 3),
            "activities_diff_pct": 0.0,
            "adjustments_sum_kg": round(adj_sum, 3), "adjustments_stated_kg": round(adj_stated, 3),
            "adjustments_diff_pct": 0.0,
            "net_removed_kg": round(meta.get("net_co2e_removed_kg", 0.0), 3),
            "status": "DERIVED FROM LEAF SUMS (calc-view capture failed; net taken from "
                      "components-tab capture, matches CSV net_co2e_removed)",
        })
        continue

    act_stated = meta.get("total_activities_kg", 0.0)
    adj_stated = meta.get("total_adjustments_kg", 0.0)

    def pct_diff(a, b):
        base = abs(b) if abs(b) > 1e-9 else (abs(a) if abs(a) > 1e-9 else 1.0)
        return abs(a - b) / base * 100.0

    act_diff = pct_diff(act_sum, act_stated)
    adj_diff = pct_diff(adj_sum, adj_stated)
    status = "OK" if act_diff <= 0.5 and adj_diff <= 0.5 else "MISMATCH >0.5%"
    if status != "OK":
        recon_fail = True
    recon_rows.append({
        "period": period, "removal_id": rid,
        "activities_sum_kg": round(act_sum, 3), "activities_stated_kg": round(act_stated, 3),
        "activities_diff_pct": round(act_diff, 3),
        "adjustments_sum_kg": round(adj_sum, 3), "adjustments_stated_kg": round(adj_stated, 3),
        "adjustments_diff_pct": round(adj_diff, 3),
        "net_removed_kg": round(meta.get("net_co2e_removed_kg", 0.0), 3),
        "status": status,
    })

excluded_removals = set()  # all-system sensitivity analysis: no removal is excluded
if recon_fail:
    print("RECONCILIATION MISMATCHES >0.5%% found (informational only; no removal excluded):")
    for r in recon_rows:
        if r["status"] != "OK" and "DERIVED" not in r["status"]:
            print(" ", r)

# ---------------------------------------------------------------------------
# Build line_category_map.csv (one row per distinct leaf-line name)
# ---------------------------------------------------------------------------
distinct_names = sorted({leaf["line"] for leaf in all_leaves})
line_map = OrderedDict()
for name in distinct_names:
    cat, reason, est_flag, sub = categorize(name)
    line_map[name] = {"category": cat, "reason": reason, "establishment_flag": est_flag, "subcategory": sub}

with open(FOLDER / "line_category_map.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["leaf_line_name", "category", "establishment_flag", "subcategory", "reason"])
    for name, d in line_map.items():
        w.writerow([name, d["category"], d["establishment_flag"], d["subcategory"], d["reason"]])

# ---------------------------------------------------------------------------
# Attach category to each leaf row (excluding excluded removals & Adjustments)
# ---------------------------------------------------------------------------
for leaf in all_leaves:
    leaf["category"] = line_map[leaf["line"]]["category"]
    leaf["subcategory"] = line_map[leaf["line"]]["subcategory"]

# Net removed per period (sum of removals' net, excluding reconciliation-failed removals)
net_removed_by_period = defaultdict(float)
net_removed_total = 0.0
removals_used = []
for key, meta in all_meta.items():
    if key in excluded_removals:
        continue
    period, rid = key
    net_removed_by_period[period] += meta.get("net_co2e_removed_kg", 0.0)
    net_removed_total += meta.get("net_co2e_removed_kg", 0.0)
    removals_used.append(key)

# Adjustments total per period (reductions, reported separately, not in materiality)
adjustments_by_period = defaultdict(float)
for key, meta in all_meta.items():
    if key in excluded_removals:
        continue
    period, rid = key
    adjustments_by_period[period] += meta.get("total_adjustments_kg", 0.0)

# Category emissions per period (Activities branch only; excluded removals dropped)
cat_by_period = defaultdict(lambda: defaultdict(float))  # [period][category] = kg
family_by_period = defaultdict(lambda: defaultdict(float))  # [period][line_name] = kg
subcat_by_period = defaultdict(lambda: defaultdict(float))  # [period][subcategory] = kg (waste disposal etc.)

for leaf in all_leaves:
    key = (leaf["period"], leaf["removal_id"])
    if key in excluded_removals:
        continue
    if leaf["branch"] != "Activities":
        continue
    cat_by_period[leaf["period"]][leaf["category"]] += leaf["value_kg"]
    family_by_period[leaf["period"]][leaf["line"]] += leaf["value_kg"]
    if leaf["subcategory"]:
        subcat_by_period[leaf["period"]][leaf["subcategory"]] += leaf["value_kg"]

def agg_over_periods(dct, periods):
    out = defaultdict(float)
    for p in periods:
        for k, v in dct.get(p, {}).items():
            out[k] += v
    return out

cat_agg_all = agg_over_periods(cat_by_period, PERIOD_ORDER)
cat_agg_last6 = agg_over_periods(cat_by_period, LAST_6)
fam_agg_all = agg_over_periods(family_by_period, PERIOD_ORDER)
fam_agg_last6 = agg_over_periods(family_by_period, LAST_6)
subcat_agg_all = agg_over_periods(subcat_by_period, PERIOD_ORDER)
subcat_agg_last6 = agg_over_periods(subcat_by_period, LAST_6)

net_all = sum(net_removed_by_period[p] for p in PERIOD_ORDER)
net_last6 = sum(net_removed_by_period[p] for p in LAST_6)

def M(cat_kg, net_kg):
    return (cat_kg / net_kg * 100.0) if net_kg else 0.0

def M_per_period(name_dict_by_period, name, net_dict):
    out = {}
    for p in PERIOD_ORDER:
        cat_kg = name_dict_by_period.get(p, {}).get(name, 0.0)
        net_kg = net_dict.get(p, 0.0)
        out[p] = M(cat_kg, net_kg)
    return out

# categories present in data
cats_present = sorted(set(list(cat_agg_all.keys()) + list(cat_agg_last6.keys())),
                       key=lambda c: ALL_CATS.index(c) if c in ALL_CATS else 999)

summary_rows = []
flagged_categories = []
for cat in cats_present:
    agg_kg = cat_agg_all.get(cat, 0.0)
    agg_t = agg_kg / 1000.0
    m_agg = M(agg_kg, net_all)
    m_last6 = M(cat_agg_last6.get(cat, 0.0), net_last6)
    per_period_m = M_per_period(cat_by_period, cat, net_removed_by_period)
    under_1_all_periods = all(per_period_m[p] < 1.0 for p in PERIOD_ORDER if net_removed_by_period[p] > 0)
    flag = (m_agg < 1.0) and under_1_all_periods
    summary_rows.append({
        "category": cat, "aggregate_t": round(agg_t, 3), "aggregate_pct": round(m_agg, 4),
        "last6_pct": round(m_last6, 4), "flag_under_1pct": "FLAG (<1% all periods & aggregate)" if flag else "",
    })
    if flag:
        flagged_categories.append((cat, agg_kg))

# Collective flagged total
collective_flagged_kg = sum(kg for _, kg in flagged_categories)
collective_flagged_pct = M(collective_flagged_kg, net_all)
reinstated = []
if collective_flagged_pct >= 1.0:
    # reinstate largest-first until collective < 1%
    remaining = sorted(flagged_categories, key=lambda x: -x[1])
    running_excluded = list(remaining)
    while running_excluded:
        total_kg = sum(kg for _, kg in running_excluded)
        if M(total_kg, net_all) < 1.0:
            break
        biggest = running_excluded.pop(0)
        reinstated.append(biggest[0])

# ---------------------------------------------------------------------------
# By_Line_Family (group spelling variants) -- group by normalized key
# ---------------------------------------------------------------------------
def normalize_family(name: str) -> str:
    n = name.lower()
    n = re.sub(r"[-_:]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    # strip embodied/process suffixes to group family
    n = re.sub(r"\b(embodied|process)\s+emissions?\b", "", n).strip()
    n = re.sub(r"\bemissions?\b", "", n).strip()
    n = re.sub(r"\bqowv\b|\bwodo\b", "", n).strip()
    n = re.sub(r"\s+", " ", n).strip()
    return n

family_group = defaultdict(set)
for name in distinct_names:
    family_group[normalize_family(name)].add(name)

family_rows = []
for fam_key, variants in family_group.items():
    agg_kg = sum(fam_agg_all.get(v, 0.0) for v in variants)
    if agg_kg == 0.0:
        continue
    last6_kg = sum(fam_agg_last6.get(v, 0.0) for v in variants)
    m_agg = M(agg_kg, net_all)
    m_last6 = M(last6_kg, net_last6)
    under_1_all_periods = True
    for p in PERIOD_ORDER:
        net_kg = net_removed_by_period.get(p, 0.0)
        if net_kg <= 0:
            continue
        fam_kg_p = sum(family_by_period.get(p, {}).get(v, 0.0) for v in variants)
        if M(fam_kg_p, net_kg) >= 1.0:
            under_1_all_periods = False
            break
    flag = (m_agg < 1.0) and under_1_all_periods
    family_rows.append({
        "family": fam_key, "variants": "; ".join(sorted(variants)),
        "aggregate_t": round(agg_kg / 1000.0, 3), "aggregate_pct": round(m_agg, 4),
        "last6_pct": round(m_last6, 4),
        "flag_under_1pct": "FLAG (<1% all periods & aggregate)" if flag else "",
    })
family_rows.sort(key=lambda r: -r["aggregate_t"])

# Collective flagged total across line families (largest-first reinstatement if >=1%)
flagged_family_amounts = [(r["family"], r["aggregate_t"] * 1000.0) for r in family_rows if r["flag_under_1pct"]]
collective_flagged_family_kg = sum(kg for _, kg in flagged_family_amounts)
collective_flagged_family_pct = M(collective_flagged_family_kg, net_all)
reinstated_families = []
if collective_flagged_family_pct >= 1.0:
    running = sorted(flagged_family_amounts, key=lambda x: -x[1])
    while running:
        total_kg = sum(kg for _, kg in running)
        if M(total_kg, net_all) < 1.0:
            break
        reinstated_families.append(running.pop(0)[0])

# waste disposal subcategory
waste_agg_kg = subcat_agg_all.get("waste disposal", 0.0)
waste_m_agg = M(waste_agg_kg, net_all)
waste_m_last6 = M(subcat_agg_last6.get("waste disposal", 0.0), net_last6)

# ---------------------------------------------------------------------------
# Kansas periods
# ---------------------------------------------------------------------------
kansas_periods = []
kansas_transit_only_periods = []
for p in PERIOD_ORDER:
    names_in_period = {leaf["line"] for leaf in all_leaves if leaf["period"] == p}
    hits = [n for n in names_in_period if any(k in n for k in KANSAS_TOKENS)]
    if hits:
        kansas_periods.append(p)
        if all(is_kansas_transit_leg(n) or any(t in n for t in TRANSIT_LEG_NAMES) for n in hits):
            kansas_transit_only_periods.append((p, hits))

# ---------------------------------------------------------------------------
# By_Period matrix (category x period, t and %)
# ---------------------------------------------------------------------------
by_period_rows = []
for cat in cats_present:
    row_t = {"category": cat}
    row_pct = {"category": cat}
    for p in PERIOD_ORDER:
        kg = cat_by_period.get(p, {}).get(cat, 0.0)
        row_t[p] = round(kg / 1000.0, 3)
        row_pct[p] = round(M(kg, net_removed_by_period.get(p, 0.0)), 4)
    by_period_rows.append((row_t, row_pct))

print("=== SUMMARY (category | aggregate t | aggregate % | last-6 % | flag) ===")
for r in summary_rows:
    print(r["category"], r["aggregate_t"], r["aggregate_pct"], r["last6_pct"], r["flag_under_1pct"])
print(f"Collective flagged total: {collective_flagged_kg/1000:.3f} t, "
      f"{collective_flagged_pct:.4f}% of aggregate net removed ({net_all/1000:.3f} t)")
if reinstated:
    print("Reinstated (largest-first) to bring collective under 1%:", reinstated)
print(f"Collective flagged LINE-FAMILY total: {collective_flagged_family_kg/1000:.3f} t, "
      f"{collective_flagged_family_pct:.4f}% of aggregate net removed")
if reinstated_families:
    print("Reinstated families (largest-first) to bring collective under 1%:", reinstated_families)
print("Kansas-token periods:", kansas_periods)
print("Kansas-token periods that are transit-leg-only (not a KS facility op):", kansas_transit_only_periods)

# ===========================================================================
# BUILD WORKBOOK
# ===========================================================================
wb = openpyxl.Workbook()
header_font = Font(bold=True)
header_fill = PatternFill("solid", fgColor=HEADER_FILL)

def style_header(ws, row=1, ncols=1):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

def autosize(ws):
    for col in ws.columns:
        length = max((len(str(c.value)) if c.value is not None else 0) for c in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(length + 2, 10), 60)

# --- Summary sheet ---
ws = wb.active
ws.title = "Summary"
headers = ["Category", "Aggregate (t CO2e)", "Aggregate M (%)", "Last-6-period M (%)", "Flag"]
ws.append(headers)
style_header(ws, ncols=len(headers))
for r in summary_rows:
    ws.append([r["category"], r["aggregate_t"], r["aggregate_pct"], r["last6_pct"], r["flag_under_1pct"]])
ws.append([])
ws.append(["Aggregate net CO2e removed (t)", round(net_all / 1000.0, 3)])
ws.append(["Last-6-period net CO2e removed (t)", round(net_last6 / 1000.0, 3)])
ws.append(["Collective total of flagged categories (t)", round(collective_flagged_kg / 1000.0, 3)])
ws.append(["Collective flagged M (%)", round(collective_flagged_pct, 4)])
ws.append(["Reinstated categories (largest-first) if collective >=1%", ", ".join(reinstated) if reinstated else "n/a - collective stayed under 1%"])
ws.append(["Collective total of flagged LINE FAMILIES (t)", round(collective_flagged_family_kg / 1000.0, 3)])
ws.append(["Collective flagged line-family M (%)", round(collective_flagged_family_pct, 4)])
ws.append(["Reinstated families (largest-first) if collective >=1%", ", ".join(reinstated_families) if reinstated_families else "n/a - collective stayed under 1%"])
ws.append(["Waste-disposal sub-category aggregate (t)", round(waste_agg_kg / 1000.0, 3)])
ws.append(["Waste-disposal sub-category aggregate M (%)", round(waste_m_agg, 4)])
ws.append(["Waste-disposal sub-category last-6 M (%)", round(waste_m_last6, 4)])
autosize(ws)

# --- By_Period sheet ---
ws2 = wb.create_sheet("By_Period")
ws2.append(["Category"] + [f"{p} (t)" for p in PERIOD_ORDER])
style_header(ws2, ncols=1 + len(PERIOD_ORDER))
for row_t, _ in by_period_rows:
    ws2.append([row_t["category"]] + [row_t[p] for p in PERIOD_ORDER])
ws2.append([])
hdr_row = ws2.max_row + 1
ws2.append(["Category"] + [f"{p} (M%)" for p in PERIOD_ORDER])
style_header(ws2, row=hdr_row, ncols=1 + len(PERIOD_ORDER))
for _, row_pct in by_period_rows:
    ws2.append([row_pct["category"]] + [row_pct[p] for p in PERIOD_ORDER])
ws2.append([])
ws2.append(["Net CO2e removed (t)"] + [round(net_removed_by_period.get(p, 0.0) / 1000.0, 3) for p in PERIOD_ORDER])
autosize(ws2)

# --- By_Line_Family sheet ---
ws3 = wb.create_sheet("By_Line_Family")
headers = ["Line family (grouped)", "Variant spellings included", "Aggregate (t)", "Aggregate M (%)", "Last-6 M (%)", "Flag"]
ws3.append(headers)
style_header(ws3, ncols=len(headers))
for r in family_rows:
    ws3.append([r["family"], r["variants"], r["aggregate_t"], r["aggregate_pct"], r["last6_pct"], r["flag_under_1pct"]])
autosize(ws3)

# --- Line_Map sheet ---
ws4 = wb.create_sheet("Line_Map")
headers = ["Leaf line name", "Table 1 category", "Establishment?", "Subcategory", "Reason"]
ws4.append(headers)
style_header(ws4, ncols=len(headers))
for name, d in line_map.items():
    ws4.append([name, d["category"], d["establishment_flag"], d["subcategory"], d["reason"]])
autosize(ws4)

# --- Reconciliation sheet ---
ws5 = wb.create_sheet("Reconciliation")
headers = ["Period", "Removal ID", "Activities sum (kg)", "Activities stated (kg)", "Activities diff %",
           "Adjustments sum (kg)", "Adjustments stated (kg)", "Adjustments diff %", "Net removed (kg)", "Status"]
ws5.append(headers)
style_header(ws5, ncols=len(headers))
for r in recon_rows:
    ws5.append([r["period"], r["removal_id"], r["activities_sum_kg"], r["activities_stated_kg"],
                r["activities_diff_pct"], r["adjustments_sum_kg"], r["adjustments_stated_kg"],
                r["adjustments_diff_pct"], r["net_removed_kg"], r["status"]])
autosize(ws5)

# --- Adjustments sheet ---
ws6 = wb.create_sheet("Adjustments")
headers = ["Period", "Total adjustments (t)"]
ws6.append(headers)
style_header(ws6, ncols=len(headers))
adj_total_all = 0.0
for p in PERIOD_ORDER:
    t = adjustments_by_period.get(p, 0.0) / 1000.0
    ws6.append([p, round(t, 3)])
    adj_total_all += adjustments_by_period.get(p, 0.0)
ws6.append(["AGGREGATE (12 periods)", round(adj_total_all / 1000.0, 3)])
ws6.append(["LAST-6", round(sum(adjustments_by_period.get(p, 0.0) for p in LAST_6) / 1000.0, 3)])
autosize(ws6)

wb.save(FOLDER / "materiality_assessment.xlsx")
print("Saved materiality_assessment.xlsx")

# ===========================================================================
# BUILD MARKDOWN
# ===========================================================================
md = []
md.append("# Materiality assessment - Charm bio-oil GHG statements (12 periods, Aug 2025-Aug 2026)\n")

md.append("## Answer\n")

r_bp = next(r for r in summary_rows if r["category"] == "Bio-oil processing")
r_st = next(r for r in summary_rows if r["category"] == "Staff travel")
r_bi = next(r for r in summary_rows if r["category"] == "Bio-oil injection")
last6_sum = r_bp["last6_pct"] + r_st["last6_pct"]

md.append(f"**(a) Current basis - last 6 periods, Basco 6 only.** Two Table 1 categories are under 1% "
          f"individually: Bio-oil processing {r_bp['last6_pct']:.4f}% and Staff travel {r_st['last6_pct']:.4f}%. "
          f"Collective: {r_bp['last6_pct']:.4f}% + {r_st['last6_pct']:.4f}% = {last6_sum:.4f}%, which stays "
          f"under the 1% collective ceiling. Waste disposal alone is {waste_m_last6:.4f}%, but it sits inside "
          f"Bio-oil injection ({r_bi['last6_pct']:.4f}%), and the module states: \"The Materiality assessment "
          "should be undertaken for complete categories of SSRs, as defined in the relevant Protocol and set "
          "out in the system boundary, as they relate to a Reporting Period.\" At category grain, waste "
          "disposal cannot be excluded on its own - only the complete Bio-oil injection category counts, "
          "and that category is well above 1%.\n")

md.append(f"\n**(b) Full 12-period basis.** Only Bio-oil processing is under 1% in aggregate "
          f"({r_bp['aggregate_pct']:.4f}%). Staff travel is {r_st['aggregate_pct']:.4f}%; waste disposal is "
          f"{waste_m_agg:.4f}%.\n")

periods_bp_over = [p for p in PERIOD_ORDER if cat_by_period.get(p, {}).get("Bio-oil processing", 0.0)
                    and M(cat_by_period[p]["Bio-oil processing"], net_removed_by_period.get(p, 0.0)) >= 1.0]
periods_st_over = [p for p in PERIOD_ORDER if cat_by_period.get(p, {}).get("Staff travel", 0.0)
                    and M(cat_by_period[p]["Staff travel"], net_removed_by_period.get(p, 0.0)) >= 1.0]
md.append(f"\n**(c) Per-period volatility.** Bio-oil processing exceeds 1% in: "
          f"{', '.join(periods_bp_over) if periods_bp_over else 'no period'}. Staff travel exceeds 1% in: "
          f"{', '.join(periods_st_over) if periods_st_over else 'no period'}. In the 07 Nov 2025-31 Jan 2026 "
          f"period, net CO2e removed was only {net_removed_by_period.get('07 Nov 2025 to 31 Jan 2026', 0.0)/1000:.3f} t "
          "- the smallest of the 12 periods - so every category's M spikes in that period purely from the "
          "small denominator.\n")

md.append("\n**(d)** The module ties the Materiality assessment to \"a Reporting Period\" and requires "
          "Project Proponents to \"repeat the Materiality Assessment when any of the following occur: The "
          "previous assessment was conducted one year or more prior to the current verification; There has "
          "been a significant change in the Net Removal estimate; There has been a change in activities "
          "associated with any of the relevant SSRs.\" A fresh assessment for a current Reporting Period is "
          "what Isometric would test - not the Kansas-era history in periods further back.\n")

flagged_fam_names = [n for n, _ in flagged_family_amounts]
md.append(f"\n**Line families.** {len(flagged_fam_names)} of {len(family_rows)} leaf-line families are under "
          f"1% individually (aggregate and every period). Their collective total is "
          f"{collective_flagged_family_kg/1000:.3f} t CO2e, {collective_flagged_family_pct:.4f}% of aggregate "
          "net removed - over the 1% collective ceiling on its own. But per §5.0's complete-category rule "
          "quoted in (a), family-level exclusion isn't the test the module applies; categories are (full "
          "family list and figures on the By_Line_Family sheet).\n")

md.append("\n## Table 1 category materiality\n")
md.append("| Category | Aggregate (t CO2e) | Aggregate M (%) | Last-6 M (%) | Flag |")
md.append("|---|---:|---:|---:|---|")
for r in summary_rows:
    md.append(f"| {r['category']} | {r['aggregate_t']:.3f} | {r['aggregate_pct']:.4f} | {r['last6_pct']:.4f} | {r['flag_under_1pct']} |")

md.append(f"\nWaste-disposal sub-category (within Bio-oil injection): {waste_agg_kg/1000:.3f} t, "
          f"{waste_m_agg:.4f}% aggregate, {waste_m_last6:.4f}% last-6.\n")

md.append("\n## Kansas activity by period\n")
md.append(f"Periods with any line naming Kansas, KS, Vaulted or Hutchinson: {', '.join(kansas_periods) if kansas_periods else 'none'}.")
if kansas_transit_only_periods:
    md.append(" Of these, the following periods' only KS-token hits are transit legs passing through "
              "Kansas en route to Louisiana (e.g. \"CO->KS->LA\"), not a Kansas facility operation - "
              "the same distinction the task draws for SOPOR/Opelousas/Maize as Louisiana-bound rail legs:")
    for p, hits in kansas_transit_only_periods:
        md.append(f"\n- {p}: {'; '.join(sorted(hits))}")
md.append("\n")

md.append("\n## Method\n")
md.append("Both CSVs were normalized to one leaf-row table (period, statement/removal ID, branch, "
          "line name, value in kg CO2e - t values multiplied by 1,000, kg values left as-is) plus, "
          "per removal, net_co2e_removed / gross_sequestration / total_activities / total_adjustments "
          "(File B's per-removal totals come from its 5 inline SUMMARY rows per removal). Each of the "
          f"{len(distinct_names)} distinct leaf-line spellings across both files was mapped once to a "
          "Bio-oil Geological Storage protocol v1.2 Table 1 category (line_category_map.csv, one reason "
          "per row); Adjustments (BCU / Constant CO2 reduction) are reductions, not SSRs, and were excluded "
          "from the materiality sums and reported separately (Adjustments sheet). For each category and "
          "period, M_category = category Activities emissions / that period's net CO2e removed, per "
          "Module v1.1 Section 5.0.\n")

md.append("\n## Rule quoted (GHG Accounting Module v1.1, Section 5.0)\n")
md.append('> "An SSR may be excluded from the system boundary only where M SSR is < 1% individually '
          'and all excluded SSRs remain <1% collectively. Where the collective total exceeds 1%, the '
          'SSRs with the highest Materiality must be reinstated in the system boundary, in descending '
          'order, until the sum of SSRs becomes < 1%."\n')
md.append('> "The Materiality assessment should be undertaken for complete categories of SSRs, as '
          'defined in the relevant Protocol and set out in the system boundary, as they relate to a '
          'Reporting Period."\n')
md.append('> "Buffer pools should not be considered."\n')

md.append("\n## Reconciliation\n")
n_derived = sum(1 for r in recon_rows if "DERIVED" in r["status"])
n_mismatch = sum(1 for r in recon_rows if r["status"] not in ("OK",) and "DERIVED" not in r["status"])
md.append(f"All-system sensitivity analysis: every one of the {len(recon_rows)} removals is included; "
          "none is excluded.\n")
if n_mismatch == 0 and n_derived == 0:
    md.append(f"All {len(recon_rows)} removals reconciled within 0.5%: sum of Activities leaf rows "
              "matches the stated total_activities, and sum of Adjustments leaf rows matches the "
              "stated total_adjustments.\n")
else:
    if n_derived:
        md.append(f"{n_derived} removals (MAR rmv_1KMR8D9XN1S0EHVH, APR rmv_1KRH4CXAP1S0M44D) have "
                   "gross_sequestration/total_activities/total_adjustments/uncertainty_discount blank "
                   "in the leaf-row export because their Certify calc-view tab capture failed. Their "
                   "raw components-tab captures (raw/rmv_..._components_2026-09-28.txt) carry every "
                   "leaf line and the removal-level net figure directly (\"REMOVAL 25.77 tCO2e\" / "
                   "\"REMOVAL 18.98 tCO2e\"), matching the net_co2e_removed already in the CSV for "
                   "both - so net was taken as-is, not re-derived. total_activities and "
                   "total_adjustments were taken as the leaf-row sums themselves (status \"DERIVED "
                   "FROM LEAF SUMS\" on the Reconciliation sheet), confirmed against the components "
                   "capture's own Mitigated/Emitted subtotals:\n")
        for r in recon_rows:
            if "DERIVED" in r["status"]:
                md.append(f"- {r['period']} / {r['removal_id']}: total_activities = "
                           f"{r['activities_sum_kg']/1000:.3f} t (leaf sum), total_adjustments = "
                           f"{r['adjustments_sum_kg']/1000:.3f} t (leaf sum), net_co2e_removed = "
                           f"{r['net_removed_kg']/1000:.3f} t (from components-tab capture)\n")
    if n_mismatch:
        md.append(f"\n{n_mismatch} other removal(s) were off by more than 0.5% between the leaf-row "
                   "sum and the stated total (see Reconciliation sheet for the exact sums); none "
                   "excluded, per the all-system instruction:\n")
        for r in recon_rows:
            if r["status"] not in ("OK",) and "DERIVED" not in r["status"]:
                md.append(f"- {r['period']} / {r['removal_id']}: Activities diff {r['activities_diff_pct']}%, "
                           f"Adjustments diff {r['adjustments_diff_pct']}%\n")

with open(FOLDER / "materiality_assessment.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("Saved materiality_assessment.md")
