from threading import Thread

g_num = 0


#  需求：采用两个线程，分别对g_num累加100万次

def sum_num1():
    for i in range(1000000):
        global g_num
        g_num += 1
    print(f'线程1累加之后的结果{g_num}')


def sum_num2():
    for i in range(1000000):
        global g_num
        g_num += 1
    print(f'线程2累加之后的结果{g_num}')


if __name__ == '__main__':
    t1 = Thread(target=sum_num1)
    t2 = Thread(target=sum_num2)

    t1.start()
    # t1.join() # 或者需要互斥锁
    t2.start()
