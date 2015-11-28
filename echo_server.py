# -*- coding: utf-8 -*-
#!/usr/bin/env python

# 写的极好，开一个echo_server可以监听多个client发送的信息
'a server example which send hello to client.'

import time, socket, threading
import json
from Tkinter import *

# 保留sock的字典对象
sock_dict={}
# event这个参数不能忘记
def print_item(event):
    ss=lb.get(lb.curselection()) # ss为元组类型，相当方便
    var1.set(ss[0])
    var2.set(ss[1])
    var3.set(ss)

def opensocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print 'Waiting for connection...'
    while True:
        # todo
        # 接受一个新连接:
        sock, addr = s.accept()
        ip_json=json.dumps(addr)
        for i in sock_dict:
            sock_dict[i].send(ip_json)

            exist_ip=json.dumps(i)
            sock.send(exist_ip)
        lb.insert(END,addr)
        sock_dict[addr]=sock
        print sock_dict
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
        try:
           data_json=json.loads(data)
           print data_json
           ip=(data_json[0],int(data_json[1]))
           print ip
           sock_sendto=sock_dict[ip]
           print sock_sendto
           sock_sendto.send(data_json[2])
           print data_json[2]
        except ValueError,e:
            print data+" is not json"

        time.sleep(1)
        if data == 'exit' or not data:
            print ("exit")
            break
        tv_get.insert(1.0,addr[0]+" "+str(addr[1])+" "+data)
        print (addr[0]+" "+str(addr[1])+" "+data)
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

def save():
    f=open("C:\\Users\\steven\\Desktop\\test2.txt",'a')
    ss_send=tv_send.get(1.0,END)
    ss_get=tv_get.get(1.0,END)
    f.write(ss_send)
    f.write(ss_get)
    f.close()

def send():
    ip=(e_ip.get(),int(e_port.get())) # 类型有点怪，但的确是对的
    sock=sock_dict[ip]
    ss_send=tv_send.get(1.0,END)
    sock.send(ss_send)
    tv_send.delete(1.0,END)

if __name__ == '__main__':
    root=Tk()
    root.title("server<<<")
    root.geometry('200x200')

    frm=Frame(root)
    frm_l=Frame(frm)
    frm_r=Frame(frm)

    Button(frm_r,text="start socket",command=lambda :socket_thread()).pack(side=TOP)
    Button(frm_r,text="send message",command=lambda :send()).pack(side=TOP)
    Button(frm_r,text="save the message",command=lambda :save()).pack(side=TOP)

    tv_get=Text(frm_l)
    tv_get.insert(1.0,"init")
    tv_get.pack(side=TOP)

    tv_send=Text(frm_l)
    tv_send.insert(1.0,"init")
    tv_send.pack(side=TOP)

    # 一个显示ip，一个显示端口
    var1=StringVar()
    var2=StringVar()
    e_ip=Entry(frm_r,textvariable=var1)
    e_port=Entry(frm_r,textvariable=var2)
    e_ip.pack()
    e_port.pack()

    # ip和端口一起显示
    var3=StringVar()
    e=Entry(frm_r,textvariable=var3)
    e.pack()

    var=StringVar()
    lb=Listbox(frm_r,height=5,selectmode=BROWSE,listvariable=var)
    lb.bind('<ButtonRelease-1>',print_item)

    scrl=Scrollbar(frm_r)
    scrl.pack(side=RIGHT,fill=Y)
    lb.configure(yscrollcommand=scrl.set)
    lb.pack(side=LEFT,fill=BOTH)
    scrl['command']=lb.yview

    frm_r.pack(side=RIGHT)
    frm_l.pack(side=LEFT)
    frm.pack()
    root.mainloop()
