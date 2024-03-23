import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://tvapp-d8049-default-rtdb.firebaseio.com/"
})

ref = db.reference('publicPersonality')

data={

    "1":{
        #key : value
        "name": "Kamel Baddari",
        "job" : "minister of higher education" ,
        "total_Attandance" :0,

    },
    "2":{
        #key : value
        "name": "Issad Rebrab",
        "job" : "Buisnessmen" ,
        "total_Attandance" :0,

    },
    "3":{
        #key : value
        "name": "Abdelmadjid Tebboune",
        "job" : "President of algeria" ,
        "total_Attandance" :0,

    },
    "3":{
        #key : value
        "name": "Abdelmadjid Tebboune",
        "job" : "President of algeria" ,
        "total_Attandance" :0,

    }
}
for key,value in data.items():
    ref.child(key).set(value)