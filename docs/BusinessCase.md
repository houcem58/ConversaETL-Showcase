# ConversaETL — Business Case

---

## The Cost of Schema-Specific ETL

Enterprise organizations maintain hundreds to thousands of ETL pipelines.
Each pipeline is schema-specific: written for a particular source, a particular
transformation pattern, and a particular downstream consumer.

When business questions change, pipelines must be rewritten.
When schemas evolve, pipelines break.
When new data sources are onboarded, the engineering cycle begins again.

**The bottleneck is not data availability. It is data access engineering.**

Industry data suggests that data engineering teams spend 60–80% of their
capacity on pipeline maintenance rather than new capability delivery. The
time from a business question to a validated analytical result — through
ticket submission, engineering prioritization, development, QA, and deployment
— commonly runs from days to weeks for non-trivial transformations.

---

## Target Personas

### Data Engineering Manager
Responsible for pipeline reliability, team capacity, and delivery velocity.
ConversaETL reduces the schema-specific pipeline backlog by enabling
validated transformation generation for common ETL patterns conversationally.

### Head of Analytics / BI
Responsible for insight delivery to business stakeholders. ConversaETL
compresses the time from a business question to a validated analytical result,
reducing dependency on engineering pipeline delivery for exploratory analysis.

### Chief Data Officer / VP Data
Responsible for data governance, compliance, and platform investment.
ConversaETL's audit trace architecture and contract-validated outputs support
governance requirements — every transformation is traceable, every rejection
is logged, and unsafe operations are blocked by design.

### Enterprise Architect
Responsible for data platform architecture decisions. ConversaETL demonstrates
that LLM-assisted systems can be architected with deterministic execution paths
and contract-enforced acceptance — not just probabilistic generation.

---

## Value Proposition by Dimension

### Engineering Velocity
Supported ETL patterns (aggregation, date wrangling, multi-table joins, data
quality checks, exploratory insight synthesis) can be generated conversationally
rather than written as schema-specific pipeline code.

For teams managing large schema portfolios, this reduces the per-schema
engineering cost for exploratory and ad-hoc transformation requests.

### Governance and Auditability
The contract validation layer provides a structured acceptance gate that
traditional pipeline approaches lack. Every result:
- Has passed schema-shape validation
- Has passed quality and null-bound constraints
- Has passed evidence requirements (for analytical outputs)
- Is accompanied by an audit trace recording operator selection,
  schema bindings, and contract decisions

This auditability is relevant for regulated industries where transformation
provenance and output accountability are compliance requirements.

### Reliability by Design
The 100% execution success rate on the full benchmark (compared to 70% for
direct LLM code generation) reflects the architectural choice to block invalid
outputs rather than return them. The system fails explicitly, not silently.

In production data pipelines, silent failures — wrong results accepted as
correct — are more costly than explicit rejections. ConversaETL is designed
to prefer explicit rejection over silent acceptance.

### Cross-Schema Generalization
The cross-schema evaluation on Spider-ETL-mini demonstrates +0.301 correctness
delta on unseen schemas, compared to the compiler-only baseline. This suggests
the typed planning approach generalizes beyond the schemas used during development
— a property required for enterprise deployment across heterogeneous data estates.

### Reduced Onboarding Cost
Traditional ETL pipelines must be developed schema-by-schema. ConversaETL's
schema profiler and semantic resolver reduce the per-schema onboarding overhead
by grounding natural-language references to actual schema columns at request time.

---

## Comparison to Adjacent Approaches

| Approach | ETL Operators | Schema Grounding | Audit Trail | Deterministic Execution | Conversational |
|----------|:------------:|:----------------:|:-----------:|:-----------------------:|:--------------:|
| Manual SQL / Pipelines | Full | Manual | Varies | Yes | No |
| Text-to-SQL (RAT-SQL, PICARD) | SQL only | Schema-linked | No | Yes (SQL) | Partial |
| LLM Data Agents | Variable | Prompt-dependent | No | No | Yes |
| dbt / Airflow / Talend | Full | Schema-coupled | Partial | Yes | No |
| **ConversaETL** | **ETL + Insight** | **Typed + Semantic** | **Yes** | **Yes** | **Yes** |

ConversaETL does not replace workflow orchestration tools. It addresses the
gap between natural-language business questions and verified ETL transformations —
a gap that existing tools, including LLM code agents, leave open.

---

## ROI Framework

The business case for a ConversaETL deployment depends on:

1. **Schema portfolio size** — organizations with larger schema estates benefit more
   from per-schema engineering cost reduction

2. **Exploratory analysis volume** — high-frequency ad-hoc transformation requests
   benefit most from conversational access vs. ticket-based pipeline delivery

3. **Compliance requirements** — regulated industries benefit from the audit trail
   and deterministic execution architecture

4. **LLM inference cost** — the typed planning stage incurs LLM API cost per request;
   the compiler and validation stages are deterministic and low-cost

A rough order-of-magnitude analysis: if engineering time for a single ad-hoc
transformation pipeline runs 2–8 hours (development + QA), and ConversaETL
reduces this to minutes for supported patterns, the break-even on deployment
investment depends primarily on request volume and engineering hourly cost.

---

## Limitations and Honest Scope

ConversaETL is a production-ready platform. Its business value claims are grounded in
rigorous benchmark evaluation with frozen reproducibility artifacts.

**Current scope limitations:**
- Evaluated on three dataset families (NASA, Retail, Olist)
- Task families cover common ETL patterns but not the full ETL surface
- The typing system has recognized gaps on highly ambiguous requests
- Multi-tenant isolation, access control, and enterprise SSO are not implemented
- Latency (~14s mean for the hybrid path) reflects research-grade LLM calls,
  not an optimized production configuration

These are engineering scope limitations, not architectural ones. The core
architecture — typed planning, deterministic compilation, contract validation —
is designed with production extension in mind. See [FutureWork.md](FutureWork.md).
