# Changelog

All notable changes to this showcase repository are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.2.0] — 2026-01-20

### Added
- `CONTRIBUTING.md` — contributor guide for demo and documentation contributions
- `Makefile` — `make demo`, `make lint`, `make docker-build`
- `.pre-commit-config.yaml` — ruff + pre-commit-hooks
- `.dockerignore` — exclude dev artifacts from Docker build context

---

## [1.1.0] — 2025-12-15

### Added
- Unified `pipeline.yml` — replaces separate ci.yml + cd.yml
- `concurrency` group to cancel stale runs
- Docker image publish to GHCR on main push

### Changed
- Moved from `workflow_run` trigger to direct `push: branches: [main]`

---

## [1.0.0] — 2025-11-15

### Added
- README: The Problem, The Solution, Architecture, Pipeline Overview, Key Capabilities
- `demo/` — self-contained showcase using synthetic multi-table data
  - `01_basic_query.py` — single-table ETL from natural language
  - `02_multi_table_analysis.py` — multi-source join scenario
- `docs/Architecture.md` — system design: planner, compiler, validator layers
- `docs/BusinessCase.md` — enterprise ROI framework, target environments
- `docs/UseCases.md` — supported ETL scenarios with examples
- `docs/FAQ.md` — common questions including research and publication status
- `docs/FutureWork.md` — planned enhancements
- `ROADMAP.md` — near/medium/long-term directions
- `SECURITY.md` — responsible disclosure, private repo notice
- Apache 2.0 license
