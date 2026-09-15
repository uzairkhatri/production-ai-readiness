import argparse
from pathlib import Path
from .scanner import Repository
from .rules import evaluate
from .scoring import build_result
from .reporters import terminal, json_report, markdown

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="production-ai-readiness", description="Audit repository evidence for production AI readiness.")
    sub = p.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit")
    audit.add_argument("path", nargs="?", default=".")
    audit.add_argument("--format", choices=("terminal", "json", "markdown"), default="terminal")
    audit.add_argument("--output")
    audit.add_argument("--fail-below", type=int, choices=range(0, 101), metavar="0-100")
    return p

def main() -> int:
    args = parser().parse_args()
    try:
        repo = Repository(Path(args.path))
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    result = build_result(str(repo.root), evaluate(repo))
    output = {"terminal": terminal, "json": json_report, "markdown": markdown}[args.format](result)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 1 if args.fail_below is not None and result.score < args.fail_below else 0

if __name__ == "__main__":
    raise SystemExit(main())
