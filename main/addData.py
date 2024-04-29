import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

ref = db.reference('publicPersonality')

data = {
    "1": {
        "name": "Kamel Baddari",
        "job": "Ministre de l'Enseignement Supérieur",
        "total_Attendance": 3,
    },
    "2": {
        "name": "Issad Rebrab",
        "job": "Homme d'affaires",
        "total_Attendance": 0,
    },
    "3": {
        "name": "Abdelmadjid Tebboune",
        "job": "Président de l'Algérie",
        "total_Attendance": 0,
    },
    "4": {
        "name": "Hillary Clinton",
        "job": "Politicienne",
        "total_Attendance": 0,
    },
    "5": {
        "name": "Yasmina Khadra",
        "job": "Écrivain",
        "total_Attendance": 0,
    },
    "6": {
        "name": "Elon Musk",
        "job": "Entrepreneur",
        "total_Attendance": 0,
    },
    "7": {
        "name": "Rachid Nekaz",
        "job": "Militant",
        "total_Attendance": 0,
    }
}

# Update the data dictionary with French names and jobs
for key, value in data.items():
    ref.child(key).update(value)


