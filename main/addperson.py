from tkinter import *
from tkinter import filedialog
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

ref = db.reference('publicPersonality')


def get_image_path():
    """Opens a file dialog to select an image."""
    image_path = filedialog.askopenfilename(
        initialdir="/", title="Select Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
    )
    if image_path:
        image_path_var.set(image_path)  # Set the image path in the StringVar
        print(image_path)
    else:
        message_label.config(text="Please select an image.", fg="red")

def save_user_info():
    """Retrieves form data, generates a filename based on index, and saves information."""
    name = name_entry.get()
    job = job_entry.get()
    image_path = image_path_var.get()  # Get the image path from StringVar
    print(image_path)
    if not name or not job or not image_path:
        message_label.config(text="Please fill in all fields.", fg="red")
        return

    # Get the latest image index or start from 1 if no images exist
    latest_index = 0
    for filename in os.listdir("images"):
        latest_index=latest_index+1
    print(latest_index)
    # Generate new filename with incremented index (adjust extension as needed)
    new_filename = f"images/{latest_index }.jpg"  # Adjust extension based on image type

    try:
        # Copy the image to the "images" folder
        with open(new_filename, "wb") as image_file:
            with open(image_path, "rb") as f:
                image_file.write(f.read())
        message_label.config(text="Information saved successfully!", fg="green")

    except FileNotFoundError:
        message_label.config(text="Error: Could not find the selected image.", fg="red")
    except PermissionError:
        message_label.config(text="Error: Insufficient permissions to save the image.", fg="red")
    except Exception as e:  # Catch other potential errors
        message_label.config(text=f"Error: {e}", fg="red")
    
    user_info = {
        "name": name,
        "job": job,
          # Store the image path as well
        "total_attendance": 0,
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
window.title("User Information Form")
# Name label and entry
name_label = Label(window, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)

name_entry = Entry(window, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Job label and entry
job_label = Label(window, text="Job:")
job_label.grid(row=1, column=0, padx=5, pady=5)

job_entry = Entry(window, width=30)
job_entry.grid(row=1, column=1, padx=5, pady=5)

# Image selection button
image_path_var = StringVar()  # To store the image path
image_button = Button(window, text="Select Image", command=get_image_path)
image_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Message label for success or error messages
message_label = Label(window, text="")
message_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Submit button
submit_button = Button(window, text="Submit", command=save_user_info)
submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()

