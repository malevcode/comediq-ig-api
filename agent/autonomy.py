"""Autonomy tracker: the "3 approved drafts in a row" rule.

Decided with Adam:
  - Every category starts as draft-only. Adam approves each draft.
  - 3 approved drafts in a row with NO edits and the category runs alone.
  - Any edit (or rejection) resets that streak to 0 and the edit is saved as a lesson.
  - Adam can change how a category works at any time, which restarts its streak.
  - Pause pulls a category back to approve-first instantly.
  - Some topics always go to Adam, even after a category graduates.

State is a small JSON file so it is easy to read and back up.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

GRADUATION_STREAK = 3
MAX_LESSONS = 50

DEFAULT_CATEGORIES = (
    "inbound_ig_dm",
    "inbound_email",
    "ig_post",
    "host_dm",
    "points_redemption",
)

# Anything mentioning these is never automated, in any category.
ALWAYS_ESCALATE = (
    "refund", "chargeback", "payment", "lawyer", "legal", "sue", "lawsuit",
    "harass", "threat", "unsafe", "assault", "press", "journalist", "reporter",
)


def must_escalate(text: str) -> bool:
    lowered = (text or "").lower()
    return any(word in lowered for word in ALWAYS_ESCALATE)


def _blank() -> Dict[str, Any]:
    return {"streak": 0, "autonomous": False, "paused": False, "lessons": []}


class Autonomy:
    def __init__(self, path: str = "agent_state/autonomy.json"):
        self.path = Path(path)
        self.state: Dict[str, Dict[str, Any]] = {}
        if self.path.exists():
            self.state = json.loads(self.path.read_text())
        for category in DEFAULT_CATEGORIES:
            self.state.setdefault(category, _blank())

    def _cat(self, category: str) -> Dict[str, Any]:
        return self.state.setdefault(category, _blank())

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.state, indent=2))

    def record(self, category: str, *, approved_without_edit: bool, edit_note: str = "") -> Dict[str, Any]:
        """Log one reviewed draft. approved_without_edit=False means Adam edited or rejected it."""
        cat = self._cat(category)
        if approved_without_edit:
            cat["streak"] += 1
            if cat["streak"] >= GRADUATION_STREAK:
                cat["autonomous"] = True
        else:
            cat["streak"] = 0
            cat["autonomous"] = False
            if edit_note:
                cat["lessons"].append({"note": edit_note, "at": datetime.now(timezone.utc).isoformat()})
                cat["lessons"] = cat["lessons"][-MAX_LESSONS:]
        return cat

    def process_changed(self, category: str) -> None:
        """Adam changed how this category works, so the streak restarts under the new process."""
        cat = self._cat(category)
        cat["streak"] = 0
        cat["autonomous"] = False

    def pause(self, category: str) -> None:
        self._cat(category)["paused"] = True

    def resume(self, category: str) -> None:
        self._cat(category)["paused"] = False

    def can_run_alone(self, category: str, text: str = "") -> bool:
        cat = self._cat(category)
        if must_escalate(text):
            return False
        return bool(cat["autonomous"]) and not cat["paused"]

    def lessons(self, category: str) -> List[str]:
        """Read these before drafting the next one."""
        return [entry["note"] for entry in self._cat(category)["lessons"]]

    def status(self) -> Dict[str, str]:
        """Human readable line per category, for the weekly report."""
        lines = {}
        for name, cat in self.state.items():
            if cat["paused"]:
                lines[name] = "paused (approve-first)"
            elif cat["autonomous"]:
                lines[name] = "autonomous"
            else:
                lines[name] = f"{cat['streak']} of {GRADUATION_STREAK}"
        return lines
