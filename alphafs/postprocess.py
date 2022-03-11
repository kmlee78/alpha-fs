import os

from alphafs.config import DATA_DIR, HISTORY, INDICATORS_DIR, LATEST_INDICATOR


def _is_version_folder(el):
    if el.startswith("v"):
        return el
    else:
        return


def get_latest_version(directory: str) -> str:
    directory_components = os.listdir(directory)
    directory_components = list(filter(_is_version_folder, directory_components))
    version_numbers = [int(v[1:]) for v in directory_components]
    version_numbers.sort()
    version_no = version_numbers[-1]
    return "v" + str(version_no)


def name_version(directory: str) -> str:
    try:
        version = get_latest_version(directory)
        return "v" + str(int(version[1:]) + 1)
    except IndexError:
        return "v1"


def reorganize_structure():
    for dir in [INDICATORS_DIR, DATA_DIR]:
        version = name_version(dir)
        os.rename(f"{dir}/{LATEST_INDICATOR}", f"{dir}/{version}")
        os.mkdir(f"{dir}/{LATEST_INDICATOR}")
        if dir == INDICATORS_DIR:
            os.mkdir(f"{dir}/{LATEST_INDICATOR}/{HISTORY}")
