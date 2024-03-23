import cv2
import os
import pickle
import face_recognition
import time
import numpy as np

# Open the video file
video_path = 'main/tebboune.mp4'
cap = cv2.VideoCapture(video_path)

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

while True:
    # Capture a frame from the video
    success, img = cap.read()
    
    # Break the loop if video ends
    if not success:
        print("End of video.")
        break

    # Resize the frame to match the size of the region in imgBackground
    img = cv2.resize(img, (640, 480))
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        # Draw rectangle around the face
        top, right, bottom, left = faceLoc
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(img, (left, top), (right, bottom), (203, 192, 255), 2)

        # Print the current time when a face is matched
        '''for i, match in enumerate(matches):
            if match:
                matched_id = Publicids[i]
                print("Face matched at:", time.strftime('%Y-%m-%d %H:%M:%S'), "ID:", matched_id)
'''
        matchindex=np.argmin(faceDis)
        #print("Match index",matchindex)
        if matches[matchindex]:
            pass
            # print("known face detected face : ",Publicids[matchindex])
    # Replace the region in imgBackground with the resized frame
            
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    # Display the combined image
    cv2.imshow("TV face", imgBackground)

    # Check for key press
    key = cv2.waitKey(30)

    # Break the loop if 'q' is pressed
    if key & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
