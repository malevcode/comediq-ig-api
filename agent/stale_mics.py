"""Stale-mic engine.

Decides which open mics to hide and which hidden ones to bring back.

The rule (decided with Adam):
  HIDE  a mic only when BOTH are true:
          1. we DMed the host at least 14 days ago and they have not replied since
          2. no user activity at the mic for 30 days
  REVIVE a hidden mic as soon as the host replies OR any user acts on it.
  Hidden means active = false plus hidden_by_agent = true. Never deleted.

This file is pure logic (no network, no database) so it is easy to test.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

HOST_SILENCE_DAYS = 14
ACTIVITY_SILENCE_DAYS = 30
# Safety valve: if one run would hide more than this share of visible mics,
# hold every hide for human approval instead. Protects against a bad data day.
MAX_HIDE_FRACTION = 0.15


@dataclass
class Decision:
    mic_id: str
    action: str  # hide | revive | keep | hold
    reason: str


def to_dt(value: Any) -> Optional[datetime]:
    """Parse an ISO string or datetime into an aware UTC datetime. Returns None if empty or bad."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_last_verified(value: Any) -> Optional[datetime]:
    """last_verified in the mic table is stored as MM/DD/YY."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip(), "%m/%d/%y").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _latest(values: Iterable[Optional[datetime]]) -> Optional[datetime]:
    real = [v for v in values if v is not None]
    return max(real) if real else None


def _handles_by_mic(mapping: Dict[str, Any]) -> Dict[str, List[str]]:
    """ig_mic_mapping.json maps handle -> [mic ids]. Flip it to mic id -> [handles]."""
    result: Dict[str, List[str]] = {}
    for handle, ids in mapping.items():
        if not isinstance(ids, list):
            ids = [ids]
        for mic_id in ids:
            result.setdefault(str(mic_id), []).append(handle)
    return result


def evaluate(
    mics: List[Dict[str, Any]],
    sent: Dict[str, Any],
    replies: Dict[str, Any],
    mapping: Dict[str, Any],
    activity: Dict[str, Any],
    now: Any,
    tracking_started_at: Any,
) -> List[Decision]:
    """Return one Decision per mic.

    mics:     rows from open_mics_historical (unique_identifier, active, hidden_by_agent, hidden_at, last_verified)
    sent:     ig_sent_messages.json  (handle -> {sent_at})
    replies:  dm_replies.json        (handle -> {messages: [{timestamp}]})
    mapping:  ig_mic_mapping.json    (handle -> [mic ids])
    activity: mic id -> latest user activity time
    tracking_started_at: when user activity tracking went live. Activity silence is measured
        from here at the earliest, so mics are not punished for a period nobody could act on them.
    """
    now_dt = to_dt(now)
    tracking_dt = to_dt(tracking_started_at)
    if now_dt is None or tracking_dt is None:
        raise ValueError("now and tracking_started_at are required")

    handles_by_mic = _handles_by_mic(mapping)
    decisions: List[Decision] = []

    for mic in mics:
        mic_id = str(mic["unique_identifier"])
        hidden = bool(mic.get("hidden_by_agent"))
        if not hidden and not mic.get("active", True):
            continue  # a human turned this one off, leave it alone

        handles = handles_by_mic.get(mic_id, [])
        last_sent = _latest(to_dt(sent[h].get("sent_at")) for h in handles if h in sent)

        host_signals: List[Optional[datetime]] = [parse_last_verified(mic.get("last_verified"))]
        for h in handles:
            for msg in (replies.get(h) or {}).get("messages", []):
                host_signals.append(to_dt(msg.get("timestamp")))
        last_host_signal = _latest(host_signals)

        last_activity = to_dt(activity.get(mic_id))

        if hidden:
            hidden_at = to_dt(mic.get("hidden_at")) or datetime.min.replace(tzinfo=timezone.utc)
            if last_host_signal and last_host_signal > hidden_at:
                decisions.append(Decision(mic_id, "revive", "host replied after the mic was hidden"))
            elif last_activity and last_activity > hidden_at:
                decisions.append(Decision(mic_id, "revive", "a user acted on the mic after it was hidden"))
            else:
                decisions.append(Decision(mic_id, "keep", "still hidden, no new signal"))
            continue

        if last_sent is None:
            decisions.append(Decision(mic_id, "keep", "no host DM on record, so the 14 day clock never started"))
            continue

        host_silent = (now_dt - last_sent) >= timedelta(days=HOST_SILENCE_DAYS) and not (
            last_host_signal and last_host_signal > last_sent
        )
        activity_clock = _latest([last_activity, tracking_dt])
        activity_silent = (now_dt - activity_clock) >= timedelta(days=ACTIVITY_SILENCE_DAYS)

        if host_silent and activity_silent:
            decisions.append(
                Decision(mic_id, "hide", f"host silent {HOST_SILENCE_DAYS}+ days and no user activity {ACTIVITY_SILENCE_DAYS}+ days")
            )
        elif host_silent:
            decisions.append(Decision(mic_id, "keep", "host silent but users are still active there"))
        else:
            decisions.append(Decision(mic_id, "keep", "host replied or the DM is still recent"))

    return decisions


def apply_safety_valve(decisions: List[Decision], visible_count: int, max_fraction: float = MAX_HIDE_FRACTION) -> List[Decision]:
    """If too many hides in one run, turn every hide into a hold that needs approval."""
    hides = [d for d in decisions if d.action == "hide"]
    if visible_count <= 0 or len(hides) <= max_fraction * visible_count:
        return decisions
    note = f"held: {len(hides)} hides is more than {int(max_fraction * 100)}% of {visible_count} visible mics"
    return [Decision(d.mic_id, "hold", note) if d.action == "hide" else d for d in decisions]


def summarize(decisions: List[Decision]) -> Dict[str, int]:
    counts: Dict[str, int] = {"hide": 0, "revive": 0, "keep": 0, "hold": 0}
    for d in decisions:
        counts[d.action] = counts.get(d.action, 0) + 1
    return counts
