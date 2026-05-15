# Contributing

Thank you for your interest in contributing to the ConversaETL showcase.

> **Note:** This repository contains only the public showcase layer. The full implementation
> (LLM planning engine, compiler, contract validator) is in a private repository.
> Research manuscript is under review — please do not reproduce evaluation claims without
> citing the original work (see [docs/FAQ.md](docs/FAQ.md)).
>
> Contributions here focus on the demo, documentation, and architecture descriptions.

## Ways to Contribute

- **Demo improvements** — extend `demo/examples/` with new ETL scenario illustrations
- **Documentation** — improve any doc in `docs/` (clarity, examples, use case additions)
- **Bug reports** — issues in the demo scripts or broken Markdown links
- **Use case descriptions** — document new ETL scenarios the architecture could address

## Development Setup

```bash
git clone https://github.com/houcem58/ConversaETL-Showcase.git
cd ConversaETL-Showcase
pip install pandas numpy
pip install pre-commit
pre-commit install
```

## Running the Demo

```bash
cd demo/examples
python 01_basic_query.py
python 02_multi_table_analysis.py
```

## Code Standards

- `ruff check demo/` must pass with no errors
- No external dependencies beyond `pandas` and `numpy` in demo scripts
- Demo scripts must run to completion in under 10 seconds on a laptop
- All data must be synthetic — no real customer data of any kind
- ConversaETL-specific terminology must match `docs/Architecture.md` exactly

## Adding a Demo Example

1. Add `demo/examples/03_your_scenario.py`
2. Use only `pandas` and `numpy` (already in requirements)
3. Must complete in under 10 seconds
4. Output must clearly show what the scenario illustrates
5. Update `demo/README.md` with a one-line description

## Documentation Standards

- Numeric claims about pipeline performance must reference the evaluation manuscript
- Note "under review" status appropriately — do not claim publication where not yet confirmed
- Internal links must use relative paths

## Pull Request Process

1. Branch from `main`
2. All CI checks must pass: lint, demo-smoke-test, docs-check
3. Update `CHANGELOG.md` under `[Unreleased]`
4. PRs require one reviewer approval
