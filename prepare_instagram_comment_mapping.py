#!/usr/bin/env python3
"""
Prepare internal Instagram username mapping for public-post comment corrections.

The generated JSON lets collect_instagram_comments.py map commenters back to
open_mics_historical.unique_identifier without adding public codes to posters.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv


DEFAULT_MAPPING_FILE = "instagram_comment_mic_mapping.json"
DEFAULT_REVIEW_CSV = "instagram_comment_mic_mapping_review.csv"
DEFAULT_TABLE = "open_mics_historical"
SUPABASE_COLUMNS = [
    "unique_identifier",
    "open_mic",
    "day",
    "start_time",
    "venue_name",
    "location",
    "changes_updates",
]


def clean_text(value: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def normalize_instagram_handle(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""

    if "@" in text:
        match = re.search(r"@([A-Za-z0-9._]{3,30})\b", text)
        return match.group(1).lower() if match else ""

    match = re.search(r"\b([A-Za-z0-9._]{3,30})\b", text)
    return match.group(1).lower() if match else ""


def row_context(row: pd.Series) -> Dict[str, str]:
    return {
        "unique_identifier": clean_text(row.get("unique_identifier")),
        "open_mic": clean_text(row.get("open_mic")),
        "day": clean_text(row.get("day")),
        "start_time": clean_text(row.get("start_time")),
        "venue_name": clean_text(row.get("venue_name")),
        "location": clean_text(row.get("location")),
        "instagram_handle": normalize_instagram_handle(row.get("changes_updates")),
    }


def build_mapping(df: pd.DataFrame) -> Dict[str, Any]:
    usernames: Dict[str, List[str]] = {}
    mics: Dict[str, Dict[str, str]] = {}
    review_rows = []

    for _, row in df.iterrows():
        context = row_context(row)
        mic_id = context["unique_identifier"]
        handle = context["instagram_handle"]
        if not mic_id:
            continue

        mics[mic_id] = context
        if handle:
            usernames.setdefault(handle, []).append(mic_id)
            review_rows.append({
                **context,
                "mic_count_for_handle": 0,
                "mapping_note": "",
            })

    for row in review_rows:
        mic_count = len(usernames.get(row["instagram_handle"], []))
        row["mic_count_for_handle"] = mic_count
        if mic_count > 1:
            row["mapping_note"] = "multiple_mics_for_commenter"

    return {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_mics": len(mics),
            "total_usernames": len(usernames),
            "multi_mic_usernames": sum(1 for mic_ids in usernames.values() if len(mic_ids) > 1),
            "instructions": (
                "Internal mapping only. Comments are matched by commenter username. "
                "Single-mic usernames can be processed directly; correction comments "
                "from multi-mic usernames are queued for review with candidate mics."
            ),
        },
        "usernames": usernames,
        "mics": mics,
        "review_rows": review_rows,
    }


def write_review_csv(mapping: Dict[str, Any], output_csv: str) -> None:
    rows = mapping.get("review_rows") or []
    columns = [
        "instagram_handle",
        "mic_count_for_handle",
        "mapping_note",
        "open_mic",
        "day",
        "start_time",
        "venue_name",
        "location",
        "unique_identifier",
    ]
    pd.DataFrame(rows, columns=columns).to_csv(output_csv, index=False)


def load_supabase_dataframe(table: str) -> pd.DataFrame:
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise SystemExit("Missing SUPABASE_URL or SUPABASE_KEY")

    from supabase import create_client

    supabase = create_client(url, key)
    rows = []
    page_size = 1000
    start = 0

    while True:
        end = start + page_size - 1
        response = (
            supabase.table(table)
            .select(",".join(SUPABASE_COLUMNS))
            .range(start, end)
            .execute()
        )
        batch = response.data or []
        rows.extend(batch)
        if len(batch) < page_size:
            break
        start += page_size

    return pd.DataFrame(rows, columns=SUPABASE_COLUMNS)


def main():
    parser = argparse.ArgumentParser(description="Create internal Instagram username comment mapping")
    parser.add_argument("csv_file", nargs="?", help="Current open mics CSV/export")
    parser.add_argument(
        "--from-supabase",
        action="store_true",
        help="Build mapping from Supabase instead of a CSV file.",
    )
    parser.add_argument("--table", default=DEFAULT_TABLE)
    parser.add_argument("--mapping-output", default=DEFAULT_MAPPING_FILE)
    parser.add_argument("--review-csv-output", default=DEFAULT_REVIEW_CSV)
    args = parser.parse_args()

    if args.from_supabase:
        df = load_supabase_dataframe(args.table)
    elif args.csv_file:
        df = pd.read_csv(args.csv_file, dtype=str, keep_default_na=False)
    else:
        raise SystemExit("Pass csv_file or --from-supabase")

    if "unique_identifier" not in df.columns:
        raise SystemExit("CSV must include unique_identifier")

    mapping = build_mapping(df)
    Path(args.mapping_output).write_text(json.dumps(mapping, indent=2) + "\n")
    write_review_csv(mapping, args.review_csv_output)

    metadata = mapping["metadata"]
    print("=" * 70)
    print("INSTAGRAM COMMENT USERNAME MAPPING")
    print("=" * 70)
    print(f"Mics mapped: {metadata['total_mics']}")
    print(f"Instagram usernames: {metadata['total_usernames']}")
    print(f"Usernames with multiple mics: {metadata['multi_mic_usernames']}")
    print(f"Mapping JSON: {args.mapping_output}")
    print(f"Review CSV: {args.review_csv_output}")
    print("=" * 70)


if __name__ == "__main__":
    main()
