import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import platform

path = 'D:/project/photo'

image_paths = []  # Create a list to store image file paths
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    # Create the full image file path
    imgPath = os.path.join(path, cl)

    # Check if the path is a file (to exclude directories)
    if os.path.isfile(imgPath):
        image_paths.append(imgPath)
        classNames.append(os.path.splitext(cl)[0])

        class_names_str = ','.join(classNames)

        print(class_names_str)


def findEncodings(image_paths):
    encodeList = []
    for imgPath in image_paths:
        img = cv2.imread(imgPath)  # Load the image
        if img is not None:  # Check if the image loaded successfully
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
    return encodeList

def markAttendance(name, attendance_record):
    with open ('Attendance.csv', 'r+')as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

            if name not in nameList and name not in attendance_record:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                attendance_record.add(name)


encodeListKnown = findEncodings(image_paths)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
attendance_record = set()

while True:
    success, imgS = cap.read()  # capture a frame from the webcam
    imgS = cv2.resize(imgS, (0, 0), None, 0.80, 0.80)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame, num_jitters=1)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
           # print(name)
            y1,x2,y2,x1 = faceLoc
            cv2.rectangle(imgS,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(imgS,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(imgS,name ,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name, attendance_record)
    cv2.imshow('Webcam',imgS)
    cv2.waitKey(1)






