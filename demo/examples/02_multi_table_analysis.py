"""
ConversaETL — Conceptual Pipeline Demo: Multi-Table Analysis
============================================================

This script illustrates how ConversaETL handles a multi-table aggregation
request that requires joining customer and order data with semantic
group_by resolution.

This is a SIMPLIFIED EDUCATIONAL ILLUSTRATION using synthetic data.
The production system's join compiler handles key resolution, cardinality
guards, post-join column validation, and contract enforcement — none of which
is exposed here.

Requirements: pandas (pip install pandas)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "sample_data"


# ---------------------------------------------------------------------------
# Typed Intermediate Representation — Multi-Table Variant
# ---------------------------------------------------------------------------

@dataclass
class MultiTableETLPlan:
    """
    Typed plan for a multi-table aggregation request.

    Illustrates the join specification that the ConversaETL planner produces.
    In production, join keys are inferred from schema relationship profiling —
    not hardcoded as they are in this illustration.
    """
    natural_language: str
    task_family: str
    primary_table: str
    join_table: str
    join_key: str              # resolved join key
    metrics: list[str]
    group_by: list[str]
    filters: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        lines = [
            "MultiTableETLPlan {",
            f"  query        : '{self.natural_language}'",
            f"  task_family  : {self.task_family}",
            f"  join         : {self.primary_table} JOIN {self.join_table}"
            f" ON {self.join_key}",
            f"  metrics      : {self.metrics}",
            f"  group_by     : {self.group_by}",
            f"  filters      : {self.filters}",
            "}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cardinality Guard (simplified illustration of join compiler safety check)
# ---------------------------------------------------------------------------

MAX_EXPANSION_RATIO = 3.0

def check_join_cardinality(
    left: pd.DataFrame, right: pd.DataFrame, key: str
) -> tuple[bool, str]:
    """
    Checks join cardinality before executing.

    In the production join compiler, this guard prevents accidental fan-out
    explosions when joining on non-unique keys. The expansion ratio ρ = |A⋈B|
    / max(|A|, |B|) must remain below a threshold.
    """
    merged_size = left.merge(right[[key]], on=key, how="left").shape[0]
    ratio = merged_size / max(len(left), len(right))
    if ratio > MAX_EXPANSION_RATIO:
        return False, f"Cardinality guard failed: expansion ratio {ratio:.2f} > {MAX_EXPANSION_RATIO}"
    return True, f"Cardinality OK (expansion ratio: {ratio:.2f})"


# ---------------------------------------------------------------------------
# Deterministic Multi-Table Compilation (simplified illustration)
# ---------------------------------------------------------------------------

def compile_multi_table(
    plan: MultiTableETLPlan,
    orders: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compiles and executes a multi-table aggregation.

    In the production system, the join compiler resolves keys from schema
    relationship profiling, enforces cardinality guards, and validates
    required columns post-join before passing to the aggregation stage.
    """
    # Apply filters on primary table
    filtered_orders = orders.copy()
    for col, val in plan.filters.items():
        if col in filtered_orders.columns:
            filtered_orders = filtered_orders[filtered_orders[col] == val]

    # Execute join
    merged = filtered_orders.merge(
        customers[["customer_id", "segment", "region"]],
        on=plan.join_key,
        how="left",
    )

    # Compute metrics
    agg_dict: dict[str, Any] = {}
    for metric in plan.metrics:
        if metric == "avg_order_value":
            agg_dict["amount"] = "mean"
        elif metric == "order_count":
            agg_dict["order_id"] = "count"
        elif metric == "refund_rate":
            pass  # computed post-aggregation

    result = (
        merged.groupby(plan.group_by)
        .agg(agg_dict)
        .reset_index()
        .rename(columns={
            "amount":   "avg_order_value",
            "order_id": "order_count",
        })
    )

    # Derived metric: refund_rate
    if "refund_rate" in plan.metrics:
        refund_counts = (
            merged[merged["status"] == "refunded"]
            .groupby(plan.group_by)["order_id"]
            .count()
            .reset_index()
            .rename(columns={"order_id": "refund_count"})
        )
        result = result.merge(refund_counts, on=plan.group_by, how="left")
        result["refund_count"] = result["refund_count"].fillna(0)
        result["refund_rate"] = (
            result["refund_count"] / result["order_count"] * 100
        ).round(1)
        result = result.drop(columns=["refund_count"])

    result["avg_order_value"] = result["avg_order_value"].round(2)
    result = result.sort_values("avg_order_value", ascending=False)
    return result


# ---------------------------------------------------------------------------
# Main Pipeline Illustration
# ---------------------------------------------------------------------------

def run_demo() -> None:
    print("=" * 65)
    print("  ConversaETL — Conceptual Pipeline Illustration")
    print("  Example: Multi-Table Analysis with Join Resolution")
    print("=" * 65)

    # Load synthetic data
    orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["order_date"])
    customers = pd.read_csv(DATA_DIR / "customers.csv")

    # ── STAGE 1: Natural Language Input ──────────────────────────────────
    nl_query = (
        "What is the average order value and refund rate "
        "per customer segment in EMEA?"
    )
    print(f"\n[STAGE 1 — INPUT]\n  Query: \"{nl_query}\"")

    # ── STAGE 1: Typed Plan ───────────────────────────────────────────────
    plan = MultiTableETLPlan(
        natural_language=nl_query,
        task_family="aggregate",
        primary_table="orders",
        join_table="customers",
        join_key="customer_id",
        metrics=["avg_order_value", "order_count", "refund_rate"],
        group_by=["segment"],
        filters={"region": "EMEA"},
    )
    print(f"\n[STAGE 1 — TYPED PLAN]\n{plan}")

    # ── STAGE 2: Join Cardinality Guard ───────────────────────────────────
    guard_ok, guard_msg = check_join_cardinality(orders, customers, "customer_id")
    print(f"\n[STAGE 2 — CARDINALITY GUARD]  {guard_msg}")
    if not guard_ok:
        print("  Pipeline halted — join guard failed.")
        return

    # ── STAGE 3: Semantic Resolution ──────────────────────────────────────
    # In this example, "segment" and "region" resolve to direct column names.
    # In the production system, the semantic resolver handles aliases and
    # cross-table column candidates.
    print("\n[STAGE 3 — SEMANTIC RESOLUTION]")
    print("  'segment' → customers.segment (direct binding)")
    print("  'region'  → orders.region     (direct binding, used as filter)")
    print("  'avg_order_value' → mean(orders.amount)")
    print("  'refund_rate'     → count(status=='refunded') / count(order_id)")

    # ── STAGE 4: Deterministic Compilation and Execution ─────────────────
    result = compile_multi_table(plan, orders, customers)
    print(f"\n[STAGE 4 — COMPILATION]  {len(result)} rows produced")

    # ── STAGE 5: Contract Validation ──────────────────────────────────────
    required = ["segment", "avg_order_value", "order_count", "refund_rate"]
    missing = [c for c in required if c not in result.columns]
    if missing:
        print(f"\n[STAGE 5 — VALIDATION]  CONTRACT FAIL — missing: {missing}")
        return
    print("\n[STAGE 5 — VALIDATION]  CONTRACT PASS — all required columns present")

    # ── Output ────────────────────────────────────────────────────────────
    print("\n[OUTPUT — Validated ETL Result]")
    print("-" * 55)
    print(result.to_string(index=False))
    print("-" * 55)
    print(
        f"\n[AUDIT TRACE]\n"
        f"  task_family : {plan.task_family}\n"
        f"  join        : {plan.primary_table} JOIN {plan.join_table} "
        f"ON {plan.join_key}\n"
        f"  metrics     : {plan.metrics}\n"
        f"  filter      : region=EMEA\n"
        f"  rows_out    : {len(result)}\n"
        f"  contract    : PASS\n"
    )
    print("=" * 65)


if __name__ == "__main__":
    run_demo()
