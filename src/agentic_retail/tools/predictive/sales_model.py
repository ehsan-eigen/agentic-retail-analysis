"""Gradient-boosted sales model + feature importance. Skeleton."""
from __future__ import annotations

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools.base import Tool, ToolResult, registry


def _run(ds: CanonicalDataset, target: str = "sales") -> ToolResult:
    # TODO: build feature matrix from fact + dims + calendar features,
    # train LightGBM with time-based CV, return feature importances,
    # cache model artifact under artifacts/{ds.name}/sales_model.pkl.
    raise NotImplementedError("sales_model tool not yet implemented")


registry.register(Tool(
    name="sales_model",
    category="predictive",
    description="Train a gradient-boosted sales model and return feature importances.",
    required_fields={"date", "store_id", "sales"},
    run=_run,
))
