from konlpy.tag import Mecab
import pandas as pd
from random import shuffle
import pickle
from gensim.models import Word2Vec

tokenizer = Mecab().morphs
word_count = {}

df = pd.read_csv("../data/refined_data.tsv", sep='\t')
data = {}

sentences = []
unique_words = set()

for i in range(len(df)):
    tokenized_title = tokenizer(df['제목'][i])
    tokenized_genre = tokenizer(df['장르'][i])
    tokenized_lyrics = tokenizer(df['가사'][i])

    words = tokenized_title + tokenized_genre + tokenized_lyrics
    sentences.append(words)

    for word in words:
        unique_words.add(word)

shuffle(sentences)

data_size = len(sentences)
train_size = int(0.7 * data_size)
test_size = data_size - train_size

data['train'] = sentences[:train_size]
data['test'] = sentences[train_size:]

pickle.dump(data, open("../data/tokenized_data.pkl", 'wb'))
pickle.dump(sentences, open("../data/sentences.pkl", 'wb'))
pickle.dump(unique_words, open("../data/unique_words.pkl", 'wb'))

try:
    model = Word2Vec.load('../data/embedded.w2v')
    print("embedded file exists:")
except FileNotFoundError:
    print("embedded file does not exist.")
    model = Word2Vec(sentences=sentences, size=100, window=5, min_count=0, workers=4, sg=1)
    model.save('../data/embedded.w2v')
