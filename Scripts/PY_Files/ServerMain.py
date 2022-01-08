import sys
import json
import threading
import time
import cv2

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
import pyvirtualcam      
from UI_StudentWindow   import Ui_MainWindow
from Detection          import Detection
from Video              import Video

class MainWindow(QMainWindow, Video, Detection, Ui_MainWindow):
    
    #Init main signal 
    sig_start = pyqtSignal()
    isEnd = False
    
    def __init__(self):
        # Step1 Load ui
        super(MainWindow, self).__init__()
        print("Initiating Main Window")
        self.setupUi()
        
        # Step Signal and Slot 
        self.startButton.clicked.connect(self.Sig_Start)
        # self.ins_ui.stopButton.clicked.connect()
        # self.ins_ui.recordButton.clicked.connect()
        
        self.sig_start.connect(self.DetectionStart)
        
        # Step Thread 
        threading.Thread.__init__(self)
    
    
    def VirtualizeCamera(self):
        
        self.ins_video.CheckCamValid()
        cap = self.cam
        with pyvirtualcam.Camera(width=self.w, height=self.h, fps=self.fps, fmt =self.fmt) as virCam:
            while True:
                ret_val, frame = cap.read()

                self.frame = cv2.resize(frame, (self.w, self.h), interpolation=cv2.COLOR_BGR2RGB)
                # cv2.imshow('my webcam', frame)
                virCam.send(frame)
                virCam.sleep_until_next_frame()
            #     if cv2.waitKey(1) == 27:
            #         break  # esc to quit
            # cv2.destroyAllWindows()
        
        

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
    