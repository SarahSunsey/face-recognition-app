import tkinter as tk
from PIL import Image, ImageTk

# Define the coordinates and button texts
button_data = [
    (820, 270, "Ajouter personne"),
    (300, 270, "Afficher bases de données"),
    (300, 540, "Supprimer personne"),
    (820, 540, "Afficher rapport")
]

# Function to handle button hover enter event
def on_enter(event):
    event.widget.config(bg="#2247CC", cursor="hand2")

# Function to handle button hover leave event
def on_leave(event):
    event.widget.config(bg="#4165E3", cursor="arrow")

# Function to create styled buttons on canvas
def create_buttons_on_canvas(canvas):
    for (x, y, text) in button_data:
        # Create button with custom style
        button = tk.Button(canvas, text=text, width=25,height=2, font=("Helvetica", 16), bg="#4165E3", fg="white")
        button_window = canvas.create_window(x, y, anchor='nw', window=button)

        # Bind hover events to buttons
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# Main function to create the GUI
def main():
    # Create main window
    root = tk.Tk()
    root.title("Background Image with Buttons")

    # Load the background image
    image_path = "main/parameterPAGE.png"  # Replace this with your image path
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create canvas widget
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()

    # Display the background image
    canvas.create_image(0, 0, image=photo, anchor='nw')

    # Create styled buttons on canvas
    create_buttons_on_canvas(canvas)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
