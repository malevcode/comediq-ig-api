#!/usr/bin/env python3
"""Weekly Comediq report.

Runs every Monday at 8am New York time (see .github/workflows/agent_weekly_report.yaml),
and on demand any time:

  python -m agent.weekly_report --force

Anything that cannot be measured yet shows as "not connected yet". The report never invents a number.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from zoneinfo import ZoneInfo

from agent.autonomy import Autonomy

NEW_YORK = ZoneInfo("America/New_York")
# One person earning more than a full month's target in a single week gets flagged for a look.
OUTLIER_WEEKLY_POINTS = 35.0
NOT_CONNECTED = "not connected yet"


def is_monday_8am_new_york(now_utc: datetime) -> bool:
    """The workflow fires at two UTC hours so it survives daylight saving. Only one is 8am here."""
    local = now_utc.astimezone(NEW_YORK)
    return local.weekday() == 0 and local.hour == 8


def _safe(fn: Callable[[], Any]) -> Any:
    """Any collector that fails returns None, and the report says 'not connected yet'."""
    try:
        return fn()
    except Exception:
        return None


def _fmt(value: Any, suffix: str = "") -> str:
    return NOT_CONNECTED if value is None else f"{value}{suffix}"


def render_markdown(data: Dict[str, Any]) -> str:
    growth = data.get("growth") or {}
    mics = data.get("mics") or {}
    points = data.get("points") or {}
    dms = data.get("host_dms")
    lines: List[str] = [
        f"# Comediq weekly report: {data['week_start']} to {data['week_end']}",
        "",
        "## Growth",
        f"- New accounts this week: {_fmt(growth.get('new_accounts'))}",
        f"- Total accounts: {_fmt(growth.get('total_accounts'))}",
        f"- Weekly active users and total usage: {NOT_CONNECTED}",
        "",
        "## Mics",
        f"- Visible mics: {_fmt(mics.get('visible'))}",
        f"- Confirmed this week: {_fmt(mics.get('confirmed'))}",
        f"- Hidden this week: {_fmt(mics.get('hidden'))}",
        f"- Revived this week: {_fmt(mics.get('revived'))}",
    ]
    stale = data.get("stale_preview")
    if stale is not None:
        lines.append(f"- Stale check preview: {stale['hide']} would hide, {stale['revive']} would revive, {stale['hold']} held for approval")
    lines += ["", "## Host DMs"]
    if dms:
        lines.append(f"- Hosts messaged: {dms['sent']}, replied: {dms['replied']} ({dms['rate']}%)")
        if dms["silent"]:
            lines.append(f"- Still silent: {dms['silent']}")
    else:
        lines.append(f"- {NOT_CONNECTED}")

    lines += ["", "## Points", f"- Issued this week: {_fmt(points.get('issued'))}"]
    outliers = points.get("outliers")
    if outliers:
        lines.append(f"- Flagged for a look (over {OUTLIER_WEEKLY_POINTS:g} points in a week): {len(outliers)} user(s)")
        for user_id, total in outliers:
            lines.append(f"  - {user_id}: {total:g} points")
    elif outliers is not None:
        lines.append("- No outlier earners")

    lines += ["", "## Marketing", f"- Post views, signups per post, inbound DM and email counts: {NOT_CONNECTED}"]

    lines += ["", "## Autonomy (approved drafts in a row, 3 to run alone)"]
    for name, status in (data.get("autonomy") or {}).items():
        lines.append(f"- {name}: {status}")

    needs = data.get("needs_you") or []
    lines += ["", "## Needs you"]
    lines += [f"- {item}" for item in needs] if needs else ["- Nothing waiting"]
    return "\n".join(lines) + "\n"


# ---- collectors (touch Supabase and local files) ----

def _count(sb, table: str, column: str, since: Optional[str] = None) -> int:
    query = sb.table(table).select(column, count="exact")
    if since:
        query = query.gte("created_at", since)
    return query.limit(1).execute().count or 0


def _rows_since(sb, table: str, columns: str, since: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    start = 0
    while True:
        page = sb.table(table).select(columns).gte("at", since).range(start, start + 999).execute().data or []
        rows.extend(page)
        if len(page) < 1000:
            return rows
        start += 1000


def host_dm_stats(sent_path: str, replies_path: str) -> Optional[Dict[str, Any]]:
    if not Path(sent_path).exists():
        return None
    sent = json.loads(Path(sent_path).read_text())
    replies = json.loads(Path(replies_path).read_text()) if Path(replies_path).exists() else {}
    replied = sum(1 for handle in sent if (replies.get(handle) or {}).get("messages"))
    total = len(sent)
    return {"sent": total, "replied": replied, "silent": total - replied, "rate": round(100 * replied / total) if total else 0}


def collect(now: datetime) -> Dict[str, Any]:
    since_dt = now - timedelta(days=7)
    since = since_dt.isoformat()
    data: Dict[str, Any] = {
        "week_start": since_dt.astimezone(NEW_YORK).date().isoformat(),
        "week_end": now.astimezone(NEW_YORK).date().isoformat(),
        "autonomy": Autonomy().status(),
        "host_dms": _safe(lambda: host_dm_stats("ig_sent_messages.json", "dm_replies.json")),
    }

    url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
    if not (url and key):
        return data

    from supabase import create_client

    sb = create_client(url, key)
    profiles = os.environ.get("PROFILES_TABLE", "profiles")

    data["growth"] = {
        "new_accounts": _safe(lambda: _count(sb, profiles, "created_at", since)),
        "total_accounts": _safe(lambda: _count(sb, profiles, "created_at")),
    }

    def mic_block() -> Dict[str, Any]:
        events = _rows_since(sb, "agent_mic_history", "event", since)
        tally = lambda name: sum(1 for e in events if e["event"] == name)
        visible = sb.table("open_mics_historical").select("unique_identifier", count="exact").eq("active", True).limit(1).execute().count
        return {"visible": visible, "confirmed": tally("confirmed"), "hidden": tally("hidden"), "revived": tally("revived")}

    data["mics"] = _safe(mic_block)

    def points_block() -> Dict[str, Any]:
        rows = _rows_since(sb, "agent_points_ledger", "user_id,points", since)
        totals: Dict[str, float] = {}
        for row in rows:
            totals[row["user_id"]] = totals.get(row["user_id"], 0.0) + float(row["points"])
        outliers = sorted(((u, t) for u, t in totals.items() if t > OUTLIER_WEEKLY_POINTS), key=lambda x: -x[1])
        return {"issued": round(sum(totals.values()), 1), "outliers": outliers}

    data["points"] = _safe(points_block)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the weekly Comediq report")
    parser.add_argument("--force", action="store_true", help="Run now even if it is not Monday 8am in New York (use for on-demand reports)")
    parser.add_argument("--out", default="reports")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    if not args.force and not is_monday_8am_new_york(now):
        print("Not Monday 8am in New York, skipping. Use --force for an on-demand report.")
        return

    report = render_markdown(collect(now))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"weekly_{now.astimezone(NEW_YORK).date().isoformat()}.md"
    path.write_text(report)
    print(report)
    print(f"Saved to {path}")


if __name__ == "__main__":
    main()
