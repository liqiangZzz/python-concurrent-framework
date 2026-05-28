import time
from multiprocessing import Process


class EatProcess(Process):
    """写一个自定义的类，继承Process"""

    def __init__(self, name):
        super().__init__()  # 注意：必须要有
        self.name = name

    def run(self) -> None:
        for i in range(6):
            print(f'进程{self.name}: 正在吃饭...')
            time.sleep(0.3)


class WorkProcess(Process):
    """写一个自定义的类，继承Process"""

    def __init__(self, name):
        super().__init__()  # 注意：必须要有
        self.name = name

    def run(self) -> None:
        for i in range(6):
            print(f'进程{self.name}: 正在做作业...')
            time.sleep(0.3)


if __name__ == '__main__':
    p1 = EatProcess('process-1')
    p2 = WorkProcess('process-2')

    p1.start()
    p1.join() # 子进程可以调用join函数：主进程就会阻塞，等待 p1 运行结束
    p2.start()  # ← 等 p1 结束后，主进程才执行到这里，启动 p2
