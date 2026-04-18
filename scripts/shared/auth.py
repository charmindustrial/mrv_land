"""Service account authentication for Drive/Sheets/Gmail.

Drive + Sheets: direct service account auth. The service account must be granted
Editor access to the target folders/sheets (share them with the SA email address).

Gmail: requires domain-wide delegation. The service account impersonates a human
user (GMAIL_IMPERSONATE_USER) to read that user's mailbox. Setup requires a
Workspace admin to authorize the SA's client ID in the admin console with the
gmail.readonly + gmail.modify scopes.

Credentials are loaded from either:
  1. GOOGLE_APPLICATION_CREDENTIALS env var (local dev with a JSON key file)
  2. Application Default Credentials (Cloud Function auto-attaches SA)
  3. Secret Manager (Cloud Function reads SA_KEY secret at startup)
"""
from __future__ import annotations

import json
import os
from typing import Any

from google.auth import default as google_auth_default
from google.oauth2 import service_account
from googleapiclient.discovery import build

from .constants import GMAIL_IMPERSONATE_USER

SCOPES_DRIVE = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
SCOPES_GMAIL = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


def _load_sa_credentials() -> service_account.Credentials:
    """Load service account credentials from env var, Secret Manager, or ADC."""
    sa_key_json = os.environ.get("SA_KEY")
    if sa_key_json:
        info = json.loads(sa_key_json)
        return service_account.Credentials.from_service_account_info(info)

    sa_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_key_path and os.path.exists(sa_key_path):
        return service_account.Credentials.from_service_account_file(sa_key_path)

    creds, _ = google_auth_default()
    return creds


def get_drive_services() -> dict[str, Any]:
    """Return Drive and Sheets API clients authenticated as the service account.

    Requires the service account to have Editor access (Drive) or Read access (Sheets)
    on target folders/sheets.
    """
    creds = _load_sa_credentials()
    scoped = creds.with_scopes(SCOPES_DRIVE) if hasattr(creds, "with_scopes") else creds
    return {
        "drive": build("drive", "v3", credentials=scoped, cache_discovery=False),
        "sheets": build("sheets", "v4", credentials=scoped, cache_discovery=False),
    }


def get_gmail_service(impersonate_user: str = GMAIL_IMPERSONATE_USER) -> Any:
    """Return Gmail API client that impersonates the given user.

    Uses domain-wide delegation. The service account must be authorized in
    Google Workspace admin console with gmail.readonly + gmail.modify scopes
    before this will work.
    """
    creds = _load_sa_credentials()
    if not hasattr(creds, "with_subject"):
        raise RuntimeError(
            "Service account credentials required for Gmail impersonation. "
            "Default credentials don't support with_subject."
        )
    delegated = creds.with_scopes(SCOPES_GMAIL).with_subject(impersonate_user)
    return build("gmail", "v1", credentials=delegated, cache_discovery=False)
