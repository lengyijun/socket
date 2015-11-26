# -*- coding: utf-8 -*-
#!/usr/bin/env python

# 写的极好，开一个echo_server可以监听多个client发送的信息
'a server example which send hello to client.'

import time, socket, threading
from Tkinter import *

def opensocket():
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

def socket_thread():
    t=threading.Thread(target=opensocket)
    t.start()

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            print ("exit")
            break
        tv_get.insert(1.0,addr[0]+" "+str(addr[1])+" "+data)
        print (addr[0]+" "+str(addr[1])+" "+data)
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

if __name__ == '__main__':
    root=Tk()
    root.title("server<<<")
    root.geometry('200x200')

    frm=Frame(root)
    frm_l=Frame(frm)
    frm_r=Frame(frm)

    Button(frm_r,text="start socket",command=lambda :socket_thread()).pack(side=TOP)
    Button(frm_r,text="send message",command=lambda :socket_thread()).pack(side=TOP)

    tv_get=Text(frm_l)
    tv_get.insert(1.0,"init")
    tv_get.pack(side=TOP)

    tv_send=Text(frm_l)
    tv_send.insert(1.0,"init")
    tv_send.pack(side=TOP)

    frm_r.pack(side=RIGHT)
    frm_l.pack(side=LEFT)
    frm.pack()

    root.mainloop()
