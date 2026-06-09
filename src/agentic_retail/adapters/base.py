from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from agentic_retail.schema import CanonicalDataset


class Adapter(ABC):
    """Map a dataset-specific directory layout into the canonical schema."""

    name: str = "base"
    grain: str = "daily"

    def __init__(self, source_dir: Path):
        self.source_dir = Path(source_dir)

    @abstractmethod
    def load(self) -> CanonicalDataset:
        ...
