import re
from typing import List

import numpy as np

# fmt: off
ENGS = [
    "r", "r", "rt", "s", "sw", "sg", "e", "e", "f", "fr",
    "fa", "fq", "ft", "fx", "fv", "fg", "a", "q", "q", "qt",
    "t", "t", "d", "w", "w", "c", "z", "x", "v", "g", "k",
    "o", "i", "O", "j", "p", "u", "P", "h", "hk", "ho", "hl",
    "y", "n", "nj", "np", "nl", "b", "m", "ml", "l"
]
KORS = list("ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
# fmt: on
BASE_CODE, CHO_CODE, JUNG_CODE, MAX_CODE = 44032, 588, 28, 55203
CHO_LIST = list("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ")
JUNG_LIST = list("ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
JONG_LIST = list(" ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")


KOR_ENG_TABLE = dict(zip(KORS, ENGS))
small_ENGS = list("abcdefghijklmnopqrstuvwxyz")
BIG_ENGS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
ENG_TRANS_TABLE = dict(zip(BIG_ENGS, small_ENGS))
EXTRA = list('1234567890-=~!@#$%^&*()_+[]{};",./<>?')


def _split(kor):
    code = ord(kor) - BASE_CODE
    if code < 0 or code > MAX_CODE - BASE_CODE:
        if kor == " ":
            return None
        if kor in CHO_LIST:
            return kor, " ", " "
        if kor in JUNG_LIST:
            return " ", kor, " "
        if kor in JONG_LIST:
            return " ", " ", kor
        return None
    return (
        CHO_LIST[code // CHO_CODE],
        JUNG_LIST[(code % CHO_CODE) // JUNG_CODE],
        JONG_LIST[(code % CHO_CODE) % JUNG_CODE],
    )


def transformation(text):
    result = ""
    for ch in text:
        if ch in BIG_ENGS:
            result += ENG_TRANS_TABLE[ch]
        elif ch in small_ENGS or ch in EXTRA:
            result += ch
        else:
            spl = _split(ch)
            if spl is not None:
                letter = "".join([v for v in spl if v != " "])
                for le in letter:
                    result += KOR_ENG_TABLE[le]
    return result


def lev(typed, compare):
    m = len(typed)
    n = len(compare)
    v0 = np.zeros(n + 1)
    v1 = np.zeros(n + 1)
    for i in range(n + 1):
        v0[i] = i
    for i in range(m):
        v1[0] = i + 1
        for j in range(n):
            deletionCost = v0[j + 1] + 1
            insertionCost = v1[j] + 1
            if typed[i] == compare[j]:
                substitutionCost = v0[j]
            else:
                substitutionCost = v0[j] + 1
            v1[j + 1] = min(deletionCost, insertionCost, substitutionCost)
        v0, v1 = v1, v0
    return v0[n]


def get_most_similar_words(target: str, words: List[str], limit: int = 1):
    typed = transformation(target)
    word_dict = dict()
    for word in words:
        compare = transformation(word)
        similarity = 1 - (lev(typed, compare) / (len(typed) + len(compare)))
        word_dict[word] = similarity
    similar_words = [
        i[0] for i in sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    ]
    return similar_words[:limit]


def trim_string(string: str) -> str:
    regex = r"\([^)]*\)|[^가-힣]"
    result = re.sub(regex, "", string)
    return result
