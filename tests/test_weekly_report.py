from datetime import datetime, timezone

from agent.weekly_report import host_dm_stats, is_monday_8am_new_york, render_markdown


def test_monday_8am_edt_and_est():
    # September 28, 2026 is a Monday and New York is on daylight time (UTC-4): 8am is 12:00 UTC.
    assert is_monday_8am_new_york(datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc))
    assert not is_monday_8am_new_york(datetime(2026, 9, 28, 13, 0, tzinfo=timezone.utc))
    # December 7, 2026 is a Monday and New York is on standard time (UTC-5): 8am is 13:00 UTC.
    assert is_monday_8am_new_york(datetime(2026, 12, 7, 13, 0, tzinfo=timezone.utc))
    assert not is_monday_8am_new_york(datetime(2026, 12, 7, 12, 0, tzinfo=timezone.utc))


def test_not_monday_never_runs():
    assert not is_monday_8am_new_york(datetime(2026, 9, 29, 12, 0, tzinfo=timezone.utc))


def base():
    return {"week_start": "2026-09-21", "week_end": "2026-09-28", "autonomy": {"ig_post": "2 of 3"}}


def test_unknown_numbers_say_not_connected_instead_of_inventing():
    text = render_markdown(base())
    assert "not connected yet" in text
    assert "Visible mics: not connected yet" in text
    assert "ig_post: 2 of 3" in text
    assert "Nothing waiting" in text


def test_real_numbers_render():
    data = base()
    data["growth"] = {"new_accounts": 12, "total_accounts": 340}
    data["mics"] = {"visible": 210, "confirmed": 30, "hidden": 2, "revived": 1}
    data["points"] = {"issued": 88.5, "outliers": [("user-9", 41.0)]}
    data["host_dms"] = {"sent": 100, "replied": 40, "silent": 60, "rate": 40}
    data["needs_you"] = ["3 Instagram post drafts to approve"]
    text = render_markdown(data)
    assert "New accounts this week: 12" in text
    assert "Hidden this week: 2" in text
    assert "user-9: 41 points" in text
    assert "replied: 40 (40%)" in text
    assert "3 Instagram post drafts to approve" in text


def test_no_em_dashes_in_report():
    assert chr(0x2014) not in render_markdown(base())


def test_host_dm_stats(tmp_path):
    sent = tmp_path / "sent.json"
    replies = tmp_path / "replies.json"
    sent.write_text('{"a": {}, "b": {}, "c": {}, "d": {}}')
    replies.write_text('{"a": {"messages": [{"message": "Y"}]}, "b": {"messages": []}}')
    stats = host_dm_stats(str(sent), str(replies))
    assert stats == {"sent": 4, "replied": 1, "silent": 3, "rate": 25}


def test_host_dm_stats_missing_file_returns_none(tmp_path):
    assert host_dm_stats(str(tmp_path / "nope.json"), str(tmp_path / "nope2.json")) is None
