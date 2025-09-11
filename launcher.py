#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息库系统启动脚本
提供菜单选择不同的功能模块
"""

import tkinter as tk
from tkinter import messagebox
import platform
import subprocess
import sys
import os

class LauncherGUI:
    """
    启动器GUI类
    提供统一的入口界面，让用户选择不同的功能模块
    包括搜索界面、数据管理界面等
    """
    
    def __init__(self):
        """
        初始化启动器GUI
        设置字体，创建主窗口和界面组件
        """
        # 设置系统字体
        self.setup_fonts()
        # 创建主窗口
        self.setup_main_window()
        # 创建界面组件
        self.setup_widgets()
    
    def setup_fonts(self):
        """
        设置系统字体
        根据操作系统自动选择合适的中文字体
        Windows使用微软雅黑，Mac使用苹方
        """
        if platform.system() == "Windows":
            # Windows系统使用微软雅黑字体
            self.font_family = "Microsoft YaHei"
        elif platform.system() == "Darwin":
            # Mac系统使用苹方字体
            self.font_family = "PingFang SC"
        else:
            self.font_family = "Arial"
    
    def setup_main_window(self):
        """
        设置主窗口
        创建Tkinter根窗口，设置标题、大小、背景色等基本属性
        """
        # 创建Tkinter根窗口实例
        self.root = tk.Tk()
        # 设置窗口标题，包含项目名称
        self.root.title("信息库系统启动器 - Lazymice Project")
        # 设置窗口初始大小为600x500像素
        self.root.geometry("600x500")
        # 设置窗口背景色为浅灰色
        self.root.configure(bg="#f5f5f5")
        # 允许窗口调整大小
        self.root.resizable(True, True)
        # 设置最小窗口大小为500x400像素，防止界面过小
        self.root.minsize(500, 400)
        
        # 将窗口居中显示在屏幕上
        self.center_window()
    
    def center_window(self):
        """
        窗口居中显示
        计算屏幕尺寸，将窗口定位在屏幕中央
        """
        # 更新窗口尺寸信息
        self.root.update_idletasks()
        # 获取窗口的宽度和高度
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        # 计算窗口在屏幕中的居中位置
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        # 设置窗口位置
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """
        设置界面组件
        创建主界面的所有组件，包括标题、按钮等
        """
        # 创建主框架
        # 背景色为浅灰色，填充整个窗口并扩展
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        # 使用pack布局，填充整个窗口，左右边距40像素，上下边距40像素
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # 创建主标题标签
        # 显示"信息库系统"，使用24号加粗字体，深灰色文字
        title_label = tk.Label(main_frame, text="信息库系统", 
                              font=(self.font_family, 24, "bold"), 
                              bg="#f5f5f5", fg="#333")
        # 使用pack布局，上下边距(0, 30)像素
        title_label.pack(pady=(0, 30))
        
        # 创建副标题标签
        # 显示项目描述，使用12号字体，深灰色文字
        subtitle_label = tk.Label(main_frame, text="Lazymice Project - 本地信息库搜索系统", 
                                 font=(self.font_family, 12), 
                                 bg="#f5f5f5", fg="#666")
        # 使用pack布局，上下边距(0, 40)像素
        subtitle_label.pack(pady=(0, 40))
        
        # 创建按钮框架
        # 用于放置功能按钮的框架
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        # 水平填充
        button_frame.pack(fill=tk.X)
        
        # 创建搜索界面按钮
        # 显示"🔍 打开搜索界面"，使用蓝色背景和白色文字
        search_button = tk.Button(button_frame, text="🔍 打开搜索界面", 
                                  font=(self.font_family, 14), bg="#4285f4", fg="white",
                                  command=self.open_search_interface, 
                                  relief=tk.FLAT, bd=0, height=2)
        # 水平填充，上下边距(0, 15)像素
        search_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建数据管理按钮
        # 显示"📝 打开数据管理"，使用绿色背景和白色文字
        manage_button = tk.Button(button_frame, text="📝 打开数据管理", 
                                 font=(self.font_family, 14), bg="#34a853", fg="white",
                                 command=self.open_data_manager, 
                                 relief=tk.FLAT, bd=0, height=2)
        # 水平填充，上下边距(0, 15)像素
        manage_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建帮助按钮
        # 显示"❓ 使用帮助"，使用黄色背景和黑色文字
        help_button = tk.Button(button_frame, text="❓ 使用帮助", 
                               font=(self.font_family, 14), bg="#fbbc04", fg="black",
                               command=self.show_help, 
                               relief=tk.FLAT, bd=0, height=2)
        # 水平填充，上下边距(0, 15)像素
        help_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建退出按钮
        # 显示"❌ 退出"，使用红色背景和白色文字
        exit_button = tk.Button(button_frame, text="❌ 退出", 
                              font=(self.font_family, 14), bg="#ea4335", fg="white",
                              command=self.root.quit, 
                              relief=tk.FLAT, bd=0, height=2)
        # 水平填充
        exit_button.pack(fill=tk.X)
        
        # 创建状态信息区域
        # 用于显示系统状态信息的框架
        status_frame = tk.Frame(main_frame, bg="#f5f5f5")
        # 水平填充，上下边距(30, 0)像素
        status_frame.pack(fill=tk.X, pady=(30, 0))
        
        # 创建状态标签
        # 显示系统状态信息，使用10号字体，深灰色文字
        self.status_label = tk.Label(status_frame, text="", 
                                    font=(self.font_family, 10), 
                                    bg="#f5f5f5", fg="#888")
        # 使用pack布局
        self.status_label.pack()
        
        # 更新状态信息
        self.update_status()
    
    def open_search_interface(self):
        """
        打开搜索界面
        启动Google搜索界面程序
        """
        try:
            # 检查google.py文件是否存在
            if os.path.exists("google.py"):
                # 使用subprocess启动新的Python进程运行google.py
                subprocess.Popen([sys.executable, "google.py"])
                # 更新状态标签显示成功信息
                self.status_label.config(text="✅ 搜索界面已启动")
            else:
                # 如果文件不存在，显示错误对话框
                messagebox.showerror("错误", "找不到 google.py 文件！")
        except Exception as e:
            # 如果启动过程中出现异常，显示错误对话框
            messagebox.showerror("错误", f"启动搜索界面失败: {e}")
    
    def open_data_manager(self):
        """
        打开数据管理界面
        启动数据管理程序
        """
        try:
            # 检查data_manager.py文件是否存在
            if os.path.exists("data_manager.py"):
                # 使用subprocess启动新的Python进程运行data_manager.py
                subprocess.Popen([sys.executable, "data_manager.py"])
                # 更新状态标签显示成功信息
                self.status_label.config(text="✅ 数据管理界面已启动")
            else:
                # 如果文件不存在，显示错误对话框
                messagebox.showerror("错误", "找不到 data_manager.py 文件！")
        except Exception as e:
            # 如果启动过程中出现异常，显示错误对话框
            messagebox.showerror("错误", f"启动数据管理界面失败: {e}")
    
    def show_help(self):
        """
        显示帮助信息
        弹出帮助对话框，介绍系统功能和使用方法
        """
        # 定义帮助文本内容
        help_text = """
信息库系统使用说明

🔍 搜索界面 (google.py)
- 模拟Google搜索页面
- 支持关键词搜索本地信息库
- 点击搜索结果查看详细内容

📝 数据管理 (data_manager.py)
- 添加、编辑、删除信息条目
- 支持标签分类管理
- 导入/导出JSON格式数据
- 实时搜索和过滤功能

💡 使用技巧
1. 先在数据管理中添加信息内容
2. 然后在搜索界面中搜索和查看
3. 支持中文搜索和标签分类
4. 数据自动保存到JSON文件

📁 文件说明
- information_database.py: 信息库核心模块
- google.py: 搜索界面
- data_manager.py: 数据管理界面
- information_database.json: 数据存储文件
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x500")
        help_window.configure(bg="#f5f5f5")
        
        # 居中显示帮助窗口
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f"600x500+{x}+{y}")
        
        # 帮助内容
        help_text_widget = tk.Text(help_window, font=(self.font_family, 11),
                                   wrap=tk.WORD, bg="white", fg="#333",
                                   relief=tk.FLAT, bd=0)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def update_status(self):
        """更新状态信息"""
        files_status = []
        
        if os.path.exists("google.py"):
            files_status.append("搜索界面 ✓")
        else:
            files_status.append("搜索界面 ✗")
        
        if os.path.exists("data_manager.py"):
            files_status.append("数据管理 ✓")
        else:
            files_status.append("数据管理 ✗")
        
        if os.path.exists("information_database.py"):
            files_status.append("信息库模块 ✓")
        else:
            files_status.append("信息库模块 ✗")
        
        status_text = " | ".join(files_status)
        self.status_label.config(text=status_text)
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LauncherGUI()
    app.run()
