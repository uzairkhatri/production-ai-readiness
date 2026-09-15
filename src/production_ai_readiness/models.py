from dataclasses import dataclass, asdict
from typing import Literal

Severity = Literal["PASS", "LOW", "MEDIUM", "HIGH"]

@dataclass(frozen=True)
class Finding:
    dimension: str
    severity: Severity
    message: str
    evidence: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class DimensionResult:
    name: str
    score: int
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict:
        return {"name": self.name, "score": self.score,
                "findings": [f.to_dict() for f in self.findings]}

@dataclass(frozen=True)
class AuditResult:
    path: str
    score: int
    verdict: str
    dimensions: tuple[DimensionResult, ...]

    def to_dict(self) -> dict:
        return {"path": self.path, "score": self.score, "verdict": self.verdict,
                "dimensions": [d.to_dict() for d in self.dimensions]}
