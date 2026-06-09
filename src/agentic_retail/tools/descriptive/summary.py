"""High-level dataset summary: row count, date range, stores, total/avg sales."""
from __future__ import annotations

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools.base import Tool, ToolResult, registry


def _run(ds: CanonicalDataset) -> ToolResult:
    f = ds.fact
    data = {
        "rows": int(len(f)),
        "date_min": str(f["date"].min().date()),
        "date_max": str(f["date"].max().date()),
        "n_stores": int(f["store_id"].nunique()),
        "n_items": int(f["item_id"].nunique()) if f["item_id"].notna().any() else 0,
        "sales_total": float(f["sales"].sum()),
        "sales_mean": float(f["sales"].mean()),
        "sales_median": float(f["sales"].median()),
    }
    summary = (
        f"{data['rows']:,} rows | {data['date_min']} → {data['date_max']} | "
        f"{data['n_stores']} stores | total sales {data['sales_total']:,.0f} | "
        f"mean {data['sales_mean']:,.2f}"
    )
    return ToolResult(tool="summary", summary=summary, data=data)


registry.register(Tool(
    name="summary",
    category="descriptive",
    description="High-level dataset summary: row count, date range, totals.",
    required_fields={"date", "store_id", "sales"},
    run=_run,
))
