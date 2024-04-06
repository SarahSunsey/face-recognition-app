import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

ref = db.reference('publicPersonality')

data = {
    "1": {
        "name": "Kamel Baddari",
        "job": "Minister of Higher Education",
        "total_Attendance": 0,
    },
    "2": {
        "name": "Issad Rebrab",
        "job": "Businessman",
        "total_Attendance": 0,
    },
    "3": {
        "name": "Abdelmadjid Tebboune",
        "job": "President of Algeria",
        "total_Attendance": 0,
    }
}

# Add new entries to the data dictionary
data["4"] = {
    "name": "Hilary Clinton",
    "job": "Politician",
    "total_Attendance": 0,
}

data["5"] = {
    "name": "Yasmina Khedra",
    "job": "Writer",
    "total_Attendance": 0,
}

data["6"] = {
    "name": "Elon Musk",
    "job": "Entrepreneur",
    "total_Attendance": 0,
}

data["7"] = {
    "name": "Rachid Nekaz",
    "job": "Activist",
    "total_Attendance": 0,
}


for key,value in data.items():
    ref.child(key).set(value)