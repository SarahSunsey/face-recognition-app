import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from deepface import DeepFace

def select_image(image_num):
    filename = filedialog.askopenfilename(title="Select Image")
    if filename:
        if image_num == 1:
            img1_path.set(filename)
            display_image(img1, filename)
        else:
            img2_path.set(filename)
            display_image(img2, filename)

def display_image(label, filename):
    img = Image.open(filename)
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def verify_images():
    img1_filename = img1_path.get()
    img2_filename = img2_path.get()

    if img1_filename and img2_filename:
        try:
            result = DeepFace.verify(img1_path=img1_filename, img2_path=img2_filename)
            messagebox.showinfo("Result", f"Verified: {result['verified']}\nDistance: {result['distance']}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Error", "Please select two images")

# Create GUI
root = tk.Tk()
root.title("Face Verification")

# Image 1
img1_path = tk.StringVar()
img1 = tk.Label(root)
img1.grid(row=0, column=0)
tk.Button(root, text="Select Image 1", command=lambda: select_image(1)).grid(row=1, column=0)

# Image 2
img2_path = tk.StringVar()
img2 = tk.Label(root)
img2.grid(row=0, column=1)
tk.Button(root, text="Select Image 2", command=lambda: select_image(2)).grid(row=1, column=1)

# Verify Button
tk.Button(root, text="Verify Images", command=verify_images).grid(row=2, columnspan=2)

root.mainloop()
