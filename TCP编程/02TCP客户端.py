import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('192.168.0.66', 8000)
client_socket.connect(server_addr)

while True:

    send_msg = input('客户端>>')
    if send_msg == 'quit':  # 退出聊天
        client_socket.send(send_msg.encode('utf8'))
        break
    client_socket.send(send_msg.encode('utf8'))

    msg = client_socket.recv(1024).decode('utf8')

    print(f'来自服务端端IP:{server_addr[0]},端口号:{server_addr[1]}：{msg}')

client_socket.close()