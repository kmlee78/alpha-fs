import pandas as pd
import sqlalchemy as sa

from alphafs.config import DATA_DIR, FS_DB, OPERATION_DIR
from alphafs.log import main_logger
from alphafs.messages import LOADING, PROCESS_DONE

REQUIRED_FIELDS = ["rcept_no", "corp_code", "sj_div", "account_id", "account_nm"]


class DataBaseReader:
    def __init__(self):
        self.data_path = f"{DATA_DIR}/{OPERATION_DIR}/{FS_DB}.db"

    def read_database(self) -> pd.DataFrame:
        engine = sa.create_engine(f"sqlite:///{self.data_path}")
        df = pd.read_sql(f"SELECT * FROM {FS_DB}", engine)
        return df


class DataProvider:
    def __init__(self):
        self.datareader = DataBaseReader()

    def load_data(self) -> pd.DataFrame:
        main_logger.info(LOADING)
        df = self.datareader.read_database()
        main_logger.info(PROCESS_DONE)
        return df

    def fetch_data(self) -> pd.DataFrame:
        df = self.load_data()
        data = df[REQUIRED_FIELDS]
        return data
