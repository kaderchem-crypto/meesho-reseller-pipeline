import re

def alias_for(name: str) -> str:
    """Provides a safe alias matching test expectations (e.g., RS019 -> ALIAS-19, RS006 -> ALIAS-06)."""
    if not name:
        return "Unknown_Alias"
    match = re.search(r'\d+', name)
    if match:
        num = int(match.group())
        # Format numbers under 100 with zero-padding (e.g., 6 -> 06, 19 -> 19)
        if num < 100:
            return f"ALIAS-{num:02d}"
        return f"ALIAS-{num}"
    return f"ALIAS-{abs(hash(name)) % 1000}"

def assert_no_raw_names_leak(text: str, forbidden_names: list) -> bool:
    """Ensures raw names do not leak into the narrative text."""
    if not text or not forbidden_names:
        return True
    for name in forbidden_names:
        if name and name.lower() in text.lower():
            return False
    return True