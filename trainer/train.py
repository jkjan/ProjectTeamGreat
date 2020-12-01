import sys
import matplotlib.pyplot as plt
import time
import datetime
from train_utils import time_since, train, get_batch_set
from hyperparameters import *


# 학습 모드로 전환
model.train()

# 손실 리스트
losses = []

# 현재 손실 값
loss = 0

# 에폭마다의 손실 합
total_loss = 0

# 현재 정보
start = time.time()
now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

# 학습 정보 출력
print()
print("----------------")
print("학습을 시작합니다.")
print("현재 시각:", now)
print("학습 데이터 : %d개" % len(train_data))
print("----------------")
print()


# 학습 시작
try:
    for iter in range(n_iter):
        input, target = get_batch_set()
        loss = train(input, target)
        print(loss)
        total_loss += loss

        # 에폭당 손실
        total_loss /= len(train_data)

        # 현재 학습 과정 출력
        if iter % print_every == 0:
            avg_loss = total_loss / print_every
            sys.stdout.write("%d %d%% (%s) %.4f\n" % (iter, iter / n_iter * 100, time_since(start), avg_loss))
            losses.append(avg_loss)
            total_loss = 0

# 중단 시그널 핸들링
except KeyboardInterrupt:
    print("training terminated.")
    pass

# 손실 그래프 출력
plt.figure()
plt.plot(losses)
plt.show()

# 모델 저장
sys.stdout.write("train finished\n")
torch.save(model, path + "/model/" + "lyrics_generator_" + now + ".pt")
sys.stdout.write("saved a model.\n")
