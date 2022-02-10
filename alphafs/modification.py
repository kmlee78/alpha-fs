import os
from typing import Dict, List

import pandas as pd

from alphafs.config import (
    ACCOUNT_ID,
    ACCOUNT_NM,
    COUNTS,
    FREQUENCY_FILE,
    HISTORY,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    MAIN,
    SYNONYM_ID,
    SYNONYM_NM,
    TEMP,
)
from alphafs.log import main_logger
from alphafs.messages import NEXT_PROCESS
from alphafs.string import get_most_similar_words, trim_string
from alphafs.system import choose_menu, confirm_continuity

MODIFICATION_TYPE = [MAIN, SYNONYM_ID, SYNONYM_NM]


def get_issue_file(sj_div: str, type: str):
    return f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{HISTORY}/{sj_div}_{type}.txt"


def load_frequency_file() -> pd.DataFrame:
    try:
        df_frequency = pd.read_csv(f"{TEMP}/{FREQUENCY_FILE}", encoding="euc-kr")
    except FileNotFoundError:
        main_logger.warning("Cache file does not exist")
        raise
    last_column = df_frequency.columns[-1]
    df_frequency = df_frequency.rename(columns={last_column: COUNTS})
    return df_frequency


def handle_existing_history(sj_div: str, type: str):
    issue_file = get_issue_file(sj_div, type)
    if os.path.isfile(issue_file):
        confirm_continuity(
            f"Modification file '{issue_file}' already exists. Do you want to update?"
        )
        os.remove(issue_file)


def save_modification_issue(inputs: str, sj_div: str, type: str):
    issue_file = get_issue_file(sj_div, type)
    with open(issue_file, mode="a") as f:
        f.write(f"{inputs}\n")


def create_main_issues(df: pd.DataFrame, indicators: Dict[str, dict], sj_div: str):
    handle_existing_history(sj_div, MAIN)
    for i, indicator in enumerate(indicators):
        df_temp = df[df[ACCOUNT_ID] == indicator]
        total = df_temp[COUNTS].sum()
        issue_str = ""
        for index in df_temp.index:
            name = df_temp.loc[index, ACCOUNT_NM]
            percentage = df_temp.loc[index, COUNTS] / total * 100
            percentage = round(percentage, 4)
            issue_str += f"{name}<|>{percentage}<|>"
        inputs = f"{i+1}<:>{sj_div}<:>{indicator}<:>{issue_str}"
        save_modification_issue(inputs, sj_div, MAIN)


def create_synonym_id_issues(indicators: Dict[str, dict], sj_div: str):
    handle_existing_history(sj_div, SYNONYM_ID)
    i = 1
    main_list = []
    for _, item in indicators.items():
        main = item[MAIN]
        issue_str = ""
        if main not in main_list:
            for account_id, item in indicators.items():
                if item[MAIN] == main:
                    issue_str += f"{account_id}<|>"
            main_list.append(main)
            inputs = f"{i}<:>{sj_div}<:>{main}<:>{issue_str}"
            save_modification_issue(inputs, sj_div, SYNONYM_ID)
            i += 1


def create_synonym_nm_issues(
    essential_list: List[str], indicators: Dict[str, dict], sj_div: str
):
    handle_existing_history(sj_div, SYNONYM_NM)
    words = [item[MAIN] for _, item in indicators.items()]
    words_trimed = [trim_string(word) for word in words]
    for i, essential in enumerate(essential_list):
        issue_str = ""
        similar_words = get_most_similar_words(essential, words_trimed, 10)
        for word in similar_words:
            issue_str += f"{word}<|>"
        inputs = f"{i+1}<:>{sj_div}<:>{essential}<:>{issue_str}"
        save_modification_issue(inputs, sj_div, SYNONYM_NM)


# TODO: how to store modified indicators and update
def create_modification_history(file_name: str, inputs: str):
    history_file = f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{HISTORY}/{file_name}.txt"
    with open(history_file, mode="a") as f:
        f.write(f"{inputs}\n")


def get_last_history_index(file_name: str) -> str:
    history_file = f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{HISTORY}/{file_name}.txt"
    last_index = ""
    try:
        with open(history_file, mode="r") as f:
            for each in f.readlines():
                last_index = each
    except FileNotFoundError:
        return "0"
    return last_index.split("<:>")[0]


def modify_main_issues(string: str, last_modified_index: str, total_count: str):
    splitted_string = string.split("<:>")
    index = splitted_string[0]
    sj_div = splitted_string[1]
    target = splitted_string[2]
    choice = splitted_string[3]
    choices = choice.split("<|>")[:-1]
    menus = {}
    if int(index) <= int(last_modified_index):
        return
    main_logger.info(f"{index}th modification issue among {total_count} issues")
    for i in range(int(len(choices) / 2)):
        menus[str(i + 1)] = f"{choices[i * 2]} -> ratio: {choices[i * 2 +1]}%"
    menus["q"] = NEXT_PROCESS

    response = choose_menu(f"Choose the main name for the account id: {target}", menus)
    if response != "q":
        new_target = menus[response].split(" -> ratio: ")[0]
        inputs = f"{index}:{target}-->{new_target}"
        file_name = f"{sj_div}_{MAIN}_{HISTORY}"
        create_modification_history(file_name, inputs)
    return response


def modify_synonym_id_issues(string, last_modified_index, total_count: str):
    splitted_string = string.split("<:>")
    index = splitted_string[0]
    sj_div = splitted_string[1]
    target = splitted_string[2]
    choice = splitted_string[3]
    choices = choice.split("<|>")[:-1]
    menus = {}
    if int(index) <= int(last_modified_index):
        return
    main_logger.info(f"{index}th modification issue among {total_count} issues")
    for i in range(len(choices)):
        menus[str(i + 1)] = choices[i]
    menus["q"] = NEXT_PROCESS

    response = choose_menu(f"Choose the account id for the main name: {target}", menus)
    if response != "q":
        new_target = menus[response]
        del choices[int(response) - 1]
        synonyms = ""
        for ch in choices:
            synonyms += f"{ch}<|>"
        inputs = f"{index}:{synonyms}-->{new_target}"
        file_name = f"{sj_div}_{SYNONYM_ID}_{HISTORY}"
        create_modification_history(file_name, inputs)
    return response


def modify_synonym_nm_issues(string, last_modified_index, total_count: str):
    splitted_string = string.split("<:>")
    index = splitted_string[0]
    sj_div = splitted_string[1]
    target = splitted_string[2]
    choice = splitted_string[3]
    choices = choice.split("<|>")[:-1]
    menus = {}
    if int(index) <= int(last_modified_index):
        return
    main_logger.info(f"{index}th modification issue among {total_count} issues")
    for i in range(len(choices)):
        menus[str(i + 1)] = choices[i]
    menus["q"] = NEXT_PROCESS

    response = choose_menu(
        f"Choose the account nm for the statement that has no account id: {target}",
        menus,
    )
    if response != "q":
        new_target = menus[response]
        inputs = f"{index}:{target}-->{new_target}"
        file_name = f"{sj_div}_{SYNONYM_NM}_{HISTORY}"
        create_modification_history(file_name, inputs)
    return response


def synchronize():
    pass
