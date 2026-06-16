from detection.sigma.rule_loader import load_rules


def match_event(event: dict) -> list[dict]:
    rules = load_rules()
    return [rule for rule in rules if rule.get("enabled", True)]