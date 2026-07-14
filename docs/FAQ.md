# ConversaETL — Frequently Asked Questions

---

## About the Project

**Q: What is ConversaETL?**

ConversaETL is an applied AI research system for conversational enterprise ETL.
It converts natural-language data transformation requests into validated, auditable
ETL outputs using a combination of LLM-assisted typed planning and a deterministic
compiler stack. See the [Architecture](Architecture.md) document for details.

---

**Q: Is this a text-to-SQL system?**

No. ConversaETL targets ETL operators — cleaning, date wrangling, joins, derived
metrics, exploratory insight synthesis — rather than SQL query strings. The accepted
transformation output is usually a structured dataframe operation, not a SQL statement.
The positioning relative to text-to-SQL systems is discussed in [Architecture.md](Architecture.md).

---

**Q: How does ConversaETL differ from LLM data agents?**

LLM data agents generate executable code or tool calls end-to-end. ConversaETL
bounds the LLM to intent inference only — it produces a typed plan, not code.
Execution is handled by deterministic compilers. This means:

- The execution path is bounded and predictable
- Schema hallucinations are caught at the semantic resolution stage
- Unsafe operations are blocked by design
- Every output passes contract validation before acceptance

The direct LLM code generation baseline in the benchmark evaluation (mean correctness:
0.308, 70% execution success rate) demonstrates what unconstrained code generation
produces under controlled conditions.

---

**Q: Is this production-ready?**

Yes. ConversaETL is a production-ready platform with full engineering implementation,
evaluated under rigorous benchmark conditions. The [Future Work](FutureWork.md)
document describes the enterprise extension roadmap (cloud deployment, multi-tenancy,
third-party integrations).

---

## Source Code and Research

**Q: Why isn't the full source code available?**

ConversaETL is the subject of research currently under review at *Data Science
and Engineering* (Springer). The full implementation — including the compiler stack,
benchmark framework, evaluation engine, and reproducibility artifacts — remains in
a private repository.

This repository is a portfolio showcase demonstrating the architecture, engineering
approach, and evaluation results of the project.

---

**Q: Will the source be released?**

A public research artifact repository is being evaluated, subject to journal
artifact policy. Contact houcem0508@gmail.com for access to the evaluation package.

---

**Q: Is there a publication I can read?**

The manuscript is currently under review. Key results are summarized in the
[README](../README.md) and [Business Case](BusinessCase.md). Contact
houcem0508@gmail.com for details.

---

**Q: Can I reproduce the benchmark results?**

The benchmark framework (ConversaBench) and evaluation artifacts are in the private
research repository. Compact evidence summaries are available in the private artifact
repository at `reproducibility/evidence/`. Full reproducibility requires dataset access
(NASA HTTP logs, Online Retail II, Olist) — see the data acquisition guidance in
the private repository's DATA.md.

---

## Collaboration and Contact

**Q: Can researchers contact you about this work?**

Yes. For research collaboration, benchmark methodology questions, or paper-related
inquiries: houcem0508@gmail.com

---

**Q: Can recruiters or hiring managers request a technical walkthrough?**

Yes. If you are evaluating this project as part of a hiring process and would
like a technical walkthrough, architecture discussion, or live demo: houcem0508@gmail.com

Specifically available for discussion:
- System architecture and design decisions
- Benchmark methodology and evaluation approach
- Compiler stack design principles
- Production extension roadmap
- Streaming and operational monitoring architecture

---

**Q: Are you open to collaboration on enterprise AI platform projects?**

Yes, in the context of employment. I am open to Technical Manager, AI Platform Lead,
and Engineering Manager roles in AI/Data platform development. See the About section
in the README for current availability.

---

## Technical Questions

**Q: What LLM providers does it support?**

The planning stage is compatible with Groq (cloud), Ollama (local/offline), and any
OpenAI-compatible provider. Provider selection is configuration-driven with no code
changes required.

---

**Q: What is the mean latency?**

The hybrid compiler path (HC) has a mean latency of approximately 14 seconds in the
benchmark evaluation, dominated by LLM planning API call time. This reflects
research-grade LLM calls without caching or batching optimization. Production
latency would benefit from plan caching, streaming responses, and provider selection.

---

**Q: Does it support streaming data?**

Yes. A Kafka-backed streaming component handles drift detection, windowed aggregate
computation, and operational monitoring. The streaming architecture is separate from
the batch ETL pipeline and shares the same schema-grounded semantic model.

---

**Q: What datasets were used for evaluation?**

Three complementary datasets representing different enterprise data substrates:
- **NASA HTTP logs** (~1.5M records) — operational/time-series data
- **Online Retail II** (~541K transactions) — transactional business data
- **Olist** — multi-table relational e-commerce (9 tables: orders, customers,
  products, sellers, payments, reviews, geolocation, order items, category translations)

Raw datasets are not redistributed. They are publicly available from their original
sources. The Spider-ETL-mini cross-schema extension uses synthetic tabular data
across e-commerce, finance, healthcare, logistics, and support domains.
