"""scale_ticket_sweep Cloud Function.

TODO — sweep every current-RP batch's Scale Tickets/ folder. For each new scale
ticket file, parse via Claude API (handles phone photos of photos), write
loaded/unloaded lbs into that batch's ops notes. Skip if cells already populated.

Key rules:
- Current period only
- For rail: write to the highlighted current offload row (find row by format query)
- For truck: write to B14 (Truck 1 Full Mass) / C14 (Truck 1 Empty Mass)
- Never overwrite existing values
- Flag unreadable tickets, don't guess
"""
from __future__ import annotations

import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def scale_ticket_sweep(request) -> tuple[str, int]:
    summary = run()
    return json.dumps(summary, default=str), 200


def run() -> dict:
    log.warning("scale_ticket_sweep not yet implemented — returning stub")
    return {"status": "not_implemented"}


if __name__ == "__main__":
    print(json.dumps(run(), default=str, indent=2))
