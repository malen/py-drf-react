# 5. 完整系统架构

from custom_plugin import CustomPlugin
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
)
from semantic_kernel.functions import KernelArguments, kernel_function


# 电商数据库插件
class EcommerceDbPlugin:
    def __init__(self):
        self.订单数据 = {
            "ORD001": {"商品": ["P001", "P002"], "金额": 899.98, "状态": "已发货"},
            "ORD002": {"商品": ["P003"], "金额": 199.99, "状态": "处理中"},
            "ORD003": {"商品": ["P001", "P003"], "金额": 499.98, "状态": "已完成"},
        }

        @kernel_function(name="orderStatusQuery", description="根据订单号查询订单状态")
        def orderStatusQuery(self, OrderID: str) -> str:
            订单 = self.订单数据.get(OrderID)
            if 订单:
                return f"订单{OrderID}：金额{订单['金额']}, 状态：{订单['状态']}"
            return f"没找到订单 {OrderID}"

        @kernel_function(description="查询用户的所有订单")
        def 查询用户订单(self, 用户ID: str) -> str:
            # 模拟用户订单查询
            return "用户订单:\n- ORD001: 已发货\n- ORD003: 已完成"


# 物流查询插件
class PackageTrackingPlugin:
    @kernel_function(name="packageTrackingQuery", description="查询物流信息")
    def packageTrackingQuery(self, OrderID: str) -> str:
        物流信息 = {
            "ORD001": "2024-01-15 已发货，预计1月18日送达",
            "ORD002": "2024-01-16 仓库处理中",
            "ORD003": "2024-01-10 已签收",
        }
        return 物流信息.get(OrderID, "暂无物流信息")


# 创建电商客服系统
ecommerce_service = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="ecommerce_service",
    instructions="你是专业的电商客服助手，帮助用户查询订单，物流，商品信息，处理售后问题",
    plugins=[EcommerceDbPlugin(), PackageTrackingPlugin(), CustomPlugin()],
    arguments=KernelArguments(
        temperature=0.1,
        max_tokens=1000,
    ),
)


async def 测试电商系统():
    测试用例 = [
        "我的订单ORD001现在到哪里了？",
        "我想查询商品P002的价格和库存",
        "用户U2345有哪些订单？",
        "订单ORD002的状态是什么？",
        "推荐一款性价比高的商品",
    ]

    for 用例 in 测试用例:
        print(f"\n用户询问：{用例}")
        响应 = await ecommerce_service.get_response(用例)
        print(f"客服回复：{响应.content}")
        print("-" * 50)


# asyncio.run(测试电商系统())
