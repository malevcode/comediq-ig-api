#!/usr/bin/env python3
"""
Prepare monthly verification updates from Instagram collection artifacts.

This merges a current mic export with:
- ig_sent_messages.json
- ig_mic_mapping.json
- dm_replies.json

It writes a full Google-Sheets-ready CSV and a narrow Supabase-ready CSV keyed by
unique_identifier. The verification status column is configurable; for August use
aug_verification_status.
"""

import argparse
import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple

import pandas as pd


VALID_STATUS_VALUES = {
    "responded_confirmed",
    "responded_changes",
    "responded_unclear",
    "no_response",
    "not_sent",
}

FIELD_LABELS = {
    "cost": "cost",
    "frequency": "frequency",
    "location": "location",
    "stage time": "stage_time",
    "stage_time": "stage_time",
    "stage-time": "stage_time",
    "latest end time": "latest_end_time",
    "latest_end_time": "latest_end_time",
    "latest-end-time": "latest_end_time",
    "end time": "latest_end_time",
    "end_time": "latest_end_time",
    "end-time": "latest_end_time",
}

FIELD_LABEL_PATTERN = re.compile(
    r"(cost|frequency|location|stage[\s_-]*time|latest[\s_-]*end[\s_-]*time|end[\s_-]*time)\s*[:=-]\s*",
    re.IGNORECASE,
)


def current_last_verified() -> str:
    """Return today's date in MM/DD/YY last_verified format."""
    return datetime.now().strftime("%m/%d/%y")


def load_json(path: str, default):
    if not os.path.exists(path):
        return default

    with open(path, "r") as f:
        return json.load(f)


def normalize_contact(value: Any) -> str:
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null", "#n/a", "n/a"}:
        return ""

    return text.lstrip("@")


def has_valid_instagram_handle(value: Any) -> bool:
    """Match the sender's Instagram handle validation without importing send script dependencies."""
    if pd.isna(value):
        return False

    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null", "#n/a", "n/a", "no", "unknown"}:
        return False
    if "http://" in text.lower() or "https://" in text.lower() or "instagram.com" in text.lower():
        return False
    if re.fullmatch(r"[+()\d\s.-]{7,}", text):
        return False

    if "@" in text:
        match = re.search(r"@([A-Za-z0-9._]{1,30})\b", text)
        if not match:
            return False
        handle = match.group(1)
    else:
        handle = text

    if not re.fullmatch(r"[A-Za-z0-9._]{3,30}", handle):
        return False

    return bool(re.search(r"[A-Za-z]", handle))


def normalize_field_label(label: str) -> str:
    normalized = re.sub(r"\s+", " ", label.strip().lower().replace("_", " ").replace("-", " "))
    return FIELD_LABELS.get(normalized, normalized.replace(" ", "_"))


def extract_field_updates(message_text: str, mic_count: int) -> Dict[int, Dict[str, str]]:
    updates: Dict[int, Dict[str, str]] = {}

    for raw_line in str(message_text).splitlines():
        line = raw_line.strip()
        if not line:
            continue

        numbered_line = re.match(r"^(\d+)[\).:\-\s]+(.+)$", line)
        if numbered_line:
            target_positions = [int(numbered_line.group(1))]
            content = numbered_line.group(2)
        elif mic_count == 1:
            target_positions = [1]
            content = line
        else:
            continue

        matches = list(FIELD_LABEL_PATTERN.finditer(content))
        if not matches:
            continue

        for index, match in enumerate(matches):
            field_name = normalize_field_label(match.group(1))
            value_start = match.end()
            value_end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            value = content[value_start:value_end].strip(" ,;|")

            if not value:
                continue

            for position in target_positions:
                if position < 1 or (mic_count and position > mic_count):
                    continue
                updates.setdefault(position, {})[field_name] = value

    return updates


def status_from_response(response: str, field_updates: Dict[str, str], raw_message: str) -> str:
    if response == "C" or field_updates:
        return "responded_changes"
    if response in {"Y", "N"}:
        return "responded_confirmed"
    if raw_message:
        return "responded_unclear"
    return "no_response"


def latest_message(response_data: Any) -> Dict[str, Any]:
    if isinstance(response_data, dict) and "messages" in response_data:
        messages = response_data.get("messages") or []
        if messages:
            return messages[0] if isinstance(messages, list) else messages
    if isinstance(response_data, list) and response_data:
        return response_data[0]
    if isinstance(response_data, dict):
        return response_data
    return {}


def build_response_indexes(
    replies: Dict[str, Any],
    mic_mapping: Dict[str, Any],
    status_column: str,
) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    by_mic_id: Dict[str, Dict[str, Any]] = {}
    by_contact: Dict[str, Dict[str, Any]] = {}

    for raw_contact, response_data in replies.items():
        contact = normalize_contact(raw_contact)
        mic_ids = response_data.get("mic_identifiers") if isinstance(response_data, dict) else None
        if not mic_ids:
            mic_ids = mic_mapping.get(contact, [])
        if not isinstance(mic_ids, list):
            mic_ids = [mic_ids] if mic_ids else []

        message = latest_message(response_data)
        raw_message = message.get("message", "")
        parsed_response = message.get("parsed_response")
        numbered_responses = message.get("numbered_responses") or {}
        timestamp = message.get("timestamp", "")
        field_updates_by_position = extract_field_updates(raw_message, len(mic_ids))

        contact_record = {
            "contact": contact,
            "raw_message": raw_message,
            "parsed_response": parsed_response,
            "timestamp": timestamp,
            "mic_ids": mic_ids,
        }
        by_contact[contact] = contact_record

        if numbered_responses:
            iterable = numbered_responses.items()
        elif parsed_response or raw_message:
            iterable = ((position, parsed_response or "") for position, _ in enumerate(mic_ids, 1))
        else:
            iterable = ()

        for position_raw, response in iterable:
            position = int(position_raw)
            mic_index = position - 1
            if 0 <= mic_index < len(mic_ids):
                mic_id = str(mic_ids[mic_index])
                field_updates = field_updates_by_position.get(position, {})
                by_mic_id[mic_id] = {
                    **contact_record,
                    "position": position,
                    status_column: status_from_response(response, field_updates, raw_message),
                    "field_updates": field_updates,
                }

    return by_mic_id, by_contact


def flatten_sent_mic_ids(mic_mapping: Dict[str, Any]) -> set:
    sent_mic_ids = set()
    for mic_ids in mic_mapping.values():
        if not isinstance(mic_ids, list):
            mic_ids = [mic_ids] if mic_ids else []
        for mic_id in mic_ids:
            sent_mic_ids.add(str(mic_id))
    return sent_mic_ids


def main():
    parser = argparse.ArgumentParser(description="Prepare monthly verification CSV updates")
    parser.add_argument("source_csv", help="Current mic export/private sheet CSV")
    parser.add_argument("--status-column", default="aug_verification_status")
    parser.add_argument("--response-prefix", default="aug")
    parser.add_argument("--last-verified", default=current_last_verified())
    parser.add_argument("--mapping-file", default="ig_mic_mapping.json")
    parser.add_argument("--replies-file", default="dm_replies.json")
    parser.add_argument("--sent-file", default="ig_sent_messages.json")
    parser.add_argument("--google-output", default="august_google_sheet_updates.csv")
    parser.add_argument("--supabase-output", default="august_supabase_updates.csv")
    parser.add_argument(
        "--include-no-response",
        action="store_true",
        help="Include no_response/not_sent rows in the Supabase output as status-only updates.",
    )
    args = parser.parse_args()

    source = pd.read_csv(args.source_csv, dtype=str, keep_default_na=False)
    if "unique_identifier" not in source.columns:
        raise ValueError("source_csv must include unique_identifier")

    sent_messages = load_json(args.sent_file, {})
    mic_mapping = load_json(args.mapping_file, {})
    replies = load_json(args.replies_file, {})

    sent_mic_ids = flatten_sent_mic_ids(mic_mapping)
    response_by_mic_id, _ = build_response_indexes(replies, mic_mapping, args.status_column)

    raw_response_col = f"{args.response_prefix}_raw_response"
    response_contact_col = f"{args.response_prefix}_response_contact"
    field_updates_col = f"{args.response_prefix}_field_updates"

    rows: List[Dict[str, Any]] = []
    for _, row in source.iterrows():
        mic_id = str(row["unique_identifier"])
        response = response_by_mic_id.get(mic_id)

        if response:
            status = response[args.status_column]
            last_verified = args.last_verified if status in {"responded_changes", "responded_confirmed"} else row.get("last_verified", "")
            raw_response = response.get("raw_message", "")
            response_contact = response.get("contact", "")
            field_updates = response.get("field_updates", {})
        elif mic_id in sent_mic_ids or has_valid_instagram_handle(row.get("changes_updates", "")):
            status = "no_response"
            last_verified = row.get("last_verified", "")
            raw_response = ""
            response_contact = ""
            field_updates = {}
        else:
            status = "not_sent"
            last_verified = row.get("last_verified", "")
            raw_response = ""
            response_contact = ""
            field_updates = {}

        output_row = row.to_dict()
        output_row[args.status_column] = status
        output_row[response_contact_col] = response_contact
        output_row[raw_response_col] = raw_response
        output_row[field_updates_col] = json.dumps(field_updates, ensure_ascii=False)
        output_row["last_verified"] = last_verified

        for field, value in field_updates.items():
            if field in output_row and value:
                output_row[field] = value

        rows.append(output_row)

    google_df = pd.DataFrame(rows)
    google_df.to_csv(args.google_output, index=False)

    if args.include_no_response:
        supabase_df = google_df.copy()
    else:
        supabase_df = google_df[
            google_df[args.status_column].isin(VALID_STATUS_VALUES)
        ].copy()

    supabase_columns = [
        "unique_identifier",
        "last_verified",
        args.status_column,
        "cost",
        "frequency",
        "location",
        "stage_time",
        "latest_end_time",
        raw_response_col,
    ]
    existing_supabase_columns = [col for col in supabase_columns if col in supabase_df.columns]
    supabase_df[existing_supabase_columns].to_csv(args.supabase_output, index=False)

    summary = google_df[args.status_column].value_counts(dropna=False)
    print("=" * 70)
    print("Monthly verification update export complete")
    print("=" * 70)
    print(f"Source rows: {len(source)}")
    print(f"Sent contacts loaded: {len(sent_messages)}")
    print(f"Sent mic IDs loaded: {len(sent_mic_ids)}")
    print(f"Reply contacts loaded: {len(replies)}")
    print("\nStatus counts:")
    print(summary.to_string())
    print(f"\nGoogle Sheets output: {args.google_output}")
    print(f"Supabase output: {args.supabase_output}")
    print("=" * 70)


if __name__ == "__main__":
    main()
