"""Gmail helpers for search, message read, and attachment download.

Uses domain-wide delegation — service account impersonates the configured user.
"""
from __future__ import annotations

import base64
import os
from typing import Any, Iterable

from .constants import TEMP_DIR


def search_messages(gmail: Any, query: str, *, max_results: int = 50) -> list[dict]:
    """Search Gmail and return a list of message stubs [{id, threadId}]."""
    resp = gmail.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    return resp.get("messages", [])


def search_unique_threads(gmail: Any, queries: Iterable[str], *, max_per_query: int = 50) -> list[str]:
    """Run multiple queries and return the deduped set of thread IDs."""
    seen: set[str] = set()
    for q in queries:
        for msg in search_messages(gmail, q, max_results=max_per_query):
            tid = msg.get("threadId")
            if tid:
                seen.add(tid)
    return list(seen)


def get_thread(gmail: Any, thread_id: str) -> dict:
    return gmail.users().threads().get(userId="me", id=thread_id, format="full").execute()


def get_message(gmail: Any, message_id: str) -> dict:
    return gmail.users().messages().get(userId="me", id=message_id, format="full").execute()


def iter_pdf_attachments(message: dict) -> Iterable[tuple[str, str]]:
    """Yield (filename, attachmentId) for every PDF attachment in a message."""
    parts = message.get("payload", {}).get("parts", []) or []
    queue = list(parts)
    while queue:
        part = queue.pop()
        if part.get("parts"):
            queue.extend(part["parts"])
            continue
        filename = part.get("filename") or ""
        mime = part.get("mimeType", "")
        att_id = part.get("body", {}).get("attachmentId")
        if att_id and (filename.lower().endswith(".pdf") or mime == "application/pdf"):
            yield filename, att_id


def download_attachment(
    gmail: Any, message_id: str, attachment_id: str, local_path: str
) -> str:
    """Download an attachment to local_path. Returns local_path."""
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    att = gmail.users().messages().attachments().get(
        userId="me", messageId=message_id, id=attachment_id
    ).execute()
    data = base64.urlsafe_b64decode(att["data"])
    with open(local_path, "wb") as f:
        f.write(data)
    return local_path


def list_pdfs_in_recent_threads(
    gmail: Any, queries: Iterable[str], *, download_dir: str = f"{TEMP_DIR}/gmail_pdfs"
) -> list[dict]:
    """High-level: search, find PDFs, download them all.

    Returns [{thread_id, message_id, filename, local_path}].
    """
    os.makedirs(download_dir, exist_ok=True)
    results: list[dict] = []
    thread_ids = search_unique_threads(gmail, queries)
    seen_attachments: set[tuple[str, str]] = set()
    for tid in thread_ids:
        thread = get_thread(gmail, tid)
        for msg in thread.get("messages", []):
            msg_id = msg["id"]
            for filename, att_id in iter_pdf_attachments(msg):
                key = (filename, att_id)
                if key in seen_attachments:
                    continue
                seen_attachments.add(key)
                safe_name = filename.replace("/", "_").replace(" ", "_") or f"{att_id}.pdf"
                local_path = os.path.join(download_dir, f"{msg_id}_{safe_name}")
                download_attachment(gmail, msg_id, att_id, local_path)
                results.append({
                    "thread_id": tid,
                    "message_id": msg_id,
                    "filename": filename,
                    "local_path": local_path,
                })
    return results
