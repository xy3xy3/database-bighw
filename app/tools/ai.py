import logging
import re
from openai import AsyncOpenAI
from jsonHelper import try_parse_json_object  # 引入 try_parse_json_object

class ai:
    def __init__(self, api_key: str, base_url: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def extract_json(self, model: str, system_prompt: str, user_prompt: str) -> dict:
        """
        使用 AI 模型提取 JSON 对象。

        :param model: 模型名称
        :param system_prompt: 系统提示内容
        :param user_prompt: 用户提示内容
        :return: JSON 对象或 None
        """
        try:
            # 包装消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # 调用 OpenAI 接口
            response = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                stream=False,
            )

            # 提取内容
            content = response.choices[0].message.content
            # 使用正则匹配 JSON 格式内容
            pattern = re.compile(r"```(?:json\\s+)?(.*?)```", re.DOTALL)
            match = pattern.search(content)

            if match:
                json_str = match.group(1).strip()
                # 调用 try_parse_json_object 解析 JSON
            else:
                json_str = content
            
            json_info, json_obj = try_parse_json_object(json_str)
            if json_obj:  # 如果解析成功
                return json_obj
            else:
                logging.warning(f"解析 JSON 失败: {json_info}")
                return None

        except Exception as e:
            logging.error(f"Error during JSON extraction: {e}")
            return None

# 测试代码
async def test():
    key = "7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901"
    url = "https://open.bigmodel.cn/api/paas/v4"
    aiApi = ai(key, url)

    model = "glm-4-flash"
    system_prompt = """用户会输入很多关于中山大学的问题，请帮忙扩展问题到1-3个，便于知识库搜索。如果用户消息带有历史记录，你需要帮忙做指代消除。
EXAMPLE INPUT: 
中山大学在哪
EXAMPLE JSON OUTPUT:
[
    {
        "question": "中山大学地理位置"
    },
    {
        "question": "怎么去中山大学"
    },
    {
        "question": "中山大学往哪走"
    }
]
EXAMPLE INPUT: 
history:
中山大学校长是谁
output:
是高松
current:
他年级多大
EXAMPLE JSON OUTPUT:
[
    {
        "question": "中山大学校长年级多大"
    },
    {
        "question": "高松年级多大"
    }
]

"""
    user_prompt = """录取多少分"""

    result = await aiApi.extract_json(model, system_prompt, user_prompt)
    print("提取的 JSON 对象:", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
