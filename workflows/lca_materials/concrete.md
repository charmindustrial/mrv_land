# Material LCA: Concrete (Ready-Mix)

**Source of Truth:** Standard Emission Factors + Calculations - 2026.csv
**EF:** 0.086234 kgCO2e/kg
**Units:** MTCO2e/T Concrete
**Source:** GREET 2024
**NAICS fallback:** Not applicable — material EF available

---

## Formula

```
GWP (kgCO2e) = mass (kg) × 0.086234
```

---

## Weight Sourcing

- **From invoice:** bag count × bag weight (e.g., 4 × 80 lb bags = 320 lb)
- Convert lbs to kg: × 0.453592

---

## Worked Example: Ready Mix 80lb Bags

**Invoice:** LA Home Builders Invoice 2603-284421, 3/18/2026
**Quantity:** 4 × 80 lb bags = 320 lb = 145.2 kg

```
GWP = 145.2 kg × 0.086234 kgCO2e/kg = 12.5 kgCO2e
```

---

## Applies To

- Bagged ready-mix concrete (Quikrete, Sakrete, etc.)
- Poured concrete pads and foundations
- Concrete blocks and stabilizers

---

## Notes

- "Ready-mix concrete US nat'l average ton delivered" per GREET 2024 — appropriate for both bagged and poured.
- Rebar within a concrete pour is accounted for separately under `steel.md`.
