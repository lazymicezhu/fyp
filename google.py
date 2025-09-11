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
from tkinter import ttk, scrolledtext, messagebox
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
    """
    执行搜索功能
    从搜索框获取查询内容，在信息库中搜索，然后显示结果
    """
    # 声明全局变量，用于在不同函数间共享状态
    global current_view, search_results
    
    # 从搜索输入框获取查询内容，去除首尾空格
    query = search_entry.get().strip()
    
    # 如果查询内容为空，直接返回，不执行搜索
    if not query:
        return
    
    # 调用信息库的搜索方法，获取搜索结果列表
    search_results = info_db.search(query)
    
    # 设置当前视图为搜索结果界面
    current_view = "results"
    
    # 切换到搜索结果界面
    show_search_results()

def show_search_results():
    """
    显示搜索结果界面
    隐藏主搜索界面，创建新的搜索结果界面，显示搜索到的条目列表
    """
    # 声明全局变量，用于状态管理
    global current_view
    
    # 隐藏主搜索界面，为搜索结果界面让出空间
    main_frame.pack_forget()
    
    # 创建搜索结果界面框架
    # 背景色为白色，宽度1150像素，高度700像素
    results_frame = tk.Frame(root, bg="white", width=1150, height=700)
    # 使用place布局，将框架居中显示在窗口中央
    results_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # 创建返回按钮
    # 按钮文字为"← 返回搜索"，使用蓝色背景和白色文字
    back_button = tk.Button(results_frame, text="← 返回搜索", 
                           font=(font_family, 12), bg="#4285f4", fg="white",
                           command=show_main_search)
    # 使用place布局，将按钮定位在(20, 20)位置
    back_button.place(x=20, y=20)
    
    # 创建搜索结果标题标签
    # 显示搜索结果数量，使用18号加粗字体，深灰色文字
    results_title = tk.Label(results_frame, text=f"搜索结果 ({len(search_results)} 条)", 
                            font=(font_family, 18, "bold"), bg="white", fg="#333")
    # 将标题定位在(20, 60)位置
    results_title.place(x=20, y=60)
    
    # 创建滚动区域组件
    # 画布组件，用于显示可滚动的内容区域
    canvas = tk.Canvas(results_frame, bg="white", height=580, width=1100)
    # 垂直滚动条，与画布的yview方法绑定
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    # 可滚动的框架，用于放置搜索结果项
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    # 绑定滚动框架的配置事件
    # 当框架大小改变时，自动更新画布的滚动区域
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # 在画布中创建窗口，将可滚动框架放入其中
    # 锚点设置为西北角(nw)，确保内容从左上角开始显示
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # 配置画布的垂直滚动命令，与滚动条联动
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 使用place布局定位画布和滚动条
    # 画布位置：(20, 100)，尺寸：1080x580
    canvas.place(x=20, y=100, width=1080, height=580)
    # 滚动条位置：(1100, 100)，高度：580
    scrollbar.place(x=1100, y=100, height=580)
    
    # 遍历搜索结果，为每个结果创建显示项
    y_position = 20  # 初始垂直位置
    for i, result in enumerate(search_results):
        # 创建单个搜索结果项的框架
        # 背景色为白色，使用凸起边框效果，边框宽度为1像素
        result_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        # 使用pack布局，水平填充，左右边距10像素，上下边距5像素
        result_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 获取内容类型，默认为"article"
        content_type = result.get("content_type", "article")
        
        # 定义不同类型对应的颜色映射
        # 每种内容类型都有独特的颜色标识
        type_colors = {
            "article": "#4285f4",  # 文章 - 蓝色
            "link": "#34a853",     # 链接 - 绿色
            "image": "#fbbc04",    # 图片 - 黄色
            "video": "#ea4335",    # 视频 - 红色
            "code": "#9c27b0",     # 代码 - 紫色
            "news": "#ff9800",     # 新闻 - 橙色
            "tutorial": "#00bcd4", # 教程 - 青色
            "tool": "#795548"      # 工具 - 棕色
        }
        
        # 定义不同类型对应的中文名称映射
        # 将英文类型名转换为中文显示名称
        type_names = {
            "article": "文章",
            "link": "链接",
            "image": "图片", 
            "video": "视频",
            "code": "代码",
            "news": "新闻",
            "tutorial": "教程",
            "tool": "工具"
        }
        
        # 创建内容类型标签
        # 显示中文类型名称，使用9号加粗字体，白色文字
        # 背景色根据类型动态设置，左右内边距8像素，上下内边距2像素
        type_label = tk.Label(result_frame, text=type_names.get(content_type, content_type), 
                             font=(font_family, 9, "bold"), bg=type_colors.get(content_type, "#666"), 
                             fg="white", padx=8, pady=2)
        # 将类型标签左对齐放置，左右边距10像素，上下边距(10, 5)像素
        type_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # 创建可点击的标题标签
        # 显示条目标题，使用14号加粗字体，蓝色文字(#1a0dab)，鼠标悬停时显示手型光标
        title_label = tk.Label(result_frame, text=result["title"], 
                              font=(font_family, 14, "bold"), bg="white", fg="#1a0dab",
                              cursor="hand2")
        # 左对齐放置，左右边距10像素，上下边距(0, 5)像素
        title_label.pack(anchor="w", padx=10, pady=(0, 5))
        # 绑定鼠标左键点击事件，点击时调用show_page_content函数显示完整内容
        title_label.bind("<Button-1>", lambda e, r=result: show_page_content(r))
        
        # 创建URL标签
        # 显示条目的URL地址，使用10号字体，绿色文字(#006621)
        url_label = tk.Label(result_frame, text=result["url"], 
                            font=(font_family, 10), bg="white", fg="#006621")
        # 左对齐放置，左右边距10像素
        url_label.pack(anchor="w", padx=10)
        
        # 根据内容类型动态显示不同的预览信息
        # 每种类型都有独特的预览方式，提供更丰富的信息展示
        if content_type == "link":
            # 链接类型：显示内容描述的前150个字符
            # 如果内容超过150字符，则截断并添加省略号
            content_preview = result["content"][:150] + "..." if len(result["content"]) > 150 else result["content"]
        elif content_type == "image":
            # 图片类型：显示图片的元数据信息
            # 获取图片的元数据，包括尺寸、格式、文件大小等信息
            metadata = result.get("metadata", {})
            metadata_info = []
            # 如果存在尺寸信息，添加到预览中
            if "dimensions" in metadata:
                metadata_info.append(f"尺寸: {metadata['dimensions']}")
            # 如果存在格式信息，添加到预览中
            if "format" in metadata:
                metadata_info.append(f"格式: {metadata['format']}")
            # 如果存在文件大小信息，添加到预览中
            if "file_size" in metadata:
                metadata_info.append(f"大小: {metadata['file_size']}")
            # 将元数据信息用"|"连接，如果没有元数据则显示内容前150字符
            content_preview = " | ".join(metadata_info) if metadata_info else result["content"][:150]
        elif content_type == "video":
            # 视频类型：显示视频的时长、平台、观看数等信息
            # 获取视频的元数据信息
            metadata = result.get("metadata", {})
            video_info = []
            # 如果存在时长信息，添加到预览中
            if "duration" in metadata:
                video_info.append(f"时长: {metadata['duration']}")
            # 如果存在平台信息，添加到预览中
            if "platform" in metadata:
                video_info.append(f"平台: {metadata['platform']}")
            # 如果存在观看数信息，添加到预览中
            if "views" in metadata:
                video_info.append(f"观看: {metadata['views']}")
            # 将视频信息用"|"连接，如果没有信息则显示内容前150字符
            content_preview = " | ".join(video_info) if video_info else result["content"][:150]
        elif content_type == "code":
            # 代码类型：显示编程语言和复杂度信息
            # 获取代码的元数据信息
            metadata = result.get("metadata", {})
            code_info = []
            # 如果存在编程语言信息，添加到预览中
            if "language" in metadata:
                code_info.append(f"语言: {metadata['language']}")
            # 如果存在复杂度信息，添加到预览中
            if "complexity" in metadata:
                code_info.append(f"复杂度: {metadata['complexity']}")
            # 将代码信息用"|"连接，如果没有信息则显示内容前150字符
            content_preview = " | ".join(code_info) if code_info else result["content"][:150]
        elif content_type == "news":
            # 新闻类型：显示新闻来源和时间信息
            # 获取新闻的元数据信息
            metadata = result.get("metadata", {})
            news_info = []
            # 如果存在来源信息，添加到预览中
            if "source" in metadata:
                news_info.append(f"来源: {metadata['source']}")
            # 如果存在发布时间信息，添加到预览中
            if "publish_time" in metadata:
                news_info.append(f"时间: {metadata['publish_time']}")
            # 将新闻信息用"|"连接，如果没有信息则显示内容前150字符
            content_preview = " | ".join(news_info) if news_info else result["content"][:150]
        elif content_type == "tutorial":
            # 教程类型：显示难度、时长、步骤数等信息
            # 获取教程的元数据信息
            metadata = result.get("metadata", {})
            tutorial_info = []
            # 如果存在难度信息，添加到预览中
            if "difficulty" in metadata:
                tutorial_info.append(f"难度: {metadata['difficulty']}")
            # 如果存在时长信息，添加到预览中
            if "duration" in metadata:
                tutorial_info.append(f"时长: {metadata['duration']}")
            # 如果存在步骤数信息，添加到预览中
            if "steps" in metadata:
                tutorial_info.append(f"步骤: {metadata['steps']}")
            # 将教程信息用"|"连接，如果没有信息则显示内容前150字符
            content_preview = " | ".join(tutorial_info) if tutorial_info else result["content"][:150]
        elif content_type == "tool":
            # 工具类型：显示价格、平台、版本等信息
            # 获取工具的元数据信息
            metadata = result.get("metadata", {})
            tool_info = []
            # 如果存在价格信息，添加到预览中
            if "price" in metadata:
                tool_info.append(f"价格: {metadata['price']}")
            # 如果存在平台信息，添加到预览中
            if "platform" in metadata:
                tool_info.append(f"平台: {metadata['platform']}")
            # 如果存在开发者信息，添加到预览中
            if "developer" in metadata:
                tool_info.append(f"开发者: {metadata['developer']}")
            # 将工具信息用"|"连接，如果没有信息则显示内容前150字符
            content_preview = " | ".join(tool_info) if tool_info else result["content"][:150]
        else:
            # 默认情况（文章类型）：显示内容的前200个字符
            # 如果内容超过200字符，则截断并添加省略号
            content_preview = result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"]
        
        # 创建内容预览标签
        # 显示动态生成的内容预览，使用11号字体，深灰色文字
        # 设置自动换行长度为1000像素，左对齐显示
        content_label = tk.Label(result_frame, text=content_preview, 
                                font=(font_family, 11), bg="white", fg="#545454",
                                wraplength=1000, justify="left")
        # 左对齐放置，左右边距10像素，上下边距(5, 10)像素
        content_label.pack(anchor="w", padx=10, pady=(5, 10))
        
        # 创建标签显示区域
        # 如果条目有标签，则显示标签信息
        if result["tags"]:
            # 将标签列表转换为字符串，用逗号分隔
            tags_text = "标签: " + ", ".join(result["tags"])
            # 创建标签显示标签，使用9号字体，深灰色文字
            tags_label = tk.Label(result_frame, text=tags_text, 
                                 font=(font_family, 9), bg="white", fg="#666")
            # 左对齐放置，左右边距10像素，上下边距(0, 10)像素
            tags_label.pack(anchor="w", padx=10, pady=(0, 10))

def show_page_content(result):
    """
    显示页面内容界面
    隐藏搜索结果界面，创建新的页面内容界面，根据内容类型显示不同的内容
    """
    # 声明全局变量，用于状态管理
    global current_view
    
    # 隐藏搜索结果界面
    # 遍历根窗口的所有子组件，销毁除主框架外的所有框架组件
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != main_frame:
            widget.destroy()
    
    # 创建页面内容界面框架
    # 背景色为白色，宽度1150像素，高度700像素
    page_frame = tk.Frame(root, bg="white", width=1150, height=700)
    # 使用place布局，将框架居中显示在窗口中央
    page_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # 创建返回按钮
    # 按钮文字为"← 返回搜索结果"，使用蓝色背景和白色文字
    back_button = tk.Button(page_frame, text="← 返回搜索结果", 
                           font=(font_family, 12), bg="#4285f4", fg="white",
                           command=show_search_results)
    # 使用place布局，将按钮定位在(20, 20)位置
    back_button.place(x=20, y=20)
    
    # 创建页面标题标签
    # 显示条目的标题，使用20号加粗字体，深灰色文字
    page_title = tk.Label(page_frame, text=result["title"], 
                         font=(font_family, 20, "bold"), bg="white", fg="#333")
    # 将标题定位在(20, 60)位置
    page_title.place(x=20, y=60)
    
    # 创建URL显示标签
    # 显示条目的URL地址，使用12号字体，绿色文字
    url_label = tk.Label(page_frame, text=result["url"], 
                        font=(font_family, 12), bg="white", fg="#006621")
    # 将URL标签定位在(20, 100)位置
    url_label.place(x=20, y=100)
    
    # 根据内容类型动态显示不同的内容
    # 每种类型都有独特的显示方式，提供最佳的用户体验
    content_type = result.get("content_type", "article")
    
    if content_type == "link":
        # 链接类型显示
        link_frame = tk.Frame(page_frame, bg="white")
        link_frame.place(x=20, y=130, width=1100, height=500)
        
        # 链接描述
        desc_label = tk.Label(link_frame, text="链接描述:", 
                             font=(font_family, 12, "bold"), bg="white", fg="#333")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        desc_text = scrolledtext.ScrolledText(link_frame, font=(font_family, 11),
                                            wrap=tk.WORD, height=8, bg="white", fg="#333")
        desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        desc_text.insert(tk.END, result["content"])
        desc_text.config(state=tk.DISABLED)
        
        # 访问链接按钮
        visit_button = tk.Button(link_frame, text="访问链接", 
                                font=(font_family, 12), bg="#4285f4", fg="white",
                                command=lambda: open_url(result["url"]))
        visit_button.pack(pady=10)
        
    elif content_type == "image":
        # 图片类型显示
        image_frame = tk.Frame(page_frame, bg="white")
        image_frame.place(x=20, y=130, width=1100, height=500)
        
        # 图片描述
        desc_label = tk.Label(image_frame, text="图片描述:", 
                             font=(font_family, 12, "bold"), bg="white", fg="#333")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        desc_text = scrolledtext.ScrolledText(image_frame, font=(font_family, 11),
                                            wrap=tk.WORD, height=6, bg="white", fg="#333")
        desc_text.pack(fill=tk.X, pady=(0, 10))
        desc_text.insert(tk.END, result["content"])
        desc_text.config(state=tk.DISABLED)
        
        # 图片信息
        metadata = result.get("metadata", {})
        if metadata:
            info_label = tk.Label(image_frame, text="图片信息:", 
                                 font=(font_family, 12, "bold"), bg="white", fg="#333")
            info_label.pack(anchor="w", pady=(10, 5))
            
            info_text = ""
            for key, value in metadata.items():
                info_text += f"{key}: {value}\n"
            
            info_display = tk.Text(image_frame, font=(font_family, 10), height=6,
                                 bg="#f5f5f5", fg="#333", relief=tk.FLAT, bd=0)
            info_display.pack(fill=tk.X)
            info_display.insert(tk.END, info_text)
            info_display.config(state=tk.DISABLED)
    
    elif content_type == "video":
        # 视频类型显示
        video_frame = tk.Frame(page_frame, bg="white")
        video_frame.place(x=20, y=130, width=1100, height=500)
        
        # 视频描述
        desc_label = tk.Label(video_frame, text="视频描述:", 
                             font=(font_family, 12, "bold"), bg="white", fg="#333")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        desc_text = scrolledtext.ScrolledText(video_frame, font=(font_family, 11),
                                            wrap=tk.WORD, height=6, bg="white", fg="#333")
        desc_text.pack(fill=tk.X, pady=(0, 10))
        desc_text.insert(tk.END, result["content"])
        desc_text.config(state=tk.DISABLED)
        
        # 视频信息
        metadata = result.get("metadata", {})
        if metadata:
            info_label = tk.Label(video_frame, text="视频信息:", 
                                 font=(font_family, 12, "bold"), bg="white", fg="#333")
            info_label.pack(anchor="w", pady=(10, 5))
            
            info_text = ""
            for key, value in metadata.items():
                info_text += f"{key}: {value}\n"
            
            info_display = tk.Text(video_frame, font=(font_family, 10), height=6,
                                 bg="#f5f5f5", fg="#333", relief=tk.FLAT, bd=0)
            info_display.pack(fill=tk.X)
            info_display.insert(tk.END, info_text)
            info_display.config(state=tk.DISABLED)
    
    elif content_type == "code":
        # 代码类型显示
        code_frame = tk.Frame(page_frame, bg="white")
        code_frame.place(x=20, y=130, width=1100, height=500)
        
        # 代码描述
        desc_label = tk.Label(code_frame, text="代码说明:", 
                             font=(font_family, 12, "bold"), bg="white", fg="#333")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        desc_text = scrolledtext.ScrolledText(code_frame, font=(font_family, 11),
                                            wrap=tk.WORD, height=4, bg="white", fg="#333")
        desc_text.pack(fill=tk.X, pady=(0, 10))
        desc_text.insert(tk.END, result["content"])
        desc_text.config(state=tk.DISABLED)
        
        # 代码内容
        code_label = tk.Label(code_frame, text="代码内容:", 
                             font=(font_family, 12, "bold"), bg="white", fg="#333")
        code_label.pack(anchor="w", pady=(10, 5))
        
        code_text = scrolledtext.ScrolledText(code_frame, font=("Consolas", 10),
                                            wrap=tk.NONE, height=12, bg="#f8f8f8", fg="#333")
        code_text.pack(fill=tk.BOTH, expand=True)
        
        # 获取代码内容（从content字段）
        code_content = result["content"]
        code_text.insert(tk.END, code_content)
        code_text.config(state=tk.DISABLED)
    
    else:
        # 默认文章类型显示
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

def open_url(url):
    """打开URL链接"""
    import webbrowser
    try:
        webbrowser.open(url)
    except Exception as e:
        messagebox.showerror("错误", f"无法打开链接: {e}")
    
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
root.geometry("1400x900")
root.configure(bg="#f5f5f5")
root.minsize(1200, 700)  # 设置最小窗口大小

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
