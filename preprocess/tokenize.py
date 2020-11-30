from konlpy.tag import Mecab
import pandas as pd
from random import shuffle
import pickle
from gensim.models import Word2Vec

tokenizer = Mecab().morphs
word_count = {}

df = pd.read_csv("../data/refined_data.tsv", sep='\t')
data = {}

data_before_shuffle = []
sentences = []
unique_words = set()

for i in range(len(df)):
    tokenized_title = tokenizer(df['제목'][i])
    tokenized_genre = tokenizer(df['장르'][i])
    tokenized_lyrics = tokenizer(df['가사'][i])

    data_before_shuffle.append((tokenized_title, tokenized_genre, tokenized_lyrics))
    words = tokenized_title + tokenized_genre + tokenized_lyrics

    for word in words:
        unique_words.add(word)

shuffle(data_before_shuffle)

data_size = len(data_before_shuffle)
train_size = int(0.7 * data_size)
test_size = data_size - train_size

data['train'] = data_before_shuffle[:train_size]
data['test'] = data_before_shuffle[train_size:]

pickle.dump(data, open("../data/tokenized_data.pkl", 'wb'))
pickle.dump(sentences, open("../data/sentences.pkl", 'wb'))
pickle.dump(unique_words, open("../data/unique_words.pkl", 'wb'))

try:
    model = Word2Vec.load('../data/embedded.w2v')
    print("embedded file exists:")
except FileNotFoundError:
    print("embedded file does not exist.")
    model = Word2Vec(sentences=sentences, size=100, window=5, min_count=5, workers=4, sg=1)
    model.save('../data/embedded.w2v')
