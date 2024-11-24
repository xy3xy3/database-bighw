# File: app/api/controller/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from app.models.AgentModel import AgentModel
from app.tools.ai import ai
import time

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: int  # 使用 Agent 的 ID
    messages: List[Message]
    stream: Optional[bool] = False

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

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    agent_model = AgentModel()
    agent = agent_model.get_agent_by_id(request.model)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # 这里只使用对话模型 (a_model)
    a_model = agent['a_model']
    if a_model['type'] != 1:
        raise HTTPException(status_code=400, detail="指定的模型不是对话模型")

    # 初始化 AI 客户端
    ai_client = ai(api_key=a_model['api_key'], base_url=a_model['base_url'])

    # 准备消息
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

    if request.stream:
        try:
            async def event_generator():
                async for chunk in ai_client.chat(model=a_model['name'], messages=messages, stream=True):
                    # 根据参考格式解析和返回数据
                    if isinstance(chunk, dict):  # 假设返回的是已解析的 JSON
                        yield f"data: {chunk}\n\n"
                    else:
                        # 如果返回的不是 JSON，需要手动组装
                        delta_content = {"content": chunk}
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
