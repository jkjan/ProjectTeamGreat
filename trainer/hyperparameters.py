from torch.optim.lr_scheduler import StepLR
import pickle
from gensim.models import Word2Vec
import torch
import torch.nn as nn
from GRU import GRU


# 필요한 데이터들 경로와 이름
path = "../data/"
data = pickle.load(open(path + "tokenized_data.pkl", "rb"))
train_data = data["train"]
test_data = data["test"]
wv = Word2Vec.load(path + "embedded.w2v")
unique_words = pickle.load(open(path + "unique_words.pkl", "rb"))

word_to_idx = {}
idx_to_words = []

for idx, word in enumerate(unique_words):
    idx_to_words.append(word)
    word_to_idx[word] = idx

word_to_idx["<EOS>"] = len(idx_to_words)
idx_to_words.append("<EOS>")

# 배치 크기
batch_size = 128

# 학습률
learning_rate = 0.02

# CUDA 정보 출력
if torch.cuda.is_available():
    print("CUDA 사용이 가능합니다.\n")
    device = torch.device("cuda")
    torch.backends.cudnn.benchmark = True
    cur_device = torch.cuda.current_device()
    print("기기        ")
    print("    번호:      ", cur_device)
    print("    이름:      ", torch.cuda.get_device_name(cur_device))
    print("메타데이터      ")
    print("    CUDA 버전: ", torch.version.cuda)
    print("    Torch 버전:", torch.__version__)
    print("    cuDNN 버전:", torch.backends.cudnn.version())
    print("메모리 사용량    ")
    print("    최대:      ", round(torch.cuda.max_memory_allocated(cur_device) / 1024 ** 3, 1), "GB")
    print("    현재:      ", round(torch.cuda.memory_allocated(cur_device) / 1024 ** 3, 1), "GB")
    print("    캐시:      ", round(torch.cuda.memory_reserved(cur_device) / 1024 ** 3, 1), "GB")
    print()
else:
    print("CUDA를 사용할 수 없습니다.")
    exit()
    device = torch.device("cpu")


# 입력 크기
input_size = 100

# 은닉층 크기
hidden_size = 128

# 출력 크기 (=총 단어 수)
output_size = len(word_to_idx)

# 층 개수
num_layers = 3

# 사용할 모델
model = GRU(input_size, hidden_size, output_size, batch_size, device, num_layers)

# 손실 함수
criterion = nn.CrossEntropyLoss()

# 역전파 때 사용할 최적화 기법
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# 학습 과정 출력 빈도
print_every = 1

# 손실 값 그래프에 입력하는 빈도
plot_every = 1

# 반복 횟수
n_iter = 100

# 학습률 스케쥴러
scheduler = StepLR(optimizer, step_size=int(n_iter/3), gamma=0.1)

# 현재 에폭
now_epoch = 0
