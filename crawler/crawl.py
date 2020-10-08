import sys
import os
from pathlib import Path
from utils import *
import pandas as pd

columns = ['년도', '가수', '제목', '남녀', '장르',
           '최고순위', '작사가', '작곡가', '소속사', '가사']

init()

try:
    name = sys.argv[1]
    print("인자가 전달되지 않았습니다.")
except IndexError:
    name = "JKJ"

path = str(Path(os.getcwd()).parent) + "/" + \
       name + "/"

artists = get_artists(path)
total_info = []

for artist in artists:
    songs_info = get_songs_info(artist)
    if songs_info is not None:
        total_info += songs_info

df = pd.DataFrame(total_info, columns=columns)
df.to_csv(path + "songs_" + name + ".csv", index=False, encoding='utf8')