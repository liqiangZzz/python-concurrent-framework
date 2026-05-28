import threading


def recursive_lock_deadlock():
    """同一个线程重复获取同一个普通锁"""
    lock = threading.Lock()

    lock.acquire()
    print("第一次获取锁成功")

    # 再次尝试获取同一个锁
    print("尝试第二次获取同一个锁...")
    lock.acquire()  # 这里会死锁！因为普通锁不可重入
    print("第二次获取锁成功")  # 永远不会执行

    lock.release()


if __name__ == '__main__':
    print("=" * 50)
    print("自死锁案例：同一线程重复获取非可重入锁")
    print("=" * 50)

    recursive_lock_deadlock()  # 程序会卡死