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
 
    # 这里只使用对话模型 (a_model)
    a_model = agent['a_model']
    if a_model['type'] != 1:
        raise HTTPException(status_code=400, detail="指定的模型不是对话模型")

    # 初始化 AI 客户端
    ai_client = ai(api_key=a_model['api_key'], base_url=a_model['base_url'])
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
   # 获取知识库 用,隔开
    base_ids = agent['base_ids'].split(",")
    if len(base_ids) > 0:
        # 暂时只实现单一知识库关联
        question = messages[-1]['content']
        questions = [question]
        knowledges = await get_knowledges(base_ids,top_n,questions)
        knowledges_text = "\n\n".join(knowledges)
        messages[-1]['content'] = f"使用下面<data></data>的知识辅助回答问题" \
        f"<data>{knowledges_text}</data>\n用户问题:\n'''{question}'''"
    if request.stream:
        try:
            async def event_generator():
                async for chunk in (await ai_client.chat(model=a_model['name'], messages=messages, stream=True)):
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
            response = await ai_client.chat(model=a_model['name'], messages=messages, stream=False)
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


async def get_knowledges(base_ids:list, questions:str,top_n:int)->list:
    # TODO:进一步并行 优化查询速度
    base_model = KnowledgeBaseModel()
    content_model = KnowledgeContentModel()
    embedding_model = base_model.get_model_details_by_base_id(base_ids[0])
    embedApi = ai(embedding_model['api_key'],embedding_model['base_url'])
    embedding_list = []
    # 得到多个问题的embedding
    for question in questions:
        embedding = await embedApi.embedding(embedding_model['model'],question)
        embedding_list.append(embedding)
    # 对每个base_id，用每个embedding去搜索
    res = []
    for embedding in embedding_list:
        contents = await content_model.get_nearest_neighbors(embedding,top_n=top_n,base_ids=base_ids)
        res.extend(contents)
    return res