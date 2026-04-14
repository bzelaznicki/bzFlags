def evaluate_flag(
    flag_enabled: bool,
    rollout_percentage: int,
    user_identifier: str,
    flag_key: str,
    overrides: dict,
) -> bool:
    if not flag_enabled:
        return False
