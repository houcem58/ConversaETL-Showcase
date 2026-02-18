# ConversaETL — Future Work and Research Roadmap

This document describes planned extensions, open research problems, and the
production development roadmap. It reflects architectural thinking, not committed
delivery timelines.

---

## Phase 1 — Research Completion (In Progress)

### Benchmark Scope Extension
- Extend ConversaBench to additional task families: window functions, recursive
  aggregations, slowly-changing dimension patterns
- Expand cross-schema evaluation coverage (current: 5 domain schemas in Spider-ETL-mini)
- Add adversarial prompts designed to trigger specific compiler failure modes

### Compiler Stack Hardening
- Improved handling of highly ambiguous schema contexts with multiple plausible bindings
- Richer date resolution for fiscal year, custom calendar, and relative temporal references
- Deeper multi-table join reasoning (current: explicit two-table joins; planned: inferred
  multi-hop join paths from schema relationship profiling)

### Evaluation Methodology
- Calibration study: relationship between plan-level LLM confidence and output correctness
- Longitudinal stability study: correctness variance across LLM provider versions
- Latency profiling: per-stage breakdown for optimization targeting

---

## Phase 2 — Production Hardening

### Performance and Scalability
- **Plan cache:** Schema-conditioned plan reuse for semantically equivalent requests
  (estimated 60–80% cache hit rate for recurring query patterns)
- **Streaming compilation:** Result delivery as a stream rather than a blocking response
- **Parallel compiler dispatch:** Independent compiler families executed in parallel
  where plan structure permits
- **Provider tiering:** Route simple requests to smaller/faster models; complex
  requests to larger models — reducing per-request LLM cost

### Enterprise Integration
- REST API layer with OpenAPI specification for programmatic access
- SDK / client library (Python first)
- Authentication and authorization middleware (JWT + RBAC)
- Webhook support for async result delivery on long-running transformations

### Multi-Tenancy and Isolation
- Schema namespace isolation per tenant
- Result and audit trace partitioning
- Per-tenant LLM provider configuration
- Tenant-specific semantic alias dictionaries

### Observability and Monitoring
- Structured logging export (JSON, compatible with ELK / Datadog / CloudWatch)
- Latency percentile tracking per compiler family and per task family
- Plan success/failure rate dashboards
- Semantic drift detection: alert when request patterns shift beyond training distribution

---

## Phase 3 — Platform Extension

### Cloud-Native Deployment
- Kubernetes operator for horizontal scaling of the compiler and planning stages
- Serverless planning tier (AWS Lambda / GCP Cloud Run) for low-traffic deployments
- Managed schema registry integration (Confluent Schema Registry, AWS Glue)

### Data Platform Integration
- **dbt integration:** ConversaETL as a conversational layer over existing dbt models
- **Airflow / Prefect integration:** Generated transformation plans emitted as
  workflow DAGs for pipeline registration
- **Snowflake / BigQuery / Redshift:** Compiler targets for cloud warehouse SQL dialects
  alongside the current pandas-based execution layer

### Self-Service Analytics Layer
- Embedded widget for BI tool integration (Tableau, Power BI, Looker)
- Scheduled transformation execution with lineage tracking
- Collaboration features: shared request history, annotation, result sharing

---

## Open Research Problems

### 1. Confidence Calibration for Plan Acceptance
The current plan critic uses structural validation. A calibrated confidence score
on the typed plan — estimating the probability that the plan correctly represents
the user's intent — would enable better routing decisions (direct to compiler vs.
clarification request vs. rejection).

### 2. Schema Evolution Handling
When the underlying schema changes (new columns, renamed columns, changed types),
the semantic resolver bindings may become stale. An online schema diffing component
that updates bindings and flags affected cached plans is an open engineering problem.

### 3. Multi-LLM Ensemble Planning
For high-ambiguity requests, an ensemble of smaller models with voting on the typed
plan structure may outperform a single large model call — with lower cost and latency.
The current architecture supports this without changes to the compiler stack.

### 4. Federated Schema Reasoning
Enterprise data estates span multiple systems (warehouse, lake, operational databases,
SaaS APIs). Extending the schema profiler to reason across federated schemas — resolving
references that span system boundaries — requires work on entity resolution at scale.

### 5. Natural Language Contract Specification
Currently, output contracts are embedded in the compiler stack. A future direction
is enabling users to specify contracts in natural language:
*"The result must include all regions, even those with zero revenue."*
Translating such constraints into formal contract specifications is an open problem.

---

## Benchmark Community Contribution

ConversaBench is designed as a benchmark contribution for the conversational ETL
research community, not only as an internal test suite. Planned contributions:

- Public release of the benchmark prompt sets and gold references (subject to
  dataset licensing constraints)
- Evaluation harness as a standalone package
- Leaderboard infrastructure for cross-system comparison
- Extension guidelines for new task families and datasets

The current benchmark is tightly coupled to the ConversaETL evaluation. Decoupling
it into an independent community resource is a planned post-publication effort.
