from threading import Lock, Thread


def recursive_lock_deadlock():
    """同一个线程重复获取同一个普通锁"""
    lock = Lock()

    lock.acquire()
    print("第一次获取锁成功")
    import time

    # 创建两把锁
    lock1 = Lock()
    lock2 = Lock()

    def thread_a():
        """线程A：先拿锁1，再拿锁2"""
        print("线程A: 等待拿锁1...")
        lock1.acquire()
        print("线程A: 拿到锁1了！")

        time.sleep(0.5)  # 让线程B有机会拿到锁2

        print("线程A: 等待拿锁2...")
        lock2.acquire()  # 等待锁2，但锁2在线程B手里
        print("线程A: 拿到锁2了！")

        lock2.release()
        lock1.release()
        print("线程A: 完成")

    def thread_b():
        """线程B：先拿锁2，再拿锁1（顺序反了）"""
        print("线程B: 等待拿锁2...")
        lock2.acquire()
        print("线程B: 拿到锁2了！")

        time.sleep(0.5)  # 让线程A有机会拿到锁1

        print("线程B: 等待拿锁1...")
        lock1.acquire()  # 等待锁1，但锁1在线程A手里
        print("线程B: 拿到锁1了！")

        lock1.release()
        lock2.release()
        print("线程B: 完成")

    if __name__ == '__main__':
        t1 = Thread(target=thread_a)
        t2 = Thread(target=thread_b)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print("程序结束")  # 永远等不到这一行
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