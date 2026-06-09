"""Canonical schema. All adapters emit dataframes matching these schemas."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


class FactSalesSchema(pa.DataFrameModel):
    date: Series[pd.Timestamp] = pa.Field(coerce=True)
    store_id: Series[str] = pa.Field(coerce=True)
    item_id: Series[str] = pa.Field(coerce=True, nullable=True)
    sales: Series[float] = pa.Field(coerce=True, ge=0, nullable=True)
    customers: Series[float] = pa.Field(coerce=True, ge=0, nullable=True)
    units: Series[float] = pa.Field(coerce=True, ge=0, nullable=True)
    promo_flag: Series[bool] = pa.Field(coerce=True, nullable=True)
    on_promotion_count: Series[float] = pa.Field(coerce=True, ge=0, nullable=True)
    is_open: Series[bool] = pa.Field(coerce=True, nullable=True)
    is_holiday: Series[bool] = pa.Field(coerce=True, nullable=True)

    class Config:
        strict = False
        coerce = True


class DimStoreSchema(pa.DataFrameModel):
    store_id: Series[str] = pa.Field(coerce=True, unique=True)
    store_type: Series[str] = pa.Field(coerce=True, nullable=True)
    size: Series[float] = pa.Field(coerce=True, nullable=True)
    assortment: Series[str] = pa.Field(coerce=True, nullable=True)
    cluster: Series[str] = pa.Field(coerce=True, nullable=True)
    region: Series[str] = pa.Field(coerce=True, nullable=True)
    competition_distance: Series[float] = pa.Field(coerce=True, nullable=True)

    class Config:
        strict = False
        coerce = True


class DimItemSchema(pa.DataFrameModel):
    item_id: Series[str] = pa.Field(coerce=True, unique=True)
    family: Series[str] = pa.Field(coerce=True, nullable=True)

    class Config:
        strict = False
        coerce = True


class DimExternalSchema(pa.DataFrameModel):
    """Per-(store, date) or per-(region, date) external signals."""
    date: Series[pd.Timestamp] = pa.Field(coerce=True)
    store_id: Series[str] = pa.Field(coerce=True, nullable=True)
    temperature: Series[float] = pa.Field(coerce=True, nullable=True)
    fuel_price: Series[float] = pa.Field(coerce=True, nullable=True)
    oil_price: Series[float] = pa.Field(coerce=True, nullable=True)
    cpi: Series[float] = pa.Field(coerce=True, nullable=True)
    unemployment: Series[float] = pa.Field(coerce=True, nullable=True)
    markdown_1: Series[float] = pa.Field(coerce=True, nullable=True)
    markdown_2: Series[float] = pa.Field(coerce=True, nullable=True)
    markdown_3: Series[float] = pa.Field(coerce=True, nullable=True)
    markdown_4: Series[float] = pa.Field(coerce=True, nullable=True)
    markdown_5: Series[float] = pa.Field(coerce=True, nullable=True)

    class Config:
        strict = False
        coerce = True


@dataclass
class CanonicalDataset:
    """In-memory bundle of canonical tables for a single dataset."""
    fact: pd.DataFrame
    dim_store: pd.DataFrame
    dim_item: Optional[pd.DataFrame] = None
    dim_external: Optional[pd.DataFrame] = None
    name: str = "dataset"
    grain: str = "daily"  # "daily" | "weekly"

    def available_fields(self) -> set[str]:
        """Non-null canonical fields available across tables. Tools check this."""
        fields: set[str] = set()
        for df in [self.fact, self.dim_store, self.dim_item, self.dim_external]:
            if df is None:
                continue
            for col in df.columns:
                if df[col].notna().any():
                    fields.add(col)
        return fields
