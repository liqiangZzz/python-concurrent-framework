import time
from multiprocessing.pool import Pool


# 吃饭任务
def eat(name):
    for i in range(6):
        print(f'正在吃饭...{name}')
        time.sleep(0.3)


# 做作业任务
def work():
    for i in range(6):
        print('正在做作业...')
        time.sleep(0.3)


# 打游戏任务
def game():
    for i in range(6):
        print('正在打游戏...')
        time.sleep(0.3)


if __name__ == '__main__':
    process_pool = Pool(2)

    # apply 函数是一个阻塞的函数（主进程） ,从进程池中请求一个新的进程去执行任务
    # process_pool.apply(eat,args=('张三',))
    # process_pool.apply(work)

    # apply_async() 是非阻塞的，调用后立即返回，任务被提交到进程池的任务队列中等待执行,会立即执行下一行代码，而不会等待任务完成。
    # 如果不加 close() 和 join()，主进程会直接结束，而主进程结束时会强制终止所有子进程，导致任务还没来得及执行就被杀死了。
    process_pool.apply_async(eat, args=('张三',))
    process_pool.apply_async(work)
    process_pool.apply_async(game)
    # 进程池关闭，进程池不再接受新的请求，但已提交的任务会继续执行
    process_pool.close()
    # 采用进程池的异步调用， 一定要手动的调用join函数。
    process_pool.join()
