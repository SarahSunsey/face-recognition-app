import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import webbrowser  # Import webbrowser module to open webpages

# Define the coordinates and button texts
button_data = [
    (820, 270, "Ajouter personne"),
    (300, 270, "Afficher bases de données"),  # Target button
    (300, 540, "Supprimer personne"),
    (820, 540, "Afficher rapport")
]


# Function to handle button hover enter event
def on_enter(event):
    event.widget.config(bg="#2247CC", cursor="hand2")


# Function to handle button hover leave event
def on_leave(event):
    event.widget.config(bg="#4165E3", cursor="arrow")


# Function to create styled buttons on canvas and handle button click
def create_buttons_on_canvas(canvas):
    for (x, y, text) in button_data:
        # Create button with custom style
        button = tk.Button(canvas, text=text, width=25, height=2, font=("Helvetica", 16), bg="#4165E3", fg="white")

        # Bind hover events to buttons
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        # Check if the button text matches the target action
        if text == "Afficher bases de données":
            def open_bdd_html():
                # Replace with the actual URL of your bdd.html file (if hosted online)
                bdd_html_url = "http://127.0.0.1:5500/main/bdd.html"  # Modify as needed
                webbrowser.open(bdd_html_url)

            # Bind the click action to the button
            button.config(command=open_bdd_html)
        if text == "Ajouter personne":
            def open_add_person_script():
                subprocess.run(["python", "main/addperson.py"])

            button.config(command=open_add_person_script)
            
        elif text == "Supprimer personne":
            def open_delete_person_script():
                subprocess.run(["python", "main/deletePerson.py"])

            button.config(command=open_delete_person_script)
        elif text == "Afficher rapport":
            def open_delete_person_script():
                subprocess.run(["python", "main/rapport.py"])

            button.config(command=open_delete_person_script)
        button_window = canvas.create_window(x, y, anchor='nw', window=button)

        # Add the button to the canvas
        button_window = canvas.create_window(x, y, anchor='nw', window=button)


# Main function to create the GUI
def main():
    # Create main window
    root = tk.Tk()
    root.title("Prametres")
    icon_image = tk.PhotoImage(file='main/logoAPP.png')
    root.iconphoto(True, icon_image)

    # Load the background image
    image_path = "main/Group 19.png"  # Replace this with your image path
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
