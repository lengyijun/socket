# -*- coding: utf-8 -*-
#!/usr/bin/python

'a socket example which send echo message to server.'

import socket,threading
import tkFileDialog
import json,time
from Tkinter import *
import tkFont
import base64

def send(s,t):
    # get_before_send()#在发送之前先接受一下消息
    t_conent=tv_send.get(1.0,END)
    addr=[e_ip.get(),e_port.get(),t_conent]
    ip_json=json.dumps(addr)
    s.send(ip_json)

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
        pass

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
    filename=tkFileDialog.askopenfilename()
    f=open(filename,'rb')
    l=f.read(2048)
    while (l):
        # print("sending")
        addr=[e_ip.get(),e_port.get(),l.encode("base64")]
        ip_json=json.dumps(addr)
        s.send(ip_json)
        l=f.read(2048)
        # time.sleep(2)
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

def get_file():
    f=open("torecv.txt",'ab')
    while True:
        l=s.recv(2048)
        while(l):
            # print("receving")
            imgdata = base64.b64decode(l)
            f.write(imgdata)
            l=s.recv(2048)
    f.close()

def use_get_file():
    t=threading.Thread(target=get_file)
    t.start()

def make_bold():
    current_tags = tv_get.tag_names("sel.first")
    if "bt" in current_tags:
        tv_get.tag_remove("bt", "sel.first", "sel.last")
    else:
        tv_get.tag_add("bt", "sel.first", "sel.last")

def seach_text():
    search_content=search_box.get()
    start=1.0
    tv_get.tag_config("start", background="black", foreground="yellow")
    tv_send.tag_config("start", background="black", foreground="yellow")
    while 1:
        pos=tv_get.search(search_content,start,stopindex=END)
        length=str(len(search_content))
        mov=str("+"+length+"c")
        if not pos:
            break
        # print pos
        tv_get.tag_add("start", pos,pos+mov)
        start=pos+mov
    # print "finish"
    start=1.0
    while 1:
        # print "start"
        pos=tv_send.search(search_content,start,stopindex=END)
        length=str(len(search_content))
        mov=str("+"+length+"c")
        if not pos:
            break
        tv_send.tag_add("start", pos,pos+mov)
        start=pos+mov


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('127.0.0.1', 9999))
    (addr, port) = s.getsockname()

    # 以下为图形化编程
    root=Tk()
    root.title(str(port)+" : "+str(addr))

    # image2 =Image.open('sjtu.gif')
    # w = image2.width
    # h = image2.height
    # print(w)
    # print(h)
    root.geometry('%dx%d+0+0' % (750,500))

    p=PhotoImage(file="sjtu.gif")

    l=Label(root,image=p)

    tv_send=Text(l,font=("Georgia", "12"),height=12,width=42)
    tv_send.insert(1.0,"<<<<")
    tv_send.place(x=20,y=20)
    t=tv_send.get(1.0,END)

    tv_get=Text(l,font=("Georgia", "12"),height=10,width=42)
    tv_get.insert(1.0,"<<<<")
    tv_get.place(x=20,y=260)

    Button(l,text="send",width=19,command=lambda :send(s,t)).place(x=520,y=20)
    Button(l,text="get",width=19,command=lambda :get_before_send()).place(x=520,y=50)
    Button(l,text="save all the text",width=19,command=lambda :save()).place(x=520,y=80)
    Button(l,text="choose a file",width=19,command=lambda :sendfile()).place(x=520,y=110)
    Button(l,text="refresh",width=19,command=lambda :refresh(s)).place(x=520,y=140)
    Button(l,text="getfile",width=19,command=lambda :use_get_file()).place(x=520,y=170)
    Button(l,text="bold",width=19, command=make_bold).place(x=520,y=200)

    var3=StringVar()
    search_box=Entry(l,textvariable=var3)
    search_box.place(x=520,y=240)
    Button(l, text="search", width=19,command=seach_text).place(x=520,y=265)

    bold_font = tkFont.Font(tv_get, tv_get.cget("font"))
    bold_font.configure(weight="bold")
    tv_get.tag_configure("bt", font=bold_font)

    bold_font_send= tkFont.Font(tv_send, tv_send.cget("font"))
    bold_font_send.configure(weight="bold")
    tv_send.tag_configure("bt_send", font=bold_font_send)


    var=StringVar()
    lb=Listbox(l,height=5,selectmode=BROWSE,listvariable=var)
    lb.bind('<ButtonRelease-1>',print_item)

    scrl=Scrollbar(lb)
    scrl.place(x=600,y=295)
    lb.configure(yscrollcommand=scrl.set)
    lb.place(x=520,y=295)
    scrl['command']=lb.yview

    var1=StringVar()
    var2=StringVar()
    e_ip=Entry(l,textvariable=var1)
    e_port=Entry(l,textvariable=var2)
    e_ip.place(x=520,y=395)
    e_port.place(x=520,y=410)

    l.pack_propagate(0)
    l.pack()

    root.mainloop()

    s.close()
