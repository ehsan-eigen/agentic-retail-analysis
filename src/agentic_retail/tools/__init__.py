from agentic_retail.tools.base import Tool, ToolResult, registry

# Import side-effect: tools register themselves on import.
from agentic_retail.tools.descriptive import summary, timeseries  # noqa: F401
from agentic_retail.tools.diagnostic import correlation  # noqa: F401
from agentic_retail.tools.predictive import sales_model  # noqa: F401
from agentic_retail.tools.prescriptive import whatif  # noqa: F401

__all__ = ["Tool", "ToolResult", "registry"]
