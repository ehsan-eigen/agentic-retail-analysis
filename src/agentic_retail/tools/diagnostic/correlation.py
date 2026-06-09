"""Correlation of external signals against sales at (store, date) level."""
from __future__ import annotations

import pandas as pd

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools.base import Tool, ToolResult, registry

_EXTERNAL_NUMERIC = [
    "temperature", "fuel_price", "oil_price", "cpi", "unemployment",
    "markdown_1", "markdown_2", "markdown_3", "markdown_4", "markdown_5",
]


def _run(ds: CanonicalDataset, method: str = "pearson") -> ToolResult:
    if ds.dim_external is None:
        return ToolResult(tool="correlation", summary="No external signals available.", data=None)

    fact_agg = (
        ds.fact.groupby(["date", "store_id"], as_index=False)["sales"].sum()
    )
    merged = fact_agg.merge(ds.dim_external, on=["date", "store_id"], how="inner")
    cols = [c for c in _EXTERNAL_NUMERIC if c in merged.columns and merged[c].notna().any()]
    if not cols:
        return ToolResult(tool="correlation", summary="No usable external columns.", data=None)

    corr = merged[["sales", *cols]].corr(method=method)["sales"].drop("sales").sort_values(key=abs, ascending=False)
    summary = "Sales correlation with external signals: " + ", ".join(
        f"{k}={v:+.2f}" for k, v in corr.items()
    )
    return ToolResult(tool="correlation", summary=summary, data=corr.to_dict())


registry.register(Tool(
    name="correlation",
    category="diagnostic",
    description="Pearson/Spearman correlation of external signals against sales.",
    required_fields={"date", "store_id", "sales"},
    run=_run,
))
