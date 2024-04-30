from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage,ttk, messagebox
import sqlite3
import tkinter as tk

def load_data(tree):
    try:
        conn = sqlite3.connect('/home/sam/Desktop/signlanguage/dbtest.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.id, users.username, users.email, video_status.video_name, video_status.status
            FROM users
            JOIN video_status ON users.id = video_status.user_id
        """)
        rows = cursor.fetchall()
        # tree.delete(*tree.get_children())  # This line clears the tree view
        for row in rows:
            tree.insert("", 'end', values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
def search(search_entry, tree):
    search = search_entry.get()

    # status = search_status.get()
    try:
        conn = sqlite3.connect('/home/sam/Desktop/signlanguage/dbtest.db')
        cursor = conn.cursor()
        cursor.execute("SELECT users.id, users.username, users.email, video_status.video_name, video_status.status\
                        FROM users JOIN video_status ON users.id = video_status.user_id\
                            WHERE users.username LIKE ? ",('%' +search +'%', ))
        rows = cursor.fetchall()
        refresh(tree)
        # tree.delete(*tree.get_children())  # This line clears the tree view
        for row in rows:
            tree.insert("", 'end', values=row)
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

def searchstatus(search_status, tree):
    search = search_status.get()

    # status = search_status.get()
    try:
        conn = sqlite3.connect('/home/sam/Desktop/signlanguage/dbtest.db')
        cursor = conn.cursor()
        cursor.execute("SELECT users.id, users.username, users.email, video_status.video_name, video_status.status\
                        FROM users JOIN video_status ON users.id = video_status.user_id\
                            WHERE video_status.status LIKE ? ",('%' +search +'%', ))
        rows = cursor.fetchall()
        refresh(tree)
        # tree.delete(*tree.get_children())  # This line clears the tree view
        for row in rows:
            tree.insert("", 'end', values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")


def refresh(tree):
    for i in tree.get_children():
        tree.delete(i)

def delete_user(username_entry, tree):
    username = username_entry.get()
    if not username:
        messagebox.showwarning("Warning", "Please enter a username to delete.")
        return

    try:
        conn = sqlite3.connect('/home/sam/Desktop/signlanguage/dbtest.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM video_status WHERE user_id IN (SELECT id FROM users WHERE username = ?)", (username,))
        # print(f"Deleted {cursor.rowcount} rows from video_status")

        # Now delete from users
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        # print(f"Deleted {cursor.rowcount} rows from users")
        # cursor.execute("DELETE FROM users JOIN video_status ON users.id = video_status.user_id WHERE username = ? ", (username,))
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()

        if affected_rows == 0:
            messagebox.showinfo("Info", "No user found with that username.")
        else:
            messagebox.showinfo("Success", "User deleted successfully.")
            refresh(tree)
            load_data(tree)  # Refresh the treeview after deletion
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        if conn:
            conn.close()

def userdetail(parent):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("/home/sam/Desktop/signlanguage/GUI/assets/frame0/")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    canvas = Canvas(
        parent,
        bg="#7EFFF7",
        height=650,
        width=950,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        228.0,
        0.0,
        950.0,
        650.0,
        fill="#76CDFF",
        outline=""
    )
    canvas.create_rectangle(
        228.0,
        0.0,
        950.0,
        70.0,
        fill="#7EFFF7",
        outline="")

    # 保存PhotoImage引用
    canvas.images = []  # 创建一个属性来保持对图像的引用

    # 创建并保存第一张图片
    image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.images.append(image_1)  # 将图片保存到列表中
    canvas.create_image(
        208.0,
        469.0,
        image=image_1
    )

    # 创建并保存第二张图片
    image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.images.append(image_2)
    canvas.create_image(
        111.0,
        103.0,
        image=image_2
    )
    canvas.create_text(
        50.0,
        278.0,
        anchor="nw",
        text="Welcome Admin!",
        fill="#0083AC",
        font=("Inter Bold", 20 * -1)
    )

    canvas.create_text(
        524.0,
        134.0,
        anchor="nw",
        text="User Information",
        fill="#000000",
        font=("Inter Bold", 20 * -1)
    )
    username_entry = tk.Entry(canvas)
    username_entry.place(x=420, y=500, width=150)
    canvas.create_text(420.0,480.0,anchor="nw",text="Entry username to delete users:",fill="gray",font=("Inter Bold", 12 * -1))
    # ????
    delete_btn = tk.Button(canvas, text="Delete User", command=lambda: delete_user(username_entry, tree))
    delete_btn.place(x=600, y=500, width=100)

    canvas.create_text(420.0,400.0,anchor="nw",text="Entry username:     Enter Status:",fill="gray",font=("Inter Bold", 12 * -1))
    search_entry = tk.Entry(canvas)
    search_entry.place(x=420,y=420, width=100)
    search_status = tk.Entry(canvas)
    search_status.place(x=520,y=420, width=100)

    search_btn = tk.Button(canvas, text="filter_name", command=lambda: search(search_entry,tree))
    search_btn.place(x=640,y=420, width=80)
    search_status_btn =tk.Button(canvas, text="filter_status", command=lambda: searchstatus(search_status,tree))
    search_status_btn.place(x=720,y=420, width=80)

    tree_frame = tk.Frame(canvas)
    tree_frame.place(x=415, y=182, width=440, height=205)

    tree_scroll_y = tk.Scrollbar(tree_frame, orient='vertical')
    tree_scroll_x = tk.Scrollbar(tree_frame, orient='horizontal')

    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Action", "Status"), show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)
    tree_scroll_y.pack(side='right', fill='y')
    tree_scroll_x.pack(side='bottom', fill='x')
    tree.pack(side="left", fill="both", expand=True)

    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Email', text='Email')
    tree.heading('Action', text='Action')
    tree.heading('Status', text='Status')
    # tree.delete(*tree.get_children())  # This line clears the tree view
    load_data(tree)  # Function to load data into the treeview
    return canvas
