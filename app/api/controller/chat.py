# File: app/api/controller/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Union
import asyncio
from models.KnowledgeContentModel import KnowledgeContentModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
from models.AgentModel import AgentModel
from tools.ai import ai
import time

router = APIRouter()

class ContentItem(BaseModel):
    type: str  # 内容类型，例如 "text"
    text: str  # 实际的内容

class Message(BaseModel):
    role: str
    content: Union[str, List[ContentItem]]  # 支持字符串或复杂的内容结构

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False
    temperature: Optional[float] = 1.0  # 新增支持的字段
    max_tokens: Optional[int] = None  # 新增支持的字段


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ChoiceMessage(BaseModel):
    role: str
    content: Optional[str] = None

class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: Optional[str] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    choices: List[Choice]
    usage: Usage

@router.post("/chat/completions")
async def chat_endpoint(request: ChatRequest):
    agent_model = AgentModel()
    agent = agent_model.get_agent_by_id(int(request.model))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    top_n = agent['top_n']
    #  对话模型
    a_model = agent['a_model']
    if a_model['type'] != 1:
        raise HTTPException(status_code=400, detail="指定的模型不是对话模型")

    # 初始化 AI 客户端
    chat_client = ai(api_key=a_model['api_key'], base_url=a_model['base_url'])
    # 搜索消息
    questions = []
    # 知识集合
    knowledges = []
    # 准备消息
    messages = []
    for msg in request.messages:
        if isinstance(msg.content, list):  # 如果 content 是复杂对象列表
            combined_text = " ".join(item.text for item in msg.content)  # 拼接为字符串
            messages.append({"role": msg.role, "content": combined_text})
        else:
            messages.append({"role": msg.role, "content": msg.content})
            
    # 问题优化模型
    q_model = agent['q_model']
    print(q_model)
    if q_model['type'] != 1:
        raise HTTPException(status_code=400, detail="指定的模型不是问题优化模型")
    q_client = ai(api_key=q_model['api_key'], base_url=q_model['base_url'])
    q_prompt = agent['q_prompt']
    questions = await questions_optimization(
        client=q_client,
        model=q_model['name'],
        messages=messages
    )
    origin_question = messages[-1]['content']
    if isinstance(questions, list):
        questions = [item['question'] for item in questions]
    elif isinstance(questions, dict):
        print(questions)
        extern_question = questions['question']
        questions = [
            extern_question,
            origin_question
        ]
    else:
        questions = [origin_question]
        
    base_ids = agent['base_ids'].split(",")
    a_prompt = agent['a_prompt']
    if len(base_ids) > 0:
        knowledges = await get_knowledges(base_ids,questions,top_n)
        knowledges_text = "\n\n".join(knowledges)
        messages[-1]['content'] = f"{a_prompt}\n\n使用下面<data></data>的知识辅助回答问题" \
        f"<data>{knowledges_text}</data>\n用户问题:\n'''{origin_question}'''"
    if request.stream:
        try:
            async def event_generator():
                async for chunk in (await chat_client.chat(model=a_model['name'], messages=messages, stream=True)):
                    delta_content = {"content": chunk}  # 修复解析逻辑
                    response = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": a_model['name'],
                        "choices": [{"index": 0, "delta": delta_content}],
                    }
                    yield f"data: {response}\n\n"

                # 结束标记
                yield f"data: [DONE]\n\n"


            return StreamingResponse(event_generator(), media_type="text/event-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            response = await chat_client.chat(model=a_model['name'], messages=messages, stream=False)
            # 构造 OpenAI 格式的响应
            openai_response = ChatCompletionResponse(
                id=f"chatcmpl-{int(time.time())}",
                created=int(time.time()),
                choices=[
                    Choice(
                        index=0,
                        message=ChoiceMessage(role="assistant", content=response),
                        finish_reason="stop"
                    )
                ],
                usage=Usage(
                    prompt_tokens=0,  # 这里需要根据实际情况填充
                    completion_tokens=len(response.split()),
                    total_tokens=len(response.split())
                )
            )
            return JSONResponse(content=openai_response.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
# 根据历史消息，获取优化后的问题集合
async def questions_optimization(client:ai,model:str, messages: list,q_prompt:str=None) -> list:
    system_prompt = f"""接下来请帮忙对问题扩展，扩展问题到1-3个，便于知识库搜索。如果用户消息带有历史记录，你需要帮忙做指代消除。
背景知识：{q_prompt}"""+"""
案例
明白了，以下是按照您的要求，使用原先不完善的中文问题并生成相应的JSON输出：

示例 1
EXAMPLE INPUT: 艾菲尔铁塔在哪  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "艾菲尔铁塔的位置"
    },
    {
        "question": "艾菲尔铁塔的地址"
    }
]
```

示例 2
EXAMPLE INPUT: 怎么去机场  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "去机场的路线"
    },
    {
        "question": "到达机场的步骤"
    }
]
```

示例 3
EXAMPLE INPUT: 光合作用是什么  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "光合作用的定义"
    },
    {
        "question": "光合作用的过程解释"
    }
]
```

示例 4
EXAMPLE INPUT: 怎么烤蛋糕  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "烤蛋糕的步骤"
    },
    {
        "question": "烤蛋糕的食谱"
    }
]
```

示例 5
EXAMPLE INPUT: iPhone什么时候发明的  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "iPhone的发明日"
    },
    {
        "question": "iPhone的创建年份"
    }
]
```

示例 6
EXAMPLE INPUT: 为什么天空是蓝色的  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "天空呈现蓝色的原因"
    },
    {
        "question": "天空为什么是蓝色的解释"
    }
]
```

示例 7
EXAMPLE INPUT: 谁发现了重力  
EXAMPLE JSON OUTPUT:
```json
[
    {
        "question": "发现重力的科学家"
    },
    {
        "question": "发现重力的人的名字"
    }
]
```
请注意输出格式必须为一个大的list，每个元素为一个字典，包含一个key为question的字符串。
不允许在[]外面再套其他questions
"""
    user_prompt = messages[-1]['content']
    history = messages[:-1]
    result = await client.extract_json(model, system_prompt, user_prompt, history)
    return result

# 根据知识库ids和问题集合查找符合要求的n个答案
async def get_knowledges(base_ids: list, questions: list, top_n: int) -> list:
    # TODO:进一步并行 优化查询速度
    base_model = KnowledgeBaseModel()
    content_model = KnowledgeContentModel()
    embedding_model = base_model.get_model_details_by_base_id(base_ids[0])
    embedApi = ai(embedding_model['api_key'], embedding_model['base_url'])
    embedding_list = []
    # 得到多个问题的embedding
    for question in questions:
        embedding = await embedApi.embedding(embedding_model['model'], question)
        embedding_list.append(embedding)
    # 对每个base_id，用每个embedding去搜索
    res = []
    for embedding in embedding_list:
        contents = content_model.get_nearest_neighbors(embedding, top_n=top_n, base_ids=base_ids)
        # 确保 contents 中的每个元素都是字符串类型
        contents = [content['content'] for content in contents]
        res.extend(contents)
    return res