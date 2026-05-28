# 第五节：Python中的多线程

讲师：肖斌

# 一、线程的相关概念

在Python中，想要实现多任务除了使用进程，还可以使用线程来完成，线程是实现多任务的另外一种方式。

## 1、什么是线程

线程是进程中执行代码的一个分支，每个执行分支（线程）要想工作执行代码需要cpu进行调度 ，也就是说线程是cpu调度的基本单位，每个进程至少都有一个线程，而这个线程就是我们通常说的主线程。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTYzY2NiN2JhYzlkYmFkNTk5Y2Q5NTUxYTUxNDUyYTVfMmZkODY0Y2EwYjIzZTJjYmY3ZTczNjk4MmRjNmRjNDRfSUQ6NzI5NDA4MTQ2ODE2OTk3Nzg1OV8xNzc5OTc2NzQxOjE3ODAwNjMxNDFfVjM)

## 2、GIL:全局解释器锁

首先需要明确的一点是GIL并不是Python的特性，它是在实现Python解析器\(CPython\)时所引入的一个概念。



**GIL****全称****global interpreter lock****，****全局解释器锁****。**



每个线程在执行的时候都需要先获取GIL，保证同一时刻只有一个线程可以执行代码，即同一时刻只有一个线程使用CPU。在CPython中，每一个Python线程执行前都需要去获得GIL锁 ，获得该锁的线程才可以执行，没有获得的只能等待 ，当具有GIL锁的线程运行完成后，其他等待的线程就会去争夺GIL锁，这就造成了，在Python中使用多线程，但同一时刻下依旧只有一个线程在运行 ，所以Python多线程其实并不是「**并行**」的，而是「**并发**」 。



看到下图，图中是Python中GIL的工作实例，其中有3个线程，线程与线程之间是顺序执行的 ，每个线程开始执行时都会去获得GIL，防止其他线程线程运行 ，每执行完一段时间后，就会释放GIL，让别的线程可以去争夺执行权限，如果自己本身也没有执行完，则本身也会参与这次争夺 。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDgxMzBkZjExM2RhNzNkYzU1NjFiMTBkZDE2ZDAwYTVfM2QxZGE5NTczOWFkYWZhYzcyMjNiZDFkYTlmZWM5MGRfSUQ6NzI5NDA4MTc3NDc1NzM4MDA5OV8xNzc5OTc2NzQxOjE3ODAwNjMxNDFfVjM)

# 二、创建线程

## 1、直接使用**Thread类**

Thread\(\[group \[, target \[, name \[, args \[, kwargs\]\]\]\]\]\)

- group: 线程组，目前只能使用None

- target: 执行的目标任务名

- args: 以元组的方式给执行任务传参

- kwargs: 以字典方式给执行任务传参

- name: 线程名，一般不用设置

```Python
# 多线程的代码
import threading, time


def add(n):
    sum = 0
    while sum < n:
        sum += 1
    print(f'sum:{sum}')


if __name__ == '__main__':
    start = time.time()
    n = 500000000
    t1 = threading.Thread(target=add, args=[n / 2])
    t2 = threading.Thread(target=add, args=[n / 2])
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('run time: %s' % str(time.time() - start))

```

**注意：即使存在****GIL**** 在有****IO****等待操作的程序中,还是****多线程****快。**

## 2、设置守护线程

线程是程序执行的最小单位，Python在进程启动起来后，会自动创建一个主线程，之后使用多线程机制可以在此基础上进行分支，产生新的子线程。子线程启动起来后，主线程默认会等待所有线程执行完成之后再退出。但是我们可以将子线程设置为守护线程，此时主线程任务一旦完成，所有子线程将会和主线程一起结束（就算子线程没有执行完也会退出）

守护线程可以在线程启动之前，通过t1\.daemon = True的形式进行设置，或者在创建子线程对象时，以参数的形式指定：

```Python
#第一种
t1 = threading.Thread(target=add, args=[n / 2], daemon=True)

#第二种
t1 = threading.Thread(target=add, args=[n / 2])
t1.daemon = True
```

## 3、继承Thread类

```Python
import threading

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
        # 线程执行的函数
        print("Thread " + self.name + " is running")

# 创建新线程
thread1 = MyThread("1")
thread2 = MyThread("2")

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()


```



# 三、线程安全

线程之间可以共享全局变量。当多个线程同时访问一个对象时，不管如何计算，如果调用这个对象的行为都可以获得正确的结果，那就称这个对象时线程安全的。 如果出现了“脏数据”。则线程不安全。



**脏数据** ：产生脏数据的原因是，当一个线程在对数据进行修改时，修改到一半时另一个线程读取了未经修改的数据并进行修改。如何避免脏数据的产生呢？一个办法就是用join方法，即先让一个线程执行完毕再执行另一个线程。但这样的本质是把多线程变成了单线程，失去了多线程的意义。另一个办法就是用**锁。**

```Python
import threading

# 定义全局变量
g_num = 0


# 循环一次给全局变量加1
def sum_num1():
    for i in range(1000000):
        global g_num
        g_num += 1

    print("sum1:", g_num)


# 循环一次给全局变量加1
def sum_num2():
    for i in range(1000000):
        global g_num
        g_num += 1
    print("sum2:", g_num)


if __name__ == '__main__':
    # 创建两个线程
    first_thread = threading.Thread(target=sum_num1)
    second_thread = threading.Thread(target=sum_num2)

    # 启动线程
    first_thread.start()
    # 启动线程
    second_thread.start()
```

**全局变量数据错误的解决办法:**

线程同步: 保证同一时刻只能有一个线程去操作全局变量 同步: 就是协同步调，按预定的先后次序进行运行。如:你说完，我再说, 好比现实生活中的对讲机

线程同步的方式:

1. **线程等待\(join\)**

2. **互斥锁**

# 四、互斥锁

## 1、同步锁和互斥锁

互斥锁: 对共享数据进行锁定，保证同一时刻只能有一个线程去操作。 也叫：同步锁。

互斥锁是**多个线程一起去抢**，抢到锁的线程先执行，没有抢到锁的线程需要等待，等互斥锁使用完释放后，其它等待的线程再去抢这个锁。

threading模块中定义了Lock变量，这个变量本质上是一个函数，通过调用这个函数可以获取一把互斥锁。

```Python
# 创建锁
lo = threading.Lock()

# 上锁
lo.acquire()

...这里编写代码能保证同一时刻只能有一个线程去操作, 对共享数据进行锁定...

# 释放锁
lo.release()
```

## 2、死锁的问题

死锁: 一直等待对方释放锁的情景就是死锁。会造成应用程序的停止响应，不能再处理其它任务了。

需求：根据下标在列表中取值, 保证同一时刻只能有一个线程去取值。

```Python
import threading
import time

# 创建互斥锁
lock = threading.Lock()


# 根据下标去取值， 保证同一时刻只能有一个线程去取值
def get_value(index):
    # 上锁
    lock.acquire()
    print(threading.current_thread())
    my_list = [3, 6, 8, 1]
    # 判断下标释放越界
    if index >= len(my_list):
        print("下标越界:", index)
        return
    value = my_list[index]
    print(value)
    time.sleep(0.2)
    # 释放锁
    lock.release()


if __name__ == '__main__':
    # 模拟大量线程去执行取值操作
    for i in range(30):
        sub_thread = threading.Thread(target=get_value, args=(i,))
        sub_thread.start()
```

**死锁****的解决办法： 在合适的地方释放锁**

```Python
# 根据下标去取值， 保证同一时刻只能有一个线程去取值def get_value(index):# 上锁
    lock.acquire()
    print(threading.current_thread())
    my_list = [3,6,8,1]
    if index >= len(my_list):
        print("下标越界:", index)
        # 当下标越界需要释放锁，让后面的线程还可以取值
        lock.release()
        return
    value = my_list[index]
    print(value)
    time.sleep(0.2)
    # 释放锁
    lock.release()
```



# 五、进程和线程的总结

## 1、定义

1. 线程是依附在进程里面的，没有进程就没有线程。

2. 一个进程默认提供一条线程，进程可以创建多个线程。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjZlNDE5NjVhMjFkZGM1NjdkZGNjYjMyMjBkNWY2ZDFfNzIyZGNmNGJjNWJjNTE4NzExZTcwMDc0MTI2ZjMwNWZfSUQ6NzI5NDA5OTk0NTkyMDY1OTQ1OV8xNzc5OTc2NzQxOjE3ODAwNjMxNDFfVjM)

## 2、区别

1. 进程之间不共享全局变量

2. 线程之间共享全局变量，但是要注意资源竞争的问题，解决办法: 互斥锁或者线程同步

3. 创建进程的资源开销要比创建线程的资源开销要大

4. 进程是操作系统资源分配的基本单位，线程是CPU调度的基本单位

5. 线程不能够独立执行，必须依存在进程中

6. 多进程开发比单进程多线程开发稳定性要强



## 3、优缺点

- 进程优缺点:

    - 优点：可以用多核

    - 缺点：资源开销大

- 线程优缺点:

    - 优点：资源开销小

    - 缺点：不能使用多核

