import os
import tkinter as tk
from tkinter import Scrollbar, Listbox, Frame, font

def list_files():
    directory = "main/rapport"  # Change this to your desired directory
    files = os.listdir(directory)
    files_without_extension = [file[:-4] for file in files if file.endswith('.txt')]
    return files_without_extension

def on_select(event):
    selected_index = listbox.curselection()[0]
    selected_file = listbox.get(selected_index)
    file_path = os.path.join("main/rapport", selected_file + ".txt")  # Add .txt extension back
    os.system(f'start "" "{file_path}"')

def update_listbox():
    files = list_files()
    listbox.delete(0, tk.END)
    for file in files:
        listbox.insert(tk.END, file)

root = tk.Tk()
root.title("rapport")

frame = Frame(root)
frame.pack()

listbox_font = font.Font(family="Helvetica", size=15)  # Change font and size as needed
listbox = Listbox(frame, width=50, height=5, bg="white", fg="#2247CC", font=listbox_font)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

update_listbox()

listbox.bind('<<ListboxSelect>>', on_select)

root.mainloop()
