import json
from pathlib import Path
from .models import AuditResult

def load_baseline(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def compare(result: AuditResult, baseline: dict) -> dict:
    old={d["name"]:d["score"] for d in baseline.get("dimensions",[])}
    changes=[]
    for d in result.dimensions:
        if d.name in old and d.score != old[d.name]:
            changes.append({"dimension":d.name,"before":old[d.name],"after":d.score,"delta":d.score-old[d.name]})
    return {"score_before":baseline.get("score"),"score_after":result.score,"delta": result.score-baseline.get("score",result.score),"dimensions":changes}
