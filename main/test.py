from mtcnn import MTCNN
import cv2

detector = MTCNN()
cap = cv2.VideoCapture('main/tebboune.mp4')

frame_skip = 20  # Process every 3rd frame
resize_factor = 0.8  # Resize frames to 50% of their original size
frame_count=0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Resize frame
    frame_resized = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)

    # Convert frame to RGB (MTCNN expects RGB format)
    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    faces = detector.detect_faces(rgb_frame)
    
    # Draw bounding boxes around detected faces
    for face in faces:
        x, y, w, h = face['box']
        x, y, w, h = int(x / resize_factor), int(y / resize_factor), int(w / resize_factor), int(h / resize_factor)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
    # Display the frame with detected faces
    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
