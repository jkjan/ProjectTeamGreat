import csv
import sys
import os
import pandas as pd
from utils import *

columns = ['년도', '가수', '제목', '남녀', '장르',
           '최고순위', '작사가', '작곡가', '소속사', '가사']

try:
    name = sys.argv[1]
except IndexError:
    print("인자가 전달되지 않았습니다. 기본값(JKJ)으로 진행합니다.")
    name = "JKJ"

path = os.getcwd() + "/" + name + "/"

# artists = get_artists(path)
artists = ["total_HSM", "total_KEH", "total_JKJ", "total_YJS"]
total_info = []

for x in range(len(artists)):
    tempList = []
    try:
        #with open(os.path.join(name, artists[x] + '.csv'), 'r', encoding='utf8') as csvfile:
    	with open(os.path.join(name,  artists[x] + '.csv'), 'r') as csvfile:
    		rdr = csv.reader(csvfile)
    		i = 0
    		for row in rdr:
        		if (i != 0):
        			tempList.append(row)
        		i += 1
    except FileNotFoundError:
    	print(artists[x] + '항목을 찾을 수 없었습니다.')
    	continue
    total_info += tempList

df = pd.DataFrame(total_info, columns=columns)
df.to_csv(path + "songs_" + name + "_total.csv", index=False, encoding='utf8')
print("전체 데이터를 저장하였습니다.")
