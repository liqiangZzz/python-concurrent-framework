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
    # 同时运行两个协程（多协程并发）
    # await 只能在 async 函数内使用
    await asyncio.gather(task_a(), task_b())


if __name__ == '__main__':
    # 入口必须是单个协程
    asyncio.run(main())

# if __name__ == '__main__':
#     # 创建一个临时协程
#     async def temp():
#         await asyncio.gather(task_a(), task_b())
#
#
#     asyncio.run(temp())