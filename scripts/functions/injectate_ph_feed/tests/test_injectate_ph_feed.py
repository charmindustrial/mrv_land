"""Unit tests — no GCP or Mangrove access needed.

Run: python -m unittest discover -s scripts/functions/injectate_ph_feed/tests
"""
from __future__ import annotations

import sys
import types
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

FN_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FN_DIR))

# main.py imports the GCP + HTTP clients at module load; stub them so the pure
# logic is testable without installing them.
for name in ("requests", "google", "google.cloud", "google.cloud.bigquery"):
    sys.modules.setdefault(name, types.ModuleType(name))
sys.modules["google.cloud"].bigquery = sys.modules["google.cloud.bigquery"]

import main  # noqa: E402
from week import last_closed_week_start, parse_week_start, week_bounds  # noqa: E402


def utc(*a):
    return datetime(*a, tzinfo=timezone.utc)


class WeekTests(unittest.TestCase):
    def test_saturday_run_targets_week_that_just_closed(self):
        # Sat 2026-10-10 07:00Z = 02:00 CDT
        self.assertEqual(last_closed_week_start(utc(2026, 10, 10, 7)), date(2026, 10, 3))

    def test_midweek_run_targets_previous_full_week(self):
        self.assertEqual(last_closed_week_start(utc(2026, 10, 14, 15)), date(2026, 10, 3))

    def test_still_friday_in_chicago(self):
        # 2026-10-10 03:00Z = Fri 10/09 22:00 CDT
        self.assertEqual(last_closed_week_start(utc(2026, 10, 10, 3)), date(2026, 9, 26))

    def test_bounds_are_chicago_midnights(self):
        start, end = week_bounds(date(2026, 8, 22))
        self.assertEqual(start.astimezone(timezone.utc), utc(2026, 8, 22, 5))
        self.assertEqual(end.astimezone(timezone.utc), utc(2026, 8, 29, 5))

    def test_dst_fall_back_week(self):
        start, end = week_bounds(date(2026, 10, 31))
        self.assertEqual(start.astimezone(timezone.utc), utc(2026, 10, 31, 5))
        self.assertEqual(end.astimezone(timezone.utc), utc(2026, 11, 7, 6))

    def test_week_start_must_be_saturday(self):
        self.assertEqual(parse_week_start("2026-10-03"), date(2026, 10, 3))
        with self.assertRaisesRegex(ValueError, "Saturday"):
            parse_week_start("2026-10-04")
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            parse_week_start("10/03/2026")


class CsvTests(unittest.TestCase):
    def test_header_matches_feed_and_drops_n_readings(self):
        out = main.to_feed_csv([{
            "window_start": "2026-10-03T00:00:00-05:00",
            "window_end": "2026-10-03T00:15:00-05:00",
            "ph_median": 2.99, "n_readings": 180,
        }])
        self.assertEqual(out, "window_start,window_end,ph_median\n"
                              "2026-10-03T00:00:00-05:00,2026-10-03T00:15:00-05:00,2.99\n")

    def test_missing_median_fails_instead_of_posting_zero(self):
        with self.assertRaisesRegex(ValueError, "missing ph_median"):
            main.to_feed_csv([{"window_start": "x", "window_end": "y", "ph_median": None}])


class RunTests(unittest.TestCase):
    ROWS = [{"window_start": "a", "window_end": "b", "ph_median": 3.0, "n_readings": 10}]
    NOW = utc(2026, 10, 14, 15)

    def test_skips_week_already_in_mangrove(self):
        with mock.patch.object(main, "query_week", return_value=self.ROWS), \
             mock.patch.object(main, "events_in_window", return_value=[{"id": "evt_x"}]), \
             mock.patch.object(main, "submit_data_feed") as submit:
            out = main.run(now=self.NOW)
        self.assertEqual(out["status"], "skipped-existing")
        submit.assert_not_called()

    def test_dry_run_never_uploads(self):
        with mock.patch.object(main, "query_week", return_value=self.ROWS), \
             mock.patch.object(main, "events_in_window", return_value=[]), \
             mock.patch.object(main, "submit_data_feed") as submit:
            out = main.run(week_start="2026-10-03", dry_run=True, now=self.NOW)
        self.assertEqual(out["status"], "dry-run")
        submit.assert_not_called()

    def test_no_injection_posts_nothing(self):
        with mock.patch.object(main, "query_week", return_value=[]), \
             mock.patch.object(main, "events_in_window") as ev, \
             mock.patch.object(main, "submit_data_feed") as submit:
            out = main.run(now=self.NOW)
        self.assertEqual(out["status"], "no-injection")
        ev.assert_not_called()
        submit.assert_not_called()

    def test_open_week_is_refused(self):
        with self.assertRaisesRegex(ValueError, "not closed"):
            main.run(week_start="2026-10-10", now=self.NOW)

    def test_live_run_submits(self):
        with mock.patch.object(main, "query_week", return_value=self.ROWS), \
             mock.patch.object(main, "events_in_window", return_value=[]), \
             mock.patch.object(main, "submit_data_feed", return_value={"pipeline_run": {"id": "run_1"}}) as submit:
            out = main.run(week_start="2026-10-03", now=self.NOW)
        self.assertEqual(out["status"], "submitted")
        self.assertEqual(out["pipeline_run"], "run_1")
        submit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
