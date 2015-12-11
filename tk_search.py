# -*- coding: utf-8 -*-
__author__ = 'jaundice'
from Tkinter import *

root = Tk()

text = Text(root)
text.insert(INSERT, "Hello, world!\n")
text.insert(END, "This is a cccccccccccccphrase.\n")
text.insert(END, "Byeccc bye...")
text.pack(expand=1, fill=BOTH)

start=1.0
while 1:
    pos=text.search("is",start,stopindex=END)
    length=str(len("is"))
    mov=str("+"+length+"c")
    if not pos:
        break
    print pos
    text.tag_config("start", background="black", foreground="yellow")
    text.tag_add("start", pos,pos+mov)
    # text.tag_add("start", pos,pos+"+1c")
    start=pos+"+1c"

root.mainloop()
