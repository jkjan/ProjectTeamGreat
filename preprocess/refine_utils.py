import re

def get_lang(c):
    if ord('가') <= ord(c) <= ord('힣'):
        return 'ko'
    elif ord('a') <= ord(c.lower()) <= ord('z'):
        return 'en'
    elif ord(c) in [32, 10, 145, 134, 147, 131, 133, 137, 157, 158, 152, 139, 142, 12288, 155, 154, 156, 159, 135, 9]:
        return 'blank'
    else:
        return 'none'

def refine_str(str):
    # 괄호 제거
    str = re.sub("\(.+\)", '', str)
    # 한글, 영어만 추출
    str = re.sub("[^a-zA-Z가-힣\s]", '', str)
    ret = ""

    for c in str:
        ret += c.lower()
    return ret


def all_blank(str):
    i = 0
    limit = len(str)
    while i < limit:
        if str[i] != ' ':
            return False
        i = i + 1
    return True