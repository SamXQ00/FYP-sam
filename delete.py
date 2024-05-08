import os
import shutil
from tkinter import messagebox

def delete_resources():
    files_to_delete = ['/home/sam/Desktop/signlanguage/model.h5', '/home/sam/Desktop/signlanguage/model.tflite']
    directory_to_delete = '/home/sam/Desktop/signlanguage/Logs'

    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted file: {file}")
        else:
            print(f"File not found: {file}")

    if os.path.exists(directory_to_delete):
        shutil.rmtree(directory_to_delete)
        print(f"Deleted directory: {directory_to_delete}")
    else:
        print(f"Directory not found: {directory_to_delete}")
        
def delete_resources_gui():
    try:
        delete_resources()
        messagebox.showinfo("Success", "Resources deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))