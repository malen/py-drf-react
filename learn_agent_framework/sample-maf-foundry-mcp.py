# Create a sample agent using the Foundry API and Agent Class
import asyncio
import warnings

from agent_framework import Agent, MCPStdioTool
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()


async def main():
    with DefaultAzureCredential() as credential:
        # TODO: FoundryChatClient不支持API KEY连接
        client = FoundryChatClient(credential=credential)

        # 为了mcp server正常工作，需要事前通过az login 登录
        azure_mcp = MCPStdioTool(
            name="Azure MCP Server",
            command="npx",
            args=["-y", "@azure/mcp@latest", "server", "start"],
            load_prompts=False,
        )

        async with (
            azure_mcp,
            Agent(
                client=client,
                name="AzureOpsAgent",
                instructions=(
                    "You are an Azure operations assistant."
                    "Use the Azure MCP tools to answer questions about "
                    "the user's Azure subscription and resources."
                    "Always show output in a nice table"
                ),
                tools=[azure_mcp],
            ) as agent,
        ):
            result = await agent.run("List all resource groups in my subscription.")
            print(f"Agent: {result}")

            result = await agent.run("What storage accounts exists?")
            print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
