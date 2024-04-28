import tkinter as tk
from tkinter import font
def create_nav_buttons(canvas):
    # 导航按钮的起始位置
    start_x = 228.0
    button_width = 150
    button_height = 70
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")  # 创建字体对象

    # 按钮文本和命令
    buttons_info = [
        ("Home", lambda: print("Home clicked")),
        ("Collection", lambda: print("Collection clicked")),
        ("Train", lambda: print("Train clicked")),
        ("Test", lambda: print("Test clicked"))
    ]
    
    # 创建按钮
    for i, (text, command) in enumerate(buttons_info):
        button = tk.Button(canvas, text=text, command=command,font=custom_font,
                           relief="flat", borderwidth=0, highlightthickness=0,
                           bg="#7EFFF7", fg="black", activebackground="#7EFFF7", activeforeground="blue")
        button_window = canvas.create_window(
            start_x + i * button_width, 0,
            anchor="nw", window=button, width=button_width, height=button_height)