import wx
import time
import sys
from socket import *
from threading import Thread


class MyServerFrame(wx.Frame):
    def __init__(self):
        # 初始化父类窗口，设置标题和尺寸
        super().__init__(None, -1, '老肖的聊天室服务器', size=(550, 600))

        # 定义核心属性
        self.server_socket = None  # 服务端监听套接字
        self.is_running = False  # 服务器运行状态标识
        self.client_dict = {}  # 存放所有在线客户端线程的字典 {用户名: 线程对象}

        # --- GUI 布局开始 ---
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)  # 垂直布局容器

        # 顶部按钮区域：水平布局
        fg = wx.BoxSizer(wx.HORIZONTAL)
        self.start_btn = wx.Button(pl, label='启动服务', size=(150, 40))
        self.save_btn = wx.Button(pl, label='保存记录', size=(150, 40))
        self.stop_btn = wx.Button(pl, label='停止服务', size=(150, 40))

        fg.Add(self.start_btn, 0, wx.ALL, 5)
        fg.Add(self.save_btn, 0, wx.ALL, 5)
        fg.Add(self.stop_btn, 0, wx.ALL, 5)

        # 只读的多行文本框，用于显示聊天日志
        self.read_text = wx.TextCtrl(pl, style=wx.TE_MULTILINE | wx.TE_READONLY)

        box.Add(fg, 0, wx.ALIGN_CENTER)
        box.Add(self.read_text, 1, wx.EXPAND | wx.ALL, 5)  # 自动拉伸填充剩余空间
        pl.SetSizer(box)

        # 绑定按钮事件到处理函数
        self.Bind(wx.EVT_BUTTON, self.start_server, self.start_btn)
        self.Bind(wx.EVT_BUTTON, self.save_log_to_file, self.save_btn)
        self.Bind(wx.EVT_BUTTON, self.stop_server, self.stop_btn)
        self.Bind(wx.EVT_CLOSE, self.on_close)  # 拦截窗口关闭事件

    def start_server(self, event):
        """点击‘启动服务’：初始化套接字并开启监听线程"""
        if self.is_running: return  # 如果已经在运行则不重复启动

        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)
            # SO_REUSEADDR 允许程序崩溃退出后立即重新占用端口，避免“端口已占用”报错
            self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.server_socket.bind(('', 8888))  # 绑定 IP 和 端口
            self.server_socket.listen(10)  # 设置最大排队连接数
            self.is_running = True

            # 开启后台子线程，负责不断接收客户端连接请求 (Accept)
            t = Thread(target=self.accept_work)
            t.daemon = True  # 设置为守护线程：主程序退出时，该线程自动结束
            t.start()

            self.log_to_ui("服务器已启动，监听端口 8888...")
            self.start_btn.Disable()  # 启动后禁用启动按钮
        except Exception as e:
            wx.MessageBox(f"启动失败: {e}")

    def accept_work(self):
        """死循环：持续监听客户端的连接请求"""
        while self.is_running:
            try:
                # accept() 会阻塞，直到有新客户端连入
                session_socket, addr = self.server_socket.accept()
                # 获取连入后的第一个数据包：约定为用户名
                username = session_socket.recv(1024).decode('utf8')

                # 为每个新连入的用户创建一个专属会话线程，负责后续的双向通信
                t = SessionThread(username, session_socket, self)
                t.daemon = True
                self.client_dict[username] = t
                t.start()

                # 通知所有人有新成员加入
                self.broadcast_msg(f"【系统通知】: 欢迎 {username} 进入聊天室")
            except:
                break  # 服务器关闭引发异常时跳出循环

    def log_to_ui(self, msg):
        """
        线程安全地在界面记录日志
        注意：在非 GUI 线程中更新界面必须使用 wx.CallAfter
        """
        current_time = time.strftime('%H:%M:%S')
        full_msg = f"{msg}\n时间: {current_time}\n{'-' * 50}\n"

        # 核心：wx.CallAfter 会把任务排入主线程队列执行，防止界面崩溃
        wx.CallAfter(self.read_text.AppendText, full_msg)
        # 自动滚动到文本框最底端
        wx.CallAfter(lambda: self.read_text.ShowPosition(self.read_text.GetLastPosition()))

    def broadcast_msg(self, msg):
        """将消息发送给当前 client_dict 里的所有在线用户"""
        self.log_to_ui(msg)  # 先在服务端自己记录一份

        # list(items) 是为了防止遍历时有线程断开导致字典大小变化抛异常
        for name, client in list(self.client_dict.items()):
            if client.isOn:
                try:
                    client.session_socket.send(msg.encode('utf8'))
                except:
                    client.isOn = False  # 发送失败说明客户端已断开

    def remove_client(self, username):
        """将离开的用户从管理字典中删除"""
        if username in self.client_dict:
            del self.client_dict[username]

    def save_log_to_file(self, event):
        """将界面上的聊天内容保存到本地 .txt 文件"""
        file_name = f'log-{time.strftime("%Y-%m-%d")}.txt'
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.read_text.GetValue())
        wx.MessageBox(f"记录已保存至: {file_name}")

    def stop_server(self, event):
        """优雅地停止服务"""
        self.broadcast_msg("【系统通知】: 服务器即将在3秒后关闭...")

        # 向所有客户端发送约定的断开指令
        for client in self.client_dict.values():
            try:
                client.session_socket.send('laoxiao^leave^laoxiao'.encode('utf8'))
            except:
                pass

        self.is_running = False
        if self.server_socket:
            self.server_socket.close()

        # 延迟2秒后退出程序，确保客户端收到了消息
        wx.CallLater(2000, sys.exit, 0)

    def on_close(self, event):
        """处理点击窗口右上角 [X] 的行为"""
        self.stop_server(None)
        event.Skip()


class SessionThread(Thread):
    """
    会话线程类：每个在线客户端都对应一个此线程的实例。
    主要任务：持续监听该客户端发送来的各种聊天内容。
    """

    def __init__(self, username, session_socket, server_frame):
        super().__init__()
        self.username = username
        self.session_socket = session_socket
        self.server_frame = server_frame
        self.isOn = True

    def run(self):
        try:
            while self.isOn:
                # 等待并接收客户端的数据
                data = self.session_socket.recv(1024).decode('utf8')

                # 如果收到空数据或离线指令，跳出接收循环
                if not data or data == 'laoxiao^leave^laoxiao':
                    break

                # 接收到正常聊天内容，通过服务器对象广播出去
                self.server_frame.broadcast_msg(f"{self.username}: {data}")
        except:
            pass  # 捕获如客户端强制关闭导致的连接重置异常
        finally:
            self.isOn = False
            # 清理套接字资源
            try:
                self.session_socket.send('laoxiao^leave^laoxiao'.encode('utf8'))
                self.session_socket.close()
            except:
                pass
            # 从服务器维护的字典中移除，并通知所有人
            self.server_frame.remove_client(self.username)
            self.server_frame.broadcast_msg(f"【系统通知】: {self.username} 离开了聊天室")


if __name__ == '__main__':
    app = wx.App()
    MyServerFrame().Show()
    app.MainLoop()  # 开启 wx 事件主循环