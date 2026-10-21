"""Injection-week arithmetic.

A week runs Saturday 00:00 -> Saturday 00:00, America/Chicago (the same window as
the INJ-MM-YYYY-Wx Ops Notes). Pure functions, no GCP dependencies, so they are
unit-testable locally.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")
SATURDAY = 5  # date.weekday(): Mon=0 ... Sat=5


def last_closed_week_start(now: datetime) -> date:
    """The Saturday that opens the most recent week fully closed by `now`.

    Run Saturday 02:00 CT -> the week that ended at 00:00 that morning.
    """
    today = now.astimezone(TZ).date()
    days_since_saturday = (today.weekday() - SATURDAY) % 7
    return today - timedelta(days=days_since_saturday + 7)


def week_bounds(week_start: date) -> tuple[datetime, datetime]:
    """Local-midnight bounds of the week, as aware datetimes (DST-safe)."""
    start = datetime(week_start.year, week_start.month, week_start.day, tzinfo=TZ)
    end_day = week_start + timedelta(days=7)
    end = datetime(end_day.year, end_day.month, end_day.day, tzinfo=TZ)
    return start, end


def parse_week_start(value: str) -> date:
    """Parse YYYY-MM-DD and require a Saturday."""
    try:
        d = date.fromisoformat(value)
    except ValueError as e:
        raise ValueError(f'week_start must be YYYY-MM-DD, got "{value}"') from e
    if d.weekday() != SATURDAY:
        raise ValueError(f"week_start must be a Saturday, got {value}")
    return d
