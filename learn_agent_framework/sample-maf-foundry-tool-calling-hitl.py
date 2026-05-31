# 演示HITL workflow （Human-In-The-Loop Workflow）中，人工干预agent执行流程的能力。
# 这个示例中，我们创建了一个简单的天气查询工具，并在agent执行过程中模拟了一个人工干预的场景：当用户询问某个城市的天气时，
# agent会调用工具获取天气信息，但在返回结果之前，
# 人工干预者会有机会修改工具的输出，以展示HITL的效果。
import asyncio
from random import randint
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


# 在这个示例中，我们使用了approval_mode="always_require"来模拟HITL场景。
# 这意味着每次工具被调用时，都会触发一个人工审批流程，审批者可以选择修改工具的输出结果。
@tool(approval_mode="always_require")
async def get_weather(city: Annotated[str, "要获取天气的城市名字"]) -> str:
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

        session = agent.create_session()
        user_input = input("请输入要查询天气的城市名称：")
        result = await agent.run(user_input, session=session)

        # 模拟人工干预：在工具调用后，人工审批者可以修改工具的输出结果
        print("\n工具调用完成，等待人工审批...")
        while result.user_input_requests:
            for request in result.user_input_requests:
                print(
                    f"Approval needed for: {request.function_call.name} with input {request.function_call.arguments}"
                )

                approval = input("是否批准工具调用？(y/n)：")
                # 模拟修改工具输出的场景：审批者可以选择修改工具的输出结果
                approval_response = request.to_function_approval_response(
                    approved=(approval.lower() == "y"),
                )

                result = await agent.run(approval_response, session=session)

        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
