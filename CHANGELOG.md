# Changelog

All notable changes to Production AI Readiness are documented here.

## 0.2.0 — 2026-09-16

### Added

- configurable exclusions, readiness thresholds and dimension weights
- file-and-line evidence for detected controls
- baseline report comparison and score deltas
- SARIF output for GitHub Code Scanning
- pull-request readiness workflow
- concrete low-evidence and production-oriented demo applications
- demo walkthrough and additional v0.2 tests

### Changed

- readiness findings now provide stronger evidence context
- scoring supports weighted dimensions

### Safety boundary

Production AI Readiness remains a static repository-evidence tool. A high score is not a certification of production safety, security, compliance or model quality.

## 0.1.0

Initial CLI with eight production-readiness dimensions, deterministic scanning, scoring, terminal/JSON/Markdown reports, tests and CI.
