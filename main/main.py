import cv2
import os

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 680)  # Set width
cap.set(4, 840)  # Set height

# Read the background image
imgBackground = cv2.imread('recources/background.png')

#import images into a list 
folderModepath='recources/modes'
modePathlist=os.listdir(folderModepath)
imgModeList=[]
for path in modePathlist:
    imgModeList.append(cv2.imread(os.path.join(folderModepath,path)))
# print(len(imgModeList))

while True:
    # Capture a frame from the webcam
    success, img = cap.read()

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    # Display the combined image
    cv2.imshow("TV face", imgBackground)

    # Check for key press
    key = cv2.waitKey(1)

    # Break the loop if 'q' is pressed
    if key & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
