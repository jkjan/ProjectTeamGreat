import time
import math
from hyperparameters import *
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
import numpy as np
import random


def get_random_batch(data):
    """
    :param data: 문자열 리스트로 된 데이터
    :return: 무작위 배치 인덱스
    """
    from_ = random.randint(0, len(data) - batch_size)
    _to = from_ + batch_size
    return from_, _to


def get_batch_set(is_train=True):
    """
    :param is_train: 학습 여부
    :return: 입력, 타겟, 입력의 최대 길이
    """
    data = train_data if is_train else test_data
    from_, _to = get_random_batch(data)
    input = batch_to_tensor(data[from_:_to], True)
    target = batch_to_tensor(data[from_:_to], False)
    return input, target


def batch_to_tensor(data, is_input):
    """
    :param data: 문자열 리스트로 된 데이터
    :param is_input: True-입력, False-타겟
    :return: 패딩된 텐서
    """
    # 텐서 패딩

    padded = pad_sequence([get_input(d) if is_input else get_target(d) for d in data])
    # 배치 별 길이 재기
    input_lengths = torch.LongTensor([torch.max(torch.nonzero(padded[:, i].data, as_tuple=False)) + 1 for i in range(padded.shape[1])])
    # 내림차순으로 정렬된 인덱스 얻기
    values, indices = input_lengths.sort(0, descending=True)
    padded = padded[:, indices]
    return padded.to(device)


def word_to_tensor(word):
    """
    :param word: 단어
    :return: 단어 벡터(1, 100)
    """
    try:
        tensor = torch.tensor(np.array(wv[word]))
        tensor = tensor.unsqueeze_(0)
        return tensor
    except KeyError:
        return None


def get_tensor_set(i, is_train=True):
    """
    :param i: 데이터 인덱스
    :param is_train: 학습 여부
    :return:
    """
    d = train_data if is_train else test_data
    input = get_input(d[i])
    target = get_target(d[i])
    return input, target


def get_input(d):
    """
    :param d: 데이터
    :return: 입력 텐서 (n, 100)
    """
    input = torch.cat([doc_to_tensor(d)])
    return input.to(device)


def get_target(data):
    """
    :param data: 문자열 리스트로 된 데이터
    :return: 타겟 텐서 (n)
    """
    target = []

    # 인덱스 기록
    for idx, word in enumerate(data):
        if word_to_idx[word] < output_size:
            target.append(word_to_idx[word])

    # EOS 추가
    target.append(word_to_idx['<EOS>'])
    return torch.LongTensor(target[1:]).to(device)


def doc_to_tensor(doc):
    """
    :param doc: 문자열 리스트
    :return: 벡터(n, 100) (n=단어 수)
    """
    tensor = None
    for word in doc:
        w_tensor = word_to_tensor(word)
        if w_tensor is not None:
            if tensor is None:
                tensor = w_tensor
            else:
                tensor = torch.cat([tensor, w_tensor])
    return tensor.to(device)


def time_since(since):
    """
    :param since: 기준 시간
    :return: 기준으로부터 흐른 시간
    """
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return "%dm %ds" % (m, s)


def train(input, target):
    """
    :param input: 입력 텐서
    :param target: 타겟 텐서
    :return: 출력, 손실 평균값
    """
    # 기울기 초기화
    hidden = model.init_hidden()
    optimizer.zero_grad()
    loss = 0

    # 단어 입력
    for i in range(input.size()[0]):
        output, hidden = model(input.data[i].unsqueeze(0), hidden)
        l = criterion(output, target.data[i])
        loss += l

    # 역전파
    loss.backward()

    # 최적화
    optimizer.step()

    # 학습률 조정
    scheduler.step()

    return loss


def generate_lyrics(str):
    input = get_input(str)
    hidden = model.init_hidden()
    generated_lyrics = ""
    word_cnt = 0

    while word_cnt < 100:
        input = input.resize(len(input), 1, input_size)
        output, hidden = model(input, hidden)
        output = output.argmax()
        word = idx_to_words[output]
        if word == "<EOS>":
            break
        generated_lyrics += '%s ' % word
        input = get_input(word)
        word_cnt += 1

    return generated_lyrics