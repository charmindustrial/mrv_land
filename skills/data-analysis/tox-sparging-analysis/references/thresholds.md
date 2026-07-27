# ToX Threshold Reference

## Catalyst Minimum Operating Temperature — see `catox_config.json`

The setpoint value is NOT restated here as an independent number — it lives in one place only,
`references/catox_config.json` (`outlet_setpoint_f`), which the processing script reads at
runtime. This is deliberate: the setpoint previously drifted (a stale 650°F literal survived in
code while the true value was 600°F) precisely because the number was duplicated across prose and
code. One canonical value = no drift. To change it, edit the config; everything follows.

The config also records the `setpoint_source`: the Intellishare **ECO300** manufacturer spec
(>98% VOC destruction efficiency), per the **CatOx Engineering Brief** Setpoint Supplement
(Garetto & Apesteguía 2001, Zuo et al. 2024, Wang & Chou 2000). This is confirmed, not
provisional. The script prints the setpoint and its source on every run so any drift is visible
in the output.

The 600°F line is drawn on the outlet in the Processed charts as the minimum operating
temperature. During active benzene destruction the exotherm drives the outlet to **850–1000°F**;
a below-600°F outlet while a campaign is winding down means benzene is exhausted (no VOCs to
drive the reaction), which is the expected completion state, not a failure.

---

## Catalyst Inlet — Preheat Requirement

Site SOP requires the operator to confirm the catalyst **inlet is at 600°F before opening the
gate valve** and introducing air into the tank. The oxidizer's integrated heat exchanger then
uses the exothermic output of destruction to sustain inlet temperature through a campaign without
external heating. Do not treat every low inlet reading as a violation: the inlet only needs to be
at 600°F at the moment sparging air is introduced, and much recorded time is between-campaign
idle.

---

## Reading Resolution

Current exports (May 2026 onward) are **5-minute** readings. Legacy exports were hourly. At the
monthly-aggregate level the difference is negligible (at-temperature fraction within ~1 point).
The finer 5-minute data resolves short (<1 h) outlet dips directly rather than by inference, so
the old "hourly resolution caveat" (transient fluctuations appearing more durable than they are)
no longer needs to be stated.

---

## Offline / Sentinel Convention

- **Current exports:** `0` = offline / no reading.
- **Legacy combined exports:** `-238` = sensor offline.

Both are converted to blank (NaN) and shown as grey shaded gaps in the charts. The processing
script handles both.
