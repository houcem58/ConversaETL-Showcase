# ADR-001 — Typed Intermediate Plan vs. Direct Code Generation

**Status:** Accepted  
**Date:** 2025-09-01  
**Author:** Houcem Hammami  
**Reviewers:** —  

---

## Context

ConversaETL must convert natural-language ETL requests into executable data transformations.
The primary design question is: should the LLM generate executable code directly, or should
it generate a structured intermediate representation that a deterministic compiler then executes?

Three approaches were evaluated during the research phase:

**Option A — Direct LLM code generation**  
The LLM receives the natural-language request and schema context and outputs executable Python
(pandas) or SQL code. The code is executed directly.

**Option B — LLM-to-AST with code execution**  
The LLM generates a semi-structured representation that is parsed into an abstract syntax tree,
which is then executed. The code execution step remains.

**Option C — Typed intermediate plan with deterministic compilation**  
The LLM generates a strictly typed, schema-free plan (task family, operator, metric reference,
group-by, filters, temporal grain). A family of deterministic compilers translates the plan into
bounded dataframe operations. No LLM-generated code is executed.

---

## Decision

**Adopted: Option C — Typed intermediate plan with deterministic compilation.**

---

## Rationale

### Failure mode visibility

In Option A, when the LLM misunderstands the request, the failure manifests as:
- A runtime error (easily caught)
- A wrong but syntactically valid transformation (silently incorrect — the worst failure mode)

In Option C, failure is explicitly attributed:
- LLM misunderstanding → plan critique catches structural invalidity
- Schema misreference → semantic resolver catches unbound column
- Output malformation → contract validator catches schema violation

**No failure mode is silent.** This is the central design requirement for a data engineering tool,
where incorrect transformations can propagate silently through downstream pipelines.

### Security and reproducibility

Option A requires executing LLM-generated code in a sandboxed environment. This introduces:
- Prompt injection risks (user input → code execution path)
- Non-determinism: the same request may generate different code across runs
- Auditability gap: the code is not inspectable until after execution

Option C is fully deterministic given a fixed plan and schema. The same typed plan produces
the same transformation on every run. The plan is auditable before execution.

### Evaluation decoupling

Option C separates the LLM planning capability from the compilation capability, enabling:
- **HC (Hybrid Compiler)** vs. **CO (Compiler-only)** vs. **LLM (direct code)** ablation
- Fair comparison of the LLM planning contribution
- Schema-only compilation as a deterministic baseline

This three-way comparison is the core of the ConversaBench evaluation methodology.

### Operator scope

ConversaETL targets ETL operators: aggregation, cleaning, deduplication, date wrangling,
join, reshape, insight synthesis. These operations form a bounded set. Direct code generation
is appropriate for open-ended SQL query engines (text-to-SQL). For a closed ETL operator space,
a typed plan maps directly to a finite compiler family — there is no generality benefit to
leaving the generation space open.

---

## Consequences

**Positive:**
- Deterministic, reproducible output for a given plan and schema
- All failures are attributed to a specific stage
- No code execution security surface
- Separable evaluation of planning vs. compilation
- Plan is human-readable and auditable

**Negative:**
- Unsupported operations (outside the 7 compiler families) produce explicit rejections, not graceful degradation
- Expanding operator support requires new compiler development, not just prompt updates
- The typed plan schema must be versioned and maintained

**Mitigation:**
- The plan critic surface + compiler family taxonomy defines the system boundary clearly
- Rejection records are structured — they explain what was rejected and why, enabling users to rephrase requests
- The compiler family taxonomy covers > 95% of common ETL requests in the ConversaBench test suite

---

## Alternatives Rejected

| Alternative | Rejection reason |
|---|---|
| Direct code generation (Option A) | Silent wrong-answer failure mode; security surface; non-determinism |
| LLM-to-AST with execution (Option B) | Still executes LLM-influenced code; adds parsing complexity without the reproducibility benefit |
| Text-to-SQL only | Different operator scope; SQL generation does not address ETL operators like deduplication, date bucketing, reshape |

---

## Review Trigger

This decision should be revisited if:
- A use case arises that requires open-ended code generation outside the 7 compiler families
- The compiler family expansion cost exceeds the benefit of rejection handling
- A vetted sandboxed code execution environment removes the security objection to Option A
