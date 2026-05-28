import threading


def recursive_lock_solution():
    """使用可重入锁 RLock 解决"""
    lock = threading.RLock()  # 改用 RLock

    lock.acquire()
    print("第一次获取锁成功")

    lock.acquire()  # RLock 允许同一线程重复获取
    print("第二次获取锁成功")

    lock.release()
    lock.release()
    print("释放完成")


if __name__ == '__main__':
    recursive_lock_solution()