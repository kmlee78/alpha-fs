from alphafs.config import (
    BS,
    CF,
    CIS,
    ESSENTIAL_LIST,
    HISTORY,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    MAIN,
    SJ_DIV,
    SYNONYM_ID,
    SYNONYM_NM,
)
from alphafs.datareader import IndicatorReader
from alphafs.modification import (
    create_main_issues,
    create_synonym_id_issues,
    create_synonym_nm_issues,
    get_issue_file,
    get_last_history_index,
    load_frequency_file,
    modify_main_issues,
    modify_synonym_id_issues,
    modify_synonym_nm_issues,
    synchronize,
)
from alphafs.system import confirm_continuity


def modify_issues(sj_div: str, type: str):
    modification_case = {
        MAIN: modify_main_issues,
        SYNONYM_ID: modify_synonym_id_issues,
        SYNONYM_NM: modify_synonym_nm_issues,
    }
    last_modified_index = get_last_history_index(f"{sj_div}_{type}_{HISTORY}").split(
        ":"
    )[0]
    total_count = get_last_history_index(f"{sj_div}_{type}")
    issue_file = get_issue_file(sj_div, type)
    with open(issue_file, mode="r") as f:
        for each in f.readlines():
            response = modification_case[type](each, last_modified_index, total_count)
            if response == "q":
                break


def main():
    df_frequency = load_frequency_file()
    for sj_div in [BS, CF, CIS]:
        df = df_frequency[df_frequency[SJ_DIV] == sj_div]
        indicators = IndicatorReader(
            f"{INDICATORS_DIR}/{LATEST_INDICATOR}/{sj_div}.json"
        ).read_indicator()
        essential_list = indicators[ESSENTIAL_LIST]
        del indicators[ESSENTIAL_LIST]

        create_main_issues(df, indicators, sj_div)
        modify_issues(sj_div, MAIN)
        create_synonym_id_issues(indicators, sj_div)
        modify_issues(sj_div, SYNONYM_ID)
        create_synonym_nm_issues(essential_list, indicators, sj_div)
        modify_issues(sj_div, SYNONYM_NM)

        confirm_continuity(f"Continue updating {sj_div} indicators?")
        synchronize(sj_div)


if __name__ == "__main__":
    main()
