# this code is provided to get the coordinates of a point selected in an image
import cv2
import sys


print("hey")
print("Number of arguments:", len(sys.argv))
print("Arguments:", sys.argv)

def click_event(event, x, y, flags, param):
    # Check for left mouse button click
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print and display the clicked coordinates
        print(f"Coordinates: ({x}, {y})")
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"({x}, {y})", (x, y), font, 1, (255, 0, 0), 2)
        cv2.imshow("Image", img)

# Read the image
img = cv2.imread("main/parameterPAGE.png")

# Create a window for displaying the image
cv2.namedWindow("Image")

# Set the mouse callback function
cv2.setMouseCallback("Image", click_event)

# Display the image
cv2.imshow("Image", img)

# Wait for user interaction (clicks)
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
