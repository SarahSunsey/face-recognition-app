import tkinter as tk
import subprocess

# Mapping of hotspot numbers to names
hotspot_names = {
    1: "Faces2",
    2: "elnahar",
    3: "elchourouk",
    4: "elbilad"
}

def on_hotspot_click(button_num):
    # Get the hotspot name based on the button_num
    if button_num in hotspot_names:
        hotspot_name = hotspot_names[button_num]
        # Launch main.py with hotspot_name as argument using subprocess
        launch_main_with_hotspot(hotspot_name)

def launch_main_with_hotspot(hotspot_name):
    # Command to run main.py with hotspot_name as argument
    cmd = ["python", "main/main.py", hotspot_name]
    subprocess.Popen(cmd)

def set_hover_effect(event):
    canvas.config(cursor="hand2")

def unset_hover_effect(event):
    canvas.config(cursor="")

def on_image_click(event):
    print("Image button clicked!")
    # Launch parameter.py using subprocess
    launch_parameter()

def launch_parameter():
    # Command to run parameter.py
    cmd = ["python", "main/parameter.py"]
    subprocess.Popen(cmd)

# Create main window
window = tk.Tk()
window.title("Transparent Hotspots")

# Load the image containing clickable areas
image_path = "main/page.png"
image = tk.PhotoImage(file=image_path)

# Create a canvas widget to display the image
canvas = tk.Canvas(window, width=image.width(), height=image.height())
canvas.pack()

# Display the image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=image)

# Define hotspot positions (x, y) and dimensions (width, height)
hotspot_positions = [
    (690, 257, 949, 369),  # Hotspot 1 (x1, y1, x2, y2)
    (333, 257, 592, 369),  # Hotspot 2 (x1, y1, x2, y2)
    (690, 509, 949, 621),  # Hotspot 3 (x1, y1, x2, y2)
    (333, 509, 592, 621)   # Hotspot 4 (x1, y1, x2, y2)
]

# Create transparent hotspots on the canvas
for i, (x1, y1, x2, y2) in enumerate(hotspot_positions, start=1):
    hotspot_tag = f"hotspot{i}"
    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="", tags=hotspot_tag)

    # Bind events for hotspot hover effect
    canvas.tag_bind(hotspot_tag, '<Enter>', set_hover_effect)
    canvas.tag_bind(hotspot_tag, '<Leave>', unset_hover_effect)
    canvas.tag_bind(hotspot_tag, '<ButtonPress-1>', lambda event, num=i: on_hotspot_click(num))

# Define the path to the image you want to display as a button
image_file_path = "main/parameter.png"

# Load the image to be displayed on specific coordinates
additional_image = tk.PhotoImage(file=image_file_path)

# Coordinates where you want to place the image
image_x, image_y = 1100, 48

# Create the image on the canvas at the specified coordinates
image_button_tag = "image_button"
canvas.create_image(image_x, image_y, anchor=tk.NW, image=additional_image, tags=image_button_tag)

# Bind events for image hover effect
canvas.tag_bind(image_button_tag, '<Enter>', set_hover_effect)
canvas.tag_bind(image_button_tag, '<Leave>', unset_hover_effect)
canvas.tag_bind(image_button_tag, '<ButtonPress-1>', on_image_click)

# To prevent the image from being garbage collected, store it as an attribute of the canvas
canvas.additional_image = additional_image

# Run the application
window.mainloop()
