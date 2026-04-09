---
type: dashboard
---

# MRV Workflow Dashboard

## Dependency Chain
[[phase1_production_period]] → [[phase2a_injection_batch_data]] → [[phase2b_injection_emissions]] → [[phase2c_mangrove]] → [[phase2d_certify_qa]] → [[phase3a_protocol_documentation]]

[[embodied_emissions_quantification]] → [[phase2b_injection_emissions]]

## Phase Status — Current Period

```dataview
TABLE status, period, depends_on AS "Depends On"
FROM "workflows"
WHERE type = "phase" AND phase != "embodied"
SORT phase ASC
```

## Open Tasks (All Files)

```dataview
TASK
FROM "workflows"
WHERE !completed
GROUP BY file.link
```

## Ad Hoc Workflows

```dataview
TABLE status, trigger
FROM "workflows"
WHERE type = "ad_hoc"
```

---

## Update Instructions

When a phase changes status, update the `status` field in that file's frontmatter:
- `not_started`
- `in_progress`
- `complete`

### Reporting Period Convention
- All phase files use `period: "{{current_rp}}"` as a template variable
- Reporting periods are **monthly** by default
- At the start of a new RP: replace `{{current_rp}}` with the actual date range (e.g., `"Apr 2 – May 1"`) across all phase files, and reset statuses
- If Garrett specifies a non-standard period, use that instead
