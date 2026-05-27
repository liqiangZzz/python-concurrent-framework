import socket

# 创建一个UDP socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定到所有IP地址的5555端口
server_socket.bind(('', 5555))
print("UDP聊天服务器启动，监听端口5555...")
print("输入 'quit' 退出聊天\n")

client_addr = None  # 保存客户端地址

while True:
    # 接收客户端消息
    message, addr = server_socket.recvfrom(1024)
    message_text = message.decode('utf8')
    client_addr = addr  # 保存客户端地址

    # 检查客户端是否退出
    if message_text == 'quit':
        print(f"客户端 {addr[0]}:{addr[1]} 已断开连接")
        break

    # 打印客户端消息
    print(f"\n[客户端 {addr[0]}:{addr[1]}]: {message_text}")

    # 服务端回复消息
    send_msg = input("[服务端] >> ")

    # 检查服务端是否要退出
    if send_msg == 'quit':
        # 通知客户端服务器要退出
        server_socket.sendto('quit'.encode('utf8'), client_addr)
        print("聊天结束，服务器已断开")
        break

    # 发送消息给客户端
    server_socket.sendto(send_msg.encode('utf8'), client_addr)

server_socket.close()
print("服务器已关闭")