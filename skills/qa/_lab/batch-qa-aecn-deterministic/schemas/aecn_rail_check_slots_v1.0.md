# AECN Rail — Deterministic Check Slots Reference — v1.0

**Status:** Design finalized 2026-05-15. Awaiting adoption in production AECN skill.
**Scope:** AECN rail delivery batches only. AECN truck, Kerry tote, Kerry tanker, and Charm-produced oil each get their own reference when those delivery routes are onboarded.
**What this is:** The minimum set of labeled entries each deterministic check needs to run. Gate 1 fills these from whatever source documents ops is using that quarter. The structure around these entries in the data file can change freely — only changes to the entries listed here require a version bump.
**Successor:** When entries are added, renamed, or removed → v1.1+ with changelog. Old batch files stay tagged with the version they were written to.

---

## Design decisions — finalized 2026-05-15

| Decision | Resolution |
|---|---|
| Layout scope | One reference per delivery route. AECN rail ≠ AECN truck. New routes get new references. |
| Label style | Underscores between words, units baked in where established (`gross_weight_lb`, `cargo_kg`, `mass_MT`). Unit is part of the label — never ambiguous. |
| Required vs. optional | Required = anything a deterministic check uses OR a checklist item asks for. Optional = context only. |
| Version stamp | Every data file writes `_schema_version: "1.0"` at the top. Audit trail. |
| Where this lives | Shared reference across the QA skill cluster — same level as adversarial review, KPI tracker. Not inside any single skill. |
| Total offloads per railcar | Operational constant (currently 4), NOT a per-batch field. Lives as a constant in `compute_mass_chain.py`. Update the script when ops changes the count. |
| Null vs. zero for unfilled entries | Humans are variable. Script treats both `null` and `0` as "not yet filled" in offload table rows. Neither is interpreted as a real value when other offloads are still pending. |
| COBB row ID | Capture TWO identifiers: (1) row number at time of QA — can shift if sheet is edited later; (2) the value in column A (batch ID) — stable regardless of row movement. |

---

## Two-model routing rule

Each check is tagged with a `check_type` in the script output:

| `check_type` | What it means | How to handle a FAIL or FLAG |
|---|---|---|
| `computation` | Pure arithmetic — the answer is definitively right or wrong | Surface directly in the checklist as a confirmed finding. No LLM judgment needed. |
| `policy` | Script detected a discrepancy, but whether it matters requires context | Route to LLM in Gate 2. LLM determines if it's a known correction lag, an expected operational imperfection, or a real error. LLM writes the evidence note and assigns Pass/Flag/Fail. |

**Why the split matters:** the script can detect that COBB ≠ Ops Notes, but only the LLM can determine whether that's because an operator told us verbally about a correction and didn't update COBB (expected lag, operational flag for Garrett) vs. an actual data integrity problem. Routing policy findings to the LLM lets each model do what it's actually good at.

---

## Check slots

Each section below lists the entries a specific deterministic check reads. Entries tagged **[R]** are required — the check returns INSUFFICIENT_DATA without them. Entries tagged **[O]** are optional and used when present.

### File metadata (all batches)

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `_schema_version` | string | R | Always `"1.0"` for this reference |
| `batch_id` | string | R | e.g. `"2-184"` |
| `oil_type` | string | R | Always `"AECN"` for this reference |
| `delivery_mode` | string | R | Always `"rail"` for this reference |
| `injection_site` | string | R | e.g. `"Basco 6 LA"` |
| `reporting_period` | string | R | e.g. `"Apr 2026"` |
| `completion_date` | date | R | ISO 8601 — injection completion date |

### Check: scale_ticket_subtraction — `check_type: computation`

Verifies that full truck weight minus empty truck weight equals the stated net, and that the pounds-to-kg conversion is correct.

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `scale_tickets.full_ticket.gross_weight_lb` | lb | R | As read from full-truck scale ticket |
| `scale_tickets.empty_ticket.gross_weight_lb` | lb | R | As read from empty-truck scale ticket |
| `scale_tickets.computed_net_lb` | lb | R | What the data file states as net (script re-derives and compares) |
| `scale_tickets.computed_net_kg` | kg | R | What the data file states as kg net (script re-derives and compares) |

Supporting context (checklist use, not check input):

| Entry | R/O | Notes |
|---|---|---|
| `scale_tickets.full_ticket.filename` | R | Source filename |
| `scale_tickets.full_ticket.ticket_number` | R | |
| `scale_tickets.full_ticket.date` | R | ISO 8601 |
| `scale_tickets.full_ticket.scale_location` | R | |
| `scale_tickets.full_ticket.tractor` | R | |
| `scale_tickets.full_ticket.trailer` | R | |
| `scale_tickets.empty_ticket.*` | R | Same fields as full ticket |

### Check: scale_ticket_vs_ops_notes_offload — `check_type: computation`

Compares the scale-derived net (in kg) against the matching offload row in Ops Notes. Tolerance ≤0.5%.

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `scale_tickets.computed_net_kg` | kg | R | From scale ticket check above |
| `offload` | string | R | Which offload this batch represents, e.g. `"offload_3"` |
| `ops_notes.offload_table[].id` | string | R | Row identifier — convention `"Rail_<railcar>_<date>_offload_N"` |
| `ops_notes.offload_table[].cargo_kg` | kg | R | Null or 0 = not yet filled (sister-batch pending). Script skips on either. |

### Check: bol_list_sum_vs_stated_total — `check_type: computation`

Verifies that the individual BOL masses sum to the total stated in Ops Notes.

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `ops_notes.bols_into_railcar[].mass_MT` | MT | R | One entry per BOL |
| `ops_notes.total_railcar_loaded_MT` | MT | R | Stated total from Ops Notes |

Supporting context:

| Entry | R/O | Notes |
|---|---|---|
| `ops_notes.bols_into_railcar[].number` | R | BOL number |
| `ops_notes.filename` | R | Ops Notes source filename |
| `ops_notes.drive_file_id` | R | |

### Check: railcar_inbound_outbound_balance — `check_type: computation`

Checks that total mass loaded into the railcar (BOLs) minus total mass offloaded (all offload rows) is ≤5%. Skipped if any offload row has cargo_kg of null or 0 (railcar not fully offloaded yet).

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `ops_notes.bols_into_railcar[].mass_MT` | MT | R | Same as above |
| `ops_notes.offload_table[].cargo_kg` | kg | R | All rows; null or 0 triggers skip |

### Check: last_offload_derivation — `check_type: computation`

If this batch is the last offload (highest offload number in the table), verifies cargo = total BOL mass − sum of all prior offloads. Skipped if not the last offload. Tolerance ≤0.5%.

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `offload` | string | R | Which offload this batch is |
| `ops_notes.offload_table[].id` | string | R | To sort and identify last row |
| `ops_notes.offload_table[].cargo_kg` | kg | R | All rows — prior offloads need real values |
| `ops_notes.bols_into_railcar[].mass_MT` | MT | R | Total inbound |

### Check: cobb_offload_consistency — `check_type: policy`

Compares the COBB sheet's offloaded quantity against Ops Notes cargo for this offload. Tolerance ≤0.5%. Hygiene-level (FLAG on mismatch, not FAIL).

**Policy routing:** a FLAG here means the script detected a discrepancy between COBB and Ops Notes. It does NOT mean the underlying mass is wrong — it means the operator-facing back-end may not have been updated. The LLM determines in Gate 2 whether this is a known correction lag (operational flag for Garrett to clean up, no verifier impact) or a real data integrity issue.

| Entry | Unit | R/O | Notes |
|---|---|---|---|
| `cobb.row_id_at_qa` | string | R | Row number in COBB sheet AT TIME OF QA — may shift later |
| `cobb.batch_id_col_a` | string | R | Value in column A — stable, used to re-locate row if sheet is edited |
| `cobb.offloaded_quantity_kg` | kg | R | Column F value |
| `offload` | string | R | To match against the Ops Notes offload table |

Supporting context:

| Entry | R/O | Notes |
|---|---|---|
| `cobb.consumed_lot` | R | e.g. `"Rail_GPRX 5188_2.27.26_offload_3"` |
| `cobb.order_line_quantity_completed_kg` | kg | R | Column G value |
| `cobb.origin_quantity_kg_full_railcar` | kg | R | Column H value |
| `cobb.injection_completion_date` | date | R | |
| `cobb.injection_ph` | | O | |

---

## Other required entries (checklist, not deterministic checks)

| Entry | R/O | Notes |
|---|---|---|
| `railcar.id` | R | e.g. `"GPRX 5188"` |
| `railcar.offload_number` | R | 1–N |
| `railcar.is_last_offload` | R | True/False |
| `certify.project_url` | R | Full URL |
| `certify.removal_id` | R | e.g. `"rmv_1KQ7Y0Y4S1S023MT"` |
| `certify.components[].name` | R | |
| `certify.components[].tCO2e` | R | |
| `certify.datapoints_count` | R | |
| `certify.sources_tab.total_count` | R | |
| `certify.sources_tab.filenames[]` | R | |
| `drive.folder_url` | R | Top-level batch folder |
| `lab_results.filename` | R | Certificate of Analysis |
| `lab_results.drive_file_id` | R | |
| `lab_results.density_g_per_cm3_at_15C` | R | |
| `lab_results.viscosity_cSt_at_40C` | R | |
| `lab_results.acid_number_mg_KOH_per_g` | R | |
| `lab_results.nitrogen_pct` | R | Can be `"<0.75"` (detection limit) |
| `lab_results.sulfur_pct` | R | Same |
| `lab_results.water_pct` | R | |
| `ops_notes.offload_table[].injected_kg` | R | |
| `ops_notes.offload_table[].alloc` | R | Allocation fraction = cargo / total railcar |
| `ops_notes.distances.AECN_to_SOPOR_per_truck_mi` | R | |
| `ops_notes.distances.SOPOR_to_Opelousas_rail_mi` | R | |
| `ops_notes.distances.Opelousas_to_Basco_truck_mi` | R | |
| `bols[].number` | R | Delivery BOLs |
| `bols[].mass_MT` | R | |
| `bols[].origin` | R | |
| `bols[].destination` | R | |

---

## Script constants (not per-batch fields)

The following operational parameters live in `compute_mass_chain.py`, not in each batch's data file. Update the script when operations change.

| Constant | Current value | Notes |
|---|---|---|
| `TOLERANCE_PCT` | 0.5% | Variance threshold for material checks |
| `LOSS_FLAG_PCT` | 5.0% | Railcar inbound-outbound loss threshold |
| `LB_TO_KG` | 0.453592 | Unit conversion |
| Expected offloads per railcar | 4 | Sanity check reference — update when ops changes |

---

## Changelog

| Version | Date | What changed |
|---|---|---|
| 1.0 | 2026-05-15 | Initial. AECN rail only. 6 deterministic checks. |
| 1.0 | 2026-05-15 | Added `check_type: computation \| policy` field to all checks and helpers. Added two-model routing rule. `cobb_offload_consistency` classified as policy; all other 5 checks as computation. |
