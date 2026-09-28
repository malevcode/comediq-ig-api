from agent.points import award, balance, ledger_entry, resolve_bad_mic_report


def test_verified_checkin_earns_one_point():
    a = award("checkin", mic_id="m1", verified_at_venue=True, dwell_minutes=25)
    assert a.granted and a.points == 1.0


def test_checkin_denied_when_location_does_not_match():
    a = award("checkin", mic_id="m1", verified_at_venue=False, dwell_minutes=25)
    assert not a.granted and a.points == 0


def test_checkin_denied_when_stay_too_short():
    a = award("checkin", mic_id="m1", verified_at_venue=True, dwell_minutes=5)
    assert not a.granted


def test_one_checkin_per_mic_per_day():
    a = award("checkin", mic_id="m1", verified_at_venue=True, dwell_minutes=30, todays_checkin_mic_ids=["m1"])
    assert not a.granted and "already" in a.reason


def test_up_to_five_mics_per_day():
    four = ["a", "b", "c", "d"]
    assert award("checkin", mic_id="e", verified_at_venue=True, dwell_minutes=30, todays_checkin_mic_ids=four).granted
    five = four + ["e"]
    assert not award("checkin", mic_id="f", verified_at_venue=True, dwell_minutes=30, todays_checkin_mic_ids=five).granted


def test_confirm_and_signup_need_location_but_not_dwell():
    assert award("confirm", mic_id="m1", verified_at_venue=True).granted
    assert award("signup", mic_id="m1", verified_at_venue=True).granted
    assert not award("confirm", mic_id="m1", verified_at_venue=False).granted


def test_premium_earns_one_and_a_half_times():
    a = award("checkin", mic_id="m1", verified_at_venue=True, dwell_minutes=30, premium=True)
    assert a.points == 1.5


def test_unknown_action_denied():
    assert not award("upvote", mic_id="m1", verified_at_venue=True).granted


def test_bad_mic_bonus_not_paid_until_confirmed():
    a = resolve_bad_mic_report(reporter_id="u1", agreeing_user_ids=[], host_silent=False)
    assert not a.granted


def test_bad_mic_bonus_paid_when_second_user_agrees():
    a = resolve_bad_mic_report(reporter_id="u1", agreeing_user_ids=["u2"], host_silent=False)
    assert a.granted and a.points == 5.0


def test_reporter_cannot_confirm_own_report():
    a = resolve_bad_mic_report(reporter_id="u1", agreeing_user_ids=["u1"], host_silent=False)
    assert not a.granted


def test_bad_mic_bonus_paid_when_host_silent():
    assert resolve_bad_mic_report(reporter_id="u1", agreeing_user_ids=[], host_silent=True).granted


def test_premium_bad_mic_bonus():
    a = resolve_bad_mic_report(reporter_id="u1", agreeing_user_ids=["u2"], host_silent=False, premium=True)
    assert a.points == 7.5


def test_monthly_pace_is_about_thirty_points_for_active_free_user():
    """Sanity check on the target: roughly 30 points a month for an active user."""
    entries = []
    for _ in range(30):  # about one verified action per day
        a = award("checkin", mic_id="m", verified_at_venue=True, dwell_minutes=30)
        entries.append(ledger_entry("u1", "checkin", "m", a))
    assert balance(entries) == 30.0
