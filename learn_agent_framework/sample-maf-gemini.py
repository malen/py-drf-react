# Create a sample agent using the Gemini API
import asyncio

from agent_framework import tool
from agent_framework_gemini import GeminiChatClient
from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:

    return f"{city} sunny"


async def main():
    agent = GeminiChatClient().as_agent(tools=[get_weather])
    response = await agent.run("今天巴黎的天气怎么样？")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
