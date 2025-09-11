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
    """数据输入GUI界面"""
    
    def __init__(self):
        self.db = InformationDatabase()
        self.setup_fonts()
        self.setup_main_window()
        self.setup_widgets()
        self.refresh_entry_list()
    
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
        self.root.title("信息库数据管理 - Lazymice Project")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_widgets(self):
        """设置界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="信息库数据管理系统", 
                              font=(self.font_family, 18, "bold"), 
                              bg="#f5f5f5", fg="#333")
        title_label.pack(pady=(0, 20))
        
        # 创建左右分栏
        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg="#f5f5f5")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 左侧：数据输入表单
        self.setup_input_form(left_frame)
        
        # 右侧：数据列表和管理
        self.setup_data_list(right_frame)
    
    def setup_input_form(self, parent):
        """设置数据输入表单"""
        # 表单框架
        form_frame = tk.LabelFrame(parent, text="添加/编辑信息", 
                                  font=(self.font_family, 12, "bold"),
                                  bg="#f5f5f5", fg="#333")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题输入
        tk.Label(form_frame, text="标题:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(10, 5))
        self.title_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        self.title_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # URL输入
        tk.Label(form_frame, text="URL:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        self.url_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        self.url_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 标签输入
        tk.Label(form_frame, text="标签 (用逗号分隔):", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        self.tags_entry = tk.Entry(form_frame, font=(self.font_family, 11), width=50)
        self.tags_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 内容输入
        tk.Label(form_frame, text="内容:", font=(self.font_family, 11), 
                bg="#f5f5f5").pack(anchor="w", padx=10, pady=(0, 5))
        self.content_text = scrolledtext.ScrolledText(form_frame, 
                                                    font=(self.font_family, 11),
                                                    height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 按钮框架
        button_frame = tk.Frame(form_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 添加按钮
        add_button = tk.Button(button_frame, text="添加", 
                              font=(self.font_family, 11), bg="#4285f4", fg="white",
                              command=self.add_entry, width=10)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 更新按钮
        update_button = tk.Button(button_frame, text="更新", 
                                 font=(self.font_family, 11), bg="#34a853", fg="white",
                                 command=self.update_entry, width=10)
        update_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 清空按钮
        clear_button = tk.Button(button_frame, text="清空", 
                                font=(self.font_family, 11), bg="#ea4335", fg="white",
                                command=self.clear_form, width=10)
        clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 保存按钮
        save_button = tk.Button(button_frame, text="保存", 
                               font=(self.font_family, 11), bg="#fbbc04", fg="black",
                               command=self.save_database, width=10)
        save_button.pack(side=tk.RIGHT)
    
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
        
        # 管理按钮
        manage_frame = tk.Frame(list_frame, bg="#f5f5f5")
        manage_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 导入导出按钮
        import_button = tk.Button(manage_frame, text="导入", 
                                 font=(self.font_family, 10), bg="#34a853", fg="white",
                                 command=self.import_data, width=8)
        import_button.pack(side=tk.LEFT, padx=(0, 5))
        
        export_button = tk.Button(manage_frame, text="导出", 
                                 font=(self.font_family, 10), bg="#fbbc04", fg="black",
                                 command=self.export_data, width=8)
        export_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 删除按钮
        delete_button = tk.Button(manage_frame, text="删除", 
                                 font=(self.font_family, 10), bg="#ea4335", fg="white",
                                 command=self.delete_entry, width=8)
        delete_button.pack(side=tk.RIGHT)
        
        # 统计信息
        self.stats_label = tk.Label(list_frame, text="", font=(self.font_family, 9), 
                                   bg="#f5f5f5", fg="#666")
        self.stats_label.pack(pady=(0, 10))
        self.update_stats()
    
    def setup_treeview(self, parent):
        """设置树形视图"""
        # 创建Treeview
        columns = ("ID", "标题", "URL", "标签", "创建时间")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        self.tree.heading("ID", text="ID")
        self.tree.heading("标题", text="标题")
        self.tree.heading("URL", text="URL")
        self.tree.heading("标签", text="标签")
        self.tree.heading("创建时间", text="创建时间")
        
        self.tree.column("ID", width=50)
        self.tree.column("标题", width=200)
        self.tree.column("URL", width=150)
        self.tree.column("标签", width=100)
        self.tree.column("创建时间", width=120)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=(0, 10))
    
    def add_entry(self):
        """添加条目"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        url = self.url_entry.get().strip()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
        
        if not title or not content:
            messagebox.showerror("错误", "标题和内容不能为空！")
            return
        
        if self.db.add_entry(title, content, url, tags):
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
        
        if not title or not content:
            messagebox.showerror("错误", "标题和内容不能为空！")
            return
        
        if self.db.update_entry(entry_id, title, content, url, tags):
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
    
    def refresh_entry_list(self):
        """刷新条目列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加所有条目
        for entry in self.db.get_all_entries():
            tags_text = ", ".join(entry['tags'][:3])  # 只显示前3个标签
            if len(entry['tags']) > 3:
                tags_text += "..."
            
            self.tree.insert("", tk.END, values=(
                entry['id'],
                entry['title'][:30] + "..." if len(entry['title']) > 30 else entry['title'],
                entry['url'][:20] + "..." if len(entry['url']) > 20 else entry['url'],
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
        """更新统计信息"""
        stats = self.db.get_statistics()
        stats_text = f"总条目: {stats['total_entries']} | 总标签: {stats['total_tags']} | 文件大小: {stats['file_size']} 字节"
        self.stats_label.config(text=stats_text)
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DataInputGUI()
    app.run()
