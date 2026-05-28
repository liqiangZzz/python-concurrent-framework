import asyncio
from asyncio import ALL_COMPLETED


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
    task1 = asyncio.create_task(task_a())
    task2 = asyncio.create_task(task_b())
    task1.cancel()
    # 仅仅得到函数的返回值
    result = await asyncio.gather(task1, task2, return_exceptions=True)  # 当第一个协程强制终止，会影响第二个协程
    # result = await asyncio.wait([task1, task2])
    print(result)

if __name__ == '__main__':
    # 入口必须是单个协程
    asyncio.run(main())
