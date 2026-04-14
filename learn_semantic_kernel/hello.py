import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent

# from semantic_kernel.connectors.ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


async def main():
    # 自动加载 .env 文件
    load_dotenv()
    # 读取变量
    # db_host = os.getenv("DB_HOST")
    # db_port = os.getenv("DB_PORT")
    # api_key = os.getenv("API_KEY")

    # 初始化聊天智能体
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version="2024-02-15-preview",
        ),
        name="SK_Assistant",
        instructions="你是一个有帮助的人工智能助手，协助用户解答问题和提供信息。",  # 智能体的行为指令
    )

    # 获取响应
    response = await agent.get_response("你好，SK！你能介绍一下自己吗？")
    print(response)


asyncio.run(main())
