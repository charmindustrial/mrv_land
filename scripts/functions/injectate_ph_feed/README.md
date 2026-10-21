# injectate_ph_feed

Weekly inline pH (PH-1041) from the SCADA historian → Mangrove.

## What it does

- Cloud Scheduler calls it **Saturdays 01:00 America/Denver (02:00 Central)**.
- Takes the Sat 00:00 → Sat 00:00 (America/Chicago) injection week that just closed.
- Queries `prod-data-warehouse-487604.dataset_ignition_scada_uscentral1.sqlt_data_3_*`
  ([`ph_15min_medians.sql`](ph_15min_medians.sql)): readings with `dataintegrity = 192`
  while **StateRun = 1** (line injecting), one **median per 15-minute interval**.
  Intervals with no injection produce no row.
- Uploads `window_start, window_end, ph_median` as CSV to the Mangrove data feed
  `ph_measurement_basco` (`datafd_Mfl1UtLkC3uRvsRx`). The feed turns each row into one
  **Inline pH measurement** event; Mangrove's weekly batch averages them.

Checked against live BigQuery for the week of 2026-10-03: 27 intervals, 4,152 readings,
mean of medians 2.993 (StateRun-gated weekly median 2.999).

## Guard rails

| Guard | Why |
|---|---|
| Skips a week that already has any `inline-ph-measurement` event | The feed sets no tracking_id; a second upload double-counts the week |
| No Scheduler retries | The upload is processed async; a fast retry could race the check above |
| Tags resolved by tagpath, never tagid | The Ignition edge node re-registers tags; PH-1041 alone has ~60 tagids |
| A week with no injection posts nothing | Returns `no-injection`, not an error |
| Missing median → error | Never posts a blank as pH 0 |

## Manual run / backfill

The scheduled run only does the week that just closed. Earlier weeks are run by hand:

```bash
URL=$(gcloud functions describe injectate_ph_feed --project=charm-mrv --region=us-central1 --format='value(serviceConfig.uri)')
curl -X POST "$URL" -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" -d '{"week_start":"2026-10-03","dry_run":true}'
```

`week_start` must be a Saturday. Drop `dry_run` to upload.

Locally (needs `pip install -r requirements.txt`, BigQuery access via ADC, and `MANGROVE_TOKEN`):
`python main.py 2026-10-03` — always a dry run.

## Deploy

```bash
./scripts/deploy/deploy_function.sh injectate_ph_feed
./scripts/deploy/create_scheduler_jobs.sh
```

Needs [gcp-setup.md](../../docs/gcp-setup.md) Step 7b first (BigQuery grants + `mangrove-api-token`).

## Tests

```bash
python -m unittest discover -s scripts/functions/injectate_ph_feed/tests
```

Week boundaries (including DST), CSV shape, and the run guards. No GCP access needed.

## Cost

`sqlt_data_3_*` is not partitioned; each run scans the one or two month tables the week
touches (~1.7 GB each, about 1¢ per run).
