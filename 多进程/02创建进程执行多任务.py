import time
from multiprocessing import Process


class EatProcess(Process):
    """写一个自定义的类，继承Process"""

    def __init__(self, name):
        super().__init__()  # 注意：必须要有
        self.name = name

    def run(self):
        for i in range(6):
            print(f'进程{self.name}: 正在吃饭...')
            time.sleep(0.3)


class WorkProcess(Process):
    """写一个自定义的类，继承Process"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(6):
            print(f'进程{self.name}: 正在做作业...')
            time.sleep(0.3)


if __name__ == '__main__':
    p1 = EatProcess('process-1')
    p2 = WorkProcess('process-2')

    p1.start()
    p2.start()