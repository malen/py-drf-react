# 3. 创建自定义插件

from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.functions import KernelArguments, kernel_function

# 自动加载 .env 文件
load_dotenv()


# 1.插件定义
class CustomPlugin:
    @kernel_function(name="query_product_stock", description="查询商品库存信息")
    def query_product_stock(
        self, product_id: Annotated[str, "商品编号"]
    ) -> Annotated[str, "库存数量"]:
        # 这里可以连接数据库或API
        库存数据 = {"P001": 50, "P002": 120, "P003": 0}

        return f"商品{product_id} 库不能：{库存数据.get(product_id, 0)}件"

    @kernel_function(name="query_product_price", description="获取商品价格")
    def query_product_price(
        self, product_id: Annotated[str, "商品编号"]
    ) -> Annotated[str, "商品价格"]:
        价格数据 = {"P001": 299.99, "P002": 599.99, "P003": 199.99}

        return f"商品{product_id} 价格：{价格数据.get(product_id, 0)}"


# 结构化输出模型，必须用英文字段名
# class 订单信息(BaseModel):
#     订单号: str
#     商品列表: list[str]
#     总金额: float
#     状态: str
class OrderInfo(BaseModel):
    order_id: str
    product_list: list[str]
    total_amount: float
    status: str


# 2.使用插件
async def 使用电商插件():
    # 配置结构化输出
    settings = OpenAIChatPromptExecutionSettings()
    settings.response_format = OrderInfo

    # 创建带插件的智能体
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="ecommerce_service",
        instructions="你是专业的电商客服助手，帮助用户查询商品信息和处理订单",
        plugins=[CustomPlugin()],
        arguments=KernelArguments(settings),
    )

    # 查询商品信息
    response = await agent.get_response("查询商品P001的库存和价格")
    print(response.content)

    # 处理订单查询
    order_response = await agent.get_response("生成一个包含P001和P002的测试订单")
    print(order_response.content)


# asyncio.run(使用电商插件())
