# Material LCA: Wood (Treated Softwood Lumber)

**Source of Truth:** ICE Database v2.0 (Circular Ecology / University of Bath)
**EF:** 0.07 kgCO2e/kg
**Units:** kgCO2e/kg, fossil CO2 only, cradle-to-gate
**Source:** ICE Database v2.0, sawn softwood — https://circularecology.com/embodied-carbon-footprint-database.html
**Status:** Conservative floor estimate — fossil emissions only; biogenic carbon excluded

**Note:** Not currently in the 2026 Standard EF CSV. If/when a lumber EF is added to the standard CSV, that becomes source of truth and this file should be updated.

---

## Formula

```
GWP (kgCO2e) = mass (kg) × 0.07
```

---

## Weight Sourcing

- **Preferred:** product spec sheet or lumber table (standard dimensional lumber weights are published)
- **Acceptable:** estimate from standard dimensions — typical pressure-treated softwood density ~500–600 kg/m³
  - Example: 6"×8"×6' post ≈ 32 kg (~70 lbs)
- Estimates are acceptable for low-cost items (under ~$100/unit)

---

## Worked Example: 6'x8' Corner Post Treated

**Invoice:** LA Home Builders Invoice 2603-284421, 3/18/2026
**Quantity:** 2 units
**Unit weight:** ~32 kg (estimated — standard 6×8 pressure-treated timber)
**Note:** Weight is an estimate; acceptable at this cost magnitude ($21/unit)

```
GWP = 2 × 32 kg × 0.07 kgCO2e/kg = 4.5 kgCO2e
```

---

## Applies To

- Pressure-treated fence posts, corner posts
- Treated lumber framing
- Timber pads, sleepers, blocking

---

## Notes

- This EF covers sawn softwood only — does not include the treatment chemical (ACQ, CCA, etc.). The preservative contribution is negligible at these quantities.
- Isometric does not publish a specific lumber EF; ICE Database v2.0 is the most defensible publicly available source.
- Do not use for engineered wood products (LVL, GLB, CLT) — those have separate ICE values.
