from asyncio import QueueEmpty
from queue import Queue
import queue
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QDateTime,QMutex
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
import cv2 as cv
import pyvirtualcam   
import numpy as np    

from PyQt5 import QtCore, QtGui, QtWidgets

from Detection          import Detection
from Video              import Video

mutex = QMutex()
class Ui_Form(object):
    def setupUi(self, Form):
      Form.setObjectName("Form")
      Form.resize(790, 463)
      self.layoutWidget = QtWidgets.QWidget(Form)
      self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 751, 331))
      self.layoutWidget.setObjectName("layoutWidget")
      self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
      self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
      self.horizontalLayout.setObjectName("horizontalLayout")
      self.lbl_sourceImage = QtWidgets.QLabel(self.layoutWidget)
      self.lbl_sourceImage.setObjectName("lbl_sourceImage")
      self.horizontalLayout.addWidget(self.lbl_sourceImage)
      self.lbl_dealedImage = QtWidgets.QLabel(self.layoutWidget)
      self.lbl_dealedImage.setObjectName("lbl_dealedImage")
      self.horizontalLayout.addWidget(self.lbl_dealedImage)
      self.layoutWidget1 = QtWidgets.QWidget(Form)
      self.layoutWidget1.setGeometry(QtCore.QRect(180, 390, 401, 25))
      self.layoutWidget1.setObjectName("layoutWidget1")
      self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
      self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
      self.horizontalLayout_2.setObjectName("horizontalLayout_2")
      self.btn_open = QtWidgets.QPushButton(self.layoutWidget1)
      self.btn_open.setObjectName("btn_open")
      self.horizontalLayout_2.addWidget(self.btn_open)
      self.btn_close = QtWidgets.QPushButton(self.layoutWidget1)
      self.btn_close.setObjectName("btn_close")
      self.horizontalLayout_2.addWidget(self.btn_close)
      self.btn_openGarry = QtWidgets.QPushButton(self.layoutWidget1)
      self.btn_openGarry.setObjectName("btn_openGarry")
      self.horizontalLayout_2.addWidget(self.btn_openGarry)

      self.retranslateUi(Form)
      QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
      _translate = QtCore.QCoreApplication.translate
      Form.setWindowTitle(_translate("Form", "Form"))
      self.lbl_sourceImage.setText(_translate("Form", ""))
      self.lbl_dealedImage.setText(_translate("Form", ""))
      self.btn_open.setText(_translate("Form", "Camera ON"))
      self.btn_close.setText(_translate("Form", "Camera Off"))
      self.btn_openGarry.setText(_translate("Form", "Detection On"))

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
            print(self.frameBuffer.qsize())
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
       self.ui=Ui_Form()
       self.ui.setupUi(self)
       self.cvThread=FrameCaptureThread()
       self.detectionThread = DetectionDealingThread()

       self.Video = Video()
       self.cstep = 0
       self.maxstep = 5
 
       self.cvThread.sig_outQImageFrame.connect(self.showRawImg)
       self.cvThread.sig_outRawFrame.connect(self.detectionThread.LoadImgBuffer)

       self.ui.btn_open.clicked.connect(self.openScarme)
       self.ui.btn_openGarry.clicked.connect(self.openDetectionScarme)
       self.ui.btn_openGarry.clicked.connect(self.cvThread.DetectionOnChange)
       self.ui.btn_close.clicked.connect(self.cvThread.end)
       self.ui.btn_close.clicked.connect(self.detectionThread.end)

       self.setWindowIcon(QIcon(r'ico\Qt.ico'))

       self.cvThread.finished.connect(self.CameraThreadIsClose)
       self.detectionThread.sig_detectionOutImg.connect(self.showDetectionImg)
       
       


    def showRawImg(self,img):

       temp = self.ui.lbl_sourceImage.size()
       img=img.scaled(temp)
       self.ui.lbl_sourceImage.setPixmap(QPixmap.fromImage(img))
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