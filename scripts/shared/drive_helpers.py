"""Common Drive + Sheets helpers used across automation functions."""
from __future__ import annotations

import hashlib
import io
import os
from typing import Any, Iterable, Optional

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .constants import TEMP_DIR


def list_folder(drive: Any, folder_id: str, *, query_extra: str = "") -> list[dict]:
    """List all files in a folder (not recursive). Returns [{id, name, mimeType}]."""
    q = f"'{folder_id}' in parents and trashed=false"
    if query_extra:
        q += f" and {query_extra}"

    files: list[dict] = []
    page_token = None
    while True:
        resp = drive.files().list(
            q=q,
            pageSize=200,
            fields="nextPageToken, files(id,name,mimeType,md5Checksum,size,modifiedTime)",
            pageToken=page_token,
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def find_child_folder(drive: Any, parent_id: str, name: str) -> Optional[dict]:
    """Find a subfolder by exact name. Returns None if not found."""
    files = list_folder(
        drive, parent_id,
        query_extra=f"mimeType='application/vnd.google-apps.folder' and name='{name}'",
    )
    return files[0] if files else None


def create_folder(drive: Any, parent_id: str, name: str) -> dict:
    """Create a folder under parent_id. Returns {id, name}."""
    meta = {
        "name": name,
        "parents": [parent_id],
        "mimeType": "application/vnd.google-apps.folder",
    }
    return drive.files().create(body=meta, fields="id,name").execute()


def ensure_folder(drive: Any, parent_id: str, name: str) -> dict:
    """Find folder by name, create if missing. Idempotent."""
    existing = find_child_folder(drive, parent_id, name)
    if existing:
        return existing
    return create_folder(drive, parent_id, name)


def create_sheet(drive: Any, parent_id: str, name: str) -> dict:
    """Create a Google Sheet inside a folder. Returns {id, name, webViewLink}."""
    meta = {
        "name": name,
        "parents": [parent_id],
        "mimeType": "application/vnd.google-apps.spreadsheet",
    }
    return drive.files().create(body=meta, fields="id,name,webViewLink").execute()


def copy_sheet(drive: Any, source_id: str, parent_id: str, new_name: str) -> dict:
    """Copy an existing Google Sheet into target folder with new name."""
    return drive.files().copy(
        fileId=source_id,
        body={"name": new_name, "parents": [parent_id]},
        fields="id,name,webViewLink",
    ).execute()


def download_file(drive: Any, file_id: str, local_path: str) -> str:
    """Download a Drive file (any binary type) to local_path. Returns local_path."""
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    request = drive.files().get_media(fileId=file_id)
    fh = io.FileIO(local_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.close()
    return local_path


def upload_file_to_folder(
    drive: Any,
    local_path: str,
    parent_id: str,
    *,
    name: Optional[str] = None,
    mimetype: str = "application/pdf",
) -> dict:
    """Upload a local file to a Drive folder. Returns {id, name, webViewLink}."""
    upload_name = name or os.path.basename(local_path)
    media = MediaFileUpload(local_path, mimetype=mimetype, resumable=False)
    meta = {"name": upload_name, "parents": [parent_id]}
    return drive.files().create(
        body=meta, media_body=media, fields="id,name,webViewLink,md5Checksum"
    ).execute()


def file_exists_in_folder(
    drive: Any, parent_id: str, name: str, *, check_md5_of: Optional[str] = None
) -> Optional[dict]:
    """Return matching file if one exists with exact name.

    If check_md5_of is a local path, only match if md5 also matches (prevents
    duplicate uploads of the same PDF with the same name).
    """
    files = list_folder(drive, parent_id, query_extra=f"name='{name}'")
    if not files:
        return None
    if not check_md5_of:
        return files[0]
    local_md5 = _md5_file(check_md5_of)
    for f in files:
        if f.get("md5Checksum") == local_md5:
            return f
    return None


def _md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --- Sheets helpers ---

def read_range(sheets: Any, sheet_id: str, a1_range: str) -> list[list[Any]]:
    """Read a range as a 2D list. Returns [] if empty."""
    resp = sheets.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=a1_range
    ).execute()
    return resp.get("values", [])


def read_all(sheets: Any, sheet_id: str, tab: str, *, cols: str = "A:Z") -> list[list[Any]]:
    """Read the full tab data range."""
    return read_range(sheets, sheet_id, f"'{tab}'!{cols}")


def write_values(
    sheets: Any,
    sheet_id: str,
    updates: list[dict],
    *,
    value_input_option: str = "USER_ENTERED",
) -> dict:
    """Batch-write values. Each update is {range, values}.

    Use value_input_option='USER_ENTERED' so '=' prefixed strings become formulas.
    """
    return sheets.spreadsheets().values().batchUpdate(
        spreadsheetId=sheet_id,
        body={"valueInputOption": value_input_option, "data": updates},
    ).execute()


def apply_row_format(
    sheets: Any,
    sheet_id: str,
    *,
    tab_sheet_id: int = 0,
    row_index_1based: int,
    start_col: int = 0,
    end_col: int = 10,
    bold: bool = True,
    bg_color: Optional[dict] = None,
) -> dict:
    """Apply bold + background color to a single row, cols start_col:end_col."""
    return sheets.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": [{
            "repeatCell": {
                "range": {
                    "sheetId": tab_sheet_id,
                    "startRowIndex": row_index_1based - 1,
                    "endRowIndex": row_index_1based,
                    "startColumnIndex": start_col,
                    "endColumnIndex": end_col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": bold},
                        "backgroundColor": bg_color or {"red": 1.0, "green": 0.949, "blue": 0.8},
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold,backgroundColor)",
            }
        }]},
    ).execute()
