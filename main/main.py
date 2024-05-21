from mtcnn import MTCNN
import cv2
import os
import pickle
import numpy as np
import face_recognition  # Ensure face_recognition is properly installed
import firebase_admin
from firebase_admin import db
import cvzone
import os
import sys
from firebase_admin import storage
from firebase_admin import credentials
import re

timer=0
strr=""
cred = credentials.Certificate("main/serviceAccountkey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://tvapp-d8049-default-rtdb.firebaseio.com/",
    'storageBucket':"tvapp-d8049.appspot.com"  # Corrected parameter name
})
bucket = storage.bucket()

print("Number of arguments:", len(sys.argv))
print("Arguments:", sys.argv)

#get name video
if len(sys.argv) > 1:
    hotspot_name = sys.argv[1]
    print(f"Received hotspot name: {hotspot_name}")
    # Use the hotspot_name as needed in your application logic
else:
    print("No hotspot name provided.")

detector = MTCNN()


def extract_date_time(filename):
  
  try:
    # Split the filename based on delimiters
    
    parts = filename.split("-")
    
    day=parts[0]
    month=parts[1]
    year=parts[2]
    hour=parts[3]
    minute=parts[4]
    print(day,month,year,hour,minute)
    return day,month,year,hour,minute
  except ValueError:
    return "Invalid filename format"  # Handle format errors
# Open the video file
video_path = f'main/TV/{hotspot_name}.mp4'
day, month, year, hour, minute = extract_date_time(hotspot_name)
print(day,month,year,hour,minute)
cap = cv2.VideoCapture(video_path)
imgpublic=[]
# Read the background image
imgBackground = cv2.imread('recources/background.png')
frame_rate = cap.get(cv2.CAP_PROP_FPS)
# Import images into a list
folderModepath = 'recources/modes'
modePathlist = os.listdir(folderModepath)
imgModeList = [cv2.imread(os.path.join(folderModepath, path)) for path in modePathlist]


# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, Publicids = encodeListKnownWithIds
print("Encode File Loaded")

frame_skip = 10  # Process every 10th frame
resize_factor = 0.8  # Resize frames to 80% of their original size
frame_count = 0
modeType = 0
output_file_path = ""
counter =0
x=0
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break
    
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Resize frame
    frame_resized = cv2.resize(frame, (640, 480))  # Resize to match the target region size

    # Convert frame to RGB (MTCNN expects RGB format)
    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    # Detect faces using MTCNN
    faces = detector.detect_faces(rgb_frame)
    # Replace the region in imgBackground with the resized frame
    
    for face in faces:
        x, y, w, h = face['box']
        x, y, w, h = int(x), int(y), int(w), int(h)  # Convert coordinates to integers
        
        # Draw bounding box around the face
        cv2.rectangle(frame_resized, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Extract face from the original frame
        face_img = frame_resized[y:y+h, x:x+w]

        # Perform face recognition
        face_img = cv2.resize(face_img, (128, 128))  # Resize for consistency with encoding
        face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(face_img_rgb)
        

        if len(face_encodings) > 0:
            encodeFace = face_encodings[0]

            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            
            # Print the current time when a face is matched
            matchindex = np.argmin(faceDis)
            if matches[matchindex]:
                if timer==0:
                    print (matchindex)
                                # Calculate total time in seconds
                    total_time_seconds = (float(hour) * 3600) + (float(minute) * 60) + (frame_count / frame_rate)
                    
                    # Calculate hours, minutes, and remaining seconds
                    matched_hours = int(total_time_seconds // 3600)
                    matched_minutes = int((total_time_seconds % 3600) // 60)
                    strr=str(matched_hours) + '.' + str(matched_minutes)
                    
                    matched_seconds = total_time_seconds % 60
                    
                    print("Matched at {:02d}:{:02d}:{:.2f}.".format(matched_hours, matched_minutes, matched_seconds))
                    publicInfo = db.reference(f'publicPersonality/{matchindex+1}').get()
                    print(publicInfo)
                    strr= float(strr)
                    timer=1
                if timer==1:
                    total_time_seconds = (float(hour) * 3600) + (float(minute) * 60) + (frame_count / frame_rate)
                    
                    # Calculate hours, minutes, and remaining seconds
                    matched_hours = int(total_time_seconds // 3600)
                    matched_minutes = int((total_time_seconds % 3600) // 60)
                    y= str(matched_hours) + '.' + str(matched_minutes)
                    strr=float(strr)
                    y=float(y)
                    if y - strr <0.01:
                        pass
                    else:
                        print("Matched at {:02d}:{:02d}".format(matched_hours, matched_minutes))
                        timer=0

                id = Publicids[matchindex]
                if counter == 0 :
                    cvzone.putTextRect(imgBackground,"LOADING",(275,400))
                    cv2.imshow("TV face",imgBackground)
                    cv2.waitKey(1)
                    counter =1 
                    modeType=1
    imgBackground[162:162 + frame_resized.shape[0], 55:55 + frame_resized.shape[1]] = frame_resized
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if counter !=0:
        if counter ==1:
            #get data
            publicInfo = db.reference(f'publicPersonality/{id}').get()
            #print(publicInfo)
            #get image
            
            blob = bucket.get_blob(f'images/{id}.jpg')
            
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgpublic = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            
            #update attandance
            ref = db.reference(f'publicPersonality/{id}')
            publicInfo['total_Attendance'] += 1
            namee=publicInfo['name']
            ref.child('total_Attendance').set(publicInfo['total_Attendance'])

            publicInfo['date'] =publicInfo['date'] +" "+ str (day) +'-' + str(month) + "-" + str(year) + " at " + str(strr) + "\n " 
            ref.child('date').set(publicInfo['date'])
            file_path = os.path.join('main', 'rapport', f'{namee}.txt')

            # Check if the file exists
            if not os.path.exists(file_path):
                # If the file doesn't exist, create it
                with open(file_path, 'w') as file:
                    pass  # This just creates an empty file

            # Open the file in append mode
            with open(file_path, 'a') as file:
                # Append the date information to the file
                file.write(publicInfo['date'] + "\n")
            
                

        #print(str(publicInfo['total_Attendance']))
        if 5< counter <=10 :
            modeType=2
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        if counter <=5:
            cv2.putText(imgBackground, str(publicInfo['total_Attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            cv2.putText(imgBackground,str(publicInfo['job']),(925,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),2)
            cv2.putText(imgBackground,str(publicInfo['name']),(925,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),2)
            imgBackground[175:175 + 216, 909:909 + 216] = imgpublic

        counter+=1
    if counter >10:
        counter=0
        modeType=0
        publicInfo=[]
        imgpublic=[]
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
       
    
    
   
        
    # Display the combined image

    cv2.imshow("TV face", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
