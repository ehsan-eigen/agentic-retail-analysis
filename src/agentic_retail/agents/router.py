"""Question → tool router. Skeleton: keyword routing now, LLM later."""
from __future__ import annotations

from dataclasses import dataclass

from agentic_retail.schema import CanonicalDataset
from agentic_retail.tools import registry
from agentic_retail.tools.base import Tool


@dataclass
class RoutingDecision:
    category: str
    tool: Tool
    rationale: str


_KEYWORDS = {
    "descriptive": ["summary", "overview", "how many", "total", "trend", "over time", "by store", "by dept"],
    "diagnostic":  ["why", "correlat", "driver", "explain", "associat"],
    "predictive":  ["predict", "forecast", "next week", "next month", "importance", "feature"],
    "prescriptive": ["what if", "should", "recommend", "optimi", "increase", "decrease"],
}


def _classify(question: str) -> str:
    q = question.lower()
    for cat, kws in _KEYWORDS.items():
        if any(k in q for k in kws):
            return cat
    return "descriptive"


class Router:
    """Pick a tool for a question. Stub for an LLM-based router."""

    def route(self, question: str, ds: CanonicalDataset) -> RoutingDecision:
        category = _classify(question)
        candidates = registry.applicable(ds, category=category)
        if not candidates:
            candidates = registry.applicable(ds, category="descriptive")
            category = "descriptive"
        tool = candidates[0]  # TODO: rank by relevance via LLM
        return RoutingDecision(
            category=category,
            tool=tool,
            rationale=f"keyword-matched category={category}, picked tool={tool.name}",
        )
