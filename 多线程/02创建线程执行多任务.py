import time
from threading import Thread


class EatThread(Thread):
    """写一个自定义的类，继承Thread"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(6):
            print(f'线程{self.name}: 正在吃饭...{i}')
            time.sleep(0.5)


class WorkThread(Thread):
    """写一个自定义的类，继承Thread"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(6):
            print(f'线程{self.name}: 正在写作业...{i}')
            time.sleep(0.5)


if __name__ == '__main__':
    t1 = EatThread('t-01')
    t2 = WorkThread('t-02')

    t1.start()
    # t1.join()
    t2.start()
