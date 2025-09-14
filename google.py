#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版Google搜索界面
修复依赖问题，可以独立运行的版本
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import json
import platform
import subprocess
import sys
import traceback

# 尝试导入PIL，如果失败则禁用图片功能
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("警告: PIL/Pillow未安装，将禁用图片功能")

# 尝试导入新模块，如果失败则使用简化版本
try:
    from information_database import InformationDatabase
except ImportError:
    print("错误: 找不到information_database.py模块")
    print("请确保information_database.py文件在同一目录下")
    sys.exit(1)

class SimpleGoogleApp:
    """
    简化版Google搜索应用
    移除了复杂的依赖，专注于核心搜索功能
    """
    
    def __init__(self):
        """初始化应用"""
        # 设置字体
        if platform.system() == "Windows":
            self.font_family = "Microsoft YaHei"
        elif platform.system() == "Darwin":
            self.font_family = "PingFang SC"  
        else:
            self.font_family = "Arial"
        
        # 创建信息库实例
        try:
            self.info_db = InformationDatabase()
        except Exception as e:
            messagebox.showerror("数据库错误", f"初始化信息库失败: {e}")
            sys.exit(1)
        
        # 应用状态
        self.current_view = "search"
        self.search_results = []
        self.current_page_data = {}
        self.current_query = ""  # 当前搜索查询，用于高亮显示
        
        # 搜索历史
        self.search_history = []
        self.load_simple_history()
        
        # 界面组件
        self.root = None
        self.main_frame = None
        self.results_frame = None
        self.page_frame = None
        
        # 初始化UI
        self.setup_ui()
    
    def load_simple_history(self):
        """加载简单的搜索历史"""
        try:
            if os.path.exists("search_history_simple.json"):
                with open("search_history_simple.json", 'r', encoding='utf-8') as f:
                    self.search_history = json.load(f)
        except Exception as e:
            print(f"加载搜索历史失败: {e}")
            self.search_history = []
    
    def save_simple_history(self):
        """保存简单的搜索历史"""
        try:
            with open("search_history_simple.json", 'w', encoding='utf-8') as f:
                json.dump(self.search_history[-20:], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存搜索历史失败: {e}")
    
    def add_to_history(self, query):
        """添加到搜索历史"""
        if query and query.strip():
            query = query.strip()
            if query in self.search_history:
                self.search_history.remove(query)
            self.search_history.insert(0, query)
            self.save_simple_history()
    
    def setup_ui(self):
        """设置用户界面"""
        try:
            # 创建主窗口
            self.root = tk.Tk()
            self.root.title("Google搜索 - 简化版")
            self.root.geometry("1024x768")
            self.root.configure(bg="white")
            
            # 居中窗口
            self.center_window()
            
            # 创建主界面
            self.setup_main_search()
            
            # 绑定键盘事件
            self.root.bind('<Return>', lambda e: self.perform_search())
            self.root.bind('<Escape>', lambda e: self.show_main_search())
            
        except Exception as e:
            print(f"UI初始化失败: {e}")
            sys.exit(1)
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_main_search(self):
        """设置主搜索界面"""
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo区域
        logo_frame = tk.Frame(self.main_frame, bg="white")
        logo_frame.pack(pady=(80, 30))
        
        # 尝试加载logo图片，加强路径和错误处理
        logo_loaded = False
        if PIL_AVAILABLE:
            # 尝试多个可能的图片路径
            logo_paths = [
                "google_logo.png",
                os.path.join(os.getcwd(), "google_logo.png"),
                os.path.join(os.path.dirname(__file__), "google_logo.png")
            ]
            
            for logo_path in logo_paths:
                try:
                    if os.path.exists(logo_path) and os.path.isfile(logo_path):
                        img = Image.open(logo_path)
                        img = img.resize((300, 100), Image.Resampling.LANCZOS)
                        self.google_logo = ImageTk.PhotoImage(img)
                        logo_label = tk.Label(logo_frame, image=self.google_logo, bg="white")
                        logo_label.pack()
                        logo_loaded = True
                        break
                except Exception as e:
                    print(f"尝试加载logo图片失败 ({logo_path}): {e}")
                    continue
        
        if not logo_loaded:
            # 使用文字logo
            logo_label = tk.Label(logo_frame, text="Google",
                                font=(self.font_family, 36, "bold"),
                                bg="white", fg="#4285f4")
            logo_label.pack()
        
        # 副标题
        subtitle = tk.Label(logo_frame, text="信息库搜索系统",
                          font=(self.font_family, 14),
                          bg="white", fg="#666")
        subtitle.pack(pady=(10, 0))
        
        # 搜索框区域
        search_frame = tk.Frame(self.main_frame, bg="white")
        search_frame.pack(pady=(0, 20))
        
        # 搜索输入框容器
        search_container = tk.Frame(search_frame, bg="#f8f9fa", relief=tk.SOLID, bd=1)
        search_container.pack()
        
        # 搜索输入框
        self.search_entry = tk.Entry(search_container,
                                   font=(self.font_family, 16),
                                   width=50, relief=tk.FLAT, bd=10,
                                   bg="#f8f9fa")
        self.search_entry.pack(padx=15, pady=12)
        self.search_entry.focus()
        
        # 绑定事件
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # 搜索历史区域（如果有历史）
        if self.search_history:
            self.create_history_section()
        
        # 按钮区域
        buttons_frame = tk.Frame(self.main_frame, bg="white")
        buttons_frame.pack(pady=(20, 40))
        
        # 搜索按钮
        search_button = tk.Button(buttons_frame, text="搜索",
                                font=(self.font_family, 13),
                                bg="#f8f9fa", fg="#333",
                                relief=tk.FLAT, bd=1,
                                padx=20, pady=8,
                                command=self.perform_search)
        search_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 数据管理按钮
        manage_button = tk.Button(buttons_frame, text="数据管理",
                                font=(self.font_family, 13),
                                bg="#f8f9fa", fg="#333",
                                relief=tk.FLAT, bd=1,
                                padx=20, pady=8,
                                command=self.open_data_manager)
        manage_button.pack(side=tk.LEFT)
    
    def create_history_section(self):
        """创建搜索历史区域"""
        if not self.search_history:
            return
        
        history_frame = tk.Frame(self.main_frame, bg="white")
        history_frame.pack(pady=(10, 20))
        
        history_title = tk.Label(history_frame, text="搜索历史",
                               font=(self.font_family, 12, "bold"),
                               bg="white", fg="#666")
        history_title.pack()
        
        # 历史记录列表
        self.history_listbox = tk.Listbox(history_frame,
                                        font=(self.font_family, 10),
                                        height=5, width=60)
        self.history_listbox.pack(pady=(5, 0))
        
        # 更新历史记录显示
        for query in self.search_history[:10]:
            self.history_listbox.insert(tk.END, query)
        
        # 绑定双击事件
        self.history_listbox.bind('<Double-1>', self.on_history_double_click)
        
        # 保存历史列表框引用
        self.history_section = history_frame
    
    def on_history_double_click(self, event):
        """历史记录双击事件"""
        try:
            selection = self.history_listbox.curselection()
            if selection:
                query = self.history_listbox.get(selection[0])
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, query)
                self.perform_search()
        except Exception as e:
            print(f"历史记录点击处理失败: {e}")
    
    def open_data_manager(self):
        """打开数据管理界面"""
        try:
            if os.path.exists("data_manager.py"):
                subprocess.Popen([sys.executable, "data_manager.py"])
            else:
                messagebox.showerror("错误", "找不到数据管理程序！")
        except Exception as e:
            messagebox.showerror("错误", f"启动数据管理失败: {e}")
    
    def perform_search(self):
        """执行搜索"""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("搜索提示", "请输入搜索关键词")
            return
        
        try:
            # 保存当前查询用于高亮显示
            self.current_query = query
            
            # 执行搜索
            self.search_results = self.info_db.search(query)
            
            # 添加到历史
            self.add_to_history(query)
            
            # 显示结果
            self.current_view = "results"
            self.show_search_results()
            
        except Exception as e:
            messagebox.showerror("搜索错误", f"搜索失败: {e}")
    
    def create_highlight_text(self, parent, text, font=None, bg="white", fg="#333", wraplength=800, height=None):
        """创建带有关键词高亮的Text组件"""
        import re
        
        # 创建Text组件
        if height:
            text_widget = tk.Text(parent, font=font or (self.font_family, 13), 
                                 bg=bg, fg=fg, wrap=tk.WORD, height=height,
                                 relief=tk.FLAT, bd=0, state=tk.NORMAL)
        else:
            text_widget = tk.Text(parent, font=font or (self.font_family, 13), 
                                 bg=bg, fg=fg, wrap=tk.WORD,
                                 relief=tk.FLAT, bd=0, state=tk.NORMAL)
        
        # 配置高亮标签
        text_widget.tag_configure("highlight", background="#ffeb3b", foreground="#333")
        
        # 如果有搜索查询，进行高亮处理
        if self.current_query and text:
            # 分割查询词
            query_words = [word.strip() for word in self.current_query.split() if word.strip()]
            
            # 插入文本并高亮关键词
            current_pos = 0
            text_lower = text.lower()
            
            # 找到所有匹配位置
            matches = []
            for word in query_words:
                word_lower = word.lower()
                start = 0
                while True:
                    pos = text_lower.find(word_lower, start)
                    if pos == -1:
                        break
                    matches.append((pos, pos + len(word)))
                    start = pos + 1
            
            # 按位置排序并合并重叠的匹配
            matches.sort()
            merged_matches = []
            for start, end in matches:
                if merged_matches and start <= merged_matches[-1][1]:
                    # 合并重叠区间
                    merged_matches[-1] = (merged_matches[-1][0], max(merged_matches[-1][1], end))
                else:
                    merged_matches.append((start, end))
            
            # 插入文本并应用高亮
            last_end = 0
            for start, end in merged_matches:
                # 插入高亮前的普通文本
                if start > last_end:
                    text_widget.insert(tk.END, text[last_end:start])
                # 插入高亮文本
                text_widget.insert(tk.END, text[start:end], "highlight")
                last_end = end
            
            # 插入剩余的普通文本
            if last_end < len(text):
                text_widget.insert(tk.END, text[last_end:])
        else:
            # 没有搜索查询或文本为空，直接插入文本
            text_widget.insert(tk.END, text or "")
        
        # 设置为只读
        text_widget.config(state=tk.DISABLED)
        
        # 计算合适的高度
        if not height:
            text_widget.update_idletasks()
            lines = text_widget.get("1.0", tk.END).count('\n') + 1
            if wraplength and len(text or "") > 0:
                # 估算换行后的行数
                estimated_lines = max(lines, len(text or "") // (wraplength // 10))
                text_widget.config(height=min(estimated_lines, 8))
            else:
                text_widget.config(height=min(lines, 8))
        
        return text_widget
    
    def create_highlight_scrollable_text(self, parent, text, font=None, bg="white", fg="#333"):
        """创建带有滚动条和关键词高亮的Text组件"""
        import re
        from tkinter import scrolledtext
        
        # 创建ScrolledText组件
        text_widget = scrolledtext.ScrolledText(parent,
                                              font=font or (self.font_family, 12),
                                              bg=bg, fg=fg, wrap=tk.WORD,
                                              relief=tk.FLAT, bd=0, state=tk.NORMAL)
        
        # 配置高亮标签
        text_widget.tag_configure("highlight", background="#ffeb3b", foreground="#333")
        
        # 如果有搜索查询，进行高亮处理
        if self.current_query and text:
            # 分割查询词
            query_words = [word.strip() for word in self.current_query.split() if word.strip()]
            
            # 插入文本并高亮关键词
            text_lower = text.lower()
            
            # 找到所有匹配位置
            matches = []
            for word in query_words:
                word_lower = word.lower()
                start = 0
                while True:
                    pos = text_lower.find(word_lower, start)
                    if pos == -1:
                        break
                    matches.append((pos, pos + len(word)))
                    start = pos + 1
            
            # 按位置排序并合并重叠的匹配
            matches.sort()
            merged_matches = []
            for start, end in matches:
                if merged_matches and start <= merged_matches[-1][1]:
                    # 合并重叠区间
                    merged_matches[-1] = (merged_matches[-1][0], max(merged_matches[-1][1], end))
                else:
                    merged_matches.append((start, end))
            
            # 插入文本并应用高亮
            last_end = 0
            for start, end in merged_matches:
                # 插入高亮前的普通文本
                if start > last_end:
                    text_widget.insert(tk.END, text[last_end:start])
                # 插入高亮文本
                text_widget.insert(tk.END, text[start:end], "highlight")
                last_end = end
            
            # 插入剩余的普通文本
            if last_end < len(text):
                text_widget.insert(tk.END, text[last_end:])
        else:
            # 没有搜索查询或文本为空，直接插入文本
            text_widget.insert(tk.END, text or "")
        
        # 设置为只读
        text_widget.config(state=tk.DISABLED)
        
        return text_widget
    
    def show_search_results(self):
        """显示搜索结果"""
        try:
            # 隐藏主界面和内容页面
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.main_frame.pack_forget()
            if hasattr(self, 'page_frame') and self.page_frame and self.page_frame.winfo_exists():
                self.page_frame.pack_forget()
            
            # 销毁旧的结果界面
            if self.results_frame and self.results_frame.winfo_exists():
                self.results_frame.destroy()
            
            # 创建结果界面
            self.results_frame = tk.Frame(self.root, bg="white")
            self.results_frame.pack(fill=tk.BOTH, expand=True)
            
            # 创建头部
            header_frame = tk.Frame(self.results_frame, bg="white", height=80)
            header_frame.pack(fill=tk.X, padx=20, pady=10)
            header_frame.pack_propagate(False)
            
            # 返回按钮
            back_button = tk.Button(header_frame, text="← 返回搜索",
                                  font=(self.font_family, 12),
                                  bg="#4285f4", fg="white",
                                  relief=tk.FLAT, padx=15, pady=8,
                                  command=self.show_main_search)
            back_button.pack(side=tk.LEFT, pady=10)
            
            # 结果标题
            title_label = tk.Label(header_frame,
                                 text=f"搜索结果 ({len(self.search_results)} 条)",
                                 font=(self.font_family, 18, "bold"),
                                 bg="white", fg="#333")
            title_label.pack(side=tk.LEFT, padx=(20, 0), pady=10)
            
            # 内容区域
            content_frame = tk.Frame(self.results_frame, bg="white")
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
            
            if not self.search_results:
                # 无结果提示
                no_results_frame = tk.Frame(content_frame, bg="white")
                no_results_frame.pack(expand=True, fill=tk.BOTH)
                
                tk.Label(no_results_frame, text="🔍",
                        font=(self.font_family, 48),
                        bg="white", fg="#ccc").pack(pady=(100, 20))
                
                tk.Label(no_results_frame, text="未找到匹配的结果",
                        font=(self.font_family, 18, "bold"),
                        bg="white", fg="#333").pack()
                
                suggestion_text = "建议:\\n• 尝试使用不同的关键词\\n• 检查拼写是否正确\\n• 尝试更简短的搜索词"
                tk.Label(no_results_frame, text=suggestion_text,
                        font=(self.font_family, 12),
                        bg="white", fg="#666",
                        justify=tk.LEFT).pack(pady=(20, 0))
            else:
                # 显示结果列表
                self.create_results_list(content_frame)
        
        except Exception as e:
            messagebox.showerror("界面错误", f"显示搜索结果失败: {e}")
    
    def create_results_list(self, parent):
        """创建搜索结果列表"""
        # 创建滚动区域
        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg="white")
        
        scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 添加鼠标滚轮支持
        def _on_mousewheel(event):
            try:
                # Windows和Linux的滚轮事件处理
                if event.delta:
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                else:
                    # Linux系统的滚轮事件
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
            except Exception as e:
                print(f"滚轮事件处理失败: {e}")
        
        # 绑定滚轮事件的递归函数
        def bind_mousewheel(widget):
            """递归绑定滚轮事件到所有子组件"""
            try:
                widget.bind("<MouseWheel>", _on_mousewheel)
                widget.bind("<Button-4>", _on_mousewheel)  
                widget.bind("<Button-5>", _on_mousewheel)
                for child in widget.winfo_children():
                    bind_mousewheel(child)
            except Exception as e:
                print(f"绑定滚轮事件失败: {e}")
        
        # 绑定滚轮事件到所有相关组件
        bind_mousewheel(canvas)
        bind_mousewheel(scrollable_content)
        bind_mousewheel(parent)
        
        # 绑定鼠标进入和离开事件来设置焦点
        def on_enter(event):
            canvas.focus_set()
            
        canvas.bind("<Enter>", on_enter)
        scrollable_content.bind("<Enter>", on_enter)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 显示搜索结果
        for i, result in enumerate(self.search_results):
            self.create_result_item(scrollable_content, result, i)
        
        # 最后再次绑定滚轮事件到所有新创建的组件
        bind_mousewheel(scrollable_content)
            
        # 保存canvas引用用于后续操作
        self.results_canvas = canvas
    
    def create_result_item(self, parent, result, index):
        """创建单个搜索结果项"""
        try:
            # 结果项容器
            result_item = tk.Frame(parent, bg="white")
            result_item.pack(fill=tk.X, padx=20, pady=15)
            
            # 标题 - 使用高亮文本组件，但保持可点击性
            title_text = self.create_highlight_text(
                result_item, result['title'],
                font=(self.font_family, 16, "bold"),
                bg="white", fg="#1a0dab",
                height=1
            )
            title_text.pack(anchor=tk.W, fill=tk.X)
            title_text.config(cursor="hand2", state=tk.NORMAL)
            title_text.bind("<Button-1>", lambda e, r=result: self.show_content_page(r))
            # 添加下划线效果
            title_text.tag_configure("underline", underline=True)
            title_text.tag_add("underline", "1.0", "end-1c")
            title_text.config(state=tk.DISABLED)
            
            # URL
            if result.get('url'):
                url_label = tk.Label(result_item, text=result['url'],
                                   font=(self.font_family, 12),
                                   bg="white", fg="#006621",
                                   anchor="w")
                url_label.pack(anchor=tk.W, pady=(2, 0))
            
            # 内容摘要 - 使用高亮文本组件
            content_preview = (result['content'][:200] + "..."
                             if len(result['content']) > 200
                             else result['content'])
            content_text = self.create_highlight_text(
                result_item, content_preview,
                font=(self.font_family, 13),
                bg="white", fg="#545454",
                wraplength=800,
                height=3
            )
            content_text.pack(anchor=tk.W, fill=tk.X, pady=(5, 0))
            
            # 标签
            if result.get('tags'):
                tags_text = "标签: " + ", ".join(result['tags'][:5])
                tags_label = tk.Label(result_item, text=tags_text,
                                     font=(self.font_family, 11),
                                     bg="white", fg="#808080",
                                     anchor="w")
                tags_label.pack(anchor=tk.W, pady=(5, 0))
            
            # 分隔线
            separator = tk.Frame(parent, height=1, bg="#e8e8e8")
            separator.pack(fill=tk.X, padx=20, pady=(10, 0))
            
        except Exception as e:
            print(f"创建搜索结果项失败: {e}")
    
    def show_content_page(self, result_data):
        """显示内容详情页面"""
        try:
            self.current_page_data = result_data
            self.current_view = "page"
            
            # 隐藏结果界面（安全检查）
            if hasattr(self, 'results_frame') and self.results_frame and self.results_frame.winfo_exists():
                self.results_frame.pack_forget()
            
            # 销毁旧的内容页面
            if self.page_frame:
                self.page_frame.destroy()
            
            # 创建内容页面
            self.page_frame = tk.Frame(self.root, bg="white")
            self.page_frame.pack(fill=tk.BOTH, expand=True)
            
            # 创建头部
            header_frame = tk.Frame(self.page_frame, bg="white", height=60)
            header_frame.pack(fill=tk.X, padx=20, pady=10)
            header_frame.pack_propagate(False)
            
            # 返回按钮
            back_button = tk.Button(header_frame, text="← 返回结果",
                                  font=(self.font_family, 12),
                                  bg="#4285f4", fg="white",
                                  relief=tk.FLAT, padx=15, pady=8,
                                  command=self.show_search_results)
            back_button.pack(side=tk.LEFT, pady=10)
            
            # 页面标题
            title_label = tk.Label(header_frame,
                                 text=result_data.get('title', '无标题'),
                                 font=(self.font_family, 18, "bold"),
                                 bg="white", fg="#333")
            title_label.pack(side=tk.LEFT, padx=(20, 0), pady=10)
            
            # 内容区域
            content_frame = tk.Frame(self.page_frame, bg="white")
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            # 使用自定义的高亮文本区域
            content = self.format_content_for_display(result_data)
            text_area = self.create_highlight_scrollable_text(
                content_frame, content,
                font=(self.font_family, 12),
                bg="white", fg="#333"
            )
            text_area.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("页面错误", f"显示内容页面失败: {e}")
    
    def format_content_for_display(self, result):
        """格式化内容用于显示"""
        content_lines = []
        
        # 标题
        content_lines.append(f"标题: {result.get('title', '无标题')}")
        content_lines.append("=" * 50)
        content_lines.append("")
        
        # URL
        if result.get('url'):
            content_lines.append(f"链接: {result['url']}")
            content_lines.append("")
        
        # 标签
        if result.get('tags'):
            content_lines.append(f"标签: {', '.join(result['tags'])}")
            content_lines.append("")
        
        # 时间信息
        if result.get('created_at'):
            content_lines.append(f"创建时间: {result['created_at']}")
        if result.get('updated_at'):
            content_lines.append(f"更新时间: {result['updated_at']}")
        if result.get('created_at') or result.get('updated_at'):
            content_lines.append("")
        
        # 内容
        content_lines.append("内容:")
        content_lines.append("-" * 50)
        content_lines.append(result.get('content', '无内容'))
        
        return "\n".join(content_lines)
    
    def show_main_search(self):
        """显示主搜索界面"""
        try:
            # 隐藏其他界面（安全检查）
            if hasattr(self, 'results_frame') and self.results_frame and self.results_frame.winfo_exists():
                self.results_frame.pack_forget()
            if hasattr(self, 'page_frame') and self.page_frame and self.page_frame.winfo_exists():
                self.page_frame.pack_forget()
            
            # 确保主界面存在且可见
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.main_frame.pack(fill=tk.BOTH, expand=True)
            else:
                # 如果主界面被意外销毁，重新创建
                self.setup_main_search()
            
            # 重置状态
            self.current_view = "search"
            
            # 聚焦搜索框（安全检查）
            if hasattr(self, 'search_entry') and self.search_entry.winfo_exists():
                self.search_entry.focus()
            
            # 刷新搜索历史显示
            self.refresh_history_display()
            
        except Exception as e:
            messagebox.showerror("界面错误", f"显示主搜索界面失败: {e}")
    
    def refresh_history_display(self):
        """刷新搜索历史显示"""
        try:
            # 如果历史区域存在，更新显示
            if hasattr(self, 'history_listbox') and self.history_listbox.winfo_exists():
                self.history_listbox.delete(0, tk.END)
                for query in self.search_history[:10]:
                    self.history_listbox.insert(tk.END, query)
        except Exception as e:
            print(f"刷新历史显示失败: {e}")
    
    def run(self):
        """启动应用程序"""
        try:
            if self.root:
                self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n用户中断程序")
        except Exception as e:
            print(f"应用程序运行失败: {e}")
        finally:
            # 保存搜索历史
            self.save_simple_history()

def main():
    """主函数"""
    try:
        app = SimpleGoogleApp()
        app.run()
    except FileNotFoundError as e:
        error_msg = f"文件路径错误: {e}"
        print(error_msg)
        print("可能的原因：")
        print("1. 文件路径包含特殊字符或中文")
        print("2. 文件被移动或删除")
        print("3. 权限不足")
        try:
            messagebox.showerror("文件路径错误", error_msg)
        except:
            pass
    except Exception as e:
        error_msg = f"程序启动失败: {e}"
        print(error_msg)
        print("详细错误信息:")
        print(traceback.format_exc())
        try:
            messagebox.showerror("启动错误", error_msg)
        except:
            pass

if __name__ == "__main__":
    main()