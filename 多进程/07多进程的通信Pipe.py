import time
from multiprocessing import Process, Pipe


def add_data(pi: Pipe):
    for i in range(6):
        pi.send(i)
        print(pi.recv()+"-----")
        time.sleep(0.3)


def read_data(pi: Pipe):
    while True:
        value = pi.recv()
        pi.send('收到')
        print(value)
        time.sleep(0.4)

if __name__ == '__main__':
    # 创建一个管道， 需要两个端点
    send_pi, recv_pi = Pipe()

    p1 = Process(target=add_data, args=(send_pi,))  # 往队列中存放数据的进程
    p2 = Process(target=read_data, args=(recv_pi,))  # 从队列中获取数据的进程

    p1.start()
    # p1.join()
    p2.start()
