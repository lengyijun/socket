# -*- coding: utf-8 -*-
__author__ = 'jaundice'
import Tkinter as tk
import tkFont

def make_bold():
    current_tags = aText.tag_names("sel.first")
    if "bt" in current_tags:
        aText.tag_remove("bt", "sel.first", "sel.last")
    else:
        aText.tag_add("bt", "sel.first", "sel.last")

root = tk.Tk()

# aText = tk.Text(root, font=("Georgia", "12"))
aText = tk.Text(root, )
aText.grid()

aButton = tk.Button(root, text="bold", command=make_bold)
aButton.grid()

bold_font = tkFont.Font(aText, aText.cget("font"))
bold_font.configure(weight="bold")
aText.tag_configure("bt", font=bold_font)

root.mainloop()
