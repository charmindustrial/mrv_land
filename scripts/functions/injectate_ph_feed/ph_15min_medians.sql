-- 15-minute injectate pH medians for one closed Saturday-to-Saturday week
-- (America/Chicago), for the Mangrove inline pH data feed.
--
-- Each raw PH-1041 reading (~5 s) is tagged with the latest StateRun value; only
-- readings with StateRun = 1 (line injecting) and dataintegrity = 192 count.
-- One row per 15-min interval that has any such readings; intervals with no
-- injection produce no row.
--
-- Both tags are resolved by TAGPATH, never by tagid: the Ignition edge node
-- re-registers tags and PH-1041 alone maps to ~60 tagids.
--
-- Cost: sqlt_data_3_* is not partitioned or clustered, so only the
-- _TABLE_SUFFIX filter limits bytes scanned (~2 GB per month table touched).
--
-- Param: @week_start DATE — the Saturday that opens the week.
WITH win AS (
  SELECT TIMESTAMP(DATETIME(@week_start), 'America/Chicago') AS w_start,
         TIMESTAMP(DATETIME(DATE_ADD(@week_start, INTERVAL 7 DAY)), 'America/Chicago') AS w_end
),
tags AS (
  SELECT id, LOWER(tagpath) AS tagpath
  FROM `prod-data-warehouse-487604.dataset_ignition_scada_uscentral1.sqlth_te`
  WHERE LOWER(tagpath) IN (
    'edge nodes/bascosite/1000-injection/1000-common/ph-1041/value',
    'edge nodes/bascosite/1000-injection/1000-common/sm_injection_common/status/staterun'
  )
),
raw AS (
  SELECT TIMESTAMP_MILLIS(CAST(d.t_stamp AS INT64)) AS ts,
         IF(t.tagpath LIKE '%/ph-1041/value', d.floatvalue, NULL) AS ph,
         IF(t.tagpath LIKE '%/staterun', CAST(d.intvalue AS INT64), NULL) AS run
  FROM `prod-data-warehouse-487604.dataset_ignition_scada_uscentral1.sqlt_data_3_*` d
  JOIN tags t ON d.tagid = t.id, win
  -- One day of lookback so the first readings of the week inherit a StateRun.
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y_%m', DATE_SUB(@week_start, INTERVAL 1 DAY))
                          AND FORMAT_DATE('%Y_%m', DATE_ADD(@week_start, INTERVAL 7 DAY))
    AND d.dataintegrity = 192
    AND TIMESTAMP_MILLIS(CAST(d.t_stamp AS INT64)) >= TIMESTAMP_SUB(w_start, INTERVAL 1 DAY)
    AND TIMESTAMP_MILLIS(CAST(d.t_stamp AS INT64)) < w_end
),
tagged AS (
  SELECT ts, ph,
         LAST_VALUE(run IGNORE NULLS) OVER (ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS run
  FROM raw
),
gated AS (
  SELECT TIMESTAMP_BUCKET(ts, INTERVAL 15 MINUTE) AS bucket, ph
  FROM tagged, win
  WHERE ph IS NOT NULL AND run = 1 AND ts >= w_start AND ts < w_end
),
per_bucket AS (
  SELECT DISTINCT bucket,
         PERCENTILE_CONT(ph, 0.5) OVER (PARTITION BY bucket) AS med,
         COUNT(*) OVER (PARTITION BY bucket) AS n
  FROM gated
)
SELECT FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%S%Ez', bucket, 'America/Chicago') AS window_start,
       FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%S%Ez', TIMESTAMP_ADD(bucket, INTERVAL 15 MINUTE), 'America/Chicago') AS window_end,
       ROUND(med, 2) AS ph_median,
       n AS n_readings   -- logged, not posted
FROM per_bucket
ORDER BY bucket
