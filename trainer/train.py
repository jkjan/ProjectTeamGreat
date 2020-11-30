from gensim.models import Word2Vec

model = Word2Vec.load('../data/embedded.w2v')
print("embedded file exists:")

vec = model.wv.similar_by_word('사랑')
print(len(model.wv.vocab))

for w, sim in vec:
    print(f'{w} {sim}')