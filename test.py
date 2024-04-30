import tkinter as tk
from collection import collection_page
from userdetail import userdetail
# from trainmodel import trainmodel
# from test_real import test_real
from navbar_menu import *
from pathlib import Path
from PIL import Image, ImageTk
# from navbar_menu import *
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
# import tkinter as tk
def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("/home/sam/Desktop/signlanguage/GUI/assets/frame0/")
    return ASSETS_PATH / Path(path)
def create_login_window():
    window = tk.Tk()
    window.title("Login")
    window.geometry("950x600")
    # icon = Image.open("/home/sam/Desktop/signlanguage/GUI/assets/frame0/admin.png")
    # window.iconbitmap("/home/sam/Desktop/signlanguage/GUI/assets/frame0/lock.ico")
    # photo = ImageTk.PhotoImage(icon)
    # window.iconphoto(True,photo)

    # window.iconbitmap(r"\home\sam\Desktop\signlanguage\GUI\assets\frame0\lock.ico")
    window.configure(bg="#61FFF5")

    canvas = Canvas(window, bg = "#61FFF5",height = 600,width = 950,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(301.0,0.0,950.0,600.0,fill="#D9D9D9",outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(259.0,368.0,image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(149.0,121.0,image=image_image_2)

    entry_image_username = PhotoImage(file=relative_to_assets("entry_username.png"))
    entry_bg_username = canvas.create_image(702.0,251.5,image=entry_image_username)
    entry_username = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    entry_username.place(x=529.0,y=227.0,width=346.0,height=47.0)

    entry_image_pass = PhotoImage(file=relative_to_assets("entry_pass.png"))
    entry_bg_pass = canvas.create_image(702.0,345.5,image=entry_image_pass)
    entry_pass = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    entry_pass.place(x=529.0,y=321.0,width=346.0,height=47.0 )

    canvas.create_text(529.0,199.0,anchor="nw",text="Username :",fill="#000000",font=("Inter MediumItalic", 15 * -1))
    canvas.create_text(529.0,298.0,anchor="nw",text="Password:",fill="#000000",font=("Inter MediumItalic", 15 * -1))
    canvas.create_text(791.0,205.0,anchor="nw",text="Example: admin",fill="#000000",font=("Inter MediumItalic", 11 * -1))
    canvas.create_text(791.0,300.0,anchor="nw",text="Example: 1234",fill="#000000",font=("Inter MediumItalic", 11 * -1))
    canvas.create_text(581.0,121.0,anchor="nw",text="Login Admin Account",fill="#000000",font=("Inter MediumItalic", 24 * -1))

    button_image_signin = PhotoImage(file=relative_to_assets("SignIn.png"))
    button_signin = Button(image=button_image_signin,borderwidth=0,highlightthickness=0,command=lambda: login(entry_username, entry_pass, window),relief="flat")
    button_signin.place(x=599.0, y=413.0, width=235.0, height=59.0)

    window.resizable(False, False)
    window.mainloop()

def login(entry_username, entry_pass, window):
    username = entry_username.get()
    password = entry_pass.get()
    if username == "admin" and password == "1234":
        messagebox.showinfo("Success", "Welcome Admin.")
        window.destroy()  # 关闭登录窗口
        app = MainApplication()  # 创建并启动主应用程序
        app.mainloop()
    else:
        messagebox.showerror("Failure", "Invalid username or password")
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("950x650")
        self.title('SignGuru Admin')
        # self.iconbitmap(r"C:\Users\Dell Inspiron\Documents\CV_Project\GUI\assets\frame0\on.ico")
        self.pages = {
            # "home": create_home_page(self),
            # "userdetail": userdetail(self),
            "collection": collection_page(self),
            # "trainmodel": trainmodel(self),
            # "test-real": test_real(self),
            "userdetail": userdetail(self) 
        }
        # 创建导航栏并初始显示首页或任何页面
        self.create_nav_buttons()
        self.show_page('userdetail')  # 默认显示集合页面
                # 初始化所有页面，但默认不显示
        for page in self.pages.values():
            page.place(x=0, y=0, width=950, height=650)

    def create_nav_buttons(self):
        start_x = 228.0
        button_width = 150
        button_height = 70
        custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        buttons_info = [
            ("User Data", "userdetail"),
            ("Test-Real", "collection")
            # ("Train", "trainmodel"),
            # ("Test-real", "test-real"),
        ]
    # 计算最后一个按钮的位置
        last_button_x = start_x + len(buttons_info) * button_width

        for i, (text, page_name) in enumerate(buttons_info):
            button = tk.Button(self, text=text, font=custom_font,
                            relief="flat", borderwidth=0, highlightthickness=0,
                            bg="#7EFFF7", fg="black", activebackground="#7EFFF7", activeforeground="blue",
                            command=lambda name=page_name: self.show_page(name))
            button.place(x=start_x + i * button_width, y=0, width=button_width, height=button_height)


        # 添加 Logout 按钮
        self.button_logout = tk.Button(self, text="Logout", font=custom_font,
                                    relief="flat", borderwidth=0, highlightthickness=0,
                                    bg="#7EFFF7", fg="black", activebackground="#7EFFF7", activeforeground="blue",
                                    command=self.logout)
        self.button_logout.place(x=last_button_x, y=0, width=button_width, height=button_height)

    # def create_navbar(self):
    #     # 创建导航按钮等
    #     pass
    def logout(self):
        if messagebox.askyesno("Logout","Do you really want to logout?"):
            self.destroy()
            create_login_window()

    def show_page(self, page_name):
        # 隐藏所有页面，显示指定页面
        # print(f"Showing page :{page_name}")
        for page in self.pages.values():
            page.place_forget()
        self.pages[page_name].place(x=0, y=0)

if __name__ == '__main__':
    create_login_window()
    # app.mainloop()

