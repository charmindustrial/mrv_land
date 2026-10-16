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

## Manufacturer O&M Guide — the unit's own limits (read in full 2026-10-08)

Intellishare **Operation & Maintenance Guide, ECO300 Electric Catox, N-24-2702A, November 2024**
(Drive file "2702A O&M..pdf", id `1qqTENyFo7jD_8s78MNC0i4n79xsgafET`, 52 pages). This is the
"catalytic oxidizer manual" the ISS-110 reply (Certify Log of Issues, Sep 2026) relied on. Quote it:

- §2.2: "Catalyst Ready Temperature: 550˚ F" · "Inlet Temperature Control Set Point: 600˚ F" ·
  "VOC Destruction Efficiency: >98%" · "Catalyst Inlet High Temperature Safety Set Point: 900˚ F" ·
  "Temperature High Limit Safety Set Point: 1100˚ F"
- §6.8: "Once set-point of 550 degrees F is reached on the TE1A an internal PLC 120 second timer is
  enabled to allow the oxidizer to stabilize. SVE/Oxidizer Ready is Enabled." Then: "Once the
  oxidizer is up to ready temperature the process inlet valve opens."
- §6.9: alarms "initiates an immediate shutdown"; inlet "above the alarm set-point of 900 degree F";
  outlet "above the alarm set-point of 1100 degree F". §6.11: "System temperature was lost for a 10
  minute period after operating temperature was reached."
- §8.1 "Heater Setpoint: 600°F", "Process Ready Temp: 500°F" (differs from §2.2's 550) · §8.2
  "Dilution Valve Setpoint: 800-900°F", "High Limit: 1100°F"
- §4.3 ¶6b (catalyst warranty): "at no time shall the catalyst outlet temperature be permitted to
  exceed 1200°F. Normal continuous operating temperature shall not exceed 1150°F for more than 15
  minutes during any 24 hours period."
- §2.5: "High Temperature Limit Control: Yokogawa" — a separate controller from the PLC that logs
  the temperatures, so logged values can sit a few degrees off the limit's own reading.
- §6.6 trend screen lists "INLET OPN%", "DILUT OPN%", "AIR FLOW", "ALARM REGISTER" — candidate
  signals for the blower/airflow indicator the verifier asked for in ISS-86 (Aug 2026).

"1,050°F" (used as an "upper limit" in the ISS-110 reply) appears nowhere in the guide except as a
gridline label on the §6.6 trend-screen picture. The earlier Intellishare proposal N-24-2702R1
(6/18/24, Drive "CATOX ENGINEERING SPECS.pdf") says "Minimum Catalyst Inlet Temperature: 600
degrees F." — pre-build; the O&M Guide is the document for the installed unit.

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

### One-train holds (added September 2026)

The all-channel check misses a hold on ONE train while the other keeps moving. The script now
also flags stretches of >=1 h where both sensors of one train repeat together with the outlet
at/above setpoint, prints the reading that follows, and recomputes the at-temperature share
without them. The tell is the release: a jump of hundreds of degrees in one 5-minute step is not
physical cooling (measured tandem declines run −29 to −56°F/h, above), so the held values were
stale.

September 2026 worked example, all Train 2: Sep 29 11:30–21:15 held 600/694°F, next reading
326/311°F; Sep 11 20:55–23:40 held 843/1008°F, next 676/729°F, then held again to Sep 12 00:55,
next 579/615°F; Sep 8 19:50–21:50 held 600/879°F, next 601/708°F. 192 readings (16 h) in total;
Train 2 at/above setpoint 55.1% as recorded, 54.1% without them. Holds at cold idle (~85–130°F)
that end in a 0–1°F step are ordinary deadband behaviour, not flagged.

Precedent for explaining these to the verifier: for August's Train 2 gaps and 66.6 h flatline,
Max asked in #mrv-ops-la whether *"these anomalies are likely the result of a temporary loss of
communication between the sensors and the PLC which was then identified and resolved by either
site staff or the ACE team?"* and Evan replied *"ya sure thats fair!"* (2026-09-09).

A frozen block is a **data-completeness** observation, not a compliance finding: compliance rests
on the sparging-blower interlock, not on the temperature record (see SKILL.md).

---

## Anomaly checks — run every period (added October 2026)

Printed after the stuck-reading check, for the chat report only. Limits and settings live in
`catox_config.json` (`manual_limits`, `anomaly_checks`). Lists longer than 20 lines are cut
short with a count of the rest.

1. **Time coverage.** Gaps in the timestamps (with the number of readings missing), repeated
   timestamps, and whether the file starts and ends at the period boundaries. A repeated 1 am
   hour on the November clock change is expected in Central-time exports and is labeled as such.
   July 2026 carries one reading past the period (Aug 01 00:01).
2. **Offline markers inside a run.** A stretch of ≤3 offline readings (`0`) with the same sensor
   above 200°F on both sides. A real shutdown leaves the unit cold, so this is a dropped reading
   the export labeled offline. The chart still shades it grey. Example: Jul 30 05:21, all four
   sensors read 0 for one reading between 386/392/701/1009°F and 371/369/661/838°F.
3. **Above the manufacturer's limits** (O&M Guide quotes above): inlet above 900°F, outlet
   above 1100°F, outlet above 1200°F, and outlet above 1150°F for more than 15 minutes in any
   rolling 24 hours. §2.5 puts the high-limit control on a separate controller from the logging
   PLC, so a logged value a few degrees over a limit doesn't show that the limit tripped. Report the value
   and time, and don't call it an alarm or a shutdown without the control-system log. Hits so far:
   June T1 outlet 1135°F (Jun 09 13:51) and 1111°F (Jun 29 20:21); September T2 inlet 901–903°F
   (Sep 13 10:20–11:05).
4. **Sudden outlet drops.** An outlet at or above 850°F falling 300°F or more within 30 minutes.
   Back-to-back falls are counted separately once the previous fall has landed, which gives
   32 (T1) / 28 (T2) for July against the 25 / 23 hand count above. The hand count's grouping rule
   wasn't recorded. A drop that follows repeated identical readings is marked: it may be a logger
   releasing a hold (the Jul 09 07:26 Train 2 case), not a real fall. Never label a drop a trip
   or an E-stop from temperature alone (see "Trips" above).

---

## Offline / Sentinel Convention

- **Current exports:** `0` = offline / no reading.
- **Legacy combined exports:** `-238` = sensor offline.

Both are converted to blank (NaN) and shown as grey shaded gaps in the charts. The processing
script handles both.
