import json
from typing import Dict, List, Tuple, Union

import pandas as pd

from alphafs.config import (
    ACCOUNT_ID,
    ACCOUNT_NM,
    COUNTS,
    ESSENTIAL_LIST,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    MAIN,
    NULL,
    RECEPT_NO,
    SJ_DIV,
    SYNONYM_ID,
    SYNONYM_NM,
    TEMP,
)


def get_essential_account_nm(
    df_original: pd.DataFrame, df: pd.DataFrame, percentage: int = 1
) -> List[str]:
    """
    Parameter 'df_original' is the originally fetched data, whereas 'df' is
    the data which is the result of frequeny parser and the function 'divide_
    based_on_account_id_existence'. It should only contain user-selected fields
    and they should not have any account ids.
    The result depends on percentage we passed. If we pass the value 30 to the
    percentage parameter, The essectial account name list will include account
    name that appears for more than 30 percentages of the number of ovaerall
    reports.
    """
    if percentage < 0 or percentage > 100:
        raise ValueError("Percentage should be between 0 and 100")
    overall_reports = df_original[RECEPT_NO].unique().shape[0]
    number_of_reports = overall_reports * percentage / 100
    essential_account_nm = (
        df[df["counts"] > number_of_reports][ACCOUNT_NM].unique().tolist()
    )
    return essential_account_nm


def divide_based_on_sj_div(df: pd.DataFrame, sj_div: str):
    return df[df[SJ_DIV] == sj_div]


def divide_based_on_account_id_existence(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_notna = df[df[ACCOUNT_ID] != NULL]
    df_na = df[df[ACCOUNT_ID] == NULL]
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
        """
        Get counts of 'target' field based on 'depends_on' fields.
        If the type of parameter 'depends_on' is list, counts of the
        'target' field would be referred to every element-element key
        in 'depends_on' list.
        """
        dependency = [depends_on] if isinstance(depends_on, str) else depends_on
        target_counts = (
            self.df[dependency + [target]].groupby(dependency)[target].value_counts()
        )
        df = self._convert_by_caching(target_counts, "id_cache.csv")
        df = df.rename(columns={f"{target}.1": COUNTS})
        return df


class IndicatorCreator:
    """
    Indicators should be made from frequency data that has only one type
    of value in sj_div column. So execute 2 functions above that starts with
    'divide' before applying frequency parser. Input parameter 'df_frequency'
    should be result of 'df_notna' of the function 'divide_based_on_account
    _id_existence'.

    Form of indicator file:
        {
            "account_id1": {
                "main": ~~~,
                "synonym_id": [...],
                "synonym_nm": [...],
                "counts": ...,
            },
            "account_id2": {
                ...
            },
            ...
        }
    """

    def __init__(self, df_frequency: pd.DataFrame):
        self.df_frequency = df_frequency

    def create_indicator(self, essential_list: List[str]) -> Dict:
        account_ids = self.df_frequency[ACCOUNT_ID].unique()
        indicators: Dict[
            str, Union[List[str], Dict[str, Union[str, List[str], int]]]
        ] = dict()
        indicators[ESSENTIAL_LIST] = essential_list
        for account_id in account_ids:
            indicators[account_id] = dict()
            synonyms = self.df_frequency[self.df_frequency[ACCOUNT_ID] == account_id][
                ACCOUNT_NM
            ].to_list()
            indicators[account_id][MAIN] = synonyms[0]
            indicators[account_id][SYNONYM_ID] = list()
            indicators[account_id][SYNONYM_NM] = list()
            indicators[account_id][COUNTS] = self.df_frequency[
                self.df_frequency[ACCOUNT_ID] == account_id
            ][COUNTS].to_list()[0]
        return indicators

    def store_indicator(self, sj_div: str, essential_list: List[str]):
        indicators = self.create_indicator(essential_list)
        with open(
            f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{sj_div}.json", "w"
        ) as json_file:
            json.dump(indicators, json_file, ensure_ascii=False)
