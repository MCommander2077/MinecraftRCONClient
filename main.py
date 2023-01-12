import os,sys,time
import time
import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
from mcrcon import MCRcon
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.messagebox as tkm
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText  # 导入多行文本框用到的包
import pyperclip as pc

def login(*args):
    loginRoot.destroy()                  # 关闭窗口
    global IP, Port, Password,mcr
    curIP = IP.get()
    curPort = Port.get()
    curPassword = Password.get()
    mcr = MCRcon(curIP,curPassword,port= int(curPort))

def window_login():
    global loginRoot
    global IP,Port,Password

    loginRoot = ttk.Window()
    loginRoot.title('Minecrat Rcon Connecter')
    loginRoot.geometry('400x300')
    loginRoot.resizable(0, 0)  # 限制窗口大小
    loginRoot.bind('<Return>', login)            # 回车绑定登录功能

    but1 = ttk.Button(loginRoot, text='登录', command=login)
    but1.place(x=10, y=150, width=70, height=30)

    IP = ttk.StringVar()
    IP.set('127.0.0.1')  # 默认显示的ip

    Port = ttk.StringVar()
    Port.set('25575')

    Password = ttk.StringVar()
    Password.set('')

    # 服务器标签
    labelIP = ttk.Label(loginRoot, text='服务器地址')
    labelIP.place(x=20, y=10, width=200, height=40)

    entryIP = ttk.Entry(loginRoot, width=80, textvariable=IP)
    entryIP.place(x=120, y=10, width=260, height=40)

    # 端口标签
    labelPort = ttk.Label(loginRoot, text='端口')
    labelPort.place(x=30, y=50, width=160, height=40)

    entryPort = ttk.Entry(loginRoot, width=80, textvariable=Port)
    entryPort.place(x=120, y=50, width=260, height=40)

    # 密码标签
    labelPassword = ttk.Label(loginRoot, text='密码')
    labelPassword.place(x=30, y=90, width=160, height=40)

    entryPassword = ttk.Entry(loginRoot, show='*', width=80, textvariable=Password)
    entryPassword.place(x=120, y=90, width=260, height=40)
    loginRoot.mainloop()

def send(*args):
    if entry.get()[0] == '$':
        command = entry.get()[1:len(entry.get)]
    else:
        resp = mcr.command(str(entry.get()))
        listbox.insert(ttk.END, str(resp), 'red')
        a.set('')

def github():
    pc.copy('https://github.com/MCommander2077/MinecraftRCONConnect/blob/main/README.md')
    tkm.showinfo('提示',message='GitHub网址已复制到剪贴板，请粘贴至游览器访问！')

def window_connect():
    global listbox,a,entry
    root = ttk.Window()
    root.title('Rcon Client')  # 窗口命名
    root['height'] = 400
    root['width'] = 580
    root.resizable(0, 0)  # 限制窗口大小

    # 创建多行文本框
    listbox = ScrolledText(root)
    listbox.place(x=5, y=0, width=570, height=320)
    # 文本框使用的字体颜色
    listbox.tag_config('red', foreground='red')
    listbox.tag_config('blue', foreground='blue')
    listbox.tag_config('green', foreground='green')
    listbox.tag_config('pink', foreground='pink')
    # 创建发送按钮
    button = tk.Button(root, text='发送', command=send)
    button.place(x=515, y=353, width=60, height=30)
    root.bind('<Return>', send)  # 绑定回车发送信息

    # 创建输入文本框和关联变量
    a = ttk.StringVar()
    a.set('连接成功！按enter发送指令')
    entry = ttk.Entry(root, width=120, textvariable=a)
    entry.place(x=5, y=350, width=570, height=40)

    # 查看在线用户按钮
    button1 = tk.Button(root, text='Github', command=github)
    button1.place(x=480, y=320, width=90, height=30)

    # 创建输入文本框和关联变量
    a = ttk.StringVar()
    a.set('')
    entry = ttk.Entry(root, width=120, textvariable=a)
    entry.place(x=5, y=350, width=570, height=40)

    root.mainloop()

if __name__ == '__main__':
    global mcr
    window_login()
    try:
        mcr.connect()
    except BaseException as error:
        tkm.showerror('错误！',message=error)
    window_connect()