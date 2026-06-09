"""Run an adapter, validate, persist canonical tables as parquet."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from agentic_retail.adapters import REGISTRY
from agentic_retail.schema import CanonicalDataset

TABLES = ["fact", "dim_store", "dim_item", "dim_external"]


def ingest(source_dir: Path, adapter_name: str, out_dir: Path) -> CanonicalDataset:
    if adapter_name not in REGISTRY:
        raise ValueError(f"Unknown adapter '{adapter_name}'. Known: {list(REGISTRY)}")
    adapter = REGISTRY[adapter_name](source_dir)
    ds = adapter.load()

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in TABLES:
        df = getattr(ds, name)
        if df is not None:
            df.to_parquet(out_dir / f"{name}.parquet", index=False)
    (out_dir / "meta.txt").write_text(f"name={ds.name}\ngrain={ds.grain}\n")
    return ds


def load_canonical(out_dir: Path) -> CanonicalDataset:
    out_dir = Path(out_dir)
    meta = dict(
        line.split("=", 1) for line in (out_dir / "meta.txt").read_text().splitlines() if line
    )

    def _read(name: str) -> pd.DataFrame | None:
        p = out_dir / f"{name}.parquet"
        return pd.read_parquet(p) if p.exists() else None

    return CanonicalDataset(
        fact=_read("fact"),
        dim_store=_read("dim_store"),
        dim_item=_read("dim_item"),
        dim_external=_read("dim_external"),
        name=meta.get("name", "dataset"),
        grain=meta.get("grain", "daily"),
    )
