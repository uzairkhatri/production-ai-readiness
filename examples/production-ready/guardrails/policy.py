"""Illustrative input/output policy boundary."""
def validate_input(value: str) -> str:
    if not value.strip():
        raise ValueError("input is required")
    return value
