from alphafs.config import DATA_DIR, FS_DB, OLD_DATA_DIR, OPERATION_DIR

PROCESS_DONE = "Process completed"
LOADING = "The process will take some time. Please wait..."

DATA_DIR_ERROR_MESSAGE = f"""Data directory structure is not standarized.
Make the directory struture as following diagram.
{DATA_DIR}/
├── {OPERATION_DIR}/
│       └── {FS_DB}.db
└── {OLD_DATA_DIR}/"""

CONFIRM_DATA_DIR_PROCESS_MESSAGE = (
    "Would you continue standarizing the directory structure automatically?"
)

DATA_DOES_NOT_EXIST_MESSAGE = "Essential db file does not exists"
