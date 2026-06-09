"""Tool protocol. Every analytical capability is a Tool with declared requirements."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from agentic_retail.schema import CanonicalDataset


@dataclass
class ToolResult:
    tool: str
    summary: str  # one-line human-readable result, for the agent layer
    data: Any = None  # structured payload (df, dict, etc.)
    artifacts: dict[str, str] = field(default_factory=dict)  # paths to saved outputs


@dataclass
class Tool:
    name: str
    category: str  # "descriptive" | "diagnostic" | "predictive" | "prescriptive"
    description: str
    required_fields: set[str]  # canonical field names this tool needs
    run: Callable[..., ToolResult]

    def is_applicable(self, ds: CanonicalDataset) -> bool:
        return self.required_fields.issubset(ds.available_fields())


class _Registry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> Tool:
        self._tools[tool.name] = tool
        return tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def all(self) -> list[Tool]:
        return list(self._tools.values())

    def applicable(self, ds: CanonicalDataset, category: str | None = None) -> list[Tool]:
        out = [t for t in self._tools.values() if t.is_applicable(ds)]
        if category:
            out = [t for t in out if t.category == category]
        return out


registry = _Registry()
