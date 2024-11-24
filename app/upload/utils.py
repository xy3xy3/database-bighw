import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

def load_data():
    import pickle
    import numpy as np
    dir = 'C://Users//86139//Desktop//大三上//ML//hw2//data'
    X_train = []
    Y_train = []
    for i in range(1, 6):
        with open(dir + r'/data_batch_' + str(i), 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        X_train.append(dict[b'data'])
        Y_train += dict[b'labels']
    X_train = np.concatenate(X_train, axis=0)
    Y_train = np.array(Y_train, dtype=np.int64)
    with open(dir + r'/test_batch', 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    X_test = dict[b'data']
    Y_test = np.array(dict[b'labels'], dtype=np.int64)
    return X_train, Y_train, X_test, Y_test


def preprocess_data(X, Y, batch_size):
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    X = (X - mean) / (std + 1e-8)  
    X = torch.tensor(X, dtype=torch.float32)
    Y = torch.tensor(Y, dtype=torch.long)
    dataset = TensorDataset(X, Y)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

def plot_all_curves(train_accuracies, test_accuracies, epochs):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))

    colors = ['blue', 'orange', 'green']
    optimizers = ['SGD', 'SGD Momentum', 'Adam']

    for i, optimizer in enumerate(optimizers):
        plt.plot(range(1, epochs + 1), train_accuracies[i], linestyle='-', color=colors[i],
                 label=f'{optimizer} Train Accuracy')
        plt.plot(range(1, epochs + 1), test_accuracies[i], linestyle='--', color=colors[i],
                 label=f'{optimizer} Test Accuracy')

    plt.title('Train and Test Accuracies for Different Optimizers')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def calculate_fc_input_size(image_size, num_conv_layers, use_pooling, kernel_size, stride, padding, pooling_kernel, pooling_stride):
    height, width = image_size
    for _ in range(num_conv_layers):
        height = (height - kernel_size + 2 * padding) // stride + 1
        width = (width - kernel_size + 2 * padding) // stride + 1
        if use_pooling:
            height = (height - pooling_kernel) // pooling_stride + 1
            width = (width - pooling_kernel) // pooling_stride + 1
    return height * width
