import cv2
import Hand_Detection as hd
cap=cv2.VideoCapture(0)
while True :
    success, img=cap.read()
    hand,out=hd.Gesture_Detection(img)
    print(out)
    print(hand)
    cv2.imshow("hand gestures",img)
    if cv2.waitKey(1) == ord('q'):
         break

cv2.destroyAllWindows()
