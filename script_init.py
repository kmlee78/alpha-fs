import warnings

from alphafs.config import ACCOUNT_ID, ACCOUNT_NM, BS, CF, CIS, COUNTS, SJ_DIV
from alphafs.datareader import fetch_data
from alphafs.identification import (
    check_data_dir_structure,
    check_indicators_dir_structure,
)
from alphafs.parser import (
    divide_based_on_account_id_existence,
    divide_based_on_sj_div,
    FrequencyParser,
    get_essential_account_nm,
    IndicatorCreator,
)

warnings.filterwarnings("ignore")


def create_indicators(data, df_frequency):
    for sj_div in [BS, CIS, CF]:
        df_frequency_temp = divide_based_on_sj_div(df_frequency, sj_div)
        df_frequency_temp = df_frequency_temp.sort_values(by=COUNTS, ascending=False)
        df_frequency_notna, df_frequency_na = divide_based_on_account_id_existence(
            df_frequency_temp
        )
        essential_account_names = get_essential_account_nm(data, df_frequency_na)
        indicator_creator = IndicatorCreator(df_frequency_notna)
        indicator_creator.store_indicator(sj_div, essential_account_names)


def main():
    check_data_dir_structure()
    check_indicators_dir_structure()
    data = fetch_data()
    frequency = FrequencyParser(data)
    df_frequency = frequency.get_frequency(
        target=ACCOUNT_NM, depends_on=[SJ_DIV, ACCOUNT_ID]
    )
    create_indicators(data, df_frequency)


if __name__ == "__main__":
    main()
