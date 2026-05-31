# Create a sample agent using the Foundry API and Agent Class
import asyncio
from random import randint

from agent_framework import Agent, Message, tool
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


@tool
async def get_weather(city: str) -> str:
    """获取指定城市的天气
    Args:
        city: 要获取天气的城市名字

    Returns:
        一个描述当前城市的天气状况的字符串
    """
    conditions = ["晴朗", "多云", "下雨", "雷暴"]
    return f"{city} 的天气是 {conditions[randint(0, 3)]}, 气温是 {randint(10, 30)}°C。"


async def main():
    with DefaultAzureCredential() as credential:
        # TODO: FoundryChatClient不支持API KEY连接
        client = FoundryChatClient(credential=credential)

        # 用as_agent的写法，client不能复用。只适合快速原型开发
        agent = Agent(
            client=client,
            name="AzureOpenAIAgent",
            description="一个用MAF集成Azure AI的代理",
            instructions="You are a helpful assistant that provides weather information.",  # 指令
            tools=[get_weather],
        )

        user_message = Message(role="user", contents=["巴黎的天气怎么样？"])
        response = await agent.run(user_message)
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
