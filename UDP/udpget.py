# udp广播案例-接收端
from socket import *
import time
import traceback

s = socket(AF_INET, SOCK_DGRAM)
# 设置套接字
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# 选择一个接收地址
s.bind(('', 9999))
while True:
    try:
        msg, addr = s.recvfrom(1024)
        print('接收消息==客户端地址:{},消息内容:{}'.format(addr, msg))
        # s.sendto("我是服务端老白,我的时间是{}".format(time.time()).encode('utf-8'), addr)
    except:
        print("接收消息异常:{}".format(traceback.format_exc()))
s.close()
