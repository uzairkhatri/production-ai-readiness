from production_ai_readiness.scanner import Repository

def test_scanner_detects_path_and_text(tmp_path):
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "test_quality.py").write_text("import logging\nassert score > 0.8\n")
    repo = Repository(tmp_path)
    assert repo.path_contains("eval")
    assert repo.text_contains("logging")
    assert repo.text_contains("assert")
