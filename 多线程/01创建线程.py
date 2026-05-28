# 采用两个线程，累加1 ，一共累加5亿次。
import time
from threading import Thread


def add(n,name):
    start = time.time()
    """
    把1累加多少次
    :param n:
    :return:
    """
    sum = 0
    while sum < n:
        sum += 1
    end = time.time()
    print(f'当前{name}加了{sum}次,用了{end-start}')

if __name__ == '__main__':
    start = time.time()
    n = 500000000

    t1 = Thread(target=add, args=(n/2,'thread-01'), daemon=True)
    t2 = Thread(target=add, args=(n/2,'thread-02'), daemon=True)
    # t1.daemon = True
    t1.start()
    t2.start()

    # t1.join()
    # t2.join()

    # 单线程
    # add(n)
    end = time.time()
    print(f'运行的时间为{end-start}')
