import pandas as pd
import re
from refine_utils import get_lang, refine_str, all_blank

df = pd.read_csv("../data/1992_2020 아이돌 음악/total_data.tsv", sep='\t')

refined = []

for i in range(len(df)):
    try:
        lyrics = df['가사'][i]

        # 한자, 히라가나, 가타카나 있을 시 정규식 과정 생략
        jp_cn = re.findall("[ぁ-ゔァ-ヴー々〆〤一-龥]", lyrics)
        if len(jp_cn) != 0:
            continue

        # 한글 하나도 없을 시 정규식 과정 생략
        ko_list = re.findall("[가-힣]", lyrics)
        if len(ko_list) == 0:
            continue

        refined_lyrics = ""
        for index, c in enumerate(lyrics):
            c = c.lower()
            lang = get_lang(c)

            # 특수문자는 무시
            if lang == 'none':
                continue
            # 공백인 유니코드들 모두 하나로 통일
            elif lang == 'blank':
                c = ' '
            # 앞뒤 글자 언어 다를 시 공백 삽입
            elif lang in ['ko', 'en']:
                if len(refined_lyrics) > 0:
                    former = get_lang(refined_lyrics[-1])
                    if former != 'blank' and former != lang:
                        refined_lyrics += ' '

            refined_lyrics += c

        # 제목, 장르 정제
        title = df['제목'][i]
        genre = df['장르'][i]
        refined_title = refine_str(title)
        refined_genre = refine_str(genre)

        # 제목, 장르, 가사 모두 공백이 아닐 경우 데이터에 추가
        if not all_blank(refined_title) and not all_blank(refined_genre) and not all_blank(refined_lyrics) != 0:
            refined.append((refined_title, refined_genre, refined_lyrics))

    except TypeError as e:
        print(e)
        print(df.iloc[i])


# 정제된 데이터 저장
columns = ['제목', '장르', '가사']
refined_df = pd.DataFrame(refined, columns=columns)
refined_df.to_csv("../data/refined_data.tsv", sep='\t', index=False, encoding='utf8')
