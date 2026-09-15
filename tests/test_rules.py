from production_ai_readiness.scanner import Repository
from production_ai_readiness.rules import evaluate

def test_evaluate_returns_all_dimensions(tmp_path):
    (tmp_path / "app.py").write_text("logger = logging\n")
    results = evaluate(Repository(tmp_path))
    assert len(results) == 8
    assert {r.name for r in results} == {"Evaluation","Observability","Guardrails","RAG Quality","Security & PII","Reliability","Cost Controls","Human Oversight"}
