from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class Config:
    exclude: tuple[str, ...] = ()
    weights: dict[str, float] | None = None
    fail_below: int | None = None

def load_config(root: Path, explicit: str | None = None) -> Config:
    path = Path(explicit) if explicit else root / ".production-ai-readiness.json"
    if not path.exists():
        return Config()
    data = json.loads(path.read_text(encoding="utf-8"))
    threshold = data.get("fail_below")
    if threshold is not None and not 0 <= int(threshold) <= 100:
        raise ValueError("fail_below must be between 0 and 100")
    weights = {str(k): float(v) for k, v in data.get("weights", {}).items()}
    return Config(tuple(data.get("exclude", ())), weights or None, int(threshold) if threshold is not None else None)
