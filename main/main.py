import cv2
import os

# Open the video file
video_path = 'main/FACES.mp4'
cap = cv2.VideoCapture(video_path)

# Read the background image
imgBackground = cv2.imread('recources/background.png')

# Import images into a list
folderModepath = 'recources/modes'
modePathlist = os.listdir(folderModepath)
imgModeList = [cv2.imread(os.path.join(folderModepath, path)) for path in modePathlist]

while True:
    # Capture a frame from the video
    success, img = cap.read()
    
    # Break the loop if video ends
    if not success:
        print("End of video.")
        break

    # Resize the frame to match the size of the region in imgBackground
    img = cv2.resize(img, (640, 480))

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
