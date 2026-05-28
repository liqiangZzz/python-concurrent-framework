import socket

# 需求：即时聊天

# 这个服务端的socket只是负责接受客户端的连接请求。
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('', 8000))

# 服务器 允许最大等待建立连接的个数。
server_socket.listen(128)

# 接受客户端的连接
# accept是阻塞的函数，
socket2, client_addr = server_socket.accept()

while True:
    # socket2, client_addr = server_socket.accept()
    # 正式开始聊天
    msg = socket2.recv(1024).decode('utf8')
    if msg == 'quit':
        break
    print(f'来自客户端IP:{client_addr[0]},端口号:{client_addr[1]}：{msg}')

    # 给客户端发送聊天信息
    send_msg = input('服务器>>')
    socket2.send(send_msg.encode('utf8'))

socket2.close()  # 端口连接
server_socket.close()