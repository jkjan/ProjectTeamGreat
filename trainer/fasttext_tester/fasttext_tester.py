import fasttext
from gensim import models

model = models.fasttext.load_facebook_model('./fastText/cc.en.300.bin')
for w, sim in model.similar_by_word('python', 10):
    print(f'{w}: {sim}')
# en_model = fasttext.load_model('./fastText/cc.en.300.bin')
# print(en_model.get_word_vector('python'))
#
# ko_model = fasttext.load_model('./fastText/cc.ko.300.bin')
# print(ko_model.get_word_vector('파이썬'))

