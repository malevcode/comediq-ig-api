from datetime import datetime, timedelta, timezone

from agent.stale_mics import Decision, apply_safety_valve, evaluate, summarize

NOW = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
TRACKING = NOW - timedelta(days=60)  # activity tracking went live long ago unless a test says otherwise


def days_ago(n):
    return (NOW - timedelta(days=n)).isoformat()


def run(mics, sent=None, replies=None, mapping=None, activity=None, tracking=TRACKING):
    return evaluate(
        mics,
        sent or {},
        replies or {},
        mapping or {"host1": ["mic1"]},
        activity or {},
        NOW,
        tracking,
    )


def mic(**kw):
    base = {"unique_identifier": "mic1", "active": True, "hidden_by_agent": False}
    base.update(kw)
    return base


def test_hides_when_host_silent_and_no_activity():
    d = run([mic()], sent={"host1": {"sent_at": days_ago(20)}})
    assert d[0].action == "hide"


def test_keeps_when_host_silent_but_users_still_active():
    d = run([mic()], sent={"host1": {"sent_at": days_ago(20)}}, activity={"mic1": days_ago(5)})
    assert d[0].action == "keep"
    assert "users are still active" in d[0].reason


def test_keeps_when_dm_is_only_13_days_old():
    d = run([mic()], sent={"host1": {"sent_at": days_ago(13)}})
    assert d[0].action == "keep"


def test_keeps_when_host_replied_after_dm():
    d = run(
        [mic()],
        sent={"host1": {"sent_at": days_ago(20)}},
        replies={"host1": {"messages": [{"timestamp": days_ago(18)}]}},
    )
    assert d[0].action == "keep"


def test_keeps_when_last_verified_is_after_dm():
    verified = (NOW - timedelta(days=10)).strftime("%m/%d/%y")
    d = run([mic(last_verified=verified)], sent={"host1": {"sent_at": days_ago(20)}})
    assert d[0].action == "keep"


def test_no_dm_on_record_never_hides():
    d = run([mic()], sent={})
    assert d[0].action == "keep"
    assert "clock never started" in d[0].reason


def test_grace_period_when_tracking_is_new():
    """Tracking went live 3 days ago, so nobody has had 30 days to act. Do not hide."""
    d = run([mic()], sent={"host1": {"sent_at": days_ago(20)}}, tracking=NOW - timedelta(days=3))
    assert d[0].action == "keep"


def test_revives_when_host_replies_after_hidden():
    hidden = mic(hidden_by_agent=True, active=False, hidden_at=days_ago(5))
    d = run(
        [hidden],
        sent={"host1": {"sent_at": days_ago(40)}},
        replies={"host1": {"messages": [{"timestamp": days_ago(1)}]}},
    )
    assert d[0].action == "revive"


def test_revives_when_user_acts_after_hidden():
    hidden = mic(hidden_by_agent=True, active=False, hidden_at=days_ago(5))
    d = run([hidden], sent={"host1": {"sent_at": days_ago(40)}}, activity={"mic1": days_ago(2)})
    assert d[0].action == "revive"


def test_stays_hidden_without_new_signal():
    hidden = mic(hidden_by_agent=True, active=False, hidden_at=days_ago(5))
    d = run([hidden], sent={"host1": {"sent_at": days_ago(40)}})
    assert d[0].action == "keep"


def test_never_touches_mic_a_human_turned_off():
    off = mic(active=False, hidden_by_agent=False)
    assert run([off], sent={"host1": {"sent_at": days_ago(40)}}) == []


def test_safety_valve_holds_mass_hides():
    decisions = [Decision(f"m{i}", "hide", "x") for i in range(20)] + [Decision("k", "keep", "x")]
    held = apply_safety_valve(decisions, visible_count=100)
    assert summarize(held)["hold"] == 20
    assert summarize(held)["hide"] == 0


def test_safety_valve_allows_normal_hides():
    decisions = [Decision(f"m{i}", "hide", "x") for i in range(5)]
    assert summarize(apply_safety_valve(decisions, visible_count=100))["hide"] == 5
