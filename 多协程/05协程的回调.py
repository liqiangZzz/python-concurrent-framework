import asyncio
import time
from functools import partial


async def eat():
    for i in range(6):
        print('正在吃饭...')
        await asyncio.sleep(0)
    return '吃饭完成'


async def work():
    for i in range(6):
        print('正在做作业...')
        await asyncio.sleep(0)
    return '做作业完成'


# 定义一个回调函数

def my_callback(coro, current_time):
    """
    这个就是协程的异步任务完成之后，自动调用的函数
    :param coro:  当前完成任务的协程对象，不需要手动传输参数
    :param current_time:  当前时间，需要手动传输的参数
    :return:
    """
    print(f'收到了一个参数{current_time}')
    print(f'当前协程的返回值是:{coro.result()}， 协程结束的时间{current_time}')


async def main():  # 其他协程的入口
    task1 = asyncio.create_task(eat())
    task2 = asyncio.create_task(work())

    task1.add_done_callback(partial(my_callback, current_time=time.strftime('%H:%M:%S')))
    # 仅仅得到函数的返回值
    # result = await asyncio.gather(task1, task2, return_exceptions=True)  # 当第一个协程强制终止，会影响第二个协程
    # 得到更加详细的返回信息
    result = await asyncio.wait([task1, task2])
    print(result)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'耗时为:{time.time() - start}')
