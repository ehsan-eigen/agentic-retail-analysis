from agentic_retail.adapters.base import Adapter
from agentic_retail.adapters.walmart import WalmartAdapter

REGISTRY: dict[str, type[Adapter]] = {
    "walmart": WalmartAdapter,
}

__all__ = ["Adapter", "WalmartAdapter", "REGISTRY"]
