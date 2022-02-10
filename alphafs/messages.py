from alphafs.config import (
    DATA_DIR,
    FS_DB,
    HISTORY,
    INDICATORS_DIR,
    LATEST_INDICATOR,
    OLD_DATA_DIR,
    OPERATION_DIR,
)

PROCESS_DONE = "Process completed"
LOADING = "The process will take some time. Please wait..."
QUIT_PROCESS = "Type 'q' if you want to quit the job or go back to previous stage"
NEXT_PROCESS = "Stop modifying and jump to the next section"

DATA_DIR_ERROR_MESSAGE = f"""
Data directory structure is not standarized.
Make the directory struture as following diagram.
{DATA_DIR}/
├── {OPERATION_DIR}/
│       └── {FS_DB}.db
└── {OLD_DATA_DIR}/"""

CONFIRM_DIR_PROCESS_MESSAGE = (
    "Would you continue standarizing the directory structure automatically?"
)

DATA_DOES_NOT_EXIST_MESSAGE = "Essential db file does not exists"

INDICATORS_DIR_ERROR_MESSAGE = f"""
INDICATOR directory structure is not standarized.
Make the directory structure as following diagram.
{INDICATORS_DIR}/
└──  {LATEST_INDICATOR}/
        └──  {HISTORY}/
"""
