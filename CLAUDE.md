# MRV_LAND — Shared Claude Code Context for Charm Industrial MRV

This repository is the shared knowledge base and workflow library for Charm Industrial's MRV (Measurement, Reporting, and Verification) team. It is designed to be read by Claude Code agents to provide consistent, accurate context across sessions and team members.

## Who Uses This

- **Garrett Lutz** — MRV team, handles production period close-outs, injection batch reporting, Mangrove data entry, Certify QA, and embodied emissions quantification
- **Max** — Garrett's manager, reviews GHG Statements, owns QA checklist process, has Claude Code agents for wellhead data transformation

## What Charm Does

Charm Industrial converts non-merchantable biomass to bio-oil via pyrolysis and permanently injects it into geological formations (salt caverns in KS, permeable reservoirs in LA) for carbon sequestration. Credits are earned on the Isometric voluntary carbon market registry. See `context/charm_project.md` for full details.

## Repository Structure

```
MRV_LAND/
  CLAUDE.md              <- you are here
  README.md              <- repo overview for humans
  workflows/             <- step-by-step MRV workflow instructions
  context/               <- shared reference knowledge (protocols, project details, EFs)
  scripts/               <- automation code (Python, etc.) — future
```

## Key Workflows (in `workflows/`)

Dependency chain:
`phase1_production_period` -> `phase2a_injection_batch_data` -> `phase2b_injection_emissions` -> `phase2c_mangrove` -> `phase2d_certify_qa` -> `phase3a_protocol_documentation`

| File | What It Does |
|------|-------------|
| phase1_production_period.md | Monthly production data close-out (CO facility) |
| phase2a_injection_batch_data.md | Injection batch verification (COBB, scale tickets, COAs) |
| phase2b_injection_emissions.md | Site emissions calculation (diesel, gasoline, argon, etc.) |
| phase2c_mangrove.md | Mangrove platform data entry via Playwright |
| phase2d_certify_qa.md | Isometric Certify QA — 9-section checklist per batch |
| phase3a_protocol_documentation.md | Final Reporting Package assembly for VVB submission |
| embodied_emissions_quantification.md | Capital equipment LCA and amortization |

## Key Context Files (in `context/`)

| File | What It Covers |
|------|---------------|
| charm_project.md | Charm's Isometric project — PDD, supply chain, carbon accounting |
| bio_oil_protocol.md | Bio-Oil Geological Storage Protocol v1.0/1.1/1.2 |
| isometric_registry_standard.md | Isometric Registry Standard v1.7/1.8/2.0 |
| isometric_modules.md | Energy Use, Feedstock, Salt Cavern, Permeable Reservoir modules |
| emission_factors.md | 2026 Standard Emission Factors (GREET, GLEC, ICE) |
| injection_batch_structure.md | Folder hierarchy, UID conventions, ops notes layout |
| verification_history.md | Prior verification results and open action items |
| production_vs_reporting_period.md | Production period != injection reporting period |

## Key Rules

- **Cell references only** — always use cell references (e.g. $J$2) for emission factors in calc sheets; never hardcode numeric values
- **Sparging 1.29%** applies to AECN only — not Charm WODO/QOWV
- **Production period != reporting period** — CO calendar month vs. injection cycle
- **EF verification** — manually verify Certify EFs against Standard EF CSV each reporting period
- **VVB is always 350 Solutions**
- **Kerry batches** — do not submit until methodology memo is approved

## Key Data Paths

| Resource | Path |
|----------|------|
| Removals Reporting | `G:\.shortcut-targets-by-id\17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b\Removals Reporting\` |
| Invoices + Tracking Docs | `G:\.shortcut-targets-by-id\1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi\Invoices + Tracking Docs\` |
| Bio-Oil Injection Tracker | Google Sheet: `116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q` |
| Mangrove project | `https://app.gomangrove.com/nexus/709/data-inputs/events` |

## How to Start a Workflow Session

Say: **"Start [phase name], period [RP or production period name]"**

The agent will:
1. Read the relevant workflow doc from `workflows/`
2. Read `workflows/current_status.md` if it exists
3. Confirm what's needed and begin
