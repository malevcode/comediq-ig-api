#!/usr/bin/env python3
"""
Prepare public draft-list codes for Instagram comment corrections.

The generated JSON lets collect_instagram_comments.py map post comments back to
open_mics_historical.unique_identifier. The generated CSV is a posting/review
source with a public comment code next to each mic.
"""

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


DEFAULT_MAPPING_FILE = "instagram_draft_mic_mapping.json"
DEFAULT_DRAFT_CSV = "instagram_draft_list.csv"


def clean_text(value: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def normalize_instagram_handle(value: Any) -> str:
    text = clean_text(value).lstrip("@")
    match = re.search(r"([A-Za-z0-9._]{3,30})", text)
    return match.group(1).lower() if match else ""


def make_public_code(mic_id: str, used_codes: set) -> str:
    seed = str(mic_id)
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest().upper()
    for length in (6, 7, 8, 10):
        code = f"OM{digest[:length]}"
        if code not in used_codes:
            used_codes.add(code)
            return code
    suffix = len(used_codes) + 1
    code = f"OM{digest[:8]}{suffix}"
    used_codes.add(code)
    return code


def row_context(row: pd.Series, code: str) -> Dict[str, str]:
    return {
        "draft_code": code,
        "unique_identifier": clean_text(row.get("unique_identifier")),
        "open_mic": clean_text(row.get("open_mic")),
        "day": clean_text(row.get("day")),
        "start_time": clean_text(row.get("start_time")),
        "venue_name": clean_text(row.get("venue_name")),
        "location": clean_text(row.get("location")),
        "instagram_handle": normalize_instagram_handle(row.get("changes_updates")),
    }


def build_mapping(df: pd.DataFrame) -> Dict[str, Any]:
    used_codes = set()
    codes: Dict[str, List[str]] = {}
    usernames: Dict[str, List[str]] = {}
    mics: Dict[str, Dict[str, str]] = {}
    draft_rows = []

    for _, row in df.iterrows():
        mic_id = clean_text(row.get("unique_identifier"))
        if not mic_id:
            continue

        code = make_public_code(mic_id, used_codes)
        context = row_context(row, code)
        codes[code] = [mic_id]
        mics[mic_id] = context
        draft_rows.append(context)

        handle = context["instagram_handle"]
        if handle:
            usernames.setdefault(handle, []).append(mic_id)

    return {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_mics": len(mics),
            "instructions": (
                "Publish draft_code next to each mic. Ask hosts to include that code "
                "when commenting corrections, e.g. 'OMABC123 starts at 8 PM'."
            ),
        },
        "codes": codes,
        "usernames": usernames,
        "mics": mics,
        "draft_rows": draft_rows,
    }


def write_draft_csv(mapping: Dict[str, Any], output_csv: str) -> None:
    rows = mapping.get("draft_rows") or []
    columns = [
        "draft_code",
        "open_mic",
        "day",
        "start_time",
        "venue_name",
        "location",
        "instagram_handle",
        "unique_identifier",
    ]
    pd.DataFrame(rows, columns=columns).to_csv(output_csv, index=False)


def main():
    parser = argparse.ArgumentParser(description="Create Instagram draft comment-code mapping")
    parser.add_argument("csv_file", help="Current open mics CSV/export")
    parser.add_argument("--mapping-output", default=DEFAULT_MAPPING_FILE)
    parser.add_argument("--draft-csv-output", default=DEFAULT_DRAFT_CSV)
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file, dtype=str, keep_default_na=False)
    if "unique_identifier" not in df.columns:
        raise SystemExit("CSV must include unique_identifier")

    mapping = build_mapping(df)
    Path(args.mapping_output).write_text(json.dumps(mapping, indent=2) + "\n")
    write_draft_csv(mapping, args.draft_csv_output)

    print("=" * 70)
    print("INSTAGRAM DRAFT COMMENT MAPPING")
    print("=" * 70)
    print(f"Mics mapped: {mapping['metadata']['total_mics']}")
    print(f"Mapping JSON: {args.mapping_output}")
    print(f"Draft CSV: {args.draft_csv_output}")
    print("\nAsk hosts to comment with the code shown next to their mic, for example:")
    print("  OMABC123 now starts at 8 PM")
    print("=" * 70)


if __name__ == "__main__":
    main()
