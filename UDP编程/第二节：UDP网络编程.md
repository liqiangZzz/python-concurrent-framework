# 第二节：UDP网络编程

讲师：肖斌

# 一、UDP协议

**UDP****网络协议****（User Data Protocol，****用户数据报协议****）：**



是一个无连接的简单的面向数据报的运输层协议。UDP不提供可靠性，它只是把应用程序传给IP层的数据报发送出去，但是并不能保证它们能到达目的地。由于UDP在传输数据报前不用在客户和服务器之间建立一个连接，且没有超时重发等机制，故而传输速度很快。



UDP是一种面向无连接的协议，每个数据报都是一个独立的信息，包括完整的源地址或目的地址，它在网络上以任何可能的路径传往目的地，因此能否到达目的地，到达目的地的时间以及内容的正确性都是不能被保证的。

**【适用情况】**

UDP是面向消息的协议，通信时不需要建立连接，数据的传输自然是不可靠的，UDP一般用于多点通信和实时的数据业务，比如



- **语音广播**

- **视频**

- **QQ**

- **TFTP****\(简单文件传送）**

- **大型网络游戏**



# 二、Socket编程

## 1、Socket（套接字）的定义

实现网络编程进行数据传输的一种技术手段,网络上各种各样的网络服务大多都是基于 Socket来完成通信的。



Socket的英文原义是“孔”或“插座”，网络上的两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为一个socket。



建立网络通信连接至少要一对端口号\(socket\)，socket本质是编程接口\(API\)，对TCP/IP的封装，TCP/IP也要提供可供程序员做网络开发所用的接口，这就是Socket编程接口。



基本上，Socket 是任何一种计算机网络通讯中最基础的内容。例如当你在浏览器地址栏中输入 http://www\.baidu\.com会打开一个套接字，然后连接到 http://www\.baidu\.com/ 并读取响应的页面然后然后显示出来。而其他一些聊天客户端如 qq和 skype 也是类似。任何网络通讯都是通过 Socket 来完成的。

**Python 官方关于 Socket 的函数请看 ****http://docs\.python\.org/library/socket\.html**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmFjZmJhZWExYjhjNTU4MTQ5ZmFlOTEwZjUyZDFlOTJfMDAzNTZkZmYyN2NlYTQ5NTg3ZjkxN2MzNzFhM2JjNTFfSUQ6NzI5MDc0MTY0NzIxNDAwMjIwNF8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

## 2、Socket的类型

socket\(family,type\[,protocal\]\) 使用给定的地址族、套接字类型、协议编号（默认为0）来创建套接字。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzVkNmUyMzkxNGU5YzNjNjBiMGFlZWRlNzI3OTE4YTlfMTk3ZTg3YmFmNWQ3MmI4NWUyMTI2MDcxYzVhMmY3OGZfSUQ6NzI5MDc0MjY2Mzg1NzUzNzAyNl8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

## 3、Socket相关函数

### 1）服务器端的socket函数

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=M2U1MWJkZGI2MzFiODc2NWQ1Y2JkYWNlMDJmOGJlODNfNzBmNTUzNzM1MmE3MmI5YWE1ZWYzZWQzMGE4ODdmYTFfSUQ6NzI5MDc0MzE1NTQ2ODc2MzE2NF8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

### 2）客户端的socket函数

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDgyYjgyY2E0OTA0MzlhZjM4YzZhODZhZTFkMDZiNjZfOTFlMGJkOGY2NGNmYmJhNGY5MDBkNzRlOGViNDU2M2FfSUQ6NzI5MDc0MzMyMzg2NTA4ODAwMV8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

### 3）公共的sokcet函数

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTBhZWQ3MmQwMmY0NjUyY2Y1OGIxNGZlMTRkMjU5NTBfN2M1NTVlN2NhNTQ1NzZkZDEzOGI5YmJjM2I0YzAwODdfSUQ6NzI5MDc0MzQ5ODgzODg2Nzk5Nl8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTI1ZTVhYjRhOTZmY2YxZmI3YzQ4MzYwOWZhZjA3ZDFfYzI5OTk5ODIwMzRlNzMxZGM1ZmJiZDE5OTc4MzU2ZTdfSUQ6NzI5MDc0MzYxMTEyMDk1OTUxNl8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

# 三、UDP编程步骤

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWU5OTJjMjEwZTFjMmY1YmY2MjRiNzc1MzkzNjFhNWJfODY1YzQwMWQ1NGVlNTM4Nzc3MmU4NjJjYWM2MTA0YmRfSUQ6NzI5MDc0MzgxNTMzNjg2OTkxNl8xNzc5OTc2NjU4OjE3ODAwNjMwNThfVjM)

UDP服务器的建立可以归纳这几步：



- 创建 socket（套接字）

- 绑定 socket 的 IP 地址和端口号

- 接收客户端数据

- 关闭连接



UDP客户端的创建可总结为这几步：



- 创建 socket（套接字）

- 向服务器发送数据

- 关闭连接



