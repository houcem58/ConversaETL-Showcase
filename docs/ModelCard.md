# Model Card — ConversaETL

**Version:** 1.0.0  
**Date:** 2025-09-01  
**Author:** Houcem Hammami  
**Task type:** Conversational ETL — natural language to typed transformation plan  

---

## System Overview

ConversaETL is a typed compilation approach to conversational ETL. The system converts
natural-language data transformation requests into verified, reproducible dataframe operations
through a five-stage pipeline: LLM planning → plan critique → semantic resolution → deterministic
compilation → contract validation.

**The system does not execute LLM-generated code.** The LLM produces a typed intermediate plan.
All execution is handled by deterministic compilers.

---

## Intended Use

**Intended users:** Data engineers, analytics engineers, business analysts with SQL fluency.

**Intended use cases:**
- Natural-language specification of ETL transformations (aggregation, cleaning, date wrangling, joins)
- Rapid prototyping of data pipeline logic with audit trail
- LLM-assisted data exploration with verifiable outputs

**Out-of-scope uses:**
- General-purpose SQL query generation (different operator scope)
- Real-time data processing (designed for batch ETL workloads)
- Text-to-dashboard or natural-language BI (different output type)

---

## Architecture Summary

| Stage | Component | Input | Output |
|---|---|---|---|
| 1 | LLM Planner | NL request + schema context | Typed intermediate plan |
| 2 | Plan Critic | Raw typed plan | Validated/normalized plan or rejection |
| 3 | Semantic Resolver | Validated plan + schema profile | Grounded plan with column bindings |
| 4 | Compiler Stack (7 families) | Grounded plan + source data | Compiled transformation result |
| 5 | Contract Validator | Compiled result + contract spec | Accepted result or structured rejection |

### Compiler Families

| Family | Operations covered |
|---|---|
| Aggregate | SUM, COUNT, AVG, MIN, MAX with GROUP BY |
| Date wrangling | Period bucketing, temporal deltas, YoY/MoM, fiscal periods |
| Cleaning | Missingness handling, type coercion, deduplication |
| Join | Key-explicit inner/left/right joins with cardinality guards |
| Transform | Derived metrics, conditional logic, pivoting, reshaping |
| Data quality | Expectation checking, profiling, null rate scoring |
| Grounded insight | Evidence-backed exploratory analysis with attribution |

---

## LLM Component

**Model:** LLM-agnostic design; evaluated with GPT-4, Claude 3 Opus, Mistral-7B-Instruct.

**Role:** Plan generation only. The LLM receives:
- Natural-language request
- Schema context (column names, types, sample values, cardinality)
- Task family taxonomy
- Operator constraints

**Output format:** Structured typed plan containing: `task_family`, `operator`, `metric_reference`,
`group_by`, `filters`, `temporal_grain`, `join_requirements`.

**The LLM does not generate code.** All transformation logic is implemented in the compiler stack.

---

## Evaluation: ConversaBench

ConversaBench is the reproducible evaluation benchmark for ConversaETL.

### Benchmark Design

| Component | Description |
|---|---|
| Task-family labels | Each test case labeled by compiler family for structured failure analysis |
| Gold reference outputs | Tables, scalars, and insight tuples with exact expected values |
| Repeated reliability rows | Each test case run 3× for variance estimation |
| Semantic-stress subset | Requests using synonyms, implicit metrics, ambiguous phrasing |
| Frozen evidence artifacts | All reference outputs versioned and frozen for reproducibility |
| Cross-schema extension | Spider-ETL-mini subset for generalization testing |

### Three-Way Ablation

| Condition | Description |
|---|---|
| **HC (Hybrid Compiler)** | Full pipeline: LLM planning + deterministic compilation |
| **CO (Compiler-only)** | Deterministic compilation without LLM planning |
| **LLM (Direct code)** | LLM generates executable code end-to-end (failure-mode baseline) |

### Results (ConversaBench v1.0)

| Condition | Exact match F1 | Schema pass rate | Contract pass rate | Notes |
|---|---|---|---|---|
| HC | 0.847 | 0.923 | 0.891 | Full pipeline |
| CO | 0.712 | 0.889 | 0.834 | No LLM planning |
| LLM | 0.691 | 0.801 | 0.743 | Direct code generation |

**Delta HC vs. CO: +0.135 F1** — LLM planning contributes measurably beyond schema-only compilation.

**Delta HC vs. LLM: +0.156 F1** — Typed compilation outperforms direct code generation under the
no-fallback policy, primarily due to elimination of silent wrong-answer failures.

### Failure Analysis by Task Family

| Task family | HC F1 | CO F1 | Common failure mode |
|---|---|---|---|
| Aggregate | 0.91 | 0.83 | Metric alias resolution |
| Date wrangling | 0.82 | 0.71 | Fiscal period boundaries |
| Cleaning | 0.88 | 0.79 | Implicit dedup intent |
| Join | 0.76 | 0.68 | Ambiguous join key selection |
| Grounded insight | 0.79 | 0.61 | Evidence requirement contracts |

---

## Limitations

1. **Operator scope:** The 7 compiler families cover common ETL operations. Requests outside
   this scope produce explicit rejections, not graceful degradation.

2. **Schema dependency:** The semantic resolver requires a profiled schema. Requests against
   unknown schemas or with heavily nested data may fail at resolution stage.

3. **LLM plan quality:** In CO (compiler-only) mode, F1 drops 13.5 points. The system's
   quality degrades proportionally to LLM plan quality for complex, multi-step requests.

4. **Temporal grain:** Fiscal calendars, non-standard week definitions, and multi-timezone
   scenarios require explicit configuration.

5. **Language:** Designed for English-language requests. Performance on non-English requests
   depends on LLM multilingual capability.

---

## Audit Trail

Every transformation produces a structured audit trace:

```json
{
  "request_id": "req-2025-08-15-001",
  "timestamp": "2025-08-15T09:32:01Z",
  "natural_language": "total revenue by region in Q2 2024",
  "task_family": "aggregate",
  "metric_resolved": "revenue → amount",
  "operator": "sum",
  "period": "2024-Q2",
  "rows_out": 5,
  "contract_status": "PASS",
  "latency_ms": 342
}
```

Rejections produce structured failure records with stage attribution and reason code.
