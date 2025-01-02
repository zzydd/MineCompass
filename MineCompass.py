import os
import re
import sys
import json
import time
import socket
import ctypes
import base64
import winreg
import hashlib
import colorsys
import requests
import win32api
import win32con
import threading
import pyperclip
import subprocess
import numpy as np
import win32com.client
from PIL import Image
import multiprocessing
import customtkinter as ctk
from cryptography.fernet import Fernet




"【全局变量】"

#【获取主机名称】
HostName = socket.gethostname()
MainProgram = os.path.realpath(sys.argv[0])

#【网络请求超时设置】
MainTimeout = 3
'''
光速：1s
音速：3s
飞速：5s
快速：10s
'''

#【网络扫描超时设置】
MainScanTimeout = 0.5
'''
光速：0.25s
音速：0.50s
飞速：1.00s
快速：2.00s
'''

#【设备相关变量】
MainState = False           # 主状态
MainAddress = "127.0.0.1"   # 设备地址
Address_ManualMode = False #是否手动指定设备地址

#【扫描相关变量】
MainNetwork = "192.168.1" #扫描网段
Network_ManualMode = False #是否手动指定网段
MainScanState = False #扫描总状态
MainScanProgressList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #扫描进度列表
MainProgress = 0 # 扫描进度(0-100,float)

#【高德API密钥】
# API密钥变量
Gaode_api_key = ("")
Private_api_key = False # 是否使用了个人密钥
# 内置API密钥密码
api_key_pwd = b'hoBDtNEakahKVQZF0sLTSRDEGJOEGmOX7W1EihSyrkE='

#【安装状态】
Main_Install_state = False
Main_StartMenu_state = False
Connect_Detecting_State = True

MainPageIndex = 0


#【UI窗口】
class MainWindow(ctk.CTk):
    def __init__(self):
        """创建基本窗口与控件"""
        super().__init__()
        #【基本窗口配置】
        self.title("Mine Compass")  #标题
        self.geometry("800x600")    #大小
        self.minsize(800, 600)  #最小限制
        self.iconbitmap(Load_Image("assets/logo.ico"))   #窗口图标
        self.grid_rowconfigure(0, weight=1) #允许上下拉伸
        self.grid_columnconfigure(1, weight=1)  #允许左右拉伸

        # 菜单框架
        self.menu = ctk.CTkFrame(self, width=200, corner_radius=0)  # 创建左侧菜单框
        self.menu.grid(row=0, column=0, sticky="nswe")  # 菜单框填充左侧区域

        #【加载图标】
        # 菜单图标
        self.general_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/compass.png")), size=(25, 25))  #首页
        self.network_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/network.png")), size=(25, 25))  #网络页
        self.location_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/location.png")), size=(25, 25))    #位置页
        self.colorpalette_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/colorpalette.png")), size=(25, 25))    #颜色页
        self.settings_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/settings.png")), size=(25, 25))    #设置页
        self.information_icon = ctk.CTkImage(Image.open(Load_Image("assets/menu/information.png")), size=(25, 25))  #信息页
        # 工具图标
        self.hide_icon = ctk.CTkImage(Image.open(Load_Image("assets/module/hide.png")), size=(20, 20))  #隐藏图标
        self.show_icon = ctk.CTkImage(Image.open(Load_Image("assets/module/show.png")), size=(20, 20))  #显示图标
        self.HSV_palette = ctk.CTkImage(Image.open(Load_Image("assets/module/HSV_palette.png")), size=(256, 256))   #HSV调色盘
        # 标题图标
        self.change_icon = ctk.CTkImage(Image.open(Load_Image("assets/title/change_wifi.png")), size=(25, 25))  #更改wifi图标
        self.set_location_icon = ctk.CTkImage(Image.open(Load_Image("assets/title/set_location.png")), size=(25, 25))   #设置位置图标
        # 贡献者图标
        self.icon_main = ctk.CTkImage(Image.open(Load_Image("assets/menu/compass.png")),size=(35, 35))  #项目图标
        self.icon_zzydd = ctk.CTkImage(Image.open(Load_Image("assets/contributor/zzydd.png")),size=(35, 35))    #ZZYDD
        self.icon_fish = ctk.CTkImage(Image.open(Load_Image("assets/contributor/fish.png")),size=(35, 35))  #spitting_Fish
        self.icon_github = ctk.CTkImage(Image.open(Load_Image("assets/contributor/github.png")),size=(35, 35))  #github
        self.icon_gaode = ctk.CTkImage(Image.open(Load_Image("assets/contributor/gaode.png")),size=(35, 35))    #高德
        self.icon_chatgpt = ctk.CTkImage(Image.open(Load_Image("assets/contributor/chatgpt.png")),size=(35, 35))    #chatgpt
        self.icon_igoutu = ctk.CTkImage(Image.open(Load_Image("assets/contributor/igoutu.png")),size=(35, 35))  #igoutu

        # 创建菜单按钮
        self.menu_buttons = []
        for i, (name, icon) in enumerate([("设备信息", self.general_icon),
                                          ("网络设置", self.network_icon),
                                          ("位置设置", self.location_icon),
                                          ("颜色设置", self.colorpalette_icon),
                                          ("更多选项", self.settings_icon),
                                          ("程序信息", self.information_icon)
                                          ]):
            menu_button = ctk.CTkButton(self.menu,
                                        text=name,
                                        height=45,
                                        width=130,
                                        anchor="w",
                                        image=icon,
                                        compound="left",
                                        font=("Microsoft YaHei UI", 16, "bold"),
                                        command=lambda idx=i: self.show_page(idx))
            menu_button.pack(fill="x", pady=15, padx=25)  # 按钮填充整个宽度
            self.menu_buttons.append(menu_button)  # 添加按钮到列表中

        # 右侧内容区域
        self.content_area = ctk.CTkFrame(self)
        self.content_area.grid(row=0, column=1, sticky="nswe")  # 填充右侧区域

        # 初始化页面
        self.pages = []
        self.create_pages()
        self.show_page(0)   #默认页


    def create_pages(self):
        """创建每个页面的内容"""

        """【设备信息页】"""
        # 页面索引
        general_page = ctk.CTkFrame(self.content_area)

        # 主标题-边框(A0)
        label_main_frame = ctk.CTkFrame(general_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0")
        label_main_frame.pack(pady=(15, 15), padx=(0, 0), anchor="center")
        # 主标题+图标(A0)
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="设备信息",
                                  text_color="white",
                                  padx=20,
                                  compound="left",
                                  image=self.general_icon,
                                  font=("Microsoft YaHei UI", 20, "bold"))
        label_main.pack(padx=(5, 10), pady=5)

        #设置文本框参数
        label_all_w = 500  # 边框-长度
        label_all_h = 40  # 边框-宽度

        # 连接状态-边框(A1)
        label_A1_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A1_frame.pack_propagate(False)
        label_A1_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 连接状态-文本(A1)
        label_A1 = ctk.CTkLabel(label_A1_frame,
                                text="连接状态：未连接",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A1.pack(side="left", padx=(5, 5), pady=0)
        # 连接状态-复制按钮(A1)
        button_A1 = ctk.CTkButton(label_A1_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A1_text())
        button_A1.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A1_text():
            label_A1_text = label_A1.cget("text")
            Copy_to_Clipboard(label_A1_text)

        # 设备地址-边框(A2)
        label_A2_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A2_frame.pack_propagate(False)
        label_A2_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 设备地址-文本(A2)
        label_A2 = ctk.CTkLabel(label_A2_frame,
                                text="设备地址：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A2.pack(side="left", padx=(5, 5), pady=0)
        # 设备地址-复制按钮(A2)
        button_A2 = ctk.CTkButton(label_A2_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A2_text())
        button_A2.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A2_text():
            label_A2_text = label_A2.cget("text")
            label_A2_text = label_A2_text.replace('设备地址：', '')
            Copy_to_Clipboard(label_A2_text)


        # 固件版本-边框(A3)
        label_A3_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A3_frame.pack_propagate(False)
        label_A3_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 固件版本-文本(A3)
        label_A3 = ctk.CTkLabel(label_A3_frame,
                                text="固件版本：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A3.pack(side="left", padx=(5, 5), pady=0)
        # 固件版本-复制按钮(A3)
        button_A3 = ctk.CTkButton(label_A3_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A3_text())
        button_A3.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A3_text():
            label_A3_text = label_A3.cget("text")
            label_A3_text = label_A3_text.replace('固件版本：', '')
            Copy_to_Clipboard(label_A3_text)

        # 构建时间-边框(A4)
        label_A4_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A4_frame.pack_propagate(False)
        label_A4_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 构建时间-文本(A4)
        label_A4 = ctk.CTkLabel(label_A4_frame,
                                text="构建时间：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A4.pack(side="left", padx=(5, 5), pady=0)
        # 构建时间-复制按钮(A4)
        button_A4 = ctk.CTkButton(label_A4_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A4_text())
        button_A4.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A4_text():
            label_A4_text = label_A4.cget("text")
            label_A4_text = label_A4_text.replace('构建时间：', '')
            Copy_to_Clipboard(label_A4_text)

        # 版本分支-边框(A5)
        label_A5_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A5_frame.pack_propagate(False)
        label_A5_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 版本分支-文本(A5)
        label_A5 = ctk.CTkLabel(label_A5_frame,
                                text="版本分支：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A5.pack(side="left", padx=(5, 5), pady=0)
        # 版本分支-复制按钮(A5)
        button_A5 = ctk.CTkButton(label_A5_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A5_text())
        button_A5.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A5_text():
            label_A5_text = label_A5.cget("text")
            label_A5_text = label_A5_text.replace('版本分支：', '')
            Copy_to_Clipboard(label_A5_text)

        # 版本哈希-边框(A6)
        label_A6_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A6_frame.pack_propagate(False)
        label_A6_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 版本哈希-文本(A6)
        label_A6 = ctk.CTkLabel(label_A6_frame,
                                text="版本哈希：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A6.pack(side="left", padx=(5, 5), pady=0)
        # 版本分支-复制按钮(A6)
        button_A6 = ctk.CTkButton(label_A6_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_A6_text())
        button_A6.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_A6_text():
            label_A6_text = label_A6.cget("text")
            label_A6_text = label_A6_text.replace('版本哈希：', '')
            Copy_to_Clipboard(label_A6_text)

        # 扫描速度-边框(A7)
        label_A7_frame = ctk.CTkFrame(general_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_A7_frame.pack_propagate(False)
        label_A7_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 扫描速度-文本(A7)
        label_A7 = ctk.CTkLabel(label_A7_frame,
                                text="扫描速度：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_A7.pack(side="left", padx=(5, 5), pady=0)
        # 扫描速度设置回调函数
        def checkbox_A7_callback(var, index, mode):
            # 获取设置值
            value = checkbox_A7_selected.get()
            # 设置全局延时设置
            Set_MainTimeout(value)
        # 扫描速度-复选框(A7)
        checkbox_A7_List = []
        checkbox_A7_selected = ctk.IntVar(value=2) # 默认值
        checkbox_A7_texts = ["光速", "音速", "飞速", "快速"]
        checkbox_A7_selected.trace_add("write", checkbox_A7_callback) # 回调函数
        checkbox_A7_frame = ctk.CTkFrame(label_A7_frame, fg_color="transparent")
        checkbox_A7_frame.pack(side="left", padx=(0, 5), pady=10, anchor="center")
        for i, text in enumerate(checkbox_A7_texts):
            checkbox = ctk.CTkRadioButton(checkbox_A7_frame,
                                          text=text,
                                          value=i + 1,  #索引
                                          border_color="grey",
                                          radiobutton_width=20,
                                          radiobutton_height=20,
                                          font=("Microsoft YaHei UI", 14),
                                          variable=checkbox_A7_selected)    #绑定变量
            checkbox.pack(side="left", padx=2)
            checkbox_A7_List.append(checkbox)

        # 扫描按钮(A8)
        button_A8 = ctk.CTkButton(general_page,
                                  text="扫描设备",
                                  height=40,
                                  width=150,
                                  font=("Microsoft YaHei UI", 20, "bold"),
                                  command=lambda: button_A8_Command())
        button_A8.pack(side="top", anchor="center", padx=(5, 5), pady=(40, 0))
        self.button_A8 = button_A8
        # 扫描按钮-按钮功能(A8)
        def button_A8_Command():
            if MainScanState:
                print(f"{MainScanState}")
                print("正在扫描,无需重复开启")
                pass
            else:
                # 指定IP模式
                if Address_ManualMode:
                    connect_ip_thread = threading.Thread(target=button_A8_Command_Manual)
                    connect_ip_thread.daemon = True
                    connect_ip_thread.start()
                # 扫描模式
                else:
                    # 启动扫描线程
                    scan_main_thread = threading.Thread(target=button_A8_Command_ScanMain)  # 创建进度统计线程
                    scan_main_thread.daemon = True  # 设置为daemon线程
                    scan_main_thread.start()  # 启动进度统计线程
                    # 启动UI更新线程
                    update_ui_thread = threading.Thread(target=button_A8_Command_Progress)  # 创建进度统计线程
                    update_ui_thread.daemon = True  # 设置为daemon线程
                    update_ui_thread.start()  # 启动进度统计线程

        # 扫描按钮-指定IP(A8)
        def button_A8_Command_Manual():
            global MainState
            print(f"指定IP模式：{MainAddress}")
            # 更新显示
            label_A1.configure(text=f"连接状态：连接中... (指定IP)")
            label_A2.configure(text=f"设备地址：{MainAddress}")
            button_A8.configure(text="正在连接",state="disabled")
            # 获取信息
            InfoList = list(GET_Info(MainAddress))
            # 判断请求
            if InfoList[0]:
                # 更新信息
                label_A1.configure(text=f"连接状态：连接成功 (指定IP)")
                label_A2.configure(text=f"设备地址：{MainAddress}")
                label_A3.configure(text=f"固件版本：{InfoList[3]}")
                label_A4.configure(text=f"构建时间：{InfoList[1]} {InfoList[2]}")
                label_A5.configure(text=f"版本分支：{InfoList[4]}")
                label_A6.configure(text=f"版本哈希：{InfoList[5]}")
                MainState = True
                print("连接成功")
            else:
                # 更新信息
                PageA_Default_UI(text="连接失败 (指定IP)")
                print("连接失败")
                Warning_Window("设备连接失败！", "Mine Compass", False)
            # 恢复按钮
            button_A8.configure(text="连接设备", state="normal")

        # 扫描按钮-扫描线程(A8)
        self.FailedTimes = 0  # 扫描失败统计
        def button_A8_Command_ScanMain():
            # 启动扫描
            state,ip = Scan_Network()
            # 判断扫描结果
            if state:
                # 获取信息
                InfoList = list(GET_Info(ip))
                # 判断请求
                if InfoList[0]:
                    # 更新信息
                    self.FailedTimes = 0
                    if Network_ManualMode:
                        label_A1.configure(text=f"连接状态：连接成功 (指定网段)")
                    else:
                        label_A1.configure(text=f"连接状态：连接成功")
                    label_A2.configure(text=f"设备地址：{ip}")
                    label_A3.configure(text=f"固件版本：{InfoList[3]}")
                    label_A4.configure(text=f"构建时间：{InfoList[1]} {InfoList[2]}")
                    label_A5.configure(text=f"版本分支：{InfoList[4]}")
                    label_A6.configure(text=f"版本哈希：{InfoList[5]}")
                else:
                    if Network_ManualMode:
                        PageA_Default_UI(f"连接失败 (指定网段)")
                    else:
                        PageA_Default_UI()
                    self.FailedTimes = self.FailedTimes + 1 # 失败计数
            else:
                if Network_ManualMode:
                    PageA_Default_UI(f"连接失败 (指定网段)")
                else:
                    PageA_Default_UI()
                self.FailedTimes = self.FailedTimes + 1  # 失败计数
                # 弹窗提醒
                if self.FailedTimes >= 3:
                    Warning_Window("请检查设备是否开机并进入配置模式！", "Mine Compass", True)
                else:
                    pass
                if self.FailedTimes == 3:
                    Info_Window("配置模式：请先连接数据线再开机！","Mine Compass", True)
                elif self.FailedTimes == 10:
                    Info_Window("你已经尝试了10次了！要不先检查一下设备？", "Mine Compass", True)
                elif self.FailedTimes == 100:
                    Questions_Window("布氏戈钔！你在干什么？你TM扫了100次了！", "Mine Compass WTF?", True)
                    Error_Window("你是傻逼吗！不知道检查一下吗？你扫你妈呢你！", "Mine Compass 114514!", True)
                else:
                    pass

        # 扫描按钮-进度更新线程(A8)
        def button_A8_Command_Progress():
            # 更新界面
            print("开始扫描-更新界面")
            PageA_Default_UI(text=f"扫描中...")
            label_A2.configure(text=f"扫描网段：{MainNetwork}.0/24")
            time.sleep(0.25)
            # 持续更新扫描进度
            while MainScanState:
                button_A8.configure(text=f"扫描进度 {'%.1f'% MainProgress}%",
                                    font=("Microsoft YaHei UI", 16, "bold"))
                time.sleep(0.2)
            # 扫描完成处理
            time.sleep(0.2)
            button_A8.configure(text=f"扫描进度 100%",
                                font=("Microsoft YaHei UI", 16, "bold"))
            time.sleep(0.5)
            button_A8.configure(text=f"扫描完成",
                                font=("Microsoft YaHei UI", 20, "bold"))
            time.sleep(1)
            if Network_ManualMode:
                button_A8.configure(text=f"扫描网段",
                                    font=("Microsoft YaHei UI", 20, "bold"))
            else:
                button_A8.configure(text=f"扫描设备",
                                    font=("Microsoft YaHei UI", 20, "bold"))

        # 页面A默认UI
        def PageA_Default_UI(text="连接失败"):
            global MainState
            # 更新信息
            label_A1.configure(text=f"连接状态：{text}")
            label_A2.configure(text=f"设备地址：")
            label_A3.configure(text=f"固件版本：")
            label_A4.configure(text=f"构建时间：")
            label_A5.configure(text=f"版本分支：")
            label_A6.configure(text=f"版本哈希：")
            MainState = False
        self.PageA_Default_UI = PageA_Default_UI

        # 添加页面A
        self.pages.append(general_page)  # 添加页面到页面列表

        """【网络设置页】"""
        #页面索引
        network_page = ctk.CTkFrame(self.content_area)
        #主标题-边框(B0)
        label_main_frame = ctk.CTkFrame(network_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0")
        label_main_frame.pack(anchor="center", padx=(0, 0), pady=15,)
        #主标题+图标(B0)
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="当前网络",
                                  text_color="white",
                                  padx=20,
                                  compound="left",
                                  image=self.network_icon,
                                  font=("Microsoft YaHei UI", 20, "bold"),)
        label_main.pack(padx=(5, 10), pady=5)

        # 设备地址-边框(B1)
        label_B1_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_B1_frame.pack_propagate(False)
        label_B1_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 设备地址-文本(B1)
        label_B1 = ctk.CTkLabel(label_B1_frame,
                                text="设备地址：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_B1.pack(side="left", padx=(5, 5), pady=0)
        self.label_B1 = label_B1
        # 设备地址-复制按钮(B1)
        button_B1 = ctk.CTkButton(label_B1_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda:copy_B1_text())
        button_B1.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_B1_text():
            label_B1_text = label_B1.cget("text")
            label_B1_text = label_B1_text.replace('设备地址：', '')
            Copy_to_Clipboard(label_B1_text)

        # 当前WLAN名称-边框(B2)
        label_B2_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_B2_frame.pack_propagate(False)
        label_B2_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 当前WLAN名称-文本(B2)
        label_B2 = ctk.CTkLabel(label_B2_frame,
                                text="WLAN连接：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_B2.pack(side="left", padx=(5, 5), pady=0)
        self.label_B2 = label_B2
        # 当前WLAN名称-复制按钮(B2)
        button_B2 = ctk.CTkButton(label_B2_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_B2_text())
        button_B2.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_B2_text():
            label_B2_text = label_B2.cget("text")
            label_B2_text = label_B2_text.replace('WLAN连接：', '')
            Copy_to_Clipboard(label_B2_text)

        # 当前WLAN密码-边框(B3)
        label_B3_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_B3_frame.pack_propagate(False)
        label_B3_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 当前WLAN密码-文本(B3)
        label_B3 = ctk.CTkLabel(label_B3_frame,
                                text="WLAN密码：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_B3.pack(side="left", padx=(5, 5), pady=0)
        self.label_B3 = label_B3
        # 当前WLAN密码-复制按钮(B3)
        button_B3 = ctk.CTkButton(label_B3_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_B3_text())
        button_B3.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_B3_text():
            Copy_to_Clipboard(self.label_B3_password)

        # 当前WLAN密码-显隐按钮(B3)
        self.hide_pwd_B3_state = True
        button_B3_1 = ctk.CTkButton(label_B3_frame,
                                    text="",
                                    width=32,
                                    height=32,
                                    image=self.hide_icon,
                                    fg_color="transparent",
                                    hover_color="lightgrey",
                                    font=("Microsoft YaHei UI", 14),
                                    command=lambda: hide_show_pwd_B3())
        button_B3_1.pack(side="right", padx=(5, 5), pady=0)

        # 当前WLAN密码-密码显隐功能方法(B3)
        self.label_B3_password = ""
        def hide_show_pwd_B3():
            if self.hide_pwd_B3_state:  # 当前隐藏-切换为显示
                self.hide_pwd_B3_state = False
                label_B3.configure(text=f"WLAN密码：{self.label_B3_password}")  # 显示密码
                button_B3_1.configure(image=self.show_icon)  # 切换按钮图标
            else:  # 当前显示-切换为隐藏
                self.hide_pwd_B3_state = True
                encrypt_pwd = ('・' * len(f"{self.label_B3_password}"))  # 替换密码
                label_B3.configure(text=f"WLAN密码：{encrypt_pwd}")  # 隐藏密码
                button_B3_1.configure(image=self.hide_icon)  # 切换按钮图标

        # 切换网络标题-边框(B4)
        label_B4_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=1,
                                      fg_color="#3B8ED0")
        label_B4_frame.pack(anchor="center", padx=(0, 0), pady=(40, 15))
        # 切换网络标题+图标(B4)
        label_B4 = ctk.CTkLabel(label_B4_frame,
                                text="切换网络",
                                text_color="white",
                                padx=20,
                                image=self.change_icon,
                                compound="left",
                                font=("Microsoft YaHei UI", 20, "bold"),)
        label_B4.pack(padx=(5, 10), pady=5)

        # 新网络名称-边框(B5)
        label_B5_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_B5_frame.pack_propagate(False)
        label_B5_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 新网络名称-文本(B5)
        label_B5 = ctk.CTkLabel(label_B5_frame,
                                text="WLAN名称：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_B5.pack(side="left", padx=(5, 5), pady=0)
        # 新网络名称-输入框(B5)
        entry_B5 = ctk.CTkEntry(label_B5_frame,
                                placeholder_text="请输入新WLAN名称",
                                corner_radius=8,
                                border_width=0,
                                width=318,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16),)
        entry_B5.pack(side="left",padx=(3, 0), pady=(1, 0))
        # 新网络名称-设置当前wifi按钮(B5)
        button_B5 = ctk.CTkButton(label_B5_frame,
                                  text="同步",
                                  corner_radius=6,
                                  width=30,
                                  height=32,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: system_wlan_sync())
        button_B5.pack(side="right", padx=(1, 4), pady=0)

        # 新网络密码-边框(B6)
        label_B6_frame = ctk.CTkFrame(network_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_B6_frame.pack_propagate(False)
        label_B6_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 新网络密码-文本(B6)
        label_B6 = ctk.CTkLabel(label_B6_frame,
                                text="WLAN密码：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_B6.pack(side="left", padx=(5, 5), pady=0)
        # 新网络密码-输入框(B6)
        entry_B6 = ctk.CTkEntry(label_B6_frame,
                                placeholder_text="请输入新WLAN密码",
                                corner_radius=8,
                                border_width=0,
                                show="・",
                                width=318,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16))
        entry_B6.pack(side="left", padx=(3, 0), pady=(1, 0))

        # 新网络密码-显隐按钮(B6)
        self.hide_pwd_B6_state = True
        button_B6 = ctk.CTkButton(label_B6_frame,
                                  text="",
                                  width=30,
                                  height=32,
                                  corner_radius=8,
                                  image=self.hide_icon,
                                  fg_color="transparent",
                                  hover_color="lightgrey",
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: hide_show_pwd_B6())
        button_B6.pack(side="right", padx=(0, 5), pady=0)
        # 新网络密码-密码显隐功能方法(B6)
        def hide_show_pwd_B6():
            if self.hide_pwd_B6_state:  # 当前隐藏-切换为显示
                self.hide_pwd_B6_state = False  #更改状态
                entry_B6.configure(show="")  # 切换密码显示状态
                button_B6.configure(image=self.show_icon)  # 切换按钮图标
            else:  # 当前显示-切换为隐藏
                self.hide_pwd_B6_state = True  #更改状态
                entry_B6.configure(show="・")  # 切换密码显示状态
                button_B6.configure(image=self.hide_icon)  # 切换按钮图标

        # 新网络-同步系统WLAN名称和密码
        def system_wlan_sync():
            # 获取系统WLAN信息
            """(名称，密码，频率，信道，协议，编码, 信息)"""
            wlan_ssid, wlan_pwd, wlan_band, wlan_channel, wlan_version, encoding_type, execute_return \
                = Get_Computer_wifi()
            # 判断WLAN频率
            wlan_band = wlan_band.replace(" ","")
            if wlan_band not in ["","2.4GHz"]: #非2.4GHz的WiFi
                Warning_Window(f"设备仅支持 2.4GHz 的 WiFi ！(当前 {wlan_band})",
                               "Mine Compass WLAN",True)
            # 判断WLAN协议
            if wlan_version not in ["","802.11b","802.11g","802.11n"]: #不支持的WiFi版本
                WiFi_Version = Get_WiFi_Version(wlan_version) #获取当前版本
                Warning_Window(f"设备不支持高于 Wi-Fi 4 的网络！(当前 {WiFi_Version})",
                               "Mine Compass WLAN", True)
            # 更新输入框内容
            if wlan_band != "" and wlan_version != "":
                entry_B5.delete(0, "end")  # 清空原有内容-B5-新WLAN名称输入框
                entry_B5.insert(0, wlan_ssid)  # 输入内容-系统WLAN-SSID
                entry_B6.delete(0, "end")  # 清空原有内容-B6-新WLAN密码输入框
                entry_B6.insert(0, wlan_pwd)  # 插入内容-系统WLAN-密码
            else:
                pass

        # 确认按钮(B7)
        button_B7 = ctk.CTkButton(network_page,
                                  text="确定",
                                  width=100,
                                  height=40,
                                  font=("Microsoft YaHei UI", 20, "bold"),
                                  command=lambda: button_B7_Command())
        button_B7.pack(side="top", anchor="center", padx=(5, 5), pady=(30, 0))

        def button_B7_Command():
            updatewifi_thread = threading.Thread(target=UpdateWiFi)
            updatewifi_thread.daemon = True
            updatewifi_thread.start()

        def UpdateWiFi():
            # 获取WiFi SSID + 密码
            new_ssid = entry_B5.get()
            new_pwd = entry_B6.get()
            # SSID判断
            if new_ssid.replace(" ","")=="":
                Warning_Window("网络名称(SSID)不能为空！","Mine Compass WLAN",True)
            else:
                # 上传WiFi
                state_code = POST_WiFi(MainAddress,new_ssid,new_pwd)
                if state_code==200:
                    Info_Window("网络修改成功，请等待设备重启! ","Mine Compass WLAN",True)
                    # 清除当前信息
                    self.show_page(0) # 展示首页
                    self.FailedTimes = 0
                    label_A1.configure(text=f"连接状态：已断开")
                    label_A2.configure(text=f"设备地址：")
                    label_A3.configure(text=f"固件版本：")
                    label_A4.configure(text=f"构建时间：")
                    label_A5.configure(text=f"版本分支：")
                    label_A6.configure(text=f"版本哈希：")
                    ResetMainInfo()
                else:
                    Warning_Window(f"网络修改失败，状态码: {state_code} ","Mine Compass WLAN",False)
                pass

        # 添加页面到列表
        self.pages.append(network_page)



        """【位置设置页】"""
        #页面索引
        location_page = ctk.CTkFrame(self.content_area)
        #主标题-边框(C0)
        label_main_frame = ctk.CTkFrame(location_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0")
        label_main_frame.pack(anchor="center", padx=(0, 0), pady=(15,5),)
        #主标题+图标(C0)
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="位置信息",
                                  text_color="white",
                                  image=self.location_icon,
                                  padx=20,
                                  compound="left",
                                  font=("Microsoft YaHei UI", 20, "bold"))
        label_main.pack(padx=(5, 10), pady=5)

        # 当前出生点坐标-边框(C1)
        label_C1_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_C1_frame.pack_propagate(False)
        label_C1_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 当前出生点坐标-文本(C1)
        label_C1 = ctk.CTkLabel(label_C1_frame,
                                text="当前坐标：",
                                padx=10,
                                font=("Microsoft YaHei UI", 16))
        label_C1.pack(side="left", padx=(5, 5), pady=0)
        self.label_C1 = label_C1
        # 当前出生点坐标-复制按钮(C1)
        button_C1 = ctk.CTkButton(label_C1_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_C1_text())
        button_C1.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_C1_text():
            label_C1_text = label_C1.cget("text")
            label_C1_text = label_C1_text.replace('坐标：', '')
            Copy_to_Clipboard(label_C1_text)

        self.label_C1_SpawnPoint = ""   # 当前出生点坐标
        self.label_C2_SpawnAddress = "" # 当前出生点地址
        self.Location_Decode_state = True

        # 当前出生点地址-边框(C2)
        label_C2_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_C2_frame.pack_propagate(False)
        label_C2_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 当前出生点地址-文本(C2)
        label_C2 = ctk.CTkLabel(label_C2_frame,
                                text="地址：",
                                padx=10,
                                font=("Microsoft YaHei UI", 16))
        label_C2.pack(side="left", padx=(5, 5), pady=0)
        self.label_C2 = label_C2
        # 当前出生点地址-复制按钮(C2)
        button_C2 = ctk.CTkButton(label_C2_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_C2_text())
        button_C2.pack(side="right", padx=(5, 5), pady=(1,0))
        def copy_C2_text():
            label_C2_text = label_C2.cget("text")
            label_C2_text = label_C2_text.replace('地址：', '')
            Copy_to_Clipboard(label_C2_text)

        # 刷新按钮(C3)
        button_C3 = ctk.CTkButton(location_page,
                                  text="刷新",
                                  width=100,
                                  height=40,
                                  font=("Microsoft YaHei UI", 20, "bold"),
                                  command=lambda: button_C3_Command())
        button_C3.pack(side="top", anchor="center", padx=(5, 5), pady=(20, 0))

        # 设置出生点标题-边框(C4)
        label_C4_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=1,
                                      fg_color="#3B8ED0")
        label_C4_frame.pack(pady=(55, 5), padx=(0, 0), anchor="center")
        # 出生点标题+图标(C4)
        label_C4 = ctk.CTkLabel(label_C4_frame,
                                text="设置位置",
                                text_color="white",
                                padx=20,
                                compound="left",
                                image=self.set_location_icon,
                                font=("Microsoft YaHei UI", 20, "bold"))
        label_C4.pack(padx=(5, 10), pady=5)

        # 新出生点地址-边框(C5)
        label_C5_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_C5_frame.pack_propagate(False)
        label_C5_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 新出生点地址-文本(C5)
        label_C5 = ctk.CTkLabel(label_C5_frame,
                                text="设置地址：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_C5.pack(side="left", padx=(5, 5), pady=0)
        # 新出生点地址-输入框(C5)
        entry_C5 = ctk.CTkEntry(label_C5_frame,
                                placeholder_text="请输入新出生点地址",
                                corner_radius=8,
                                border_width=0,
                                width=333,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 14))
        entry_C5.pack(side="left",padx=(3, 0), pady=(1, 0))
        # 新出生点地址-定位按钮(C5)
        button_C5 = ctk.CTkButton(label_C5_frame,
                                  text="定位",
                                  corner_radius=6,
                                  width=30,
                                  height=32,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda:Auto_Positioning())
        button_C5.pack(side="right", padx=(1, 4), pady=0)

        # 新出生点坐标-边框(C6)
        label_C6_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_C6_frame.pack_propagate(False)
        label_C6_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 新出生点坐标-文本(C6)
        label_C6 = ctk.CTkLabel(label_C6_frame,
                                text="设置坐标：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_C6.pack(side="left", pady=0, padx=(5, 3))
        # 新出生点坐标-文本-东经(C6)
        label_C6_1 = ctk.CTkLabel(label_C6_frame,
                                  text="东经",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_C6_1.pack(side="left", pady=0, padx=0)
        # 新出生点坐标-输入框-东经(C6)
        entry_C6_1 = ctk.CTkEntry(label_C6_frame,
                                  placeholder_text="D.DD",
                                  corner_radius=8,
                                  border_width=0,
                                  width=139,
                                  height=label_all_h - 6,
                                  bg_color="transparent",
                                  font=("Microsoft YaHei UI", 16))
        entry_C6_1.pack(side="left",padx=(3, 0), pady=(1, 0))
        # 新出生点坐标-文本-北纬(C6)
        label_C6_2 = ctk.CTkLabel(label_C6_frame,
                                  text="北纬",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_C6_2.pack(side="left", pady=0, padx=0)
        # 新出生点坐标-输入框-北纬(C6)
        entry_C6_2 = ctk.CTkEntry(label_C6_frame,
                                  placeholder_text="D.DD",
                                  corner_radius=8,
                                  border_width=0,
                                  width=139,
                                  height=label_all_h - 6,
                                  bg_color="transparent",
                                  font=("Microsoft YaHei UI", 16))
        entry_C6_2.pack(side="left",padx=(3, 0), pady=(1, 0))

        # 模拟下界-框架(C7)
        label_C7_frame = ctk.CTkFrame(location_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_C7_frame.pack_propagate(False)
        label_C7_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 模拟下界-文本(C7)
        label_C7 = ctk.CTkLabel(label_C7_frame,
                                text="磁场异常：",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_C7.pack(side="left", padx=(5, 4), pady=0)
        # 模拟下界-文本说明(C7)
        label_C7_1 = ctk.CTkLabel(label_C7_frame,
                                text="模拟下界和末地的异常磁场",
                                padx=10,
                                font=("Microsoft YaHei UI", 16))
        label_C7_1.pack(side="left", padx=(1, 5), pady=0)
        # 模拟下界-开关(C7)
        switch_C7 = ctk.CTkSwitch(label_C7_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_C7_Event())
        switch_C7.pack(side="right", padx=(5, 5), pady=0)

        # 上传按钮(C8)
        button_C8 = ctk.CTkButton(location_page,
                                  text="绑定",
                                  width=100,
                                  height=40,
                                  font=("Microsoft YaHei UI", 20, "bold"),
                                  command=lambda: button_C8_Command())
        button_C8.pack(side="top", anchor="center", padx=(5, 5), pady=(20, 0))
        # 上传按钮-上传坐标(C8)
        def button_C8_Command():
            UpdateLocation_thread = threading.Thread(target=UpdateLocation)
            UpdateLocation_thread.daemon = True
            UpdateLocation_thread.start()
        def UpdateLocation():
            # 自动定位
            state = Auto_Positioning(mode=1)
            if state:
                # 获取坐标
                lng_text = entry_C6_1.get()
                lat_text = entry_C6_2.get()
                # 处理输入
                lng = lng_text.replace("°", "")
                lat = lat_text.replace("°", "")
                # 上传坐标
                state_code = POST_Spawn(MainAddress,lng,lat)
                if state_code==200:
                    Info_Window("出生点上传成功！","Mine Compass", False)
                    # 刷新坐标
                    # button_C3_Refresh()
                else:
                    Warning_Window(f"出生点上传失败！状态码: {state_code}","Mine Compass", False)
            else:
                pass

        #刷新按钮-获取当前坐标(C3)
        def button_C3_Command():
            RefreshLocation_thread = threading.Thread(target=RefreshLocation)
            RefreshLocation_thread.daemon = True
            RefreshLocation_thread.start()
        def RefreshLocation():
            # 获取坐标
            lng, lat = GET_Spawn(MainAddress)
            Now_SpawnPoint = (f"{lng}°E  {lat}°N")
            # 读取缓存(出生点坐标)
            state_read,Cache_SpawnPoint = Read_Cache("Cache-SpawnPoint.ini")
            # 判断位置变化
            if Now_SpawnPoint == self.label_C1_SpawnPoint and self.Location_Decode_state:
                print("位置与当前相同，无需重新定位")
                pass
            elif Now_SpawnPoint == Cache_SpawnPoint and self.Location_Decode_state:
                print("位置与缓存相同，无需重新定位")
                pass
            else: # [位置变化 或 定位失败 - 重新地理编码]
                # 地理编码
                self.label_C1_SpawnPoint = Now_SpawnPoint
                now_SpawnAddress, state = Location_Decode(lng, lat)
                self.Location_Decode_state = state
                self.label_C2_SpawnAddress = now_SpawnAddress
            # 更新输入框
            label_C1.configure(text=f"坐标：{self.label_C1_SpawnPoint}")
            label_C2.configure(text=f"地址：{self.label_C2_SpawnAddress}")
            # 更新缓存
            Write_Cache("Cache-SpawnPoint.ini",f"{self.label_C1_SpawnPoint}")
            Write_Cache("Cache-SpawnAddress.ini", f"{self.label_C2_SpawnAddress}")

        # 模拟下届开关事件-C7
        self.simulate_nether = False # 是否模拟下界
        self.state_switch_C7 = False
        self.switch_C7 = switch_C7
        def switch_C7_Event():
            # 获取状态
            state = switch_C7.get()
            # 更改状态
            if state == 0:
                self.state_switch_C7 = False
            elif state == 1:
                self.state_switch_C7 = True
            # 执行操作
            if self.state_switch_C7:
                self.simulate_nether = True
                # 启动模拟下届线程
                simulate_nether_thread = threading.Thread(target=Simulate_Nether)
                simulate_nether_thread.daemon = True
                simulate_nether_thread.start()
            else:
                self.simulate_nether = False

        # 模拟下届线程
        def Simulate_Nether():
            index_now = 0
            POST_Index(MainAddress,0) #0帧起手
            while self.simulate_nether:
                # 生成一组(10个)不重复的随机数
                random_list = np.random.choice(np.linspace(0, 28, 29, dtype=int),
                                                  size=10, replace=False)
                print(f"\n[模拟下界] 新随机数组生成：{random_list}\n")
                for random in random_list:
                    print(f"[模拟下界] 目标帧已刷新，新目标{random}")
                    # 停止判断
                    if not self.simulate_nether:
                        break
                    # 随机方向
                    way = np.random.choice(np.linspace(0, 1, 2, dtype=int))
                    # 判断正反转
                    if way==0: # 正转
                        while index_now!=random and self.simulate_nether:
                            # 正步进
                            index_now = index_now+1
                            if index_now>28:
                                index_now=0
                            else:
                                pass
                            # 发送请求
                            print(f"[模拟下界] 正步进，目标{random}；当前{index_now}")
                            POST_Index(MainAddress, index_now)
                            time.sleep(0.05)
                        print(f"[模拟下界] 正步进完成")

                    elif way==1: # 反转
                        while index_now != random and self.simulate_nether:
                            # 正步进
                            index_now = index_now - 1
                            if index_now < 0:
                                index_now = 28
                            else:
                                pass
                            # 发送请求
                            print(f"[模拟下界] 负步进，目标{random}；当前{index_now}")
                            POST_Index(MainAddress, index_now)
                            time.sleep(0.05)
                        print(f"[模拟下界] 负步进完成")

                    else:
                        pass

        # 输入框上次内容
        self.last_address_text = ""
        self.last_lng_text = ""
        self.lase_lat_text = ""
        self.change_address_text = False
        self.change_lng_text = False
        self.change_lat_text = False

        # 自动定位功能
        def Auto_Positioning(mode=0):
            # 读取输入框
            address_text = entry_C5.get()
            lng_text = entry_C6_1.get()
            lat_text = entry_C6_2.get()

            # 判断变化
            if address_text != self.last_address_text:
                self.change_address_text = True
            else:
                self.change_address_text = False
            if lng_text != self.last_lng_text:
                self.change_lng_text = True
            else:
                self.change_lng_text = False
            if lat_text != self.lase_lat_text:
                self.change_lat_text = True
            else:
                self.change_lat_text = False

            #输入框全空，未输入完成 - 使用IP定位
            if address_text=="" and (lng_text=="" or lat_text==""):
                # IP定位
                Info_Window("未输入地址，将采用IP定位！(市级精度)","Mine Compass 定位",True)
                address, lng, lat, state = Location_IP()
                # 更新输入框
                entry_C5.delete(0, "end")  # 地址-清空
                entry_C5.insert(0, address)  # 地址-输入
                entry_C6_1.delete(0, "end")  # 经度-清空
                entry_C6_1.insert(0, lng)  # 经度-输入
                entry_C6_2.delete(0, "end")  # 维度-清空
                entry_C6_2.insert(0, lat)  # 维度-输入
                print("输入框全空，未输入完成 - 使用IP定位")

            #已输入地址 且 地址或坐标有变化 - 使用地理编码定位
            elif (address_text!="" and (
                    self.change_address_text
                    or self.change_lng_text
                    or self.change_lat_text)):
                #地理编码
                lng, lat, state = Location_Encoding(address_text)
                # 更新输入框
                entry_C6_1.delete(0, "end")  # 经度-清空
                entry_C6_1.insert(0, lng)  # 经度-输入
                entry_C6_2.delete(0, "end")  # 维度-清空
                entry_C6_2.insert(0, lat)  # 维度-输入
                print("已输入地址 且 地址或坐标有变化 - 使用地理编码定位")

            # 已输入地址 但 地址和坐标无变化 - 提示
            elif (address_text != "" and(
                    not self.change_address_text
                    and not self.change_lng_text
                    and not self.change_lat_text)):
                if mode==1:
                    pass # 上传函数调用-取消提示
                else:
                    Info_Window("无变化，无需重新定位。", "Mine Compass 定位", True)

            # 未输入地址 且 输入了坐标 - 使用地理解码:
            elif address_text== "" and lng_text!= "" and lat_text!= "":
                # 处理输入
                lng_check = lng_text.replace("°", "")
                lat_check = lat_text.replace("°", "")
                # 匹配格式
                pattern = r"^([-+]?\d+(?:\.\d*)?)$"  # 匹配格式：DD.DDDD′
                match_lng = re.match(pattern, lng_check)
                match_lat = re.match(pattern, lat_check)
                if match_lng and match_lat:
                    lng = lng_check
                    lat = lat_check
                    pass  # 格式匹配
                else:
                    # 格式转化
                    if not match_lng:
                        lng = Location_Convert(lng_text)
                    elif match_lng:
                        lng = lng_check
                    else:
                        lng = 0
                    if not match_lat:
                        lat = Location_Convert(lat_text)
                    elif match_lat:
                        lat = lat_check
                    else:
                        lat = 0
                # 坐标验证
                try:
                    lng = float(lng)
                    lat = float(lat)
                except Exception as error:
                    Warning_Window(f"非法输入！请检查输入！\n{error}", "Mine Compass 定位", True)
                    return False
                if -180<lng<180 and -90<lat<90: # 合法坐标
                    # 地理解码
                    address, state = Location_Decode(str(lng), str(lat))
                    # 更新输入框
                    entry_C5.delete(0, "end")  # 地址-清空
                    entry_C5.insert(0, address)  # 地址-输入
                else:
                    Warning_Window("非法坐标！请检查输入","Mine Compass 定位",True)
                    return False
                print("未输入地址 且 输入了坐标 - 使用地理解码:")
            # WTF?
            else:
                Questions_Window("无法定位，你在开玩笑吗？", "Mine Compass 定位", True)
                return False

            # 更新输入框历史记录
            address_new = entry_C5.get()
            lng_new = entry_C6_1.get()
            lat_new = entry_C6_2.get()
            self.last_address_text = address_new
            self.last_lng_text = lng_new
            self.lase_lat_text = lat_new
            return True

        self.pages.append(location_page)  #添加页面到页面列表



        """【颜色设置页】"""
        #页面索引
        colorpalette_page = ctk.CTkFrame(self.content_area)
        #主标题-边框
        label_main_frame = ctk.CTkFrame(colorpalette_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0",)
        label_main_frame.pack(pady=(15,10), padx=(0, 0), anchor="center")
        #主标题+图标
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="颜色设置",
                                  text_color="white",
                                  padx=20,
                                  compound="left",
                                  image=self.colorpalette_icon,
                                  font=("Microsoft YaHei UI", 20, "bold"))
        label_main.pack(padx=(5, 10), pady=5)

        # 颜色滑块-边框(D1)
        label_D1_frame = ctk.CTkFrame(colorpalette_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=190)
        label_D1_frame.pack_propagate(False)
        label_D1_frame.pack(anchor="center", padx=(0, 10), pady=(5, 0))

        # 红色-框架(D1R)
        label_D1R_frame = ctk.CTkFrame(label_D1_frame,
                                       corner_radius=5,
                                       border_width=0,
                                       border_color="grey",
                                       width=label_all_w,
                                       height=label_all_h,
                                       fg_color="transparent",
                                       bg_color="transparent")
        label_D1R_frame.pack_propagate(False)
        label_D1R_frame.pack(anchor="center", padx=(5, 5), pady=(5, 0))
        # 红色-文本(D1R)
        label_D1R = ctk.CTkLabel(label_D1R_frame,
                                 text="红色",
                                 padx=10,
                                 font=("Microsoft YaHei UI", 18))
        label_D1R.pack(side="left", padx=(5, 0), pady=0)
        # 红色-滑块(D1R)
        slider_D1R = ctk.CTkSlider(label_D1R_frame,
                                   from_=0, to=255,
                                   number_of_steps=255,
                                   width=320,
                                   progress_color="#3B8ED0")
        slider_D1R.pack(side="left", padx=(5,5))
        # 红色-输入框(D1R)
        entry_D1R = ctk.CTkEntry(label_D1R_frame,
                                 placeholder_text="R",
                                 corner_radius=6,
                                 border_width=2,
                                 width=85,
                                 height=label_all_h - 10,
                                 justify="center",
                                 bg_color="transparent",
                                 font=("Microsoft YaHei UI", 16))
        entry_D1R.pack(side="left", padx=(5, 5), pady=(1, 0))

        # 绿色-框架(D1G)
        label_D1G_frame = ctk.CTkFrame(label_D1_frame,
                                       corner_radius=5,
                                       border_width=0,
                                       border_color="grey",
                                       width=label_all_w,
                                       height=label_all_h,
                                       fg_color="transparent",
                                       bg_color="transparent")
        label_D1G_frame.pack_propagate(False)
        label_D1G_frame.pack(anchor="center",  padx=(5, 5), pady=(5, 0))
        # 绿色-文本(D1G)
        label_D1G = ctk.CTkLabel(label_D1G_frame,
                                 text="绿色",
                                 padx=10,
                                 font=("Microsoft YaHei UI", 18))
        label_D1G.pack(side="left", padx=(5, 0), pady=0)
        # 绿色-滑块(D1G)
        slider_D1G = ctk.CTkSlider(label_D1G_frame,
                                   from_=0, to=255,
                                   number_of_steps=255,
                                   width=320,
                                   progress_color="#3B8ED0")
        slider_D1G.pack(side="left", padx=(5, 5))
        # 绿色-输入框(D1G)
        entry_D1G = ctk.CTkEntry(label_D1G_frame,
                                 placeholder_text="G",
                                 corner_radius=6,
                                 border_width=2,
                                 width=85,
                                 height=label_all_h - 10,
                                 justify="center",
                                 bg_color="transparent",
                                 font=("Microsoft YaHei UI", 16))
        entry_D1G.pack(side="left",padx=(5, 5), pady=(1, 0))

        # 蓝色-框架(D1B)
        label_D1B_frame = ctk.CTkFrame(label_D1_frame,
                                       corner_radius=5,
                                       border_width=0,
                                       border_color="grey",
                                       width=label_all_w,
                                       height=label_all_h,
                                       fg_color="transparent",
                                       bg_color="transparent")
        label_D1B_frame.pack_propagate(False)
        label_D1B_frame.pack(anchor="center", padx=(5, 5), pady=(5, 0))
        # 蓝色-文本(D1B)
        label_D1B = ctk.CTkLabel(label_D1B_frame,
                                 text="蓝色",
                                 padx=10,
                                 font=("Microsoft YaHei UI", 18))
        label_D1B.pack(side="left", padx=(5, 0), pady=0)
        # 蓝色-滑块(D1B)
        slider_D1B = ctk.CTkSlider(label_D1B_frame,
                                   from_=0, to=255,
                                   number_of_steps=255,
                                   width=320,
                                   progress_color="#3B8ED0")
        slider_D1B.pack(side="left", padx=(5, 5))
        # 蓝色-输入框(D1B)
        entry_D1B = ctk.CTkEntry(label_D1B_frame,
                                 placeholder_text="B",
                                 corner_radius=6,
                                 border_width=2,
                                 width=85,
                                 height=label_all_h - 10,
                                 justify="center",
                                 bg_color="transparent",
                                 font=("Microsoft YaHei UI", 16))
        entry_D1B.pack(side="left", padx=(5, 5), pady=(1, 0))

        # 亮度-框架(D1V)
        label_D1V_frame = ctk.CTkFrame(label_D1_frame,
                                       corner_radius=5,
                                       border_width=0,
                                       border_color="grey",
                                       width=label_all_w,
                                       height=label_all_h,
                                       fg_color="transparent",
                                       bg_color="transparent")
        label_D1V_frame.pack_propagate(False)
        label_D1V_frame.pack(anchor="center", padx=(5, 5), pady=(5, 0))
        # 亮度-文本(D1V)
        label_D1V = ctk.CTkLabel(label_D1V_frame,
                                 text="亮度",
                                 padx=10,
                                 font=("Microsoft YaHei UI", 18))
        label_D1V.pack(side="left", padx=(5, 0), pady=0,)
        # 亮度-滑块(D1V)
        slider_D1V = ctk.CTkSlider(label_D1V_frame,
                                   from_=0, to=100,
                                   number_of_steps=1000,
                                   width=320,
                                   progress_color="#3B8ED0")
        slider_D1V.pack(side="left", padx=(5, 5))
        # 亮度-输入框(D1V)
        entry_D1V = ctk.CTkEntry(label_D1V_frame,
                                 placeholder_text="V",
                                 corner_radius=6,
                                 border_width=2,
                                 width=85,
                                 height=label_all_h - 10,
                                 justify="center",
                                 bg_color="transparent",
                                 font=("Microsoft YaHei UI", 16),)
        entry_D1V.pack(side="left", padx=(5, 5), pady=(1, 0))

        # 总颜色-边框(D2)
        label_D2_frame = ctk.CTkFrame(colorpalette_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_D2_frame.pack_propagate(False)
        label_D2_frame.pack(anchor="center", padx=(0, 10), pady=(10, 0))
        # 总颜色-文本(D2)
        label_D2 = ctk.CTkLabel(label_D2_frame,
                                text="当前",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_D2.pack(side="left", padx=(10, 0), pady=0)
        # 总颜色-16进制输入框(D2)(HEX)
        entry_D2 = ctk.CTkEntry(label_D2_frame,
                                placeholder_text="#FFFFFF",
                                corner_radius=8,
                                border_width=0,
                                width=100,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16))
        entry_D2.pack(side="left", padx=(10, 5), pady=(1, 0))
        # 总颜色-文本(D2_1)(HEX)
        label_D2_1 = ctk.CTkLabel(label_D2_frame,
                                  text="预览",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_D2_1.pack(side="left", padx=(40, 0), pady=0)
        # 总颜色-预览(D2_1)(HEX)
        label_D2_1_frame = ctk.CTkFrame(label_D2_frame,
                                        corner_radius=6,
                                        border_width=0,
                                        border_color="grey",
                                        width=50,
                                        height=label_all_h-10,
                                        fg_color="#3B8ED0")
        label_D2_1_frame.pack_propagate(False)
        label_D2_1_frame.pack(side="left",padx=(5, 5), pady=(1, 0))

        # 屏幕取色-按钮(D2)
        button_D2 = ctk.CTkButton(label_D2_frame,
                                  text="屏幕取色",
                                  width=83,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: GET_COLOR())
        button_D2.pack(side="right", padx=(5, 20), pady=0)

        # 调色盘总框架
        label_D3_frame = ctk.CTkFrame(colorpalette_page,
                                      corner_radius=5,
                                      border_width=0,
                                      border_color="grey",
                                      width=label_all_w+3,
                                      height=256,
                                      fg_color="transparent",
                                      bg_color="transparent")
        label_D3_frame.pack_propagate(False)
        label_D3_frame.pack(anchor="center", padx=(3, 10), pady=(13, 0))
        # 调色盘
        image_label_D3 = ctk.CTkLabel(label_D3_frame,
                                      text="",
                                      image=self.HSV_palette,
                                      fg_color="transparent",
                                      bg_color="transparent")
        image_label_D3.pack(side="left")

        # 色彩循环开关-框架
        label_D4_frame = ctk.CTkFrame(label_D3_frame,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=220,
                                      height=label_all_h)
        label_D4_frame.pack_propagate(False)
        label_D4_frame.pack(anchor="center", padx=(20, 0), pady=(10, 0))
        # 色彩循环开关-文本
        label_D4 = ctk.CTkLabel(label_D4_frame,
                                text="色彩循环",
                                padx=10,
                                font=("Microsoft YaHei UI", 17))
        label_D4.pack(side="left", padx=(5, 5), pady=0)
        # 色彩循环开关-开关
        switch_D4 = ctk.CTkSwitch(label_D4_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda:switch_D4_Event())
        switch_D4.pack(side="right", padx=(5, 5), pady=0,)
        self.switch_D4 = switch_D4

        # 同步更新开关-框架
        label_D5_frame = ctk.CTkFrame(label_D3_frame,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=220,
                                      height=label_all_h)
        label_D5_frame.pack_propagate(False)
        label_D5_frame.pack(anchor="center", padx=(20, 0), pady=(15, 0))
        # 同步更新开关-文本
        label_D5 = ctk.CTkLabel(label_D5_frame,
                                text="同步更新",
                                padx=10,
                                font=("Microsoft YaHei UI", 17))
        label_D5.pack(side="left", padx=(5, 5), pady=0)
        # 同步更新开关-开关
        switch_D5 = ctk.CTkSwitch(label_D5_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_D5_Event())
        switch_D5.pack(side="right", padx=(5, 5), pady=0)  # 将开关放在右侧
        self.switch_D5 = switch_D5

        # 上传按钮
        button_D6 = ctk.CTkButton(label_D3_frame,
                                  text="上传",
                                  height=40,
                                  width=100,
                                  font=("Microsoft YaHei UI", 20, "bold"),
                                  command=lambda: button_D6_Command())
        button_D6.pack(side="top", anchor="center", padx=(20, 0), pady=(40, 0))

        def button_D6_Command():
            updatecolor_button_thread = threading.Thread(target=Update_Color)
            updatecolor_button_thread.daemon = True
            updatecolor_button_thread.start()


        #【界面更新函数】
        def Update_UI(r, g, b, v, hex_mode=0, slider_mod=0):
            # 统一类型
            r = int(r)
            g = int(g)
            b = int(b)
            v = v * 100
            v = round(v, 1)
            # 更新输入框
            entry_D1R.delete(0, "end")
            entry_D1R.insert(0, str(r))
            entry_D1G.delete(0, "end")
            entry_D1G.insert(0, str(g))
            entry_D1B.delete(0, "end")
            entry_D1B.insert(0, str(b))
            entry_D1V.delete(0, "end")
            entry_D1V.insert(0, str(f"{v:.1f}"))
            # 更新滑块
            if slider_mod==1:
                smooth_set_slider(slider_D1R, r, duration=100)
                smooth_set_slider(slider_D1G, g, duration=100)
                smooth_set_slider(slider_D1B, b, duration=100)
                smooth_set_slider(slider_D1V, v, duration=100)
            else:
                slider_D1R.set(r)
                slider_D1G.set(g)
                slider_D1B.set(b)
                slider_D1V.set(v)
            # 更新HEX
            if hex_mode == 1:  # (不更新)
                pass
            else:
                Update_UI_HEX(r, g, b)

        #【界面更新函数 - HEX更新】
        def Update_UI_HEX(r, g, b):
            # 转化HEX
            hex_color = RGB_to_HEX(r, g, b)
            # 更新HEX颜色
            entry_D2.delete(0, "end")
            entry_D2.insert(0, str(hex_color))
            # 更新预览
            label_D2_1_frame.configure(fg_color=str(hex_color))

        # 获取颜色
        def Get_Color():
            # 读取数据
            r_str = entry_D1R.get()
            g_str = entry_D1G.get()
            b_str = entry_D1B.get()
            v_str = entry_D1V.get()
            # 统一数据
            r = int(r_str)
            g = int(g_str)
            b = int(b_str)
            v = float(v_str)/100
            # 返回数据
            return r,g,b,v


        # 调色盘-鼠标位置计算HSV颜色
        def mouse_position_to_rgb(mouse_x,mouse_y,frame_width,frame_height):
            # 计算HSV颜色
            # X轴 - 色相H [0, 360]
            h = (mouse_x / frame_width) * 360
            # Y轴 - 饱和度S [0, 360]
            s = (mouse_y / frame_height)
            # 亮度V
            v = entry_D1V.get()
            v = float(v)/100
            # HSV转RGB
            r, g, b = HSV_to_RGB(h,s,v)
            return r, g, b, v

        # RGB 同步 HEX
        def sync_RGB_to_HEX():
            r, g, b, v = Get_Color() # 获取颜色
            Update_UI_HEX(r,g,b)

        # RGB 同步 HSV
        def sync_RGB_to_HSV(mode=0):
            r, g, b, v_tmp = Get_Color()  # 获取颜色
            h, s, v = RGB_to_HSV(r, g, b) # 转化为HSV
            v = round(v*100,1)
            # 更新HSV亮度
            entry_D1V.delete(0, "end")
            entry_D1V.insert(0, str(f"{v:.1f}"))
            if mode==1:
                smooth_set_slider(slider_D1V, v, duration=100)
            else:
                slider_D1V.set(v)

        # HSV 同步 RGB
        def sync_HSV_to_RGB(mode=0):
            r, g, b, v = Get_Color() # 获取颜色
            h_now, s_now, v_now = RGB_to_HSV(r, g, b) # 计算当前RGB的HSV值
            r_new, g_new, b_new = HSV_to_RGB(h_now, s_now, v) # 替换v, 重新计算RGB
            # 更新界面
            if mode == 1:
                entry_D1R.delete(0, "end")
                entry_D1R.insert(0, str(r_new))
                entry_D1G.delete(0, "end")
                entry_D1G.insert(0, str(g_new))
                entry_D1B.delete(0, "end")
                entry_D1B.insert(0, str(b_new))
                slider_D1R.set(r_new)
                slider_D1G.set(g_new)
                slider_D1B.set(b_new)
                Update_UI_HEX(r_new, g_new, b_new)
            else:
                Update_UI(r_new, g_new, b_new, v,hex_mode=0,slider_mod=1)


        # 滑块变化事件
        # 红色-滑块(D1R)
        def slider_D1R_Event(value):
            entry_D1R.delete(0, "end")
            entry_D1R.insert(0, str(int(value)))
            sync_RGB_to_HEX()
            sync_RGB_to_HSV()
        # 绿色-滑块(D1G)
        def slider_D1G_Event(value):
            entry_D1G.delete(0, "end")
            entry_D1G.insert(0, str(int(value)))
            sync_RGB_to_HEX()
            sync_RGB_to_HSV()
        # 蓝色-滑块(D1B)
        def slider_D1B_Event(value):
            entry_D1B.delete(0, "end")
            entry_D1B.insert(0, str(int(value)))
            sync_RGB_to_HEX()
            sync_RGB_to_HSV()
        # 亮度-滑块(D1V)
        def slider_D1V_Event(value):
            value = round(value,1)
            entry_D1V.delete(0, "end")
            entry_D1V.insert(0, str(f"{value:.1f}"))
            sync_HSV_to_RGB(mode=1)

        # 滑块滚轮事件
        def slider_D1R_Wheel_Event(event):
            value = slider_D1R.get()
            value_max = int(slider_D1R.cget("to"))
            value_min = int(slider_D1R.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 2
                if value_min<=value_new<=value_max:
                    slider_D1R.set(value_new)
                    slider_D1R_Event(value_new)
                else:
                    slider_D1R.set(value_min)
                    slider_D1R_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 2
                if value_min <= value_new <= value_max:
                    slider_D1R.set(value_new)
                    slider_D1R_Event(value_new)
                else:
                    slider_D1R.set(value_max)
                    slider_D1R_Event(value_max)

        def slider_D1G_Wheel_Event(event):
            value = slider_D1G.get()
            value_max = int(slider_D1G.cget("to"))
            value_min = int(slider_D1G.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 2
                if value_min <= value_new <= value_max:
                    slider_D1G.set(value_new)
                    slider_D1G_Event(value_new)
                else:
                    slider_D1G.set(value_min)
                    slider_D1G_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 2
                if value_min <= value_new <= value_max:
                    slider_D1G.set(value_new)
                    slider_D1G_Event(value_new)
                else:
                    slider_D1G.set(value_max)
                    slider_D1G_Event(value_max)

        def slider_D1B_Wheel_Event(event):
            value = slider_D1B.get()
            value_max = int(slider_D1B.cget("to"))
            value_min = int(slider_D1B.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 2
                if value_min <= value_new <= value_max:
                    slider_D1B.set(value_new)
                    slider_D1B_Event(value_new)
                else:
                    slider_D1B.set(value_min)
                    slider_D1B_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 2
                if value_min <= value_new <= value_max:
                    slider_D1B.set(value_new)
                    slider_D1B_Event(value_new)
                else:
                    slider_D1B.set(value_max)
                    slider_D1B_Event(value_max)

        def slider_D1V_Wheel_Event(event):
            value = slider_D1V.get()
            value_max = int(slider_D1V.cget("to"))
            value_min = int(slider_D1V.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 1
                if value_min <= value_new <= value_max:
                    slider_D1V.set(value_new)
                    slider_D1V_Event(value_new)
                else:
                    slider_D1V.set(value_min)
                    slider_D1V_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 1
                if value_min <= value_new <= value_max:
                    slider_D1V.set(value_new)
                    slider_D1V_Event(value_new)
                else:
                    slider_D1V.set(value_max)
                    slider_D1V_Event(value_max)

        # 输入框事件
        # 红色-输入框(D1R)
        def entry_D1R_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_D1R:
                return
            if self.MouseState_slider_D1V:
                return
            # 获取输入框内容
            try:
                value = int(entry_D1R.get())
            except:
                value = -1
            # 判断范围
            if 0<=value<=255:
                # 在范围内-更新滑块
                smooth_set_slider(slider_D1R, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_D1R.get()
                entry_D1R.delete(0, "end")
                entry_D1R.insert(0, str(int(slider_value)))
            # 更新HEX
            sync_RGB_to_HEX()
            # 更新HSV
            sync_RGB_to_HSV(mode=1)

        # 绿色-输入框(D1G)
        def entry_D1G_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_D1G:
                return
            if self.MouseState_slider_D1V:
                return
            # 获取输入框内容
            try:
                value = int(entry_D1G.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 255:
                # 在范围内-更新滑块
                smooth_set_slider(slider_D1G, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_D1G.get()
                entry_D1G.delete(0, "end")
                entry_D1G.insert(0, str(int(slider_value)))
            # 更新HEX
            sync_RGB_to_HEX()
            # 更新HSV
            sync_RGB_to_HSV(mode=1)

        # 蓝色-输入框(D1B)
        def entry_D1B_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_D1B:
                return
            if self.MouseState_slider_D1V:
                return
            # 获取输入框内容
            try:
                value = int(entry_D1B.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 255:
                # 在范围内-更新滑块
                smooth_set_slider(slider_D1B, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_D1B.get()
                entry_D1B.delete(0, "end")
                entry_D1B.insert(0, str(int(slider_value)))
            # 更新HEX
            sync_RGB_to_HEX()
            # 更新HSV
            sync_RGB_to_HSV(mode=1)

        # 亮度-输入框(D1V)
        def entry_D1V_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_D1V:
                return
            # 获取输入框内容
            try:
                value = float(entry_D1V.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 100:
                # 在范围内-更新滑块
                smooth_set_slider(slider_D1V, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_D1V.get()
                entry_D1V.delete(0, "end")
                entry_D1V.insert(0, str(f"{float(slider_value):.1f}"))
            # 更新RGB+HEX
            sync_HSV_to_RGB(mode=0)
            # 更新HSV
            sync_RGB_to_HSV(mode=1)

        # HEX颜色-输入框(D2)
        def entry_HEX_Event(event):
            # 获取颜色
            hex_color = entry_D2.get()
            # 转化颜色
            r,g,b = HEX_to_RGB(hex_color)
            h,s,v = RGB_to_HSV(r,g,b)
            # 更新界面
            Update_UI(r,g,b,v,hex_mode=0,slider_mod=1)

        # 【调色盘单击取色】
        def Palette_Get_Color(event):
            # 触发事件判断
            event_type = 0
            if "ButtonPress" in str(event):
                event_type = 1
            elif "Motion" in str(event):
                event_type = 0
            # 获取鼠标点击位置的全局坐标
            mouse_global_x = event.x_root
            mouse_global_y = event.y_root
            # 获取调色盘框架的全局位置和尺寸
            frame_global_x = image_label_D3.winfo_rootx()
            frame_global_y = image_label_D3.winfo_rooty()
            frame_width = image_label_D3.winfo_width()
            frame_height = image_label_D3.winfo_height()

            # 判断鼠标点击是否在调色盘框架内
            if (frame_global_x <= mouse_global_x <= frame_global_x + frame_width) and (
                    frame_global_y <= mouse_global_y <= frame_global_y + frame_height):
                # 获取鼠标相对位置
                mouse_x = event.x
                mouse_y = event.y
                # 通过位置计算RGB
                r, g, b, v = mouse_position_to_rgb(mouse_x, mouse_y, frame_width, frame_height)
                # 更新界面
                if not GET_COLOR_STATE:
                    if (
                            (slider_D1R in self.smooth_slider_executing_list)
                            or (slider_D1G in self.smooth_slider_executing_list)
                            or (slider_D1B in self.smooth_slider_executing_list)
                            or (slider_D1V in self.smooth_slider_executing_list)
                    ):
                        return # 进度条有动画在执行-直接返回
                    else:
                        Update_UI(r, g, b, v, hex_mode=0, slider_mod=event_type)
            else:
                pass

        # 绑定事件
        image_label_D3.bind("<Button-1>",Palette_Get_Color)
        image_label_D3.bind("<B1-Motion>",Palette_Get_Color)


        #【滑块鼠标点击检测】
        self.MouseState_slider_D1R = False
        self.MouseState_slider_D1G = False
        self.MouseState_slider_D1B = False
        self.MouseState_slider_D1V = False
        # 获得焦点
        def MousePress_slider_D1R(event): # 滑块-R-获得焦点
            self.MouseState_slider_D1R = True
        def MousePress_slider_D1G(event): # 滑块-G-获得焦点
            self.MouseState_slider_D1G = True
        def MousePress_slider_D1B(event): # 滑块-B-获得焦点
            self.MouseState_slider_D1B = True
        def MousePress_slider_D1V(event): # 滑块-V-获得焦点
            self.MouseState_slider_D1V = True
        # 失去焦点
        def MouseRelease_slider_D1R(event): # 滑块-R-失去焦点
            self.MouseState_slider_D1R = False
        def MouseRelease_slider_D1G(event): # 滑块-G-失去焦点
            self.MouseState_slider_D1G = False
        def MouseRelease_slider_D1B(event): # 滑块-B-失去焦点
            self.MouseState_slider_D1B = False
        def MouseRelease_slider_D1V(event): # 滑块-V-失去焦点
            self.MouseState_slider_D1V = False
        # 绑定事件
        slider_D1R.bind("<Button-1>",MousePress_slider_D1R)
        slider_D1G.bind("<Button-1>",MousePress_slider_D1G)
        slider_D1B.bind("<Button-1>",MousePress_slider_D1B)
        slider_D1V.bind("<Button-1>",MousePress_slider_D1V)
        slider_D1R.bind("<MouseWheel>",slider_D1R_Wheel_Event)
        slider_D1G.bind("<MouseWheel>",slider_D1G_Wheel_Event)
        slider_D1B.bind("<MouseWheel>",slider_D1B_Wheel_Event)
        slider_D1V.bind("<MouseWheel>",slider_D1V_Wheel_Event)
        slider_D1R.bind("<ButtonRelease>", MouseRelease_slider_D1R)
        slider_D1G.bind("<ButtonRelease>", MouseRelease_slider_D1G)
        slider_D1B.bind("<ButtonRelease>", MouseRelease_slider_D1B)
        slider_D1V.bind("<ButtonRelease>", MouseRelease_slider_D1V)

        # 开关状态
        self.state_switch_D4 = False
        self.state_switch_D5 = False

        # 开关事件-D4
        def switch_D4_Event():
            # 获取状态
            state = switch_D4.get()
            print(state)
            # 更改状态
            if state == 0:
                self.state_switch_D4 = False
                print("开关关闭")
            elif state == 1:
                print("开关开启")
                self.state_switch_D4 = True
                self.state_switch_D5 = False
            # 执行操作
            if self.state_switch_D4:
                print("启动色彩循环线程")
                # 刷新其他控件
                switch_D5.deselect()
                switch_D5_Event()
                # 修改状态
                self.ColorCycle_state = True
                # 启动色彩循环线程
                colorCycle_thread = threading.Thread(target=ColorCycle_thread)
                colorCycle_thread.daemon = True
                colorCycle_thread.start()
            else:
                # 修改状态
                print("关闭色彩循环线程")
                self.ColorCycle_state = False

        # 开关事件-D5
        def switch_D5_Event():
            # 获取状态
            state = switch_D5.get()
            # 更改状态
            if state == 0:
                self.state_switch_D5 = False
            elif state == 1:
                self.state_switch_D4 = False
                self.state_switch_D5 = True
            # 执行操作
            if self.state_switch_D5:
                print("启动色彩同步线程")
                # 刷新其他控件
                switch_D4.deselect()
                switch_D4_Event()
                # 修改状态
                self.UpdateColor_Continuous =True
                # 启动线程
                updateColor_thread = threading.Thread(target=UpdateColor_thread)
                updateColor_thread.daemon = True
                updateColor_thread.start()
            else:
                # 修改状态
                print("关闭色彩同步线程")
                self.UpdateColor_Continuous = False
        # 上传颜色
        def Update_Color():
            # 从预览获取颜色
            hex_color = label_D2_1_frame.cget("fg_color")
            # 上传颜色
            state_code = POST_Color(MainAddress, hex_color)
            return state_code

        # 持续上传颜色
        self.UpdateColor_Continuous = False # 是否持续上传
        def UpdateColor_thread():
            print("正在持续上传...")
            while self.UpdateColor_Continuous:
                state = Update_Color()
                if state!=200:
                    print(f"上传失败！状态码: {state}")
                time.sleep(0.02)
            print("持续上传结束！")

        # 色彩循环
        self.ColorCycle_state = False
        def ColorCycle_thread():
            """
            变化过程：
            0 → R
            R → RG → G → GB → B → BR → R ◀
            """
            # [0]
            POST_Color(MainAddress,"#000000")
            # [0 → R]
            for i in range(0,52):
                r = 0+i*5
                g = 0
                b = 0
                hex_color = RGB_to_HEX(r,g,b)
                POST_Color(MainAddress,hex_color)
                if not self.ColorCycle_state:
                    break
            # 主循环
            while self.ColorCycle_state:
                # [R → RG]
                for i in range(0,52):
                    r = 255
                    g = 0+i*5
                    b = 0
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
                # [RG → G]
                for i in range(0,52):
                    r = 255-i*5
                    g = 255
                    b = 0
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
                # [G → GB]
                for i in range(0,52):
                    r = 0
                    g = 255
                    b = 0+i*5
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
                # [GB → B]
                for i in range(0,52):
                    r = 0
                    g = 255-i*5
                    b = 255
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
                # [B → BR]
                for i in range(0,52):
                    r = 0+i*5
                    g = 0
                    b = 255
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
                # [BR → R]
                for i in range(0,52):
                    r = 255
                    g = 0
                    b = 255-i*5
                    hex_color = RGB_to_HEX(r, g, b)
                    POST_Color(MainAddress, hex_color)
                    if not self.ColorCycle_state:
                        break
            # 循环结束-上传当前颜色
            Update_Color()
            pass



        #【默认颜色】
        Update_UI(255,255,255,1,0,0)

        # 绑定事件-红色(D1R)
        slider_D1R.configure(command=slider_D1R_Event)  # 滑块变化时触发
        entry_D1R.bind("<FocusOut>", entry_D1R_Event)  # 输入框失去焦点触发
        entry_D1R.bind("<Return>", entry_D1R_Event)  # 输入框回车触发
        # 绑定事件-绿色(D1G)
        slider_D1G.configure(command=slider_D1G_Event)  # 滑块变化时触发
        entry_D1G.bind("<FocusOut>",entry_D1G_Event )  # 输入框失去焦点触发
        entry_D1G.bind("<Return>", entry_D1G_Event)  # 输入框回车触发
        # 绑定事件-蓝色(D1B)
        slider_D1B.configure(command=slider_D1B_Event)  # 滑块变化时触发
        entry_D1B.bind("<FocusOut>", entry_D1B_Event)  # 输入框失去焦点触发
        entry_D1B.bind("<Return>", entry_D1B_Event)  # 输入框回车触发
        # 绑定事件-亮度(D1V)
        slider_D1V.configure(command=slider_D1V_Event)  # 滑块变化时触发
        entry_D1V.bind("<FocusOut>", entry_D1V_Event)  # 输入框失去焦点触发
        entry_D1V.bind("<Return>", entry_D1V_Event)  # 输入框回车触发
        # 绑定事件-总HEX(D2)
        entry_D2.bind("<FocusOut>", entry_HEX_Event)  # 输入框失去焦点触发
        entry_D2.bind("<Return>", entry_HEX_Event)  # 输入框回车触发

        # 添加函数为类方法
        self.Update_UI = Update_UI
        self.Update_UI_HEX = Update_UI_HEX

        # 添加页面到页面列表
        self.pages.append(colorpalette_page)



        """【更多选项页】"""
        #页面索引
        settings_page = ctk.CTkFrame(self.content_area)
        #主标题-边框
        label_main_frame = ctk.CTkFrame(settings_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0")
        label_main_frame.pack(anchor="center", padx=(0, 0), pady=15,)
        #主标题+图标
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="更多选项",
                                  text_color="white",
                                  padx=20,
                                  compound="left",
                                  image=self.settings_icon,
                                  font=("Microsoft YaHei UI", 20, "bold"))
        label_main.pack(padx=(5, 10), pady=5)

        # 设置帧索引-边框(E1)
        label_E1_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E1_frame.pack_propagate(False)
        label_E1_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 设置帧索引-文本(E1)
        label_E1 = ctk.CTkLabel(label_E1_frame,
                                text="设置帧索引",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E1.pack(side="left", padx=(5, 0), pady=0,)
        # 设置帧索引-滑块(E1)
        slider_E1 = ctk.CTkSlider(label_E1_frame,
                                  from_=0, to=100,
                                  number_of_steps=100,
                                  width=230,
                                  progress_color="#3B8ED0")
        slider_E1.pack(side="left", padx=(5, 5))
        # 设置帧索引-输入框(E1)
        entry_E1 = ctk.CTkEntry(label_E1_frame,
                                placeholder_text="index",
                                corner_radius=6,
                                border_width=2,
                                width=70,
                                height=label_all_h - 10,
                                justify="center",
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16),)
        entry_E1.pack(side="left", padx=(5, 5), pady=(1, 0))
        # 设置帧索引-开关(E1)
        switch_E1 = ctk.CTkSwitch(label_E1_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E1_Event())
        switch_E1.pack(side="right", padx=(5, 5), pady=0)  # 将开关放在右侧
        # 启用E1全部控件
        def Enabled_E1():
            label_E1.configure(text_color=['gray10', '#DCE4EE'])
            slider_E1.configure(state="normal", progress_color="#3B8ED0",button_color=['#3B8ED0', '#1F6AA5'])
            entry_E1.configure(state="normal", text_color=['gray10', '#DCE4EE'])
            switch_E1.configure(state="normal")
        # 禁用E1全部控件
        def Disabled_E1():
            label_E1.configure(text_color=["gray36","gray"])
            slider_E1.configure(state="disabled",progress_color="grey",button_color=['gray36', '#D5D9DE'])
            entry_E1.configure(state="disabled",text_color="grey")
            switch_E1.deselect()
            switch_E1_Event()
            switch_E1.configure(state="disabled")
        self.Disabled_E1 = Disabled_E1
        self.Enabled_E1 = Enabled_E1

        # 设置方位角-边框(E2)
        label_E2_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E2_frame.pack_propagate(False)
        label_E2_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 设置方位角-文本(E2)
        label_E2 = ctk.CTkLabel(label_E2_frame,
                                text="设置方位角",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E2.pack(side="left", padx=(5, 0), pady=0,)
        # 设置方位角-滑块(E2)
        slider_E2 = ctk.CTkSlider(label_E2_frame,
                                  from_=0, to=360,
                                  number_of_steps=360,
                                  width=230,
                                  progress_color="#3B8ED0")
        slider_E2.pack(side="left", padx=(5, 5))
        # 设置方位角-输入框(E2)
        entry_E2 = ctk.CTkEntry(label_E2_frame,
                                placeholder_text="angle",
                                corner_radius=6,
                                border_width=2,
                                width=70,
                                height=label_all_h - 10,
                                justify="center",
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16),)
        entry_E2.pack(side="left", padx=(5, 5), pady=(1, 0))
        # 设置方位角-开关(E2)
        switch_E2 = ctk.CTkSwitch(label_E2_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E2_Event())
        switch_E2.pack(side="right", padx=(5, 5), pady=0)
        # 启用E2全部控件
        def Enabled_E2():
            label_E2.configure(text_color=['gray10', '#DCE4EE'])
            slider_E2.configure(state="normal", progress_color="#3B8ED0",button_color=['#3B8ED0', '#1F6AA5'])
            entry_E2.configure(state="normal", text_color=['gray10', '#DCE4EE'])
            switch_E2.configure(state="normal")
        # 禁用E2全部控件
        def Disabled_E2():
            label_E2.configure(text_color=["gray36","gray"])
            slider_E2.configure(state="disabled",progress_color="grey",button_color=['gray36', '#D5D9DE'])
            entry_E2.configure(state="disabled",text_color="grey")
            switch_E2.deselect()
            switch_E2_Event()
            switch_E2.configure(state="disabled")
        self.Disabled_E2 = Disabled_E2
        self.Enabled_E2 = Enabled_E2

        # 设置方位角-边框(E3)
        label_E3_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E3_frame.pack_propagate(False)
        label_E3_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 设置自转速-文本(E3)
        label_E3 = ctk.CTkLabel(label_E3_frame,
                                text="设置自转速",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E3.pack(side="left", padx=(5, 0), pady=0,)
        # 设置自转速-滑块(E3)
        slider_E3 = ctk.CTkSlider(label_E3_frame,
                                  from_=0, to=100,
                                  number_of_steps=100,
                                  width=230,
                                  progress_color="#3B8ED0")
        slider_E3.pack(side="left", padx=(5, 5))
        # 设置自转速-输入框(E3)
        entry_E3 = ctk.CTkEntry(label_E3_frame,
                                placeholder_text="speed",
                                corner_radius=6,
                                border_width=2,
                                width=70,
                                height=label_all_h - 10,
                                justify="center",
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 16),)
        entry_E3.pack(side="left", padx=(5, 5), pady=(1, 0))
        # 设置自转速-开关(E3)
        switch_E3 = ctk.CTkSwitch(label_E3_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E3_Event())
        switch_E3.pack(side="right", padx=(5, 5), pady=0)
        # 启用E3全部控件
        def Enabled_E3():
            label_E3.configure(text_color=['gray10', '#DCE4EE'])
            slider_E3.configure(state="normal", progress_color="#3B8ED0",button_color=['#3B8ED0', '#1F6AA5'])
            entry_E3.configure(state="normal", text_color=['gray10', '#DCE4EE'])
            switch_E3.configure(state="normal")
        # 禁用E3全部控件
        def Disabled_E3():
            label_E3.configure(text_color=["gray36","gray"])
            slider_E3.configure(state="disabled", progress_color="grey",button_color=['gray36', '#D5D9DE'])
            entry_E3.configure(state="disabled", text_color="grey")
            switch_E3.deselect()
            switch_E3_Event()
            switch_E3.configure(state="disabled")
        self.Disabled_E3 = Disabled_E3
        self.Enabled_E3 = Enabled_E3

        # 自定义网段-边框(E4)
        label_E4_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E4_frame.pack_propagate(False)
        label_E4_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 自定义网段-文本(E4)
        label_E4 = ctk.CTkLabel(label_E4_frame,
                                text="自定义网段",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E4.pack(side="left", padx=(5, 5), pady=0)
        # 自定义网段-输入框(E4)
        entry_E4 = ctk.CTkEntry(label_E4_frame,
                                placeholder_text="手动指定扫描网段，如192.168.1.x",
                                corner_radius=8,
                                border_width=0,
                                width=265,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 14))
        entry_E4.pack(side="left",padx=(5, 1), pady=(1, 0))
        # 自定义网段-使能开关(E4)
        switch_E4 = ctk.CTkSwitch(label_E4_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E4_Event())
        switch_E4.pack(side="right", padx=(5, 5), pady=0)

        # 自定义地址-边框(E5)
        label_E5_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E5_frame.pack_propagate(False)
        label_E5_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 自定义地址-文本(E5)
        label_E5 = ctk.CTkLabel(label_E5_frame,
                                text="自定义地址",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E5.pack(side="left", padx=(5, 5), pady=0)
        # 自定义地址-输入框(E5)
        entry_E5 = ctk.CTkEntry(label_E5_frame,
                                placeholder_text="手动设置设备地址，如192.168.1.14",
                                corner_radius=8,
                                border_width=0,
                                width=265,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 14))
        entry_E5.pack(side="left", padx=(5, 1), pady=(1, 0))
        # 自定义地址-使能开关(E5)
        switch_E5 = ctk.CTkSwitch(label_E5_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E5_Event())
        switch_E5.pack(side="right", padx=(5, 5), pady=0)

        # 高德API密钥-边框(E6)
        label_E6_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E6_frame.pack_propagate(False)
        label_E6_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 高德API密钥-文本(E6)
        label_E6 = ctk.CTkLabel(label_E6_frame,
                                text="高德API密钥",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E6.pack(side="left", padx=(5, 0), pady=0,)
        # 高德API密钥-输入框(E6)
        entry_E6 = ctk.CTkEntry(label_E6_frame,
                                placeholder_text="推荐使用个人密钥，启用将解除限制",
                                corner_radius=8,
                                border_width=0,
                                show="·",
                                width=265,
                                height=label_all_h - 6,
                                bg_color="transparent",
                                font=("Microsoft YaHei UI", 14))
        entry_E6.pack(side="left",padx=(0, 1), pady=(1, 0))
        # 高德API密钥-显隐按钮(E6)
        self.hide_pwd_E6_state = True  # 密码显隐状态
        button_E6 = ctk.CTkButton(label_E6_frame,
                                  text="",
                                  width=30,
                                  height=32,
                                  corner_radius=8,
                                  image=self.hide_icon,
                                  fg_color="transparent",
                                  hover_color="lightgrey",
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: hide_show_pwd_E6())
        button_E6.pack(side="left", padx=(0, 5), pady=0)
        # 高德API密钥-使能开关(E6)
        switch_E6 = ctk.CTkSwitch(label_E6_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E6_Event())
        switch_E6.pack(side="right", padx=(5, 5), pady=0)
        # 高德API密钥-密钥显隐功能方法(E6)
        def hide_show_pwd_E6():
            if self.hide_pwd_E6_state:  # 当前隐藏-切换为显示
                self.hide_pwd_E6_state = False  # 更改状态
                entry_E6.configure(show="")  # 切换密码显示状态
                button_E6.configure(image=self.show_icon)  # 切换按钮图标
            else:  # 当前显示-切换为隐藏
                self.hide_pwd_E6_state = True  # 更改状态
                entry_E6.configure(show="·")  # 切换密码显示状态
                button_E6.configure(image=self.hide_icon)  # 切换按钮图标
        # 高德API密钥-状态同步(E6)
        if Private_api_key:
            switch_E6.select() # 开启开关
            entry_E6.delete(0, "end")   # 清空输入框
            entry_E6.insert(0, str(Gaode_api_key))  # 输入个人密钥
            entry_E6.configure(state="disabled", text_color="grey")
        else:
            pass

        # 高级选项-框架(E7)
        label_E7_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E7_frame.pack_propagate(False)
        label_E7_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 高级选项-文本(E7)
        label_E7 = ctk.CTkLabel(label_E7_frame,
                                text="更多调试项",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E7.pack(side="left", padx=(5, 5), pady=0)
        # 高级选项-重启按钮(E7)
        button_E7 = ctk.CTkButton(label_E7_frame,
                                    text="重启设备",
                                    width=130,
                                    height=30,
                                    font=("Microsoft YaHei UI", 14),
                                    command=lambda: button_E7_command())
        button_E7.pack(side="left", padx=(5, 5), pady=(1, 0))
        # 高级选项-允许帧索引超限-文本(E7)
        label_E7_1 = ctk.CTkLabel(label_E7_frame,
                                  text="解除帧索引限制",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 17))
        label_E7_1.pack(side="left", pady=0, padx=(32, 5))
        # 高级选项-允许帧索引超限-开关(E7)
        switch_E7 = ctk.CTkSwitch(label_E7_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E7_Event())
        switch_E7.pack(side="right", padx=(5, 5), pady=0)
        # 启用E7全部控件
        def Enabled_E7():
            label_E7.configure(text_color=['gray10', '#DCE4EE'])
            label_E7_1.configure(text_color=['gray10', '#DCE4EE'])
            button_E7.configure(state="normal")
            switch_E7.configure(state="normal")
        # 禁用E7全部控件
        def Disabled_E7():
            label_E7.configure(text_color=["gray36", "gray"])
            label_E7_1.configure(text_color=["gray36", "gray"])
            button_E7.configure(state="disabled")
            switch_E7.deselect()
            switch_E7_Event()
            switch_E7.configure(state="disabled")
        self.Disabled_E7 = Disabled_E7
        self.Enabled_E7 = Enabled_E7

        # 安装进系统-框架(E8)
        label_E8_frame = ctk.CTkFrame(settings_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=label_all_h)
        label_E8_frame.pack_propagate(False)
        label_E8_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 安装进系统-文本(E8)
        label_E8 = ctk.CTkLabel(label_E8_frame,
                                text="安装进系统",
                                padx=10,
                                font=("Microsoft YaHei UI", 18))
        label_E8.pack(side="left", padx=(5, 5), pady=0)
        # 安装进系统-安装按钮(E8)
        button_E8_1 = ctk.CTkButton(label_E8_frame,
                                    text="安装",
                                    width=60,
                                    height=30,
                                    font=("Microsoft YaHei UI", 14),
                                    command=lambda:button_E7_1_command())
        button_E8_1.pack(side="left", padx=(5, 5), pady=(1,0))
        if Main_Install_state:
            button_E8_1.configure(text="已安装",state="disabled")
        else:
            pass
        # 安装进系统-卸载按钮(E8)
        button_E8_2 = ctk.CTkButton(label_E8_frame,
                                    text="卸载",
                                    width=60,
                                    height=30,
                                    font=("Microsoft YaHei UI", 14),
                                    command=lambda: button_E7_2_command())
        button_E8_2.pack(side="left", padx=(5, 5), pady=(1,0))
        if not Main_Install_state:
            button_E8_2.configure(state="disabled")
        else:
            pass
        # 安装进系统-开始菜单文本(E8)
        label_E8_1 = ctk.CTkLabel(label_E8_frame,
                                  text="添加至开始菜单",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 17))
        label_E8_1.pack(side="left", pady=0, padx=(32, 5))
        # 安装进系统-开始菜单开关(E8)
        switch_E8 = ctk.CTkSwitch(label_E8_frame,
                                  text="",
                                  width=50,
                                  height=35,
                                  command=lambda: switch_E8_Event())
        switch_E8.pack(side="right", padx=(5, 5), pady=0)
        if Main_StartMenu_state:
            switch_E8.select()
        else:
            switch_E8.deselect()

        # 按钮操作-重启设备(E7)
        def button_E7_command():
            reboot_button_thread = threading.Thread(target=reboot_button)
            reboot_button_thread.daemon = True
            reboot_button_thread.start()
        def reboot_button():
            state = Reboot_Device(MainAddress)
            if state=="ForceReboot":
                Warning_Window("强制重启指令已发送！","Mine Compass 强制重启", False)
                self.PageA_Default_UI("未连接 (强制重启，请重新连接)")
                self.Disabled_E1()
                self.Disabled_E2()
                self.Disabled_E3()
                self.Disabled_E7()
            elif state==200:
                Info_Window("设备正在重启，请稍等","Mine Compass 重启", False)
                self.PageA_Default_UI("未连接 (设备重启, 请重新连接)")
                self.Disabled_E1()
                self.Disabled_E2()
                self.Disabled_E3()
                self.Disabled_E7()
            else:
                Warning_Window(f"设备重启失败，状态码:{state}","Mine Compass 重启", False)

        # 按钮操作-安装进系统(E8-1)
        def button_E7_1_command():
            # 安装进系统
            state1 = Install_to_system()
            if state1:
                button_E8_1.configure(text="已安装", state="disabled")
                button_E8_2.configure(state="normal")
            else:
                pass
            # 创建开始菜单
            state2 = Configure_StartMenu(mode=1)
            if state2:
                switch_E8.select()
            else:
                pass

        # 按钮操作-从系统卸载(E8-2)
        def button_E7_2_command():
            thread = threading.Thread(target=Uninstall_from_system)
            thread.daemon = True
            thread.start()
            # 关闭开始菜单按钮
            switch_E8.deselect()


        # 设置滑块默认值
        slider_E1.set(0)
        slider_E2.set(0)
        slider_E3.set(0)

        # 设置索引-滑块事件
        def slider_E1_Event(value):
            entry_E1.delete(0, "end")
            entry_E1.insert(0, str(int(value)))
        # 设置方位角-滑块事件
        def slider_E2_Event(value):
            entry_E2.delete(0, "end")
            entry_E2.insert(0, str(int(value)))
        # 设置自转速度-滑块事件
        def slider_E3_Event(value):
            entry_E3.delete(0, "end")
            entry_E3.insert(0, str(int(value)))

        # 滑块滚轮事件
        def slider_E1_Wheel_Event(event):
            value = slider_E1.get()
            value_max = int(slider_E1.cget("to"))
            value_min = int(slider_E1.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 1
                if value_min<=value_new<=value_max:
                    slider_E1.set(value_new)
                    slider_E1_Event(value_new)
                else:
                    slider_E1.set(value_min)
                    slider_E1_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 1
                if value_min <= value_new <= value_max:
                    slider_E1.set(value_new)
                    slider_E1_Event(value_new)
                else:
                    slider_E1.set(value_max)
                    slider_E1_Event(value_max)

        def slider_E2_Wheel_Event(event):
            value = slider_E2.get()
            value_max = int(slider_E2.cget("to"))
            value_min = int(slider_E2.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 3
                if value_min<=value_new<=value_max:
                    slider_E2.set(value_new)
                    slider_E2_Event(value_new)
                else:
                    slider_E2.set(value_min)
                    slider_E2_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 3
                if value_min <= value_new <= value_max:
                    slider_E2.set(value_new)
                    slider_E2_Event(value_new)
                else:
                    slider_E2.set(value_max)
                    slider_E2_Event(value_max)

        def slider_E3_Wheel_Event(event):
            value = slider_E3.get()
            value_max = int(slider_E3.cget("to"))
            value_min = int(slider_E3.cget("from_"))
            if event.delta > 0:  # 向上滚动
                value_new = value - 1
                if value_min<=value_new<=value_max:
                    slider_E3.set(value_new)
                    slider_E3_Event(value_new)
                else:
                    slider_E3.set(value_min)
                    slider_E3_Event(value_min)
            else:  # 鼠标向下滚动
                value_new = value + 1
                if value_min <= value_new <= value_max:
                    slider_E3.set(value_new)
                    slider_E3_Event(value_new)
                else:
                    slider_E3.set(value_max)
                    slider_E3_Event(value_max)


        # 设置索引-输入框事件
        def entry_E1_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_E1:
                return
            # 获取输入框内容
            try:
                value = float(entry_E1.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 100:
                # 在范围内-更新滑块
                smooth_set_slider(slider_E1, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_E1.get()
                entry_E1.delete(0, "end")
                entry_E1.insert(0, str(int(slider_value)))

        # 设置方位角-输入框事件
        def entry_E2_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_E2:
                return
            # 获取输入框内容
            try:
                value = float(entry_E2.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 360:
                # 在范围内-更新滑块
                smooth_set_slider(slider_E2, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_E2.get()
                entry_E2.delete(0, "end")
                entry_E2.insert(0, str(int(slider_value)))

        # 设置自转速度-输入框事件
        def entry_E3_Event(event):
            # 滑块拖动冲突检测
            if self.MouseState_slider_E3:
                return
            # 获取输入框内容
            try:
                value = float(entry_E3.get())
            except:
                value = -1
            # 判断范围
            if 0 <= value <= 100:
                # 在范围内-更新滑块
                smooth_set_slider(slider_E3, value, duration=50)
            else:
                # 不在范围内-使用滑块值
                slider_value = slider_E3.get()
                entry_E3.delete(0, "end")
                entry_E3.insert(0, str(int(slider_value)))

        # 【滑块鼠标点击检测】
        self.MouseState_slider_E1 = False
        self.MouseState_slider_E2 = False
        self.MouseState_slider_E3 = False
        # 获得焦点
        def MousePress_slider_E1(event):  # 滑块-E1-获得焦点
            self.MouseState_slider_E1 = True
        def MousePress_slider_E2(event):  # 滑块-E2-获得焦点
            self.MouseState_slider_E2 = True
        def MousePress_slider_E3(event):  # 滑块-E3-获得焦点
            self.MouseState_slider_E3 = True
        # 失去焦点
        def MouseRelease_slider_E1(event):  # 滑块-E1-失去焦点
            self.MouseState_slider_E1 = False
        def MouseRelease_slider_E2(event):  # 滑块-E2-失去焦点
            self.MouseState_slider_E2 = False
        def MouseRelease_slider_E3(event):  # 滑块-E3-失去焦点
            self.MouseState_slider_E3 = False
        # 绑定事件
        slider_E1.bind("<Button-1>", MousePress_slider_E1)
        slider_E2.bind("<Button-1>", MousePress_slider_E2)
        slider_E3.bind("<Button-1>", MousePress_slider_E3)
        slider_E1.bind("<MouseWheel>", slider_E1_Wheel_Event)
        slider_E2.bind("<MouseWheel>", slider_E2_Wheel_Event)
        slider_E3.bind("<MouseWheel>", slider_E3_Wheel_Event)
        slider_E1.bind("<ButtonRelease>", MouseRelease_slider_E1)
        slider_E2.bind("<ButtonRelease>", MouseRelease_slider_E2)
        slider_E3.bind("<ButtonRelease>", MouseRelease_slider_E3)

        # 绑定事件-帧索引(E1)
        slider_E1.configure(command=slider_E1_Event)  # 滑块变化时触发
        entry_E1.bind("<FocusOut>", entry_E1_Event)  # 输入框失去焦点触发
        entry_E1.bind("<Return>", entry_E1_Event)  # 输入框回车触发
        # 绑定事件-设置方位角(E2)
        slider_E2.configure(command=slider_E2_Event)  # 滑块变化时触发
        entry_E2.bind("<FocusOut>", entry_E2_Event)  # 输入框失去焦点触发
        entry_E2.bind("<Return>", entry_E2_Event)  # 输入框回车触发
        # 绑定事件-设置自转转速(E3)
        slider_E3.configure(command=slider_E3_Event)  # 滑块变化时触发
        entry_E3.bind("<FocusOut>", entry_E3_Event)  # 输入框失去焦点触发
        entry_E3.bind("<Return>", entry_E3_Event)  # 输入框回车触发

        # 开关状态
        self.state_switch_E1 = False
        self.state_switch_E2 = False
        self.state_switch_E3 = False
        self.state_switch_E4 = False
        self.state_switch_E5 = False
        self.state_switch_E6 = False
        self.state_switch_E7 = False
        self.state_switch_E8 = False

        # 开关事件-E1-设帧索引
        def switch_E1_Event():
            # 获取开关状态
            state = switch_E1.get()
            # 更改状态
            if state==0:
                self.state_switch_E1 = False
            elif state==1:
                self.state_switch_E1 = True
                self.state_switch_E2 = False
                self.state_switch_E3 = False
            # 执行操作
            if self.state_switch_E1:
                # 判断文本框
                entry_value = entry_E1.get()
                if entry_value=="":
                    slider_value = slider_E1.get()
                    entry_E1.delete(0, "end")
                    entry_E1.insert(0, str(int(slider_value)))
                # 刷新其他控件
                switch_E2.deselect()
                switch_E3.deselect()
                switch_E2_Event()
                switch_E3_Event()
                # 启动线程
                set_index_thread = threading.Thread(target=Set_Index_thread)
                set_index_thread.daemon = True
                set_index_thread.start()
            else:
                pass

        # 开关事件-E2-设置方位角
        def switch_E2_Event():
            # 获取状态
            state = switch_E2.get()
            # 更改状态
            if state == 0:
                self.state_switch_E2 = False
            elif state == 1:
                self.state_switch_E1 = False
                self.state_switch_E2 = True
                self.state_switch_E3 = False
            # 执行操作
            if self.state_switch_E2:
                # 判断文本框
                entry_value = entry_E2.get()
                if entry_value == "":
                    slider_value = slider_E2.get()
                    entry_E2.delete(0, "end")
                    entry_E2.insert(0, str(int(slider_value)))
                # 刷新其他控件
                switch_E1.deselect()
                switch_E3.deselect()
                switch_E1_Event()
                switch_E3_Event()
                # 启动线程
                set_azimuth_thread = threading.Thread(target=Set_Azimuth_thread)
                set_azimuth_thread.daemon = True
                set_azimuth_thread.start()
            else:
                pass

        # 开关事件-E3-启动旋转
        def switch_E3_Event():
            # 获取状态
            state = switch_E3.get()
            if state == 0:
                self.state_switch_E3 = False
            elif state == 1:
                self.state_switch_E1 = False
                self.state_switch_E2 = False
                self.state_switch_E3 = True
            # 执行操作
            if self.state_switch_E3:
                # 判断文本框
                entry_value = entry_E3.get()
                if entry_value == "":
                    slider_value = slider_E3.get()
                    entry_E3.delete(0, "end")
                    entry_E3.insert(0, str(int(slider_value)))
                # 刷新其他控件
                switch_E1.deselect()
                switch_E2.deselect()
                switch_E1_Event()
                switch_E2_Event()
                # 启动线程
                set_rotation_thread = threading.Thread(target=Set_Rotation_thread)
                set_rotation_thread.daemon = True
                set_rotation_thread.start()
            else:
                pass

        # 开关事件-E4-指定网段
        def switch_E4_Event():
            # 获取状态
            state = switch_E4.get()
            # 更改状态
            if state == 0:
                self.state_switch_E4 = False
            elif state == 1:
                self.state_switch_E4 = True
                self.state_switch_E5 = False
            # 执行操作
            if self.state_switch_E4:
                # 锁定当前控件
                entry_E4.configure(state="disabled",text_color="grey")
                # 刷新其他控件
                switch_E5.deselect()
                switch_E5_Event()
                # 获取网段
                network = entry_E4.get()
                # 检查网段是否合法
                check = Check_IPv4_Network(network)
                if check:
                    # 解析数据
                    network_list = network.split(".") # 分割
                    network_main = f"{network_list[0]}.{network_list[1]}.{network_list[2]}"
                    # 切换网段手动设置
                    print(f"手动设置网段：{network_main}")
                    Switch_Network_ManualMode(state=True,network=network_main)
                    self.button_A8.configure(text="扫描网段")
                    Info_Window("设置成功！请确认指南针和本机在同网段中！", "Mine Compass 网段设置", False)
                else:
                    switch_E4.deselect()
                    switch_E4_Event()
                    switch_E5_Event()
                    Warning_Window("输入的网段不合法！", "Mine Compass 网段设置", False)
            else:
                # 解锁当前控件
                entry_E4.configure(state="normal",text_color=['gray10', '#DCE4EE'])
                # 切换网段自动识别
                Switch_Network_ManualMode(state=False)
                self.button_A8.configure(text="扫描设备")


        # 开关事件-E5-指定IP
        def switch_E5_Event():
            # 获取状态
            state = switch_E5.get()
            # 更改状态
            if state == 0:
                self.state_switch_E5 = False
            elif state == 1:
                self.state_switch_E4 = False
                self.state_switch_E5 = True
            # 执行操作
            if self.state_switch_E5:
                # 锁定当前控件
                entry_E5.configure(state="disabled",text_color="grey")
                # 刷新其他控件
                switch_E4.deselect()
                switch_E4_Event()
                # 获取IP
                ip = entry_E5.get()
                # 检查IP是否合法
                check = Check_IPv4(ip)
                if check:
                    # 切换手动IP
                    Switch_Address_ManualMode(state=True,ip=ip)
                    # 更新界面
                    self.PageA_Default_UI("未连接 (指定IP)")
                    self.button_A8.configure(text="连接设备")
                    Info_Window("仅限调试！平时请勿开启此选项！","Mine Compass IP设置",False)
                else:
                    switch_E5.deselect()
                    switch_E4_Event()
                    switch_E5_Event()
                    Warning_Window("输入的IP地址不合法！","Mine Compass IP设置",False)
            else:
                # 解锁当前控件
                entry_E5.configure(state="normal",text_color=['gray10', '#DCE4EE'])
                # 切换自动扫描
                Switch_Address_ManualMode(state=False)
                self.button_A8.configure(text="扫描设备")

        # 开关事件-E6-设置个人密钥
        def switch_E6_Event():
            # 获取状态
            state = switch_E6.get()
            if state == 0:
                self.state_switch_E6 = False
            elif state == 1:
                self.state_switch_E6 = True
            # 执行操作
            if self.state_switch_E6:
                # 锁定当前控件
                entry_E6.configure(state="disabled",text_color="grey")
                # 读取用户密钥
                aip_key = entry_E6.get()
                # 加载用户密钥
                set_user_api_key_thread = threading.Thread(target=Set_User_API_Key,args=(aip_key,))
                set_user_api_key_thread.daemon = True
                set_user_api_key_thread.start()
            else:
                # 解锁当前控件
                entry_E6.configure(state="normal",text_color=['gray10', '#DCE4EE'])
                # 加载内置密钥
                Load_Built_API_Key()
                # 删除本地密钥文件
                try:
                    os.remove(f"{User_Appdata_Path}/MineCompass/Gaode-API-Key.bin")
                except Exception as error:
                    Error_Window(f"密钥文件销毁失败！\n{error}", "Mine Compass 个人密钥", False)

        # 开关事件-E7-解除帧索引限制
        def switch_E7_Event():
            # 获取状态
            state = switch_E7.get()
            # 更改状态
            if state == 0:
                self.state_switch_E7 = False
            elif state == 1:
                self.state_switch_E7 = True
            # 执行操作
            if self.state_switch_E7:
                Info_Window("解除限制可能会显示设计预期外的画面","Mine Compass",False)
            else:
                pass

        # 开关事件-E8-添加开始菜单
        def switch_E8_Event():
            # 获取状态
            state = switch_E8.get()
            # 更改状态
            if state == 0:
                self.state_switch_E8 = False
            elif state == 1:
                self.state_switch_E8 = True
            # 执行操作
            if self.state_switch_E8:
                if Main_Install_state:
                    Configure_StartMenu(mode=1)
                else:
                    self.state_switch_E8 = False
                    switch_E8.deselect()
                    switch_E8_Event()
                    Warning_Window("无法添加，程序未安装，请先点击安装按钮！","Mine Compass 安装程序", False)
            else:
                Configure_StartMenu(mode=0)
                pass

        # 设置帧索引线程
        def Set_Index_thread():
            index_old = -1
            while self.state_switch_E1:
                # 获取帧索引
                try:
                    index = slider_E1.get()
                    index = int(index)
                except:
                    time.sleep(0.05)
                    continue
                # 允许超限-直接设置
                if self.state_switch_E7:
                    if index_old!=index:
                        # 发送请求
                        POST_Index(MainAddress, index)
                # 不允许超限-转化后设置
                else:
                    index_new = index % 29
                    if index_old != index:
                        # 发送请求
                        POST_Index(MainAddress, index_new)
                index_old = index
                time.sleep(0.01)

        # 设置方位角线程
        def Set_Azimuth_thread():
            azimuth_old = -1
            while self.state_switch_E2:
                # 获取方位角
                try:
                    azimuth = slider_E2.get()
                    azimuth = int(azimuth)
                except:
                    time.sleep(0.05)
                    continue
                # 发送请求
                if azimuth_old != azimuth:
                    POST_Azimuth(MainAddress, azimuth)
                # 更新数据
                azimuth_old = azimuth
                time.sleep(0.01)

        # 设置自转速度线程
        def Set_Rotation_thread():
            index = 0
            while self.state_switch_E3:
                # 获取速度
                try:
                    speed = slider_E3.get()
                    speed = int(speed)
                except:
                    time.sleep(0.05)
                    continue
                # 速度判断
                if speed==0:
                    POST_Index(MainAddress, index)
                    time.sleep(0.5)
                    print("等待中")
                else:
                    # 计算间隔
                    frame_speed = (100 - speed) / 1000
                    print(f"帧速度：{frame_speed}")
                    # 显示帧
                    POST_Index(MainAddress, index)
                    index = index+1
                    if index>=29:
                        index = 0
                    # 暂停
                    time.sleep(frame_speed)

        self.pages.append(settings_page)  # 添加页面到页面列表



        """【程序信息页】"""
        #页面索引
        information_page = ctk.CTkFrame(self.content_area)
        #主标题-边框
        label_main_frame = ctk.CTkFrame(information_page,
                                        corner_radius=8,
                                        border_width=1,
                                        fg_color="#3B8ED0")
        label_main_frame.pack(anchor="center", padx=(0, 0), pady=15,)
        #主标题+图标
        label_main = ctk.CTkLabel(label_main_frame,
                                  text="相关信息",
                                  text_color="white",
                                  padx=20,
                                  compound="left",
                                  image=self.information_icon,
                                  font=("Microsoft YaHei UI", 20, "bold"))
        label_main.pack(padx=(5, 10), pady=5)  #标签内部间距

        # 程序信息-框架(F1)
        label_F1_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F1_frame.pack_propagate(False)
        label_F1_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 程序信息-文本-标题(F1)
        label_F1 = ctk.CTkLabel(label_F1_frame,
                                text="程序信息：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F1.pack(side="left", padx=(5, 5), pady=0)
        # 程序信息-图片(F1)
        image_label_F1 = ctk.CTkLabel(label_F1_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_main)
        image_label_F1.pack(side="left", padx=(0, 5), pady=0)
        # 程序信息-文本-内容(F1)
        label_F1_2 = ctk.CTkLabel(label_F1_frame,
                                  text="Mine Compass v1.2.0",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F1_2.pack(side="left", padx=(5, 5), pady=0)
        # 程序信息-复制按钮(F1)
        button_F1 = ctk.CTkButton(label_F1_frame,
                                  text="复制",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda: copy_F1_text())
        button_F1.pack(side="right", padx=(5, 10), pady=0)
        def copy_F1_text():
            label_F1_text = label_F1.cget("text")
            Copy_to_Clipboard(label_F1_text)

        # 项目地址-框架(F2)
        label_F2_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F2_frame.pack_propagate(False)
        label_F2_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 项目地址-文本-标题(F2)
        label_F2 = ctk.CTkLabel(label_F2_frame,
                                text="项目地址：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F2.pack(side="left", padx=(5, 5), pady=0)
        # 项目地址-图片(F2)
        image_label_F2 = ctk.CTkLabel(label_F2_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_github)
        image_label_F2.pack(side="left", padx=(0, 5), pady=0)
        # 项目地址-文本-内容(F2)
        label_F2_2 = ctk.CTkLabel(label_F2_frame,
                                  text="zzydd/MineCompass",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F2_2.pack(side="left", padx=(5, 5), pady=0)
        # 项目地址-复制按钮(F2)
        button_F2 = ctk.CTkButton(label_F2_frame,
                                  text="访问",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda:Open_URL("https://github.com/zzydd/MineCompass"))
        button_F2.pack(side="right", padx=(5, 10), pady=0)

        # 程序作者-框架(F3)
        label_F3_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F3_frame.pack_propagate(False)
        label_F3_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 程序作者-文本-标题(F3)
        label_F3 = ctk.CTkLabel(label_F3_frame,
                                text="程序作者：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F3.pack(side="left", padx=(5, 5), pady=0)
        # 程序作者-图片(F3)
        image_label_F3 = ctk.CTkLabel(label_F3_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_zzydd,)
        image_label_F3.pack(side="left", padx=(0, 5), pady=0)
        # 程序作者-文本-内容(F3)
        label_F3_2 = ctk.CTkLabel(label_F3_frame,
                                  text="ZZYDD",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F3_2.pack(side="left", padx=(5, 5), pady=0)
        # 程序作者-访问空间按钮(F3)
        button_F3 = ctk.CTkButton(label_F3_frame,
                                  text="空间",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda:Open_URL("https://space.bilibili.com/543085311"))
        button_F3.pack(side="right", padx=(5, 10), pady=0)

        # 界面设计-框架(F4)
        label_F4_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F4_frame.pack_propagate(False)
        label_F4_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 界面设计-文本-标题(F4)
        label_F4 = ctk.CTkLabel(label_F4_frame,
                                text="界面设计：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F4.pack(side="left", padx=(5, 5), pady=0)
        # 界面设计-图片(F4)
        image_label_F4 = ctk.CTkLabel(label_F4_frame,
                                      padx=0,
                                      text="",
                                      image=self.icon_fish)
        image_label_F4.pack(side="left", padx=(0, 5), pady=0)
        # 界面设计-文本-内容(F4)
        label_F4_2 = ctk.CTkLabel(label_F4_frame,
                                  text="spitting_Fish",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F4_2.pack(side="left", padx=(5, 5), pady=0)
        # 界面设计-访问空间按钮(F4)
        button_F4 = ctk.CTkButton(label_F4_frame,
                                  text="空间",
                                  width=60,
                                  height=30,
                                  font=("Microsoft YaHei UI", 14),
                                  command=lambda:Open_URL("https://space.bilibili.com/1298697780"))
        button_F4.pack(side="right", padx=(5, 10), pady=0)

        # 定位支持-框架(F5)
        label_F5_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F5_frame.pack_propagate(False)
        label_F5_frame.pack(anchor="center", padx=(0, 10), pady=(15, 0))
        # 定位支持-文本-标题(F5)
        label_F5 = ctk.CTkLabel(label_F5_frame,
                                text="定位支持：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F5.pack(side="left", padx=(5, 5), pady=0)
        # 定位支持-图片(F5)
        image_label_F5 = ctk.CTkLabel(label_F5_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_gaode)
        image_label_F5.pack(side="left", padx=(0, 5), pady=0)
        # 定位支持-文本-内容(F5)
        label_F5_2 = ctk.CTkLabel(label_F5_frame,
                                  text="高德地图开放平台",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F5_2.pack(side="left", padx=(5, 5), pady=0)

        # 技术指导-框架(F6)
        label_F6_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F6_frame.pack_propagate(False)
        label_F6_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 技术指导-文本-标题(F6)
        label_F6 = ctk.CTkLabel(label_F6_frame,
                                text="技术指导：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F6.pack(side="left", padx=(5, 5), pady=0)
        # 技术指导-图片(F6)
        image_label_F6 = ctk.CTkLabel(label_F6_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_chatgpt)
        image_label_F6.pack(side="left", padx=(0, 5), pady=0)
        # 技术指导-文本-内容(F6)
        label_F6_2 = ctk.CTkLabel(label_F6_frame,
                                  text="OpenAI ChatGPT",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F6_2.pack(side="left", padx=(5, 5), pady=0)

        # 图标来源-框架(F7)
        label_F7_frame = ctk.CTkFrame(information_page,
                                      corner_radius=8,
                                      border_width=2,
                                      border_color="grey",
                                      width=label_all_w,
                                      height=50)
        label_F7_frame.pack_propagate(False)
        label_F7_frame.pack(anchor="center", padx=(0, 10), pady=(20, 0))
        # 图标来源-文本-标题(F7)
        label_F7 = ctk.CTkLabel(label_F7_frame,
                                text="图标来源：",
                                padx=10,
                                font=("Microsoft YaHei UI", 20))
        label_F7.pack(side="left", padx=(5, 5), pady=0)
        # 图标来源-图片(F7)
        image_label_F7 = ctk.CTkLabel(label_F7_frame,
                                      text="",
                                      padx=0,
                                      image=self.icon_igoutu)
        image_label_F7.pack(side="left", padx=(0, 5), pady=0)
        # 图标来源-文本-内容(F7)
        label_F7_2 = ctk.CTkLabel(label_F7_frame,
                                  text="ICONS8",
                                  padx=10,
                                  font=("Microsoft YaHei UI", 18))
        label_F7_2.pack(side="left", padx=(5, 5), pady=0)


        self.pages.append(information_page)  #添加页面到页面列表

        """【类方法】"""

        # 【焦点移除判断】
        Entry_List = [entry_B5, entry_B6, entry_C5, entry_C6_1, entry_C6_2,
                      entry_D1R, entry_D1G, entry_D1B, entry_D1V, entry_D2,
                      entry_E1, entry_E2, entry_E3, entry_E4, entry_E5,  entry_E6 ]
        def remove_focus(event):
            """移除输入框焦点"""
            widget = event.widget  #获取控件
            while widget:
                if widget in Entry_List:
                    return  # 在白名单列表中-不转移焦点
                widget = widget.master  # 递归获取父控件
            self.focus()  # 不在白名单列表中-转移焦点


        # 绑定鼠标点击事件
        self.bind("<Button-1>", remove_focus)

        # 【平滑设置滑块】
        self.smooth_slider_stop_list = [] # 需要停止动画的滑块列表
        self.smooth_slider_executing_list = [] # 正在执行动画的滑块列表
        def smooth_set_slider(slider, target_value, duration=0.5, steps=50):
            # 判断动画是否在执行
            if slider in self.smooth_slider_executing_list:
                self.smooth_slider_stop_list.append(slider)

            self.smooth_slider_executing_list.append(slider)
            current_value = slider.get()  # 获取当前值
            steps = 50  # 动画的帧数
            step_duration = duration // steps  # 每帧持续时间
            step_value = (target_value - current_value) / steps  # 每帧的值变化
            # print(f"当前值：{current_value}；动画帧数：{steps}；每帧时间：{step_duration}；每帧变化：{step_value}")
            def update_step(step=0):
                nonlocal current_value
                if (step < steps) and (slider not in self.smooth_slider_stop_list):
                    current_value += step_value
                    slider.set(current_value)
                    slider.update_idletasks()
                    slider.after(step_duration, update_step, step + 1)  # 下一帧
                elif slider in self.smooth_slider_stop_list:
                    if slider in self.smooth_slider_stop_list:
                        self.smooth_slider_stop_list.remove(slider)
                    if slider in self.smooth_slider_executing_list:
                        self.smooth_slider_executing_list.remove(slider)
                    # print("新动画执行，取消老动画")
                    pass
                else:
                    slider.set(target_value)  # 确保最终值精确到目标值
                    slider.update_idletasks()
                    if slider in self.smooth_slider_stop_list:
                        self.smooth_slider_stop_list.remove(slider)
                    if slider in self.smooth_slider_executing_list:
                        self.smooth_slider_executing_list.remove(slider)
            update_step()  # 开始动画


    # 【页面显示】
    def show_page(self, index):
        """切换显示页面"""
        global MainState
        global MainPageIndex
        MainPageIndex = index
        # 判断状态
        if index in [0,4,5]: # 页面白名单
            pass
        else:
            if not MainState:
                index = 0
                Info_Window("设备未连接，请先连接设备！","Mine Compass", True)

        # 任何页面切换时执行的命令
        self.simulate_nether = False # 停止模拟下界
        self.UpdateColor_Continuous = False  # 停止上传颜色
        self.ColorCycle_state = False # 停止色彩循环


        # 指定页面展示时执行的命令
        if index==0:
            if MainState:
                # 启动命令线程
                page0_cmd_thread = threading.Thread(target=GET_Info, args=(MainAddress,))
                page0_cmd_thread.daemon = True
                page0_cmd_thread.start()
        elif index==1:
            def page1_cmd():
                # 获取信息
                ssid,pwd = GET_WiFi(MainAddress)
                self.label_B1.configure(text=f"设备地址：   {MainAddress}")
                self.label_B2.configure(text=f"WLAN连接：{ssid}")
                # 更新密码
                self.label_B3_password = pwd
                encrypt_pwd = ('・' * len(f"{self.label_B3_password}"))  # 替换密码
                self.label_B3.configure(text=f"WLAN密码：{encrypt_pwd}")  # 隐藏密码
            # 启动命令线程
            page1_cmd_thread = threading.Thread(target=page1_cmd)
            page1_cmd_thread.daemon = True
            page1_cmd_thread.start()

        elif index==2:
            def page2_cmd():
                # 更新模拟下界开关状态
                self.state_switch_C7 = False
                self.switch_C7.deselect()
                # 获取坐标
                lng,lat = GET_Spawn(MainAddress)
                Now_SpawnPoint = (f"{lng}°E  {lat}°N")
                # 读取缓存(出生点坐标)
                state_SpawnPoint_read, Cache_SpawnPoint = Read_Cache("Cache-SpawnPoint.ini")
                # 判断位置变化
                if Now_SpawnPoint==self.label_C1_SpawnPoint and self.Location_Decode_state:
                    print("位置与当前相同,无需重新定位")
                elif Now_SpawnPoint==Cache_SpawnPoint and state_SpawnPoint_read and self.Location_Decode_state:
                    print("位置与缓存相同,无需重新定位")
                    self.label_C1_SpawnPoint = Now_SpawnPoint
                    # 读取地址缓存
                    state_SpawnAddress_read, Cache_SpawnAddress = Read_Cache("Cache-SpawnAddress.ini")
                    if state_SpawnAddress_read:
                        self.label_C2_SpawnAddress = Cache_SpawnAddress
                    else:
                        self.label_C2_SpawnAddress = "北京天安门"
                else:
                    # 地理编码
                    self.label_C1_SpawnPoint = Now_SpawnPoint
                    Now_SpawnAddress, state = Location_Decode(lng,lat)
                    self.label_C2_SpawnAddress = Now_SpawnAddress
                # 更新输入框
                self.label_C1.configure(text=f"坐标：{self.label_C1_SpawnPoint}")
                self.label_C2.configure(text=f"地址：{self.label_C2_SpawnAddress}")
            # 启动命令线程
            page2_cmd_thread = threading.Thread(target=page2_cmd)
            page2_cmd_thread.daemon = True
            page2_cmd_thread.start()

        elif index==3:
            def page3_cmd():
                # 上传默认颜色
                POST_Color(MainAddress,"#00FFFF") #不要问为什么是这个颜色，问就因为是我喜欢
                # 刷新按钮状态
                self.state_switch_D4 = False
                self.state_switch_D5 = False
                self.switch_D4.deselect()
                self.switch_D5.deselect()
            # 启动命令线程
            page3_cmd_thread = threading.Thread(target=page3_cmd)
            page3_cmd_thread.daemon = True
            page3_cmd_thread.start()

        elif index==4:
            def page4_cmd():
                if MainState:
                    GET_Info(MainAddress)
                    self.Enabled_E1()
                    self.Enabled_E2()
                    self.Enabled_E3()
                    self.Enabled_E7()
                else:
                    self.Disabled_E1()
                    self.Disabled_E2()
                    self.Disabled_E3()
                    self.Disabled_E7()
            # 启动命令线程
            page4_cmd_thread = threading.Thread(target=page4_cmd)
            page4_cmd_thread.daemon = True
            page4_cmd_thread.start()

        elif index==5:
            pass
        # 切换页面
        for widget in self.content_area.winfo_children():  # 隐藏当前显示的所有子控件
            widget.pack_forget()
        self.pages[index].pack(fill="both", expand=True)  # 显示选定页面

    #【关闭窗口】
    def close_window(self):
        self.quit()  # 停止主事件循环
        self.destroy() # 销毁窗口


#---------------------------------------------------------------------------------------------------------------------------------
"""【功能函数】"""

#【获取系统时间】
def Get_DateTime(sec=False):
    struct_time = time.localtime() # 获取结构化时间
    NowDate = time.strftime("%Y-%m-%d", struct_time) # 当前日期
    if sec:
        NowTime = time.strftime("%H:%M:%S", struct_time) # 当前时间(带秒)
    else:
        NowTime = time.strftime("%H:%M", struct_time)  # 当前时间(不带秒)
    return NowDate, NowTime


#【复制内容到剪切板】
def Copy_to_Clipboard(content):
    try:
        pyperclip.copy(content)
        return True
    except:
        return False


#【打开URL】
def Open_URL(url):
    os.popen(f"start {url}")


#【加载图片资源】
def Load_Image(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


#【设置全局延时设置】
def Set_MainTimeout(mode):
    global MainTimeout
    global MainScanTimeout
    if mode==1:
        MainTimeout = 1
        MainScanTimeout = 0.25
    elif mode==2:
        MainTimeout = 3
        MainScanTimeout = 0.5
    elif mode==3:
        MainTimeout = 5
        MainScanTimeout = 1
    elif mode==4:
        MainTimeout = 10
        MainScanTimeout = 2
    else:
        MainTimeout = 3
        MainScanTimeout = 0.5

#【错误弹窗】
def Error_Window(content, title, pause):
    """( 内容，标题，是否中断 )"""
    #中断模式弹窗
    if pause:
        win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONERROR)
    #同步模式弹窗
    else:
        #弹窗窗口
        def window_main():
            win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONERROR)
        #弹窗线程
        winbox_t = threading.Thread(target=window_main)
        winbox_t.daemon = True  # 设置为daemon线程
        winbox_t.start()  # 启动弹窗线程


#【警告弹窗】
def Warning_Window(content, title, pause):
    """( 内容，标题，是否中断 )"""
    #中断模式弹窗
    if pause:
        win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONWARNING)
    #同步模式弹窗
    else:
        #弹窗窗口
        def window_main():
            win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONWARNING)
        #弹窗线程
        winbox_t = threading.Thread(target=window_main)
        winbox_t.daemon = True  # 设置为daemon线程
        winbox_t.start()  # 启动弹窗线程


#【信息弹窗】
def Info_Window(content, title, pause):
    """( 内容，标题，是否中断 )"""
    #中断模式弹窗
    if pause:
        win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONASTERISK)
    #同步模式弹窗
    else:
        #弹窗窗口
        def window_main():
            win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONASTERISK)
        #弹窗线程
        winbox_t = threading.Thread(target=window_main)
        winbox_t.daemon = True  # 设置为daemon线程
        winbox_t.start()  # 启动弹窗线程


#【疑问弹窗】
def Questions_Window(content, title, pause):
    """( 内容，标题，是否中断 )"""
    #中断模式弹窗
    if pause:
        win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONQUESTION)
    #同步模式弹窗
    else:
        #弹窗窗口
        def window_main():
            win32api.MessageBox(0, f"{content}", f"{title}", win32con.MB_ICONQUESTION)
        #弹窗线程
        winbox_t = threading.Thread(target=window_main)
        winbox_t.daemon = True  # 设置为daemon线程
        winbox_t.start()  # 启动弹窗线程


#【判断wifi协议】
def Get_WiFi_Version(version):
    if version == "802.11":
        return "802.11"
    elif version == "802.11b":
        return "WiFi 1"
    elif version == "802.11a" or version == "802.11g":
        return "WiFi 2"
    elif version == "802.11n":
        return "WiFi 4"
    elif version == "802.11ac":
        return "WiFi 5"
    elif version == "802.11ax":
        return "WiFi 6"
    elif version == "802.11be":
        return "WiFi 7"
    elif version == "802.11bn":
        return "WiFi 8" #写了再说。你用的是外星科技吗？！
    else:
        return version


#【获取系统WLAN SSID+密码】
def Get_Computer_wifi():
    # return(名称，密码，频率，信道，协议，编码, 信息)
    result = ""
    encoding_type = "utf-8"
    try:
        # 获取WLAN编码
        encoding_list = ["utf-8", "utf-16", "utf-32", "gbk"]
        for encoding_type in encoding_list:
            try:
                #获取SSID编码
                result = subprocess.check_output("chcp 65001 & netsh wlan show interfaces",
                                                 shell=True, encoding=encoding_type)
                break
            except:
                encoding_type = ("utf-8")
            #未知编码
            Warning_Window("无效数据，SSID编码失败", "Mine Compass WLAN", False)
            return "", "", "", "", "", "", "未知编码"


        # 获取SSID
        ssid_match = re.search(r"SSID\s*:\s*(.+)", result)
        if ssid_match:
            wlan_ssid = ssid_match.group(1).strip() #匹配成功
        else:
            Warning_Window("无法获取SSID，请确保开启系统WLAN！", "Mine Compass WLAN", False)
            return "", "", "", "", "", "", "SSID获取失败"

        # 读取波段类型
        band_match = re.search(r"Band\s*:\s*(\S.*)", result)
        if band_match:
            wlan_band = band_match.group(1).strip()
        else:
            wlan_band = ("Unknown")
            pass

        # 获取信号频道
        channel_match = re.search(r"Channel\s*:\s*(\d+)", result)
        if channel_match:
            wlan_channel = int(channel_match.group(1).strip()) #获取频道
        else:
            wlan_channel = 0
            pass

        # 获取协议版本
        version_match = re.search(r"Radio type\s*:\s*(\S+)", result)
        if version_match:
            wlan_version = version_match.group(1).strip()
        else:
            wlan_version = f"Unknown"
            pass

        # 获取密码
        command = f'chcp 65001 & netsh wlan show profile name="{wlan_ssid}" key=clear'
        profile_info = subprocess.check_output(command, shell=True, encoding=encoding_type)
        password_match = re.search(r"Key Content\s*:\s*(.+)", profile_info)
        if password_match:
            wlan_pwd = password_match.group(1).strip()
        else:
            wlan_pwd = ""  # 没有设置密码或未能找到密码

        # 返回数据
        # (名称，密码，频率，信道，协议，编码, 信息)
        return wlan_ssid, wlan_pwd, wlan_band, wlan_channel, wlan_version, encoding_type, "系统WLAN获取成功"

    except Exception as error:
        Error_Window(f"系统WLAN获取出错：\n{error}","Mine Compass WLAN", False)
        return "", "", "", "", "", "", f"系统WLAN获取出错：{error}"


'''
【内置高德API使用限制】

[地理编码] 日总量5000次；用户每日限制40次；每分钟限制6次。| 合计：每日至少能提供125位用户 
[地理解码] 日总量5000次；用户每日限制40次；每分钟限制6次。| 合计：每日至少能提供125位用户 
[IP定位]  日总量5000次；用户每日限制40次；每分钟限制6次。| 合计：每日至少能提供125位用户 
'''

#【地理编码-地址推坐标】[高德API]
def Location_Encoding (address):
    # [统计API使用]
    if not Private_api_key:
        # 读取数据
        NowDate, NowTime = Get_DateTime()   # 获取时间
        reg_Date, reg_type = Build_Gaode_api_Stats("LocationEncoding_LatestDate",mode=0) # 读取注册表日期
        reg_Time, reg_type = Build_Gaode_api_Stats("LocationEncoding_LatestTime",mode=0) # 读取注册表时间
        reg_Data_Daily, reg_type = Build_Gaode_api_Stats("LocationEncoding_Daily",mode=0) # 读取注册表数据-每日值
        reg_Data_Minute, reg_type = Build_Gaode_api_Stats("LocationEncoding_Minute", mode=0)  # 读取注册表数据-每分钟值
        # 转化格式
        reg_Data_Daily = int(reg_Data_Daily)
        reg_Data_Minute = int(reg_Data_Minute)
        # 日期相同 且 时间不同
        if NowDate==reg_Date and NowTime!=reg_Time:
            # 判断每日限制
            if reg_Data_Daily<=40:
                print(f"内置接口调用-地理编码-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily+1
                Build_Gaode_api_Stats("LocationEncoding_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理编码-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内置地理编码接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                             "Mine Compass 地理编码", False)
                return 90, 0, False
            # 重置每分钟限制
            print(f"内置接口调用-地理编码-每分钟限制重置")
            Build_Gaode_api_Stats("LocationEncoding_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            Build_Gaode_api_Stats("LocationEncoding_Minute", mode=1, data="0")  # 写入注册表数据

        # 日期相同 且 时间相同
        elif NowDate==reg_Date and NowTime==reg_Time:
            # 判断每日限制
            if reg_Data_Daily <= 40:
                print(f"内置接口调用-地理编码-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily + 1
                Build_Gaode_api_Stats("LocationEncoding_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理编码-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内置地理编码接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                               "Mine Compass 地理编码", False)
                return 90, 0, False
            # 判断每分钟限制
            if reg_Data_Minute <= 6:
                print(f"内置接口调用-地理编码-每分钟次数未超限-当前次数{reg_Data_Minute}")
                # 递增数据
                reg_Data_Minute = reg_Data_Minute + 1
                Build_Gaode_api_Stats("LocationEncoding_Minute", mode=1, data=f"{reg_Data_Minute}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理编码-每分钟次数超限-当前次数{reg_Data_Minute}")
                Warning_Window(f"内置地理编码接口访问过快！请暂缓1分钟！(6次/分钟)\n使用个人API密钥可解除限制",
                               "Mine Compass 地理编码", False)
                return 90, 0, False

        # 日期不同-重置数据
        else:
            # 写入注册表
            print("内置接口调用-地理编码-重置所有数据")
            state, info = Build_Gaode_api_Stats("LocationEncoding_LatestDate", mode=1, data=NowDate)  # 写入注册表日期
            state, info = Build_Gaode_api_Stats("LocationEncoding_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            state, info = Build_Gaode_api_Stats("LocationEncoding_Daily", mode=1, data="0")  # 写入注册表数据
            state, info = Build_Gaode_api_Stats("LocationEncoding_Minute", mode=1, data="0")  # 写入注册表数据

    else:
        print("使用个人密钥，无需限制")
        pass

    # [调用API]
    try:
        api = f"http://restapi.amap.com/v3/geocode/geo?address={address}&key={Gaode_api_key}"  # 地理编码API接口
        response = requests.get(api) # 访问API
        response_data = response.json() #解析数据
        # 读取数据
        if response_data['status'] == '1':
            #解析坐标
            location = response_data['geocodes'][0]['location']
            lng, lat = location.split(',')
            return float(lng) , float(lat), True # (经度，维度，状态)
        else:
            #解析错误
            try:
                state_code = response_data['status']
                info_text = response_data['info']
                info_code = response_data['infocode']
                Warning_Window(f"坐标获取失败！\n状态 {state_code}；代码 {info_code}；错误 {info_text}",
                               "Mine Compass 地理编码",False)
            except Exception as error:
                state_code = "0"
                info_text = "UnknownError"
                info_code = "0"
                Error_Window(f"坐标获取失败！未知错误！\n{error}",
                             "Mine Compass 地理编码",False)
            return 90, 0, False
    except Exception as error:
        Error_Window(f"坐标获取失败！未知错误！\n{error}",
                     "Mine Compass 地理编码", False)
        return 90, 0, False


#【地理解码-坐标推地址】[高德API]
def Location_Decode (lng,lat):
    # [统计API使用]
    if not Private_api_key:
        # 读取数据
        NowDate, NowTime = Get_DateTime()   # 获取时间
        reg_Date, reg_type = Build_Gaode_api_Stats("LocationDecode_LatestDate",mode=0) # 读取注册表日期
        reg_Time, reg_type = Build_Gaode_api_Stats("LocationDecode_LatestTime",mode=0) # 读取注册表时间
        reg_Data_Daily, reg_type = Build_Gaode_api_Stats("LocationDecode_Daily",mode=0) # 读取注册表数据-每日值
        reg_Data_Minute, reg_type = Build_Gaode_api_Stats("LocationDecode_Minute", mode=0)  # 读取注册表数据-每分钟值
        # 转化格式
        reg_Data_Daily = int(reg_Data_Daily)
        reg_Data_Minute = int(reg_Data_Minute)
        # 日期相同 且 时间不同
        if NowDate==reg_Date and NowTime!=reg_Time:
            # 判断每日限制
            if reg_Data_Daily<=40:
                print(f"内置接口调用-地理解码-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily+1
                Build_Gaode_api_Stats("LocationDecode_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理解码-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内置地理解码接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                             "Mine Compass 地理解码", False)
                return "北京天安门", False
            # 重置每分钟限制
            print(f"内置接口调用-地理解码-每分钟限制重置")
            Build_Gaode_api_Stats("LocationDecode_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            Build_Gaode_api_Stats("LocationDecode_Minute", mode=1, data="0")  # 写入注册表数据

        # 日期相同 且 时间相同
        elif NowDate==reg_Date and NowTime==reg_Time:
            # 判断每日限制
            if reg_Data_Daily <= 40:
                print(f"内置接口调用-地理解码-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily + 1
                Build_Gaode_api_Stats("LocationDecode_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理解码-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内置地理解码接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                               "Mine Compass 地理解码", False)
                return "北京天安门", False
            # 判断每分钟限制
            if reg_Data_Minute <= 6:
                print(f"内置接口调用-地理解码-每分钟次数未超限-当前次数{reg_Data_Minute}")
                # 递增数据
                reg_Data_Minute = reg_Data_Minute + 1
                Build_Gaode_api_Stats("LocationDecode_Minute", mode=1, data=f"{reg_Data_Minute}")  # 写入注册表数据
            else:
                print(f"内置接口调用-地理解码-每分钟次数超限-当前次数{reg_Data_Minute}")
                Warning_Window(f"内置地理解码接口访问过快！请暂缓1分钟！(6次/分钟)\n使用个人API密钥可解除限制",
                               "Mine Compass 地理解码", False)
                return "北京天安门", False

        # 日期不同-重置数据
        else:
            # 写入注册表
            print("内置接口调用-地理解码-重置所有数据")
            state, info = Build_Gaode_api_Stats("LocationDecode_LatestDate", mode=1, data=NowDate)  # 写入注册表日期
            state, info = Build_Gaode_api_Stats("LocationDecode_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            state, info = Build_Gaode_api_Stats("LocationDecode_Daily", mode=1, data="0")  # 写入注册表数据
            state, info = Build_Gaode_api_Stats("LocationDecode_Minute", mode=1, data="0")  # 写入注册表数据

    else:
        print("使用个人密钥，无需限制")
        pass

    # [调用API]
    try:
        api = f"http://restapi.amap.com/v3/geocode/regeo?location={lng},{lat}&key={Gaode_api_key}" #逆地理编码API接口
        response = requests.get(api) # 访问API
        response_data = response.json() #解析数据
        # 读取数据
        if response_data['status'] == '1':
            #解析地址
            address = response_data['regeocode']['formatted_address']
            if str(address) in ["","[]"]:
                Info_Window("当前坐标未找到结果", "Mine Compass 地理解码", False)
                return "北京天安门", False
            else:
                return address, True
        else:
            #解析错误
            try:
                state_code = response_data['status']
                info_text = response_data['info']
                info_code = response_data['infocode']
                Warning_Window(f"地址获取失败！\n状态 {state_code}；代码 {info_code}；错误 {info_text}",
                               "Mine Compass 地理解码",False)
            except Exception as error:
                Error_Window(f"地址获取失败！未知错误！\n{error}",
                             "Mine Compass 地理解码",False)
            return "北京天安门", False
    except Exception as error:
        Error_Window(f"地址获取失败！未知错误！\n{error}",
                     "Mine Compass 地理解码", False)
        return "北京天安门", False


#【转化坐标】
def Location_Convert(dms_str):
    try:
        # 处理字符串
        dms_str = dms_str.replace("'","′")
        dms_str = dms_str.replace("’", "′")
        dms_str = dms_str.replace("''","″")
        dms_str = dms_str.replace('"', "″")
        dms_str = dms_str.replace("‘’", "″")
        # 匹配格式
        pattern_1 = r"([-+]?\d+)°(\d+)′(\d+(?:\.\d+)?)″" # 匹配格式：DDD°MM′SS.SSS″
        pattern_2 = r"([-+]?\d+)°(\d+(?:\.\d+)?)′"       # 匹配格式：DDD°MM.MMMM′
        match_1 = re.match(pattern_1, dms_str)  # 匹配1
        match_2 = re.match(pattern_2, dms_str)  # 匹配2

        # 判断格式+提取数值
        if match_1:
            # 格式1
            degrees, minutes, seconds = map(float, match_1.groups())
        elif match_2:
            # 格式2
            degrees, minutes = map(float, match_2.groups())
            seconds = 0
        else:
            # 格式错误
            degrees, minutes, seconds = 0, 0, 0

        # 转化
        decimal = abs(degrees) + minutes / 60 + seconds / 3600
        decimal = round(decimal,6)
        # 负数判断
        if degrees<0:
            decimal = -decimal
        else:
            pass
        # 返回数据
        return decimal
    except Exception as error:
        Error_Window(f"坐标转化失败！未知错误！\n{error}",
                     "Mine Compass 坐标转化", False)
        return 0


#【IP定位】[高德API]
def Location_IP():
    # [统计API使用]
    if not Private_api_key:
        # 读取数据
        NowDate, NowTime = Get_DateTime()   # 获取时间
        reg_Date, reg_type = Build_Gaode_api_Stats("IP_Positioning_LatestDate",mode=0) # 读取注册表日期
        reg_Time, reg_type = Build_Gaode_api_Stats("IP_Positioning_LatestTime",mode=0) # 读取注册表时间
        reg_Data_Daily, reg_type = Build_Gaode_api_Stats("IP_Positioning_Daily",mode=0) # 读取注册表数据-每日值
        reg_Data_Minute, reg_type = Build_Gaode_api_Stats("IP_Positioning_Minute", mode=0)  # 读取注册表数据-每分钟值
        # 转化格式
        reg_Data_Daily = int(reg_Data_Daily)
        reg_Data_Minute = int(reg_Data_Minute)
        # 日期相同 且 时间不同
        if NowDate==reg_Date and NowTime!=reg_Time:
            # 判断每日限制
            if reg_Data_Daily<=40:
                print(f"内置接口调用-IP定位-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily+1
                Build_Gaode_api_Stats("IP_Positioning_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-IP定位-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内-IP定位接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                             "Mine Compass-IP定位", False)
                return "北京天安门", 0, 0, False
            # 重置每分钟限制
            print(f"内置接口调用-IP定位-每分钟限制重置")
            Build_Gaode_api_Stats("IP_Positioning_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            Build_Gaode_api_Stats("IP_Positioning_Minute", mode=1, data="0")  # 写入注册表数据

        # 日期相同 且 时间相同
        elif NowDate==reg_Date and NowTime==reg_Time:
            # 判断每日限制
            if reg_Data_Daily <= 40:
                print(f"内置接口调用-IP定位-每日次数未超限-当前次数{reg_Data_Daily}")
                # 递增数据
                reg_Data_Daily = reg_Data_Daily + 1
                Build_Gaode_api_Stats("IP_Positioning_Daily", mode=1, data=f"{reg_Data_Daily}")  # 写入注册表数据
            else:
                print(f"内置接口调用-IP定位-每日次数超限-当前次数{reg_Data_Daily}")
                Warning_Window(f"今日内-IP定位接口使用次数已用完！(40次/日)\n建议注册并使用个人API密钥以解除限制",
                               "Mine Compass-IP定位", False)
                return "北京天安门", 0, 0, False
            # 判断每分钟限制
            if reg_Data_Minute <= 6:
                print(f"内置接口调用-IP定位-每分钟次数未超限-当前次数{reg_Data_Minute}")
                # 递增数据
                reg_Data_Minute = reg_Data_Minute + 1
                Build_Gaode_api_Stats("IP_Positioning_Minute", mode=1, data=f"{reg_Data_Minute}")  # 写入注册表数据
            else:
                print(f"内置接口调用-IP定位-每分钟次数超限-当前次数{reg_Data_Minute}")
                Warning_Window(f"内-IP定位接口访问过快！请暂缓1分钟！(6次/分钟)\n使用个人API密钥可解除限制",
                               "Mine Compass-IP定位", False)
                return "北京天安门", 0, 0, False

        # 日期不同-重置数据
        else:
            # 写入注册表
            print("内置接口调用-IP定位-重置所有数据")
            state, info = Build_Gaode_api_Stats("IP_Positioning_LatestDate", mode=1, data=NowDate)  # 写入注册表日期
            state, info = Build_Gaode_api_Stats("IP_Positioning_LatestTime", mode=1, data=NowTime)  # 写入注册表时间
            state, info = Build_Gaode_api_Stats("IP_Positioning_Daily", mode=1, data="0")  # 写入注册表数据
            state, info = Build_Gaode_api_Stats("IP_Positioning_Minute", mode=1, data="0")  # 写入注册表数据

    else:
        print("使用个人密钥，无需限制")
        pass

    # [调用API]
    try:
        # 请求API
        api = f"http://restapi.amap.com/v3/ip?&key={Gaode_api_key}"  # 自动获取IP
        response = requests.get(api)    # 访问API
        response_data = response.json() # 解析数据

        if response_data['status'] == '1':
            #解析地址数据
            province = response_data["province"] #省份
            city = response_data["city"] #城市
            address = (f"{province}{city}") #地理地址
            # 解析区域坐标--
            rectangle = response_data["rectangle"]  # 区域范围
            area = rectangle.split(';')
            lng1, lat1 = map(float, area[0].split(','))
            lng2, lat2 = map(float, area[1].split(','))
            # 计算中心点
            center_lng = (lng1 + lng2) / 2
            center_lat = (lat1 + lat2) / 2
            center_lng = round(center_lng, 6)
            center_lat = round(center_lat, 6)
            #返回数据
            return address,center_lng,center_lat, True
        else:
            # 解析错误
            try:
                state_code = response_data['status']
                info_text = response_data['info']
                info_code = response_data['infocode']
                Warning_Window(f"IP定位失败！\n状态 {state_code}；代码 {info_code}；错误 {info_text}",
                               "Mine Compass IP定位", False)
            except Exception as error:
                Error_Window(f"地址获取失败！未知错误！\n{error}",
                             "Mine Compass IP定位", False)
            return "北京天安门", 0, 0, False
    except Exception as error:
        Error_Window(f"地址获取失败！未知错误！\n{error}",
                     "Mine Compass IP定位", False)
        return "北京天安门", 0, 0, False


#【颜色转化】
# RGB转HEX
def RGB_to_HEX(r,g,b):
    # 限定范围
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    # 格式化为16进制
    hex_color = f"#{r:02X}{g:02X}{b:02X}"
    return hex_color
# HEX转RGB
def HEX_to_RGB(hex_color):
    # 格式化
    hex_color = hex_color.lstrip('#').lower()
    # 检查长度
    if len(hex_color) != 6:
        Warning_Window("16进制颜色输入长度错误！","Mine Compass 颜色转化", True)
        return 255,255,255
    # 检查输入
    for i in range(0, 6, 2):
        if not all(c in '0123456789abcdef' for c in hex_color[i:i + 2]):
            Warning_Window("16进制颜色输入格式错误！", "Mine Compass 颜色转化", True)
            return 255,255,255
    # 转化颜色
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

# RGB转HSV
def RGB_to_HSV(r,g,b):
    # 格式化RGB
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    # 转化
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # 转化色相H范围
    h = h*360
    return h, s, v

# HSV转RGB
def HSV_to_RGB(h,s,v):
    # 转化色相
    h = h / 360.0
    # 转化
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    # 转化范围
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return r, g, b



#【修改系统光标】
# 光标常量
OCR_NORMAL = 32512  # 标准箭头光标
OCR_CROSS = 32515  # 十字光标

# 修改系统光标
def Set_Cursor(cursor_type):
    # 加载光标
    cursor = ctypes.windll.user32.LoadCursorW(None, cursor_type)
    # 设置光标
    check = ctypes.windll.user32.SetSystemCursor(cursor, OCR_NORMAL)
    return check

# 恢复系统光标
def Reset_Cursor():
    # 恢复默认
    check = ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0)
    return check


#【屏幕取色】

# 鼠标左击检测
def Mouse_Left_Click():
    left_click = ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000 != 0
    return left_click
# ESC检测
def Press_ESC_Key():
    esc_key_pressed = ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000 != 0
    return esc_key_pressed
# 回车检测
def Press_Enter_Key():
    enter_key_pressed = ctypes.windll.user32.GetAsyncKeyState(0x0D) & 0x8000 != 0
    return enter_key_pressed

# 取色
def Get_Color_at_Cursor():
    # 定义 POINT 结构
    point = ctypes.create_string_buffer(8)  # POINT 结构需要 8 字节（两个 long，每个 4 字节）
    # 获取鼠标当前位置
    ctypes.windll.user32.GetCursorPos(point)
    x, y = ctypes.c_long.from_buffer(point, 0).value, ctypes.c_long.from_buffer(point, 4).value
    # 获取屏幕设备上下文并读取像素值
    hdc = ctypes.windll.user32.GetDC(0)  # 0 表示全屏设备上下文
    pixel = ctypes.windll.gdi32.GetPixel(hdc, x, y)
    ctypes.windll.user32.ReleaseDC(0, hdc)  # 释放设备上下文
    # 解析 RGB 值
    r = pixel & 0xFF
    g = (pixel >> 8) & 0xFF
    b = (pixel >> 16) & 0xFF
    # 更新数值
    return r, g, b

#【循环屏幕取色】

# [颜色获取进程]
def GET_COLOR_Loop_GET(GET_COLOR_List,delay=0.05,mode=0):
    # 设置进程DPI
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    # 模式0-循环取色
    if mode==0:
        while True:
            #取色
            r,g,b = Get_Color_at_Cursor()
            # print(f"颜色获取进程：{r},{g},{b}")
            # 更新变量
            try:
                GET_COLOR_List[0] = r
                GET_COLOR_List[1] = g
                GET_COLOR_List[2] = b
            except EOFError:
                # 出错终止
                try:
                    GET_COLOR_List[3] = True
                except:
                    pass
                break
            # 停止判断
            stop = GET_COLOR_List[3]
            if stop:
                break
            # 循环间隔
            time.sleep(delay)
        print("【结束】屏幕取色进程结束")

    # 模式1-单次取色
    elif mode==1:
        # 取色
        r, g, b = Get_Color_at_Cursor()
        try:
            GET_COLOR_List[0] = r
            GET_COLOR_List[1] = g
            GET_COLOR_List[2] = b
        except EOFError:
            # 出错终止
            try:
                GET_COLOR_List[3] = True
            except:
                pass

# [界面更新线程]
def GET_COLOR_Loop_READ(delay=0.05,hex_mode=1):
    while True:
        # 读取变量
        r = GET_COLOR_List[0]
        g = GET_COLOR_List[1]
        b = GET_COLOR_List[2]
        stop = GET_COLOR_List[3]
        # 计算亮度
        h,s,v = RGB_to_HSV(r, g, b)
        v = round(float(v),4)
        # print(f"界面更新线程：{r},{g},{b},{v},{stop}")
        # 更新界面
        app.Update_UI(int(r),int(g),int(b),float(v),hex_mode,1)
        # 停止判断
        if stop:
            break
        # 间隔
        time.sleep(delay)
    print("【结束】界面更新线程结束")

# [颜色预览线程]
def GET_COLOR_Loop_Preview(delay=0.01):
    while True:
        # 读取变量
        r = GET_COLOR_List[0]
        g = GET_COLOR_List[1]
        b = GET_COLOR_List[2]
        stop = GET_COLOR_List[3]
        # 更新界面
        app.Update_UI_HEX(r,g,b)
        # 停止判断
        if stop:
            break
        # 间隔
        time.sleep(delay)
    print("【结束】颜色预览线程结束")

# [停止检测线程]
def GET_COLOR_Loop_STOP():
    global GET_COLOR_STATE
    # 延时启动
    time.sleep(0.8)
    # 等待停止指令
    while True:
        if Press_ESC_Key():
            break
        if Press_Enter_Key():
            break
        if Mouse_Left_Click():
            break
        time.sleep(0.01)
    # 发送指令
    GET_COLOR_List[3] = True
    GET_COLOR_STATE = False
    Reset_Cursor()
    print("【结束】停止检测线程结束")




# 【取色启动器】
GET_COLOR_STATE = False
def GET_COLOR(delay_get=0.05,delay_read=0.05,delay_preview=0.05,main_mode=0,preview_mode=1):

    global GET_COLOR_STATE
    if not GET_COLOR_STATE:
        # 连续取色模式
        if main_mode==0:
            # 更新状态
            GET_COLOR_STATE = True
            GET_COLOR_List[0] = 0
            GET_COLOR_List[1] = 0
            GET_COLOR_List[2] = 0
            GET_COLOR_List[3] = False
            # 修改光标
            Set_Cursor(OCR_CROSS)
            # 启动取色进程
            get_color_progress = multiprocessing.Process(target=GET_COLOR_Loop_GET,args=(GET_COLOR_List,delay_get))
            get_color_progress.daemon = True
            get_color_progress.start()
            print("【启动】颜色获取进程启动完毕")
            # 启动界面更新线程
            update_color_thread = threading.Thread(target=lambda:GET_COLOR_Loop_READ(delay_read,preview_mode))
            update_color_thread.daemon = True
            update_color_thread.start()
            print("【启动】界面更新线程启动完毕")
            # 启动颜色预览
            color_preview_thread = threading.Thread(target=lambda:GET_COLOR_Loop_Preview(delay_preview))
            color_preview_thread.daemon = True
            color_preview_thread.start()
            print("【启动】颜色预览线程启动完毕")
            # 启动停止检测
            stop_check_thread = threading.Thread(target=GET_COLOR_Loop_STOP)
            stop_check_thread.daemon = True
            stop_check_thread.start()
            print("【启动】停止检测线程启动完毕")
            return None

        # 单次取色模式
        elif main_mode==1:
            # 更新状态
            GET_COLOR_STATE = True
            GET_COLOR_List[0] = 0
            GET_COLOR_List[1] = 0
            GET_COLOR_List[2] = 0
            GET_COLOR_List[3] = False
            # 启动取色进程
            get_color_progress = multiprocessing.Process(target=GET_COLOR_Loop_GET, args=(GET_COLOR_List, delay_get,1))
            get_color_progress.daemon = True
            get_color_progress.start()
            get_color_progress.join()
            print(GET_COLOR_List)
            pass

    else:
        print("【警告】屏幕取色已启动")

    if main_mode==2:
        GET_COLOR_List[3] = True
        GET_COLOR_STATE = False
        Reset_Cursor()



#【局域网扫描设备】

# 获取本机IP+网段
def Get_HostNetwork():
    global MainNetwork
    # 获取IP
    host_ip = socket.gethostbyname(HostName)
    # 获取网段
    network_list = host_ip.split(".")
    host_network = (f"{network_list[0]}.{network_list[1]}.{network_list[2]}")
    if Network_ManualMode:
        pass # 手动指定网段模式
    else:
        MainNetwork = host_network

    return host_ip


# 扫描专用请求函数
def GET_Info_Scan(ip):
    try:
        api = (f'http://{ip}/info')  #API接口
        response = requests.get(api, timeout=MainScanTimeout) #请求
        ReturnCode = response.status_code
        if ReturnCode == 200: #请求成功
            return True
        else: #请求失败
            return False
    except:
        return False


#扫描线程
def ScanIP_thread(network,ip_start,ip_end,index):
    global MainState
    global MainAddress
    global MainScanState
    global MainScanProgressList
    # 遍历扫描所有IP
    for ip_now in range(ip_start, ip_end+1):
        if MainScanState:
            # 发送请求
            state = GET_Info_Scan(f"{network}.{ip_now}")
            # print(f"正在扫描IP：{network}.{ip_now}")
            # 计算进度
            progress = (ip_now-ip_start+1)/(ip_end-ip_start+1) #计算进度 (已扫描数+1)/(总个数)
            progress = round(progress,5) #进度保留5为小数
            try:
                #更新线程进度
                MainScanProgressList[index-1] = progress
            except:
                pass
            if state:
                # 扫描成功-更新地址
                MainState = True
                MainAddress = (f"{network}.{ip_now}")
                print(f'扫描成功！IP地址：{network}.{ip_now}')
                try:
                    MainScanState = False #修改线程总开关
                except:
                    pass
                break #扫描成功，停止扫描
            else:
                pass
        else:
            break

#扫描进度统计线程
def ScanProgress_thread ():
    global MainProgress
    while MainScanState:
        MainProgress = np.mean(MainScanProgressList) #统计所有线程平均进度
        MainProgress = round(MainProgress*100,2) #保留2位小数并换算成百分比
        print(f"扫描进度：{'%.2f'% MainProgress}%")#格式化并打印进度
        if MainProgress>=100:
            break #进度达到100，结束进程
        time.sleep(0.2)
    #结束处理
    MainProgress = 100  #扫描结束，直接拉满进度
    print(f"扫描进度：{'%.2f'% MainProgress}%") #格式化并打印进


# 启动局域网扫描
def Scan_Network():
    global MainState
    global MainAddress
    global MainProgress
    global MainScanState
    global MainScanProgressList
    # 更新数据
    MainState = False
    MainScanState = True  # 扫描总状态
    MainProgress = 0  # 扫描进度(0-100,float)
    MainScanProgressList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 扫描进度列表
    # 更新网段
    Get_HostNetwork()
    # 尝试连接初始地址
    state_default = GET_Info_Scan(f"192.168.4.1")
    # 读取上次缓存地址
    state_read, cache_ip = Read_Cache("Cache-IP.ini")
    # 检查缓存地址
    if state_read:
        check_cache_ip = Check_IPv4(cache_ip)
    else:
        check_cache_ip = False
    # 尝试连接缓存地址
    if check_cache_ip:
        state_cache = GET_Info_Scan(f"{cache_ip}")
    else:
        state_cache = False
    # 判断模式
    if state_default:
        # 初始地址连接成功
        MainState = True
        MainAddress = (f"192.168.4.1")
        MainScanState = False
        print(f'扫描成功！IP地址：192.168.4.1 (初始地址)')
    elif state_cache:
        # 缓存地址连接成功
        MainState = True
        MainAddress = (f"{cache_ip}")
        MainScanState = False
        print(f'扫描成功！IP地址：{cache_ip} (缓存地址)')
    else:
        # 普通模式-执行扫描
        print("开始扫描...")
        # 启动扫描统计线程
        ST_P = threading.Thread(target=ScanProgress_thread)  # 创建进度统计线程
        ST_P.daemon = True  # 设置为daemon线程
        ST_P.start()  # 启动进度统计线程
        # 启动扫描线程
        ScanThreadList = []  # 创建线程列表
        for i in range(16):  # 扫描线程数
            start_ip = i * 16  # 起始IP
            end_ip = start_ip + 15  # 结束IP
            ScanThread = threading.Thread(target=ScanIP_thread, args=(MainNetwork, start_ip, end_ip, i + 1))  # 创建扫描线程
            ScanThreadList.append(ScanThread)  # 添加线程至列表
            ScanThread.daemon = True  # 设置为daemon线程
            ScanThread.start()  # 启动线程
        # 等待扫描线程
        for st in ScanThreadList:
            st.join()
        # 等待扫描进度统计线程
        ST_P.join()
    # 写入缓存(设备IP)
    Write_Cache(f"Cache-IP.ini",f"{MainAddress}")
    # 返回数据(设备IP)
    if MainState:
        print("设备扫描成功！")
        MainScanState = False
        return True, MainAddress
    else:
        print("未发现设备！")
        MainScanState = False
        return False, "127.0.0.1"


#【手动设置网段切换】
def Switch_Network_ManualMode(state, network="192.168.1"):
    global MainNetwork
    global Network_ManualMode
    if state:
        print(f"开启手动网段模式: {network}")
        Network_ManualMode = True
        MainNetwork = network
    else:
        print("关闭手动网段模式")
        Network_ManualMode = False
        MainNetwork = Get_HostNetwork()

#【手动设置IP切换】
def Switch_Address_ManualMode(state, ip="127.0.0.1"):
    global MainAddress
    global Address_ManualMode
    if state:
        print("开启手动IP模式")
        Address_ManualMode = True
        MainAddress = ip
        ResetMainInfo()
    else:
        print("关闭手动IP模")
        Address_ManualMode = False



#【重置数据】
def ResetMainInfo():
    global HostName
    global MainState
    global MainAddress
    MainState = False  # 主状态
    if Address_ManualMode:
        pass
    else:
        MainAddress = "127.0.0.1"
    HostName = socket.gethostname()


#【检查IPv4】
def Check_IPv4(ip):
    ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}'
                              r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')
    check = ipv4_pattern.match(ip)
    return check

#【检查IPv4网段】
def Check_IPv4_Network(network):
    pattern = re.compile(
        r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){2}'
        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'
        r'(\.([0-9a-zA-Z]+|x))?(/([0-9]|[1-2][0-9]|3[0-2]))?$'
    )
    check = pattern.match(network)
    return check


#【获取CPUID】
# 【获取 CPU ID】
def Get_CPUID():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'ProcessorId'],
            capture_output=True, text=True, startupinfo=startupinfo
        )
        lines = result.stdout.strip().split("\n")
        cpuid = lines[2].strip() if len(lines) > 2 else "Unknown"
        return cpuid
    except:
        return "ERROR2025ZZYDD"

# 【获取主板序列号】
def Get_Motherboard_SN():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            ['wmic', 'baseboard', 'get', 'SerialNumber'],
            capture_output=True, text=True, startupinfo=startupinfo
        )
        lines = result.stdout.strip().split("\n")
        serial = lines[2].strip() if len(lines) > 2 else "Unknown"
        return serial
    except:
        return "ERROR2025ZZYDD"


#【加载内置API密钥数据】
def Load_Built_API_Key():
    try:
        # 导入数据
        import api_key
        global Gaode_api_key
        global Private_api_key
        # 提取数据
        raw_data = api_key.API_Key_Data
        # 提取二进制数据
        bin_data = raw_data().key
        # 进行Base64解码 →  加密API密钥
        encrypt_data = base64.b64decode(bin_data)
        # 加载Fernet密钥
        key = Fernet(api_key_pwd)
        # 进行Fernet解密
        api_key_data = bytearray(key.decrypt(encrypt_data))
        # 进行UTF-16解码
        main_api_key = api_key_data.decode("utf-16")
        # 设置数据
        Gaode_api_key = main_api_key
        # 设置状态
        Private_api_key = False
        return True,None
    except Exception as error:
        return False,error

#【加载(设置)用户API密钥】
def Set_User_API_Key(api_key):
    global Gaode_api_key
    global Private_api_key
    # 加密并写入文件
    state, encrypt_data = Encrypt_UserData(api_key)
    if state:
        # 写入文件
        with open(f"{User_Appdata_Path}/MineCompass/Gaode-API-Key.bin", "wb") as file:
            file.write(encrypt_data)
        # 加载密钥
        Gaode_api_key = api_key
        # 更改状态
        Private_api_key = True
    else:
        Private_api_key = False
        pass


#【加密用户数据】
def Encrypt_UserData(data):
    try:
        # 获取硬件唯一标识
        cpuid = Get_CPUID() #CPUID
        serial = Get_Motherboard_SN() #主板SN
        pwd = (f"{cpuid}@{serial}") # 生成密码
        # 生成密钥
        pwd_sha256 = hashlib.sha256(pwd.encode('utf-8'))
        bin_key = base64.urlsafe_b64encode(pwd_sha256.digest())
        main_key = Fernet(bin_key)  # 主密钥
        # 加密数据
        encode_data = str(data).encode("utf-8") # 编码数据
        encrypt_data = main_key.encrypt(encode_data) # 加密
        # 返回数据
        return True,encrypt_data
    except Exception as error:
        Error_Window(f"数据加密出错！\n{error}","Mine Compass 数据加密", True)
        return False,None

#【解密用户数据】
def Decrypt_UserData(encrypt_data):
    # 获取硬件唯一标识
    try:
        cpuid = Get_CPUID()  # CPUID
        serial = Get_Motherboard_SN()  # 主板SN
        pwd = (f"{cpuid}@{serial}")  # 生成密码
        # 生成密钥
        pwd_sha256 = hashlib.sha256(pwd.encode('utf-8'))
        bin_key = base64.urlsafe_b64encode(pwd_sha256.digest())
        main_key = Fernet(bin_key)  # 主密钥
        # 解密数据
        decrypt_data = bytearray(main_key.decrypt(encrypt_data)) # 解密
        data = decrypt_data.decode("utf-8") # 解码
        # 返回数据
        return True,data
    except Exception as error:
        Error_Window(f"数据解密失败！请确保设备和文件合法！\n{error}","Mine Compass 数据解密", True)
        return False, None


#【加密内置数据】
def Encrypt_BuildData(data):
    try:
        # 加载密钥
        main_key = Fernet(api_key_pwd)
        # 加密数据
        encode_data = str(data).encode("utf-8") # 编码数据
        encrypt_data = main_key.encrypt(encode_data) # 加密
        # 返回数据
        return True,encrypt_data
    except Exception as error:
        Error_Window(f"数据加密出错！\n{error}","Mine Compass 内置加密", True)
        return False,None

#【解密内置数据】
def Decrypt_BuildData(encrypt_data):
    # 获取硬件唯一标识
    try:
        # 加载密钥
        main_key = Fernet(api_key_pwd)
        # 解密数据
        decrypt_data = bytearray(main_key.decrypt(encrypt_data)) # 解密
        data = decrypt_data.decode("utf-8") # 解码
        # 返回数据
        return True,data
    except Exception as error:
        Error_Window(f"数据解密失败！请确密钥和文件正确！\n{error}","Mine Compass 内置解密", True)
        return False, None


#【内置高德API使用统计】
def Build_Gaode_api_Stats(api,mode,data=""):
    '''
    api: 使用的API类型
    mode: 操作类型，0=读取，1=写入
    '''
    # [读取]
    if mode==0:
        try:
            # 打开注册表
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\MineCompass", 0, winreg.KEY_READ)
            # 读取键值
            reg_value, reg_type = winreg.QueryValueEx(reg_key, f"{api}")
            # 解密
            state,value = Decrypt_BuildData(reg_value)
            # 返回
            if state:
                return value, reg_type
            else:
                print("解密出错")
                return -1, None
        except FileNotFoundError:
            print("键值不存在")
            return -1, None
        except Exception as error:
            Error_Window(f"注册表读取失败！\n{error}","Mine Compass 读取注册表", False)
            return -1, None

    # [写入]
    else:
        try:
            # 加密数据
            state,bin_data = Encrypt_BuildData(data)
            if state:
                # 创建注册表
                reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\MineCompass")
                # 写入键值
                winreg.SetValueEx(reg_key, f"{api}", 0, winreg.REG_BINARY,bin_data)
                return True, True
            else:
                return False, "Encrypt_BuildData False"
        except Exception as error:
            Error_Window(f"注册表写入失败！\n{error}","Mine Compass 写入注册表", False)
            return False, error

#【创建快捷方式】
def Create_Shortcut(target, shortcut_path, icon_path=None):
    # 创建Shell对象
    shell = win32com.client.Dispatch("WScript.Shell")
    # 创建快捷方式对象
    shortcut = shell.CreateShortCut(shortcut_path)
    # 设置快捷方式的目标路径
    shortcut.Targetpath = target
    # 设置快捷方式的起始位置（即工作目录）
    shortcut.WorkingDirectory = os.path.dirname(target)
    # 如果提供了图标路径，则设置图标
    if icon_path:
        shortcut.IconLocation = icon_path
    # 保存快捷方式
    shortcut.save()


#【安装进系统】
def Install_to_system():
    global Main_Install_state
    try:
        # 复制文件
        with open(MainProgram,"rb") as file:
            data = file.read()
        with open(f"{User_Appdata_Path}/MineCompass/MineCompass.exe","wb") as file:
             file.write(data)
        # 创建快捷方式
        Create_Shortcut(target=f"{User_Appdata_Path}/MineCompass/MineCompass.exe",
                        shortcut_path=f"{User_Desktop_Path}/MCompass.lnk")
        Main_Install_state = True
        # 弹窗提示
        Info_Window("Mine Compass 安装成功！","Mine Compass 安装程序", False)
        return True
    except Exception as error:
        Main_Install_state = False
        Error_Window(f"Mine Compass 安装失败！\n{error}", "Mine Compass 安装程序", True)
        return False


#【从系统卸载】
def Uninstall_from_system():
    global Main_Install_state
    global Main_StartMenu_state
    try:
        # 删除快捷方式
        try:
            os.remove(f"{User_Desktop_Path}/MCompass.lnk")
        except:
            pass
        # 创建删除脚本
        script = ('''
        @echo off
        chcp 65001> nul
        title Mine Compass 卸载程序
        color 06
        cd /d %~dp0
        cd /d ..
        echo.
        echo.准备中，请等待3秒...
        echo.
        timeout /t 3 /NOBREAK >nul
        cls
        echo.
        echo.【Mine Compass 卸载程序】
        echo.
        echo.将删除 Mine Compass 的所有数据！包括个人密钥和所有配置！
        echo.(指南针固件里的配置信息不会被清除)
        echo.
        echo.终止卸载请关闭此窗口，按任意键开始卸载！
        echo.完成后，卸载程序也将自毁。
        echo.
        echo.[按任意键开始卸载]→
        pause >nul
        taskkill /f /im MineCompass.exe
        rmdir /s /q MineCompass & msg %username% /time:5 "Mine Compass 卸载完成！" & exit
        ''')
        # 写入脚本
        with open(f"{User_Appdata_Path}/MineCompass/Uninstall.bat","w",encoding="utf-8") as file:
            file.write(script.replace("        ",""))
        # 执行脚本
        os.system(f"start {User_Appdata_Path}/MineCompass/Uninstall.bat")
        # 删除开始菜单
        Configure_StartMenu(mode=0)
        Main_Install_state = False
        Main_StartMenu_state = False
        # 退出程序
        time.sleep(1)
        Info_Window("江湖再见！", "Mine Compass 告别", False)
        time.sleep(3)
        app.close_window() # 关闭主窗口
    except Exception as error:
        Error_Window(f"卸载程序出错！手动卸载请删除以下目录:\n {User_Appdata_Path}\\MineCompass\n\n错误信息:\n {error}",
                     "Mine Compass 卸载程序", True)
        app.close_window() # 关闭主窗口

#【开始菜单选项】
def Configure_StartMenu(mode=0):
    global Main_StartMenu_state
    if mode==1 and Main_Install_state:
        # 创建开始菜单快捷方式
        Create_Shortcut(target=f"{User_Appdata_Path}/MineCompass/MineCompass.exe",
                        shortcut_path=f"{User_Menu_Path}/Mine Compass.lnk")
        Main_StartMenu_state = True
        print("开始菜单图标已添加")
        return True
    elif mode == 1 and not Main_Install_state:
        print("程序未安装")
        return False
    elif mode==0:
        try:
            os.remove(f"{User_Menu_Path}/Mine Compass.lnk")
            print("开始菜单图标已删除")
        except FileNotFoundError:
            print("开始菜单图标不存在")
            pass
        except Exception as error:
            Error_Window(f"开始菜单项移除失败！\n{error}","Mine Compass 安装程序", False)
        return False
    else:
        print("状态异常")
        return False

#【读取缓存】
def Read_Cache(file):
    try:
        # 打开文件
        with open (f"{User_Appdata_Path}/MineCompass/{file}","r",encoding="utf-8") as file:
            data = file.read()
        # 返回数据
        return True, data
    except FileNotFoundError:
        return False, None
    except Exception as error:
        Error_Window(f"缓存读取出错！\n{error}", "Mine Compass 缓存", False)
        return False, None

#【写入缓存】
def Write_Cache(file,data):
    try:
        # 打开文件
        with open (f"{User_Appdata_Path}/MineCompass/{file}","w",encoding="utf-8") as file:
            file.write(data)
        # 返回数据
        return True
    except FileNotFoundError:
        return False
    except Exception as error:
        Error_Window(f"缓存写入出错！\n{error}", "Mine Compass 缓存", False)
        return False


# 【连接检测线程】
def Connect_Detecting():
    global MainState
    print("[检测线程] 检测线程启动")
    Failed_Times = 0 # 失败次数
    while Connect_Detecting_State:
        if MainState:
            state, ip = GET_IP(ip=MainAddress,timeout=1)
            if state:
                Failed_Times = 0
                print("[检测线程] 设备已连接")
            elif not state and MainPageIndex==1 and MainAddress=="192.168.4.1":
                print("[检测线程] 设备未连接-网络配置")
            else:
                Failed_Times = Failed_Times+1
                print("[检测线程] 设备连接失败")
            if Failed_Times>=3:
                MainState = False
                app.PageA_Default_UI(text="连接断开 (设备离线)")
                app.show_page(0)
                Warning_Window("连接断开！请检查设备状态！","Mine Compass",False)
                print("[检测线程] 设备断开连接")
            else:
                pass
            time.sleep(2)
        else:
            print("[检测线程] 设备未连接")
            time.sleep(5)

    print("[检测线程] 检测线程退出")





#---------------------------------------------------------------------------------------------------------------------------------
"【请求API接口】"

# [1]【获取IP】
def GET_IP(ip,timeout=0):
    try:
        api = (f'http://{ip}/ip')  #API接口
        if timeout==0:
            response = requests.get(api, timeout=MainTimeout) #请求
        else:
            response = requests.get(api, timeout=timeout)  # 请求
        ReturnCode = response.status_code
        if ReturnCode == 200: #请求成功
            text = response.text
            print(text)
            return True,text
        else: #请求失败
            return False,None
    except:
        return False,None

# [2]【设置索引】
def POST_Index(ip, index):
    # 设置请求的 URL
    api = f"http://{ip}/setIndex?index={index}"
    try:
        # 发送 POST 请求
        response = requests.post(api)
        code = response.status_code
        return code
    except:
        return False

# [3]【获取信息】
def GET_Info(ip):
    try:
        api = (f'http://{ip}/info')  #API接口
        response = requests.get(api, timeout=MainTimeout) #请求
        ReturnCode = response.status_code
        if ReturnCode == 200: #请求成功
            data = json.loads(response.text) #解析数据
            buildDate = data["buildDate"]
            buildTime = data["buildTime"]
            buildVersion = data["buildVersion"]
            gitBranch = data["gitBranch"]
            gitCommit = data["gitCommit"]
            return True, buildDate,buildTime,buildVersion,gitBranch,gitCommit
        else: #请求失败
            return False, False, False, False, False, False
    except:
        return False, False, False, False, False, False

# [4]【获取WiFi】
def GET_WiFi(ip):
    try:
        api = (f'http://{ip}/wifi')  #API接口
        response = requests.get(api, timeout=MainTimeout) #请求
        ReturnCode = response.status_code
        if ReturnCode == 200: #请求成功
            data = json.loads(response.text) #解析数据
            ssid = data["ssid"]
            password = data["password"]
            return ssid,password
        else: #请求失败
            return False, False
    except:
        return False, False

# [5]【获取出生点】
def GET_Spawn(ip):
    try:
        api = (f'http://{ip}/spawn')  #API接口
        response = requests.get(api, timeout=MainTimeout) #请求
        ReturnCode = response.status_code
        if ReturnCode == 200: #请求成功
            data = json.loads(response.text)
            lng = data["longitude"]
            lat = data["latitude"]
            return lng,lat
        else: #请求失败
            return False, False
    except:
        return False, False

# [6]【设置出生点】
def POST_Spawn(ip, lng, lat):
    # 设置请求的 URL
    api = f"http://{ip}/spawn?latitude={lat}&longitude={lng}"
    try:
        # 发送 POST 请求
        response = requests.post(api)
        code = response.status_code
        return code
    except:
        return False

# [7]【设置颜色】
def POST_Color(ip, hex_color):
    # 处理颜色
    hex_color = hex_color.replace("#","")
    # 设置请求的 URL
    api = f"http://{ip}/setColor?color=%23{hex_color}"
    try:
        # 发送 POST 请求
        response = requests.post(api)
        code = response.status_code
        return code
    except:
        return False

# [8]【设置方位角】
def POST_Azimuth(ip, azimuth):
    # 设置请求的 URL
    api = f"http://{ip}/setAzimuth?azimuth={azimuth}"
    try:
        # 发送 POST 请求
        response = requests.post(api)
        code = response.status_code
        return code
    except:
        return False

# [9]【设置WLAN】
def POST_WiFi(ip, ssid, password):
    # 设置请求的 URL
    api = f"http://{ip}/setWiFi?ssid={ssid}&password={password}"
    try:
        # 发送 POST 请求
        response = requests.post(api)
        code = response.status_code
        return code
    except:
        return False

# [10]【重启设备】
def Reboot_Device(ip):
    if Press_ESC_Key():
        # 发送负索引崩溃重启
        reboot_thread = threading.Thread(target=lambda:POST_Index(ip, -10))
        reboot_thread.daemon = True
        reboot_thread.start()
        return "ForceReboot"
    else:
        # 通过网络设置进行重启
        ssid,pwd = GET_WiFi(ip) # 获取当前密码
        state = POST_WiFi(ip,ssid,pwd)  # 发送当前密码
        return state

# [404]
def Fuck_404():
    os.popen("start https://zzydd.github.io/404/")
    return "404 Not Found. Are you an idiot?! 你是傻逼吗？！"



#---------------------------------------------------------------------------------------------------------------------------------



"""【主函数】"""
if __name__ == "__main__":

    """启动任务载荷"""
    # 获取信息
    User_Appdata_Path = os.environ['LOCALAPPDATA'] # 用户Appdata-Local位置
    User_Menu_Path = os.path.join(os.environ['APPDATA'], "Microsoft", "Windows", "Start Menu", "Programs")
    User_Desktop_Path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    # 创建进程管理器
    multiprocessing.freeze_support()  # 必须调用以支持多进程
    Progress_Manager = multiprocessing.Manager()
    GET_COLOR_List = Progress_Manager.list([0,0,0,False])

    """测试任务载荷"""

    """主任务载荷"""
    # 适配DIP
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # 创建程序数据目录
    try:
        os.makedirs(f"{User_Appdata_Path}/MineCompass")
    except FileExistsError:
        pass

    # 读取安装状态
    install_check = os.path.isfile(f"{User_Appdata_Path}/MineCompass/MineCompass.exe")
    if install_check:
        Main_Install_state = True
    else:
        Main_Install_state = False

    # 读取菜单状态
    menu_check = os.path.isfile(f"{User_Menu_Path}/Mine Compass.lnk")
    if menu_check:
        Main_StartMenu_state = True
    else:
        Main_StartMenu_state = False


    # 加载用户高德API密钥
    try:
        # 取用户密钥加密数据
        with open(f"{User_Appdata_Path}/MineCompass/Gaode-API-Key.bin","rb") as file:
            encrypt_data = file.read()
        # 解密数据
        try:
            state,decrypt_data = Decrypt_UserData(encrypt_data)
            if state:
                Gaode_api_key = decrypt_data # 加载密钥
                Private_api_key = True # 更改状态
                print("个人密钥加载成功")
            else:
                # 删除文件
                try:
                    os.remove(f"{User_Appdata_Path}/MineCompass/Gaode-API-Key.bin")
                except Exception as error:
                    Error_Window(f"密钥文件销毁失败！\n{error}","Mine Compass 个人密钥", False)
        except:
            pass
    except FileNotFoundError:
        print("未找到个人密钥")
        pass
    except Exception as error:
        Error_Window(f"个人高德API密钥加载出错！\n{error}","Mine Compass 个人密钥",True)
        print("个人密钥加载失败")

    # 加载内置高德API密钥
    if not Private_api_key:
        state,info = Load_Built_API_Key()
        if not state:
            Error_Window(f"内置高德API密钥加载出错！\n{info}","Mine Compass 内置密钥",True)
            print("内置密钥加载失败")
        else:
            print("内置密钥加载成功")
            pass
    else:
        pass
    # 启动检测线程
    Connect_Detecting_Thread = threading.Thread(target=Connect_Detecting)
    Connect_Detecting_Thread.daemon = True
    Connect_Detecting_Thread.start()

    # 启动主窗口
    ctk.set_appearance_mode("System")  # 根据系统主题设置外观模式
    ctk.set_default_color_theme("blue")  # 设置默认颜色主题
    #ctk.set_default_color_theme("green")  # 设置默认颜色主题
    app = MainWindow()  # 创建主窗口实例
    app.mainloop()  # 运行主循环

    """结束任务载荷"""
    # 停止检测线程
    Connect_Detecting_State = False
    # 恢复光标
    Reset_Cursor()
    # 释放进程管理器
    Progress_Manager.shutdown()
    print("【结束】主进程结束")

