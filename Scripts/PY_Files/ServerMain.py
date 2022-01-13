import sys
import json
from threading import Thread
import time
from tkinter import W
import cv2
import numpy as np
import queue
import pyvirtualcam      

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import QIcon, QImage, QPixmap
from UI_StudentWindow   import Ui_MainWindow
from Detection          import Detection
from Video              import Video


class EmittingStr(QObject):
        textWritten = pyqtSignal(str)  #定义一个发送str的信号
        def write(self, text):
            self.textWritten.emit(str(text))
 


class FrameProduce_Thread(QThread):
    
    sig_OutFrame = pyqtSignal(np.ndarray)
    isProduceFrame = False
    def __init__(self):
        super(FrameProduce_Thread, self).__init__()
        self.video = Video()
        self.cap = self.video.cam
        print(self.video.CheckCamValid())
    
    # def end(self):
    #     if(self.isProduceFrame):
    #         self.isProduceFrame = False

    def run(self):
        # check whether camera is valid
        self.isProduceFrame = True
        if not self.video.CheckCamValid():
            print("Camera is not valid")
            time.sleep(20)
            return
        # Thread to create virtual cam and update it to a buffer 
        with pyvirtualcam.Camera(width=self.video.w, height=self.video.h, fps=self.video.fps, fmt = self.video.fmt) as cam:
            while self.isProduceFrame:
                ret_val, frame = self.cap.read()

                if ret_val:
                    frame = cv2.resize(frame, (self.video.w, self.video.h), interpolation=cv2.COLOR_BGR2RGB)
                    # cv2.imshow('my webcam', frame)
                    self.sig_OutFrame.emit(frame)
                    cam.send(frame)
                    cam.sleep_until_next_frame()
                else:
                    print("Cannot open virtual cam")
                time.sleep(20)
                
            print("closing camera...")
            self.cap.release()
        self.isProduceFrame = False
    


class MainWindow(QMainWindow, Video, Detection, Ui_MainWindow):
    
    #Init main signal 
    sig_startCap = pyqtSignal()
    sig_endCap = pyqtSignal()
    sig_startDect = pyqtSignal()
    sig_endDect = pyqtSignal()
    sig_newFrame = pyqtSignal()
    
    #Store all debug message
    debugMessageLog = []
    frameBuffer = queue.Queue()
    
    def __init__(self):
        # Step1 Load ui
        super(MainWindow, self).__init__()
        print("Initiating Main Window")
        self.setupUi(self)
        
        self.thread_FrameProduce = FrameProduce_Thread()
        self.isStartedCapture = False
        self.isStartedDetection = False
        
        self.frameCount = 0
        self.frameStep = 1
        
        # Step Signal and Slot 
        self.startButton.clicked.connect(self.Sig_CaptureStateChange)
        self.stopButton.clicked.connect(self.Sig_DetetionStateChange)
        # self.recordButton.clicked.connect()
        self.sig_startCap.connect(self.CaptureStart)
        self.sig_endCap.connect(self.CaptureEnd)
        self.sig_startDect.connect(self.DetectionStart)
        self.sig_endDect.connect(self.DetectionEnd)
        self.sig_newFrame.connect(self.DisplayFrame)
        
        self.thread_FrameProduce.sig_OutFrame.connect(self.AddFrameBuffer)
        
        # Step set terminal output to debug window 
        sys.stdout = EmittingStr(textWritten=self.PassDebugMessage)
        sys.stderr = EmittingStr(textWritten=self.PassDebugMessage)

    
    def AddFrameBuffer(self, img):
        self.frameCount += 1
        if (self.frameCount == self.frameStep):
            if(self.isStartedDetection):
                img = self.DetectByFrame(img, self.w, self.h)
            self.frameBuffer.put_nowait(img)
            self.sig_newFrame.emit()
        pass
    
    def DisplayFrame(self):
        windowSize = self.videoWidget.size()
        displayFrame = self.frameBuffer.get_nowait()
        
        #step1 convert frame into QImage type 
        h,w,_ = displayFrame.shape
        bPerLine = 3 * W
        displayFrame=QImage(displayFrame.data, w, h, bPerLine,QImage.Format_RGB888).rgbSwapped()
        
        #Step2 Display image on videoWidget
        displayFrame = displayFrame.scaled(windowSize)
        self.videoWidget.setPixmap(QPixmap.fromImage(displayFrame))
        pass
        
    def CaptureStart(self):
        print("Capture Start")
        self.thread_FrameProduce.start()
        pass
    
    def CaptureEnd(self):
        print("Capture End")
        self.thread_FrameProduce.quit()
        pass
    
    
    def DetectionStart(self):
        print("Detection Start")
        self.isStartedDetection = True
        pass
    
    def DetectionEnd(self):
        print("Detection End")
        self.isStartedDetection = False
        pass
            
        
    
    def Sig_CaptureStateChange(self):
        if not self.isStartedCapture:
            self.sig_startCap.emit()
            self.isStartedCapture = True
        else:
            self.sig_endCap.emit()
            self.isStartedCapture = False
    
    def Sig_DetetionStateChange(self):
        if not self.isStartedDetection:
            self.sig_startDect.emit()
            self.isStartedDetection = True
        else:
            self.sig_endDect.emit()
            self.isStartedDetection = False
    
    def PassDebugMessage(self, message):
        self.debugMessageLog.append(time.time() + message)
        self.DebugMessage.append(time.time() + message)
        
    def WriteDebugMessage(self, fileName):
        with open(fileName, 'w') as file:
            file.writelines(self.debugMessageLog)
        file.close()
        
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
