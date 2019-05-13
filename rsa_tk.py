#!/usr/bin/env python
# coding=utf-8
"""
synopsis: rsa加解密工具(可视化版)
author: haoranzeus@gmail.com (zhanghaoran)
"""
import json
import os
import tkinter
from tkinter import filedialog

import rsa_tool


class AboutShow:
    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.title('关于')
        self.setup_ui()

    def setup_ui(self):
        tkinter.Label(self.root, text='作者').pack(side=tkinter.TOP)
        tkinter.Label(self.root, text='张浩然').pack(side=tkinter.TOP)
        tkinter.Label(self.root, text='haoranzeus@gmail.com').pack()


class show:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('WoodenRSA')
        # 配置文件
        if not os.path.isfile('rsatool_conf.json'):
            path_dict = {
                'pubkey_path': '',
                'privkey_path': ''
            }
            pathes = json.dumps(path_dict)
            with open('rsatool_conf.json', 'w+') as f:
                f.write(pathes)

        # 菜单栏
        self.menubar = tkinter.Menu(self.root)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='帮助', menu=self.filemenu)
        self.filemenu.add_command(label='关于', command=self.about)
        self.root.config(menu=self.menubar)     # 将菜单显示出来

        self.frm = tkinter.Frame(self.root)
        # Top
        tkinter.Label(self.root, text='WoodenRSA--RSA加解密小工具', font=('Arial', 15)).pack()
        # 公钥路径
        self.pubkey_path = tkinter.StringVar()
        self.frm_title1 = tkinter.Frame(self.root)
        tkinter.Label(self.frm_title1, text='公钥路径:').pack(side=tkinter.LEFT)
        tkinter.Entry(self.frm_title1, textvariable=self.pubkey_path, width=70
                      ).pack(side=tkinter.LEFT)
        tkinter.Button(self.frm_title1, text='打开公钥', width=8, height=1,
                       command=self.openpubkey).pack()
        self.frm_title1.pack()
        # 私钥路径
        self.privkey_path = tkinter.StringVar()
        self.frm_title2 = tkinter.Frame(self.root)
        tkinter.Label(self.frm_title2, text='私钥路径:').pack(side=tkinter.LEFT)
        tkinter.Entry(self.frm_title2, textvariable=self.privkey_path, width=70
                      ).pack(side=tkinter.LEFT)
        tkinter.Button(self.frm_title2, text='打开私钥', width=8, height=1,
                       command=self.openprivkey).pack()
        self.frm_title2.pack()
        self.frm = tkinter.Frame(self.root)
        # Left
        self.frm_l = tkinter.Frame(self.frm)
        tkinter.Label(self.frm_l, text='密文',
                      font=('Arial', 12)).pack(side=tkinter.TOP)
        self.ciphertext = tkinter.Text(
                self.frm_l, width=20, height=5, font=('Verdana', 15))
        self.ciphertext.pack(side=tkinter.BOTTOM)

        self.frm_l.pack(side=tkinter.LEFT)
        # Middle
        self.frm_m = tkinter.Frame(self.frm)
        tkinter.Button(self.frm_m, text='密文->明文', width=10, height=1,
                       command=self.decrypt).pack()
        tkinter.Button(self.frm_m, text='密文<-明文', width=10, height=1,
                       command=self.encrypt).pack()
        self.frm_m.pack(side=tkinter.LEFT)
        # Right
        self.frm_r = tkinter.Frame(self.frm)
        tkinter.Label(self.frm_r, text='明文',
                      font=('Arial', 12)).pack(side=tkinter.TOP)
        self.cleartext = tkinter.Text(
                self.frm_r, width=20, height=5, font=('Verdana', 15))
        self.cleartext.pack(side=tkinter.BOTTOM)
        self.frm_r.pack()
        # pack
        self.frm.pack(side=tkinter.RIGHT)
        self.datainit()

    def datainit(self):
        # 读取配置，设置公钥私钥路径
        with open('rsatool_conf.json', 'r') as f:
            conf_text = f.read()
            conf_dict = json.loads(conf_text)
            self.pubkey_path.set(conf_dict['pubkey_path'])
            self.privkey_path.set(conf_dict['privkey_path'])

    def reset_path(self):
        """
        重置公钥私钥路径
        """
        privkey_path = self.privkey_path.get()
        pubkey_path = self.pubkey_path.get()
        path_dict = {
            'pubkey_path': pubkey_path,
            'privkey_path': privkey_path
        }
        path_text = json.dumps(path_dict)
        with open('rsatool_conf.json', 'w+') as f:
            f.write(path_text)

    def openpubkey(self):
        path = filedialog.askopenfilename(title='选择公钥文件')
        self.pubkey_path.set(path)
        self.reset_path()

    def openprivkey(self):
        path = filedialog.askopenfilename(title='选择私钥文件')
        self.privkey_path.set(path)
        self.reset_path()

    def decrypt(self):
        privkey_path = self.privkey_path.get()
        ciphertext = self.ciphertext.get('1.0', tkinter.END)
        rsatool = rsa_tool.RsaTool(priv_file=privkey_path)
        cleartext = rsatool.decryptone(str(ciphertext).strip())
        self.cleartext.delete('1.0', tkinter.END)
        self.cleartext.insert('1.0', cleartext)

    def encrypt(self):
        pubkey_path = self.pubkey_path.get()
        cleartext = self.cleartext.get('1.0', tkinter.END)
        rsatool = rsa_tool.RsaTool(pub_file=pubkey_path)
        ciphertext = rsatool.encryptone(str(cleartext).strip())
        self.ciphertext.delete('1.0', tkinter.END)
        self.ciphertext.insert('1.0', ciphertext)

    def about(self):
        about_show = AboutShow()
        self.root.wait_window(about_show)

    def get_txt_pubkey(self):
        return self.pubkey.get()


def main():
    show()
    tkinter.mainloop()


if __name__ == '__main__':
    main()
