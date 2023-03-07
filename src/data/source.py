from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from ..data.loader import DataSchema
from .loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(self,
               years: Optional[list[str]],
               months: Optional[list[str]],
               fleets: Optional[list[str]],
               start_date: str,
               end_date: str,
               ) -> DataSource:

        if years is None:
            years = self.unique_years
        if months is None:
            months = self.unique_months
        if fleets is None:
            fleets = self.unique_fleets

        date_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
        pd_date_range = pd.DataFrame(date_range, columns=[DataSchema])
        pd_date_range[DataSchema.OM] = 0

        filtered_data = self._data.query(
            'date in @date_range and '
            'year in @years and '
            'month in @months and '
            'fleet in @fleets')
        return DataSource(filtered_data)

    def fleet_pivot_table(self) -> pd.DataFrame:
        pt = self.pivot_table(
            values=DataSchema.OM,
            index=[DataSchema.FLEET],
            aggfunc='count',
        )
        return pt.reset_index().sort_values(DataSchema.OM, ascending=False)

    def system_pivot_table(self) -> pd.DataFrame:
        pt = self.pivot_table(
            values=DataSchema.OM,
            index=[DataSchema.SYSTEM],
            aggfunc='count',
        )
        return pt.reset_index().sort_values(DataSchema.OM, ascending=False)

    def line_chart_pivot_table(self) -> pd.DataFrame:
        pt = self.pivot_table(values=DataSchema.OM, index=DataSchema.DATE, aggfunc='count').reset_index()
        return pd.concat([pt, pd_date_range], axis=0).drop_duplicates(subset=DataSchema.DATE, keep='first').sort_values(
            by=DataSchema.DATE)

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.YEAR].tolist()

    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.MONTH].tolist()

    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def all_fleets(self) -> list[str]:
        return self._data[DataSchema.FLEET].tolist()

    @property
    def unique_fleets(self) -> list[str]:
        return sorted(set(self.all_fleets))

    @property
    def all_dates(self) -> list[str]:
        return self._data[DataSchema.DATE].tolist()

    @property
    def unique_dates(self) -> list[str]:
        return sorted(set(self.all_dates), key=str)

    # @property
    # def date_range(self):
    #     return [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    #
    # @property
    # def pd_date_range(self) -> pd.DataFrame:
    #     pd_date_range = pd.DataFrame(self.date_range, columns=[DataSchema])
    #     pd_date_range[DataSchema.OM] = 0
    #     return pd_date_range
