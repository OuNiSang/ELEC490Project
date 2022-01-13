from mimetypes import init
from multiprocessing.dummy import Process
from queue import Queue
import queue
import sys
from xml.dom.expatbuilder import FragmentBuilder
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QDateTime, QMutex
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
import cv2 as cv2
import pyvirtualcam      
import numpy as np  

from PyQt5 import QtCore, QtGui, QtWidgets


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
      self.btn_open.setText(_translate("Form", "打开摄像头"))
      self.btn_close.setText(_translate("Form", "关闭摄像头"))
      self.btn_openGarry.setText(_translate("Form", "打开灰度图"))

#创建新线程

class Thread_UpdateWidget(QThread):
    def __init__(self):
        super(Thread_UpdateWidget,self).__init__()
    pass


class MianWindow(QWidget):
    
    sig_rawCapture = pyqtSignal(np.ndarray)
    isVirtualCamStarted = False
    frameBuffer = queue.Queue()
    updateStep = 5
    currentN = 0
    mutex = QMutex() #lock
    thread_Update = Thread_UpdateWidget()
    
    def __init__(self,parent=None):
       super(MianWindow,self).__init__(parent)
       self.ui=Ui_Form()
       self.ui.setupUi(self)
       
       self.sig_rawCapture.connect(Process)
    
    def Process(self, img):
        self.currentN += 1
        try:
            if self.currentN >= self.updateStep:
                self.frameBuffer.put(img)
                self.currentN = 0
        except:
            print("Frame drop")

    def StartVirtualCam(self):
        w = 1024
        h = 768
        fps = 30
        fmt = pyvirtualcam.PixelFormat.BGR
        cap = cv2.VideoCapture(0)
        self.isVirtualCamStarted = True
        
        with pyvirtualcam.Camera(width=w, height=h, fps=fps, fmt = fmt) as cam:
            while self.isVirtualCamStarted:
                ret_val, frame = cap.read()
                self.sig_rawCapture.emit(frame)
                    
                frame = cv2.resize(frame, (w, h), interpolation=cv2.COLOR_BGR2RGB)
                # cv2.imshow('my webcam', frame)
                cam.send(frame)
                cam.sleep_until_next_frame()
                if not self.isVirtualCamStarted:
                    cap.release()
                    break  # esc to quit
                cv2.waitKey(20)
            # cv2.destroyAllWindows()


if __name__=='__main__':
   app = QApplication(sys.argv)
   form = MianWindow()
   form.show()
   sys.exit(app.exec_())