# 6.2. 错误处理与重试机制


import asyncio

from full_system_architecture import ecommerce_service
from performance_tracking_and_logging import 监控装饰器
from semantic_kernel.exceptions import ServiceResponseException
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class EnhancedAgent:
    def __init__(self, base_agent):
        self.base_agent = base_agent

    # 重试装饰器
    @retry(
        stop=stop_after_attempt(3),  # 最多重试几次（1次正常请求（失败）+3次重试）
        wait=wait_exponential(
            multiplier=1, min=2, max=6
        ),  # 每次等多久重试（指数退避重试：第一次等2秒，第二次4秒，第三次6秒），multiplier是等待时间倍数
        retry=retry_if_exception_type(ServiceResponseException),  # 什么错误才重试
    )
    @监控装饰器.监控性能
    async def get_response_safely(self, message: str):
        """带重试机制的响应获取"""
        print(f"正在处理请求：{message}")
        return await self.base_agent.get_response(message)


async def main():
    # 1. 创建增强型智能体
    enhanced_agent = EnhancedAgent(ecommerce_service)

    # 2. 调用异步方法
    response = await enhanced_agent.get_response_safely("我想查询商品P002的价格和库存")

    print("客服回复：", response)


asyncio.run(main())
