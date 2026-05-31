from agent_framework import Agent, MCPStdioTool
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


async def playwright_mcp_news_agent():
    from agent_framework_foundry import FoundryChatClient

    credential = DefaultAzureCredential()
    client = FoundryChatClient(credential=credential)

    async with MCPStdioTool(
        name="PlaywrightNewsAgent",
        command="npx",
        args=["@playwright/mcp@latest"],
        load_prompts=False,
    ) as mcp_server:
        agent = Agent(
            client=client,
            name="NewsReaderAgent",
            instructions="你是一名乐于助人的助手，像人类一样阅读新闻网站。你可以浏览页面、打开文章，并清晰地总结内容。请注重准确性与表达清晰，并适当使用表情符号（emoji）。",
            tools=[mcp_server],
        )

        result = await agent.run(
            """
            1. 打开 https://www.bbc.com/news 网站。
            2. 提取前三条头条标题。
            3. 每一个总结1-2个要点。
            """
        )
        print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(playwright_mcp_news_agent())
