import os, sys, time
import platform
import threading
from mcrcon import MCRcon
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.messagebox as tkm
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText  # 导入多行文本框用到的包
import pyperclip as pc


class app():
    # def __init__(self, command):
    #    command = command[1:len(str(entry.get()))]

    def local_log(self, string):
        if __name__ == "__main__":
            print(str(string))

    def command_use(self, command):
        command = command[1:len(str(entry.get()))]
        app.local_log(command)
        if command == 'help':
            listbox.insert(ttk.END,
'''命令帮助
$help - 帮助
$exit - 退出
$disconnect - 断开连接
''', 'blue')
#$language English/Chinese - 切换语言为英文/中文
            a.set('')
        if command == 'exit':
            mcr.disconnect()
            sys.exit(0)
        if command == 'disconnect':
            mcr.disconnect()
            listbox.insert(ttk.END,'已断开链接', 'blue')
            root.destroy()
            main()
    
    def readconfig():
        if platform.system() == 'Windows':
            try:
                config_file = open("C:/ProgramData/RCON_config.txt",'r+')
                config = config_file.read().split('&&')
                return config
            except BaseException as error:
                config_file = open("C:/ProgramData/RCON_config.txt",'w+')
                config_file.write("127.0.0.1&&25575&&password")
                config_file = open("C:/ProgramData/RCON_config.txt",'r+')
                config = config_file.read().split('&&')
                return config
        return False

    def saveconfig(self,path,string):
        if platform.system() == 'Windows':
            config_file = open(str(path),'w+')
            config_file.write(str(string))
            return True
        return False

def login(*args):
    loginRoot.destroy()                  # 关闭窗口
    global IP, Port, Password, mcr
    curIP = IP.get()
    curPort = Port.get()
    curPassword = Password.get()
    mcr = MCRcon(curIP, curPassword, port=int(curPort))
    app.saveconfig("C:/ProgramData/RCON_config.txt", str(curIP+'&&'+curPort+'&&'+curPassword))


class window():
    def login(self):
        global loginRoot
        global IP, Port, Password

        loginRoot = ttk.Window()
        loginRoot.title('我的世界RCON链接')
        loginRoot.geometry('400x300')
        loginRoot.resizable(0, 0)  # 限制窗口大小
        loginRoot.bind('<Return>', login)            # 回车绑定登录功能

        but1 = ttk.Button(loginRoot, text='登录', command=login)
        but1.place(x=10, y=150, width=70, height=30)

        
        config = app.readconfig()

        IP = ttk.StringVar()
        Port = ttk.StringVar()
        Password = ttk.StringVar()
        
        if not config==False:
            IP.set(config[0])  # 默认显示
            Port.set(config[1])
            Password.set(config[2])
        else:
            IP.set('127.0.0.1')  # 默认显示
            Port.set('25575')
            Password.set('P^$$vvOrd')

        # 服务器标签
        labelIP = ttk.Label(loginRoot, text='服务器地址')
        labelIP.place(x=15, y=10, width=200, height=40)

        entryIP = ttk.Entry(loginRoot, width=80, textvariable=IP)
        entryIP.place(x=120, y=10, width=260, height=40)

        # 端口标签
        labelPort = ttk.Label(loginRoot, text='服务器RCON端口')
        labelPort.place(x=15, y=50, width=160, height=40)

        entryPort = ttk.Entry(loginRoot, width=80, textvariable=Port)
        entryPort.place(x=120, y=50, width=260, height=40)

    # 密码标签
        labelPassword = ttk.Label(loginRoot, text='密码')
        labelPassword.place(x=15, y=90, width=160, height=40)

        entryPassword = ttk.Entry(
            loginRoot, show='*', width=80, textvariable=Password)
        entryPassword.place(x=120, y=90, width=260, height=40)
        loginRoot.mainloop()

    def connect(self):
        global listbox, a, entry
        global root
        root = ttk.Window()
        root.title('RCON Client')  # 窗口命名
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



def send(*args):
    if entry.get()[0] == '$':
        command = entry.get()
        app.command_use(command)
    else:
        try:
            resp = mcr.command(str(entry.get()))
        except BaseException as error:
            listbox.insert(ttk.END, str('发送失败！错误原因：' + error), 'black')
        listbox.insert(ttk.END, str(resp), 'black')
        a.set('')


def github():
    pc.copy('https://github.com/MCommander2077/MinecraftRCONConnect/blob/main/README.md')
    tkm.showinfo('提示', message='GitHub网址已复制到剪贴板，请粘贴至游览器访问！')


def useful_commands():
    pc.copy('https://www.iecraft.com/news/essential.html')
    tkm.showinfo('提示', message='常用指令网址已复制到剪贴板，请粘贴至游览器访问！')


def main():
    global app,window,firstrun
    if firstrun:
        firstrun = False
        app = app()
        window = window()
    else:
        pass
    window.login('')
    try:
        mcr.connect()
    except BaseException as error:
        tkm.showerror('错误！', message=error)
        sys.exit(error)
    window.connect('')


if __name__ == '__main__':
    firstrun = False
    main()
