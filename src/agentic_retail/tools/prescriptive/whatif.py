"""What-if simulator on top of a trained sales model. Skeleton."""
from __future__ import annotations

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools.base import Tool, ToolResult, registry


def _run(ds: CanonicalDataset, intervention: dict | None = None) -> ToolResult:
    # TODO: load cached sales_model, apply the intervention to features
    # (e.g. promo_flag=1 for a subset, markdown_1 += X), predict, compare
    # to baseline forecast.
    raise NotImplementedError("whatif tool not yet implemented")


registry.register(Tool(
    name="whatif",
    category="prescriptive",
    description="Predict the effect of an intervention (promo, markdown, price) on sales.",
    required_fields={"date", "store_id", "sales"},
    run=_run,
))
