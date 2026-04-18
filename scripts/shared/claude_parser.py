"""Claude API wrapper for the LLM-dependent parts of the MRV automation.

Used for parsing SGS Certificate of Analysis PDFs (extract carbon%, client ID, etc.)
and for reading scale ticket images (photos of photos, messy inputs).

Requires ANTHROPIC_API_KEY env var. Model: claude-sonnet-4-6 by default.
"""
from __future__ import annotations

import base64
import json
import os
from typing import Any

from anthropic import Anthropic

DEFAULT_MODEL = "claude-sonnet-4-6"


def _client() -> Anthropic:
    return Anthropic()  # reads ANTHROPIC_API_KEY from env


def parse_sgs_coa_pdf(pdf_path: str, *, model: str = DEFAULT_MODEL) -> list[dict]:
    """Parse a multi-page SGS CoA PDF. Returns one dict per sample (page).

    Each sample dict contains:
      {certificate_number, client_id, fraction, carbon_pct, hydrogen_pct,
       nitrogen_pct, sampled_date, analyzed_date}

    Values may be None if not extractable on that page.
    """
    with open(pdf_path, "rb") as f:
        pdf_b64 = base64.standard_b64encode(f.read()).decode()

    system_prompt = (
        "You are extracting structured data from a multi-page SGS Certificate of "
        "Analysis PDF. Each page is one sample. Return a JSON array with one "
        "object per page.\n\n"
        "Schema per object:\n"
        "  certificate_number: string like 'SR26-XXXXX.NNN'\n"
        "  client_id: full CLIENT ID field (e.g. 'BATCH 2-186' or '301047 WODO')\n"
        "  fraction: 'QOWV' or 'WODO' if present in CLIENT ID, else null\n"
        "  carbon_pct: float (from Carbon row, % m/m column)\n"
        "  hydrogen_pct: float\n"
        "  nitrogen_pct: string (may be literal like '<0.75')\n"
        "  sampled_date: ISO date string\n"
        "  analyzed_date: ISO date string\n\n"
        "If a field can't be read clearly, set it to null. Do NOT guess. "
        "Return ONLY valid JSON — no markdown, no commentary."
    )

    resp = _client().messages.create(
        model=model,
        max_tokens=8192,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64,
                    },
                },
                {"type": "text", "text": "Extract every sample. Return the JSON array."},
            ],
        }],
    )

    text = resp.content[0].text.strip()
    # Strip ```json fences if the model added them
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)


def parse_scale_ticket(image_or_pdf_path: str, *, model: str = DEFAULT_MODEL) -> dict:
    """Parse a single scale ticket image or PDF. Handles phone photos of photos.

    Returns:
      {gross_weight_lbs: int|None, tare_weight_lbs: int|None, net_weight_lbs: int|None,
       ticket_number: str|None, date: str|None, scale_location: str|None,
       ticket_type: 'full'|'empty'|'unknown', confidence: 'high'|'medium'|'low'}
    """
    ext = os.path.splitext(image_or_pdf_path)[1].lower()
    with open(image_or_pdf_path, "rb") as f:
        data_b64 = base64.standard_b64encode(f.read()).decode()

    if ext == ".pdf":
        media = {
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": data_b64},
        }
    else:
        media_type = {
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp", ".gif": "image/gif",
        }.get(ext, "image/jpeg")
        media = {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": data_b64},
        }

    system_prompt = (
        "Extract data from a truck scale ticket. Tickets can be PDF printouts "
        "or phone photos (sometimes photos of photos — do your best).\n\n"
        "Return ONE JSON object:\n"
        "  gross_weight_lbs: int (the heaviest weight — full truck)\n"
        "  tare_weight_lbs: int (the lightest weight — empty truck)\n"
        "  net_weight_lbs: int (gross - tare, verify if printed)\n"
        "  ticket_number: string\n"
        "  date: ISO date string\n"
        "  scale_location: string (e.g. 'Pilot Travel Center, Bunkie LA')\n"
        "  ticket_type: 'full' if loaded/gross only, 'empty' if tare only, 'both' if both\n"
        "  confidence: 'high' | 'medium' | 'low' — based on legibility\n\n"
        "If a field can't be read, set null. Don't guess. Return ONLY valid JSON."
    )

    resp = _client().messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [
                media,
                {"type": "text", "text": "Extract the scale data. Return JSON."},
            ],
        }],
    )

    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)
