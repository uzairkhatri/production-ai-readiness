from .models import AuditResult, DimensionResult

def build_result(path: str, dimensions: tuple[DimensionResult, ...], weights: dict[str,float] | None = None) -> AuditResult:
    if not dimensions:
        score=0
    elif weights:
        total=sum(max(0,weights.get(d.name,1.0)) for d in dimensions)
        score=round(sum(d.score*max(0,weights.get(d.name,1.0)) for d in dimensions)/total) if total else 0
    else:
        score=round(sum(d.score for d in dimensions)/len(dimensions))
    has_high=any(f.severity=="HIGH" for d in dimensions for f in d.findings)
    verdict="READY" if score>=85 and not has_high else "NEEDS WORK" if score>=60 else "NOT READY"
    return AuditResult(path,score,verdict,dimensions)
