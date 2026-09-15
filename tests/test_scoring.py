from production_ai_readiness.models import DimensionResult, Finding
from production_ai_readiness.scoring import build_result

def dim(name, score, severity="PASS"):
    return DimensionResult(name, score, (Finding(name, severity, "test", "test"),))

def test_ready_requires_high_score_and_no_high_findings():
    result = build_result(".", tuple(dim(str(i), 100) for i in range(8)))
    assert result.score == 100
    assert result.verdict == "READY"

def test_high_finding_prevents_ready():
    dims = [dim(str(i), 100) for i in range(8)]
    dims[0] = dim("Evaluation", 100, "HIGH")
    assert build_result(".", tuple(dims)).verdict == "NEEDS WORK"

def test_low_score_is_not_ready():
    assert build_result(".", tuple(dim(str(i), 0, "HIGH") for i in range(8))).verdict == "NOT READY"
