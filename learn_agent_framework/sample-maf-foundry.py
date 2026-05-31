# Create a sample agent using the Foundry API
import asyncio

from agent_framework import tool
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
    agent = FoundryChatClient(
        credential=credential
    ).as_agent(
        name="AzureOpenAIAgent",
        instructions="You are a helpful assistant that provides weather information.",  # 指令
        tools=[get_weather],
    )
    response = await agent.run("今天巴黎的天气怎么样？")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
