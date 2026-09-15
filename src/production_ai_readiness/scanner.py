from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = {".git", ".venv", "venv", "node_modules", "vendor", "dist", "build", "__pycache__"}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".env", ".ini", ".cfg"}

@dataclass(frozen=True)
class Evidence:
    path: str
    line: int
    term: str

    def display(self) -> str:
        return f"{self.path}:{self.line} ({self.term})"

class Repository:
    def __init__(self, root: Path, excludes: tuple[str, ...] = ()):
        self.root = root.resolve()
        if not self.root.exists() or not self.root.is_dir():
            raise ValueError(f"Not a directory: {root}")
        self.excludes = set(DEFAULT_EXCLUDES) | set(excludes)
        self.files = tuple(self._files())
        self.paths = tuple(str(p.relative_to(self.root)).lower() for p in self.files)

    def _files(self):
        for p in self.root.rglob("*"):
            rel = p.relative_to(self.root)
            if p.is_file() and not any(part in self.excludes for part in rel.parts):
                yield p

    def path_evidence(self, *terms: str) -> Evidence | None:
        for p, absolute in zip(self.paths, self.files):
            for term in terms:
                if term.lower() in p:
                    return Evidence(str(absolute.relative_to(self.root)), 1, term)
        return None

    def text_evidence(self, *terms: str) -> Evidence | None:
        needles = tuple(t.lower() for t in terms)
        for p in self.files:
            if p.suffix.lower() not in TEXT_SUFFIXES and p.name.lower() not in {"dockerfile", "makefile"}:
                continue
            try:
                for number, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    lower = line.lower()
                    for needle in needles:
                        if needle in lower:
                            return Evidence(str(p.relative_to(self.root)), number, needle)
            except OSError:
                continue
        return None

    def path_contains(self, *terms: str) -> bool:
        return self.path_evidence(*terms) is not None

    def text_contains(self, *terms: str) -> bool:
        return self.text_evidence(*terms) is not None
