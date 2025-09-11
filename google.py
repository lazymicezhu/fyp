#################################################################
###╔══════════════════════════════════════════════════════════╗##
###║                      Lazymice Project                    ║##
###║      Author: Lazymice                                    ║##
###║      Start Date: 2025-09-11                              ║##
###║      Description: FYP Project                            ║##
###╚══════════════════════════════════════════════════════════╝##
#################################################################

'''
导入tkinter 用于创建GUI
导入PTL中的Image和ImageTK 用于处理和显示图片
导入platform 用于判断当前操作系统
导入json 用于数据存储
导入re 用于正则表达式搜索
'''
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import platform
import json
import re

'''
自动选择合适的中文字体
Windows 用微软雅黑
Mac 用苹方
'''
if platform.system() == "Windows":
    font_family = "Microsoft YaHei"
elif platform.system() == "Darwin":
    font_family = "PingFang SC"

# 导入独立的信息库模块
from information_database import InformationDatabase

# 创建信息库实例
info_db = InformationDatabase()

# 全局变量
current_view = "search"  # 当前视图：search 或 results 或 page
search_results = []

def perform_search():
    """执行搜索功能"""
    global current_view, search_results
    query = search_entry.get().strip()
    
    if not query:
        return
    
    # 搜索信息库
    search_results = info_db.search(query)
    current_view = "results"
    
    # 切换到搜索结果界面
    show_search_results()

def show_search_results():
    """显示搜索结果"""
    global current_view
    
    # 隐藏主搜索界面
    main_frame.pack_forget()
    
    # 创建搜索结果界面
    results_frame = tk.Frame(root, bg="white", width=1150, height=700)
    results_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # 返回按钮
    back_button = tk.Button(results_frame, text="← 返回搜索", 
                           font=(font_family, 12), bg="#4285f4", fg="white",
                           command=show_main_search)
    back_button.place(x=20, y=20)
    
    # 搜索结果标题
    results_title = tk.Label(results_frame, text=f"搜索结果 ({len(search_results)} 条)", 
                            font=(font_family, 18, "bold"), bg="white", fg="#333")
    results_title.place(x=20, y=60)
    
    # 创建滚动区域
    canvas = tk.Canvas(results_frame, bg="white", height=580, width=1100)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.place(x=20, y=100, width=1080, height=580)
    scrollbar.place(x=1100, y=100, height=580)
    
    # 显示搜索结果
    y_position = 20
    for i, result in enumerate(search_results):
        # 创建结果项框架
        result_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        result_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 标题（可点击）
        title_label = tk.Label(result_frame, text=result["title"], 
                              font=(font_family, 14, "bold"), bg="white", fg="#1a0dab",
                              cursor="hand2")
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        title_label.bind("<Button-1>", lambda e, r=result: show_page_content(r))
        
        # URL
        url_label = tk.Label(result_frame, text=result["url"], 
                            font=(font_family, 10), bg="white", fg="#006621")
        url_label.pack(anchor="w", padx=10)
        
        # 内容预览
        content_preview = result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"]
        content_label = tk.Label(result_frame, text=content_preview, 
                                font=(font_family, 11), bg="white", fg="#545454",
                                wraplength=1000, justify="left")
        content_label.pack(anchor="w", padx=10, pady=(5, 10))
        
        # 标签
        if result["tags"]:
            tags_text = "标签: " + ", ".join(result["tags"])
            tags_label = tk.Label(result_frame, text=tags_text, 
                                 font=(font_family, 9), bg="white", fg="#666")
            tags_label.pack(anchor="w", padx=10, pady=(0, 10))

def show_page_content(result):
    """显示页面内容"""
    global current_view
    
    # 隐藏搜索结果界面
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != main_frame:
            widget.destroy()
    
    # 创建页面内容界面
    page_frame = tk.Frame(root, bg="white", width=1150, height=700)
    page_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # 返回按钮
    back_button = tk.Button(page_frame, text="← 返回搜索结果", 
                           font=(font_family, 12), bg="#4285f4", fg="white",
                           command=show_search_results)
    back_button.place(x=20, y=20)
    
    # 页面标题
    page_title = tk.Label(page_frame, text=result["title"], 
                         font=(font_family, 20, "bold"), bg="white", fg="#333")
    page_title.place(x=20, y=60)
    
    # URL显示
    url_label = tk.Label(page_frame, text=result["url"], 
                        font=(font_family, 12), bg="white", fg="#006621")
    url_label.place(x=20, y=100)
    
    # 内容区域（可滚动）
    content_text = scrolledtext.ScrolledText(page_frame, 
                                            font=(font_family, 12),
                                            wrap=tk.WORD, 
                                            width=100, height=25,
                                            bg="white", fg="#333",
                                            relief=tk.FLAT, bd=0)
    content_text.place(x=20, y=130, width=1100, height=500)
    
    # 插入内容
    content_text.insert(tk.END, result["content"])
    content_text.config(state=tk.DISABLED)  # 设为只读
    
    current_view = "page"

def show_main_search():
    """显示主搜索界面"""
    global current_view
    
    # 销毁其他界面
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != main_frame:
            widget.destroy()
    
    # 显示主搜索界面
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    current_view = "search"

def on_search_key(event):
    """处理搜索框按键事件"""
    if event.keysym == "Return":
        perform_search()

'''
创建主窗口root
设置窗口标题
设置窗口大小
设置窗口背景色
'''
root = tk.Tk()
root.title("Google UI Mockup - 本地信息库搜索")
root.geometry("1200x800")
root.configure(bg="#f5f5f5")

'''
创建一个顶部栏top_bar 背景色和主窗口一致 设置高度
用pack布局 横向填满顶部
'''
#top_bar = tk.Frame(root, bg="#f5f5f5", height=60)
#top_bar.pack(fill=tk.X, side=tk.TOP)

'''
在顶部栏放一个标签 显示“浏览器界面”
背景色浅灰 文字颜色灰色 字体用自动选择的中文字体 设置字号
用 place 布局 定位在 (20, 20)
'''
#browser_label = tk.Label(top_bar, text="浏览器界面", bg="#f5f5f5", fg="#bdbdbd", font=(font_family, 10))
#browser_label.place(x=20, y=20)


'''
创建主内容区 main_frame 背景白色 宽 1150 高 700
用 place 布局 居中显示在窗口的 50% 高度处
'''
main_frame = tk.Frame(root, bg="white", width=1150, height=700)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

'''
在主内容区左上角创建一个小框 arrow_frame 用于放箭头
箭头标签 arrow_label 显示 "»"，字体加粗，字号 16 颜色深灰
用 pack 布局 箭头有内边距
'''
#arrow_frame = tk.Frame(main_frame, bg="white", width=30, height=40)
#arrow_frame.place(x=0, y=30)
#arrow_label = tk.Label(arrow_frame, text="»", bg="white", fg="#444", font=(font_family, 16, "bold"))
#arrow_label.pack(padx=5, pady=5)

# logo图片
'''
打开并缩放 Google logo 图片为 300x100
转换为 Tkinter 可用的图片对象
创建标签 logo_label 显示 logo 图片 背景白色
用 place 布局 居中显示在主内容区的 45% 高度处
logo_label.image = logo 这行是为了防止图片被垃圾回收导致不显示
'''
logo_img = Image.open("google_logo.png").resize((300, 100))
logo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(main_frame, image=logo, bg="white")
logo_label.image = logo
logo_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# 搜索框（带图片icon和边框）
'''
在主内容区创建一个搜索框外层 search_frame 背景白色
用 place 居中显示在主内容区的 62% 高度处
'''
search_frame = tk.Frame(main_frame, bg="white")
search_frame.place(relx=0.5, rely=0.62, anchor=tk.CENTER)

# 搜索框外层Frame用于显示边框
'''
在搜索框外层再嵌套一个 search_border 用于显示边框
边框颜色为浅灰色  宽度 1  样式为实线
'''
search_border = tk.Frame(search_frame, bg="#dadce0", bd=1, relief=tk.SOLID)
search_border.pack()

# 搜索icon图片
'''
打开并缩放搜索图标图片为 28x28
转换为 Tkinter 可用的图片对象
创建标签 icon_label 显示搜索图标 背景白色
用 pack 布局 左侧显示 左右有内边距
'''
icon_img = Image.open("search_bar_1.png").resize((28, 28))
icon = ImageTk.PhotoImage(icon_img)
icon_label = tk.Label(search_border, image=icon, bg="white")
icon_label.image = icon
icon_label.pack(side=tk.LEFT, padx=(10, 5))

# 输入框
'''
创建输入框 search_entry 字体用自动选择的中文字体 字号 16
无边框 样式为平面
宽度 40 个字符 文字颜色深灰 背景白色
用 pack 布局 左侧显示 垂直内边距 10 右侧内边距 10
绑定回车键事件
'''
search_entry = tk.Entry(search_border, font=(font_family, 16), bd=0, relief=tk.FLAT, width=40, fg="#444", bg="white")
search_entry.pack(side=tk.LEFT, ipady=10, padx=(0, 10))
search_entry.bind("<KeyPress>", on_search_key)

# 搜索按钮
search_button = tk.Button(search_border, text="搜索", 
                         font=(font_family, 14), bg="#4285f4", fg="white",
                         command=perform_search, relief=tk.FLAT, bd=0)
search_button.pack(side=tk.RIGHT, padx=(0, 10), pady=5)

# 管理按钮（在主内容区右上角）
def open_data_manager():
    """打开数据管理界面"""
    import subprocess
    import sys
    try:
        subprocess.Popen([sys.executable, "data_manager.py"])
    except Exception as e:
        print(f"无法打开数据管理界面: {e}")

manage_button = tk.Button(main_frame, text="数据管理", 
                         font=(font_family, 12), bg="#34a853", fg="white",
                         command=open_data_manager, relief=tk.FLAT, bd=0)
manage_button.place(x=1050, y=20)

'''
启动 Tkinter 主事件循环 窗口开始响应用户操作
'''
root.mainloop()
