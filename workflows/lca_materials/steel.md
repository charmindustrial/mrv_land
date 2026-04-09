# Material LCA: Steel (Virgin, Unalloyed / Carbon Steel)

**Source of Truth:** Standard Emission Factors + Calculations - 2026.csv
**EF:** 2.818 kgCO2e/kg
**Units:** MTCO2e/T Steel (= kgCO2e/kg)
**Source:** GREET 2025
**NAICS fallback:** Not applicable — material EF available

---

## Formula

```
GWP (kgCO2e) = mass (kg) × 2.818
```

No recycling adjustment applied — the 2026 GREET value is the standard; do not layer on OpenLCA recycling credits.

---

## Weight Sourcing

- **Preferred:** manufacturer spec sheet or SDS
- **Acceptable:** retailer product listing for the exact SKU (document the URL)
- **Last resort:** standard reference dimensions (e.g., AISC section tables for structural steel) — note as estimate

---

## Worked Example: Wire Filled Gate 12' Black (WFGBL12)

**Invoice:** LA Home Builders Invoice 2603-284421, 3/18/2026
**Quantity:** 2 units
**Unit weight:** 61 lbs (27.7 kg)
**Source:** Tractor Supply Co. product listing for WFGBL12
**Material:** Steel (frame = 1-3/4" round steel tubing, powder-coat finish; mesh fill = steel wire)

```
GWP = 2 × 27.7 kg × 2.818 kgCO2e/kg = 156.2 kgCO2e
```

---

## Applies To

Items that are primarily carbon/unalloyed steel. Common examples:
- Gates, fencing, panels
- Tanks (carbon steel)
- Structural steel, beams, channels
- Storage containers (Conex/shipping containers)
- IBC totes (steel pallet component)
- Piping and fittings (carbon steel)

For **stainless steel** items, see `stainless_steel.md` (EF = 0.720746 kgCO2e/kg, GREET 2024).

---

## Notes

- Prior LCA docs in the existing inventory (e.g., shipping container) used OpenLCA/ecoinvent with a recycling-adjusted formula. Those historical values stand as-is. All new items use 2026 GREET 2.818.
- If an item is mixed material (e.g., steel frame + rubber seals), split by mass and apply the relevant material EF to each component. See `embodied_emissions_quantification.md` Step 1.
