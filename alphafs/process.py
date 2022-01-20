from alphafs.exceptions import BreakException
from alphafs.log import system_logger


def confirm_continuity(message: str):
    confirm = input(f"{message} [y/n]")
    while confirm != "y":
        if confirm == "n":
            raise BreakException("Process down")
        else:
            system_logger.debug("Choose between 'y' and 'n'")
        confirm = input(f"{message} [y/n]")
