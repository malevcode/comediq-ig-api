#!/usr/bin/env python3
"""
Apply processed DM/SMS/comment response updates to Supabase.

Dry-run by default. Add --apply after reviewing processed_responses.json,
ai_parse_results.json, and/or supabase_response_updates.sql.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv

from process_responses import (
    AI_UPDATE_FIELDS,
    DEFAULT_AI_QUEUE_FILE,
    DEFAULT_AI_RESULTS_FILE,
    default_verification_column,
    load_ai_results,
    normalize_ai_result_entries,
    should_stamp_last_verified,
)


def current_last_verified() -> str:
    return datetime.now().strftime("%m/%d/%y")


def load_json(path: str) -> Any:
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise SystemExit(f"Could not read {path}: {e}")
    return data


def load_queue_by_id(path: str) -> Dict[str, Dict[str, Any]]:
    data = load_json(path)
    items = data if isinstance(data, list) else data.get("items", [])
    if not isinstance(items, list):
        items = []
    return {
        item.get("queue_id"): item
        for item in items
        if isinstance(item, dict) and item.get("queue_id")
    }


def direct_payloads(
    processed_file: str,
    verification_column: str,
    last_verified: str,
) -> List[Tuple[str, Dict[str, Any]]]:
    processed = load_json(processed_file)
    if not isinstance(processed, dict):
        return []
    rows = []
    for item in processed.get("direct_supabase_updates", []):
        if not isinstance(item, dict):
            continue
        mic_id = item.get("mic_identifier")
        active = item.get("active")
        status = item.get("verification_status")
        if not mic_id or active not in (True, False):
            continue
        rows.append((
            mic_id,
            {
                "active": active,
                "last_verified": item.get("last_verified") or last_verified,
                verification_column: status or "responded_confirmed",
            },
        ))
    return rows


def ai_payloads(
    ai_results_file: str,
    ai_queue_file: str,
    verification_column: str,
    last_verified: str,
) -> List[Tuple[str, Dict[str, Any]]]:
    queue_by_id = load_queue_by_id(ai_queue_file)
    rows = []

    for result in normalize_ai_result_entries(load_ai_results(ai_results_file)):
        if not isinstance(result, dict):
            continue

        queue_item = queue_by_id.get(result.get("queue_id"))
        mic_id = result.get("mic_identifier") or (queue_item or {}).get("mic_identifier")
        if not mic_id or mic_id == "fill_with_existing_unique_identifier":
            continue

        payload: Dict[str, Any] = {}
        if result.get("active") is not None:
            payload["active"] = result.get("active")

        updates = result.get("updates") or result.get("proposed_updates") or {}
        has_updates = isinstance(updates, dict) and any(value not in (None, "") for value in updates.values())
        verification_status = result.get("verification_status")
        if not verification_status:
            verification_status = "responded_changes" if has_updates or result.get("active") is not None else "responded_unclear"

        payload[verification_column] = verification_status
        if should_stamp_last_verified(verification_status):
            payload["last_verified"] = result.get("last_verified") or last_verified

        if isinstance(updates, dict):
            for field, value in updates.items():
                if field in AI_UPDATE_FIELDS and value not in (None, ""):
                    payload[field] = value

        if payload:
            rows.append((mic_id, payload))

    return rows


def main():
    parser = argparse.ArgumentParser(description="Apply processed response updates to Supabase")
    parser.add_argument("--processed-file", default="processed_responses.json")
    parser.add_argument("--ai-results-file", default=DEFAULT_AI_RESULTS_FILE)
    parser.add_argument("--ai-queue-file", default=DEFAULT_AI_QUEUE_FILE)
    parser.add_argument("--table", default="open_mics_historical")
    parser.add_argument("--verification-column", default=default_verification_column())
    parser.add_argument("--last-verified", default=current_last_verified())
    parser.add_argument("--direct-only", action="store_true", help="Apply only direct Y/N updates")
    parser.add_argument("--ai-only", action="store_true", help="Apply only reviewed AI result updates")
    parser.add_argument("--apply", action="store_true", help="Actually update Supabase. Without this, dry-run only.")
    args = parser.parse_args()

    rows: List[Tuple[str, Dict[str, Any]]] = []
    if not args.ai_only:
        rows.extend(direct_payloads(args.processed_file, args.verification_column, args.last_verified))
    if not args.direct_only:
        rows.extend(ai_payloads(args.ai_results_file, args.ai_queue_file, args.verification_column, args.last_verified))

    print("=" * 70)
    print("RESPONSE SUPABASE APPLY")
    print("=" * 70)
    print(f"Table: {args.table}")
    print(f"Verification column: {args.verification_column}")
    print(f"Rows prepared: {len(rows)}")

    if not args.apply:
        print("\nDry run only. Add --apply to write these updates.")
        for mic_id, payload in rows[:10]:
            print(f"- {mic_id}: {payload}")
        if len(rows) > 10:
            print(f"... and {len(rows) - 10} more")
        return

    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env")
        sys.exit(1)

    from supabase import create_client

    supabase = create_client(url, key)
    updated = 0
    for mic_id, payload in rows:
        supabase.table(args.table).update(payload).eq("unique_identifier", mic_id).execute()
        updated += 1

    print(f"\n✅ Updated {updated} rows in {args.table}")
    print("=" * 70)


if __name__ == "__main__":
    main()
