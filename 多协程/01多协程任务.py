import asyncio

async def task_a():
    """协程A"""
    for i in range(3):
        print(f"任务A: 第{i + 1}次")
        await asyncio.sleep(0.5)  # 模拟等待，主动让出控制权


async def task_b():
    """协程B"""
    for i in range(3):
        print(f"任务B: 第{i + 1}次")
        await asyncio.sleep(0.5)  # 模拟等待，主动让出控制权


async def main():  # 其他协程的入口

    # 使用 asyncio.gather()并发执行（真正的多协程）
    await task_a()
    await task_a()


if __name__ == '__main__':
    asyncio.run(main())
