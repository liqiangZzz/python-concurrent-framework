import socket
import sys

# 创建UDP socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 服务器地址和端口
SERVER_IP = '192.168.0.103'  # 修改为你的服务器IP
SERVER_PORT = 5555

print("UDP聊天客户端启动...")
print("连接到服务器...")
print("输入 'quit' 退出聊天\n")

# 设置超时，避免无限阻塞
client_socket.settimeout(5)

while True:
    try:
        # 发送消息给服务端
        send_msg = input("[客户端] >> ")

        # 发送消息
        client_socket.sendto(send_msg.encode('utf8'), (SERVER_IP, SERVER_PORT))

        # 如果发送的是quit，退出循环
        if send_msg == 'quit':
            print("已退出聊天")
            break

        # 接收服务器回复的消息（设置超时避免永久阻塞）
        try:
            message, addr = client_socket.recvfrom(1024)
            message_text = message.decode('utf8')

            # 检查服务器是否退出
            if message_text == 'quit':
                print("\n服务器已断开连接！")
                break

            # 打印服务器消息
            print(f"[服务器 {addr[0]}:{addr[1]}]: {message_text}")

        except socket.timeout:
            print("等待服务器响应超时...")
            continue

    except KeyboardInterrupt:
        print("\n用户中断连接")
        break
    except Exception as e:
        print(f"发生错误：{e}")
        break

client_socket.close()
print("客户端已关闭")