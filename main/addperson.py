from tkinter import *
from tkinter import filedialog
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter as tk

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

ref = db.reference('publicPersonality')


def get_image_path():
    """Opens a file dialog to select an image."""
    image_path = filedialog.askopenfilename(
        initialdir="/", title="Sélectionner une image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
    )
    if image_path:
        image_path_var.set(image_path)  # Set the image path in the StringVar
        print(image_path)
    else:
        message_label.config(text="Veuillez sélectionner une image.", fg="red")

def save_user_info():
    """Retrieves form data, generates a filename based on index, and saves information."""
    name = name_entry.get()
    job = job_entry.get()
    image_path = image_path_var.get()  # Get the image path from StringVar
    print(image_path)
    if not name or not job or not image_path:
        message_label.config(text="Veuillez remplir tous les champs.", fg="red")
        return

    # Get the latest image index or start from 1 if no images exist
    latest_index =0
    for filename in os.listdir("images"):
        # Check if the filename is a number
        try:
            number = int(filename.split(".")[0])  # Extract number before extension
            if number > latest_index:
                latest_index = number
        except ValueError:
            pass  # Ignore non-numeric filenames
    latest_index+=1
    print(latest_index)
    # Generate new filename with incremented index (adjust extension as needed)
    new_filename = f"images/{latest_index }.jpg"  # Adjust extension based on image type

    try:
        # Copy the image to the "images" folder
        with open(new_filename, "wb") as image_file:
            with open(image_path, "rb") as f:
                image_file.write(f.read())
        message_label.config(text="Les informations ont été enregistrées avec succès !", fg="green")

    except FileNotFoundError:
        message_label.config(text="Error: Could not find the selected image.", fg="red")
    except PermissionError:
        message_label.config(text="Error: Insufficient permissions to save the image.", fg="red")
    except Exception as e:  # Catch other potential errors
        message_label.config(text=f"Error: {e}", fg="red")
    
    user_info = {
        "name": name,
        "job": job,
        "total_Attendance": 0,
        "date":"",
    }

    next_key = latest_index   # Call the get_highest_key function

    # Push the user information to Firebase under the calculated key
    try:
        ref.child(str(next_key)).set(user_info)
        # Update the database with the user information under the generated key
        
        message_label.config(text="Information saved successfully!", fg="green")

    except Exception as e:
        message_label.config(text=f"Error saving data: {e}", fg="red")

# Create the main window
window = Tk()
window.configure(bg='#5678F0')
window.title("Ajouter une personne")
icon_image = tk.PhotoImage(file='main/logoAPP.png')
window.iconphoto(True, icon_image)
# Name label and entry
def set_styles():
    # Label style
    label_style = {'font': ('Arial', 17), 'fg': 'white', 'bg': '#5678F0', 'padx': 10, 'pady': 5}

    # Entry style
    entry_style = {'font': ('Arial', 17), 'fg': 'white', 'bg': '#5678F0', 'width': 25, 'borderwidth': 2}

    return label_style, entry_style

# Function to create and grid labels
def create_and_grid_labels(label_text, row_num, col_num):
    label_style, _ = set_styles()
    label = tk.Label(window, text=label_text, **label_style)
    label.grid(row=row_num, column=col_num, sticky='w', padx=5, pady=5)

# Function to create and grid entry widgets
def create_and_grid_entry(row_num, col_num):
    _, entry_style = set_styles()
    entry = tk.Entry(window, **entry_style)
    entry.grid(row=row_num, column=col_num, padx=5, pady=5)
    return entry

# Create and grid labels and entry widgets
create_and_grid_labels("Nom Complet:", 0, 0)
name_entry = create_and_grid_entry(0, 1)

create_and_grid_labels("Metier:", 1, 0)
job_entry = create_and_grid_entry(1, 1)

# Image selection button
image_path_var = StringVar()  # To store the image path
image_button = Button(window, text="Choisir image", command=get_image_path, bg="#82EE5C")
image_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Message label for success or error messages
message_label = Label(window, text="",bg="#5678F0")
message_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Submit button
submit_button = tk.Button(window, text="Soumettre",width="20", command=save_user_info, bg="#82EE5C", fg="black")  # Set background color to blue and foreground (text) color to white
submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()

