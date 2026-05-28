import time
from multiprocessing import Process, Manager, Semaphore


def add_data(shared_list, sem_can_read, sem_can_write):
    """
    发送端：利用信号量提醒接收端有新数据
    """
    for i in range(6):
        # 1. 一个阻塞方法
        sem_can_write.acquire()

        # 2. 往共享列表存数据
        shared_list.append(i)
        print(f"发送端存入了: {i}")

        # 3. 释放“读”信号，通知接收端：数据准备好了
        sem_can_read.release()

        time.sleep(0.3)


def read_data(shared_list, sem_can_read, sem_can_write):
    """
    接收端：等待信号量，收到信号后再去列表取数据
    """
    while True:
        # 1. 阻塞等待：如果没有读信号（计数器为0），就一直停在这里
        sem_can_read.acquire()

        # 2. 从共享列表取数据
        if len(shared_list) > 0:
            value = shared_list.pop(0)
            print(f"接收端取出了: {value}")

        # 3. 释放“写”信号，通知发送端：可以继续存了
        sem_can_write.release()


if __name__ == '__main__':
    with Manager() as manager:
        # 创建一个共享列表存储数据
        shared_data = manager.list()

        # 创建两个信号量
        # sem_can_read: 初始为0，表示一开始没数据可读
        # sem_can_write: 初始为1，表示允许存入数据
        can_read = Semaphore(0)
        can_write = Semaphore(1)

        p1 = Process(target=add_data, args=(shared_data, can_read, can_write))
        p2 = Process(target=read_data, args=(shared_data, can_read, can_write))

        p2.daemon = True
        p1.start()
        p2.start()

        p1.join()
        print("主进程结束")