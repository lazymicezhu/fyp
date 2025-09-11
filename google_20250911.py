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
'''
import tkinter as tk
from PIL import Image, ImageTk
import platform

'''
自动选择合适的中文字体
Windows 用微软雅黑
Mac 用苹方
'''
if platform.system() == "Windows":
    font_family = "Microsoft YaHei"
elif platform.system() == "Darwin":
    font_family = "PingFang SC"

'''
创建主窗口root
设置窗口标题
设置窗口大小
设置窗口背景色
'''
root = tk.Tk()
root.title("Google UI Mockup")
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
'''
search_entry = tk.Entry(search_border, font=(font_family, 16), bd=0, relief=tk.FLAT, width=40, fg="#444", bg="white")
search_entry.pack(side=tk.LEFT, ipady=10, padx=(0, 10))

'''
启动 Tkinter 主事件循环 窗口开始响应用户操作
'''
root.mainloop()
