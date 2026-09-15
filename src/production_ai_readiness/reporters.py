import json
from .models import AuditResult

def terminal(result: AuditResult) -> str:
    lines=["PRODUCTION AI READINESS","="*60,"",f"Overall Score: {result.score} / 100",f"Verdict: {result.verdict}",""]
    for d in result.dimensions:
        filled=round(d.score/10); lines.append(f"{d.name:<21} [{'#'*filled}{'-'*(10-filled)}] {d.score:>3}")
    lines += ["","Findings","-"*60]
    for d in result.dimensions:
        for f in d.findings:
            if f.severity!="PASS": lines.append(f"{f.severity:<7} {d.name:<20} {f.message} [{f.evidence}]")
    return "\n".join(lines)

def json_report(result: AuditResult) -> str: return json.dumps(result.to_dict(),indent=2)

def markdown(result: AuditResult) -> str:
    lines=["# Production AI Readiness Report","",f"**Score:** {result.score}/100  ",f"**Verdict:** {result.verdict}","","## Dimensions","","| Dimension | Score |","|---|---:|"]
    lines += [f"| {d.name} | {d.score} |" for d in result.dimensions]
    lines += ["","## Findings",""]
    for d in result.dimensions:
        for f in d.findings:
            if f.severity!="PASS": lines.append(f"- **{f.severity} · {d.name}:** {f.message} — `{f.evidence}`")
    return "\n".join(lines)

def sarif(result: AuditResult) -> str:
    rules={}; results=[]
    levels={"HIGH":"error","MEDIUM":"warning","LOW":"note"}
    for d in result.dimensions:
        for f in d.findings:
            if f.severity=="PASS": continue
            rule_id=d.name.lower().replace(" & ","-").replace(" ","-")
            rules[rule_id]={"id":rule_id,"name":d.name,"shortDescription":{"text":d.name+" readiness"}}
            results.append({"ruleId":rule_id,"level":levels[f.severity],"message":{"text":f.message+" "+f.evidence}})
    doc={"version":"2.1.0","$schema":"https://json.schemastore.org/sarif-2.1.0.json","runs":[{"tool":{"driver":{"name":"Production AI Readiness","rules":list(rules.values())}},"results":results}]}
    return json.dumps(doc,indent=2)
