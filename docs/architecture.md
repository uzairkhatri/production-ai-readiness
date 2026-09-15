# Architecture

Production AI Readiness intentionally starts with a deterministic static-analysis core.

```text
CLI
 |
 v
Repository Scanner
 |
 v
Rule Engine (8 dimensions)
 |
 v
Scoring
 |
 +--> Terminal
 +--> JSON
 +--> Markdown
```

## Trust boundary

The scanner treats the target repository as untrusted input. v0.1 reads text files but does not execute target code, import the target project, call external services, or send repository content to an LLM.

## Rule philosophy

Rules should be explainable and evidence-based. A detector should say what it searched for. Absence of static evidence is a finding about **coverage/evidence**, not proof that a runtime control is absent.

Future runtime adapters should remain opt-in and separate from the static core.
