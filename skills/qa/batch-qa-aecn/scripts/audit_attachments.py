#!/usr/bin/env python3
"""
audit_attachments.py — STRUCTURAL evidence-attachment gate (all oil types).

Reconciling a value is NOT the same as confirming its required evidence is
attached/linked to the component in Certify. W1 (AECN) passed mass / pyrolysis /
transport on values that reconciled while the Ops Notes was never uploaded to
Certify. This gate makes that impossible to miss again, for every batch type that
runs audit_checklist.py.

Refuses to pass three ways:
  1. `certify.attachment_map` absent  -> FAIL (you cannot skip by not capturing).
  2. No required-evidence matrix for this batch -> FAIL (define it from the real
     batch's components; do NOT guess). A matrix is resolved from, in order:
        a) log['certify']['required_evidence']  (per-batch, built at QA time)
        b) MATRICES[oil_type]                   (registered after validation on a real batch)
  3. Any component missing a required source CATEGORY among its attached files -> FAIL.

`certify.attachment_map` = { "<datapoint/component name>": ["<attached source filename>", ...] }
captured from the Certify Sources tab (each source row lists its linked datapoint).

A matrix = { "<component-name substring>": ["<required category>", ...] }.

Run standalone:  python3 audit_attachments.py <source_reads.json>
Imported by audit_checklist.py so the standard pre-delivery audit enforces it.
"""
import json, re, sys
from pathlib import Path

# Filename patterns per source category (shared across oil types; extend as needed).
CATEGORY_PATTERNS = {
    # Added 2026-08-31 from INJ-08-2026-W4: individually-uploaded rail scale
    # tickets are also filed as "<RAILCAR>_LD<N>_FULL/EMPTY_<ticket#>.pdf"
    # (e.g. "SHPX215076_LD1_FULL_1124426227412.pdf") on batches where scale
    # tickets are uploaded to Certify Sources directly rather than only
    # Ops-Notes-hyperlinked.
    # Added 2026-09-17 from INJ-09-2026-W1: that week's Certify uploads are named
    # "Full_<RAILCAR>_offload_<N>.pdf" / "Empty_<RAILCAR>_offload_<N>.pdf" rather
    # than the "<RAILCAR>_LD<N>_FULL_<ticket#>.pdf" form used in August, so the
    # gate reported 16 attached tickets as missing.
    # Added 2026-10-06 from INJ-09-2026-W4-KERRY: Kerry tanker tickets are uploaded
    # as "Sept_W4_Full_Scale_Ticket_Kerry.jpg" (underscores), which "Scale Ticket"
    # (space) did not match, so the attached pair read as missing.
    "scale_ticket": r"Ticket_Rail|Ticket Rail|Scale[ _]Ticket|Weigh|_LD\d+_(FULL|EMPTY)_|^(Full|Empty)_[A-Za-z]+\d+_offload_\d+",
    # AECN inbound BOLs are filed either as "documents 2386-R.pdf" or bare
    # "2386-R.pdf" (the bare form is what INJ-07-2026-W1 uses), so match the
    # 4-digit + "-R" invoice number with or without a leading word.
    # Added 2026-09-30: direct-truck AECN BOLs are numbered "-T" and filed as
    # "Billing Documents 2505-T.pdf", which none of the other patterns matched.
    "bol":          r"[Cc]amion|\b\d{4}-[RT]\b|Bill of Lading|BOL",
    "ops_notes":    r"Ops Notes|INJ-\d{2}-\d{4}-W",
    "lab":          r"W1 AECN\.pdf|CoA|Certificate of Analysis|SR\d{2}-\d|SGS|CHARM INDUSTRIAL|WODO\.pdf|Aqueous\.pdf|QOWV\.pdf",
    "ef_sheet":     r"Standard Emission Factors|GLEC",
    # BCU / REC reductions are evidenced by the EAC retirement certificate.
    # Added 2026-08-06 from the first Aqueous batch, whose BCU component is the
    # only place a retirement certificate carries a datapoint.
    "eac_cert":     r"RetirementCertificate|Retirement Certificate|RD-EACs|EACs|BCU",
    # The AECN pyrolysis EMBODIED carbon intensity is evidenced by its own
    # derivation sheet ("AECN Embodied Emissions Calc Sheet"), not by the
    # process-side LCA workbooks — both are valid CI derivations.
    "lca":          r"LCA|Supporting GHG|Bioenergy AE|Cote-Nord|Embodied Emissions Calc Sheet",
    # "Distance" added 2026-08-06 from the first Kerry tanker batch, whose route
    # evidence is filed as "Kerry to Basco Distance.png" — a Google Maps capture
    # that none of the AECN-era route filename patterns matched.
    "map_or_watco": r"to SOPOR|Railyard to Basco|AECN to Basco|to B6|image \(44\)|Watco|Google Maps|Maps|Routing Map|Distance",
    "production_ci":r"Production Period|CI|Production Emissions|PP\d",   # Charm WODO/Aqueous
}

# Validated, real-batch matrices, keyed by oil type. AECN matrix validated on
# INJ-06-2026-W1. Kerry / WODO / Aqueous are intentionally absent — they must be
# defined from their first real batch (via log['certify']['required_evidence'])
# rather than guessed here.
MATRICES = {
    "AECN": {
        "Mass of Injectant":            ["scale_ticket", "ops_notes"],
        "Allocated Bio-Oil Mass":       ["scale_ticket", "bol", "ops_notes"],
        "Carbon Content":               ["lab"],
        "Carbon Intensity - AECN Pyrolysis": ["lca"],
        "Allocated Distance":           ["ops_notes", "map_or_watco"],
        "Distance from":                ["map_or_watco"],
        "Emissions Factor":             ["ef_sheet"],
        "Emission Factors":             ["ef_sheet"],
    },
    # WODO matrix validated on INJ-06-2026-W1 (weekly time-block, tote-based,
    # Production-Period CI folded into one pyrolysis component, flatbed transport).
    # Tote-based: no scale tickets / BOLs. Mass + distance-allocation basis is the
    # Ops Notes (which embeds the WODO Shipments & EE Allocation tab); CI evidenced
    # by Ops Notes per-PP CIs; lab CoA + Ops Notes copy on Carbon Content.
    "WODO": {
        "Mass of Injectant":                 ["ops_notes"],
        "Carbon Content of Bio-oil Injected": ["lab", "ops_notes"],
        "Transported CO to Basco":           ["ops_notes"],
        "WODO Tote - Carbon Intensity":      ["ops_notes"],
        "WODO Tote - Mass":                  ["ops_notes"],
        "Aggregate Distance":                ["ops_notes", "map_or_watco"],
        "Distance from":                     ["map_or_watco"],
        "Emissions Factor":                  ["ef_sheet"],
        # Added 2026-08-06 from INJ-07-2026-W2, the first WODO batch to carry a
        # BCU reduction at first delivery. Evidenced by the EAC retirement
        # certificate, same as the Aqueous matrix.
        "Constant CO":                       ["eac_cert"],
    },
    # Aqueous (QOWV) matrix validated on INJ-07-2026-W1-QOWV (2026-08-06) — the
    # deferred June-W2 Aqueous batch. Same weekly time-block, tote-based shape as
    # WODO: no scale tickets / BOLs, mass and distance-allocation basis is the Ops
    # Notes (which embeds the QOWV Shipments & EE Allocation tab), production CI
    # folded into one mass-weighted pyrolysis component evidenced by the Ops Notes,
    # lab CoA + Ops Notes copy on Carbon Content. Differs from WODO only in the
    # datapoint names (QOWV-prefixed) and in carrying a BCU reduction datapoint,
    # which is evidenced by the EAC retirement certificate.
    # Key must be UPPER CASE: the resolver at ~line 160 upper-cases log['oil_type']
    # before the lookup. Registered 2026-08-06 as "Aqueous", which never matched, so
    # every Aqueous batch silently fell through to its per-batch required_evidence.
    # Re-keyed to "AQUEOUS" 2026-09-22 on INJ-09-2026-W2-QOWV and re-validated against
    # that batch's live Certify sources.
    "AQUEOUS": {
        "Mass of Injectant":                           ["ops_notes"],
        "Carbon Content of Bio-oil Injected":          ["lab", "ops_notes"],
        "QOWV Transport Mass":                         ["ops_notes"],
        "QOWV Pyrolysis Mass":                         ["ops_notes"],
        "QOWV Pyrolysis Emissions - Carbon Intensity": ["ops_notes"],
        "QOWV Embodied Distance":                      ["ops_notes", "map_or_watco"],
        "Distance from":                               ["map_or_watco"],
        "Emissions Factor":                            ["ef_sheet"],
        "Constant CO":                                 ["eac_cert"],
    },
    # Kerry TANKER matrix, validated on INJ-07-2026-W4 (2026-08-06) — the first
    # Kerry batch delivered by flatbed-haul tanker rather than in totes. Shape is
    # closer to an AECN truck batch than to the earlier Kerry tote batches: one
    # full + empty CAT Scale ticket pair is the mass evidence, one composite SGS
    # sample carries carbon content, one Google Maps capture carries the route,
    # and a BCU reduction is evidenced by the EAC retirement certificate.
    #
    # Note the asymmetry between the two mass datapoints, which is deliberate:
    #   - "Allocated Kerry Oil Gross Mass" is the transported mass and IS fully
    #     derivable from the ticket pair alone (full minus empty), so tickets
    #     suffice.
    #   - "Mass of Injectant" is that figure LESS the Kerry-specific filtration
    #     loss (0.071% calciner solids). Neither the deduction nor the constant
    #     behind it appears on any scale ticket — both live only in the Ops
    #     Notes. Without the Ops Notes attached, a verifier reconciling the
    #     tickets lands on the gross mass and cannot explain the reported
    #     injectant mass. Hence ops_notes is required here.
    # If Kerry ever reverts to totes, do NOT reuse this matrix — the tote batches
    # have no scale tickets at all.
    "KERRY": {
        "Mass of Injectant":                  ["scale_ticket", "ops_notes"],
        "Allocated Kerry Oil Gross Mass":     ["scale_ticket"],
        "Carbon Content of Bio-oil Injected": ["lab"],
        "Route Distance":                     ["map_or_watco"],
        "Emissions Factor - Flatbed":         ["ef_sheet"],
        "Distance emission factor":           ["ef_sheet"],
        "Constant CO":                        ["eac_cert"],
        # Added 2026-10-06 from INJ-09-2026-W4-KERRY: Certify now names the EF and
        # BCU datapoints as below, which none of the three keys above matched, so
        # those datapoints went unchecked.
        "Emissions Factor - Truck Transport Fuel Use": ["ef_sheet"],
        "Emissions Factor - Vehicle Embodied Emissions": ["ef_sheet"],
        "BCUs Applied":                       ["eac_cert"],
    },
}


def _cat_present(files, category):
    pat = CATEGORY_PATTERNS.get(category)
    if pat is None:
        return False
    rx = re.compile(pat, re.IGNORECASE)
    return any(rx.search(f) for f in files)


def _resolve_matrix(log):
    cert = log.get("certify") or {}
    if isinstance(cert.get("required_evidence"), dict) and cert["required_evidence"]:
        return cert["required_evidence"], "log.certify.required_evidence"
    oil = (log.get("oil_type") or "").strip().upper()
    if oil in MATRICES:
        return MATRICES[oil], f"MATRICES[{oil}]"
    return None, None


def audit_attachments(log):
    """Return (ok, failures[list[str]])."""
    failures = []
    cert = log.get("certify") or {}
    amap = cert.get("attachment_map")
    if not amap or not isinstance(amap, dict):
        failures.append(
            "certify.attachment_map NOT CAPTURED — cannot verify required evidence is "
            "attached in Certify. Capture each datapoint's linked sources from the Certify "
            "Sources tab into certify.attachment_map, then re-run."
        )
    matrix, _src = _resolve_matrix(log)
    if matrix is None:
        oil = log.get("oil_type") or "?"
        failures.append(
            f"required-evidence matrix NOT DEFINED for oil_type='{oil}'. Build it from THIS "
            "batch's actual components (do not guess) and put it in log.certify.required_evidence "
            "(or register it in audit_attachments.MATRICES after validating on a real batch)."
        )
    if failures:  # cannot proceed to per-component checks without both inputs
        return False, failures

    for comp, required in matrix.items():
        matched = {k: v for k, v in amap.items() if comp.lower() in k.lower()}
        if not matched:
            continue  # component not present on this entry — not this gate's job
        for dp, files in matched.items():
            for cat in required:
                if not _cat_present(files, cat):
                    failures.append(
                        f"{dp}: required '{cat}' evidence NOT attached in Certify "
                        f"(attached: {len(files)} file(s), none matches {cat}). "
                        f"Per the evidence matrix this component requires {required}."
                    )
    return (len(failures) == 0), failures


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: audit_attachments.py <source_reads.json>", file=sys.stderr)
        return 2
    log = json.load(open(Path(argv[0])))
    ok, failures = audit_attachments(log)
    print(f"Attachment audit: {'PASS' if ok else 'FAIL'} ({len(failures)} gap(s)).")
    for f in failures:
        print(f"  - {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
