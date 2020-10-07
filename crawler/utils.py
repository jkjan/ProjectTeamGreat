import requests
from bs4 import BeautifulSoup
import sys
import os
from pathlib import Path
import urllib.request
import urllib.parse
from seleniumrequests import Chrome
import re

webdriver = None


# 파일에서 아티스트 목록 뽑아오기
def get_artists(path):
    path += "toFind.txt"

    to_find = None
    try:
        to_find = open(path, "rt")
    except FileNotFoundError:
        print("파일이 존재하지 않습니다:", path)
        exit(1)

    artists = []
    print("다음 아티스트에 대해서 검색합니다.")

    while True:
        artist = to_find.readline()
        if len(artist) == 0:
            break
        if artist[-1] == '\n':
            artist = artist[:-1]
        artist = delete_bracket(artist)
        artists.append(artist)
        print(artist)
    print()

    return artists


# 아티스트 id 얻어오기
def get_artist_id(artist):
    artist = urllib.parse.quote_plus(artist)
    url = "https://www.melon.com/search/artist/index.htm?" \
          "q=" + artist + "&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=" \
                          "srch_form#params%5Bq%5D=" + artist + "&params%5Bsq%5D=&params%5Bsort%5D=weight&params%5Bsection%5D=all&params%5Bsex%5D=&params%5BactType%5D=&params%5Bdomestic%5D=&params%5BgenreCd%5D=" \
                                                                "&params%5BactYear%5D=2000+2010+" \
                                                                "&po=pageObj&startIndex=1"

    soup = get_soup(url)
    try:
        div = soup.select("a.thumb")[0].get('href')
        return div.split("'")[-2]
    except IndexError:
        print(artist + "에 대하여 검색된 아티스트가 없습니다.")
        return None


# url 에서 수프 가져오기
def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Connection': 'keep-alive'}

    try:
        html = requests.get(url, headers=headers).text
        return BeautifulSoup(html, 'html5lib')
    except requests.exceptions.ConnectionError as e:
        print("인터넷 연결을 확인하시길 바랍니다.")
        print(e)
        exit(0)


# 아티스트 명에서 괄호 제거
def delete_bracket(artist):
    artist = artist.split("(")
    return artist[0]

# 드라이버 초기화
def init():
    global webdriver
    driver_path = open("driver_path.txt", "rt")
    webdriver = Chrome(driver_path.readline())
    webdriver.implicitly_wait(3)


# 곡 리스트 얻어오기
def get_songs_info(artist):
    artist_id = get_artist_id(artist)
    if artist_id is None:
        return None

    start_index = 1

    artist_info = get_artist_info(artist_id)
    total_info = []

    while True:
        url = "https://www.melon.com/artist/song.htm?" \
              "artistId=" + artist_id + "#params%5BlistType%5D=A&params%5BorderBy%5D=ISSUE_DATE&params%5B" \
                                        "artistId%5D=" + artist_id + "&po=pageObj&startIndex=" + str(start_index)

        # JavaScript 처리 후 페이지 소스 받아오기 위해 selenium 사용
        webdriver.get(url)
        html = webdriver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        list_tags = soup.find_all('a', {'class': 'btn btn_icon_detail'})

        # 전곡 다 뒤졌으면 break
        if len(list_tags) == 0:
            break

        # 리스트 내 모든 곡에 대해서 아티스트 정보 + 곡 정보 합치기
        for tag in list_tags:
            song_id = tag.get('href').split("'")[-2]
            song_info = get_song_info(song_id)

            if song_info is None:
                continue

            song_info = {**artist_info, **song_info, '최고순위': '-', '가수': artist}
            # TODO : 최고순위?
            total_info.append(song_info)

        start_index += 50

    return total_info


# 아티스트 정보 얻어오기
def get_artist_info(artist_id):
    url = "https://www.melon.com/artist/detail.htm?" \
          "artistId=" + artist_id
    soup = get_soup(url)
    info_list = soup.select_one("div.section_atistinfo03 > dl")
    dts = info_list.select("dt")
    dds = info_list.select("dd")
    artist_info = {
        '남녀': '-',
        '소속사': '-'
    }

    for i in range(len(dts)):
        # 성별
        if dts[i].text == '유형':
            types = dds[i].get_text(separator='').replace(" ", "")
            types = re.sub(r"\s+", "", types).split('|')
            if '남성' in types:
                artist_info['남녀'] = 'male'
            elif '여성' in types:
                artist_info['남녀'] = 'female'
            elif '혼성' in types:
                artist_info['남녀'] = 'mixed'
            else:
                artist_info['남녀'] = '-'

        # 소속사
        elif dts[i].text == '소속사명':
            artist_info['소속사'] = dds[i].text

    return artist_info


def get_text(text):
    return text.strip().replace('\t', '')


# 곡 정보 얻어오기
def get_song_info(song_id):
    url = "https://www.melon.com/song/detail.htm?" \
          "songId=" + song_id
    soup = get_soup(url)
    song_info = {}

    # 제목
    text = soup.select_one("div.song_name").get_text(separator='\n')
    song_title = get_text(text)[2:].strip().replace('\n', '')
    song_info['제목'] = song_title

    # 발매일, 장르
    dts = soup.select("div.meta > dl > dt")
    dds = soup.select("div.meta > dl > dd")
    for i in range(len(dts)):
        if dts[i].text == '발매일':
            release_date = dds[i].text.split('.')
            release_date = ''.join(release_date)
            song_info['년도'] = release_date
            year = release_date[:4]

            # 발매일 확인
            try:
                if not 2000 <= int(year) <= 2010:
                    return None
            except ValueError:
                return None

        elif dts[i].text == '장르':
            song_info['장르'] = dds[i].text

    # 가사
    try:
        lyrics = soup.select_one("div.lyric").get_text(separator=' ')
        lyrics = get_text(lyrics)
        lyrics = lyrics.replace('\n', ' ')
        song_info['가사'] = lyrics
    except AttributeError:
        song_info['가사'] = '-'

    # 작곡/작사
    writers = soup.select("div.entry")
    for w in writers:
        try:
            contribute = w.select_one("div.meta > span").text
        except AttributeError:
            continue
        if contribute in ['작사', '작곡']:
            div = w.find("div", {'class': 'ellipsis artist'})
            name = div.select_one('a').text

            if contribute in song_info.keys():
                song_info[contribute + '가'].append(name)
            else:
                song_info[contribute + '가'] = [name]

    for contribute in ['작사가', '작곡가']:
        if contribute not in song_info.keys():
            song_info[contribute] = '-'
        else:
            song_info[contribute] = ", ".join(song_info[contribute])

    return song_info
