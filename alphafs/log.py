import logging
import logging.config
import sys

LOGGING_CONFIG = dict(
    version=1,
    loggers={
        "alphafs": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
            "propagte": "no",
        },
        "system": {
            "level": "DEBUG",
            "handlers": ["miniconsole"],
            "propagate": "no",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "msg",
            "stream": sys.stdout,
        },
        "miniconsole": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "msg",
            "stream": sys.stdout,
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "WARNING",
            "formatter": "msg",
            "filename": "warning.log",
        },
    },
    formatters={
        "msg": {
            "class": "logging.Formatter",
            "format": "%(name)s: %(message)s",
        }
    },
)

logging.config.dictConfig(LOGGING_CONFIG)
main_logger = logging.getLogger("alphafs")
system_logger = logging.getLogger("system")
