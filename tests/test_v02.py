import json
from production_ai_readiness.config import load_config
from production_ai_readiness.scanner import Repository
from production_ai_readiness.rules import evaluate
from production_ai_readiness.scoring import build_result
from production_ai_readiness.reporters import sarif
from production_ai_readiness.baseline import compare

def test_evidence_has_file_and_line(tmp_path):
    (tmp_path/"app.py").write_text("import logging\nlogger = logging.getLogger(__name__)\n")
    result=evaluate(Repository(tmp_path))
    obs=next(d for d in result if d.name=="Observability")
    found=[f for f in obs.findings if f.severity=="PASS" and "Logging" in f.message]
    assert found and "app.py:" in found[0].evidence

def test_config_excludes_and_weights(tmp_path):
    (tmp_path/".production-ai-readiness.json").write_text(json.dumps({"exclude":["generated"],"weights":{"Evaluation":2},"fail_below":70}))
    cfg=load_config(tmp_path)
    assert cfg.exclude==("generated",) and cfg.weights["Evaluation"]==2 and cfg.fail_below==70

def test_sarif_is_valid_shape(tmp_path):
    (tmp_path/"app.py").write_text("print('x')")
    result=build_result(str(tmp_path),evaluate(Repository(tmp_path)))
    doc=json.loads(sarif(result))
    assert doc["version"]=="2.1.0" and doc["runs"][0]["tool"]["driver"]["name"]=="Production AI Readiness"

def test_baseline_comparison(tmp_path):
    (tmp_path/"app.py").write_text("print('x')")
    result=build_result(str(tmp_path),evaluate(Repository(tmp_path)))
    delta=compare(result,{"score":result.score+5,"dimensions":[]})
    assert delta["delta"]==-5
