import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://tvapp-d8049-default-rtdb.firebaseio.com/",
    'storageBucket':"tvapp-d8049.appspot.com"  # Corrected parameter name
})

folderpath = 'images'
Pathlist = os.listdir(folderpath)
imgList = []
publicIDS = []

# Initialize Firebase Storage bucket
bucket = storage.bucket()

for path in Pathlist:
    img = cv2.imread(os.path.join(folderpath, path))
    if img is not None:
        imgList.append(img)
        publicIDS.append(os.path.splitext(path)[0])

        # Upload image to Firebase Storage
        blob = bucket.blob(f'{folderpath}/{path}')
        blob.upload_from_filename(os.path.join(folderpath, path))

def findEncoding(imageList):
    encodeList = []
    for img in imageList:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Encode face if detected
        face_encodings = face_recognition.face_encodings(img_rgb)
        if face_encodings:
            encodeList.append(face_encodings[0])
        else:
            print(f"No face detected in image: {img}")
    return encodeList

print("Encoding started...")
encodeListKnown = findEncoding(imgList)
encodeListKnownwithIDS = [encodeListKnown, publicIDS]
print("Encoding complete")

# Save encoded data to file
with open("encodeFile.p", "wb") as file:
    pickle.dump(encodeListKnownwithIDS, file)
print("File saved")
