from hashlib import sha256

def evaluate_flag(
    flag_enabled: bool,
    rollout_percentage: int,
    user_identifier: str,
    flag_key: str,
    overrides: dict,
) -> bool:
    if not flag_enabled:
        return False
    if rollout_percentage == 0:
        return False
    
    hashed_string = sha256(bytes(user_identifier + flag_key, "utf-8")).hexdigest()
    score = int("0x" + hashed_string, 0) 
    if score % 101 > rollout_percentage:
        return False

    return True
