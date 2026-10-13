# Materiality assessment - Charm bio-oil GHG statements (12 periods, Aug 2025-Aug 2026)

## Answer

**(a) Current basis - last 6 periods, Basco 6 only.** Two Table 1 categories are under 1% individually: Bio-oil processing 0.1166% and Staff travel 0.7834%. Collective: 0.1166% + 0.7834% = 0.9000%, which stays under the 1% collective ceiling. Waste disposal alone is 0.2131%, but it sits inside Bio-oil injection (2.7943%), and the module states: "The Materiality assessment should be undertaken for complete categories of SSRs, as defined in the relevant Protocol and set out in the system boundary, as they relate to a Reporting Period." At category grain, waste disposal cannot be excluded on its own - only the complete Bio-oil injection category counts, and that category is well above 1%.


**(b) Full 12-period basis.** Only Bio-oil processing is under 1% in aggregate (0.5213%). Staff travel is 1.3658%; waste disposal is 1.0333%.


**(c) Per-period volatility.** Bio-oil processing exceeds 1% in: 01 Aug 2025 to 15 Aug 2025, 16 Aug 2025 to 08 Sep 2025, 09 Sep 2025 to 30 Sep 2025, 01 Oct 2025 to 06 Nov 2025, 07 Nov 2025 to 31 Jan 2026. Staff travel exceeds 1% in: 16 Aug 2025 to 08 Sep 2025, 01 Oct 2025 to 06 Nov 2025, 07 Nov 2025 to 31 Jan 2026, 01 Feb 2026 to 02 Mar 2026, MAR, MAY, JUN. In the 07 Nov 2025-31 Jan 2026 period, net CO2e removed was only 43.467 t - the smallest of the 12 periods - so every category's M spikes in that period purely from the small denominator.


**(d)** The module ties the Materiality assessment to "a Reporting Period" and requires Project Proponents to "repeat the Materiality Assessment when any of the following occur: The previous assessment was conducted one year or more prior to the current verification; There has been a significant change in the Net Removal estimate; There has been a change in activities associated with any of the relevant SSRs." A fresh assessment for a current Reporting Period is what Isometric would test - not the Kansas-era history in periods further back.


**Line families.** 68 of 124 leaf-line families are under 1% individually (aggregate and every period). Their collective total is 112.243 t CO2e, 1.6872% of aggregate net removed - over the 1% collective ceiling on its own. But per §5.0's complete-category rule quoted in (a), family-level exclusion isn't the test the module applies; categories are (full family list and figures on the By_Line_Family sheet).


## Table 1 category materiality

| Category | Aggregate (t CO2e) | Aggregate M (%) | Last-6 M (%) | Flag |
|---|---:|---:|---:|---|
| Pyrolysis or other process | 954.981 | 14.3546 | 13.5047 |  |
| Bio-oil processing | 34.679 | 0.5213 | 0.1166 |  |
| Bio-oil transport | 1151.759 | 17.3124 | 12.0673 |  |
| Bio-oil injection | 257.361 | 3.8685 | 2.7943 |  |
| Staff travel | 90.864 | 1.3658 | 0.7834 |  |

Waste-disposal sub-category (within Bio-oil injection): 68.741 t, 1.0333% aggregate, 0.2131% last-6.


## Kansas activity by period

Periods with any line naming Kansas, KS, Vaulted or Hutchinson: 01 Aug 2025 to 15 Aug 2025, 16 Aug 2025 to 08 Sep 2025, 09 Sep 2025 to 30 Sep 2025, 01 Oct 2025 to 06 Nov 2025, 07 Nov 2025 to 31 Jan 2026, 01 Feb 2026 to 02 Mar 2026, AUG.
 Of these, the following periods' only KS-token hits are transit legs passing through Kansas en route to Louisiana (e.g. "CO->KS->LA"), not a Kansas facility operation - the same distinction the task draws for SOPOR/Opelousas/Maize as Louisiana-bound rail legs:

- AUG: CO->KS-> LA Flatbed Truck Transport Process Emissions - QOWV



## Method

Both CSVs were normalized to one leaf-row table (period, statement/removal ID, branch, line name, value in kg CO2e - t values multiplied by 1,000, kg values left as-is) plus, per removal, net_co2e_removed / gross_sequestration / total_activities / total_adjustments (File B's per-removal totals come from its 5 inline SUMMARY rows per removal). Each of the 219 distinct leaf-line spellings across both files was mapped once to a Bio-oil Geological Storage protocol v1.2 Table 1 category (line_category_map.csv, one reason per row); Adjustments (BCU / Constant CO2 reduction) are reductions, not SSRs, and were excluded from the materiality sums and reported separately (Adjustments sheet). For each category and period, M_category = category Activities emissions / that period's net CO2e removed, per Module v1.1 Section 5.0.


## Rule quoted (GHG Accounting Module v1.1, Section 5.0)

> "An SSR may be excluded from the system boundary only where M SSR is < 1% individually and all excluded SSRs remain <1% collectively. Where the collective total exceeds 1%, the SSRs with the highest Materiality must be reinstated in the system boundary, in descending order, until the sum of SSRs becomes < 1%."

> "The Materiality assessment should be undertaken for complete categories of SSRs, as defined in the relevant Protocol and set out in the system boundary, as they relate to a Reporting Period."

> "Buffer pools should not be considered."


## Reconciliation

All-system sensitivity analysis: every one of the 153 removals is included; none is excluded.

2 removals (MAR rmv_1KMR8D9XN1S0EHVH, APR rmv_1KRH4CXAP1S0M44D) have gross_sequestration/total_activities/total_adjustments/uncertainty_discount blank in the leaf-row export because their Certify calc-view tab capture failed. Their raw components-tab captures (raw/rmv_..._components_2026-09-28.txt) carry every leaf line and the removal-level net figure directly ("REMOVAL 25.77 tCO2e" / "REMOVAL 18.98 tCO2e"), matching the net_co2e_removed already in the CSV for both - so net was taken as-is, not re-derived. total_activities and total_adjustments were taken as the leaf-row sums themselves (status "DERIVED FROM LEAF SUMS" on the Reconciliation sheet), confirmed against the components capture's own Mitigated/Emitted subtotals:

- MAR / rmv_1KMR8D9XN1S0EHVH: total_activities = 7.921 t (leaf sum), total_adjustments = 4.937 t (leaf sum), net_co2e_removed = 25.770 t (from components-tab capture)

- APR / rmv_1KRH4CXAP1S0M44D: total_activities = 23.010 t (leaf sum), total_adjustments = 8.709 t (leaf sum), net_co2e_removed = 18.980 t (from components-tab capture)
