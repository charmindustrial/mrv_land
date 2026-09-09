"""Build the QA checklist for Kerry batch INJ-07-2026-W4 (tanker mode)."""
import sys

sys.path.insert(0, "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/skills/qa/batch-qa-kerry/templates")
from build_kerry_checklist import build_kerry_checklist

OUT = ("/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/"
       "batch-INJ-07-2026-W4-KERRY/Kerry_Batch_INJ-07-2026-W4_QA_Checklist.xlsx")

meta = {
    "batch_id": "INJ-07-2026-W4 (Kerry portion)",
    "reporting_period": "01 Jul 2026 - 31 Jul 2026 (injection week 19-25 Jul 2026)",
    "reviewer": "Claude QA Agent",
    "date": "2026-08-06",
    "injection_site": "Basco 6",
    "delivery_mode": "Tanker (flatbed-haul) - FIRST Kerry tanker batch",
    "certify_removal": "rmv_1KYZ3JPB51S0VE5Q  |  GHG statement ggs_1KZBX6AX41S029JS (DRAFT)",
}

F = {}

# ---------------------------------------------------------------- Section 1
F["1.1"] = {
    "status": "Pass",
    "evidence": (
        "Certify Carbon Content of Bio-oil Injected (per injection) is 52.8 %. SGS Certificate of "
        "Analysis SR26-04592.002, Client ID '07-2026-W4 Kerry', reports Carbon 52.8 % (m/m) by ASTM "
        "D5291 (Method C). Direct one-to-one match. No weighting is applicable: this batch is a single "
        "tanker with one composite sample (Ops Notes Composite Sample ID '07-2026-W4 Kerry'), not the "
        "multi-tote arrangement the April VVB Guidance weighted-average method was written for. "
        "[log:lab_results.carbon_pct_mm] [log:certify.components.Injection sequestration]"
    ),
    "ref": "SGS CoA SR26-04592.002; Certify Injection sequestration",
}
F["1.2"] = {
    "status": "Pass",
    "evidence": (
        "The Certify Sources tab links the carbon-content datapoint to 'W4 Kerry-AECN SGS COA.pdf' plus one "
        "further source (the Ops Notes, added 2026-08-10). Opened the CoA from Certify and read page 2 "
        "directly: Certificate SR26-04592.002, SGS Order 5482329, Location BASCO LOUISIANA, Sampled "
        "24-Jul-2026 08:00, Analysed 31-Jul-2026, signed by Jared Camardelle, Laboratory Supervisor. The "
        "sample date sits inside the 19-25 Jul injection week and the client ID names this batch. One "
        "shipment, one sample, one certificate - full coverage. "
        "[log:certify.certify_sources_enumeration] [log:lab_results]"
    ),
    "ref": "Certify Sources tab; SGS CoA SR26-04592.002 p.2",
}
F["1.3"] = {
    "status": "Pass",
    "evidence": (
        "Certify carries +/-0.2112 on the 52.8 % carbon content, read from the INPUTS section of the "
        "Injection sequestration modal. Expected value is 0.004 x measured, i.e. 0.004 x 52.8 = 0.2112. "
        "Exact match. The Ops Notes Kerry tab independently records C Content Uncertainty 0.002112 "
        "against C Content 0.528 (same 0.4 % relative), and its Testing Uncertainty constant is 0.004. "
        "[log:uncertainty_verification.layer_2_correctness.carbon_content]"
    ),
    "ref": "Certify component modal INPUTS; Ops Notes Kerry tab",
}
F["1.4"] = {
    "status": "Pass",
    "evidence": (
        "Certify Mass of Injectant (per injection) is 16,725.66 kg. Ops Notes Kerry tab, 'Net Injected "
        "(kg) - MOBI' reads 16,725.66; the Summary tab Kerry row reads 16,725.66114. All three agree. "
        "[log:ops_notes.kerry_ledger_row.net_injected_kg_mobi] [log:ops_notes.summary_tab_kerry_row.mobi_kg]"
    ),
    "ref": "Certify Datapoints; Ops Notes Kerry + Summary tabs",
}
F["1.5"] = {
    "status": "Pass",
    "evidence": (
        "Recomputed from the tickets rather than from the sheet. Full 73,300 lb minus empty 36,400 lb is "
        "36,900 lb; 36,900 x 0.453592 kg/lb gives 16,737.54 kg, matching the Ops Notes Net Oil figure. "
        "Filtration loss applies the Kerry-specific calciner solids constant of 0.071 %: 16,737.54 x "
        "0.00071 equals 11.8836, entered as 11.88 kg. 16,737.54 minus 11.88 gives 16,725.66 kg MOBI. Both "
        "the constant and the deduction are now visible to a verifier: the Ops Notes was attached to this "
        "removal on 2026-08-10. Sparging Loss is 0.00 kg for Kerry on both the Kerry tab and the Summary "
        "tab, and the 1.29 % sparging constant is absent from the Kerry tab constants block - correct, "
        "Kerry enters the homogenisation tank un-sparged. [log:ops_notes] [log:ops_notes.filtration_check]"
    ),
    "ref": "CAT Scale tickets 4921 / 8165; Ops Notes Kerry tab constants",
}
F["1.6"] = {
    "status": "Pass",
    "evidence": (
        "Certify applies +/-72.57 kg to Mass of Injectant, read from the component modal INPUTS. That is the "
        "correct figure. Per-weighing precision follows the scale that did the weighing, not the oil type "
        "(Max, 2026-08-10): 2.5 lb / 1.13 kg is the precision of Charm's tote scale, and 72.57 kg is the "
        "precision of a commercial truck scale. This tanker was weighed on CAT Scale weighbridges - ticket "
        "4921 reads 'SCALE: 1895 / LOVES COUNTRY STORES ... WILSON TOWNSHIP WI' and ticket 8165 reads "
        "'SCALE: 1864 / LOVES US HWY 190 / PORT BARRE LA' - so the commercial-scale spec governs, exactly as "
        "it does for an AECN tanker. One discrete weighing event, so 1 x 72.57 kg. The Kerry skill reference "
        "previously carried 1.13 kg for tanker mode; it has been corrected to key off the scale rather than "
        "the oil type. [log:uncertainty_verification.layer_2_correctness.mass_of_injectant]"
    ),
    "ref": "Certify component modal INPUTS; CAT Scale tickets 4921 / 8165",
}
F["1.7"] = {
    "status": "Pass",
    "evidence": (
        "Re-checked 2026-08-10. The Mass of Injectant datapoint now carries three sources: "
        "'INJ-07-2026-W4 Ops Notes.xlsx', 'W4 Kerry CAT Scale Ticket 4921 FULL.jpg' and "
        "'W4 Kerry CAT Scale Ticket 8165 EMPTY.jpg' (Sources tab now shows 8 sources, up from 6). The chain "
        "closes end to end on attached evidence: the tickets, both downloaded and read at pixel level, give "
        "73,300 lb and 36,400 lb with axle weights summing exactly to each stated gross and the same tractor "
        "07 / trailer 1013 on both, i.e. 36,900 lb = 16,737.54 kg; the Ops Notes then carries the 0.071 % "
        "calciner solids constant and the resulting 11.88 kg filtration deduction down to the reported "
        "16,725.66 kg. Both ticket dates fall within 14 days of the 25 Jul injection. Remaining open "
        "question, not a defect: no Bill of Lading or other origin-side document exists in the Drive folder "
        "or Certify Sources, so the conservative MIN(scale-ticket net, origin BOL mass) test has no second "
        "leg - Kerry tote shipments carry no BOL, and Garrett should confirm whether a tanker shipment "
        "generates one. [log:scale_tickets] [log:bol] [log:certify.attachment_map]"
    ),
    "ref": "Certify Sources tab (8 sources); CAT Scale tickets 4921 / 8165; INJ-07-2026-W4 Ops Notes.xlsx",
}

# --------------------------------------------------------------- Section 2A
F["2A.1"] = {
    "status": "Pass",
    "evidence": (
        "Certify uses 0.1384 kgCO2e/(t.mi). Read the live Standard Emission Factors sheet, 2026 tab, this "
        "session: 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck | MT CO2e/t-mi | 0.0001384 | "
        "0 | 0.0001384 | GLEC V3.2 2025 | ISOMETRIC'. 0.0001384 MTCO2e/t-mi is 0.1384 kgCO2e/(t.mi) - "
        "exact match to the current tab. Superseded values on older tabs are 0.1367939 (GLEC V3.0) and "
        "0.135156 (GLEC V3.0 2024); neither is in use here. "
        "[log:emission_factors.flatbed_process]"
    ),
    "ref": "Standard EFs sheet 2026 tab (GLEC V3.2 2025)",
}
F["2A.2"] = {
    "status": "Pass",
    "evidence": (
        "Re-checked 2026-08-10. This datapoint now cites 'Standard Emission Factors + Calculations (8).xlsx' "
        "in place of the superseded 'Truck and Trailer EE 2025.pdf'. Opened the new source in Certify: it is "
        "the full Standard Emission Factors workbook, with its '2026' tab active and the 2025 equivalents "
        "carried as hidden tabs. That is the tab I verified the 0.1384 kgCO2e/(t.mi) figure against in the "
        "live workbook, so the evidence now matches the reported value. Scope note: Certify renders this "
        "file as a limited preview, so I confirmed the workbook identity and its tab structure in Certify "
        "and the value itself in the live source workbook, rather than reading the cell inside the uploaded "
        "copy. [log:emission_factors.flatbed_process]"
    ),
    "ref": "Certify Sources: Standard Emission Factors + Calculations (8).xlsx, 2026 tab",
}
F["2A.3"] = {
    "status": "Pass",
    "evidence": (
        "Certify Route Distance Kerry to Basco is 1,090 mi. The attached Google Maps evidence runs 4343 Expo "
        "Dr, Manitowoc, WI 54220 to 4687 LA-115, St Landry, LA 71367 and offers three routes: 1,059 mi via "
        "I-57 S, 1,071 mi via I-57 S and US-165 S, and 1,090 mi via I-55 S. Certify uses 1,090 - the longest "
        "of the three, matching Charm's convention of taking the longest Google Maps distance (which is why "
        "no uncertainty is carried on distance). The Wisconsin origin agrees with where the tickets were "
        "weighed, and the St Landry destination agrees with the Port Barre LA empty weigh. "
        "[log:distance_evidence]"
    ),
    "ref": "Certify Datapoints; Kerry to Basco Distance.png",
}
F["2A.4"] = {
    "status": "Pass",
    "evidence": (
        "'Kerry to Basco Distance.png' is attached to the distance datapoint and is the one source marked "
        "PUBLIC on the Sources tab. Downloaded it from Certify and read the image directly: the 1,090 mi / "
        "16 hr 49 min via I-55 S route is visible on the map and in the route list, with both endpoint "
        "addresses shown in the entry fields. Evidence value confirms the reported value. "
        "[log:distance_evidence.routes_offered]"
    ),
    "ref": "Certify Sources: Kerry to Basco Distance.png (read as image)",
}
F["2A.5"] = {
    "status": "Pass",
    "evidence": (
        "Certify 'Allocated Kerry Oil Gross Mass' is 16,737.54 kg. The Ops Notes Kerry tab column 'Gross "
        "Mass (kg) - transport' reads 16,737.54, and the Summary tab Kerry row 'Mass Used (kg)' reads the "
        "same. The basis is correct: the transport factor is applied to the pre-filtration mass actually "
        "hauled (16,737.54 kg), not to the post-filtration MOBI of 16,725.66 kg. Using MOBI here would "
        "under-report transport emissions. [log:certify.components.Kerry to Basco Flatbed Truck Transport "
        "Process Emissions.mass_basis_check]"
    ),
    "ref": "Certify Datapoints; Ops Notes Kerry tab col E, Summary tab",
}
F["2A.6"] = {
    "status": "Pass",
    "evidence": (
        "Recomputed independently: 73,300 lb less 36,400 lb is 36,900 lb; 36,900 x 0.453592 gives "
        "16,737.54 kg. Matches the Ops Notes figure to the cent. The conversion constant used is the one "
        "declared in the Kerry tab constants block (Kg/Lbs 0.453592). Component output checks out too: "
        "16.73754 t x 1,090 mi x 0.1384 kgCO2e/(t.mi) equals 2,524.96 kg, i.e. the 2.525 tCO2e Certify "
        "reports. [log:scale_tickets.net_derivation] [log:emission_factors.flatbed_process]"
    ),
    "ref": "CAT Scale tickets 4921 / 8165; Ops Notes Kerry tab constants",
}
F["2A.7"] = {
    "status": "Pass",
    "evidence": (
        "Certify applies +/-72.57 kg to Allocated Kerry Oil Gross Mass, read from the Transport Process "
        "modal INPUTS. Correct on the same basis as item 1.6: the precision follows the commercial truck "
        "scale that weighed the tanker, not the oil type, and one weighing event gives 1 x 72.57 kg. "
        "[log:uncertainty_verification.layer_2_correctness.mass_of_load]"
    ),
    "ref": "Certify component modal INPUTS; CAT Scale tickets 4921 / 8165",
}

# --------------------------------------------------------------- Section 2B
F["2B.1"] = {
    "status": "Pass",
    "evidence": (
        "Certify uses 0.11979 kgCO2e/km. Read the live Standard Emission Factors sheet, 2026 tab: "
        "'Vehicle Embodied Emissions --Non-Tanker Truck | MT CO2e/mi | 0.0001927908256 | 0 | 0.0001928 | "
        "GLEC V3.2 2025'. Converting, 0.1927908256 kgCO2e/mi divided by 1.60934 km/mi gives 0.1197824 "
        "kgCO2e/km, matching the 0.11979 shown. This is the current value; the 0.0401 kgCO2e/km figure that "
        "failed on Kerry batch K-002 derives from the superseded GREET 2024 basis, whereas Certify "
        "reports 0.11979 here. Non-tanker (flatbed) is the right vehicle class for a Kerry flatbed "
        "haul. The value is sound; it is the attached evidence that is stale, which is item 2B.2. "
        "[log:emission_factors.non_tanker_embodied]"
    ),
    "ref": "Standard EFs sheet 2026 tab (GLEC V3.2 2025)",
}
F["2B.2"] = {
    "status": "Fail",
    "evidence": (
        "Still open as of 2026-08-10 - Max has fixed the process-side factor (item 2A.2) but reports this "
        "datapoint is locked and is awaiting technical assistance. The Distance emission factor still cites "
        "'Standard Emission Factors + Calculations - Truck and Trailer EE 2025.pdf' as its only source. I "
        "read that document in full: one page, headed 'GREET 2024 Values', whose non-tanker result lines "
        "read 'Non- Tanker Truck Total Embodied Emissions (MTCO2e)/Mile w/ Deadhead  0.0000644927' and "
        "'Converted to kgCO2e/km  0.04007398255' - against the 0.11979 kgCO2e/km reported in Certify. The "
        "reported value is correct (see 2B.1); the evidence behind it is the superseded vintage. Useful for "
        "unblocking: the replacement derivation is already on this removal. The workbook attached on "
        "2026-08-10 for the process factor, 'Standard Emission Factors + Calculations (8).xlsx', contains a "
        "'Truck and Trailer EE 2026' tab whose cell A1 reads 'GREET 2025 Values', with the same row "
        "structure as the old PDF down to 'Converted to MTCO2e/km'. Re-pointing this datapoint at that "
        "workbook should close the finding without needing a new document. "
        "[log:emission_factors.attached_evidence_document]"
    ),
    "ref": "Certify Sources: Truck and Trailer EE 2025.pdf (p.1); Standard Emission Factors + Calculations (8).xlsx, 'Truck and Trailer EE 2026' tab",
}
F["2B.3"] = {
    "status": "Pass",
    "evidence": (
        "The embodied component uses the same Route Distance Kerry to Basco datapoint, 1,090 mi, as the "
        "process component - one route, one distance, consistently applied. The modal shows no Mass of Load "
        "input, which is correct: the embodied factor is per-distance and mass-independent. Output checks "
        "out: 1,090 mi x 1.60934 km/mi gives 1,754.18 km; x 0.11979 kgCO2e/km gives 210.1 kg, i.e. the "
        "0.210 tCO2e reported. [log:certify.components.Kerry to Basco Flatbed Truck Transport Embodied "
        "Emissions]"
    ),
    "ref": "Certify Transport Embodied component modal",
}
F["2B.4"] = {
    "status": "Pass",
    "evidence": (
        "Same 'Kerry to Basco Distance.png' evidence as item 2A.4, opened and read directly from Certify. "
        "It shows the 1,090 mi Manitowoc WI to St Landry LA route, confirming the distance input to the "
        "embodied component. [log:distance_evidence]"
    ),
    "ref": "Certify Sources: Kerry to Basco Distance.png (read as image)",
}

# --------------------------------------------------------------- Section 2C
F["2C.1"] = {
    "status": "Pass",
    "evidence": (
        "The Constant CO2 reduction component carries 2,525 kgCO2e, read from its modal INPUTS. Transport "
        "process emissions are 2,524.96 kgCO2e. The BCU therefore equals-or-exceeds the process emission it "
        "offsets, satisfying the rule. Embodied emissions of 210 kg are correctly left un-offset - embodied "
        "is not BCU-eligible. Supporting source is the TERC Certificate of Retirement, read directly: 2,795 "
        "TERCs retired by Amazon.com Services LLC on behalf of Charm Industrial, Inc, dated Dec 18 2025, "
        "vintage 2024, Renewable Diesel TERCS, verified by Turner, Mason & Company, certificate "
        "TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000, on the stated basis that each TERC is one tCO2e "
        "reduced. 2,795 t comfortably supports the 2.525 t drawn here. Whether the pool is over-drawn "
        "across all removals is an inventory-level reconciliation outside a single batch. "
        "[log:bcu_evidence] [log:certify.components.Constant CO2 reduction.bcu_check]"
    ),
    "ref": "Certify Constant CO2 reduction modal; Charm-RetirementCertificate-RD-EACs-20251218.pdf",
}

# ---------------------------------------------------------------- Section 3
F["3.1"] = {
    "status": "Pass",
    "evidence": (
        "SGS CoA SR26-04592.002 reports Density at 15 C of 1.231 g/cm3 by ASTM D4052, read from the "
        "certificate page. That sits above the 1.01 g/cm3 formation-fluid floor with substantial margin, so "
        "the oil is denser than the formation fluid as injection requires. For context on the same "
        "certificate, the AECN sample (SR26-04592.001) reads 1.211 g/cm3 - the two oils sharing the "
        "homogenisation tank are closely matched on density. [log:lab_results.density_15C_g_cm3]"
    ),
    "ref": "SGS CoA SR26-04592.002, ASTM D4052",
}
F["3.2"] = {
    "status": "Pass",
    "evidence": (
        "Hydrogen 6.7 % (m/m) by ASTM D5291 (Method C), read from the certificate. Reported as required. No "
        "range test is applied: Kerry has no established baseline dataset, so there is no validated range to "
        "test against and inventing one would be worse than saying so. The result carries the SGS '#' "
        "qualifier - see sidebar S.4. AECN on the same certificate reads 7.1 %. "
        "[log:lab_results.hydrogen_pct_mm]"
    ),
    "ref": "SGS CoA SR26-04592.002, ASTM D5291",
}
F["3.3"] = {
    "status": "Pass",
    "evidence": (
        "Nitrogen reported as <0.75 % (m/m) by ASTM D5291 (Method C) - a below-detection-limit result, which "
        "is a reported value, not a gap. The AECN sample on the same certificate returns the same <0.75 %. "
        "No Kerry baseline range exists to test against. [log:lab_results.nitrogen_pct_mm]"
    ),
    "ref": "SGS CoA SR26-04592.002, ASTM D5291",
}
F["3.4"] = {
    "status": "Pass",
    "evidence": (
        "Kinematic Viscosity at 40 C reported as 7,074 cSt by ASTM D445, read from the certificate. Present "
        "as required. The magnitude is striking next to the AECN sample's 24.34 cSt on the same certificate "
        "- roughly 290 times more viscous - which is a handling observation rather than a reporting defect, "
        "so it is carried in the sidebar rather than scored here. [log:lab_results.kinematic_viscosity_40C_cSt]"
    ),
    "ref": "SGS CoA SR26-04592.002, ASTM D445",
}
F["3.5"] = {
    "status": "Pass",
    "evidence": (
        "Acid Number (Inflection end-point) reported as 67 mg KOH/g by ASTM D664 (Method A), with Titration "
        "Solvent Volume 60 mL recorded alongside it. Read from the certificate. AECN on the same certificate "
        "reads 66 mg KOH/g - the two oils are near-identical on acidity. [log:lab_results.acid_number_mgKOH_g]"
    ),
    "ref": "SGS CoA SR26-04592.002, ASTM D664",
}
F["3.6"] = {
    "status": "Fail",
    "evidence": (
        "Still open - re-verified 2026-08-10, with COBB showing 'Last updated 1 hour ago'. pH is recorded "
        "nowhere for this batch. The Ops Notes Kerry tab has a pH column and a constant reading "
        "'pH range (target)  2.0 - 4.0', but the cell on the single ledger row is empty, as is the Notes "
        "cell beside it. The COBB tracker is the only other place injection_ph lives, and it still holds no "
        "row for this batch: a query returning every Calciner row in the tracker comes back with K-001 and "
        "K-002 only, and a grouped count over July still returns INJ-07-2026-W1 alone. Kerry's incoming pH "
        "is not a formality - COBB records K-001 at injection_ph 13 against that same 2.0 - 4.0 target and "
        "K-002 at 2.9, so the reading moves batch to batch on this waste-derived stream. There is no record "
        "of the Kerry oil's own pH as received, which is the reading the Kerry tab's target range is written "
        "against. The AECN offloads injected the same week carry pH 2.90 on their own tab, but that is a "
        "different material and does not stand in for this one. "
        "[log:ops_notes] [log:ops_notes.kerry_ledger_row.ph] [log:cobb]"
    ),
    "ref": "Ops Notes Kerry tab col H; COBB 'Basco Injection -- COBB' tab",
}

SIDEBAR = [
    {
        "title": "COBB tracker has no row for this batch - and none for W2 or W3 either",
        "detail": (
            "Re-verified 2026-08-10, with the sheet showing 'Last updated 1 hour ago'. The "
            "'Basco Injection -- COBB' tab holds no INJ-07-2026-W4 row for Kerry or for AECN. Its only "
            "July entries are INJ-07-2026-W1_bio_oil (16 lots) and INJ-07-2026-W1_oily_fraction (17 lots); "
            "W2, W3 and W4 are all absent. The sheet banner reads 'Last updated 3 days ago'. Six independent "
            "query methods were run before concluding absence: a full Drive export, then gviz queries on "
            "'INJ-07-2026-W4', on 'INJ-07', on 'W4' or Kerry or kc_/KC_, on 'Calciner' or 'K-0', and a "
            "grouped count by batch. Every Kerry row in the entire tracker belongs to K-001 or K-002. "
            "Consequences: no kc_NNNN consumed lot has been assigned to this tanker, and injection pH has no "
            "second home (see item 3.6). This is a whole-batch entry lag rather than a Kerry-specific error, "
            "which is why it sits here and not as its own failed item - but the Kerry portion cannot be "
            "closed out in the tracker until it lands."
        ),
        "ref": "COBB 'Basco Injection -- COBB' tab",
    },
    {
        "title": "Ops Notes Kerry tab is still labelled for totes",
        "detail": (
            "The tab header reads 'BATCH HEADER - Kerry (Calciner Waste Oil, IBC Totes)' and its Section 1 is "
            "titled 'IBC LEDGER (one row per Kerry tote; tote tag mass is authoritative)'. This batch is a "
            "single flatbed-haul tanker - the one ledger row carries UID 'TANKER Freiburger 07/26' and the "
            "columns actually in use are Full Ticket (lb) and Empty Ticket 2 (lb). The numbers are right; the "
            "labels describe the previous delivery mode and will read as a contradiction to a verifier "
            "comparing the tab title against the scale tickets."
        ),
        "ref": "Ops Notes Kerry tab, rows 1 and 8",
    },
    {
        "title": "Three scale tickets exist, two were used - and the conservative one was chosen",
        "detail": (
            "Drive holds a third ticket, 3157, weighed empty at Racine WI on 7-12-26 at 36,380 lb before "
            "loading; it is deliberately named 'preload-reference-only' and is not uploaded to Certify. The "
            "tare actually used is ticket 8165, weighed at Port Barre LA on 7-17-26 after offload, at 36,400 "
            "lb. Charm took the heavier tare, which yields the lower net and under-credits by 20 lb (9.07 kg). "
            "That is the right call and worth keeping. What is missing is any written rule: the July VVB "
            "Guidance documents a standard-empty-weight method for AECN rail trailers but says nothing about "
            "which empty weighing governs a Kerry tanker. A one-paragraph note in the guidance doc would turn "
            "a filename convention into a documented method."
        ),
        "ref": "Kerry Scale Tickets folder; VVB Guidance Jul 1-31",
    },
    {
        "title": "Both carbon and hydrogen results carry the SGS out-of-range qualifier",
        "detail": (
            "On certificate SR26-04592, Carbon and Hydrogen on both samples - Kerry 52.8 / 6.7 and AECN 39.4 / "
            "7.1 - are marked '#', which the certificate footnote defines verbatim as 'Result is outside of "
            "test method limits and/or analytical range used in method precision study'. Carbon is the direct "
            "multiplier in the sequestration calculation, so this is worth surfacing: it is the laboratory's "
            "own statement that the ASTM D5291 precision study does not cover this result. It is not an error "
            "and the value is used as reported. I can only speak to this certificate - I have not reviewed "
            "whether the qualifier recurs across Charm's wider CoA history, and that would be the useful "
            "thing to establish before a verifier asks."
        ),
        "ref": "SGS CoA SR26-04592.001-002, footnote",
    },
    {
        "title": "Kerry is roughly 290 times more viscous than the AECN it is homogenised with",
        "detail": (
            "Kerry kinematic viscosity at 40 C is 7,074 cSt against AECN's 24.34 cSt on the same certificate, "
            "with the two oils sharing the homogenisation tank at Basco. Densities are close (1.231 vs 1.211 "
            "g/cm3) and acid numbers nearly identical (67 vs 66 mg KOH/g), so viscosity is the one parameter "
            "that diverges sharply. Recorded as an operational observation for Garrett - it has no bearing on "
            "the credit calculation."
        ),
        "ref": "SGS CoA SR26-04592.001-002, ASTM D445",
    },
    {
        "title": "Kerry uses its own filtration solids constant, and it is not the AECN one",
        "detail": (
            "The Kerry tab declares 'Filtration Solids Content (Kerry Calciner) 0.071%', where every other "
            "oil tab in the same workbook uses 0.00195 (0.195%). Applied here it yields 11.88 kg of "
            "filtration loss on 16,737.54 kg. The arithmetic is correct and the constant is clearly labelled "
            "as Kerry-specific. It is now visible to a verifier as well, since the Ops Notes was attached to "
            "the removal on 2026-08-10. Noting it because it is easy to mistake for an error when read next "
            "to the AECN tabs, and because the derivation of the 0.071% figure itself is not documented in "
            "the July VVB Guidance."
        ),
        "ref": "Ops Notes Kerry tab constants block",
    },
    {
        "title": "Kerry mass-uncertainty spec settled - it follows the scale, not the oil",
        "detail": (
            "Resolved by Max on 2026-08-10 and recorded here so it does not get re-litigated. Per-weighing "
            "precision is a property of the instrument, not of the oil type: 2.5 lb / 1.13 kg is Charm's "
            "tote scale, 72.57 kg is a commercial truck scale. Kerry in totes therefore gets 1.13 kg per "
            "tote; Kerry by tanker gets 72.57 kg, the same as an AECN tanker. The Kerry skill and its "
            "checklist reference previously said 1.13 kg for both modes and have been corrected, with the "
            "instruction to read the scale name off the ticket before choosing. Certify already had 72.57 "
            "kg on this batch and was right."
        ),
        "ref": "Max 2026-08-10; skills/qa/batch-qa-kerry/SKILL.md, Uncertainty Reference",
    },
    {
        "title": "Statement-level reporting-period emissions section is empty for July",
        "detail": (
            "Re-verified 2026-08-10. The July GHG statement's 'Reporting period emissions' tab still reads "
            "'No components / 0 components', "
            "and this removal carries no injection-site component either. Charm's documented practice is to "
            "hold site emissions as sub-components on a scapegoat removal rather than in this section, so an "
            "empty section is not by itself wrong - but I did not trace which of the statement's other eight "
            "entries carries them, because site-emissions accounting sits outside Kerry-batch scope and has "
            "its own QA. Raising it only so somebody confirms the July site emissions have a home before the "
            "statement leaves DRAFT."
        ),
        "ref": "Certify ggs_1KZBX6AX41S029JS, Reporting period emissions tab",
    },
    {
        "title": "BCU certificate is vintage 2024, retired Dec 2025, applied to a July 2026 injection",
        "detail": (
            "Stating the dates rather than a rule: the TERC certificate behind the 2.525 tCO2e reduction is "
            "vintage year 2024, retired 18 Dec 2025, and is drawn against an injection that took place 19-25 "
            "Jul 2026. I have not read the BCU eligibility criteria (Transportation Emissions Accounting "
            "v1.1, EC1-EC5) in this session, so I am not asserting that any vintage or timing requirement is "
            "or is not met - only surfacing the spread so it can be checked by whoever owns EAC eligibility. "
            "The quantity itself is sound: 2,795 t retired against 2.525 t drawn."
        ),
        "ref": "Charm-RetirementCertificate-RD-EACs-20251218.pdf",
    },
    {
        "title": "Certify sequestered range starts a day after the Ops Notes week",
        "detail": (
            "Certify records this removal as 19 Jul 2026 to 25 Jul 2026 while the Ops Notes declares the week "
            "as 7/18/2026 to 7/25/2026. The AECN removal for the same week (rmv_1KZBJBN9C1S0M5R5) carries the "
            "identical 19-25 Jul range, so the convention is applied consistently across the batch and nothing "
            "falls outside the July reporting period either way. Noted only because date-boundary questions "
            "come up in verification and it is cheaper to have the answer ready."
        ),
        "ref": "Certify removal header; Ops Notes Summary tab",
    },
]

res = build_kerry_checklist(OUT, meta, F, SIDEBAR, mode="tanker")
print("counts:", res["counts"])
print("out:", res["out_path"])
for k, v in res["item_status"].items():
    if v != "Pass":
        print(f"  {k}: {v}")
