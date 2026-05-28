import time
from multiprocessing import Process, Manager


def add_data(q_to_read, q_back_to_add):
    """
    进程1：生产者进程
    负责：向队列发送数据，并等待接收者的反馈
    :param q_to_read: 发送数据的队列
    :param q_back_to_add: 接收反馈的队列
    """
    for i in range(6):
        # 1. 向接收进程发送数据
        q_to_read.put(i)

        # 2. 阻塞等待接收进程的确认消息
        # 如果接收端没 put，这里会一直停住
        response = q_back_to_add.get()
        print(f"发送端收到反馈: {response} ----- (当前数据:{i})")

        time.sleep(0.3)


def read_data(q_to_read, q_back_to_add):
    """
    进程2：消费者进程
    负责：循环监听队列数据，打印并返回‘收到’反馈
    :param q_to_read: 获取数据的队列
    :param q_back_to_add: 发送反馈的队列
    """
    while True:
        # 1. 阻塞获取数据，直到队列中有新元素
        value = q_to_read.get()

        # 2. 打印接收到的数据
        print(f"接收端正在处理: {value}")

        # 3. 向发送进程返回反馈
        q_back_to_add.put('收到')

        time.sleep(0.4)


if __name__ == '__main__':
    # 使用 Manager 开启一个服务端进程，负责管理共享对象
    # with 语句确保 Manager 进程在执行完毕后能安全关闭
    with Manager() as manager:
        # 1. 通过 Manager 创建进程安全的队列 (Queue)
        # Manager().Queue() 的优势：不仅可以在 Process 中使用，也可以在 Pool 进程池中使用
        # 创建两个队列来模拟 Pipe 的双向通信逻辑
        queue_send = manager.Queue()  # 主 -> 从 (传递数据)
        queue_receive = manager.Queue()  # 从 -> 主 (传递反馈)

        # 2. 定义并初始化两个子进程
        # 将共享的队列对象作为参数传递给目标函数
        p1 = Process(target=add_data, args=(queue_send, queue_receive))
        p2 = Process(target=read_data, args=(queue_send, queue_receive))

        # 3. 设置守护进程
        # 因为 p2 (read_data) 内部是 while True 死循环，将其设为守护进程
        # 这样当主进程和 p1 执行完结束时，p2 会被自动强制关闭
        p2.daemon = True

        # 4. 启动进程
        p1.start()
        p2.start()

        # 5. 等待 p1 (add_data) 执行完毕
        # p1 完成循环后，主进程才会继续往下走
        p1.join()

    print("--- 所有通信任务结束 ---")