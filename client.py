#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a socket example which send echo message to server.'

import socket,threading
import tkFileDialog
import json
from Tkinter import *

def send(s,t):
    # get_before_send()#在发送之前先接受一下消息
    t_conent=tv_send.get(1.0,END)
    addr=[e_ip.get(),e_port.get(),t_conent]
    ip_json=json.dumps(addr)
    s.send(ip_json)
    # try:
    #     ss=s.recv(1024)
    #     ss_json=json.loads(ss)
    #     tv_get.insert(1.0,ss_json[0])
    #     tv_get.insert("\n")
    #     tv_get.insert(1.0,ss_json[1])
    # except ValueError,e:
    #     print "cannot decode <<<<<<<,"
    #     tv_get.insert(1.0,ss)

def get_before_send():
    try:
        ss=s.recv(1024)
        ss_json=json.loads(ss)
        tv_get.insert(1.0,ss_json[0])
        tv_get.insert(1.0,ss_json[1])
        tv_get.insert(END,"\n")
        lb.insert(END,str(ss_json[0])+'/'+str(ss_json[1]))
    except ValueError:
        tv_get.insert(END,ss)
        tv_get.insert(END,"\n")
    except:
        print "no message now"

# 这个get虽然开了一个新的线程，但效果并不总是很好
def get():
    try:
        ss=s.recv(1024)
        ss_json=json.loads(ss)
        tv_get.insert(1.0,ss_json[0])
        tv_get.insert(1.0,ss_json[1])
        tv_get.insert(END,"\n")
        lb.insert(END,str(ss_json[0])+'/'+str(ss_json[1]))
    except ValueError:
        tv_get.insert(END,ss)
        tv_get.insert(END,"\n")
    except:
        get()

def save():
    ss_send=tv_send.get(1.0,END)
    ss_get=tv_get.get(1.0,END)
    f=open("C:\\Users\\steven\\Desktop\\test1.txt",'a')
    f.write(ss_send)
    f.write(ss_get)
    f.close()

def print_item(event):
    ss=lb.get(lb.curselection()).split('/') # ss为元组类型，相当方便
    var1.set(ss[0])
    var2.set(ss[1])

def sendfile():
    # filename=tkFileDialog.askopenfilename()
    f=open('tosend.png','rb')
    l=f.read(512)
    while (l):
        print("sending")
        addr=[e_ip.get(),e_port.get(),l.decode("ISO-8859-1")]
        # addr=[e_ip.get(),e_port.get(),l.decode('latin-1')]
        ip_json=json.dumps(addr)
        s.send(ip_json)
        l=f.read(256)
    f.close()

def refresh(s):
    s.send("refresh")
    ss=s.recv(1024)
    ss_json=json.loads(ss)
    lb.delete(0,END)
    for item in ss_json:
        # tv_get.insert(END,item[0])
        # tv_get.insert(1.0,item[1])
        #如果出现1/2，请再刷新一遍,原因不详
        tv_get.insert(END,"\n")
        lb.insert(END,str(item[0])+'/'+str(item[1]))

def get_file_0():
    f=open("torecv.png",'wb')
    while True:
        l=s.recv(1024).encode("ISO-8859-1")
        while(l):
            print("receving")
            f.write(l)
            l=s.recv(1024)
        f.close()

def get_file():
    f=open("torecv.png",'wb')
    try:
        ss=s.recv(1024)
        f.write(ss)
        tv_get.insert(END,"\n")
    except ValueError:
        tv_get.insert(END,ss)
        tv_get.insert(END,"\n")
    except:
        get()

def use_get_file():
    t=threading.Thread(target=get_file)
    t.start()

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('127.0.0.1', 9999))
    (addr, port) = s.getsockname()
    print addr
    print port

    # 以下为图形化编程
    root=Tk()
    root.title(str(port)+" : "+str(addr))
    root.geometry('200x200')

    frm=Frame(root)
    frm_l=Frame(frm)
    frm_r=Frame(frm)

    tv_send=Text(frm_r)
    tv_send.insert(1.0,"<<<<")
    tv_send.pack(side=TOP)
    t=tv_send.get(1.0,END)

    Button(frm_l,text="send",command=lambda :send(s,t)).pack(side=TOP)
    Button(frm_l,text="get",command=lambda :get_before_send()).pack(side=TOP)
    Button(frm_l,text="save all the text",command=lambda :save()).pack(side=TOP)
    Button(frm_l,text="choose a file",command=lambda :sendfile()).pack(side=TOP)
    Button(frm_l,text="refresh",command=lambda :refresh(s)).pack(side=TOP)
    Button(frm_l,text="getfile",command=lambda :use_get_file()).pack(side=TOP)

    tv_get=Text(frm_r)
    tv_get.insert(1.0,"<<<<")
    tv_get.pack(side=TOP)

    frm_l.pack(side=LEFT)
    frm_r.pack(side=RIGHT)
    frm.pack()

    var=StringVar()
    lb=Listbox(frm_l,height=5,selectmode=BROWSE,listvariable=var)
    lb.bind('<ButtonRelease-1>',print_item)

    scrl=Scrollbar(frm_l)
    scrl.pack(side=RIGHT,fill=Y)
    lb.configure(yscrollcommand=scrl.set)
    lb.pack(side=LEFT,fill=BOTH)
    scrl['command']=lb.yview

    var1=StringVar()
    var2=StringVar()
    e_ip=Entry(frm_r,textvariable=var1)
    e_port=Entry(frm_r,textvariable=var2)
    e_ip.pack()
    e_port.pack()

    # 新开一个线程监听新用户上线的消息消息
    # t = threading.Thread(target=get)
    # t.start()

    root.mainloop()

    s.close()