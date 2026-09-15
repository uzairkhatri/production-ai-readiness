from dataclasses import dataclass
from .models import Finding, DimensionResult
from .scanner import Repository

@dataclass(frozen=True)
class Check:
    label: str
    kind: str
    terms: tuple[str, ...]
    severity: str
    missing: str

RULES = {
    "Evaluation": (
        Check("evaluation suite", "path", ("eval", "evaluation"), "HIGH", "No dedicated AI evaluation evidence detected."),
        Check("quality assertions", "text", ("assert", "metric", "score", "expected"), "MEDIUM", "No quality assertion/metric evidence detected."),
    ),
    "Observability": (
        Check("telemetry", "text", ("opentelemetry", "langfuse", "langsmith", "prometheus", "trace_id"), "HIGH", "No AI tracing/telemetry evidence detected."),
        Check("logging", "text", ("logging", "logger", "structlog"), "MEDIUM", "No application logging evidence detected."),
    ),
    "Guardrails": (
        Check("validation", "text", ("pydantic", "validate", "schema", "guardrail"), "HIGH", "No structured validation/guardrail evidence detected."),
        Check("policy", "path", ("policy", "guardrail", "safety"), "MEDIUM", "No explicit policy/guardrail module detected."),
    ),
    "RAG Quality": (
        Check("retrieval", "text", ("retriev", "vector", "embedding", "rerank"), "MEDIUM", "No retrieval/RAG implementation evidence detected."),
        Check("retrieval evaluation", "text", ("recall@", "precision@", "mrr", "ndcg", "retrieval_eval"), "HIGH", "No retrieval-quality evaluation evidence detected."),
    ),
    "Security & PII": (
        Check("security controls", "text", ("authorize", "authentication", "permission", "secret", "api_key"), "HIGH", "No security/authentication control evidence detected."),
        Check("PII/privacy", "text", ("pii", "redact", "privacy", "personal data"), "MEDIUM", "No PII/privacy handling evidence detected."),
    ),
    "Reliability": (
        Check("timeouts/retries", "text", ("timeout", "retry", "backoff", "tenacity"), "HIGH", "No timeout/retry evidence detected."),
        Check("fallbacks", "text", ("fallback", "circuit breaker", "circuit_breaker"), "MEDIUM", "No fallback/circuit-breaker evidence detected."),
    ),
    "Cost Controls": (
        Check("usage controls", "text", ("token_budget", "cost_limit", "rate_limit", "rate limit", "quota"), "MEDIUM", "No explicit token/cost/rate-limit control evidence detected."),
        Check("caching", "text", ("cache", "redis"), "LOW", "No caching evidence detected."),
    ),
    "Human Oversight": (
        Check("approval", "text", ("human_in_the_loop", "human-in-the-loop", "approval", "requires_review"), "HIGH", "No human approval/review mechanism evidence detected."),
        Check("escalation", "text", ("escalat", "manual review", "human review"), "MEDIUM", "No escalation/manual-review evidence detected."),
    ),
}

def evaluate(repo: Repository) -> tuple[DimensionResult, ...]:
    results = []
    for dimension, checks in RULES.items():
        findings = []
        passed = 0
        for check in checks:
            ok = repo.path_contains(*check.terms) if check.kind == "path" else repo.text_contains(*check.terms)
            if ok:
                passed += 1
                findings.append(Finding(dimension, "PASS", f"{check.label.capitalize()} evidence detected.", ", ".join(check.terms)))
            else:
                findings.append(Finding(dimension, check.severity, check.missing, f"Searched: {', '.join(check.terms)}"))
        results.append(DimensionResult(dimension, round(100 * passed / len(checks)), tuple(findings)))
    return tuple(results)
