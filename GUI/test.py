import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
import cv2
import Hand_Detection as hd
import time
#For testing only
ret = ['1','2','3','4','5']
def Test():
        
    cap=cv2.VideoCapture(0)
    while True :
        success, img=cap.read()
        hand,out=hd.Gesture_Detection(img)
        # print(hand)
        cv2.imshow("hand gestures",img)
        if cv2.waitKey(1) == ord('q'):
            break
        print(out)
        

# cap=cv2.VideoCapture(0)
# while True :
#     _,img = cap.read()
#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x,y,w,h) in faces:
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = img[y:y+h, x:x+w]
#         eyes = eye_cascade.detectMultiScale(roi_gray)
#         for (ex,ey,ew,eh) in eyes:
#             cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)  
#     if len(eyes) == 0:
#         print("Is Closed")
#     else:
#         print('Is Open')

#     print(faces)
#     cv2.imshow('img',img)

#     cv2.waitKey(1)
Test()