#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a socket example which send echo message to server.'

import socket
from Tkinter import *

# root=Tk()
# root.title("echo client")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print s.recv(1024)
while True:
    content=raw_input("please input ")
    s.send(content)
    print s.recv(1024)
s.send('exit')
s.close()
