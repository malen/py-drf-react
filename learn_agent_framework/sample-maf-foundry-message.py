# Create a sample agent using the Foundry API and Agent Class
import asyncio

from agent_framework import Agent, Message, tool
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureDeveloperCliCredential
from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:

    return f"{city} sunny"


async def main():
    # 需要事前安装azd 命令，并通过azd auth login登录成功。
    credential = AzureDeveloperCliCredential()

    # TODO: FoundryChatClient不支持API KEY连接
    client = FoundryChatClient(credential=credential)

    # 用as_agent的写法，client不能复用。只适合快速原型开发
    agent = Agent(
        client=client,
        name="AzureOpenAIAgent",
        instructions="You are a helpful assistant that provides weather information.",  # 指令
        tools=[get_weather],
    )

    user_message = Message(role="user", contents=["天巴黎的天气怎么样？"])
    response = await agent.run(user_message)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
