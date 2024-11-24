
from openai import AsyncOpenAI


class ai:
    def __init__(self,api_key:str,base_url:str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    async def embedding(self,model:str,text:str)->list:
        try:
            embedding = await self.client.embeddings.create(
                model=model,
                input=text,
            )
            return embedding.data[0].embedding
        except Exception as e:
            print(e)
            return None
    async def chat(self,model:str,messages:str,stream:bool=False)->list:
        try:
            res = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                stream = stream,
            )
            if stream:
                async for chunk in res:
                    '''
ChatCompletionChunk(id='20241124155243734b4ca3e3af48ae', choices=[Choice(delta=ChoiceDelta(content='', function_call=None, refusal=None, role='assistant', tool_calls=None), finish_reason='stop', index=0, logprobs=None)], created=1732434763, model='glm-4-flash', object=None, service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=50, prompt_tokens=9, total_tokens=59, completion_tokens_details=None, prompt_tokens_details=None))
                    '''
                    # print(chunk.choices[0].delta.content or "", end="")
                    print(chunk)
            else:
                return res.choices[0].message.content
        except Exception as e:
            print(e)
            return None

async def test():
    key = "7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901"
    url = "https://open.bigmodel.cn/api/paas/v4"
    aiApi = ai(key,url)
    #测试embedding
    # model = "embedding-3"
    # text = "你好"
    # res = await aiApi.embedding(model,text)
    # print(type(res))
    # print(res)
    # 测试chat
    model = "glm-4-flash"
    msg = [
        {"role": "user", "content": "你好,中山大学在哪里"},
    ]
    res = await aiApi.chat(model,msg,True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(test())