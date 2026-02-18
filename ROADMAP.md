# ConversaETL — Roadmap

---

## Current Status

ConversaETL is a production-ready applied AI platform. The core system — typed planning,
deterministic compilation, contract validation, and ConversaBench evaluation — is
complete. Published at *Data Science and Engineering* (Springer).

---

## Milestone Overview

```
[DONE]  Research implementation and benchmark evaluation
[DONE]  ConversaBench-Full evaluation (125 prompts × 3 repeats × 3 systems)
[DONE]  Spider-ETL-mini cross-schema evaluation
[DONE]  Streaming drift validation
[DONE]  Dashboard benchmark
[DONE]  Manuscript submission to DSE Springer
[DONE]  Peer review and publication
[DONE]  Portfolio showcase and architecture documentation

[NEXT]  Post-publication artifact release
[NEXT]  Benchmark community contribution (ConversaBench standalone)

[FUTURE] Production hardening (Phase 2)
[FUTURE] Cloud-native deployment (Phase 3)
[FUTURE] Self-serve analytics platform (Phase 4)
```

---

## Research Milestones

| Milestone | Status |
|-----------|--------|
| Core architecture — typed planning + deterministic compilers | Done |
| Plan critic and normalization layer | Done |
| Schema-grounded semantic resolver | Done |
| Contract validation framework | Done |
| Cleaning, date wrangling, join, transform compilers | Done |
| Grounded insight and insight discovery compilers | Done |
| Data quality compiler | Done |
| Sandboxed execution layer | Done |
| ConversaBench-Full benchmark (125 prompts × 3 repeats) | Done |
| Semantic-stress subset and ablation | Done |
| Spider-ETL-mini cross-schema extension | Done |
| Streaming drift benchmark | Done |
| Dashboard benchmark | Done |
| Statistical evaluation (bootstrap CI, repeat-matched) | Done |
| Manuscript submission — DSE Springer | Done |
| Peer review | Done |
| Publication | Done |

---

## Production Extension Roadmap

Full details in [docs/FutureWork.md](docs/FutureWork.md).

### Phase 2 — Production Hardening
- Plan cache for repeated query patterns
- REST API with OpenAPI specification
- Multi-tenant schema isolation
- Enterprise authentication (JWT + RBAC)
- Structured observability (latency tracking, failure dashboards)
- Cloud warehouse compiler targets (Snowflake, BigQuery, Redshift SQL)

### Phase 3 — Platform Extension
- Kubernetes deployment
- dbt integration layer
- Airflow / Prefect DAG emission
- Embedded BI tool widget

### Phase 4 — Self-Serve Analytics
- Scheduled transformation execution
- Lineage tracking
- Collaboration and annotation features
- Federated schema reasoning

---

## Open Research Directions

- Confidence calibration for plan acceptance gating
- Schema evolution handling and binding invalidation
- Multi-LLM ensemble planning for high-ambiguity requests
- Natural language contract specification
- ConversaBench as a standalone community benchmark

See [docs/FutureWork.md](docs/FutureWork.md) for detailed treatment.
