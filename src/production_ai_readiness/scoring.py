from .models import AuditResult, DimensionResult

def build_result(path: str, dimensions: tuple[DimensionResult, ...]) -> AuditResult:
    score = round(sum(d.score for d in dimensions) / len(dimensions)) if dimensions else 0
    has_high = any(f.severity == "HIGH" for d in dimensions for f in d.findings)
    if score >= 85 and not has_high:
        verdict = "READY"
    elif score >= 60:
        verdict = "NEEDS WORK"
    else:
        verdict = "NOT READY"
    return AuditResult(path, score, verdict, dimensions)
