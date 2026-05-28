# 第六节：Python中的协程

讲师：肖斌

# 一、协程的相关概念

如果都用多线程, 那么在高并发下, cpu大部分的时间都将用于切换线程上下文, 而且线程的切换是在内核态完成的, 会耗费额外的空间和时间，浪费了很多cpu时间片段。



协程（coroutine），又称为微线程，纤程。\(协程是一种用户态的轻量级线程\)



可以理解为一种在线程里跑的子线程, 它的默认栈空间很小 。 当多个协程在一个线程上运行时, 协程间会切换着运行, 协程的切换完全在用户态完成, 而且时机由程序员来自行调度, 从而使得线程的并发量大大提升。



简单的说：
**协程的核心思想就在于执行者对控制流的 “主动让出” 和 “恢复”。相对于，线程此类的 “抢占式调度” 而言，协程是一种 “协作式调度” 方式，协程之间执行任务按照一定顺序交替执行。**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NWYxZTdjYmIzMjExNzM0ZjRkYzUzODFhYWM4OGMyMWRfZDgzZDcxYmJjNjUyZjFlZjNlMzRjZWJiZGUzMTA2MTVfSUQ6NzI5NDQ2OTE2MTMwMzcxOTkzOF8xNzc5OTYxMzczOjE3ODAwNDc3NzNfVjM)

不过协程只适用于IO密集型程序\(大部分时间在等待\), 对于计算密集型程序, 协程的优势并不大, 因为没有给它切换的时间, cpu大部分时间都在工作。



# 二、定义协程（异步函数）

asyncio库 是用来编写 **协程** 代码的库，使用 **async/await** 语法。被用作多个提供高性能 Python 异步框架的基础，包括网络和网站服务，数据库连接库，分布式任务队列等。

async关键字定义的函数就是异步函数，也可以理解为：定义一个协程。 调用异步函数：add2\(1\)； 异步函数的实例化对象就是一个协程。

注意：这个协程并不会因为这个\&\#34;调用\&\#34;而开始执行\. 在实例化后,这个协程的状态是pending, 即**将要发生的**

```Python
# 普通函数定义
def add1(x):
    print(x+1)
    return x+1

# 异步函数的定义
async def add2(x):
    print("in async fun add")
    return x+2
```

# 三、启动多协程任务

`asyncio\.`**`run`**\(*coro*, *\**, *debug=False*\) 函数用来运行最高层级的入口点 \&\#34;test1\(\)\&\#34; 函数 。

## 第一种：多协程同步

以下代码段会打印 \&\#34;hello\&\#34;，等待 1 秒，再打印 \&\#34;world\&\#34;:





```Python
import asyncio

async def test1():
    print('hello')
      # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。
      # 当前协程挂起时，事件循环可以去执行其他协程（任务）。
    await asyncio.sleep(1)
    print('world')

coroutine = test1() 
print(coroutine)
asyncio.run(coroutine)
```

```Python
import asyncio
import time


async def eat():
    for i in range(6):
        print('正在吃饭...')
        await asyncio.sleep(0.5)


# 做作业任务
async def work():
    for i in range(6):
        print('正在做作业...')
        await asyncio.sleep(0.5)


async def main():
    await eat()
    await work()


if __name__ == '__main__':
    asyncio.run(main())
```

而上面最核心的动作就是切换别的方法，怎么切换？**用await关键字**。

## 第二种：多协程异步

是的，切则切了，可切的对吗？事实上这两个协程任务并没有达成“协作”，因为它们是同步执行的，所以并不是在方法内await了，就可以达成协程的工作方式，我们需要并发启动这两个协程任务：

```Python
import asyncio
import time


async def eat():
    for i in range(6):
        print('正在吃饭...')
        await asyncio.sleep(0.5)


# 做作业任务
async def work():
    for i in range(6):
        print('正在做作业...')
        await asyncio.sleep(0.5)

async def main():
    await asyncio.gather(eat(), work())

if __name__ == '__main__':
    asyncio.run(main())
```

如果没有asyncio\.gather的参与，协程方法就是普通的同步方法，就算用async声明了异步也无济于事。而asyncio\.gather的基础功能就是将协程任务并发执行，从而达成“协作”。



## 第三种：多任务异步

我们通过asyncio\.create\_task对eat和work进行封装，返回的对象是一个异步任务，再通过await进行调用，由此两个单独的异步方法就都被绑定到同一个Eventloop（事件循环中）了，这样虽然写法上同步，但其实是异步执行：

```Python
import asyncio
import time


async def eat():
    for i in range(6):
        print('正在吃饭...')
        await asyncio.sleep(0.5)


# 做作业任务
async def work():
    for i in range(6):
        print('正在做作业...')
        await asyncio.sleep(0.5)


async def main():
    # await eat()
    # await work()
    await asyncio.gather(eat(), work())


async def create_task():
    task1 = asyncio.create_task(eat())
    task2 = asyncio.create_task(work())

    await task1
    await task2
    #await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(create_task())
```



# 四、协程的返回值和监控

## 1、获取协程结束后的返回值

解决了并发执行的问题，现在假设每个异步任务都会返回一个操作结果; 怎么得到协程的返回结果呢？

```Python
import asyncio
import time


async def eat():
    for i in range(6):
        print('正在吃饭...')
        await asyncio.sleep(0.5)
    return '吃饭完成'

# 做作业任务
async def work():
    for i in range(6):
        print('正在做作业...')
        await asyncio.sleep(0.5)
    return '做作业完成'



async def create_task():
    task1 = asyncio.create_task(eat())
    task2 = asyncio.create_task(work())

    # await task1
    # await task2
    # 得到返回值
    # result = await asyncio.gather(task1, task2)
    # 更加详细的返回信息
    result = await asyncio.wait([task1, task2])
    print(result)

if __name__ == '__main__':
    asyncio.run(create_task())
```

默认情况下：

- asyncio\.wait会等待全部任务完成 \(return\_when=ALL\_COMPLETED\)，

- return\_when=FIRST\_COMPLETED（第一个协程完成就返回）

- return\_when=‘FIRST\_EXCEPTION’（出现第一个异常就返回）。



## 2、强制终止协程

task1\.cancel（） : 终止任务（终止协程）

这里task1被手动取消，但会影响task2的执行，这违背了协程“互相提携”的特性。所以，需要asyncio\.gather方法捕获协程任务的异常。

return\_exceptions=True ： 有外面的线程捕获协程里面的异常。

```Python

async def create_task():
    task1 = asyncio.create_task(eat())
    task2 = asyncio.create_task(work())
    task1.cancel()
    # await task1
    # await task2
    # 得到返回值
    result = await asyncio.gather(task1, task2, return_exceptions=True)
    # 更加详细的返回信息
    # result = await asyncio.wait([task1, task2], return_when=asyncio.ALL_COMPLETED)
    print(result)

if __name__ == '__main__':
    asyncio.run(create_task())
```

## 3、协程任务回调

假设协程任务执行完毕之后，需要立刻进行回调操作，比如将任务结果推送到其他接口服务上。这个时候，需要用到添加回调函数： add\_done\_callback

```Python
def call_back(coroutine, current_time):
    print(f'收到回调参数：{current_time}')
    print(f'回调函数，任务1的返回值:{coroutine.result()}, 结束时间：{current_time}')


async def create_task():
    task1 = asyncio.create_task(eat())
    task2 = asyncio.create_task(work())
    # 如果回调函数没有参数
    # task1.add_done_callback(call_back)
    # 如果回调函数有参数
    task1.add_done_callback(partial(call_back, current_time=time.strftime('%H:%M:%S')))
    # 得到返回值
    result = await asyncio.gather(task1, task2, return_exceptions=True)
    # 更加详细的返回信息
    # result = await asyncio.wait([task1, task2], return_when=asyncio.ALL_COMPLETED)
    print(result)


if __name__ == '__main__':
    asyncio.run(create_task())
```

# 五、总结

协程任务的调度远比多线程的系统级调度要复杂，稍不留神就会造成业务上的“同步”阻塞，弄巧成拙，适得其反。这也解释了为什么相似场景中多线程的出场率要远远高于协程，就是因为多线程不需要考虑启动后的“切换”问题。

1. 线程和协程推荐在IO密集型的任务\(比如网络调用\)中使用，而在CPU密集型的任务中，表现较差。

2. 对于CPU密集型的任务，则需要多个进程，绕开GIL的限制，利用所有可用的CPU核心，提高效率。

3. 在高并发下的最佳实践就是多进程\+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。

