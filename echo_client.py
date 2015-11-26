#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a socket example which send echo message to server.'

import socket
from Tkinter import *

def send(s,t):
    # content=raw_input("please inout ")
    t_conent=tv_send.get(1.0,END)
    s.send(t_conent)
    tv_get.insert(1.0,s.recv(1024))

def get():
    ss=s.recv(1024)
    tv_get.insert(1.0,ss)

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('127.0.0.1', 9999))
    # 接收欢迎消息:
    print s.recv(1024)

    # 以下为图形化编程
    root=Tk()
    root.title("echo_client")
    root.geometry('200x200')

    frm=Frame(root)
    frm_l=Frame(frm)
    frm_r=Frame(frm)

    tv_send=Text(frm_r)
    tv_send.insert(1.0,"<<<<")
    tv_send.pack(side=TOP)
    t=tv_send.get(1.0,END)
    Button(frm_l,text="send",command=lambda :send(s,t)).pack(side=TOP)
    Button(frm_l,text="get",command=lambda :get()).pack(side=TOP)

    tv_get=Text(frm_r)
    tv_get.insert(1.0,"<<<<")
    tv_get.pack(side=TOP)

    frm_l.pack(side=LEFT)
    frm_r.pack(side=RIGHT)
    frm.pack()
    root.mainloop()

    s.close()


