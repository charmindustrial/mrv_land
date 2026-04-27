# Permit Compliance Parameters — Basco 6 EW Well No. 001

**Permit**: Order No. IMD 2025-05 EW
**Operator**: Charm Louisiana, LLC (Operator Code C1116)
**Well**: Basco 6 EW Well No. 001, Serial Number 974025, API 17039880180000
**Location**: Section 006, Township 02 South, Range 02 East, Evangeline Parish, Louisiana
**Injection Zone**: 1,600–3,680 feet (Miocene formation)
**Effective Date**: August 8, 2025 (valid up to 5 years)

---

## Compliance Limits

### 1. Maximum Surface Injection Pressure (Order Item 4)

| Parameter | Limit | Column |
|---|---|---|
| Maximum Authorized Surface Injection Pressure (MASIP) | **455 psig** | `surface_pressure_psi` |

The MASIP is determined by the "Fracture Gradient Chart, Louisiana Gulf Coast" by Ben Eaton. It is based on calculating 90% of the fracture pressure utilizing a formation pore pressure of 9.0 ppg and does not account for tubing frictional losses.

### 2. Annular Pressure Requirements (Order Item 6)

| Parameter | Limit | Column |
|---|---|---|
| Minimum tubing-casing annulus pressure | **200 psig** | `annular_pressure_psi` |
| Minimum annular-to-surface differential during injection | **≥50 psig above actual operating surface injection pressure** | `annular_pressure_psi - surface_pressure_psi` (when `injecting == "YES"`) |

Charm must maintain a tubing-casing annulus pressure that exceeds the operating injection pressure at all times. The minimum is 200 psig. Operating below 200 psig requires written Commissioner approval.

During actual injection, the tubing-casing annular pressure must be at least 50 psig greater than the well's actual operating surface injection pressure.

**Exemptions** (Order Item 6c): The annular pressure requirements do not apply during:
- Workovers
- Well or reservoir tests
- Other routine maintenance
- Time periods of less than 4 consecutive hours where well mechanical integrity is not determined to be lacking and timely action is taken to correct pressure fluctuations

### 3. Continuous Monitoring (Order Item 16)

Charm must continuously record surface injection pressures and flow rates and document volumes injected during each injection event. This data is reported in quarterly monitoring reports (Order Item 5).

Quarterly reports must contain at minimum: waste pH, viscosity, specific gravity, carbon content, volume of waste injected, tubulars gauge pressure, and flow rate — in tabular and graphical presentations. Due within 30 days after end of each calendar quarter.

---

## Non-Compliance Reporting (Order Item 9)

Any noncompliance that may endanger health or the environment must be reported by phone at (225) 342-5515 within 24 hours, with written submission within 5 days. Non-compliance events include:

- Evidence that injected bio-oil may endanger the USDW
- Noncompliance with a permit condition or malfunction that may cause fluid migration
- Triggering of a shut-off system (downhole or surface)
- Any failure to maintain mechanical integrity

---

## Key Context for Data Review

- The Basco well has **negative native pressure** — the formation draws fluid in once flow is established. This means `surface_pressure_psi = 0` during active injection is expected behavior, not a sensor fault.
- The USDW base is at approximately 1,170 feet below ground level.
- External cement extends above the top of the injection zone into a sufficient confining zone.
