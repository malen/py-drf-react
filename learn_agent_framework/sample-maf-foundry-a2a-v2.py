import asyncio
import threading
import time

import uvicorn
from agent_framework_a2a import A2AAgent
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

FOUNDER_PORT = 9999
FOUNDER_URL = f"http://localhost:{FOUNDER_PORT}"

load_dotenv()


# --------------------------------------------------------------------
# PART 1: The Founder Agent (runs as an A2A server)
#
# Think of this as a microservice. Other agents can discover it
# via its Agent Card and send it messages over HTTP.
# --------------------------------------------------------------------
def start_founder():
    # ------ A2A SDK imports (the protocol layer) ----
    from a2a.server.request_handlers import DefaultRequestHandler  # Routes A2A requests
    from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
    from a2a.server.tasks import InMemoryTaskStore  # Tracks tasks in memory
    from a2a.types import (  # Metadata about the agent
        AgentCapabilities,
        AgentCard,
        AgentInterface,
    )

    # ------ Microsoft Agent Framework imports (the AI layer) ----
    from agent_framework import Agent  # Core agent class
    from agent_framework.a2a import A2AExecutor  # Bridges MAF agent <-> A2A protocol
    from agent_framework.foundry import FoundryChatClient  # Foundry as the LLM backend
    from starlette.applications import Starlette

    # 1. Create the AI agent with its personality
    agent = Agent(
        client=FoundryChatClient(credential=DefaultAzureCredential()),
        name="Founder Raj",
        instructions=(
            "You are Raj, a hyper-confident startup founder."
            "When given a theme, invent a startup with:"
            "a catchy name, a one-line elevator pitch,"
            "a business model, and a funding ask (e.g. '$2M seed)."
            "Be creative and slightly over-the-top. Keep it under 100 words."
        ),
    )

    # 2. Define the Agent Card - this is how other agents discover you
    card = AgentCard(
        name="Founder Raj",
        description="A startup founder who pitches bold ideas.",
        supported_interfaces=[
            AgentInterface(url=FOUNDER_URL, protocol_binding="JSONRPC")
        ],
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[],
    )

    # 3. Wire it all together: Agent -> A2AExecutor -> RequestHandler -> App
    handler = DefaultRequestHandler(
        agent_executor=A2AExecutor(agent),  # A2AExecutor adapts the MAF Agent for A2A
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )

    server = Starlette(
        routes=[
            *create_agent_card_routes(card),
            *create_jsonrpc_routes(handler, "/"),
        ]
    )

    uvicorn.run(server, host="0.0.0.0", port=FOUNDER_PORT, log_level="warning")


# --------------------------------------------------------------------
# PART 2: The VC Shark Agent (runs as an A2A client)
#
# This agent doesn't need a server - it just calls the Founder
# over A2A, gets the pitch, and reviews it locally.
# --------------------------------------------------------------------
async def run_shark_tank():
    from agent_framework import Agent
    from agent_framework.foundry import FoundryChatClient

    # 1. Create the Shark agent (runs locally, no A2A server needed)
    shark = Agent(
        client=FoundryChatClient(credential=DefaultAzureCredential()),
        name="Shark Priya",
        instructions=(
            "You are Priya, a ruthless but fair VC investor."
            "You will be given a startup pitch. Evaluate it:"
            "- Verdict: FUND or PASS\n"
            "- If FUND: state your offer (amount for equity %)\n"
            "- If PASS: state the fatal flaw\n"
            "- End with a witty one-liner\n"
            "Be sharp and dramatic. Keep it under 80 words."
        ),
    )

    # 2. The theme for our pitch round
    themes = ["Pitch me a cybersecurity startup"]

    # 3. Connect to the Founder's A2A server
    async with A2AAgent(name="Founder Raj", url=FOUNDER_URL) as founder:
        for i, theme in enumerate(themes, 1):
            print(f"\n{'-' * 55}")
            print(f"ROUND {i}")
            print(f"{'-' * 55}")
            print(f"Theme: {theme}")

            # Step A - Send the theme to the Founder via A2A
            founder_response = await founder.run(theme)

            # Extract text from the A2A response messages
            pitch = ""
            for msg in founder_response.messages:
                if msg.text:
                    pitch += msg.text
            print(f"Founder Raj:\n{pitch}\n")

            # Step B - Feed the pitch to the Shark for evaluation
            review = await shark.run(
                f"A founder just pitched you this startup:\n\n{pitch}"
            )
            print(f"Shark Priya:\n{review}")

    print(f"\n{'-' * 55}")
    print("THAT'S A WRAP!")
    print(f"{'-' * 55}")


# --------------------------------------------------------------------
# PART 3: Main - spin up the founder server, then run the show!
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Start the Founder agent in the background
    print(f"Starting Founder Raj's A2A server on port {FOUNDER_PORT}...")
    threading.Thread(target=start_founder, daemon=True).start()

    # Give the server a few seconds to start up
    time.sleep(3)
    print("Founder is up! Now running Shark Priya's agent to review the pitch...\n")

    # Run the async conversation with the Shark agent
    asyncio.run(run_shark_tank())


# VERDICT: PASS.
# “Always-on predictive firewall” for *every endpoint* is vague, expensive,
# and likely non-differentiated—hard to prove low false positives, integration friction is brutal,
# and “predict the next malicious move” is a buzzword unless you’ve got hard benchmarks.
# Also $3.5M seed for an unvalidated model + pilots screams burn.

# 结论（VERDICT）：我决定不投 / 跳过这个项目。
# “为每个终端提供始终在线（always-on）的预测型防火墙（predictive firewall）”这个概念比较模糊、成本高，而且很可能缺乏差异化竞争优势。
# 很难证明它能够保持较低的误报率（false positives），与现有系统的集成阻力（integration friction）也非常大。
# 此外，“预测下一步恶意行为（predict the next malicious move）”这种说法更像是营销术语（buzzword），除非你能拿出扎实的基准测试（hard benchmarks）来证明其效果。
# 再加上，一个尚未验证有效性的模型（unvalidated model）加上试点项目（pilots）就要融资 350 万美元种子轮（$3.5M seed），给人的感觉是资金消耗（burn）会非常快。
