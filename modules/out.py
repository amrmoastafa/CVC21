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
        # cv2.imshow("hand gestures",img)
        if cv2.waitKey(1) == ord('q'):
            break
        print(type(out))
        if out in ret:
            return out
cv2.destroyAllWindows()
def Output_data(img):
    hand,out=hd.Gesture_Detection(img)