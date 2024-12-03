import json
import random
import string
import traceback
from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Union
import asyncio
from models.ConfigModel import ConfigModel
from models.KnowledgeContentModel import KnowledgeContentModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
from models.AgentModel import AgentModel
from models.MessageModel import MessageModel

from tools.ai import ai
import time

# 导入logging模块并配置日志格式
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

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
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    session_id: Optional[str] = None

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
async def chat_endpoint(request: ChatRequest, authorization: Optional[str] = Header(None)):
    try:
        # 从请求头中提取 Bearer Token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        provided_api_key = authorization.split("Bearer ")[1]
        # 获取配置中的 API Key
        config_model = ConfigModel()
        stored_api_key = await config_model.get_config("api_key")
        # 验证 API Key 是否匹配
        if not stored_api_key or provided_api_key != stored_api_key:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": {
                        "message": f"[{provided_api_key}]无效的令牌",
                        "type": "api_error"
                    }
                }
            )
        session_id = request.session_id if request.session_id else ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        message_model = MessageModel()

        agent_model = AgentModel()
        if request.model.startswith("gpt-"):
            id = 1
        else:
            id = int(request.model)
        agent = await agent_model.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        top_n = agent['top_n']
        # 对话模型
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
        if q_model['type'] != 1:
            raise HTTPException(status_code=400, detail="指定的模型不是问题优化模型")
        q_client = ai(api_key=q_model['api_key'], base_url=q_model['base_url'])
        q_prompt = agent['q_prompt']
        questions = await questions_optimization(client=q_client, model=q_model['name'], messages=messages)
        origin_question = messages[-1]['content']
        if isinstance(questions, list):
            questions = [item['question'] for item in questions]
        elif isinstance(questions, dict):
            if questions.get("questions") and isinstance(questions.get("questions"), list):
                questions = [item['question'] for item in questions.get("questions")]
            elif questions.get("question") and isinstance(questions.get("question"), str):
                questions = [questions.get("question"), origin_question]
            else:
                questions = [origin_question]
        else:
            questions = [origin_question]
        user_message = {
            "session_id": session_id,
            "role": "user",
            "content": messages[-1]['content']
        }
        await message_model.save(user_message)
        base_ids = agent['base_ids'].split(",")
        a_prompt = agent['a_prompt']
        if len(base_ids) > 0:
            knowledges = await get_knowledges(base_ids, questions, top_n)
            knowledges_text = "\n\n".join(knowledges)
            questions_str = ",".join(questions)
            messages[-1]['content'] = f"{a_prompt}\n\n使用下面<data></data>的知识辅助回答问题,该结果来源于用户问题经过优化后的问题在知识库搜索" \
            f"<data>{knowledges_text}</data>\n用户问题:\n'''{origin_question}'''\n优化后的问题是:{questions_str}"
        if request.stream:
            async def event_generator():
                collected_response = ""
                start_time = time.time()
                async for chunk in (await chat_client.chat(model=a_model['name'], messages=messages, stream=True)):
                    delta_content = chunk.strip()
                    collected_response += delta_content
                    response = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": a_model['name'],
                        "choices": [{
                            "index": 0,
                            "delta": {"content": delta_content}
                        }],
                    }
                    yield f"data: {json.dumps(response)}\n\n"
                end_time = time.time()
                logging.info(f"大模型回答耗时: {end_time - start_time}秒")
                # 记录AI消息
                ai_message = {"session_id": session_id, "role": "assistant", "content": collected_response}
                await message_model.save(ai_message)
                # 结束标记
                response = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": a_model['name'],
                    "choices": [{
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop"
                    }],
                }
                yield f"data: {json.dumps(response)}\n\n"
                yield f"data: [DONE]\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")
        else:
            start_time = time.time()
            response_text = await chat_client.chat(model=a_model['name'], messages=messages, stream=False)
            end_time = time.time()
            logging.info(f"大模型回答耗时: {end_time - start_time}秒")
            openai_response = ChatCompletionResponse(
                id=f"chatcmpl-{int(time.time())}",
                created=int(time.time()),
                choices=[Choice(index=0, message=ChoiceMessage(role="assistant", content=response_text), finish_reason="stop")],
                usage=Usage(prompt_tokens=0, completion_tokens=len(response_text.split()), total_tokens=len(response_text.split())))
            # 记录AI消息
            ai_message = {"session_id": session_id, "role": "assistant", "content": response_text}
            await message_model.save(ai_message)
            return JSONResponse(content=openai_response.dict())
    except Exception as e:
        errmsg = f"{e} {traceback.format_exc()}"
        logging.error(errmsg)
        raise HTTPException(status_code=500, detail=errmsg)

# 根据历史消息，获取优化后的问题集合
async def questions_optimization(client: ai, model: str, messages: list, q_prompt: str = None) -> list:
    start_time = time.time()
    system_prompt = f"""接下来请帮忙对问题扩展，扩展问题到1-3个，便于知识库搜索。
如果用户消息带有历史记录，你需要帮忙做指代消除。
背景知识：{q_prompt}""" + """
案例
示例 1
EXAMPLE INPUT: 艾菲尔铁塔在哪
EXAMPLE JSON OUTPUT:
```json
{
    "questions": [
        {
            "question": "艾菲尔铁塔的位置"
        },
        {
            "question": "艾菲尔铁塔的地址"
        }
    ]
}
```

示例 2
EXAMPLE INPUT: 怎么去机场
EXAMPLE JSON OUTPUT:
```json
{
    "questions": [
        {
            "question": "去机场的路线"
        },
        {
            "question": "到达机场的步骤"
        }
    ]
}
```

示例 3:指代消除
EXAMPLE History: 蔡徐坤是明星吗?
EXAMPLE INPUT: 他最近在哪里演出
EXAMPLE JSON OUTPUT:
```json
{
    "questions": [
        {
            "question": "蔡徐坤最近演出地点"
        },
        {
            "question": "蔡徐坤演出时间"
        }
    ]
}
```

现在请结合用户的历史聊天记录对当前问题进行修改扩充
"""
    user_prompt = messages[-1]['content']
    history = messages[:-1]
    result = await client.extract_json(model, system_prompt, user_prompt, history)
    end_time = time.time()
    logging.info(f"问题优化耗时: {end_time - start_time}秒")
    return result

# 根据知识库ids和问题集合查找符合要求的n个答案
async def get_knowledges(base_ids: list, questions: list, top_n: int) -> list:
    start_time = time.time()
    base_model = KnowledgeBaseModel()
    content_model = KnowledgeContentModel()
    embedding_model = await base_model.get_model_details_by_base_id(base_ids[0])
    embedApi = ai(embedding_model['api_key'], embedding_model['base_url'])
    embedding_list = []
    # 得到多个问题的embedding
    for question in questions:
        embedding = await embedApi.embedding(embedding_model['model'], question)
        embedding_list.append(embedding)
    # 对每个base_id，用每个embedding去搜索
    res = []
    for embedding in embedding_list:
        contents = await content_model.get_nearest_neighbors(embedding, top_n=top_n, base_ids=base_ids)
        # 确保 contents 中的每个元素都是字符串类型
        contents = [content['content'] for content in contents]
        res.extend(contents)
    end_time = time.time()
    logging.info(f"向量搜索耗时: {end_time - start_time}秒")
    return res