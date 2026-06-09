# agentic-retail-analysis

An autonomous AI agent framework for multi-step retail data analysis,
inventory forecasting, and conversational business intelligence.

Maps arbitrary retail data to a canonical schema, then answers descriptive /
diagnostic / predictive / prescriptive questions via a tool-based agent.

## Layout

```
src/agentic_retail/
  schema/        canonical fact + dim schemas (pandera)
  adapters/      dataset-specific mappers → canonical (walmart implemented)
  ingest/        load adapter, validate, persist as parquet
  tools/         analytical capabilities, registered + schema-aware
    descriptive/    summary, timeseries
    diagnostic/     correlation
    predictive/     sales_model (stub)
    prescriptive/   whatif       (stub)
  agents/        router (keyword now, LLM later)
  api/           cli entrypoint
```

## Quickstart (Walmart)

Put `train.csv`, `stores.csv`, `features.csv` in `data/walmart/`, then:

```bash
pip install -e .
retail ingest --source data/walmart --adapter walmart --out artifacts/walmart
retail tools  --data artifacts/walmart
retail ask    --data artifacts/walmart "what's the total sales trend over time?"
retail ask    --data artifacts/walmart "why do sales change — any correlations?"
```

## Design

- **Canonical schema is the contract.** Every adapter emits `fact_sales` +
  dimension tables matching `schema/canonical.py`. Tools never see raw
  columns.
- **Tools declare `required_fields`.** Router only offers tools whose inputs
  exist in the loaded dataset, so the same agent degrades gracefully across
  datasets with different columns.
- **LLM is out of the hot path.** Query-time work is deterministic Python;
  the router is keyword-based for now and will become an LLM call later.
  Auto-ingest (LLM-mapped adapters) is a planned next step.
