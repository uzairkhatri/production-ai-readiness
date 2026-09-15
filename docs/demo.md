# Demo

The repository includes two intentionally different sample applications.

## Incomplete example

```bash
production-ai-readiness audit examples/sample-ai-app
```

This sample contains very little production evidence and should produce multiple findings.

## Production-oriented example

```bash
production-ai-readiness audit examples/production-ready
```

This example deliberately contains repository evidence for several readiness controls: evaluation, validation, retrieval, logging, PII handling, reliability, cost controls and human review.

The examples are not claims that either application is production-safe. They demonstrate how the static evidence model behaves.

## CI gate

```bash
production-ai-readiness audit . --format sarif --output readiness.sarif --fail-below 50
```

This makes the audit useful as a pull-request signal while preserving human review for architecture, runtime behavior, security and model quality.
