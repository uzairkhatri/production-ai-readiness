from pathlib import Path

DEFAULT_EXCLUDES = {".git", ".venv", "venv", "node_modules", "vendor", "dist", "build", "__pycache__"}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".env", ".ini", ".cfg"}

class Repository:
    def __init__(self, root: Path):
        self.root = root.resolve()
        if not self.root.exists() or not self.root.is_dir():
            raise ValueError(f"Not a directory: {root}")
        self.files = tuple(self._files())
        self.paths = tuple(str(p.relative_to(self.root)).lower() for p in self.files)

    def _files(self):
        for p in self.root.rglob("*"):
            if p.is_file() and not any(part in DEFAULT_EXCLUDES for part in p.parts):
                yield p

    def path_contains(self, *terms: str) -> bool:
        terms = tuple(t.lower() for t in terms)
        return any(any(t in p for t in terms) for p in self.paths)

    def text_contains(self, *terms: str) -> bool:
        needles = tuple(t.lower() for t in terms)
        for p in self.files:
            if p.suffix.lower() not in TEXT_SUFFIXES and p.name.lower() not in {"dockerfile", "makefile"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            if any(n in text for n in needles):
                return True
        return False
