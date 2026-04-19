# 4. 构建专业智能体团队

import asyncio

from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# 自动加载 .env 文件
load_dotenv()

# 客服智能体
customer_care_agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="customer_care",
    instructions="处理客户咨询、订单查询、售后服务等客户服务问题",
)


# 技术支持智能体
tech_support_agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="tech_support",
    instructions="解决技术问题、产品使用指导、故障排查等技术支持工作",
)

# 销售智能体
sales_advisor_agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="sales_advisor",
    instructions="产品推荐、价格咨询、促销活动介绍等销售相关工作",
)

# 总调度智能体
总调度智能体 = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="intelligent_scheduler",
    instructions="分析用户问题并分发给合适的专业智能体处理，最后汇总结果给用户",
    plugins=[customer_care_agent, tech_support_agent, sales_advisor_agent],
)


async def 多智能体协作示例():
    print("欢迎使用智能客服系统！请输入‘退出’结束对话")

    while True:
        用户输入 = input("用户:> ")

        if 用户输入.lower() == "退出":
            break

        响应 = await 总调度智能体.get_response(用户输入)
        print(f"客服:> {响应.content}")


asyncio.run(多智能体协作示例())
