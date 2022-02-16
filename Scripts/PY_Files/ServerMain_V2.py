import queue
import sys
import cv2 as cv
import pyvirtualcam   
import numpy as np   
 

from PyQt5.QtCore       import Qt, QThread, pyqtSignal,QDateTime,QMutex
from PyQt5.QtGui        import QIcon,QImage,QPixmap
from PyQt5.QtWidgets    import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
from PyQt5              import QtCore, QtGui, QtWidgets
from asyncio            import QueueEmpty
from queue              import Queue
from Detection          import Detection
from Video              import Video
from UI_StudentWindow   import Ui_MainWindow

mutex = QMutex()

class FrameCaptureThread(QThread):

    sig_outQImageFrame=pyqtSignal(QImage)
    sig_outRawFrame = pyqtSignal(np.ndarray)
   
    def __init__(self,parent=None):
       super(FrameCaptureThread,self).__init__(parent)
       self.cv=cv
       self.cvCap=self.cv.VideoCapture(0)

       self.garryIsOpen=False
       self.threadIsOpen=True
       self.isDetectionOn = False


    def end(self):
       if(self.threadIsOpen):
           virCam.close()
           self.threadIsOpen=   False
           self.isDetectionOn = False

    def DetectionOnChange(self):
        # print("change state")
        self.isDetectionOn = not self.isDetectionOn
        # print(self.isDetectionOn)

    def run(self):
       self.threadIsOpen=True
       while self.threadIsOpen:
          
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
   
    sig_detectionOutImg = pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        super(DetectionDealingThread,self).__init__(parent)
        self.cv=cv
        self.cvCap=self.cv.VideoCapture(0)
        self.Detector = Detection() 
        self.bufferSize = 20
        self.frameBuffer = queue.Queue(self.bufferSize)

        self.threadIsOpen=True

    def LoadImgBuffer(self,img):
        if (self.frameBuffer.not_full):
            if(mutex.tryLock(10)):
                self.frameBuffer.put(img)
                mutex.unlock()
        else:
            print("Frame Buffer is full")
        
    def end(self):
        if(self.threadIsOpen):
           virCam.close()
           self.threadIsOpen=False


    def run(self):
        self.threadIsOpen=True
        while self.threadIsOpen:
            # print(self.frameBuffer.qsize())
            if (mutex.tryLock(20)):
                if(self.frameBuffer.not_empty):
                    for num in range(self.frameBuffer.qsize()):
                        detectResult = self.Detector.DetectByFrame(self.frameBuffer.get())
                        if detectResult is not None: self.sig_detectionOutImg.emit(detectResult)
                    mutex.unlock()
            cv.waitKey(50)

        
class MianWindow(QWidget):

    def __init__(self,parent=None):
       
       super(MianWindow,self).__init__(parent)
       self.ui= Ui_MainWindow()
       self.ui.setupUi(self)
       self.cvThread=FrameCaptureThread()
       self.detectionThread = DetectionDealingThread()

       self.Video = Video()
       self.cstep = 0
       self.maxstep = 5
 
       self.cvThread.sig_outQImageFrame.connect(self.showRawImg)
       self.cvThread.sig_outRawFrame.connect(self.detectionThread.LoadImgBuffer)

       self.ui.btn_open.clicked.connect(self.openScarme)
       self.ui.btn_detect.clicked.connect(self.openDetectionScarme)
       self.ui.btn_detect.clicked.connect(self.cvThread.DetectionOnChange)
       self.ui.btn_stop.clicked.connect(self.cvThread.end)
       self.ui.btn_stop.clicked.connect(self.detectionThread.end)

    #    self.setWindowIcon(QIcon(r'ico\Qt.ico'))

       self.cvThread.finished.connect(self.CameraThreadIsClose)
       self.detectionThread.sig_detectionOutImg.connect(self.showDetectionImg)
       
       


    def showRawImg(self,img):

       temp = self.ui.lbl_camOut.size()
       img=img.scaled(temp)
       self.ui.lbl_camOut.setPixmap(QPixmap.fromImage(img))
       # now = QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
    
    def showDetectionImg(self, img):
        # frame=cv.flip(img,1)
        h,w,ch=img.shape
        bPerLine=3*w
        imgQ=QImage(img.data, w, h, bPerLine,QImage.Format_RGB888).rgbSwapped()
        
        temp = self.ui.lbl_dealedImage.size()
        imgQ=imgQ.scaled(temp)
        self.ui.lbl_dealedImage.setPixmap(QPixmap.fromImage(imgQ))
       
    def openDetectionScarme(self,img):
        if not self.detectionThread.isRunning():
            print("Detection Start")
            self.detectionThread.start()
        else:
            self.detectionThread.end()

        # now=QDateTime.currentDateTime().toString('hh:mm:ss.zzz')


    def CameraThreadIsClose(self):
    #    virCam.close() 
       self.msgBox=QMessageBox()
       self.msgBox.setWindowIcon(QIcon(r'ico\Qt.ico'))
       self.msgBox.information(self,'Message','Thread Over！！！',buttons=QMessageBox.Yes)

    def openScarme(self):
       if(self.cvThread.isRunning()==False):
           print("Camera On")
           self.cvThread.start()
           global virCam
           virCam = pyvirtualcam.Camera(width=1024, height=768, fps=30, fmt = pyvirtualcam.PixelFormat.BGR )
           
    def __del__(self):
        print("Disableing camera")
        virCam.close()
        self.cvThread.terminate()
        self.detectionThread.terminate()
        

if __name__=='__main__':
   app = QApplication(sys.argv)
   form = MianWindow()
   form.show()
   sys.exit(app.exec_())