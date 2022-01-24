import os

from alphafs.config import (
    DATA_DIR,
    FS_DB,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    OLD_DATA_DIR,
    OPERATION_DIR,
    TEMP,
)
from alphafs.exceptions import FileDoesNotExist
from alphafs.log import main_logger
from alphafs.messages import (
    CONFIRM_DIR_PROCESS_MESSAGE,
    DATA_DIR_ERROR_MESSAGE,
    DATA_DOES_NOT_EXIST_MESSAGE,
    INDICATORS_DIR_ERROR_MESSAGE,
    PROCESS_DONE,
)
from alphafs.process import confirm_continuity


def setup_data_dir_structure():
    os.mkdir * TEMP
    os.mkdir(DATA_DIR)
    os.mkdir(f"{DATA_DIR}/{OPERATION_DIR}")
    os.mkdir(f"{DATA_DIR}/{OLD_DATA_DIR}")


def setup_indicators_dir_structure():
    os.mkdir(INDICATORS_DIR)
    os.mkdir(f"{INDICATORS_DIR}/{LATEST_INDICATOR}")


def check_data_dir_structure():
    current_dir_components = os.listdir()

    if DATA_DIR not in current_dir_components:
        main_logger.info(DATA_DIR_ERROR_MESSAGE)
        confirm_continuity(CONFIRM_DIR_PROCESS_MESSAGE)
        setup_data_dir_structure()
        main_logger.info(PROCESS_DONE)

    operation_dir_components = os.listdir(f"{DATA_DIR}/{OPERATION_DIR}")
    if f"{FS_DB}.db" not in operation_dir_components:
        main_logger.warning(f"{DATA_DOES_NOT_EXIST_MESSAGE}: {FS_DB}.db")
        raise FileDoesNotExist("No data file")


def check_indicators_dir_structure():
    current_dir_components = os.listdir()

    if INDICATORS_DIR not in current_dir_components:
        main_logger.info(INDICATORS_DIR_ERROR_MESSAGE)
        confirm_continuity(CONFIRM_DIR_PROCESS_MESSAGE)
        setup_indicators_dir_structure()
        main_logger.info(PROCESS_DONE)
