from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from ui.mediaplayer import Ui_MainWindow


def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 360000
    # h, r = divmod(ms, 36000)
    m, r = divmod(ms, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d" % (m,s))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup()
        self.makeConnections()
        self.show()

    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.mediaPlayerWidget.setLayout(vbox)
        return videoOutput


    def update_duration(self, duration):
        print("!", duration)
        print("?", self.mediaPlayer.duration())
        
        self.timeSlider.setMaximum(duration)

        if duration >= 0:
            self.totalTime.setText(hhmmss(duration))

    def update_position(self, position):
        if position >= 0:
            self.currentTime.setText(hhmmss(position))

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
        

    def onActionOpenTriggered(self):
        path = QFileDialog.getOpenFileName(self,"Open","/")
        filepath = path[0]
        if filepath == "":
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()



if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()