#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 写的极好，开一个echo_server可以监听多个client发送的信息
'a server example which send hello to client.'

import time, socket, threading
from Tkinter import *

# root=Tk()
# root.title("echo server")

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            print ("exit")
            break
        # print (addr)
        print (addr[0]+" "+str(addr[1])+" "+data)
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('127.0.0.1', 9999))
s.listen(5)
print 'Waiting for connection...'
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
