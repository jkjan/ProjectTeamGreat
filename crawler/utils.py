import requests
from bs4 import BeautifulSoup
import sys
import os
from pathlib import Path
import urllib.request
import urllib.parse


def get_artists():
    open_file = "toFind.txt"
    try:
        name = sys.argv[1]
        print("인자가 전달되지 않았습니다.")
    except IndexError:
        name = "JKJ"

    path = str(Path(os.getcwd()).parent) + "/" + \
        name + "/" + \
        open_file

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


# url 에서 수프 가져오기
def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    try:
        req = urllib.request.Request(url, headers=headers)
        f = urllib.request.urlopen(req)
        html = f.read().decode('utf8')
        return BeautifulSoup(html, 'html5lib')
    except requests.exceptions.ConnectionError as e:
        print("인터넷 연결을 확인하시길 바랍니다.")
        print(e)
        exit(0)


# 아티스트 명에서 괄호 제거
def delete_bracket(artist):
    artist = artist.split("(")
    return artist[0]


# 곡 리스트 얻어오기
def get_songs_list(id):
    start_index = 1
    while True:
        print(start_index)
        url = "https://www.melon.com/artist/song.htm?" \
              "artistId=" + id + "#params%5BlistType%5D=A&params%5BorderBy%5D=ISSUE_DATE&params%5B" \
              "artistId%5D=" + id + "&po=pageObj&startIndex=" + str(start_index)

        print(url)
        soup = get_soup(url)
        list_tags = soup.find_all('a', {'class': 'btn btn_icon_detail'})
        if len(list_tags) == 0:
            break
        for tag in list_tags:
            song_id = tag.get('href').split("'")[-2]
            title = tag.find("span").text
            print(song_id, title)
        start_index += 50
