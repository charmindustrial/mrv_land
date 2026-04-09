# Charm Industrial MRV Workflow — Master Index

## Workflow Files

| File | Phase | Session Type |
|------|-------|-------------|
| [phase1_production_period.md](phase1_production_period.md) | Production Period (CO calendar month) | Spreadsheet — long sessions OK |
| [phase2a_injection_batch_data.md](phase2a_injection_batch_data.md) | Injection Batch Data (COBB, scale tickets, COAs) | Spreadsheet — long sessions OK |
| [phase2b_injection_emissions.md](phase2b_injection_emissions.md) | Injection Emission Data (site emissions, BCU Quant) | Spreadsheet — long sessions OK |
| [phase2c_mangrove.md](phase2c_mangrove.md) | Mangrove Data Entry | Playwright — keep short, one category per session |
| [phase2d_certify_qa.md](phase2d_certify_qa.md) | Certify QA Check | Playwright — one batch at a time |

## How to Start a Session

Say: **"Start [phase name], period [RP or production period name]"**

I will:
1. Read the relevant workflow doc
2. Read `current_status.md` if it exists
3. Confirm what's needed and begin

## Key Paths

| Resource | Path |
|----------|------|
| Removals Reporting | `G:\.shortcut-targets-by-id\17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b\Removals Reporting\` |
| Invoices + Tracking Docs | `G:\.shortcut-targets-by-id\1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi\Invoices + Tracking Docs\` |
| Bio-Oil Injection Tracker | Google Sheet: `116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q` |
| Standard EF file | `C:\Users\Garett Lutz\Downloads\Standard Emission Factors + Calculations - 2026.csv` |
| Playwright upload folder | `C:\Users\Garett Lutz\Desktop\Claude\.playwright-mcp\` |
| Mangrove project | `https://app.gomangrove.com/nexus/709/data-inputs/events` |

## Key Rules
- Always use cell references (e.g. $J$2) for emission factors — never hardcode numbers
- Sparging 1.29% applies to AECN only — not Charm WODO/QOWV
- Kerry batches: use same methodology as most recent prior period unless told otherwise
- Production period ≠ injection reporting period (CO calendar month vs. injection cycle)
- Playwright uploads: files must be in `.playwright-mcp\` folder first
- Auto route map: always uncheck "Update distance and attach route map as evidence" for site emission events

## Current Period
See `current_status.md`
