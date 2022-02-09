from typing import Dict

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


def choose_menu(title: str, menus: Dict[str, str]):
    cursor = ""
    valid_cursors = menus.keys()
    while cursor not in valid_cursors:
        print(title)
        for index in menus:
            print(f"{index}. {menus[index]}")
        cursor = input("Select: ")
        if cursor in valid_cursors:
            return cursor
        else:
            system_logger.debug("Please type valid value")
