import pandas as pd
import sqlalchemy as sa

from alphafs.config import (
    ACCOUNT_ID,
    ACCOUNT_NM,
    CORP_CODE,
    DATA_DIR,
    FS_DB,
    IS,
    OPERATION_DIR,
    RECEPT_NO,
    SCE,
    SJ_DIV,
)
from alphafs.log import main_logger
from alphafs.messages import LOADING, PROCESS_DONE

REQUIRED_FIELDS = [
    RECEPT_NO,
    CORP_CODE,
    SJ_DIV,
    ACCOUNT_ID,
    ACCOUNT_NM,
]
data_path = f"{DATA_DIR}/{OPERATION_DIR}/{FS_DB}.db"
engine = sa.create_engine(f"sqlite:///{data_path}")


def _load_data() -> pd.DataFrame:
    df = pd.read_sql(f"SELECT * FROM {FS_DB}", engine)
    return df


def _process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[REQUIRED_FIELDS]
    df = df[(df[SJ_DIV] != SCE) & (df[SJ_DIV] != IS)]
    return df


def fetch_data() -> pd.DataFrame:
    main_logger.info(LOADING)
    df = _load_data()
    data = _process_data(df)
    main_logger.info(PROCESS_DONE)
    return data
