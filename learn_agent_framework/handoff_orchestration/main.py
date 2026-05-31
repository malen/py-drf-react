from agent_framework import AgentResponse, Message
from agent_framework_foundry import FoundryChatClient
from agent_framework_orchestrations import HandoffAgentUserRequest, HandoffBuilder
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

CUSTOMER_PROMPT = "你好，我需要关于我最近订单 #12345 的帮助。产品收到时已经损坏，我想申请更换一个新的产品。"

# 脚本回复，模拟客户和代理之间的对话
SCRIPTED_RESPONSES = [
    "商品到货时已损坏，我希望寄送一个替换商品到同一地址。",
    "好的！你能确认运费不会再次收取吗？",
    "谢谢确认",
]

# 支持协调员：负责接收客户请求，进行初步分类，并将问题分配给相应的代理。
# 账单代理：专门处理与订单、支付和退款相关的问题。
# 技术代理：专门处理与产品使用、故障排除和技术支持相关的问题。
# 主管代理：负责监督整个流程，处理升级问题，并确保客户满意度。
AGENT_CONFIG = {
    "SupportCoordinator": "你是支持协调员，负责接收客户请求，进行初步分类，并将问题分配给相应的代理。",
    "BillingAgent": "你是账单代理，专门处理与订单、支付和退款相关的问题。",
    "TechnicalAgent": "你是技术代理，专门处理与产品使用、故障排除和技术支持相关的问题。",
    "SupervisorAgent": "你是主管代理，负责监督整个流程，处理升级问题，并确保客户满意度。",
}


async def run_handoff_example() -> str:
    credential = DefaultAzureCredential()
    client = FoundryChatClient(credential=credential)

    agents = {
        name: client.as_agent(
            name=name,
            instructions=instructions,
            require_per_service_call_history_persistence=True,  # 每个服务调用都持久化历史记录，便于后续查询和分析
        )
        for name, instructions in AGENT_CONFIG.items()
    }
    # triage, billing, technical, supervisor = agents.values()
    triage = agents["SupportCoordinator"]
    billing = agents["BillingAgent"]
    technical = agents["TechnicalAgent"]
    supervisor = agents["SupervisorAgent"]

    workflow = (
        HandoffBuilder(
            name="af_handoff",
            participants=list(agents.values()),
            termination_condition=lambda state: (
                sum(1 for m in state if m.author_name == "user")
                >= 4  # 终止条件：当客户发出至少4条消息后结束流程
            ),
        )
        .with_start_agent(triage)
        .add_handoff(triage, [billing, technical, supervisor])
        .add_handoff(billing, [technical, triage])
        .add_handoff(technical, [billing, triage])
        .add_handoff(supervisor, [triage])
        .build()
    )

    scripted_iter = iter(SCRIPTED_RESPONSES)
    events = []

    async for e in workflow.run(CUSTOMER_PROMPT, stream=True):
        if e.type == "request_info" and isinstance(e.data, HandoffAgentUserRequest):
            user_reply = next(
                scripted_iter, "谢谢你的帮助，再见！"
            )  # 获取下一个预设回复，或使用默认回复 如果没有更多预设回复了
            # responses = {
            #     e.data.request_id: [Message(role="user", contents=user_reply)]
            # }  # 构造回复消息
            # events = [
            #     e async for e in workflow.run(responses, stream=True)
            # ]  # 继续处理新的事件
            await workflow.run(
                [Message(role="user", contents=user_reply)], stream=False
            )  # 直接发送用户回复，不需要再次迭代事件

    for event in events:
        if event.type == "output" and isinstance(event.data, AgentResponse):
            return "\n".join(
                f"{m.author_name or m.role}: {m.text}"
                for m in event.data.messages
                if m.text and m.text.strip()
            )
    return "没有收到代理的回复。"


async def main():
    print(
        "================ Agent Framework - Handoff Orchestration Example =================\n"
    )
    print(await run_handoff_example() or "没有收到代理的回复。")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
