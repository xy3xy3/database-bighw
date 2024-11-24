# 机器学习与数据挖掘 作业2

## 1. 线性分类器

$$
\mathbf{\hat{y}} = \mathbf{\omega}\mathbf{x} + \mathbf{b}
$$

### 数据预处理

首先使用给定load_data()函数读取CIFAR10数据集

然后实现preprocess_data()函数，通过计算均值和方差的方式将数据归一化：

```
def preprocess_data(X, Y, batch_size):
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    X = (X - mean) / (std + 1e-8)  
    X = torch.tensor(X, dtype=torch.float32)
    Y = torch.tensor(Y, dtype=torch.long)
    dataset = TensorDataset(X, Y)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader
```

### 参数初始化

本实验没有手动调整模型参数初始化方式，采用pytorch默认参数初始化方法

在pytorch中，Linear权重矩阵的初始化使用的是**均匀分布**，其范围为

$$
\mathbf{W} \sim \mathcal{U} \left( -\frac{1}{\sqrt{\text{in\_features}}}, \frac{1}{\sqrt{\text{in\_features}}} \right)
$$

其中，in_features 是输入的特征维度。

Linear偏置向量初始化为**零向量**

$$
\mathbf{b} = 0
$$

### 训练方式&训练结果

模型定义如下
```
class SoftmaxClassifier(nn.Module):
    def __init__(self, input_size=32*32*3, num_classes=10):
        super(SoftmaxClassifier, self).__init__()
        self.linear = nn.Linear(input_size, num_classes)

    def forward(self, x):
        return self.linear(x)
```

分别使用SGD算法、SGD Momentum算法和 Adam算法训练模型

```
optimizers = [
        ('SGD', optim.SGD(models[0].parameters(), lr=lr, momentum=0)),
        ('SGD Momentum', optim.SGD(models[1].parameters(), lr=lr, momentum=0.9)),
        ('Adam', optim.Adam(models[2].parameters(), lr=lr))
    ]
```

在确保可以达到过拟合的条件下，采取如下超参数配置

```
epochs = 100
lr = 1e-3
batch_size = 64
```

训练结果可视化如下

![Linear_cls_loss](assets\Linear_cls_loss.png)

![Linear_cls_acc](assets\Linear_cls_acc.png)

记录各个优化器在测试集上得到的最佳准确率如下
```
Best Test Accuracies:
SGD optimizer: Best Test Accuracy = 41.38%
SGD Momentum optimizer: Best Test Accuracy = 39.07%
Adam optimizer: Best Test Accuracy = 36.81%
```

观察结果，发现在CIFAR-10图像分类任务中，相同超参数配置下，SGD优化器得到的结果最好，SGD with Momentum=0.9次之，最后Adam优化器收敛速度最慢，并且在测试集上的准确率最低。

## 2. MLP

![MLP](assets\MLP.png)

数据预处理及参数初始化同线性分类器

### 训练方式&训练结果

模型定义如下，为了比较使用不同网络层数和不同神经元数量对模型性能的影响，设置hidden_dim与num_layers参数，方便后续的网格化搜索。

```
class MLP(nn.Module):
    def __init__(self, input_size=32*32*3, hidden_dim=128, num_layers=2, num_classes=10):
        super(MLP, self).__init__()
        layers = []

        in_dim = input_size
        for _ in range(num_layers):
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.ReLU())
            in_dim = hidden_dim

        layers.append(nn.Linear(in_dim, num_classes))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)
```

超参数设置如下

```
epochs = 100
lr = 1e-3
batch_size = 1024
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
```

同样，我们还需要比较各个优化器在使用MLP进行图像分类任务上的差别：

```
optimizers = [
        ('SGD', lambda params: optim.SGD(params, lr=lr, momentum=0)),
        ('SGD Momentum', lambda params: optim.SGD(params, lr=lr, momentum=0.9)),
        ('Adam', lambda params: optim.Adam(params, lr=lr))
]
```

本实验中，设置不同网络层数与神经元数量如下，在训练时进行排列组合

```
hidden_dims = [64, 128, 256, 512]
    num_layers_options = [1, 2, 3]
```

训练结果如下表格所示

| Hidden Dim | Num Layers | Optimizer       | Best Test Acc (%) |
|------------|------------|-----------------|-------------------|
| 64         | 1          | SGD             | 42.38            |
| 64         | 1          | SGD Momentum    | 50.78            |
| 64         | 1          | Adam            | 50.81            |
| 64         | 2          | SGD             | 37.67            |
| 64         | 2          | SGD Momentum    | 51.21            |
| 64         | 2          | Adam            | 52.10            |
| 64         | 3          | SGD             | 28.08            |
| 64         | 3          | SGD Momentum    | 50.39            |
| 64         | 3          | Adam            | 51.63            |
| 128        | 1          | SGD             | 43.02            |
| 128        | 1          | SGD Momentum    | 52.55            |
| 128        | 1          | Adam            | 52.00            |
| 128        | 2          | SGD             | 37.62            |
| 128        | 2          | SGD Momentum    | 52.26            |
| 128        | 2          | Adam            | 53.03            |
| 128        | 3          | SGD             | 29.99            |
| 128        | 3          | SGD Momentum    | 51.88            |
| 128        | 3          | Adam            | 53.01            |
| 256        | 1          | SGD             | 43.51            |
| 256        | 1          | SGD Momentum    | 53.18            |
| 256        | 1          | Adam            | 53.22            |
| 256        | 2          | SGD             | 37.22            |
| 256        | 2          | SGD Momentum    | 53.48            |
| 256        | 2          | Adam            | 54.38            |
| 256        | 3          | SGD             | 29.84            |
| 256        | 3          | SGD Momentum    | 53.16            |
| 256        | 3          | Adam            | 54.58            |
| 512        | 1          | SGD             | 43.98            |
| 512        | 1          | SGD Momentum    | 54.15            |
| 512        | 1          | Adam            | 54.24            |
| 512        | 2          | SGD             | 38.47            |
| 512        | 2          | SGD Momentum    | 54.44            |
| 512        | 2          | Adam            | 57.01            |
| 512        | 3          | SGD             | 31.42            |
| 512        | 3          | SGD Momentum    | 53.84            |
| 512        | 3          | Adam            | 55.28            |

从实验结果中可以看出，在Num Layers，Optimizer相同的情况下，神经元数量越多，在验证集上的准确率越高

| Hidden Dim | Num Layers | Optimizer       | Best Test Acc (%) |
|------------|------------|-----------------|-------------------|
| 64         | 1          | Adam            | 50.81            |
| 128        | 1          | Adam            | 52.00            |
| 256        | 1          | Adam            | 53.22            |
| 512        | 1          | Adam            | 54.24            |

同时，在Hidden Dim, Optimizer相同的情况下，Num Layers越大，在验证集上的准确率普遍也越高

| Hidden Dim | Num Layers | Optimizer       | Best Test Acc (%) |
|------------|------------|-----------------|-------------------|
| 256        | 1          | Adam            | 53.22            |
| 256        | 2          | Adam            | 54.38            |
| 256        | 3          | Adam            | 54.58            |

最后，在Hidden Dim, Num Layers相同的情况下，Adam优化器略微优于SGD Momentum优化器，大幅优于SGD优化器

| Hidden Dim | Num Layers | Optimizer       | Best Test Acc (%) |
|------------|------------|-----------------|-------------------|
| 512        | 3          | SGD             | 31.42            |
| 512        | 3          | SGD Momentum    | 53.84            |
| 512        | 3          | Adam            | 55.28            |


## 3. CNN

LeNet是一个 7 层的神经网络，包含 3 个卷积层，2 个池化层，1 个全连接层，1个输出层。其中所有卷积层的卷积核都为 5x5，步长=1，池化方法都为平均池化，激活函数选择ReLU，网络结构如下：

![LeNet](assets\LeNet.png)

LeNet的最后一个卷积也可以视为全连接层，本实验为了方便比较不同模型结构，采取展平并全连接的方式替代最后一个卷积层。

模型定义如下，为了方便后续比较不同的卷积层数、滤波器数量和Pooling的使用对模型性能的影响，设置可控的参数num_conv_layers、filter_sizes以及use_pooling。激活函数默认采用ReLU。

```
class LeNet(nn.Module):
    def __init__(self, num_classes=10, num_conv_layers=2, filter_sizes=[6, 16], use_pooling=True, activation=nn.ReLU):
        super(LeNet, self).__init__()

        layers = []
        in_channels = 3 

        for i in range(num_conv_layers):
            out_channels = filter_sizes[i]
            layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=0))
            layers.append(activation())
            if use_pooling:
                layers.append(nn.AvgPool2d(kernel_size=2, stride=2)) 
            in_channels = out_channels

        self.feature_extractor = nn.Sequential(*layers)

        fc_input_size = filter_sizes[-1] * calculate_fc_input_size(image_size=(32, 32), num_conv_layers=num_conv_layers, use_pooling=use_pooling, kernel_size=5, stride=1, padding=0, pooling_kernel=2, pooling_stride=2)

        self.classifier = nn.Sequential(
            nn.Linear(fc_input_size, 120),
            activation(),
            nn.Linear(120, 84),
            activation(),
            nn.Linear(84, num_classes)
        )

    def forward(self, x):
        x = self.feature_extractor(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
```

特别地，由于卷积的padding均为0，卷积层的数量以及是否使用pooling都会影响卷积后的特征图尺寸，这里我们采用calculate_fc_input_size()函数动态计算卷积后的特征图尺寸。

```
def calculate_fc_input_size(image_size, num_conv_layers, use_pooling, kernel_size, stride, padding, pooling_kernel, pooling_stride):
    height, width = image_size
    for _ in range(num_conv_layers):
        height = (height - kernel_size + 2 * padding) // stride + 1
        width = (width - kernel_size + 2 * padding) // stride + 1
        if use_pooling:
            height = (height - pooling_kernel) // pooling_stride + 1
            width = (width - pooling_kernel) // pooling_stride + 1
    return height * width

```

在确保收敛的条件下，设置如下超参数

```
epochs = 100
lr = 1e-3
batch_size = 1024
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
```

同样，我们还需要比较各个优化器在使用CNN进行图像分类任务上的差别：

```
optimizers = [
        ('SGD', lambda params: optim.SGD(params, lr=lr, momentum=0)),
        ('SGD Momentum', lambda params: optim.SGD(params, lr=lr, momentum=0.9)),
        ('Adam', lambda params: optim.Adam(params, lr=lr))
    ]

```

本实验中，设置LeNet网络结构配置如下

```
experiment_configs = [
    # 单层卷积
    {"num_conv_layers": 1, "filter_sizes": [12], "use_pooling": True, "activation": nn.ReLU},
    {"num_conv_layers": 1, "filter_sizes": [6], "use_pooling": True, "activation": nn.ReLU},
    {"num_conv_layers": 1, "filter_sizes": [6], "use_pooling": False, "activation": nn.ReLU},
    
    # 两层卷积
    {"num_conv_layers": 2, "filter_sizes": [12, 32], "use_pooling": True, "activation": nn.ReLU},
    {"num_conv_layers": 2, "filter_sizes": [6, 16], "use_pooling": True, "activation": nn.ReLU}, # 原版配置
    {"num_conv_layers": 2, "filter_sizes": [6, 16], "use_pooling": False, "activation": nn.ReLU},
    
    # 三层卷积
    {"num_conv_layers": 3, "filter_sizes": [6, 16, 32], "use_pooling": False, "activation": nn.ReLU},
    {"num_conv_layers": 3, "filter_sizes": [12, 32, 64], "use_pooling": False, "activation": nn.ReLU},
]
```
注:由于原图尺寸为32x32, 若采用3次池化, 特征图大小将缩减为4x4, 小于卷积核大小5x5, 因此这里在三层卷积的配置中均未采用池化操作

训练结果如下表格所示

| Num Conv Layers | Filter Sizes     | Use Pooling | Optimizer       | Best Test Accuracy |
|-----------------|------------------|-------------|-----------------|---------------------|
| 1               | [12]            | True        | SGD             | 34.64%             |
| 1               | [12]            | True        | SGD Momentum    | 58.24%             |
| 1               | [12]            | True        | Adam            | 60.33%             |
| 1               | [6]             | True        | SGD             | 30.40%             |
| 1               | [6]             | True        | SGD Momentum    | 53.42%             |
| 1               | [6]             | True        | Adam            | 56.55%             |
| 1               | [6]             | False       | SGD             | 38.31%             |
| 1               | [6]             | False       | SGD Momentum    | 54.96%             |
| 1               | [6]             | False       | Adam            | 54.99%             |
| 2               | [12, 32]        | True        | SGD             | 18.51%             |
| 2               | [12, 32]        | True        | SGD Momentum    | 54.74%             |
| 2               | [12, 32]        | True        | Adam            | 65.73%             |
| 2               | [6, 16]         | True        | SGD             | 20.55%             |
| 2               | [6, 16]         | True        | SGD Momentum    | 49.38%             |
| 2               | [6, 16]         | True        | Adam            | 61.62%             |
| 2               | [6, 16]         | False       | SGD             | 37.03%             |
| 2               | [6, 16]         | False       | SGD Momentum    | 56.42%             |
| 2               | [6, 16]         | False       | Adam            | 57.90%             |
| 3               | [6, 16, 32]     | False       | SGD             | 26.92%             |
| 3               | [6, 16, 32]     | False       | SGD Momentum    | 56.34%             |
| 3               | [6, 16, 32]     | False       | Adam            | 54.72%             |
| 3               | [12, 32, 64]    | False       | SGD             | 36.35%             |
| 3               | [12, 32, 64]    | False       | SGD Momentum    | 63.32%             |
| 3               | [12, 32, 64]    | False       | Adam            | 62.81%             |

分析实验结果，可以发现, 在其他配置相同的情况下：

1. 卷积层数越多,模型在测试集上的准确率越高,性能更强
2. 滤波器数量越多,模型在测试集上的准确率越高,性能更强
3. 池化操作对于模型性能有明显的增强作用

## 综合比较

综上, 在CIFAR-10图像分类任务上, 线性分类器、MLP和CNN各自最好的表现如下:

| Model           | Best Test Accuracy |
|-----------------|--------------------|
| 线性分类器       | 41.38%             |
| MLP             | 57.01%             |
| CNN             | 63.32%             |

### 总体分析

- 线性分类器由于模型能力有限，性能较低，适合用于简单任务或初步尝试。
- MLP在增加深度和宽度后能够学习复杂的特征，适合中等复杂度的任务。
- CNN通过卷积和池化操作有效地捕获图像的空间特征，是解决图像分类问题的首选。