from alphafs.config import BS, CF, CIS
from alphafs.log import main_logger
from alphafs.messages import LOADING, PROCESS_DONE
from alphafs.modification import create_modification_issues, load_frequency_file


def main():
    main_logger.info(LOADING)
    for sj_div in [BS, CF, CIS]:
        df_frequency = load_frequency_file()
        create_modification_issues(df_frequency, sj_div)
    main_logger.info(PROCESS_DONE)


if __name__ == "__main__":
    main()
