import pandas as pd
import sqlalchemy as sa

from alphafs.config import DATA_DIR, FS_DB, OPERATION_DIR
from alphafs.log import main_logger
from alphafs.messages import LOADING, PROCESS_DONE

REQUIRED_FIELDS = ["rcept_no", "corp_code", "sj_div", "account_id", "account_nm"]


class DataReader:
    def __init__(self):
        self.data_path = f"{DATA_DIR}/{OPERATION_DIR}/{FS_DB}.db"

    def read_data(self):
        engine = sa.create_engine(f"sqlite:///{self.data_path}")
        df = pd.read_sql(f"SELECT * FROM {FS_DB}", engine)
        return df


class DataProvider:
    def __init__(self):
        datareader = DataReader()
        main_logger.info(LOADING)
        self.data = datareader.read_data()
        main_logger.info(PROCESS_DONE)

    def fetch_data(self):
        data = self.data[REQUIRED_FIELDS]
        return data
