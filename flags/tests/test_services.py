from flags.services import evaluate_flag

def test_disabled_flag_returns_false():
    result = evaluate_flag(
        flag_enabled=False,
        rollout_percentage=100,
        user_identifier="user_123",
        flag_key="bzflags-test",
        overrides={}
    )
    assert result is False


def test_fully_enabled_flag_returns_true():
    result = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=100,
        user_identifier="user_123",
        flag_key="bzflags-test",
        overrides={}
    )
    assert result is True
