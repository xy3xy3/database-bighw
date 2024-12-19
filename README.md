用python fastapi，sqlmodel实现的数据库大作业


# AGENT-LLM

支持向量数据库的大模型对话智能体平台

## 表

### knowledgebase

存储知识库

包含名称，介绍字段

id,name,desc,model_id（向量模型id）

### knowledge

存储知识库的内容

包含内容，向量字段，base_id（该数据库在datavec，所以只记录id，不设置外键）

id,base_id,content,embedding

### model

存储模型，包括

id,name,base_url,api_key,type（0embedding,1chat）

### agent

关联模型和知识库

id,name,base_ids,max_ref(引用token上限),min_cor(相关度下限),
q_model_id(问题优化模型id),q_prompt(问题优化的提示),
a_model_id(答案生成模型id),a_prompt(答案生成的提示，可能需要一些变量指代知识库的知识)

### message

存储对话内容，包含id，time，session_id，role，content



# 环境配置

opengauss datavec docker
```shell
docker run --name opengauss --privileged=true -d -e GS_PASSWORD=OGSql@123 -v ./data:/var/lib/opengauss -p 5432:5432 swr.cn-north-4.myhuaweicloud.com/opengauss-x86-64/opengauss-datavec:7.0.0-rc1
```

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


```shell
conda activate dbhw
cd app
python main.py
```

# 技术路径
- fastgpt
- openGauss 提供数据库
- https://github.com/xqdoo00o/chatgpt-web 提供对话前端
- langchain