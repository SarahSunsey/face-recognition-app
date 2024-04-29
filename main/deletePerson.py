import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import messagebox
import os

# Initialize Firebase app
cred = credentials.Certificate("main/serviceAccountkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

def fetch_data_by_id(person_id):
    try:
        ref = db.reference(f'publicPersonality/{person_id}')
        person_data = ref.get()
        if person_data:
            return person_data.get('name', 'Name not found')
        else:
            return 'Person not found'
    except Exception as e:
        return f'Error: {e}'

def delete_data_by_id(person_id):
    try:
        ref = db.reference(f'publicPersonality/{person_id}')
        person_data = ref.get()
        if person_data:
            confirm = messagebox.askquestion("Confirm Deletion", f"Are you sure you want to delete {person_data.get('name')}?")
            if confirm == 'yes':
                ref.delete()
                # Delete image file
                image_path = f'images/{person_id}.jpg'
                if os.path.exists(image_path):
                    os.remove(image_path)
                    return f"Data for {person_data.get('name')} and image deleted successfully!"
                else:
                    return f"Data for {person_data.get('name')} deleted from Firebase, but image not found locally."
            else:
                return "Deletion cancelled."
        else:
            return 'Person not found'
    except Exception as e:
        return f'Error: {e}'

def fetch_button_clicked():
    person_id = id_entry.get().strip()
    name = fetch_data_by_id(person_id)
    result_label.config(text=f"Name: {name}")

def delete_button_clicked():
    person_id = id_entry.get().strip()
    result = delete_data_by_id(person_id)
    messagebox.showinfo("Deletion Result", result)

# Create GUI window
window = tk.Tk()
window.configure(bg='#5678F0')
window.title("Suprimmer personne")
icon_image = tk.PhotoImage(file='main/logoAPP.png')
window.iconphoto(True, icon_image)

# Create ID input field
id_label = tk.Label(window, text="Entrez ID de la personne que vous souhaitez supprimer :",width="60",bg="#5678F0",fg="white",font=(20))
id_label.pack()
id_entry = tk.Entry(window, width=10,font=20)
id_entry.pack()

# Create buttons for fetch and delete operations
fetch_button = tk.Button(window, text="Récupérer le nom", command=fetch_button_clicked,width=20)
fetch_button.pack(pady=20)

delete_button = tk.Button(window, text="Supprimer les données", command=delete_button_clicked)
delete_button.pack(pady=10)

# Create label to display result
result_label = tk.Label(window, text="", font=("Helvetica", 12))
result_label.pack(pady=20)

# Run the main GUI event loop
window.mainloop()
