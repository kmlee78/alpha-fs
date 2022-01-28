import os
from typing import Callable, Dict

from alphafs.exceptions import BreakException
from alphafs.log import system_logger
from alphafs.messages import QUIT_PROCESS


def confirm_continuity(message: str):
    confirm = input(f"{message} [y/n]")
    while confirm != "y":
        if confirm == "n":
            raise BreakException("Process down")
        else:
            system_logger.debug("Choose between 'y' and 'n'")
        confirm = input(f"{message} [y/n]")


def choose_menu(title: str, menus: Dict[str, Callable]):
    os.system("cls||clear")
    cursor = None
    menu_counts = len(menus)
    menu_content = list(menus.keys())
    valid_cursors = [str(x) for x in range(1, menu_counts + 1)]
    while cursor not in valid_cursors:
        print(title)
        for no, menu in enumerate(menu_content):
            print(f"{no + 1}. {menu}")
        system_logger.debug(QUIT_PROCESS)
        cursor = input("Select: ")
        os.system("cls||clear")
        if cursor in valid_cursors:
            menus[menu_content[int(cursor) - 1]]()
        elif cursor != "q":
            system_logger.debug("Please type valid value")
        else:
            break
