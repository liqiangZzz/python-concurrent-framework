import time
from multiprocessing import Process


# 吃饭任务
def eat():
    for i in range(6):
        print('正在吃饭...')
        time.sleep(0.3)


# 做作业任务
def work():
    for i in range(6):
        print('正在做作业...')
        time.sleep(0.3)


if __name__ == '__main__':
    # 创建一个子进程, 每个任务由一个独立的子进程来完成
    p1 = Process(target=eat)
    p2 = Process(target=work)

    p1.start()
    p2.start()