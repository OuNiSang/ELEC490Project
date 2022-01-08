import sys
import json
import _thread
import time

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
import pyvirtualcam      
from UI_StudentWindow   import Ui_MainWindow
from Detection          import Detection
from Video              import Video

class MainWindow(QMainWindow):
    
    #Init main signal 
    sig_start = pyqtSignal()
    
    def __init__(self):
        # Step1 Load ui
        super(MainWindow, self).__init__()
        print("Initiating Main Window")
        self.ins_ui = Ui_MainWindow()
        self.ins_ui.setupUi()
        
        #Signal and Slot 
        self.ins_ui.startButton.clicked.connect(self.Sig_Start)
        # self.ins_ui.stopButton.clicked.connect()
        # self.ins_ui.recordButton.clicked.connect()
        
        self.sig_start.connect(self.DetectionStart)
        
        # Step2 Load Detection
        self.ins_detection = Detection()
        
        # Step3 load Video
        self.ins_video = Video()
        

    def DetectionStart(self):
        
        # Step1 Check Camera avilibility
        self.ins_video.CheckCamValid()
        
        # Step2 obtaining data while dispactch 
        w = self.ins_video.w
        h = self.ins_video.h
        with pyvirtualcam.Camera(width = w, height = h, fps = self.ins_video.fps) as cam: 
            pass  
            
        
    
    def Sig_Start(self):
        self.sig_start.emit()
    