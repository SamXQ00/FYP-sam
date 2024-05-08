
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from navbar_menu import *
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sqlite3
import tkinter as tk
# from collecting import *
# from delete import *
# from preprocess_data import *
from test_real import *
import threading
def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("/home/sam/Desktop/signlanguage/GUI/assets/frame0")
    return ASSETS_PATH / Path(path)

def collection_page(parent):
    canvas = Canvas(parent,bg = "#7EFFF7",height = 650,width = 950,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(228.0,0.0,950.0,650.0,fill="#76CDFF",outline="")
    canvas.images = []
    image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.images.append(image_1)
    image_1 = canvas.create_image(208.0,469.0,image=image_1)
    canvas.create_rectangle(228.0,0.0,950.0,70.0,fill="#7EFFF7",outline="")

    image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.images.append(image_2)
    image_2 = canvas.create_image(111.0,103.0,image=image_2)
    # image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    # canvas.images.append(image_3)
    # image_3 = canvas.create_image(119.0,274.0,image=image_3)
 
    canvas.create_text(400.0,300.0,anchor="nw",text="Note: This test real are using OpenCv windows.",fill="red",font=("Inter Bold", 16 * -1))
    # canvas.create_text(450.0,370.0,anchor="nw",text="    Please do not close the application until finished. ",fill="red",font=("Inter Bold", 16 * -1))
    # canvas.create_text(440.0,390.0,anchor="nw",text="2) Delete the previous model before training new model. ",fill="red",font=("Inter Bold", 16 * -1))
    # canvas.create_text(440.0,410.0,anchor="nw",text="3) Make sure accuracy greater than 80%",fill="red",font=("Inter Bold", 16 * -1))
    canvas.create_text(524.0,135.0,anchor="nw",text="Test-real",fill="#000000",font=("Inter Bold", 20 * -1))
    button_image_start = PhotoImage(file=relative_to_assets("button_start_test.png"))
    canvas.images.append(button_image_start)
    button_start_test = Button(canvas,image=button_image_start,borderwidth=0,highlightthickness=0,command=lambda: start_test(),relief="flat")
    button_start_test.place(x=485.0,y=200.0,width=213.0,height=50.0)
    # create_nav_buttons(canvas)
    return canvas
    # create_nav_buttons(canvas)
    # window.resizable(False, False)
    # window.mainloop()
   # canvas.create_text(524.0,130.0,anchor="nw",text="Collect Data",fill="#000000",font=("Inter Bold", 20 * -1))
    # canvas.create_text(524.0,
    #     250.0,
    #     anchor="nw",
    #     text="Train Model",
    #     fill="#000000",
    #     font=("Inter Bold", 20 * -1)
    # )

    # entry_image_1 = PhotoImage(
    #     file=relative_to_assets("entry_collect.png"))
    # canvas.images.append(entry_image_1)
    # entry_bg_1 = canvas.create_image(
    #     536.0,
    #     198.0,
    #     image=entry_image_1
    # )
    # entry_collect = Entry(
    #     bd=0,
    #     bg="#FFFFFF",
    #     fg="#000716",
    #     highlightthickness=0
    # )
    # entry_collect.place(
    #     x=388.0,
    #     y=180.0,
    #     width=296.0,
    #     height=38.0
    # )

    # canvas.create_text(
    #     388.0,
    #     158.0,
    #     anchor="nw",
    #     text="Enter action: ",
    #     fill="#000000",
    #     font=("Inter ExtraLight", 15 * -1)
    # )

    # button_image_1 = PhotoImage(
    #     file=relative_to_assets("button_start.png"))
    # canvas.images.append(button_image_1)
    # button_start = Button(
    #     image=button_image_1,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: on_start(entry_collect),
    #     relief="flat"
    # )
    # button_start.place(
    #     x=720.0,
    #     y=180.0,
    #     width=143.0,
    #     height=40.0
    # )
    # button_stop = Button(
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: stop_camera(canvas),
    #     relief="flat"
    # )
    # button_stop.place(
    #     x=830.0,
    #     y=180.0,
    #     width=143.0,
    #     height=40.0
    # )
    # button_delete = PhotoImage(
    #     file=relative_to_assets("button_delete.png"))
    # canvas.images.append(button_delete)  # 将图片保存到列表中
    # button_delete = Button(
    #     canvas,
    #     image=button_delete,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: delete_resources_gui(),
    #     relief="flat"
    # )
    # button_delete.place(
    #     x=396.0,
    #     y=280.0,
    #     width=87.0,
    #     height=47.0
    # )

    # button_train = PhotoImage(
    #     file=relative_to_assets("button_train.png"))
    # canvas.images.append(button_train)  # 将图片保存到列表中
    # button_train = Button(
    #     canvas,
    #     image=button_train,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: start_train(canvas),
    #     relief="flat"
    # )
    # button_train.place(
    #     x=562.0,
    #     y=280.0,
    #     width=87.0,
    #     height=47.0
    # )

    # button_accuracy = PhotoImage(
    #     file=relative_to_assets("button_accuracy.png"))
    # canvas.images.append(button_accuracy)  # 将图片保存到列表中
    # button_accuracy = Button(
    #     canvas,
    #     image=button_accuracy,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: run_accuracy_check(),
    #     relief="flat"
    # )
    # button_accuracy.place(
    #     x=735.0,
    #     y=280.0,
    #     width=87.0,
    #     height=47.0
    # )
    # canvas.create_rectangle(
    #     396.0,
    #     300.0,
    #     822.0,
    #     430.0,
    #     fill="#D9D9D9",
    #     outline="")
