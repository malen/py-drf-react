from agent_framework import Agent, Content, Message
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


async def main():
    with open("a2a.png", "rb") as f:
        image_bytes = f.read()

    with DefaultAzureCredential() as credential:
        client = FoundryChatClient(credential=credential)

        agent = Agent(
            client=client,
            name="ImageAnalyzer",
            description="An assistant that analyzes images and provides descriptions.",
            instructions="You are an assistant that analyzes images and provides descriptions.",
        )

        # message = Message(
        #     role="user", contents=[image_bytes], content_type="image/jpeg"
        # )
        message = Message(
            role="user",
            contents=[
                Content.from_data(data=image_bytes, media_type="image/png"),
                Content.from_text("请分析这张图片，描述一下你都看到了什么？"),
            ],
        )

        response = await agent.run(message)
        print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
