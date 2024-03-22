import cv2
import face_recognition
import pickle
import os

folderpath = '../images'
Pathlist = os.listdir(folderpath)
imgList = []
publicIDS = []

for path in Pathlist:
    imgList.append(cv2.imread(os.path.join(folderpath, path)))
    publicIDS.append(os.path.splitext(path)[0])  # Fix: Append to list

def findEncoding(imageList):
    encodeList = []
    for img in imageList:
        # Fix: Convert image from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img_rgb)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding started...")
encodeListKnown = findEncoding(imgList)
encodeListKnownwithIDS=[encodeListKnown,publicIDS]
print("Encoding complete")

file = open("encodeFile.p","wb")
pickle.dump(encodeListKnownwithIDS,file)
file.close()
print("file saved")