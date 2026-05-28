import multiprocessing
import time
from multiprocessing import Process, Queue

# 加上这一行，强制使用 fork 方式启动（macOS 解决方案）
multiprocessing.set_start_method('fork', force=True)


def add_data(q: Queue):
    for i in range(6):
        q.put(f'数据{i}')
        time.sleep(0.3)


def read_data(q: Queue):
    while True:
        # get函数是一个阻塞的函数，get从队列中获取一个值，并且这个值从队列中删除。
        value = q.get()
        print(value)
        time.sleep(0.4)


if __name__ == '__main__':
    q = Queue(100)
    p1 = Process(target=add_data, args=(q,))  # 往队列中存放数据的进程
    p2 = Process(target=read_data, args=(q,))  # 从队列中获取数据的进程

    p1.start()
    # p1.join()
    p2.start()
