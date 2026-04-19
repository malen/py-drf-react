# 6.3. 性能监控与日志记录

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SemanticKernel")


class 监控装饰器:
    @staticmethod
    def 监控性能(func):
        async def 包装函数(*args, **kwargs):
            开始时间 = datetime.now()
            try:
                结果 = await func(*args, **kwargs)
                耗时 = (datetime.now() - 开始时间).total_seconds()
                logger.info(f"{func.__name__} 执行成功，耗时：{耗时:.2f}s")
                return 结果
            except Exception as e:
                耗时 = (datetime.now() - 开始时间).total_seconds()
                logger.error(
                    f"{func.__name__} 执行失败，耗时：{耗时:.2f}s, 错误：{str(e)}"
                )
                raise

        return 包装函数

    @staticmethod
    def 追踪请求(func):
        async def 包装函数(*args, **kwargs):
            print(f"→ 开始请求: {func.__name__}")
            print(f"  参数: {kwargs}")
            结果 = await func(*args, **kwargs)
            print(f"← 请求完成: {func.__name__}")
            print(f"  结果: {结果.content[:100]}...")
            return 结果

        return 包装函数
