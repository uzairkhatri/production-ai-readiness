import json
from .models import AuditResult

def terminal(result: AuditResult) -> str:
    lines = ["PRODUCTION AI READINESS", "=" * 60, "", f"Overall Score: {result.score} / 100", f"Verdict: {result.verdict}", ""]
    for d in result.dimensions:
        filled = round(d.score / 10)
        lines.append(f"{d.name:<21} [{'#'*filled}{'-'*(10-filled)}] {d.score:>3}")
    lines += ["", "Findings", "-" * 60]
    for d in result.dimensions:
        for f in d.findings:
            if f.severity != "PASS":
                lines.append(f"{f.severity:<7} {d.name:<20} {f.message}")
    return "\n".join(lines)

def json_report(result: AuditResult) -> str:
    return json.dumps(result.to_dict(), indent=2)

def markdown(result: AuditResult) -> str:
    lines = ["# Production AI Readiness Report", "", f"**Score:** {result.score}/100  ", f"**Verdict:** {result.verdict}", "", "## Dimensions", "", "| Dimension | Score |", "|---|---:|"]
    lines += [f"| {d.name} | {d.score} |" for d in result.dimensions]
    lines += ["", "## Findings", ""]
    for d in result.dimensions:
        for f in d.findings:
            if f.severity != "PASS":
                lines.append(f"- **{f.severity} · {d.name}:** {f.message} _{f.evidence}_")
    return "\n".join(lines)
