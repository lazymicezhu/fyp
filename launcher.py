#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息库系统启动脚本
提供菜单选择不同的功能模块
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import platform
import subprocess
import sys
import os

# 导入新增的配置和异常处理模块
from config import config
from exceptions import safe_execute, UIError, error_handler

# 设置 CustomTkinter 外观
ctk.set_appearance_mode("auto")  # "auto", "dark", "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

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
        使用配置模块中的字体设置，避免重复代码
        """
        font_config = config.get_font_config("default")
        self.font_family = font_config.family
    
    def setup_main_window(self):
        """
        设置主窗口
        创建CustomTkinter根窗口，设置标题、大小等基本属性
        """
        # 创建CustomTkinter根窗口实例
        self.root = ctk.CTk()
        # 设置窗口标题，包含项目名称
        self.root.title("信息库系统启动器 - Lazymice Project")
        # 设置窗口初始大小为550x650像素
        self.root.geometry("550x650")
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
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 创建主标题标签
        title_label = ctk.CTkLabel(main_frame, text="信息库系统", 
                                  font=ctk.CTkFont(family=self.font_family, size=28, weight="bold"))
        title_label.pack(pady=(30, 10))
        
        # 创建副标题标签
        subtitle_label = ctk.CTkLabel(main_frame, text="Lazymice Project - 本地信息库搜索系统", 
                                     font=ctk.CTkFont(family=self.font_family, size=14))
        subtitle_label.pack(pady=(0, 40))
        
        # 创建按钮框架
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill=tk.X, padx=30)
        
        # 创建搜索界面按钮
        search_button = ctk.CTkButton(button_frame, text="仿Google检索界面", 
                                     font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
                                     height=50, corner_radius=12,
                                     command=self.open_search_interface)
        search_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建数据管理按钮
        manage_button = ctk.CTkButton(button_frame, text="打开数据管理", 
                                     font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
                                     height=50, corner_radius=12,
                                     fg_color="#2fa572", hover_color="#106A43",
                                     command=self.open_data_manager)
        manage_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建帮助按钮
        help_button = ctk.CTkButton(button_frame, text="使用帮助", 
                                   font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
                                   height=50, corner_radius=12,
                                   fg_color="#ff9500", hover_color="#cc7700",
                                   command=self.show_help)
        help_button.pack(fill=tk.X, pady=(0, 15))
        
        # 创建外观切换按钮
        appearance_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        appearance_frame.pack(fill=tk.X, pady=(10, 15))
        
        appearance_label = ctk.CTkLabel(appearance_frame, text="外观模式:", 
                                       font=ctk.CTkFont(family=self.font_family, size=14))
        appearance_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.appearance_mode = ctk.CTkOptionMenu(appearance_frame,
                                               values=["auto", "light", "dark"],
                                               command=self.change_appearance_mode,
                                               font=ctk.CTkFont(family=self.font_family, size=12),
                                               width=120, height=32)
        self.appearance_mode.set("auto")
        self.appearance_mode.pack(side=tk.LEFT)
        
        # 创建退出按钮
        exit_button = ctk.CTkButton(button_frame, text="❌ 退出", 
                                   font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
                                   height=50, corner_radius=12,
                                   fg_color="#dc2626", hover_color="#991b1b",
                                   command=self.root.quit)
        exit_button.pack(fill=tk.X)
        
        # 创建状态信息区域
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.pack(fill=tk.X, pady=(30, 20), padx=30)
        
        # 创建状态标签
        self.status_label = ctk.CTkLabel(status_frame, text="", 
                                        font=ctk.CTkFont(family=self.font_family, size=12))
        self.status_label.pack()
        
        # 更新状态信息
        self.update_status()
    
    def change_appearance_mode(self, new_appearance_mode):
        """改变外观模式"""
        ctk.set_appearance_mode(new_appearance_mode)
    
    @safe_execute(UIError, show_user_error=True)
    def open_search_interface(self):
        """
        打开搜索界面
        启动Google搜索界面程序，优先使用重构版本
        使用安全执行装饰器处理异常
        """
        try:
            # 优先使用改进版本的google.py（已修复路径问题和添加滚轮滑动）
            if os.path.exists("google.py"):
                subprocess.Popen([sys.executable, "google.py"])
                self.status_label.configure(text="✅ 搜索界面已启动 (改进版本)")
            elif os.path.exists("google_simple.py"):
                subprocess.Popen([sys.executable, "google_simple.py"])
                self.status_label.configure(text="✅ 搜索界面已启动 (简化版本)")
            elif os.path.exists("google_refactored.py"):
                subprocess.Popen([sys.executable, "google_refactored.py"])
                self.status_label.configure(text="✅ 搜索界面已启动 (重构版本)")
            else:
                raise UIError("未找到搜索界面文件", component="launcher", action="open_search")
        except subprocess.SubprocessError as e:
            raise UIError(f"启动搜索界面进程失败: {str(e)}", component="launcher", action="subprocess")
        except Exception as e:
            raise UIError(f"启动搜索界面失败: {str(e)}", component="launcher", action="open_search")
    
    @safe_execute(UIError, show_user_error=True)
    def open_data_manager(self):
        """
        打开数据管理界面
        启动数据管理程序
        使用安全执行装饰器处理异常
        """
        try:
            if os.path.exists("data_manager.py"):
                subprocess.Popen([sys.executable, "data_manager.py"])
                self.status_label.configure(text="✅ 数据管理界面已启动")
            else:
                raise UIError("未找到数据管理文件", component="launcher", action="open_data_manager")
        except subprocess.SubprocessError as e:
            raise UIError(f"启动数据管理进程失败: {str(e)}", component="launcher", action="subprocess")
        except Exception as e:
            raise UIError(f"启动数据管理界面失败: {str(e)}", component="launcher", action="open_data_manager")
    
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
        
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("650x550")
        
        # 居中显示帮助窗口
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (help_window.winfo_screenheight() // 2) - (550 // 2)
        help_window.geometry(f"650x550+{x}+{y}")
        
        # 创建主框架
        main_frame = ctk.CTkFrame(help_window, corner_radius=15)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 添加标题
        title_label = ctk.CTkLabel(main_frame, text="📖 使用帮助", 
                                  font=ctk.CTkFont(family=self.font_family, size=24, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # 帮助内容
        help_text_widget = ctk.CTkTextbox(main_frame, 
                                         font=ctk.CTkFont(family=self.font_family, size=13),
                                         wrap="word", corner_radius=10)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        help_text_widget.insert("0.0", help_text)
        help_text_widget.configure(state="disabled")
    
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
        self.status_label.configure(text=status_text)
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LauncherGUI()
    app.run()
