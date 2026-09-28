"""Comediq Points rules.

Decided with Adam:
  - 1 point for a verified check-in, confirm-active, or sign-up
  - up to 5 different mics a day, one check-in per mic per day
  - a check-in only counts if the phone matched the venue and stayed about 20 minutes
  - 5 point bonus for reporting a bad mic, paid only once it is confirmed
    (the host stays silent OR a second user agrees)
  - premium accounts earn 1.5x
  - points live on the user profile, so they are the same on web and mobile

Pure logic, no database. The caller writes accepted awards to agent_points_ledger.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

BASE_POINTS = {"checkin": 1.0, "confirm": 1.0, "signup": 1.0}
BAD_MIC_BONUS = 5.0
MAX_CHECKINS_PER_DAY = 5
MIN_DWELL_MINUTES = 20
PREMIUM_MULTIPLIER = 1.5


@dataclass
class Award:
    granted: bool
    points: float
    reason: str


def _scale(points: float, premium: bool) -> float:
    return round(points * (PREMIUM_MULTIPLIER if premium else 1.0), 1)


def award(
    action: str,
    *,
    mic_id: str,
    verified_at_venue: bool,
    dwell_minutes: float = 0,
    premium: bool = False,
    todays_checkin_mic_ids: Iterable[str] = (),
) -> Award:
    """Decide whether one action earns points, and how many."""
    if action not in BASE_POINTS:
        return Award(False, 0.0, f"unknown action: {action}")
    if not verified_at_venue:
        return Award(False, 0.0, "location did not match the venue")

    if action == "checkin":
        if dwell_minutes < MIN_DWELL_MINUTES:
            return Award(False, 0.0, f"stay at least {MIN_DWELL_MINUTES} minutes to check in")
        already = set(todays_checkin_mic_ids)
        if mic_id in already:
            return Award(False, 0.0, "already checked into this mic today")
        if len(already) >= MAX_CHECKINS_PER_DAY:
            return Award(False, 0.0, f"daily limit of {MAX_CHECKINS_PER_DAY} mics reached")

    return Award(True, _scale(BASE_POINTS[action], premium), f"{action} verified")


def resolve_bad_mic_report(
    *,
    reporter_id: str,
    agreeing_user_ids: Iterable[str],
    host_silent: bool,
    premium: bool = False,
) -> Award:
    """Pay the 5 point bonus only once the report is confirmed by someone other than the reporter."""
    others = {u for u in agreeing_user_ids if u != reporter_id}
    if others:
        return Award(True, _scale(BAD_MIC_BONUS, premium), "a second user agreed the mic is dead")
    if host_silent:
        return Award(True, _scale(BAD_MIC_BONUS, premium), "the host stayed silent")
    return Award(False, 0.0, "report not confirmed yet")


def ledger_entry(user_id: str, action: str, mic_id: str, result: Award) -> Dict[str, Any]:
    """Shape of a row for agent_points_ledger."""
    return {"user_id": user_id, "action": action, "mic_id": mic_id, "points": result.points, "reason": result.reason}


def balance(entries: List[Dict[str, Any]]) -> float:
    return round(sum(float(e["points"]) for e in entries), 1)
