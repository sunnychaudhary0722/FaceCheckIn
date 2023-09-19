import cv2
import numpy as np
import face_recognition
#load image

imgShahrukh = face_recognition.load_image_file('sharukh0.jpg')
imgShahrukh = cv2.cvtColor(imgShahrukh,cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('sharukhtest.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgShahrukh)[0]
encodeShahrukh = face_recognition.face_encodings(imgShahrukh)[0]
cv2.rectangle(imgShahrukh,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
#18 compare two faces
results =face_recognition.compare_faces([encodeShahrukh],encodeTest)
#shows distance
faceDis = face_recognition.face_distance([encodeShahrukh],encodeTest)
print(results,faceDis)
#22 put text on the comparing photo
cv2.putText(imgTest,f'{results}{round(faceDis[0],4)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

#show output name
cv2.imshow('Shahrukh Khan',imgShahrukh)
cv2.imshow('Shahrukh test',imgTest)
cv2.waitKey(0)