from datetime import datetime
import pandas as pd


class Dataset:
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)
        self.df['rep_date'] = pd.to_datetime(self.df['rep_date'])

        # TODO: readonly
        self.source_types = self.df['source'].unique().tolist()
        self.fuel_types = self.df['fuel'].unique().tolist()
        self.min_date: datetime = self.df['rep_date'].min()
        self.max_date: datetime = self.df['rep_date'].max()
    

    def filter(self, *,
               min_date: datetime | None = None,
               max_date: datetime | None = None,
               sources: list[str] | None = None,
               fuels: list[str] | None = None
    ):
        df = self.df
        if min_date is not None:
            df = df[df['rep_date'] >= min_date]
        if max_date is not None:
            df = df[df['rep_date'] <= max_date]
        if sources is not None:
            df = df[df['source'].isin(sources)]
        if fuels is not None:
            df = df[df['fuel'].isin(fuels)]
        return df
