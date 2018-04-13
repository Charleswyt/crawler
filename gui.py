#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on
Finished on
@author: Wang Yuntao
"""

import tkinter as tk


class GUI:
    def __init__(self):
        pass


def func():
    print("Hello")


window = tk.Tk()                                                                    # 初始化窗口界面

window.title("Facebook Crawl")
window.geometry("500x350")

var_user_name = tk.StringVar()
var_user_name.set("example@python.com")
var_password = tk.StringVar()
tk.Label(window, text="User name: ").place(x=50, y=150)
tk.Label(window, text="Password: ").place(x=50, y=190)

entry_user_name = tk.Entry(window, textvariable=var_user_name)
entry_user_name.place(x=160, y=150)
entry_password = tk.Entry(window, textvariable=var_password, show="*")
entry_password.place(x=160, y=190)


window.mainloop()

