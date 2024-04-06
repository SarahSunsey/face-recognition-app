from mtcnn import MTCNN
import cv2
import os
import pickle
import numpy as np
import face_recognition  # Ensure face_recognition is properly installed

# Initialize MTCNN detector
detector = MTCNN()

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

frame_skip = 10  # Process every 20th frame
resize_factor = 0.8  # Resize frames to 80% of their original size
frame_count = 0

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
                frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                # Get frame rate
                frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
                # Calculate current time in seconds
                current_time_seconds = frame_number / frame_rate
                # Convert seconds to minutes
                current_time_minutes = current_time_seconds / 60

                # Format the current time to display only two decimal places
                current_time_formatted = "{:.2f}".format(current_time_minutes)
                print("Face detected at minute:", current_time_formatted)


    # Replace the region in imgBackground with the resized frame
    imgBackground[162:162 + frame_resized.shape[0], 55:55 + frame_resized.shape[1]] = frame_resized

    # Display the combined image
    cv2.imshow("TV face", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
