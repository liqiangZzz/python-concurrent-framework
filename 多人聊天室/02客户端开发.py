import wx
import sys
from socket import *
from threading import Thread


class MyClientFrame(wx.Frame):
    def __init__(self, username):
        super().__init__(None, -1, f'客户端 - {username}', size=(450, 550))
        self.username = username
        self.client_socket = None
        self.is_on = False  # 状态标识：是否在线

        # --- GUI 界面构建 ---
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # 顶部操作按钮
        btns = wx.BoxSizer(wx.HORIZONTAL)
        self.conn_btn = wx.Button(pl, label='进入聊天室', size=(150, 40))
        self.leave_btn = wx.Button(pl, label='离开聊天室', size=(150, 40))
        btns.Add(self.conn_btn, 1, wx.ALL, 5)
        btns.Add(self.leave_btn, 1, wx.ALL, 5)

        # 聊天记录显示区域
        self.log_text = wx.TextCtrl(pl, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # 消息输入框：PROCESS_ENTER 允许拦截回车事件
        self.input_text = wx.TextCtrl(pl, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, size=(-1, 100))

        # 底部功能按钮
        bottom_btns = wx.BoxSizer(wx.HORIZONTAL)
        self.clear_btn = wx.Button(pl, label='重置内容', size=(150, 40))
        self.send_btn = wx.Button(pl, label='发送消息', size=(150, 40))
        bottom_btns.Add(self.clear_btn, 1, wx.ALL, 5)
        bottom_btns.Add(self.send_btn, 1, wx.ALL, 5)

        # 将布局添加到 BoxSizer
        box.Add(btns, 0, wx.EXPAND)
        box.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 5)
        box.Add(self.input_text, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(bottom_btns, 0, wx.EXPAND)

        pl.SetSizer(box)

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.connect_server, self.conn_btn)
        self.Bind(wx.EVT_BUTTON, self.send_message, self.send_btn)
        self.Bind(wx.EVT_BUTTON, self.leave, self.leave_btn)
        self.Bind(wx.EVT_BUTTON, lambda e: self.input_text.Clear(), self.clear_btn)

        # 监听回车键发送，优化聊天体验
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.send_message)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def connect_server(self, event):
        """点击‘连接’：发起 TCP 三次握手并启动监听子线程"""
        if self.is_on: return

        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            # 连接服务器（这里使用本机测试地址）
            self.client_socket.connect(('127.0.0.1', 8888))
            # 连接建立后第一件事：发送自己的用户名给服务器登记
            self.client_socket.send(self.username.encode('utf8'))
            self.is_on = True

            # 连接成功后禁用连接按钮，光标自动聚焦到输入框
            self.conn_btn.Disable()
            self.input_text.SetFocus()

            # 开启子线程，死循环监听服务器广播的消息
            t = Thread(target=self.recv_data)
            t.daemon = True
            t.start()

            self.log_text.AppendText("成功连接至服务器...\n")
        except Exception as e:
            wx.MessageBox(f"无法连接服务器: {e}")

    def recv_data(self):
        """客户端子线程逻辑：不断读取服务器发送的消息"""
        while self.is_on:
            try:
                data = self.client_socket.recv(1024).decode('utf8')
                # 收到特定的退出指令，停止接收逻辑
                if not data or data == 'laoxiao^leave^laoxiao':
                    break

                # 核心：通过 wx.CallAfter 线程安全地更新界面显示
                wx.CallAfter(self.update_log, data)
            except:
                break

        # 退出循环说明连接已断开，清理资源
        self.is_on = False
        if self.client_socket:
            self.client_socket.close()
        self.client_socket = None

        # 恢复‘进入按钮’为可用状态，并在记录中提示离线
        wx.CallAfter(self.conn_btn.Enable)
        wx.CallAfter(self.log_text.AppendText, "已断开与服务器的连接。\n")

    def update_log(self, msg):
        """将新消息添加到记录框，并滚动到底部"""
        self.log_text.AppendText(msg + "\n" + "-" * 40 + "\n")
        self.log_text.ShowPosition(self.log_text.GetLastPosition())

    def send_message(self, event):
        """发送用户在输入框里写的内容"""
        if not self.is_on:
            wx.MessageBox("请先进入聊天室！")
            return

        msg = self.input_text.GetValue().strip()
        if msg:
            try:
                self.client_socket.send(msg.encode('utf8'))
                # 发送成功后清空输入框并重置焦点
                self.input_text.Clear()
                self.input_text.SetFocus()
            except:
                self.is_on = False

    def leave(self, event):
        """主动点击‘离开’：发送离线信号"""
        if self.client_socket:
            try:
                self.client_socket.send('laoxiao^leave^laoxiao'.encode('utf8'))
            except:
                pass
        self.is_on = False

    def on_close(self, event):
        """窗口关闭前自动断开 Socket"""
        self.leave(None)
        event.Skip()  # 继续执行窗口销毁逻辑


if __name__ == '__main__':
    app = wx.App()

    # 启动前先弹出一个对话框输入名字
    dlg = wx.TextEntryDialog(None, '请输入你的昵称:', '聊天室登录', '小王')
    if dlg.ShowModal() == wx.ID_OK:
        name = dlg.GetValue().strip()
        if not name: name = "无名氏"
        frame = MyClientFrame(name)
        frame.Show()
        app.MainLoop()
    else:
        # 如果点击取消，直接退出程序
        sys.exit(0)