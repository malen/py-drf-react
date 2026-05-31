from collections import defaultdict

from agent_framework import AgentResponse
from agent_framework_orchestrations import ConcurrentBuilder
from dotenv import load_dotenv

load_dotenv()

PROMPT = "巴黎旅行建议"

MAX_OUTPUT_RULE = "\n".join(
    [
        "回答尽量简短。",
        "列出两条简短的要点。",
        "每条要点不超过15个字。",
        "不要添加补充说明。",
    ]
)


def print_agent_block(agent_name: str, text: str) -> None:
    print(f"\n{'=' * 20} {agent_name} {'=' * 20}")
    print(text.strip())
    print(f"{'=' * 50}\n")


def print_agent_report(agent_outputs: dict[str, list[str]]) -> None:
    sections = {
        "Food & Dining": "FoodExpert",
        "Accommodation": "AccommodationExpert",
        "Activities": "ActivitiesExpert",
        "Transport": "TransportExpert",
        "Budget": "BudgetExpert",
    }

    print("\n\n" + "#" * 50)
    print("Final Travel Plan Report")
    print("#" * 50 + "\n")

    for section_title, agent_name in sections.items():
        outputs = "\n".join(agent_outputs.get(agent_name, [])).strip()
        if not outputs:
            continue

        print(f"\n{'#' * 10} {section_title} {'#' * 10}\n")
        print(outputs)

    print("\nReport generated from concurrent agent outputs\n")


async def main():

    from agent_framework import Agent
    from agent_framework_foundry import FoundryChatClient

    # ------ Microsoft Agent Framework imports (the AI layer) ----
    from azure.identity import DefaultAzureCredential  # Azure authentication

    credential = DefaultAzureCredential()
    client = FoundryChatClient(credential=credential)

    food_agent = Agent(
        client=client,
        name="FoodExpert",
        instructions=f"你是一个美食专家，专门为旅行者推荐目的地的餐饮选择。{MAX_OUTPUT_RULE}",
    )
    accommodation_agent = Agent(
        client=client,
        name="AccommodationExpert",
        instructions=f"你是一个住宿专家，专门为旅行者推荐目的地的住宿选择。{MAX_OUTPUT_RULE}",
    )
    activities_agent = Agent(
        client=client,
        name="ActivitiesExpert",
        instructions=f"你是一个活动专家，专门为旅行者推荐目的地的活动和景点。{MAX_OUTPUT_RULE}",
    )
    transport_agent = Agent(
        client=client,
        name="TransportExpert",
        instructions=f"你是一个交通专家，专门为旅行者推荐目的地的交通方式。{MAX_OUTPUT_RULE}",
    )
    budget_agent = Agent(
        client=client,
        name="BudgetExpert",
        instructions=f"你是一个预算专家，专门为旅行者制定合理的旅行预算。{MAX_OUTPUT_RULE}",
    )

    workflow = ConcurrentBuilder(
        participants=[
            food_agent,
            accommodation_agent,
            activities_agent,
            transport_agent,
            budget_agent,
        ],
    ).build()

    print("Running concurrent agent orchestration...")
    print(f"Prompt: {PROMPT}\n")

    agent_outputs: dict[str, list[str]] = defaultdict(list)

    async for event in workflow.run(PROMPT, stream=True):
        if event.type == "output" and isinstance(event.data, AgentResponse):
            messages = event.data.messages
            for message in messages:
                if not message.text:
                    continue
                agent_name = message.author_name or "UnknownAgent"
                if agent_name == "user":
                    continue
                agent_outputs[agent_name].append(message.text)

    if not agent_outputs:
        print("No agent outputs received.")
        return

    print("\n INDIVIDUAL AGENT OUTPUTS:")
    for agent_name in [
        "FoodExpert",
        "AccommodationExpert",
        "ActivitiesExpert",
        "TransportExpert",
        "BudgetExpert",
    ]:
        if agent_name in agent_outputs:
            text = "\n".join(agent_outputs[agent_name]).strip()
            print_agent_block(agent_name, text)

    print_agent_report(agent_outputs)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
