from typing import Dict, List

import pandas as pd

from alphafs.config import (
    ACCOUNT_ID,
    ACCOUNT_NM,
    BS,
    CF,
    CIS,
    COUNTS,
    ESSENTIAL_LIST,
    FREQUENCY_FILE,
    HISTORY,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    MAIN,
    SJ_DIV,
    SYNONYM_ID,
    SYNONYM_NM,
    TEMP,
)
from alphafs.datareader import IndicatorReader
from alphafs.log import main_logger
from alphafs.string import get_most_similar_words, trim_string


def load_frequency_file() -> pd.DataFrame:
    try:
        df_frequency = pd.read_csv(f"{TEMP}/{FREQUENCY_FILE}", encoding="euc-kr")
    except FileNotFoundError:
        main_logger.warning("Cache file does not exist")
        raise
    last_column = df_frequency.columns[-1]
    df_frequency = df_frequency.rename(columns={last_column: COUNTS})
    return df_frequency


def save_modification_issue(inputs: str, sj_div: str, type: str):
    with open(
        f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{HISTORY}/{sj_div}_{type}.txt", mode="a"
    ) as f:
        f.write(f"{inputs}\n")


def create_main_issues(df: pd.DataFrame, indicators: Dict[str, dict], sj_div: str):
    for i, indicator in enumerate(indicators):
        df_temp = df[df[ACCOUNT_ID] == indicator]
        total = df_temp[COUNTS].sum()
        issue_str = ""
        for index in df_temp.index:
            name = df_temp.loc[index, ACCOUNT_NM]
            percentage = df_temp.loc[index, COUNTS] / total * 100
            percentage = round(percentage, 2)
            issue_str += f"{name}|{percentage}|"
        inputs = f"{i+1}:{sj_div}:{indicator}:{issue_str}"
        save_modification_issue(inputs, sj_div, MAIN)


def create_synonym_id_issues(indicators: Dict[str, dict], sj_div: str):
    i = 1
    main_list = []
    for _, item in indicators.items():
        main = item[MAIN]
        issue_str = main
        if main not in main_list:
            for account_id, item in indicators.items():
                if item[MAIN] == main:
                    issue_str += f"|{account_id}"
            main_list.append(main)
            inputs = f"{i}:{sj_div}:{issue_str}"
            save_modification_issue(inputs, sj_div, SYNONYM_ID)
            i += 1


def create_synonym_nm_issues(
    essential_list: List[str], indicators: Dict[str, dict], sj_div: str
):
    words = [item[MAIN] for _, item in indicators.items()]
    words_trimed = [trim_string(word) for word in words]
    for i, essential in enumerate(essential_list):
        issue_str = essential
        similar_words = get_most_similar_words(essential, words_trimed, 10)
        for word in similar_words:
            issue_str += f"|{word}"
        inputs = f"{i+1}:{sj_div}:{issue_str}"
        save_modification_issue(inputs, sj_div, SYNONYM_NM)


def create_modification_issues(df_frequency: pd.DataFrame, sj_div: str):
    if sj_div not in [BS, CIS, CF]:
        raise ValueError("Invalid value")
    df = df_frequency[df_frequency[SJ_DIV] == sj_div]
    indicators = IndicatorReader(
        f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{sj_div}.json"
    ).read_indicator()
    essential_list = indicators[ESSENTIAL_LIST]
    del indicators[ESSENTIAL_LIST]

    create_main_issues(df, indicators, sj_div)
    create_synonym_id_issues(indicators, sj_div)
    create_synonym_nm_issues(essential_list, indicators, sj_div)


# TODO: how to store modified indicators and update
def create_modification_history(indicators: Dict[str, str]):
    pass


def read_modification_history():
    pass


def synchronize():
    pass
