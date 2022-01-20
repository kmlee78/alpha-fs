import os

from alphafs.config import DATA_DIR, FS_DB, OLD_DATA_DIR, OPERATION_DIR
from alphafs.exceptions import FileDoesnotExist
from alphafs.log import main_logger
from alphafs.messages import (
    CONFIRM_DATA_DIR_PROCESS_MESSAGE,
    DATA_DIR_ERROR_MESSAGE,
    DATA_DOES_NOT_EXIST_MESSAGE,
    PROCESS_DONE,
)
from alphafs.process import confirm_continuity


def setup_data_dir_structure():
    os.mkdir(DATA_DIR)
    os.mkdir(f"{DATA_DIR}/{OPERATION_DIR}")
    os.mkdir(f"{DATA_DIR}/{OLD_DATA_DIR}")


def check_init_structure():
    current_dir_components = os.listdir()

    if DATA_DIR not in current_dir_components:
        main_logger.info(DATA_DIR_ERROR_MESSAGE)
        confirm_continuity(CONFIRM_DATA_DIR_PROCESS_MESSAGE)
        setup_data_dir_structure()
        main_logger.info(PROCESS_DONE)

    operation_dir_components = os.listdir(DATA_DIR)
    if FS_DB not in operation_dir_components:
        main_logger.warning(f"{DATA_DOES_NOT_EXIST_MESSAGE}: {FS_DB}.db")
        raise FileDoesnotExist("No data file")
