
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from queue import Queue
from threading import Thread
from ui.mediaplayer import Ui_MainWindow
from Out import *
import Hand_Detection as hd
import sys,os
import cv2
import time

q = Queue()
flag = 0

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup()
        self.makeConnections()
        self.show()

    def setup(self):
        # Function that sets up all the required objects before making connections
        gestures_list = ['1','2','3','4','5','up','down']
        cap=cv2.VideoCapture(0)
        t1 = Thread(target = self.detectGesture,args=(gestures_list,cap))
        t1.start()
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
        
    def hhmmss(self,ms):
        # Function to calculate time in minutes , seconds from milli seconds
        m, r = divmod(ms, 60000)
        s, _ = divmod(r, 1000)
        return ("%d:%02d" % (m,s))

    def makeMediaPlayer(self):
        # Function to instantiate the mediaplayer object
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        # Function to set up the QVideo widget
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.mediaPlayerWidget.setLayout(vbox)
        return videoOutput


    def update_duration(self, duration):
        # print("!", duration)
        # print("?", self.mediaPlayer.duration())
        
        self.timeSlider.setMaximum(duration)

        if duration >= 0:
            self.totalTime.setText(self.hhmmss(duration))

    def update_position(self, position):
        if position >= 0:
            self.currentTime.setText(self.hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def makeConnections(self):
        self.actionOpen.triggered.connect(self.onActionOpenTriggered)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
        self.volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)
        self.timeSlider.valueChanged.connect(self.mediaPlayer.setPosition)
        self.mediaPlayer.durationChanged.connect(self.update_duration)
        self.mediaPlayer.positionChanged.connect(self.update_position)
        self.ipmodulePushButton.clicked.connect(self.viewWin)
        self.mediaPlayer.volumeChanged.connect(self.volumeSlider.setValue)

    
    def viewWin(self):
        global flag
        if flag == 0:
            q.put("True")
        elif flag ==1:
            q.put("False")

    def detectGesture(self,gest,cap):
        while True :
            success, img=cap.read()
            hand,out=hd.Gesture_Detection(img)
            # print(hand)
            time.sleep(0.2)
            global flag
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
            if q.empty() is not True:
                view = q.get()
                if view == "True":
                    flag = 1
                elif view == "False":
                    flag = 0
                    cv2.destroyAllWindows()
            if flag == 1:
                cv2.imshow("hand gestures",img)
            print(out)
            if out in gest:
                if out == '1':
                    self.mediaPlayer.pause()
                    continue
                elif out == '2':
                    self.mediaPlayer.play()
                    continue
                elif out == '3':
                    self.mediaPlayer.setVolume((self.mediaPlayer.volume() - 10))
                    continue
                elif out == '4':
                    self.mediaPlayer.setVolume((self.mediaPlayer.volume() + 10))
                    continue
                elif out == 'up':
                    if self.mediaPlayer.playbackRate() < 3.0:
                        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() + 0.5)
                    print(self.mediaPlayer.playbackRate())
                    continue
                elif out == 'down':
                    if self.mediaPlayer.playbackRate() > 1.0:
                        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() - 0.5)
                    print(self.mediaPlayer.playbackRate())
                    continue
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)

            if (len(eyes) == 0) or (len(faces) == 0):
                print("eyes closed")
                self.mediaPlayer.pause()
                continue

        cv2.destroyAllWindows()


    def onActionOpenTriggered(self):
        path = QFileDialog.getOpenFileName(self,"Open","/")
        filepath = path[0]
        if filepath == "":
            return
        self.groupBox.setEnabled(True)
        self.timeSlider.setEnabled(True)
        self.volumeSlider.setEnabled(True)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()



if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())