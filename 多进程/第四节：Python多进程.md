# 第四节：Python多进程

讲师：肖斌

# 一、多任务的概念

多任务是指在**同一时间内**执行**多个任务**，例如: 现在电脑安装的操作系统都是多任务操作系统，可以同时运行着多个软件。有以下两种执行方式：

- **并发**

- **并行**

**并发:**

在一段时间内**交替**去执行任务。

**例如:**

对于单核cpu处理多任务,操作系统轮流**让各个软件交替执行**，假如:软件1执行0\.01秒，切换到软件2，软件2执行0\.01秒，再切换到软件3，执行0\.01秒……这样反复执行下去。表面上看，每个软件都是交替执行的，但是，由于CPU的执行速度实在是太快了，我们感觉就像这些软件都在同时执行一样，这里需要注意单核cpu是并发的执行多任务的。

**并行****:**

对于多核cpu处理多任务，操作系统会给cpu的每个内核安排一个执行的软件，**多个内核是真正的一起执行软件**。这里需要注意**多核cpu是****并行****的执行多任务，始终有多个软件一起执行**。



## 1、进程和线程的定义

**进程**（Process），顾名思义，就是进行中的程序。进程是python中最小的资源分配单元，进程之间的数据，内存是不共享的，每启动一个进程，都要独立分配资源和拷贝访问的数据，所以进程的启动和销毁的代价是比较大。



Python中的多线程无法利用多核优势，如果想要充分地使用多核CPU的资源，在python中大部分情况需要使用多进程。



**线程**是操作系统能够进行运算调度的最小单位，它被包含在进程之中，是进程中的实际运作单位，一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并发执行不同的任务。 在同一个进程内的线程的数据是可以进行互相访问的，这点区别于多进程。



一个进程至少要包含一个线程，每个进程在启动的时候就会自动的启动一个线程，进程里面的第一个线程就是主线程，每次在进程内创建的子线程都是由主线程进程创建和销毁，子线程也可以由主线程创建出来的线程创建和销毁线程。



**进程与线程的区别**

1. 线程是执行的指令集，进程是资源的集合；

2. 一个程序中默认有一个 主进程 ,一个进程中默认有一个主线程

3. 线程的启动速度要比进程的启动速度要快；

4. 一个新的线程很容易被创建，一个新的进程创建需要对父进程进行一次克隆；

5. 线程共享创建它的进程的内存空间，进程的内存是独立的。

6. 两个线程共享的数据都是同一份数据，两个子进程的数据不是共享的，而且数据是独立的;

7. 同一个进程的线程之间可以直接交流，同一个主进程的多个子进程之间是不可以进行交流，如果两个进程之间需要通信，就必须要通过一个中间代理来实现;

8. 一个线程可以控制和操作同一个进程里的其他线程，线程与线程之间没有隶属关系，但是进程只能操作子进程；

# 二、创建一个进程

Python提供了跨平台的多进行模块\&\#34;multiprocessing\&\#34;。

## 1、Process类的说明

**Process\(\[group \[, target \[, name \[, ****args**** \[, kwargs\]\]\]\]\]\)**

- group：指定进程组，目前只能使用None

- target：执行的目标任务名

- name：进程名字

- args：以元组方式给执行任务传参

- kwargs：以字典方式给执行任务传参

**Process创建的实例对象的常用方法:**

- start\(\)：启动子进程实例（创建子进程）

- join\(\)：阻塞当前进程，等待子进程执行结束

- terminate\(\)：不管任务是否完成，立即终止子进程

**Porcess对象其他的函数与属性**

- name：进程的名称；

- daemon：布尔值，是否是守护进程；

- pid：进程ID；

- exitcode：进程退出码；

- run\(\)：表示进程所要做的事情，通过向参数taget指定一个函数的方式指定run的行为，或者在子类中重载该方法；

- is\_alive\(\)：判断进程是否还活着；



## 2、直接使用Process创建进程

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Yzc3M2I4MWNhNGQwMTI2N2NlZDM4MzNjNDg3YzRlMGFfYmJhYzk1MjkyMjk4MjVkNDc3ZWM0YzBlYWViMWM5MDdfSUQ6NzI5MTg2NTU2OTk4MzQ2MzQyNV8xNzc5OTc2NzE1OjE3ODAwNjMxMTVfVjM)

```Python
import os
from multiprocessing import Process

def run_a_sub_proc(name):
    print(f'子进程：{name}（{os.getpid()}）开始...')

if __name__ == '__main__':
    print(f'主进程（{os.getpid()}）开始...')
    # 通过对Process类进行实例化创建一个子进程
    p = Process(target=run_a_sub_proc, args=('测试进程', ))
    p.start()
   

```

注意：这里需要明确以下主进程和子进程。当我们通过python demo\.py开始执行demo\.py这个程序时，程序被赋予了声明，成为一个进程，这个进程是 **主进程** 。而在主进程执行过程，通过对Process类进行实例化创建的是 **子进程** 。

## 3、继承Process类创建进程

```Python
from multiprocessing import Process     # 多进程的类
import time
import random
 
# 创建一个进程类Pros
class Pros(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name
 
    def run(self):
        print('%s 开始运行！' % self.name)
        # 随机睡眠1~5秒
        time.sleep(random.randrange(1, 5))
        print('%s 结束！' % self.name)
 
 
if __name__ == "__main__":

    # 创建3个子进程
    for i in range(3):
        num = "p" + str(i+1)
        num = Pros(f"子进程{num}")
        num.start()     # start方法会自动调用进程类中的run方法

 

```

## 4、join函数

在多进程中，join\(\)方法会使主进程进入阻塞，直到调用join\(\)方法的子进程执行完毕。即：使主进程进入阻塞，直到调用join\(\)方法的子进程执行完毕。

## 5、进程池（Pool）

**大家思考一个问题：在一台计算机中进程可以无限制的创建吗？**



进程池\(Pool\)的作用， 当进程数过多时，用于限制进程数。Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来它。



语法：Pool\(\[numprocess \[,initializer \[, initargs\]\]\]\)       \# 创建进程池

```Python
参数介绍：
    1 numprocess:要创建的进程数，如果省略，将默认使用cpu_count()的值
    2 initializer：是每个工作进程启动时要执行的可调用对象，默认为None
    3 initargs：是要传给initializer的参数组
```

```Python
import os, time
from multiprocessing import Process, Pool

def run_a_sub_proc(name):
    print(f'子进程：{name}（{os.getpid()}）开始！')
    for i in range(2):
        print(f'子进程：{name}（{os.getpid()}）运行中...')
        time.sleep(1)
    print(f'子进程：{name}（{os.getpid()}）结束！')

if __name__ == '__main__':
    print(f'主进程（{os.getpid()}）开始...')
    p = Pool(3)
    for i in range(1, 5):
        p.apply_async(run_a_sub_proc, args=(f"进程-{i}",))
    p.close()
    p.join()

```

apply\(\) ：该函数用于传递不定参数，主进程会被阻塞直到函数执行结束（不建议使用）函数原型如下：

```Plain Text
apply(func, args=(), kwds={})
```

apply\_async ：与apply用法一致，但它是非阻塞的且支持结果返回后进行回调，函数原型如下：

```Plain Text
apply_async(func[, args=()[, kwds={}[, callback=None]]])
```



# 三、进程之间的通信

**大家思考一下：在多进程中可以使用全局变量来共享数据吗？**

```Python
import multiprocessing
import time

# 定义全局变量
g_list = list()


# 添加数据的任务
def add_data():for i in range(5):
        g_list.append(i)
        print("add:", i)
        time.sleep(0.2)

    # 代码执行到此，说明数据添加完成
    print("add_data:", g_list)


def read_data():
    print("read_data", g_list)


if __name__ == '__main__':
    # 创建添加数据的子进程
    add_data_process = multiprocessing.Process(target=add_data)
    # 创建读取数据的子进程
    read_data_process = multiprocessing.Process(target=read_data)

    # 启动子进程执行对应的任务
    add_data_process.start()
    # 主进程等待添加数据的子进程执行完成以后程序再继续往下执行，读取数据
    add_data_process.join()
    read_data_process.start()

    print("main:", g_list)

    # 总结: 多进程之间不共享全局变量
```

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTZlZDhmM2Y1YTI4NDE5YjFiOTRiNGJmYzc3MDFlNjZfNjQ1ZWZiYzkzZDQyYzc3ODIzMmE3OTliM2YxMzFhNWRfSUQ6NzI5MTg3Njk0ODkwMzkzNjAwMl8xNzc5OTc2NzE1OjE3ODAwNjMxMTVfVjM)

创建子进程会对主进程资源进行拷贝，也就是说子进程是主进程的一个副本，好比是一对双胞胎，之所以进程之间不共享全局变量，是因为操作的不是同一个进程里面的全局变量，只不过不同进程里面的全局变量名字相同而已。

## 1、进程队列（Queue）通信

Queue（\[maxsize\]）:建立一个共享的队列\(内部维护着数据的共享\)，多个进程可以向队列里存/取数据。其中，参数是队列最大项数，省略则无限制。

```Python
from multiprocessing import Process, Queue
import time, os

def prodcut(q):
    print("开始生产.")
    for i in range(5):
        time.sleep(1)
        q.put('产品'+str(i))
        print("产品"+str(i)+"生产完成")

def consume(q):
    while True:
        prod = q.get()
        print("消费者：{}，消费产品:{}".format(os.getpid(), prod))
        time.sleep(1)

if __name__ == '__main__':
    q = Queue()
    p = Process(target=prodcut, args=(q, ))  # 生产者
    c1 = Process(target=consume, args=(q, ))  # 消费者1
    c2 = Process(target=consume, args=(q, ))  # 消费者2
    p.start()
    c1.start()
    c2.start()
    p.join()  # 当生产者结束后，将两个消费则也结束
    c1.terminate()
    c2.terminate()


```

## 2、管道\(Pipe\)

如果你创建了很多个子进程，那么其中任何一个子进程都可以对Queue进行存（put）和取（get）。但Pipe不一样，Pipe只提供两个端点，只允许两个子进程进行存（send）和取（recv）。也就是说，Pipe实现了两个子进程之间的通信。

```Python
from multiprocessing import Pipe, Pool
import os,time

def product(send_pipe):
    print("开始生产.")
    for i in range(5):
        time.sleep(1)
        send_pipe.send("产品"+str(i))
        print("产品" + str(i) + "生产完成")

def consume(recv_pipe):
    while True:
        print("消费者：{}，消费产品:{}".format(os.getpid(), recv_pipe.recv()))
        time.sleep(1)

if __name__ == '__main__':
    # 使用进程池来创建进程
    send_pipe, recv_pipe = Pipe()
    pool = Pool(2)
    pool.apply_async(product, args=(send_pipe,))
    pool.apply_async(consume, args=(recv_pipe,))
    pool.close()
    pool.join()


```



# 补充：计算密集型 vs\. IO密集型



是否采用多任务的第二个考虑是任务的类型。我们可以把任务分为**计算密（****CPU****）集型和****IO****密集型**。



计算密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、浮点运算、对视频进行高清解码等等，全靠CPU的运算能力。这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。



第二种任务的类型是IO密集型，涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。

