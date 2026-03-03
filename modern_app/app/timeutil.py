# filename: modern_app/app/timeutil.py
from datetime import datetime, timezone

def utc_now_z() -> str:
    # ISO 8601 string with Z suffix
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
