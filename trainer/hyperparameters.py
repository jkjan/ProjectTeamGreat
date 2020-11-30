from torch.optim.lr_scheduler import StepLR
import pickle
from gensim.models import Word2Vec
import torch
import torch.nn as nn
from GRU import GRU


# paths, names of needed data
path = "../data/"
data = pickle.load(open(path + "tokenized_data.pkl", "rb"))
train_data = data['train']
test_data = data['test']
model = Word2Vec.load(path + "embedded.w2v")
unique_words = pickle.load(open(path + "unique_words.pkl", "rb"))

# a size of batch
batch_size = 128

# learning rate
learning_rate = 0.02

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA is available.\n")
    torch.backends.cudnn.benchmark = True
    cur_device = torch.cuda.current_device()
    print('Device:      ')
    print("    Index:   ", cur_device)
    print("    Name:    ", torch.cuda.get_device_name(cur_device))
    print('METADATA:    ')
    print('    CUDA ver: ', torch.version.cuda)
    print('    Torch ver:', torch.__version__)
    print('    cuDNN ver:', torch.backends.cudnn.version())
    print('Memory Usage:')
    print('    Max Alloc:', round(torch.cuda.max_memory_allocated(cur_device) / 1024 ** 3, 1), 'GB')
    print('    Allocated:', round(torch.cuda.memory_allocated(cur_device) / 1024 ** 3, 1), 'GB')
    print('    Cached:   ', round(torch.cuda.memory_reserved(cur_device) / 1024 ** 3, 1), 'GB')
    print()
else:
    device = torch.device("cpu")


# input size
input_size = 100

# the number of hidden layers
hidden_size = 128

# a size of output tensor
output_size = len(model.wv.vocab)

# the number of layers
num_layers = 3

# a deep learning model to use
model = GRU(input_size, hidden_size, output_size, batch_size, device, num_layers)

# loss function
criterion = nn.CrossEntropyLoss()

# optimizer with backpropagation
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# print frequency
print_every = 1

# plot frequency
plot_every = 1

# the number of iteration
n_iter = 100

# learning rate scheduler
scheduler = StepLR(optimizer, step_size=int(n_iter/3), gamma=0.1)

# a current epoch
now_epoch = 0
