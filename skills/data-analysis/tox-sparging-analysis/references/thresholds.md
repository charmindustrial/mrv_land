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

The Brief's exact wording is: *"Site SOP requires operators to confirm the catalyst inlet is at
600°F before **closing** the gate valve and introducing air into the tank."* (CatOx Engineering
Brief, "System controls" → "Catalyst preheat requirement"). Earlier versions of this skill said
"before **opening** the gate valve" — that was wrong; the Brief says closing, matching its
"Closed-loop routing" paragraph: *"Once the gate valve is closed, the system is fully closed."*

Note also that the Brief describes 600°F as a **catalyst inlet** setpoint — *"is operated at a
catalyst inlet setpoint of 600°F (315°C, 588 K)"* (Setpoint Supplement) — while also calling it a
floor the outlet clears during destruction: *"an exothermic reaction raises outlet temperatures to
850–1000°F — well above the 600°F minimum threshold."* Both readings are in the Brief, so drawing
the line on the outlet chart is supported, but do not describe it as an outlet-only setpoint. The
Brief states where the inlet's heat comes from during a campaign: *"The oxidizer's integrated heat
exchanger uses this exothermic output to sustain inlet temperature throughout a sparging campaign
without external heating."* Do not treat every low inlet reading as a violation: the inlet needs
to be at 600°F at the moment sparging air is introduced, and much recorded time is
between-campaign idle.

---

## Reading the three temperature regimes — MEASURED FACTS vs WORKING THEORY

Max asked (Aug 2026) what the temperature patterns actually indicate. The split below is
deliberate: the measured column is reproducible from any period's export, the theory column is
inference that the temperature record **cannot** confirm on its own. Keep them separate. Do not
promote the theory to a conclusion, and do not put any of it in a verifier-facing workbook.

### Measured in the July 2026 data (reproducible — recompute per period)

Gap between outlet and inlet, by band, over 8,338 readings (49 h logger hold excluded):

| Band | T1 hours | T1 outlet−inlet | T2 hours | T2 outlet−inlet |
|---|---|---|---|---|
| Outlet ≥850°F | 152 h | +291°F | 167 h | +304°F |
| Outlet 600–850, inlet ≥600 | 94 h | +187°F | 146 h | +81°F |
| Outlet <600, inlet ≥600 | 0.33 h (4 readings) | −24°F | 0.25 h (3 readings) | −1°F |
| Both <600, both >200 | 110 h | +7.8°F | 126 h | +5.2°F |
| Both ≤200 (cold) | 289 h | −1°F | 225 h | 0°F |

Also measured: the long tandem declines fall on 100% of steps at −29 to −56°F/h. Four ran to
ambient; fitting a cooling curve to each recovered an ambient of 68.5–81.5°F (not supplied — the
fit found it, and it matches Louisiana July ambient) and a characteristic time of 14.4–16.7 h
(mean 15.55 h, spread 1.06 h) across both trains, episodes weeks apart. Fit quality was R² 0.50–0.83
with typical misses of 30–80°F, so a single cooling curve is an approximation, not a precise
description — the repeatability of the characteristic time is the durable part, not the curve.

### Supported by the Brief (quote these, do not paraphrase)

- Exotherm band: *"When benzene-rich air contacts the catalyst at operating temperature, an
  exothermic reaction raises outlet temperatures to 850–1000°F — well above the 600°F minimum
  threshold."*
- Where inlet heat comes from: *"The oxidizer's integrated heat exchanger uses this exothermic
  output to sustain inlet temperature throughout a sparging campaign without external heating."*
- The interlock, which is what carries the no-venting case: *"The sparging blower cannot activate
  unless the oxidizer is on. This is a hard control with no operator override."* And: *"In all
  cases the blower interlock applies: sparging does not continue while the catalyst is offline."*
- The stated limit on reading the data: *"There is no single sensor signal that cleanly
  distinguishes \"actively stripping benzene\" from \"blower running with benzene exhausted.\""*

### WORKING THEORY — not established, do not present as fact

The chain below fits the July numbers and the Brief's description of the heat exchanger, but the
temperature record cannot confirm it, and no E-stop log, blower-status signal, or airflow record
was available to test it:

> Gas stops → the exotherm stops → the inlet loses the heat source the Brief describes → inlet and
> outlet fall together → the unit coasts to ambient. On that reading, outlet-below-600-while-inlet-
> holds-above-600 is a brief pass-through rather than a state the unit rests in, which would explain
> why it measured 4 and 3 readings out of 8,338. Tandem decline would then be the ordinary
> end-of-campaign shape, not a fault.

**Where this stops being knowable from temperature.** A near-zero gap is equally consistent with
nothing flowing and with gas flowing through a catalyst too cold to light off — the Brief's own
limitation quote above says as much. So the temperature data does not by itself establish that
nothing is being vented; the interlock quote does. The repeatable ~15 h cooling time is consistent
with an idle vessel losing heat to still air (forced air would cool it faster and the rate would
track airflow), but that is corroboration, not proof.

**Trips.** Rapid falls from ≥850°F (≥300°F inside 30 min) occurred 25 times on Train 1 and 23 on
Train 2 in July; most recovered within an hour or two. Jul 12 Train 2 (repeated spikes to
1,048–1,055°F each collapsing to 200–400°F, then back to ~990°F) is the pattern the Brief attaches
to trips — *"overheating from a high-concentration exothermic event, or condensate from the
knock-out drum entering the oxidizer"* — but nothing in the temperature record identifies a trip as
a trip. Do not label any event an E-stop without the control-system log.

**Watch for logger artifacts before calling any collapse real.** Jul 09 07:56 Train 2 looked like
an 869°F→316°F collapse; the actual sequence is `869 869 869 869 869 869 869 869 979 316 316 316…`
— held values on both sides. See the stuck-reading section below.

---

## Reading Resolution

Current exports (May 2026 onward) are **5-minute** readings. Legacy exports were hourly. At the
monthly-aggregate level the difference is negligible (at-temperature fraction within ~1 point).
The finer 5-minute data resolves short (<1 h) outlet dips directly rather than by inference, so
the old "hourly resolution caveat" (transient fluctuations appearing more durable than they are)
no longer needs to be stated.

---

## Held / Frozen Readings — check every period

Separate from the offline sentinel, the data historian sometimes **holds the last good value**
instead of recording a fresh reading. Short repeats are normal (the historian only logs a change
once it exceeds a deadband). What is not normal is a repeat spanning **all four channels on both
trains, starting and ending at the same instant**: two independent oxidizer trains cannot
physically hold four temperatures constant to the exact degree, so such a block is a logging
artifact and those rows are not live readings.

This matters for the reported numbers because **a value frozen above the setpoint counts as
at-temperature and inflates the at-temperature share.** The script runs this check on every run
and prints each all-channel frozen block plus the at-temperature share recalculated with the
blocks excluded. Report the figure **both ways** — as recorded, and excluding held readings.

The July 2026 period is the worked example: all four channels froze at Jul 25 05:26 and released
together at Jul 27 06:41 — 49.2 hours, with the outlets held at 660°F (Train 1) and 630°F
(Train 2), i.e. above setpoint. Site cause was a failed control panel card, corroborated in
`#injection-ops-la` (cody, 2026-07-25 17:06:33 PDT: *"Yes nothing will run without the card."*).
Six shorter all-channel blocks totalling ~17 h appeared in the same period.

A frozen block is a **data-completeness** observation, not a compliance finding: compliance rests
on the sparging-blower interlock, not on the temperature record (see SKILL.md).

---

## Offline / Sentinel Convention

- **Current exports:** `0` = offline / no reading.
- **Legacy combined exports:** `-238` = sensor offline.

Both are converted to blank (NaN) and shown as grey shaded gaps in the charts. The processing
script handles both.
