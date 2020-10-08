import sys
import os
from pathlib import Path
from utils import *
import pandas as pd
import time
import datetime

columns = ['년도', '가수', '제목', '남녀', '장르',
           '최고순위', '작사가', '작곡가', '소속사', '가사']

init()

try:
    name = sys.argv[1]
except IndexError:
    print("인자가 전달되지 않았습니다. 기본값(JKJ)으로 진행합니다.")
    name = "JKJ"

path = os.getcwd() + "/" + name + "/"

artists = get_artists(path)
recently_succeeded = 0

try:
    current = open("recently_succeeded.txt", "rt")
    recently_succeeded = int(current.readline())
    print("최근", artists[recently_succeeded], "데이터까지 성공한 기록이 있습니다. 이어서 진행합니다.")
    recently_succeeded += 1
    current.close()
except FileNotFoundError:
    pass

for i in range(recently_succeeded, len(artists)):
    songs_info = get_songs_info(artists[i])

    if songs_info is None:
        continue
    try:
        df = pd.DataFrame(songs_info, columns=columns)
        df.to_csv(path + "songs_" + name + "_" + artists[i] + ".csv", index=False, encoding='utf8')
        print(artists[i], "데이터를 저장하였습니다.")
        current = open("recently_succeeded.txt", "wt")
        current.write(str(i))
        current.close()

    except Exception as e:
        print(artists[i], "데이터를 저장하는 도중 예상치 못한 오류가 발생하였습니다.")
        print(e)

    # next_start = datetime.datetime.now() + datetime.timedelta(minutes=15)
    # print("15분간 휴식합니다.", next_start.strftime("%H시 %M분"), "에 재개합니다.")
