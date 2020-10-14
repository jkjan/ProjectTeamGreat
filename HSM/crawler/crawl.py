import sys
import os
from utils import *
import pandas as pd


# 데이터 열
columns = ['년도', '가수', '제목', '남녀', '장르',
           '최고순위', '작사가', '작곡가', '소속사', '가사']

# 인자 확인
try:
    name = sys.argv[1]
except IndexError:
    print("인자가 전달되지 않았습니다. 기본값(JKJ)으로 진행합니다.")
    name = "HSM"

# 경로 얻기
path = os.getcwd() + "/" + name + "/"

# 크롤링 할 아티스트 정보 가져오기
artists = get_artists(path)
recently_succeeded = 0
total_info = []

# 세이브 파일 확인
try:
    current = open("crawler/recently_succeeded.txt", "rt")
    recently_succeeded = int(current.readline())
    print("최근", artists[recently_succeeded], "데이터까지 성공한 기록이 있습니다. 이어서 진행합니다.")
    recently_succeeded += 1
    current.close()
except FileNotFoundError:
    pass

# 드라이버 초기화
init()

for i in range(recently_succeeded, len(artists)):
    songs_info = get_songs_info(artists[i])

    if songs_info is None:
        continue
    try:
        # #debugLog1 2020-10-11T08:59
        #
        # 에러가 한 번 발생 하여 recently_succeeded.txt를 이용하여 다시 시작 해야하는 경우 문제점 발생.
        # 만약 서버단에서 블락이되어 프로그램이 종료된 경우 total_info가 증발하게 됌.
        # 따라서 프로그램을 재개하게 되면 에러가 발생한 지점 이후의 songs_info들만 total_info에 저장이 됌.
        # 다만 재개 한 경우에도 각 각의 songs_info들은 순서에 맞게 csv로 저장이 정상적으로 됌.
        # 로직을 바꿔야 하지만 그렇게 되면 현재까지 크롤링한 데이터들을 다시 크롤링 해야함.
        # 그렇기에 우선 현재 폴더에 csvMerger.py를 작성하여 각각의 데이터들을 합치는 코드들 작성해 두었음.
        # 각 폴더의 songs_[name]_total.csv 파일들은 상기 코드로 우선 합쳐둔 것.
        total_info += songs_info
        df = pd.DataFrame(songs_info, columns=columns)
        df.to_csv(path + "songs_" + name + "_" + artists[i] + ".csv", index=False, encoding='utf8')
        print(artists[i], "데이터를 저장하였습니다.")
        current = open("crawler/recently_succeeded.txt", "wt")
        current.write(str(i))
        current.close()
    except Exception as e:
        print(artists[i], "데이터를 저장하는 도중 예상치 못한 오류가 발생하였습니다.")
        print(e)

# 전체 파일 저장
df = pd.DataFrame(total_info, columns=columns)
df.to_csv(path + "songs_" + name + "_total.csv", index=False, encoding='utf8')
print("전체 데이터를 저장하였습니다.")
