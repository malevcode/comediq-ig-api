from agent.autonomy import Autonomy, must_escalate


def make(tmp_path):
    return Autonomy(str(tmp_path / "autonomy.json"))


def test_starts_draft_only(tmp_path):
    a = make(tmp_path)
    assert not a.can_run_alone("inbound_ig_dm")
    assert a.status()["inbound_ig_dm"] == "0 of 3"


def test_graduates_after_three_clean_approvals(tmp_path):
    a = make(tmp_path)
    for _ in range(2):
        a.record("inbound_ig_dm", approved_without_edit=True)
    assert not a.can_run_alone("inbound_ig_dm")
    a.record("inbound_ig_dm", approved_without_edit=True)
    assert a.can_run_alone("inbound_ig_dm")


def test_an_edit_resets_the_streak_and_saves_a_lesson(tmp_path):
    a = make(tmp_path)
    a.record("inbound_ig_dm", approved_without_edit=True)
    a.record("inbound_ig_dm", approved_without_edit=True)
    a.record("inbound_ig_dm", approved_without_edit=False, edit_note="never promise a specific show spot")
    assert a.status()["inbound_ig_dm"] == "0 of 3"
    assert a.lessons("inbound_ig_dm") == ["never promise a specific show spot"]


def test_edit_after_graduating_pulls_it_back(tmp_path):
    a = make(tmp_path)
    for _ in range(3):
        a.record("ig_post", approved_without_edit=True)
    assert a.can_run_alone("ig_post")
    a.record("ig_post", approved_without_edit=False, edit_note="captions too long")
    assert not a.can_run_alone("ig_post")


def test_categories_graduate_separately(tmp_path):
    a = make(tmp_path)
    for _ in range(3):
        a.record("inbound_email", approved_without_edit=True)
    assert a.can_run_alone("inbound_email")
    assert not a.can_run_alone("inbound_ig_dm")


def test_pause_switch_overrides_graduation(tmp_path):
    a = make(tmp_path)
    for _ in range(3):
        a.record("host_dm", approved_without_edit=True)
    a.pause("host_dm")
    assert not a.can_run_alone("host_dm")
    assert a.status()["host_dm"] == "paused (approve-first)"
    a.resume("host_dm")
    assert a.can_run_alone("host_dm")


def test_changing_the_process_restarts_the_streak(tmp_path):
    a = make(tmp_path)
    a.record("ig_post", approved_without_edit=True)
    a.record("ig_post", approved_without_edit=True)
    a.process_changed("ig_post")
    assert a.status()["ig_post"] == "0 of 3"


def test_sensitive_topics_always_escalate_even_when_graduated(tmp_path):
    a = make(tmp_path)
    for _ in range(3):
        a.record("inbound_ig_dm", approved_without_edit=True)
    assert a.can_run_alone("inbound_ig_dm", "what time does the mic start?")
    assert not a.can_run_alone("inbound_ig_dm", "I want a refund for my ticket")
    assert must_escalate("I am a journalist writing about comedy")


def test_state_survives_a_restart(tmp_path):
    a = make(tmp_path)
    a.record("ig_post", approved_without_edit=True)
    a.save()
    assert make(tmp_path).status()["ig_post"] == "1 of 3"
