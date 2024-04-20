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


# Open the video file
video_path = f'main/{hotspot_name}.mp4'
cap = cv2.VideoCapture(video_path)
imgpublic=[]
# Read the background image
imgBackground = cv2.imread('recources/background.png')

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
                # Get current frame number
                if counter ==0:
                    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    # Get frame rate
                    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
                    # Calculate current time in seconds
                    current_time_seconds = frame_number / frame_rate
                    if current_time_seconds > 60 :
                        x==1
                    if x==1:
                        current_time_seconds= current_time_seconds / 60

                    # Format the current time to display only two decimal places
                    
                    print("Face detected at : ",current_time_seconds)
                    info=db.reference(f'publicPersonality/{id}').get()
                    
                    if info is not None:
                                            # Extract name from info (assuming info is a dictionary)
                        name = str(info['name'])

                        # Construct the output file path
                        filename = name + ".txt"
                        output_file_path = os.path.join('main/rapport', filename)

                        try:
                            # Attempt to open the file in append mode ('a')
                            with open(output_file_path, 'a') as file:
                                # Write the face detection information into the file
                                file.write(f"Face detected at: {current_time_seconds}\n")
                                print(f"Face detection information appended to '{output_file_path}'.")
                        except FileNotFoundError:
                            # File does not exist, so create it and write the content
                            with open(output_file_path, 'w') as file:
                                # Write the face detection information into the file
                                file.write(f"ABDELMAJID TEBBOUNE RAPPORT :")
                                file.write(f"Face detected at: {current_time_seconds}\n")
                                print(f"File '{output_file_path}' created and face detection information written.")

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
            ref.child('total_Attendance').set(publicInfo['total_Attendance'])
            
                

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
