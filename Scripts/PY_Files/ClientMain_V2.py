import queue
import sys
import cv2 as cv
import pyvirtualcam   
import numpy as np   
 

from PyQt5.QtCore       import Qt, QThread, pyqtSignal,QDateTime,QMutex
from PyQt5.QtGui        import QIcon,QImage,QPixmap
from PyQt5.QtWidgets    import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
from PyQt5              import QtCore, QtGui, QtWidgets
from Detection          import Detection
from Video              import Video
from UI_StudentWindow   import Ui_MainWindow
from MySocket           import MySocket

mutex       = QMutex()
IMG_GOOD    = "./img/gui/Green.png"
IMG_BAD     = "./img/gui/Red.png"
SCORE_GOOD  = 60

class FrameCaptureThread(QThread):

    sig_outQImageFrame=pyqtSignal(QImage)
    sig_outRawFrame = pyqtSignal(np.ndarray)
   
    def __init__(self,parent=None):
       super(FrameCaptureThread,self).__init__(parent)
       self.cv=cv
       self.cvCap=self.cv.VideoCapture(0)

       self.isThreadOpen=True
       self.isDetectionOn = False


    def end(self):
       if(self.isThreadOpen):
           virCam.close()
           self.isThreadOpen=   False
           self.isDetectionOn = False

    def DetectionOnChange(self):
        # print("change state")
        self.isDetectionOn = not self.isDetectionOn
        # print(self.isDetectionOn)

    def run(self):
       self.isThreadOpen=True
       while self.isThreadOpen:
          
        ret,frame=self.cvCap.read()
        outframe = cv.resize(frame, (1024, 768), interpolation=cv.COLOR_BGR2RGB)
        if self.isDetectionOn:
            self.sig_outRawFrame.emit(frame)
        
        #sending it to virtual camera 
        virCam.send(outframe)
        virCam.sleep_until_next_frame()
        
        frame=cv.flip(frame,1)
        h,w,ch=frame.shape
        bPerLine=3*w
        qImgFrame=QImage(frame.data, w, h, bPerLine,QImage.Format_RGB888).rgbSwapped()
        self.sig_outQImageFrame.emit(qImgFrame)

        self.cv.waitKey(30)

class DetectionDealingThread(QThread):
   
    sig_detectionOutResult = pyqtSignal(float)
    def __init__(self,parent=None):
        super(DetectionDealingThread,self).__init__(parent)
        self.cv=cv
        self.cvCap=self.cv.VideoCapture(0)
        self.Detector = Detection() 
        self.bufferSize = 5                #Send for every 20 frame
        self.frameBuffer = queue.Queue(self.bufferSize)

        self.isThreadOpen=True

    def LoadImgBuffer(self,img):
        if (self.frameBuffer.not_full):
            if(mutex.tryLock(10)):
                self.frameBuffer.put(img)
                mutex.unlock()
        else:
            print("Frame Buffer is full")
        
    def end(self):
        if(self.isThreadOpen):
           virCam.close()
           self.isThreadOpen=False


    def run(self):
        self.isThreadOpen=True
        _cnt = 0
        detectResult = 100
        while self.isThreadOpen:
            # print(self.frameBuffer.qsize())
            if(_cnt == 0):
                detectResult = 100
            if (mutex.tryLock(20)):
                if(self.frameBuffer.not_empty):
                    for num in range(self.frameBuffer.qsize()):
                        detectResult += self.Detector.DetectByFrame(self.frameBuffer.get())
                        print("size",self.frameBuffer.qsize(),_cnt,detectResult)
                        _cnt += 1
                        if detectResult is not None and _cnt >= self.bufferSize: 
                            print(detectResult)
                            self.sig_detectionOutResult.emit(max(detectResult, 0.0))
                            detectResult = 100
                            _cnt = 0
                            break
                    if(not self.frameBuffer.empty()):
                        print("CLEAR")
                        self.frameBuffer.queue.clear()
                    
                    mutex.unlock()
            cv.waitKey(50)
                  
class MianWindow(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
       
       super(MianWindow,self).__init__(parent)
       self.ui= Ui_MainWindow()
       self.ui.setupUi(self)
       self.captureThread=FrameCaptureThread()
       self.detectionThread = DetectionDealingThread()
       self.s = MySocket()
       self.isConnect = False;

       self.Video = Video()
       self.cstep = 0
       self.maxstep = 5
 
       self.captureThread.sig_outQImageFrame.connect(self.ShowRawImg)
       self.captureThread.sig_outRawFrame.connect(self.detectionThread.LoadImgBuffer)

       self.ui.btn_open.clicked.connect(self.OpenScarme)
       self.ui.btn_open.clicked.connect(self.captureThread.DetectionOnChange)
       self.ui.btn_stop.clicked.connect(self.OpenStoped)
       self.ui.btn_connect.clicked.connect(self.OpenConnect)
       
       self.img_Good = QPixmap(IMG_GOOD)
       self.img_Bad = QPixmap(IMG_BAD)
    
    #    self.setWindowIcon(QIcon(r'ico\Qt.ico'))

       self.captureThread.finished.connect(self.CloseCamera)
       self.detectionThread.sig_detectionOutResult.connect(self.ShowDetectionResult)
    
        
    def OpenConnect(self):
        if not self.isConnect:
            _check = self.SetupConnection()
            if not _check:
                return
            
        else:
            try:
                self.s.s.close()
                self.isConnect = False
            except:
                return
    
    def OpenStoped(self):
        
        self.detectionThread.end()
        self.captureThread.end()
        self.s.s.close()
        self.isConnect = False
        self.CloseCamera()
    
    def OpenScarme(self):
       if(self.captureThread.isRunning()==False):
           print("Camera On")
           self.captureThread.start()
           self.ui.lbl_camOut.setText(" ") #Clear text on the img 
           global virCam
           virCam = pyvirtualcam.Camera(width=1024, height=768, fps=30, fmt = pyvirtualcam.PixelFormat.BGR )
           if not self.detectionThread.isRunning():
                print("Detection Start")
                self.detectionThread.start()
                
    def SetupConnection(self):
        while not self.isConnect:
            print("Enter Your Host IP")
            self.addr,r = QtWidgets.QInputDialog().getText(self, "Input Your Host IPV4 Adress",
                                                    "Adress: Like \"127.0.0.1 \" ",
                                                    QtWidgets.QLineEdit.Normal,
                                                    QtCore.QDir.home().dirName())
            if not r:
                return False
            self.port,r = QtWidgets.QInputDialog().getText(self, "Input Your Host IPV4 Adress's port",
                                                    "Port: Like \"80 \" ",
                                                    QtWidgets.QLineEdit.Normal,
                                                    QtCore.QDir.home().dirName())
            if not r:
                return False
            try:
              print("Try:",self.addr, self.port)
              self.s.connect(self.addr, self.port)
              print("Connected!!")
            except:
                reply = QMessageBox.warning(self,"Warning",
                                                        "Cannot connect to the Host server: {0} {1}\n Retry?".format(self.addr, self.port),
                                                        QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return False
            self.isConnect = True
        return True
                
    
    def ShowRawImg(self,img):

       temp = self.ui.lbl_camOut.size()
       img=img.scaled(temp)
       self.ui.lbl_camOut.setPixmap(QPixmap.fromImage(img))
       # now = QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
    
    def ShowDetectionResult(self, score):
        
        self.ui.lbl_Status.setText("Score = {0}".format(score))
        print("Score:",score)
        
        #TODO: sending result to the server 
        if self.isConnect:
            print("Try Sending...")
            self.s.mysend(str(score))
            
        #TODO: add sound warning 
        #TODO: setup text for score indication 
        #TODO: store the score 
        if score > SCORE_GOOD:
            self.ui.lbl_Status.setPixmap(self.img_Good)
            return
        self.ui.lbl_Status.setPixmap(self.img_Bad)

           
    def CloseCamera(self):
    #    virCam.close() 
       self.msgBox_Stop=QMessageBox()
       self.msgBox_Stop.setWindowIcon(QIcon(r'ico\Qt.ico'))
       self.msgBox_Stop.information(self,'Message','Thread Over?????????',buttons=QMessageBox.Yes)
       
    def __del__(self):
        print("Disableing camera")
        virCam.close()
        if self.captureThread.isRunning():
            self.captureThread.quit()
        if self.detectionThread.isRunning():
            self.detectionThread.quit()
            
        del self.captureThread
        del self.detectionThread
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MianWindow()
    form.show()
    sys.exit(app.exec_())