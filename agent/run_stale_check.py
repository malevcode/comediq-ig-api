#!/usr/bin/env python3
"""Run the stale-mic check against Supabase.

Dry run by default (prints what it WOULD do). Add --apply to write changes.

Needs, in this order:
  1. sql/001_agent_foundation.sql already run in Supabase
  2. SUPABASE_URL and SUPABASE_KEY in the environment (service key, so it can write)
  3. ig_sent_messages.json, ig_mic_mapping.json, dm_replies.json in the repo root
     (the same files the monthly DM workflow already produces)

Example:
  python -m agent.run_stale_check --tracking-started 2026-10-01
  python -m agent.run_stale_check --tracking-started 2026-10-01 --apply
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from agent.stale_mics import apply_safety_valve, evaluate, summarize, to_dt

MIC_TABLE = "open_mics_historical"


def load_json(path: str) -> Dict[str, Any]:
    file = Path(path)
    if not file.exists():
        print(f"Missing {path}. Run the monthly DM workflow first so the 14 day clock has a start.")
        sys.exit(1)
    return json.loads(file.read_text())


def fetch_all(query_builder, page_size: int = 1000) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    start = 0
    while True:
        page = query_builder().range(start, start + page_size - 1).execute().data or []
        rows.extend(page)
        if len(page) < page_size:
            return rows
        start += page_size


def latest_activity_by_mic(sb) -> Dict[str, Any]:
    """Newest verified user action per mic. Empty if nobody has acted yet."""
    rows = fetch_all(lambda: sb.table("agent_mic_activity").select("mic_id,at").eq("verified_at_venue", True))
    latest: Dict[str, Any] = {}
    for row in rows:
        when = to_dt(row["at"])
        if when and (row["mic_id"] not in latest or when > latest[row["mic_id"]]):
            latest[row["mic_id"]] = when
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description="Hide stale mics and revive hidden ones")
    parser.add_argument("--tracking-started", required=True, help="YYYY-MM-DD the day user check-in tracking went live")
    parser.add_argument("--apply", action="store_true", help="Write changes. Without this it is a dry run.")
    parser.add_argument("--sent", default="ig_sent_messages.json")
    parser.add_argument("--replies", default="dm_replies.json")
    parser.add_argument("--mapping", default="ig_mic_mapping.json")
    args = parser.parse_args()

    url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Missing SUPABASE_URL or SUPABASE_KEY")
        sys.exit(1)

    from supabase import create_client

    sb = create_client(url, key)
    now = datetime.now(timezone.utc)

    mics = fetch_all(lambda: sb.table(MIC_TABLE).select("*").or_("active.eq.true,hidden_by_agent.eq.true"))
    visible = sum(1 for m in mics if m.get("active") and not m.get("hidden_by_agent"))

    decisions = evaluate(
        mics,
        load_json(args.sent),
        load_json(args.replies) if Path(args.replies).exists() else {},
        load_json(args.mapping),
        latest_activity_by_mic(sb),
        now,
        args.tracking_started + "T00:00:00+00:00",
    )
    decisions = apply_safety_valve(decisions, visible)
    counts = summarize(decisions)

    print("=" * 70)
    print("STALE MIC CHECK", "(APPLYING)" if args.apply else "(dry run)")
    print("=" * 70)
    print(f"Visible mics: {visible}")
    print(f"Hide: {counts['hide']}  Revive: {counts['revive']}  Hold for approval: {counts['hold']}  Keep: {counts['keep']}")
    for d in decisions:
        if d.action != "keep":
            print(f"- {d.action.upper():6} {d.mic_id}: {d.reason}")

    if not args.apply:
        print("\nDry run only. Add --apply to write these changes.")
        return

    stamp = now.isoformat()
    for d in decisions:
        if d.action == "hide":
            sb.table(MIC_TABLE).update({"active": False, "hidden_by_agent": True, "hidden_at": stamp}).eq("unique_identifier", d.mic_id).execute()
        elif d.action == "revive":
            sb.table(MIC_TABLE).update({"active": True, "hidden_by_agent": False, "hidden_at": None}).eq("unique_identifier", d.mic_id).execute()
        else:
            continue
        event = "hidden" if d.action == "hide" else "revived"
        sb.table("agent_mic_history").insert({"mic_id": d.mic_id, "event": event, "reason": d.reason, "at": stamp}).execute()

    print(f"\nApplied {counts['hide']} hides and {counts['revive']} revives.")


if __name__ == "__main__":
    main()
