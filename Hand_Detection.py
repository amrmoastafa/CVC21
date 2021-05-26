import cv2
import mediapipe

medhands=mediapipe.solutions.hands
hands=medhands.Hands(max_num_hands=2,min_detection_confidence=0.7)
draw=mediapipe.solutions.drawing_utils

def Gesture_Detection(img):
    img = cv2.flip(img,1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    res = hands.process(imgrgb)
    landmark_list=[]
    fingers_tips_landmarks=[4,8,12,16,20] #list of all landmarks of the tips of fingers
    output=''
    label=''
    if res.multi_hand_landmarks:
        for idx, classification in enumerate(res.multi_handedness):
            label = classification.classification[0].label
            if label == 'Right':
                for hand_landmarks in res.multi_hand_landmarks:
                    for id,lm in enumerate(hand_landmarks.landmark):
                        h,w,c= img.shape
                        cx,cy=int(lm.x * w) , int(lm.y * h)
                        landmark_list.append([id,cx,cy])
                        if len(landmark_list) != 0 and len(landmark_list)==21:
                            count_fingers=[]
                            if (landmark_list[4][2] > landmark_list[0][2]) and (landmark_list[8][1] > landmark_list[6][1]) and (landmark_list[16][1] > landmark_list[14][1]) and (landmark_list[12][1] > landmark_list[10][1]) and (landmark_list[20][1] > landmark_list[18][1])  and (landmark_list[4][2] > landmark_list[8][2]):
                                output='down'
                            elif (landmark_list[4][2] < landmark_list[0][2]) and (landmark_list[8][1] > landmark_list[6][1]) and (landmark_list[16][1] > landmark_list[14][1]) and (landmark_list[12][1] > landmark_list[10][1]) and (landmark_list[20][1] > landmark_list[18][1]) and (landmark_list[4][2] < landmark_list[9][2]) :
                                output='up'
                            else :         
                            # #thumb and dealing with flipping of hands
                                if landmark_list[12][1] > landmark_list[20][1]:
                                    if landmark_list[fingers_tips_landmarks[0]][1] > landmark_list[fingers_tips_landmarks[0]-1][1]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)
                                else:
                                    if landmark_list[fingers_tips_landmarks[0]][1] < landmark_list[fingers_tips_landmarks[0]-1][1]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)
                    
                            #others
                                for id in range (1,5):
                                    if landmark_list[fingers_tips_landmarks[id]][2] < landmark_list[fingers_tips_landmarks[id]-2][2]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)

                            if len(count_fingers)!=0:
                                if sum(count_fingers)==0 and (output !='up' or output !='down'):
                                    output='0'
                                elif sum(count_fingers)==1 and (output !='up' or output !='down'):
                                    output='1'
                                elif sum(count_fingers)==2 and (output !='up' or output !='down'):
                                    output='2'
                                elif sum(count_fingers)==3 and (output !='up' or output !='down'):
                                    output='3'
                                elif sum(count_fingers)==4 and (output !='up' or output !='down'):
                                    output='4'
                                elif sum(count_fingers)==5 and (output !='up' or output !='down'):
                                    output='5'
                                fingercount=count_fingers.count(1)
                        #change color of points and lines
                        # draw.draw_landmarks(img,hand_landmarks,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))

            elif label== 'Left':
                for hand_landmarks in res.multi_hand_landmarks:
                    for id,lm in enumerate(hand_landmarks.landmark):
                        h,w,c= img.shape
                        cx,cy=int(lm.x * w) , int(lm.y * h)
                        landmark_list.append([id,cx,cy])
                        if len(landmark_list) != 0 and len(landmark_list)==21:
                            count_fingers=[]
                            if (landmark_list[4][2] > landmark_list[0][2]) and (landmark_list[8][1] < landmark_list[6][1]) and (landmark_list[16][1] < landmark_list[14][1]) and (landmark_list[12][1] < landmark_list[10][1]) and (landmark_list[20][1] < landmark_list[18][1])  and (landmark_list[4][2] > landmark_list[8][2]):
                                output='down'
                            elif (landmark_list[4][2] < landmark_list[0][2]) and (landmark_list[8][1] < landmark_list[6][1]) and (landmark_list[16][1] < landmark_list[14][1]) and (landmark_list[12][1] < landmark_list[10][1]) and (landmark_list[20][1] < landmark_list[18][1]) and (landmark_list[4][2] < landmark_list[9][2]):
                                output='up'
                            else :         
                            # #thumb and dealing with flipping of hands
                                if landmark_list[12][1] > landmark_list[20][1]:
                                    if landmark_list[fingers_tips_landmarks[0]][1] > landmark_list[fingers_tips_landmarks[0]-1][1]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)
                                else:
                                    if landmark_list[fingers_tips_landmarks[0]][1] < landmark_list[fingers_tips_landmarks[0]-1][1]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)
                    
                            #others
                                for id in range (1,5):
                                    if landmark_list[fingers_tips_landmarks[id]][2] < landmark_list[fingers_tips_landmarks[id]-2][2]:
                                        count_fingers.append(1)
                                    else:
                                        count_fingers.append(0)

                            if len(count_fingers)!=0 and (output !='up' or output !='down'):
                                if sum(count_fingers)==0 :
                                    output='0'
                                elif sum(count_fingers)==1 :
                                    output='1'
                                elif sum(count_fingers)==2 :
                                    output='2'
                                elif sum(count_fingers)==3 :
                                    output='3'
                                elif sum(count_fingers)==4 :
                                    output='4'
                                elif sum(count_fingers)==5 :
                                    output='5'
                                fingercount=count_fingers.count(1)                    
                        #change color of points and lines
                        # draw.draw_landmarks(img,hand_landmarks,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))
                
    return label,output        

