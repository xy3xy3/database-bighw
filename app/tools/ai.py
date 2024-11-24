from openai import AsyncOpenAI

from openai import AsyncOpenAI

class ai:
    def __init__(self, api_key: str, base_url: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def embedding(self, model: str, text: str) -> list:
        """生成文本嵌入"""
        try:
            embedding = await self.client.embeddings.create(
                model=model,
                input=text,
            )
            return embedding.data[0].embedding
        except Exception as e:
            print(e)
            return None

    async def chat(self, model: str, messages: list, stream: bool = False):
        """聊天方法，兼容 OpenAI 风格的 API"""
        try:
            res = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                stream=stream,
            )

            if stream:
                # 返回一个异步生成器
                async def stream_responses():
                    async for chunk in res:
                        try:
                            # 检查 delta 是否为对象或者字典
                            delta = getattr(chunk.choices[0].delta, 'content', '') if hasattr(chunk.choices[0].delta, 'content') else ''
                            if delta:  # 如果有新内容，返回
                                yield delta
                        except Exception as e:
                            print(f"Error processing chunk: {e}")
                            continue


                return stream_responses()
            else:
                # 提取非流式返回的内容
                return res.choices[0].message.content
        except Exception as e:
            print(f"Error during chat: {e}")
            return None


# 测试代码，确保兼容性
async def test():
    key = "7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901"
    url = "https://open.bigmodel.cn/api/paas/v4"
    aiApi = ai(key, url)

    # 测试 embedding
    # model = "embedding-3"
    # text = "你好"
    # res = await aiApi.embedding(model, text)
    # print(type(res))
    # print(res)

    # 测试 chat
    model = "glm-4-flash"
    msg = [
        {"role": "user", "content": "你好,中山大学在哪里"},
    ]
    print("非流式返回结果：")
    res = await aiApi.chat(model, msg, stream=False)
    print(res)

    print("\n流式返回结果：")
    async for chunk in aiApi.chat(model, msg, stream=True):
        print(chunk, end="")

if __name__ == '__main__':
    import asyncio
    asyncio.run(test())
