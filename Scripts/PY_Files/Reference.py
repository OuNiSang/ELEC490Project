import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QDateTime
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
import cv2 as cv
import pyvirtualcam      

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
class DealImgThread(QThread):
   #设置一个原图像信号，一个灰度转换后的图
   singoutSource=pyqtSignal(QImage)
   singoutGarry=pyqtSignal(QImage)
   def __init__(self,parent=None):
       super(DealImgThread,self).__init__(parent)
       self.cv=cv
       self.cvCap=self.cv.VideoCapture(0)
       #设置灰度转换是否打开
       self.garryIsOpen=False
       self.threadIsOpen=True

   def openGarry(self):
       if(self.garryIsOpen==False):
           self.garryIsOpen=True

   # def start(self):
   #     self.threadIsOpen=True

   def end(self):
       if(self.threadIsOpen):
           self.threadIsOpen=False


   def run(self):
       self.threadIsOpen=True
       while self.threadIsOpen:
           with pyvirtualcam.Camera(width=1024, height=768, fps=30, fmt = pyvirtualcam.PixelFormat.BGR ) as cam:
            ret,frame=self.cvCap.read()
            outframe = cv.resize(frame, (1024, 768), interpolation=cv.COLOR_BGR2RGB)
            cam.send(outframe)
            cam.sleep_until_next_frame()
            
            frame=self.cv.flip(frame,1)
            h,w,ch=frame.shape
            bytesPerLine=3*w
            qImg=QImage(frame.data, w, h, bytesPerLine,QImage.Format_RGB888).rgbSwapped()
            self.singoutSource.emit(qImg)
            #打开灰度转换功能
            if(self.garryIsOpen==True):
                #这里不太知道怎么把QImage转换为灰度图，就用了个折中的办法，先转化为灰度图，再转化为三通道的BGR图
                garryImg = self.cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                garryImg=self.cv.cvtColor(garryImg, cv.COLOR_GRAY2BGR)
                gImg = QImage(garryImg.data, w, h, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                self.singoutGarry.emit(gImg)
           self.cv.waitKey(20)


class MianWindow(QWidget):
   def __init__(self,parent=None):
       super(MianWindow,self).__init__(parent)
       self.ui=Ui_Form()
       self.ui.setupUi(self)
       self.cvThread=DealImgThread()
       #原始图片信号连接
       self.cvThread.singoutSource.connect(self.showImg)
       #灰度转换后信号连接
       self.cvThread.singoutGarry.connect(self.showGarry)
       self.ui.btn_open.clicked.connect(self.openScarme)
       self.ui.btn_openGarry.clicked.connect(self.cvThread.openGarry)
       self.ui.btn_close.clicked.connect(self.cvThread.end)
       #一般图标在初始化的时候就要设置，要不然后面的显示不了
       self.setWindowIcon(QIcon(r'ico\Qt.ico'))
       #线程结束通知
       self.cvThread.finished.connect(self.CameraThreadIsClose)

   def showImg(self,img):
       #先取的原来lable的尺寸，然后再转换一下
       temp = self.ui.lbl_sourceImage.size()
       img=img.scaled(temp)
       self.ui.lbl_sourceImage.setPixmap(QPixmap.fromImage(img))
       # now = QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
       # print(now + ':原图触发！')

   def CameraThreadIsClose(self):
       self.msgBox=QMessageBox()
       self.msgBox.setWindowIcon(QIcon(r'ico\Qt.ico'))
       self.msgBox.information(self,'信息提示框','线程执行结束！！！',buttons=QMessageBox.Yes)

   def openScarme(self):
       if(self.cvThread.isRunning()==False):
           self.cvThread.start()

   def showGarry(self,img):
       temp = self.ui.lbl_dealedImage.size()
       img=img.scaled(temp)
       self.ui.lbl_dealedImage.setPixmap(QPixmap.fromImage(img))
       # now=QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
       # print(now+':Garry触发！')


if __name__=='__main__':
   app = QApplication(sys.argv)
   form = MianWindow()
   form.show()
   sys.exit(app.exec_())