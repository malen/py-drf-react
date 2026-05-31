"""
顺序编排示例：一个简单的工作流，包含三个代理：分析师、优化器和审核员。每个代理依次处理输入并将结果传递给下一个代理，最终输出优化后的社交媒体帖子。
"""

from textwrap import dedent

from agent_framework import AgentResponseUpdate, WorkflowBuilder
from dotenv import load_dotenv

load_dotenv()

PROMPT = """
刚完成今天早上的锻炼。能够坚持自己的健身计划，感觉很不错。
到现在已经 3 周了，我能看到一些进步。
还有人在努力保持运动动力吗？
""".strip()


async def main():
    from agent_framework import Agent
    from agent_framework_foundry import FoundryChatClient
    from azure.identity import AzureDeveloperCliCredential

    credential = AzureDeveloperCliCredential()
    client = FoundryChatClient(credential=credential)
    analyzer = Agent(
        client=client,
        name="AnalyzerAgent",
        instructions=dedent("""
            你是一名社交媒体分析师。
            给定一篇社交媒体帖子后，请仅用 3 句话完成分析：
            1. 分析帖子的整体语气。
            2. 指出互动性或参与度方面的不足。
            3. 提供一条最重要的改进建议。

            要求：
            - 简洁明了
            - 每个要点一句话
            - 不要输出额外解释""").strip(),
    )

    optimizer = Agent(
        client=client,
        name="OptimizerAgent",
        instructions=dedent("""
            你是一名社交媒体内容优化专家。
            请重写给定的帖子，以提升用户互动率。

            要求：
            - 保留原意
            - 提高吸引力和可读性
            - 添加合适的表情符号
            - 添加相关话题标签（Hashtags）
            - 增加明确的行动号召（Call-to-Action）
            - 风格自然、适合社交媒体平台

            只输出优化后的帖子，不要添加解释、分析或其他内容。""").strip(),
    )

    reviewer = Agent(
        client=client,
        name="ReviewerAgent",
        instructions=dedent("""
            你是一名社交媒体内容审核与优化专家。

            请对给定帖子进行润色和优化，重点关注：
            - 语法和表达是否自然流畅
            - 话题标签（Hashtags）是否相关且有效
            - 表情符号（Emojis）是否使用得当、不过多也不过少

            要求：
            - 保持原意不变
            - 提升整体可读性和专业性
            - 仅输出最终优化后的帖子

            不要输出解释、分析或任何额外内容。""").strip(),
    )

    # TODO: 未来版本不会自动推断最后的输出，必须明确指定output_from。否则会警告
    workflow = (
        WorkflowBuilder(
            start_executor=analyzer,
            output_from="all",
        )
        .add_edge(analyzer, optimizer)
        .add_edge(optimizer, reviewer)
        .build()
    )

    print("\n=== Agent Framework - Sequential Workflow ===\n")

    last_author: str | None = None

    async for event in workflow.run(PROMPT, stream=True):
        if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                print(f"\n--- {author} ---\n")
                if last_author is not None:
                    print("\n")
                print(f"[{author}]: {update.text}", end="", flush=True)
                last_author = author
            else:
                print(update.text, end="", flush=True)
        else:
            print(f"\n[Event]: {event.type}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
