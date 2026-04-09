# Material LCA: Industrial Machines (Heavy, Unspecified)

**Source:** ecoinvent via OpenLCA
**LCA Database Tag:** `Industrial machine production, heavy, unspecified | industrial machine, heavy, unspecified | APOS, U`
**EF (production):** 1.937 kgCO2e/kg
**EF (steel disposal — collection):** 0.07 kgCO2e/kg
**EF (steel disposal — recycling):** 0.06 kgCO2e/kg
**Note:** Not in the 2026 Standard EF CSV — no GREET equivalent for complex industrial machinery. OpenLCA/ecoinvent is the appropriate method here.

---

## Formula

```
GWP (kgCO2e) = mass (kg) × 1.937 + mass (kg) × 0.07 + mass (kg) × 0.06
             = mass (kg) × 2.067
```

Steel disposal factors applied to full unit mass (conservative — assumes steel is predominant material).

---

## Weight Sourcing

- **Preferred:** manufacturer spec sheet or product datasheet (weight in kg/lbs)
- **Acceptable:** retailer or distributor product listing for exact model
- **Last resort:** estimate from comparable units in the same class

---

## Worked Example: Kaeser Aircenter SM15 Compressor

**Unit mass:** 239.95 kg (from manufacturer datasheet)

```
GWP = 239.95 × 1.937 + 239.95 × 0.07 + 239.95 × 0.06
    = 464.82 + 16.80 + 14.40
    = 495.97 kgCO2e
```

---

## Applies To

Complex machinery where material composition is not easily broken out:
- Air compressors
- Pumps (centrifugal, triplex, progressive cavity)
- Generators
- Motors and VFDs
- Blowers, fans
- Pressure washers
- Welders
- Forklifts and telehandlers

**Decision rule:** Use this category when the item is a multi-material assembled machine and a material-level breakdown (steel + rubber + HDPE, etc.) is not available from a spec sheet or SDS. If material composition IS available, prefer the component-level material EFs from the 2026 Standard EF CSV.

---

## Notes

- The ecoinvent dataset is based on a rock crusher as the reference industrial machine. It is a generic proxy — not item-specific.
- No energy for assembly is included in this dataset.
- End-of-life: full unit mass modeled as both recycled and disposed without recycling — conservative estimate.
- For items that are clearly dominated by a single material (e.g., a steel tank), use `steel.md` instead.
