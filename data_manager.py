#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息库数据输入管理界面
提供便捷的GUI界面来管理信息库数据
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import platform
from information_database import InformationDatabase

class DataInputGUI:
    """
    数据输入GUI界面类
    提供完整的图形用户界面来管理信息库数据
    包括添加、编辑、删除、导入导出等功能
    """
    
    def __init__(self):
        """
        初始化数据输入GUI界面
        创建信息库实例，设置字体，创建主窗口和组件
        """
        # 创建信息库实例，用于数据操作
        self.db = InformationDatabase()
        # 设置系统字体
        self.setup_fonts()
        # 创建主窗口
        self.setup_main_window()
        # 创建界面组件
        self.setup_widgets()
        # 刷新数据列表显示
        self.refresh_entry_list()
    
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
        self.root.title("信息库数据管理 - Lazymice Project")
        # 设置窗口初始大小为1200x800像素
        self.root.geometry("1200x800")
        # 设置窗口背景色为浅灰色
        self.root.configure(bg="#f5f5f5")
        # 设置最小窗口大小为1000x600像素，防止界面过小
        self.root.minsize(1000, 600)
        
        # 尝试设置窗口图标
        # 如果图标文件不存在，则忽略错误继续执行
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_widgets(self):
        """
        设置界面组件
        创建主界面的所有组件，包括标题、左右分栏、表单和列表
        """
        # 创建主框架
        # 背景色为浅灰色，填充整个窗口并扩展
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        # 使用pack布局，填充整个窗口，左右边距20像素，上下边距20像素
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建标题标签
        # 显示"信息库数据管理系统"，使用18号加粗字体，深灰色文字
        title_label = tk.Label(main_frame, text="信息库数据管理系统", 
                              font=(self.font_family, 18, "bold"), 
                              bg="#f5f5f5", fg="#333")
        # 使用pack布局，上下边距(0, 20)像素
        title_label.pack(pady=(0, 20))
        
        # 创建左右分栏布局
        # 左侧框架：用于数据输入表单
        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        # 左对齐，填充垂直方向并扩展，右边距10像素
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧框架：用于数据列表显示
        right_frame = tk.Frame(main_frame, bg="#f5f5f5")
        # 右对齐，填充垂直方向，左边距10像素
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 左侧：数据输入表单
        self.setup_input_form(left_frame)
        
        # 右侧：数据列表和管理
        self.setup_data_list(right_frame)
    
    def setup_input_form(self, parent):
        """
        设置数据输入表单
        创建包含标题、URL、内容类型、元数据、内容等字段的输入表单
        """
        # 创建表单框架
        # 使用LabelFrame创建带标题的框架，标题为"添加/编辑信息"
        form_frame = tk.LabelFrame(parent, text="添加/编辑信息", 
                                  font=(self.font_family, 12, "bold"),
                                  bg="#f5f5f5", fg="#333")
        # 填充父容器并扩展
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题输入区域
        # 标题标签，使用11号字体，左对齐
        tk.Label(form_frame, text="标题:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(10, 5))
        # 标题输入框，使用11号字体，宽度50字符
        self.title_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        self.title_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建URL输入区域
        # URL标签，使用11号字体，左对齐
        tk.Label(form_frame, text="URL:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        # URL输入框，使用11号字体，宽度50字符
        self.url_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        self.url_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建内容类型选择区域
        # 内容类型标签，使用11号字体，左对齐
        tk.Label(form_frame, text="内容类型:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        
        # 创建类型选择框架
        type_frame = tk.Frame(form_frame, bg="#f5f5f5")
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        type_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建内容类型变量，默认值为"article"
        self.content_type_var = tk.StringVar(value="article")
        # 定义所有支持的内容类型
        content_types = [
            ("文章", "article"),    # 文章类型
            ("链接", "link"),       # 链接类型
            ("图片", "image"),      # 图片类型
            ("视频", "video"),      # 视频类型
            ("代码", "code"),       # 代码类型
            ("新闻", "news"),       # 新闻类型
            ("教程", "tutorial"),   # 教程类型
            ("工具", "tool")        # 工具类型
        ]
        
        # 创建单选按钮组
        # 遍历内容类型列表，为每种类型创建单选按钮
        for i, (text, value) in enumerate(content_types):
            # 创建单选按钮，显示中文名称，绑定到content_type_var变量
            rb = tk.Radiobutton(type_frame, text=text, variable=self.content_type_var, 
                               value=value, font=(self.font_family, 10), bg="#f5f5f5",
                               command=self.on_content_type_change)
            # 使用grid布局，每行4个按钮，左对齐，右边距10像素，上下边距2像素
            rb.grid(row=i//4, column=i%4, sticky="w", padx=(0, 10), pady=2)
        
        # 创建标签输入区域
        # 标签说明文字，使用11号字体，左对齐
        tk.Label(form_frame, text="标签 (用逗号分隔):", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(10, 5))
        # 标签输入框，使用11号字体，宽度50字符
        self.tags_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        self.tags_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建元数据输入区域
        # 使用LabelFrame创建带标题的框架，标题为"元数据 (可选)"
        self.metadata_frame = tk.LabelFrame(form_frame, text="元数据 (可选)", 
                                           font=(self.font_family, 10, "bold"),
                                           bg="#f5f5f5", fg="#333")
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        self.metadata_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建元数据输入框
        # 使用Text组件，支持多行输入，自动换行
        self.metadata_text = tk.Text(self.metadata_frame, font=(self.font_family, 10),
                                    height=3, wrap=tk.WORD)
        # 水平填充，左右边距10像素，上下边距10像素
        self.metadata_text.pack(fill=tk.X, padx=10, pady=10)
        
        # 创建内容输入区域
        # 内容标签，使用11号字体，左对齐
        tk.Label(form_frame, text="内容:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        # 创建带滚动条的文本输入框
        # 使用ScrolledText组件，支持多行输入和滚动
        self.content_text = scrolledtext.ScrolledText(form_frame, 
                                                    font=(self.font_family, 11),
                                                    height=12, wrap=tk.WORD)
        # 填充整个区域并扩展，左右边距10像素，上下边距(0, 10)像素
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 创建按钮框架 - 竖向排列
        # 用于放置操作按钮的框架
        button_frame = tk.Frame(form_frame, bg="#f5f5f5")
        # 水平填充，左右边距10像素，上下边距(0, 10)像素
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 创建按钮容器 - 每行一个按钮
        # 用于组织按钮布局的容器框架
        buttons_container = tk.Frame(button_frame, bg="#f5f5f5")
        # 左对齐放置
        buttons_container.pack(anchor="w")
        
        # 创建添加按钮 - 第一行
        # 显示"➕ 添加"，使用蓝色背景和白色文字
        add_button = tk.Button(buttons_container, text="➕ 添加", 
                              font=(self.font_family, 11), bg="#4285f4", fg="white",
                              command=self.add_entry, width=15)
        # 水平填充，上下边距(0, 8)像素
        add_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建更新按钮 - 第二行
        # 显示"✏️ 更新"，使用绿色背景和白色文字
        update_button = tk.Button(buttons_container, text="✏️ 更新", 
                                 font=(self.font_family, 11), bg="#34a853", fg="white",
                                 command=self.update_entry, width=15)
        # 水平填充，上下边距(0, 8)像素
        update_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建清空按钮 - 第三行
        # 显示"🗑️ 清空"，使用红色背景和白色文字
        clear_button = tk.Button(buttons_container, text="🗑️ 清空", 
                                font=(self.font_family, 11), bg="#ea4335", fg="white",
                                command=self.clear_form, width=15)
        # 水平填充，上下边距(0, 8)像素
        clear_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建保存按钮 - 第四行
        # 显示"💾 保存"，使用黄色背景和黑色文字
        save_button = tk.Button(buttons_container, text="💾 保存", 
                               font=(self.font_family, 11), bg="#fbbc04", fg="black",
                               command=self.save_database, width=15)
        # 水平填充
        save_button.pack(fill=tk.X)
    
    def setup_data_list(self, parent):
        """设置数据列表"""
        # 列表框架
        list_frame = tk.LabelFrame(parent, text="数据列表", 
                                 font=(self.font_family, 12, "bold"),
                                 bg="#f5f5f5", fg="#333")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 搜索框
        search_frame = tk.Frame(list_frame, bg="#f5f5f5")
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="搜索:", font=(self.font_family, 10), 
                bg="#f5f5f5").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=(self.font_family, 10), width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.search_entry.bind("<KeyRelease>", self.filter_entries)
        
        search_button = tk.Button(search_frame, text="搜索", 
                                font=(self.font_family, 10), bg="#4285f4", fg="white",
                                command=self.filter_entries)
        search_button.pack(side=tk.LEFT)
        
        # 数据列表
        self.setup_treeview(list_frame)
        
        # 管理按钮区域 - 竖向排列
        manage_frame = tk.Frame(list_frame, bg="#f5f5f5")
        manage_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 按钮容器 - 每行一个按钮
        buttons_container = tk.Frame(manage_frame, bg="#f5f5f5")
        buttons_container.pack(anchor="w")  # 左对齐
        
        # 创建导入按钮 - 第一行
        import_button = tk.Button(buttons_container, text="📥 导入", 
                                 font=(self.font_family, 10), bg="#34a853", fg="white",
                                 command=self.import_data, width=15)
        import_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建导出按钮 - 第二行
        export_button = tk.Button(buttons_container, text="📤 导出", 
                                 font=(self.font_family, 10), bg="#fbbc04", fg="black",
                                 command=self.export_data, width=15)
        export_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建刷新按钮 - 第三行
        refresh_button = tk.Button(buttons_container, text="🔄 刷新", 
                                  font=(self.font_family, 10), bg="#4285f4", fg="white",
                                  command=self.refresh_entry_list, width=15)
        refresh_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建删除按钮 - 第四行
        delete_button = tk.Button(buttons_container, text="🗑️ 删除", 
                                 font=(self.font_family, 10), bg="#ea4335", fg="white",
                                 command=self.delete_entry, width=15)
        delete_button.pack(fill=tk.X, pady=(0, 8))
        
        # 创建批量删除按钮 - 第五行
        batch_delete_button = tk.Button(buttons_container, text="🗑️ 批量删除", 
                                      font=(self.font_family, 10), bg="#d73527", fg="white",
                                      command=self.batch_delete_entries, width=15)
        batch_delete_button.pack(fill=tk.X)
        
        # 统计信息区域
        stats_frame = tk.Frame(list_frame, bg="#f5f5f5")
        stats_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # 统计信息标题
        stats_title = tk.Label(stats_frame, text="📊 数据统计", 
                              font=(self.font_family, 11, "bold"), 
                              bg="#f5f5f5", fg="#333")
        stats_title.pack(anchor="w", pady=(0, 5))
        
        # 统计信息内容
        self.stats_label = tk.Label(stats_frame, text="", 
                                   font=(self.font_family, 10), 
                                   bg="#f5f5f5", fg="#666",
                                   justify="left", wraplength=400)
        self.stats_label.pack(anchor="w", pady=(0, 10))
        self.update_stats()
    
    def setup_treeview(self, parent):
        """设置树形视图"""
        # 创建Treeview
        columns = ("ID", "类型", "标题", "URL", "标签", "创建时间")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        self.tree.heading("ID", text="ID")
        self.tree.heading("类型", text="类型")
        self.tree.heading("标题", text="标题")
        self.tree.heading("URL", text="URL")
        self.tree.heading("标签", text="标签")
        self.tree.heading("创建时间", text="创建时间")
        
        self.tree.column("ID", width=50)
        self.tree.column("类型", width=80)
        self.tree.column("标题", width=250)
        self.tree.column("URL", width=200)
        self.tree.column("标签", width=150)
        self.tree.column("创建时间", width=120)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=(0, 10))
    
    def on_content_type_change(self):
        """内容类型变化时的处理"""
        content_type = self.content_type_var.get()
        
        # 更新元数据提示
        type_hints = {
            "article": "文章内容，支持长文本",
            "link": "外部链接，如: https://example.com",
            "image": "图片信息，如: 图片描述、尺寸、格式等",
            "video": "视频信息，如: 时长、分辨率、平台等",
            "code": "代码信息，如: 编程语言、框架、版本等",
            "news": "新闻信息，如: 来源、时间、摘要等",
            "tutorial": "教程信息，如: 难度、时长、步骤数等",
            "tool": "工具信息，如: 功能、价格、平台等"
        }
        
        # 更新内容标签
        content_label_text = "内容:" if content_type == "article" else f"内容 ({type_hints.get(content_type, '')}):"
        # 这里需要更新标签文本，但需要先找到标签对象
        
        # 更新元数据提示
        metadata_hints = {
            "article": "作者、字数、分类等",
            "link": "网站类型、访问频率等",
            "image": "文件大小、颜色、主题等",
            "video": "上传者、观看次数、质量等",
            "code": "GitHub链接、许可证、依赖等",
            "news": "发布时间、重要性、相关话题等",
            "tutorial": "目标受众、前置知识、完成时间等",
            "tool": "开发者、更新频率、用户评价等"
        }
        
        # 更新元数据框架标题
        self.metadata_frame.config(text=f"元数据 ({metadata_hints.get(content_type, '可选')})")
    
    def add_entry(self):
        """添加条目"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        url = self.url_entry.get().strip()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
        content_type = self.content_type_var.get()
        
        # 解析元数据
        metadata_text = self.metadata_text.get("1.0", tk.END).strip()
        metadata = {}
        if metadata_text:
            try:
                # 尝试解析JSON格式的元数据
                import json
                metadata = json.loads(metadata_text)
            except:
                # 如果不是JSON，则按行解析为键值对
                for line in metadata_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        if not title:
            messagebox.showerror("错误", "标题不能为空！")
            return
        
        if content_type == "article" and not content:
            messagebox.showerror("错误", "文章类型的内容不能为空！")
            return
        
        if self.db.add_entry(title, content, url, tags, content_type, metadata):
            self.db.save_data()
            self.refresh_entry_list()
            self.clear_form()
            messagebox.showinfo("成功", "条目添加成功！")
        else:
            messagebox.showerror("错误", "添加失败！")
    
    def update_entry(self):
        """更新条目"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要更新的条目！")
            return
        
        item = self.tree.item(selected_item[0])
        entry_id = int(item['values'][0])
        
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        url = self.url_entry.get().strip()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
        content_type = self.content_type_var.get()
        
        # 解析元数据
        metadata_text = self.metadata_text.get("1.0", tk.END).strip()
        metadata = {}
        if metadata_text:
            try:
                import json
                metadata = json.loads(metadata_text)
            except:
                for line in metadata_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        if not title:
            messagebox.showerror("错误", "标题不能为空！")
            return
        
        if content_type == "article" and not content:
            messagebox.showerror("错误", "文章类型的内容不能为空！")
            return
        
        if self.db.update_entry(entry_id, title, content, url, tags, content_type, metadata):
            self.db.save_data()
            self.refresh_entry_list()
            self.clear_form()
            messagebox.showinfo("成功", "条目更新成功！")
        else:
            messagebox.showerror("错误", "更新失败！")
    
    def delete_entry(self):
        """删除条目"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要删除的条目！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的条目吗？"):
            item = self.tree.item(selected_item[0])
            entry_id = int(item['values'][0])
            
            if self.db.delete_entry(entry_id):
                self.db.save_data()
                self.refresh_entry_list()
                messagebox.showinfo("成功", "条目删除成功！")
            else:
                messagebox.showerror("错误", "删除失败！")
    
    def clear_form(self):
        """清空表单"""
        self.title_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.metadata_text.delete("1.0", tk.END)
        self.content_type_var.set("article")
        self.on_content_type_change()
    
    def on_item_double_click(self, event):
        """双击条目事件"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            entry_id = int(item['values'][0])
            entry = self.db.get_entry_by_id(entry_id)
            
            if entry:
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, entry['title'])
                
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, entry['url'])
                
                self.tags_entry.delete(0, tk.END)
                self.tags_entry.insert(0, ", ".join(entry['tags']))
                
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", entry['content'])
                
                # 设置内容类型
                content_type = entry.get('content_type', 'article')
                self.content_type_var.set(content_type)
                self.on_content_type_change()
                
                # 设置元数据
                self.metadata_text.delete("1.0", tk.END)
                metadata = entry.get('metadata', {})
                if metadata:
                    try:
                        import json
                        metadata_text = json.dumps(metadata, ensure_ascii=False, indent=2)
                    except:
                        metadata_text = '\n'.join([f"{k}: {v}" for k, v in metadata.items()])
                    self.metadata_text.insert("1.0", metadata_text)
    
    def refresh_entry_list(self):
        """刷新条目列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加所有条目
        for entry in self.db.get_all_entries():
            tags_text = ", ".join(entry['tags'][:2])  # 只显示前2个标签
            if len(entry['tags']) > 2:
                tags_text += "..."
            
            content_type = entry.get('content_type', 'article')
            type_display = {
                'article': '文章',
                'link': '链接',
                'image': '图片',
                'video': '视频',
                'code': '代码',
                'news': '新闻',
                'tutorial': '教程',
                'tool': '工具'
            }.get(content_type, content_type)
            
            self.tree.insert("", tk.END, values=(
                entry['id'],
                type_display,
                entry['title'][:25] + "..." if len(entry['title']) > 25 else entry['title'],
                entry['url'][:15] + "..." if len(entry['url']) > 15 else entry['url'],
                tags_text,
                entry['created_at'][:10]  # 只显示日期
            ))
        
        self.update_stats()
    
    def filter_entries(self, event=None):
        """过滤条目"""
        query = self.search_entry.get().strip()
        if not query:
            self.refresh_entry_list()
            return
        
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 搜索并添加匹配的条目
        results = self.db.search(query)
        for entry in results:
            tags_text = ", ".join(entry['tags'][:3])
            if len(entry['tags']) > 3:
                tags_text += "..."
            
            self.tree.insert("", tk.END, values=(
                entry['id'],
                entry['title'][:30] + "..." if len(entry['title']) > 30 else entry['title'],
                entry['url'][:20] + "..." if len(entry['url']) > 20 else entry['url'],
                tags_text,
                entry['created_at'][:10]
            ))
    
    def save_database(self):
        """保存数据库"""
        if self.db.save_data():
            messagebox.showinfo("成功", "数据库保存成功！")
        else:
            messagebox.showerror("错误", "数据库保存失败！")
    
    def import_data(self):
        """导入数据"""
        filename = filedialog.askopenfilename(
            title="选择导入文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.db.import_from_json(filename):
                self.db.save_data()
                self.refresh_entry_list()
                messagebox.showinfo("成功", "数据导入成功！")
            else:
                messagebox.showerror("错误", "数据导入失败！")
    
    def export_data(self):
        """导出数据"""
        filename = filedialog.asksaveasfilename(
            title="保存导出文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.db.export_to_json(filename):
                messagebox.showinfo("成功", f"数据导出成功！\n保存到: {filename}")
            else:
                messagebox.showerror("错误", "数据导出失败！")
    
    def update_stats(self):
        """
        更新统计信息
        显示数据库的详细统计信息，包括条目数量、标签数量、内容类型分布等
        """
        # 获取数据库统计信息
        stats = self.db.get_statistics()
        content_types = stats.get('content_types', {})
        
        # 格式化内容类型信息
        type_lines = []
        for content_type, count in content_types.items():
            type_name = {
                "article": "📄 文章",
                "link": "🔗 链接", 
                "image": "🖼️ 图片",
                "video": "🎥 视频",
                "code": "💻 代码",
                "news": "📰 新闻",
                "tutorial": "📚 教程",
                "tool": "🛠️ 工具"
            }.get(content_type, f"📝 {content_type}")
            type_lines.append(f"{type_name}: {count}")
        
        # 格式化文件大小
        file_size = stats['file_size']
        if file_size < 1024:
            size_text = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_text = f"{file_size / 1024:.1f} KB"
        else:
            size_text = f"{file_size / (1024 * 1024):.1f} MB"
        
        # 创建多行统计信息
        stats_lines = [
            f"📊 总条目数: {stats['total_entries']}",
            f"🏷️ 总标签数: {stats['total_tags']}",
            f"💾 文件大小: {size_text}",
            "",
            "📋 内容类型分布:",
            *type_lines
        ]
        
        # 设置统计信息文本
        stats_text = "\n".join(stats_lines)
        self.stats_label.config(text=stats_text)
    
    def batch_delete_entries(self):
        """批量删除条目"""
        # 创建批量删除对话框
        delete_window = tk.Toplevel(self.root)
        delete_window.title("批量删除条目")
        delete_window.geometry("500x400")
        delete_window.configure(bg="#f5f5f5")
        delete_window.resizable(False, False)
        
        # 居中显示窗口
        delete_window.update_idletasks()
        x = (delete_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (delete_window.winfo_screenheight() // 2) - (400 // 2)
        delete_window.geometry(f"500x400+{x}+{y}")
        
        # 使窗口模态
        delete_window.transient(self.root)
        delete_window.grab_set()
        
        # 主框架
        main_frame = tk.Frame(delete_window, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="批量删除条目", 
                              font=(self.font_family, 16, "bold"), 
                              bg="#f5f5f5", fg="#333")
        title_label.pack(pady=(0, 20))
        
        # 说明文本
        info_label = tk.Label(main_frame, 
                              text="请输入要删除的ID列表，用逗号分隔\n例如: 1,3,5,7", 
                              font=(self.font_family, 11), 
                              bg="#f5f5f5", fg="#666")
        info_label.pack(pady=(0, 10))
        
        # ID输入框
        id_frame = tk.Frame(main_frame, bg="#f5f5f5")
        id_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(id_frame, text="ID列表:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w")
        
        id_entry = tk.Entry(id_frame, font=(self.font_family, 11), width=50)
        id_entry.pack(fill=tk.X, pady=(5, 0))
        
        # 预览区域
        preview_frame = tk.LabelFrame(main_frame, text="预览要删除的条目", 
                                     font=(self.font_family, 11, "bold"),
                                     bg="#f5f5f5", fg="#333")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 预览列表
        preview_tree = ttk.Treeview(preview_frame, columns=("ID", "标题", "URL"), 
                                   show="headings", height=8)
        preview_tree.heading("ID", text="ID")
        preview_tree.heading("标题", text="标题")
        preview_tree.heading("URL", text="URL")
        
        preview_tree.column("ID", width=50)
        preview_tree.column("标题", width=200)
        preview_tree.column("URL", width=150)
        
        preview_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def update_preview():
            """更新预览列表"""
            # 清空现有项目
            for item in preview_tree.get_children():
                preview_tree.delete(item)
            
            # 解析ID列表
            id_text = id_entry.get().strip()
            if not id_text:
                return
            
            try:
                id_list = [int(x.strip()) for x in id_text.split(",") if x.strip()]
            except ValueError:
                return
            
            # 显示要删除的条目
            for entry_id in id_list:
                entry = self.db.get_entry_by_id(entry_id)
                if entry:
                    preview_tree.insert("", tk.END, values=(
                        entry['id'],
                        entry['title'][:30] + "..." if len(entry['title']) > 30 else entry['title'],
                        entry['url'][:20] + "..." if len(entry['url']) > 20 else entry['url']
                    ))
        
        # 绑定输入事件
        id_entry.bind("<KeyRelease>", lambda e: update_preview())
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X)
        
        # 确认删除按钮
        confirm_button = tk.Button(button_frame, text="确认删除", 
                                  font=(self.font_family, 12), bg="#d73527", fg="white",
                                  command=lambda: self.execute_batch_delete(id_entry.get().strip(), delete_window),
                                  width=12)
        confirm_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 取消按钮
        cancel_button = tk.Button(button_frame, text="取消", 
                                 font=(self.font_family, 12), bg="#666", fg="white",
                                 command=delete_window.destroy, width=12)
        cancel_button.pack(side=tk.RIGHT)
        
        # 刷新按钮
        refresh_button = tk.Button(button_frame, text="刷新预览", 
                                  font=(self.font_family, 12), bg="#4285f4", fg="white",
                                  command=update_preview, width=12)
        refresh_button.pack(side=tk.LEFT)
        
        # 初始预览
        update_preview()
    
    def execute_batch_delete(self, id_text, window):
        """执行批量删除"""
        if not id_text.strip():
            messagebox.showerror("错误", "请输入要删除的ID列表！")
            return
        
        try:
            # 解析ID列表
            id_list = [int(x.strip()) for x in id_text.split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("错误", "ID格式不正确！请输入数字，用逗号分隔。")
            return
        
        if not id_list:
            messagebox.showerror("错误", "没有有效的ID！")
            return
        
        # 检查ID是否存在
        valid_ids = []
        invalid_ids = []
        for entry_id in id_list:
            entry = self.db.get_entry_by_id(entry_id)
            if entry:
                valid_ids.append(entry_id)
            else:
                invalid_ids.append(entry_id)
        
        if invalid_ids:
            messagebox.showwarning("警告", f"以下ID不存在: {', '.join(map(str, invalid_ids))}")
        
        if not valid_ids:
            messagebox.showerror("错误", "没有有效的ID可以删除！")
            return
        
        # 确认删除
        if messagebox.askyesno("确认删除", 
                              f"确定要删除 {len(valid_ids)} 个条目吗？\n"
                              f"ID列表: {', '.join(map(str, valid_ids))}"):
            
            # 执行删除
            success_count = 0
            failed_ids = []
            
            for entry_id in valid_ids:
                if self.db.delete_entry(entry_id):
                    success_count += 1
                else:
                    failed_ids.append(entry_id)
            
            # 保存数据
            self.db.save_data()
            
            # 刷新列表
            self.refresh_entry_list()
            
            # 关闭窗口
            window.destroy()
            
            # 显示结果
            if success_count == len(valid_ids):
                messagebox.showinfo("成功", f"成功删除 {success_count} 个条目！")
            else:
                messagebox.showwarning("部分成功", 
                                     f"成功删除 {success_count} 个条目\n"
                                     f"删除失败: {', '.join(map(str, failed_ids))}")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DataInputGUI()
    app.run()
