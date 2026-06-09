"""Walmart adapter: train.csv + stores.csv + features.csv -> canonical."""
from __future__ import annotations

import pandas as pd

from agentic_retail.adapters.base import Adapter
from agentic_retail.schema import CanonicalDataset
from agentic_retail.schema.canonical import (
    DimExternalSchema,
    DimStoreSchema,
    FactSalesSchema,
)


class WalmartAdapter(Adapter):
    name = "walmart"
    grain = "weekly"

    def load(self) -> CanonicalDataset:
        train = pd.read_csv(self.source_dir / "train.csv", parse_dates=["Date"])
        stores = pd.read_csv(self.source_dir / "stores.csv")
        features = pd.read_csv(self.source_dir / "features.csv", parse_dates=["Date"])

        fact = pd.DataFrame({
            "date": train["Date"],
            "store_id": train["Store"].astype(str),
            "item_id": train["Dept"].astype(str),
            "sales": train["Weekly_Sales"].astype(float),
            "is_holiday": train["IsHoliday"].astype(bool),
        })

        dim_store = pd.DataFrame({
            "store_id": stores["Store"].astype(str),
            "store_type": stores["Type"].astype(str),
            "size": stores["Size"].astype(float),
        })

        dim_external = pd.DataFrame({
            "date": features["Date"],
            "store_id": features["Store"].astype(str),
            "temperature": features["Temperature"],
            "fuel_price": features["Fuel_Price"],
            "cpi": features["CPI"],
            "unemployment": features["Unemployment"],
            "markdown_1": features.get("MarkDown1"),
            "markdown_2": features.get("MarkDown2"),
            "markdown_3": features.get("MarkDown3"),
            "markdown_4": features.get("MarkDown4"),
            "markdown_5": features.get("MarkDown5"),
        })

        fact = FactSalesSchema.validate(fact, lazy=True)
        dim_store = DimStoreSchema.validate(dim_store, lazy=True)
        dim_external = DimExternalSchema.validate(dim_external, lazy=True)

        return CanonicalDataset(
            fact=fact,
            dim_store=dim_store,
            dim_external=dim_external,
            name=self.name,
            grain=self.grain,
        )
