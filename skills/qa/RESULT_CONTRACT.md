# QA Result Publication Contract

This document defines the canonical output shape for QA skills under `skills/qa/`. Every QA run (batch QA, site emissions QA) writes results conforming to this contract so downstream consumers (the operator's manual review today, a future Gaia UI tomorrow, BigQuery analytics in Q3+) can read them without coupling to skill internals.

## Where results land

Per QA run, write **all** of the following to a single destination folder:

| Artifact | Filename | Purpose |
|---|---|---|
| Human-readable checklist | `Batch_<ID>_QA_Checklist.xlsx` (batch QA) or `<RP>_Site_Emissions_QA_Checklist.xlsx` (site emissions) | What the operator opens |
| Machine-readable result | `Batch_<ID>_QA_Result.json` or `<RP>_Site_Emissions_QA_Result.json` | What downstream tooling consumes |
| Adversarial review notes | `Batch_<ID>_Adversarial_Review.md` | Audit trail of Gate 3 challenges |
| Source extraction log | `Batch_<ID>_Source_Reads.json` | Audit trail of Gate 1 reads |

**Destination:**
- **Batch QA:** the batch's Drive folder (the same folder containing scale tickets, Ops Notes, BOLs)
- **Site Emissions QA:** the RP's Site Emissions Drive folder (alongside the per-category subfolders)

If the operator passes an explicit output destination at QA initiation, use that. Otherwise default to the inferred Drive folder above.

Republish artifacts on each iteration (overwrite, don't accumulate `_v1`/`_v2` files in the folder). The JSON's `qa_run.iteration` counter tracks revision history; the registry's `iterations[]` array preserves prior runs if needed.

## JSON Schema — Batch QA Result

```json
{
  "schema_version": "1.0",
  "qa_type": "batch_aecn",                    // "batch_aecn" | "batch_wodo" | "site_emissions" | etc.
  "batch_id": "2-188",
  "removal_id": "rmv_1KXXX...",
  "supplier_reference_id": "ba_xxx",          // Certify supplier ref
  "reporting_period": "2026-04-01 to 2026-04-30",
  "oil_type": "AECN",                         // "AECN" | "WODO" | "QOWV" | "Kerry"
  "transport_mode": "truck",                  // "truck" | "rail" | "flatbed" | null
  "site": "Basco 6",                          // "Basco 6" | "Vaulted KS" | etc.

  "qa_run": {
    "iteration": 1,                           // 1 = initial, 2+ = re-runs after operator corrections
    "started_at": "2026-05-03T13:00:00Z",     // T0
    "completed_at": "2026-05-03T13:42:18Z",   // T4 (agent finished publishing)
    "agent_version": "qa-batch-aecn@1.0",
    "operator": "garrett.lutz@charmindustrial.com",
    "skill_path": "~/.claude/skills/qa/batch-qa/SKILL.md"
  },

  "summary": {
    "total_items": 47,
    "pass": 39,
    "fail": 2,
    "flag": 4,
    "na": 2,
    "is_submittable": false                   // true iff fail == 0 (flags allowed)
  },

  "sections": [
    {
      "section_id": "2",
      "title": "Scale Tickets & Mass Determination",
      "items": [
        {
          "id": "2.3",
          "description": "Tractor and trailer numbers match between empty and full tickets",
          "status": "FAIL",                   // PASS | FAIL | FLAG | N/A
          "evidence": "Full ticket TKT-12345.pdf shows tractor #4421, empty ticket TKT-12346.pdf shows tractor #4422. Mismatch.",
          "primary_sources": [
            {"type": "scale_ticket_pdf", "filename": "TKT-12345.pdf", "drive_url": "https://..."},
            {"type": "scale_ticket_pdf", "filename": "TKT-12346.pdf", "drive_url": "https://..."}
          ],
          "verifier_reference": "VR Sec 5.1",
          "fail_classification": "material",   // "material" | "non_material" | null (only set when status=FAIL)
          "expected_value": "tractor numbers match",
          "observed_value": "4421 vs 4422"
        }
      ]
    }
  ],

  "adversarial_review": {
    "ran_at": "2026-05-03T13:35:00Z",         // T3
    "challenged_items": [
      {"item_id": "5.4", "reason": "Evidence note cited COBB but did not name tab + row", "resolution": "Re-read COBB row 47 of Basco Injection -- COBB tab; updated evidence note"}
    ],
    "confirmed_items_count": 41,              // not the full list — just the count
    "review_notes_path": "Batch_2-188_Adversarial_Review.md"
  },

  "timestamps": {
    "T0_initiation": "2026-05-03T13:00:00Z",
    "T1_data_gathering_complete": "2026-05-03T13:18:45Z",
    "T2_checklist_draft_complete": "2026-05-03T13:30:12Z",
    "T3_adversarial_review_complete": "2026-05-03T13:35:00Z",
    "T4_publication_complete": "2026-05-03T13:42:18Z",
    "T5_operator_review_start": null,         // populated when operator opens the file
    "T6_operator_acknowledges": null,
    "T7_corrections_begin": null,
    "T8_corrections_complete": null,
    "T9_re_review_complete": null,
    "T10_cycle_closed": null
  },

  "artifacts": {
    "checklist_xlsx": "Batch_2-188_QA_Checklist.xlsx",
    "result_json":    "Batch_2-188_QA_Result.json",
    "adversarial_md": "Batch_2-188_Adversarial_Review.md",
    "source_reads_json": "Batch_2-188_Source_Reads.json"
  },

  "next_action_recommended": "Fix 2 FAIL items in Certify (see sections 2.3, 5.4). Re-run QA after corrections. 4 FLAG items are advisory — do not block submission."
}
```

## JSON Schema — Site Emissions QA Result

Same shape with these differences:
- `qa_type: "site_emissions"`
- `batch_id` → omitted; replaced with `"reporting_period"` and `"scapegoat_removal_ids": [...]`
- Sections reflect the site emissions categories (diesel, gasoline, electricity, embodied, BCU/REC, etc.) rather than batch sections
- `transport_mode` and `oil_type` are null

## What MUST be in every status entry

For every checklist item, regardless of status:

- **`evidence`** must cite specific values from specific primary sources. Generic "confirmed" or "matches" notes are non-compliant.
- **`primary_sources[]`** must list the actual documents read. Empty array only allowed for purely calculation-based items (e.g., "gross-to-net independent recalc"), and even those should reference the input datapoints.
- **`status`** must be one of `PASS | FAIL | FLAG | N/A` (uppercase, exact).
- **`verifier_reference`** is the protocol/VR section the item maps to (e.g., "VR Sec 5.1", "Bio-oil Geol Storage v1.1 Sec C").

## Forward-compatibility notes

This schema is versioned (`schema_version`). When changes are needed:
- Additive changes (new optional fields): bump minor version (1.0 → 1.1)
- Breaking changes (renamed/removed fields): bump major (1.0 → 2.0) and update all skills + downstream consumers
- Never silently break the contract

## When Q3 Gaia hosting comes online

This contract is the API surface between QA execution and any UI:
- Gaia UI reads the JSON, renders sections + items as a table, surfaces FAILs prominently
- BigQuery ingest takes the JSON and writes one row per item to a `qa_results` table
- Trends/dashboards query BigQuery, not the JSON files directly
- The .xlsx remains the human deliverable for verifier handoff
