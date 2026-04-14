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


def test_zero_percent_rollout_returns_false():
    result = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=0,
        user_identifier="user_123",
        flag_key="bzflags-test",
        overrides={}
    )
    assert result is False


def test_rollout_is_deterministic():
    user_identifier = "user_123"
    flag_key = "bzflags-test"

    result_1 = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=50,
        user_identifier=user_identifier,
        flag_key=flag_key,
        overrides={}
    )

    result_2 = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=50,
        user_identifier=user_identifier,
        flag_key=flag_key,
        overrides={}
    ) 

    assert result_1 == result_2 


def test_sticky_rollouts():
    user_identifier = "user_123"
    flag_key = "bzflags-test"

    result_1 = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=90,
        user_identifier=user_identifier,
        flag_key=flag_key,
        overrides={}
    )

    result_2 = evaluate_flag(
        flag_enabled=True,
        rollout_percentage=10,
        user_identifier=user_identifier,
        flag_key=flag_key,
        overrides={}
    )

    assert not result_2 or result_1
