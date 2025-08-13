# ConversaETL Demo

Self-contained conceptual illustration of the ConversaETL pipeline.
Uses synthetic data only. No connection to external services or APIs required.

---

## What This Demonstrates

These examples illustrate:

1. **The typed intermediate representation** — the structured plan that the
   LLM-assisted planner produces (not raw code)
2. **Plan critique** — structural validation before compilation
3. **Semantic resolution** — binding natural-language references to schema columns
4. **Deterministic execution** — bounded dataframe operations, not LLM-generated code
5. **Contract validation** — schema and quality checks before result acceptance
6. **Audit traces** — structured record of every pipeline decision

This is a simplified educational illustration. The production system's LLM
planner, compiler stack, and evaluation engine are not exposed here.

---

## Requirements

```bash
pip install pandas
```

---

## Examples

### Example 1 — Basic Temporal Aggregation

Processes the request: *"What are total sales by product category in Q2 2024?"*

Demonstrates: period filtering, semantic metric resolution, aggregation, contract validation.

```bash
python examples/01_basic_query.py
```

Expected output:

```
=================================================================
  ConversaETL — Conceptual Pipeline Illustration
  Example: Temporal Aggregation with Period Filter
=================================================================

[STAGE 1 — INPUT]
  Query: "What are total sales by product category in Q2 2024, ranked by revenue?"

[STAGE 1 — TYPED PLAN]
TypedETLPlan {
  query      : 'What are total sales by product category in Q2 2024...'
  task_family: aggregate
  metric     : revenue
  group_by   : ['category']
  period     : 2024-Q2
  operator   : sum
  filters    : {}
}

[STAGE 2 — PLAN CRITIQUE]  OK
[STAGE 3 — SEMANTIC RESOLUTION]  'revenue' → 'amount'
[STAGE 4 — COMPILATION]  2 rows produced
[STAGE 5 — VALIDATION]  CONTRACT PASS

[OUTPUT — Validated ETL Result]
-----------------------------------------
      category  total_amount
       Software       14470.5
      Services        2800.0
-----------------------------------------

[AUDIT TRACE]
  task_family : aggregate
  metric      : revenue → amount
  period      : 2024-Q2
  operator    : sum
  rows_out    : 2
  contract    : PASS
```

---

### Example 2 — Multi-Table Analysis with Join Resolution

Processes the request: *"What is the average order value and refund rate per
customer segment in EMEA?"*

Demonstrates: multi-table join, cardinality guard, derived metric computation,
group_by semantic resolution.

```bash
python examples/02_multi_table_analysis.py
```

---

## Synthetic Data

| File | Description | Rows |
|------|-------------|------|
| `sample_data/orders.csv` | Transaction orders with amount, date, status, region | 30 |
| `sample_data/customers.csv` | Customer accounts with segment and region | 9 |
| `sample_data/products.csv` | Product catalog with category and pricing | 9 |

All data is fully synthetic. No personal information, no real business records.

---

## What Is Not Shown Here

The following components from the production system are not included in this demo:

- LLM-assisted typed planner (requires LLM provider credentials)
- Full semantic metric resolver with cross-table candidate scoring
- Deterministic compiler stack (7 compiler families)
- ConversaBench evaluation framework
- Streaming pipeline (requires Kafka)
- Dashboard interface (requires Gradio/Dash)

These components are in the private research repository.
See [docs/Architecture.md](../docs/Architecture.md) for the full system description.
