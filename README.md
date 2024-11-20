用python fastapi，sqlmodel实现的数据库大作业


# AGENT-LLM

支持向量数据库的大模型对话智能体平台

## 表

### knowledgebase

存储知识库

包含名称，介绍字段

### knowledge

存储知识库的内容

包含内容，向量字段，base_id（该数据库在datavec，所以只记录id，不设置外键）

### model

存储模型，包括name,base_url,api_key,type（0embedding,1chat）

### agent

关联模型和知识库

### history

存储对话历史，包含id，时间，agent_id

### message

存储对话内容，包含id，时间，history_id，role，content，关联history的id字段



# 环境配置

使用conda python 3.12 环境
```shell
conda create -n dbhw python=3.12 -y
conda activate dbhw
```

安装依赖包
```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```