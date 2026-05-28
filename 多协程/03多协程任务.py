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


async def main():
    # create_task = 启动 （并发执行的核心方法）
    # await = 等待完成
    task1 = asyncio.create_task(task_a())
    task2 = asyncio.create_task(task_b())

    await task1
    await task2

    # 等于上边
    # await asyncio.gather(task_a(), task_b())


if __name__ == '__main__':
    # 入口必须是单个协程
    asyncio.run(main())
