from typing import List, Tuple, Union

import pandas as pd

from alphafs.config import ACCOUNT_ID, NULL, SJ_DIV, TEMP


class DataSeparator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def divide_based_on_sj_div(self, sj_div: str):
        return self.df[self.df[SJ_DIV] == sj_div]

    def divide_based_on_account_id_existence(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_notna = self.df[self.df[ACCOUNT_ID] != NULL]
        df_na = self.df[self.df[ACCOUNT_ID] == NULL]
        return df_notna, df_na


class FrequencyParser:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _convert_by_caching(self, df: pd.Series, file_name: str) -> pd.DataFrame:
        file_path = f"{TEMP}/{file_name}"
        df.to_csv(file_path, encoding="euc-kr")
        df = pd.read_csv(file_path, encoding="euc-kr")
        return df

    def get_frequency(
        self, target: str, depends_on: Union[List[str], str]
    ) -> pd.DataFrame:
        """Get counts of 'target' field based on 'depends_on' fields.
        If the type of parameter 'depends_on' is list, counts of the
        'target' field would be referred to every element-element key
        in 'depends_on' list."""
        dependency = [depends_on] if isinstance(depends_on, str) else depends_on
        target_counts = (
            self.df[dependency + [target]].groupby(dependency)[target].value_counts()
        )
        df = self._convert_by_caching(target_counts, "id_cache.csv")
        df = df.rename(columns={f"{target}.1": "counts"})
        return df
