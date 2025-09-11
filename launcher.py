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
    """启动器GUI"""
    
    def __init__(self):
        self.setup_fonts()
        self.setup_main_window()
        self.setup_widgets()
    
    def setup_fonts(self):
        """设置字体"""
        if platform.system() == "Windows":
            self.font_family = "Microsoft YaHei"
        elif platform.system() == "Darwin":
            self.font_family = "PingFang SC"
        else:
            self.font_family = "Arial"
    
    def setup_main_window(self):
        """设置主窗口"""
        self.root = tk.Tk()
        self.root.title("信息库系统启动器 - Lazymice Project")
        self.root.geometry("500x400")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)
        
        # 居中显示窗口
        self.center_window()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """设置界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # 标题
        title_label = tk.Label(main_frame, text="信息库系统", 
                              font=(self.font_family, 24, "bold"), 
                              bg="#f5f5f5", fg="#333")
        title_label.pack(pady=(0, 30))
        
        # 副标题
        subtitle_label = tk.Label(main_frame, text="Lazymice Project - 本地信息库搜索系统", 
                                 font=(self.font_family, 12), 
                                 bg="#f5f5f5", fg="#666")
        subtitle_label.pack(pady=(0, 40))
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X)
        
        # 搜索界面按钮
        search_button = tk.Button(button_frame, text="🔍 打开搜索界面", 
                                  font=(self.font_family, 14), bg="#4285f4", fg="white",
                                  command=self.open_search_interface, 
                                  relief=tk.FLAT, bd=0, height=2)
        search_button.pack(fill=tk.X, pady=(0, 15))
        
        # 数据管理按钮
        manage_button = tk.Button(button_frame, text="📝 打开数据管理", 
                                 font=(self.font_family, 14), bg="#34a853", fg="white",
                                 command=self.open_data_manager, 
                                 relief=tk.FLAT, bd=0, height=2)
        manage_button.pack(fill=tk.X, pady=(0, 15))
        
        # 帮助按钮
        help_button = tk.Button(button_frame, text="❓ 使用帮助", 
                               font=(self.font_family, 14), bg="#fbbc04", fg="black",
                               command=self.show_help, 
                               relief=tk.FLAT, bd=0, height=2)
        help_button.pack(fill=tk.X, pady=(0, 15))
        
        # 退出按钮
        exit_button = tk.Button(button_frame, text="❌ 退出", 
                              font=(self.font_family, 14), bg="#ea4335", fg="white",
                              command=self.root.quit, 
                              relief=tk.FLAT, bd=0, height=2)
        exit_button.pack(fill=tk.X)
        
        # 状态信息
        status_frame = tk.Frame(main_frame, bg="#f5f5f5")
        status_frame.pack(fill=tk.X, pady=(30, 0))
        
        self.status_label = tk.Label(status_frame, text="", 
                                    font=(self.font_family, 10), 
                                    bg="#f5f5f5", fg="#888")
        self.status_label.pack()
        
        self.update_status()
    
    def open_search_interface(self):
        """打开搜索界面"""
        try:
            if os.path.exists("google.py"):
                subprocess.Popen([sys.executable, "google.py"])
                self.status_label.config(text="✅ 搜索界面已启动")
            else:
                messagebox.showerror("错误", "找不到 google.py 文件！")
        except Exception as e:
            messagebox.showerror("错误", f"启动搜索界面失败: {e}")
    
    def open_data_manager(self):
        """打开数据管理界面"""
        try:
            if os.path.exists("data_manager.py"):
                subprocess.Popen([sys.executable, "data_manager.py"])
                self.status_label.config(text="✅ 数据管理界面已启动")
            else:
                messagebox.showerror("错误", "找不到 data_manager.py 文件！")
        except Exception as e:
            messagebox.showerror("错误", f"启动数据管理界面失败: {e}")
    
    def show_help(self):
        """显示帮助信息"""
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
