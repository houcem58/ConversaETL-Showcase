# ConversaETL — Use Cases

Supported ETL patterns with synthetic examples. All data in this document is synthetic.

---

## 1. Temporal Aggregation and Period Comparison

**Business question type:** How did a metric change between two periods?

```
Request: "Compare revenue between Q1 and Q2 2024, broken down by product category.
          Show the absolute and percentage change."

Typed plan:
  task_family:   date_wrangling
  metric:        revenue
  group_by:      [category]
  periods:       [Q1-2024, Q2-2024]
  operator:      period_delta

Output (synthetic):
  category          | Q1_revenue | Q2_revenue | delta   | pct_change | direction
  ------------------+------------+------------+---------+------------+-----------
  Software          |  124,500   |  138,200   | +13,700 |    +11.0%  | increase
  Professional Svcs |   87,300   |   79,100   |  -8,200 |     -9.4%  | decrease
  Hardware          |   45,200   |   51,800   |  +6,600 |    +14.6%  | increase
```

**Why this is hard for direct LLM code generation:**
Period delta requires correct temporal bucketing, null-safe arithmetic, and
a result schema with entity, both period values, delta, and direction — not
just a number. Direct LLM generation frequently produces incorrect period
boundaries, missing direction columns, or unsafe division.

---

## 2. Data Quality Assessment

**Business question type:** What is the quality state of this dataset?

```
Request: "Profile the completeness and validity of the customer table.
          Flag columns with high null rates or suspicious value distributions."

Typed plan:
  task_family:  data_quality
  operator:     profile_and_flag
  targets:      [all columns]
  thresholds:   null_rate > 0.05, type_validity < 0.95

Output (synthetic):
  column           | null_rate | type_valid | anomaly_flag | note
  -----------------+-----------+------------+--------------+-------------------
  customer_id      |   0.000   |    1.000   |     PASS     |
  email            |   0.032   |    0.981   |     PASS     |
  acquisition_date |   0.071   |    0.999   |     FLAG     | null_rate > 0.05
  lifetime_value   |   0.000   |    0.943   |     FLAG     | type_validity < 0.95
  segment          |   0.004   |    1.000   |     PASS     |
```

---

## 3. Multi-Table Join and Aggregation

**Business question type:** What is the combined view across multiple data sources?

```
Request: "What is the average order value and refund rate per customer segment,
          combining order and customer data?"

Typed plan:
  task_family:  aggregate
  join:         orders JOIN customers ON customer_id
  metrics:      [avg_order_value, refund_rate]
  group_by:     [segment]

Output (synthetic):
  segment      | avg_order_value | refund_rate | order_count
  -------------+-----------------+-------------+------------
  Enterprise   |       4,820.00  |       2.1%  |         142
  Mid-Market   |       1,340.00  |       3.7%  |         891
  SMB          |         280.00  |       5.2%  |       3,204
```

**Key challenge addressed:**
The join compiler resolves the join key, enforces cardinality guardrails
(preventing accidental fan-out explosion), and validates required columns
in the post-join result before accepting the output.

---

## 4. Exploratory Insight with Evidence

**Business question type:** Which entities are driving a metric, and in what direction?

```
Request: "Which product categories showed the strongest revenue growth from
          H1 to H2 last year? Provide evidence for each."

Typed plan:
  task_family:   grounded_insight
  metric:        revenue
  entity:        category
  periods:       [H1-2023, H2-2023]
  operator:      ranked_delta
  evidence_cols: [entity, metric_h1, metric_h2, delta, pct_change, direction]

Output — insight tuple (synthetic):
  entity            | metric_h1 | metric_h2 | delta    | pct_change | direction
  ------------------+-----------+-----------+----------+------------+-----------
  Cloud Services    |  89,200   |  142,300  | +53,100  |    +59.5%  | increase
  Professional Svcs |  94,100   |  112,800  | +18,700  |    +19.9%  | increase
  On-Premise SW     | 118,400   |   97,200  | -21,200  |    -17.9%  | decrease

Contract: PASS — entity, both period metrics, delta, direction all present
Audit:    task=grounded_insight, metric=revenue, periods=[H1-2023,H2-2023]
```

**Why evidence columns matter:**
An exploratory insight answer without evidence columns is a claim, not a result.
The contract layer requires entity, both period metric values, delta, and direction
to be present in the output — otherwise the result is rejected. This prevents
the system from returning partial or fabricated insight answers.

---

## 5. Schema Injection and Fuzzy Column Resolution

**Business question type:** Requests with ambiguous or approximate column references.

```
Request: "What are the top 10 customers by total spend?"

Challenge: "Spend" is not a column name. The schema has "amount", "total_amount",
           "invoice_value", and "payment_received" across different tables.

Semantic resolution:
  "spend" → candidate match: amount (orders.amount, confidence: 0.91)
           → secondary: total_amount (invoices.total_amount, confidence: 0.74)
  Selected: orders.amount (primary transaction metric)
  Binding recorded in audit trace.

Output (synthetic):
  customer_id | company_name        | total_spend | order_count
  ------------+---------------------+-------------+------------
  CUST-042    | Meridian Systems    |  284,200.00 |          47
  CUST-019    | Apex Data Group     |  251,700.00 |          38
  ...
```

---

## 6. Operational Monitoring via Streaming

**Business question type:** Is this stream behaving within normal bounds?

```
Configuration:
  Source:    Kafka topic — order_events
  Window:    5-minute tumbling windows
  Monitor:   order_amount distribution drift
  Threshold: KS statistic > 0.15 → drift alert

Runtime output (synthetic):
  window_start         | window_end           | event_count | ks_stat | alert
  ---------------------+----------------------+-------------+---------+-------
  2024-06-15 14:00:00  | 2024-06-15 14:05:00  |         847 |   0.091 | PASS
  2024-06-15 14:05:00  | 2024-06-15 14:10:00  |         912 |   0.082 | PASS
  2024-06-15 14:10:00  | 2024-06-15 14:15:00  |         203 |   0.287 | ALERT ← low volume + drift
```

---

## 7. Cross-Schema Generalization

**Business question type:** Same request pattern, unseen schema.

ConversaETL was evaluated on Spider-ETL-mini — a cross-schema benchmark covering
e-commerce, finance, healthcare, logistics, and support domains. The schema
profiler and semantic resolver generalize the same typed planning approach
to schemas not seen during development.

Delta on cross-schema evaluation: **+0.301** over the compiler-only baseline.

---

## Supported Task Families

| Family | Description | Example Request Pattern |
|--------|-------------|------------------------|
| aggregate / join | Multi-table aggregation with key-explicit joins | "Total X by Y, combining A and B" |
| date_wrangling | Period bucketing, temporal deltas, latency metrics | "Compare X between Q1 and Q2" |
| cleaning / quality | Missingness, type validity, outlier detection | "Profile the completeness of table X" |
| schema / fuzzy | Ambiguous column references, schema-injection prompts | "Top 10 customers by spend" |
| grounded_insight | Evidence-backed exploratory analysis | "Which categories grew fastest" |
| exploratory (streaming) | Drift detection, windowed monitoring | "Alert if order volume drops by 20%" |

---

## Out of Scope (Current Research Version)

- Free-form SQL generation (ConversaETL targets ETL operators, not SQL strings)
- Schema-less or fully unstructured data sources
- Real-time sub-second latency (mean HC path: ~14s with research-grade LLM calls)
- Multi-tenant production deployment
- Enterprise SSO and access-control integration

These are engineering scope boundaries, not architectural limitations.
See [FutureWork.md](FutureWork.md) for the production extension roadmap.
