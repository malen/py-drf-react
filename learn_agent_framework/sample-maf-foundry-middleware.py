from typing import Awaitable, Callable

from agent_framework import Agent, AgentContext, AgentMiddleware
from agent_framework_foundry import FoundryChatClient
from dotenv import load_dotenv

load_dotenv()


class SecurityMiddleware(AgentMiddleware):
    def __init__(self):
        super().__init__()

    async def process(
        self,
        context: AgentContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        user_input = context.messages[-1].text
        banned_words = ["hack", "password", "secret"]

        if any(word in user_input.lower() for word in banned_words):
            raise ValueError(
                "Input contains banned words. Please rephrase your request."
            )

        print(f"[SECURITY] Input: {user_input} passed security check.")

        result = await call_next()
        print(f"[SECURITY] Response sent: {result}")


async def main():
    # 这里的示例展示了如何在MAF Foundry Agent中集成一个安全检查中间件。
    # 这个SecurityMiddleware会检查用户输入中是否包含敏感词，如果包含则拒绝执行工具调用。
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()
    agent = Agent(
        client=FoundryChatClient(credential=credential),
        name="SecureAgent",
        description="A secure assistant that ensures safety in all interactions.",
        instructions="You are a helpful assistant that provides information while ensuring security.",
        middleware=[SecurityMiddleware()],
    )

    try:
        user_input = input("请输入您的请求：")
        result = await agent.run(user_input)
        print(f"Agent Response: {getattr(result, 'text', str(result))}")
    except ValueError as e:
        print(f"Security Alert: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
