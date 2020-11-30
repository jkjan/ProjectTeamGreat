from konlpy.tag import Mecab

ko_tokenizer = Mecab().morphs

sent = "this is a test. 이것은 테스트입니다."

print(ko_tokenizer(sent))
