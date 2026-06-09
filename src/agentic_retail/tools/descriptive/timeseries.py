"""Sales aggregated over time, optionally grouped by store/item."""
from __future__ import annotations

import pandas as pd

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools.base import Tool, ToolResult, registry


def _run(
    ds: CanonicalDataset,
    freq: str = "W",
    group_by: str | None = None,
    top_n: int = 5,
) -> ToolResult:
    f = ds.fact.copy()
    f["date"] = pd.to_datetime(f["date"])
    if group_by and group_by in f.columns:
        ts = (
            f.groupby([pd.Grouper(key="date", freq=freq), group_by])["sales"]
            .sum()
            .reset_index()
        )
        leaders = (
            ts.groupby(group_by)["sales"].sum().nlargest(top_n).index.tolist()
        )
        ts = ts[ts[group_by].isin(leaders)]
        summary = f"Sales by {group_by} (top {top_n}) at freq={freq}, {ts['date'].nunique()} periods"
    else:
        ts = f.groupby(pd.Grouper(key="date", freq=freq))["sales"].sum().reset_index()
        summary = f"Total sales at freq={freq}, {len(ts)} periods, peak {ts['sales'].max():,.0f}"
    return ToolResult(tool="timeseries", summary=summary, data=ts)


registry.register(Tool(
    name="timeseries",
    category="descriptive",
    description="Aggregate sales over time, optionally grouped (store_id, item_id).",
    required_fields={"date", "sales"},
    run=_run,
))
