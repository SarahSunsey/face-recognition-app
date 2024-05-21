import tkinter as tk
from PIL import Image, ImageTk
import subprocess

def start_main_page():
    # Start the Mainpage.py script
    subprocess.Popen(["python", "main/Mainpage.py"])

def on_button_click(event):
    # Check if the click event occurs within the button coordinates
    x, y = event.x, event.y
    if 473 <= x <= 802 and 58 <= y <= 585:
        start_main_page()

# Create a Tkinter window
root = tk.Tk()
root.title("AlgerieVision")

# Load the background image
background_image = Image.open("main/menu.png")
photo = ImageTk.PhotoImage(background_image)

# Create a canvas to display the image
canvas = tk.Canvas(root, width=background_image.width, height=background_image.height)
canvas.pack()

# Display the background image
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Create a transparent button
button = canvas.create_rectangle(473, 58, 802, 585, fill="", outline="")
canvas.tag_bind(button, "<Button-1>", on_button_click)

# Set cursor to pointer when hovering over the button
canvas.config(cursor="hand2")
icon_image = tk.PhotoImage(file='main/logoAPP.png')
root.iconphoto(True, icon_image)

root.mainloop()
