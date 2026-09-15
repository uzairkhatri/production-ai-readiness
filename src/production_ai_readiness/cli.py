import argparse, json
from pathlib import Path
from .scanner import Repository
from .rules import evaluate
from .scoring import build_result
from .reporters import terminal,json_report,markdown,sarif
from .config import load_config
from .baseline import load_baseline,compare

def parser():
    p=argparse.ArgumentParser(prog="production-ai-readiness",description="Audit repository evidence for production AI readiness.")
    sub=p.add_subparsers(dest="command",required=True); audit=sub.add_parser("audit")
    audit.add_argument("path",nargs="?",default="."); audit.add_argument("--format",choices=("terminal","json","markdown","sarif"),default="terminal")
    audit.add_argument("--output"); audit.add_argument("--fail-below",type=int,choices=range(0,101),metavar="0-100")
    audit.add_argument("--config"); audit.add_argument("--baseline",help="Previous JSON report to compare against")
    audit.add_argument("--diff-output",help="Write baseline comparison as JSON")
    return p

def main():
    args=parser().parse_args(); root=Path(args.path)
    try:
        cfg=load_config(root,args.config); repo=Repository(root,cfg.exclude)
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print(f"error: {exc}"); return 2
    result=build_result(str(repo.root),evaluate(repo),cfg.weights)
    output={"terminal":terminal,"json":json_report,"markdown":markdown,"sarif":sarif}[args.format](result)
    if args.output: Path(args.output).write_text(output+"\n",encoding="utf-8")
    else: print(output)
    if args.baseline:
        try: delta=compare(result,load_baseline(args.baseline))
        except (OSError,json.JSONDecodeError) as exc:
            print(f"error: baseline: {exc}"); return 2
        if args.diff_output: Path(args.diff_output).write_text(json.dumps(delta,indent=2)+"\n",encoding="utf-8")
        else: print(f"Baseline delta: {delta['delta']:+}")
    threshold=args.fail_below if args.fail_below is not None else cfg.fail_below
    return 1 if threshold is not None and result.score<threshold else 0

if __name__=="__main__": raise SystemExit(main())
