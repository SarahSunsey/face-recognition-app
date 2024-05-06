import cv2
import numpy as np

# Create a blank black image
test_img = np.zeros((500, 1000, 3), dtype=np.uint8)

# Use cv2.putText() to add text
cv2.putText(test_img, 'Test Message', (50, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


y = 14,5
y = float (14.5)
print
# Display the image
cv2.imshow('Test Image', test_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
