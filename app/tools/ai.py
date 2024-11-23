
from openai import AsyncOpenAI


class ai:
    def __init__(self,api_key:str,base_url:str):
        self.ai = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    async def embedding(self,model:str,text:str)->list:
        try:
            embedding = await self.ai.embeddings.create(
                model=model,
                input=text,
            )
            return embedding.data[0].embedding
        except Exception as e:
            print(e)
            return None

async def test():
    key = "7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901"
    url = "https://open.bigmodel.cn/api/paas/v4"
    model = "embedding-3"
    text = "你好"
    aiApi = ai(key,url)
    res = await aiApi.embedding(model,text)
    # 获取对象类型
    print(type(res))
    print(res)
if __name__ == '__main__':
    import asyncio
    asyncio.run(test())