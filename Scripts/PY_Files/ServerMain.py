import sys
import cv2 as cv
from cv2 import isContourConvex
import numpy as np  
import time 
import threading
 

from PyQt5.QtCore       import Qt, QThread, pyqtSignal,QDateTime,QMutex,QStringListModel
from PyQt5.QtGui        import QIcon,QImage,QPixmap
from PyQt5.QtWidgets    import QDialog, QApplication, QWidget,QMessageBox,QMenu,QLabel,QGraphicsItem
from PyQt5              import QtCore, QtGui, QtWidgets
from MySocket           import MySocket
from math               import *
from UI_TeacherWindow   import Ui_MainWindow
from matplotlib.backends.qt_compat      import QtWidgets
from matplotlib.backends.backend_qtagg  import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure                  import Figure

mutex       = QMutex()
list_connection = []

class PltThread(QThread):
    
    def __init__(self, parent = None):
        super(PltThread, self).__init__(parent)
        self.isThreadOpen = False
        self.isPloting = False
        self.list_localTime = 0
        self.UpdateSec = 2


    
    def ShowScorePltAndCurrentScore(self):
        
        if(not self.isPloting):
            return
  
        # print("Updating PLT")
        self.list_localTime = time.time() - gui.startTime
        # print(self.list_localTime)
        # format data
        _numOfShownData = 10
        _dx = gui.list_time.copy()
        _dy = gui.list_score.copy()
        _currentScore = _dy[len(_dy)-1]
        
        # format axis
        gui.score_canvas_ax.set(xlim=[max(0,self.list_localTime - self.UpdateSec*3*(_numOfShownData/2)), 
                                      self.list_localTime + self.UpdateSec*3*(_numOfShownData/2)]
                                , ylim=[ max(-10, _currentScore - 70) , min(110, _currentScore + 80)])
                
        # use PLT to output image 
        gui.score_canvas_line.set_data(_dx, _dy)
        gui.score_canvas_line.figure.canvas.draw()
        cv.waitKey(20)
    
    def ChangePltState(self):
        self.isPloting = not self.isPloting
        if(self.isPloting):
            self._timer = gui.score_canvas.new_timer(self.UpdateSec*10)
            self._timer.add_callback(self.ShowScorePltAndCurrentScore)
            self._timer.start()

        
    def end(self):
        if(self.isThreadOpen):
            self.isThreadOpen = False
    
    def run(self):
        self.isThreadOpen = True
        while self.isThreadOpen:
            pass

class ScoreThread(QThread):
    
    sig_outTotalScore = pyqtSignal(float)
    
    def __init__(self, parent = None):
        super(ScoreThread, self).__init__(parent)
        self.isThreadOpen = True
        self.numClient = 0
        self.currentScoreNum = 0
        self.currentScore = 0
        self.avgScore = 0
        self.isCalculating = False
    
    def ChangeCalculationState(self):
        self.isCalculating = not self.isCalculating
    
    def LoadScore(self, score):
        if not self.isCalculating:
            return
        try:
            if(mutex.tryLock(5)):
                self.currentScore += float(score)
                self.currentScoreNum += 1
            mutex.unlock()
        except:
            print("Cannot load score",score)
    
    def CalculateTotalScore(self):
        # based on number of client calculate total score
        try:
            if(mutex.tryLock(5)):
                self.avgScore = self.currentScore / self.numClient
                print("AVG score = ",self.avgScore)
                self.currentScoreNum = 0
                self.currentScore = 0
            mutex.unlock()
        except:
            print("Cannot cal total score")

    def addC(self):
        # add number of connected client 
        # print("C Add")
        self.numClient += 1
    
    def subC(self):
        # del number of connected client 
        # print("C sub")
        self.numClient -= 1
       
    def end(self):
        if(self.isThreadOpen):
            self.isThreadOpen = False
    
    def run(self):
        self.isThreadOpen = True
        while self.isThreadOpen:
            if self.currentScoreNum < self.numClient or self.numClient == 0 or not self.isCalculating:
                # print("n")
                continue
            print("t",self.currentScoreNum,self.numClient)
            self.CalculateTotalScore()
            self.sig_outTotalScore.emit(self.avgScore)

class SocketThread(QThread):
    
    sig_ClientConnect = pyqtSignal(str)
    sig_ClientClose = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super(SocketThread, self).__init__(parent)
        self.isThreadOpen = False
        self.isBinded = False
        self.s = MySocket()
        
        
    def BindHost(self, addr, port):
        self.addr = addr
        self.port = port
        # print("Binding",addr,port)
        self.s.bind(self.addr, self.port)
        self.isBinded = True
    
    def DeconnectClient(self, addr):
        self.sig_ClientClose.emit(str(addr))
        
    def end(self):
        if(self.isThreadOpen):
            self.isThreadOpen = False
            self.isBinded = False
            self.s.s.close()
    
    def run(self):
        self.isThreadOpen = True
        self.s.s.listen(5)
        while self.isThreadOpen:
            if not self.isBinded:
                continue
            clientsock,clientaddress=self.s.s.accept()
            # clientsock = MySocket(clientsock)
            if(mutex.tryLock(20)):
                if clientaddress not in list_connection:
                    list_connection.append(str(clientaddress))
                self.sig_ClientConnect.emit(str(clientaddress))
                print('connect from:',str(clientaddress))
                #Create thread for this client for recieving score
                t=threading.Thread(target=TcpLinkThread,args=(clientsock,clientaddress))
                t.start()
            mutex.unlock()


def TcpLinkThread(clientsock, clientaddress):
    while True:
        try:
            recvdata=clientsock.recv(200).decode('utf-8')
            #send to score thread
            gui.scoreThread.LoadScore(recvdata)
            if not recvdata:
                break
        except:
            clientsock.close()
            print(clientaddress,'offline')
            # inform offline addr and remove from list 
            _index = list_connection.index(str(clientaddress))
            if(mutex.tryLock(10)):
                list_connection.pop(_index)
                gui.socketThread.DeconnectClient(clientaddress)
            mutex.unlock()
            break
        
class MainWindow(QtWidgets.QMainWindow):
    
    sig_isCalandPlt = pyqtSignal()
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.s = MySocket()
        self.list_score = []
        self.list_time = []
        self.list_clientInfo = []
        self.clipboard = QApplication.clipboard()
        self.startTime = 0
        self.totalTime = 0
        
        self.socketThread   = SocketThread()
        self.scoreThread    = ScoreThread()
        self.pltThread      = PltThread()
        
        self.isConnect = False
        self.isReciving = False
        self.isScoring = False 
        self.isPause = False
        
        self.ui.btn_start.clicked.connect(self.OpenConnect)
        self.ui.btn_link.clicked.connect(self.OpenCopyLink)
        
        self.scoreThread.sig_outTotalScore.connect(self.UpdateTotalAvgScore)
        self.socketThread.sig_ClientConnect.connect(self.scoreThread.addC)
        self.socketThread.sig_ClientConnect.connect(self.ShowUpdateClientList)
        self.socketThread.sig_ClientClose.connect(self.scoreThread.subC)
        self.socketThread.sig_ClientClose.connect(self.ShowUpdateClientList)
        self.sig_isCalandPlt.connect(self.scoreThread.ChangeCalculationState)
        self.sig_isCalandPlt.connect(self.pltThread.ChangePltState)
        
        self.score_canvas = FigureCanvas(Figure())
        self.ui.layout_totalScore.addWidget(self.score_canvas)
        self.ui.layout_totalScore.addWidget(NavigationToolbar(self.score_canvas, self))
        self.score_canvas_ax = self.score_canvas.figure.subplots()
        self.score_canvas_ax.set(xlim=[0, 10], ylim=[0,100])
        self.score_canvas_line, = self.score_canvas_ax.plot(0,0)
        
        self.model_listClient = QStringListModel()
        self.model_listClient.setStringList(list_connection)
        self.ui.list_clients.setModel(self.model_listClient)
        

    
    def OpenCopyLink(self):
        if not self.isConnect:
            _check = self.SetupConnection()
            if not _check:
                return
        else:
            try:
                msg = "{0}\n{1}".format(self.addr, self.port)
                reply = QMessageBox.information(self,"Info",
                                            "You gonna copy this to your student for your IP address and Port\n Please check your Information: "+msg,
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
                #copy to clickboard 
                self.clipboard.setText(msg)
            except:
                return
    
    def OpenPause(self):
        #TODO Stop Score Thread calculating final result 
        self.sig_isCalandPlt.emit()
        pass 
    
    def OpenConnect(self):
        
        if not self.isConnect:
            _check = self.SetupConnection()
            if not _check:
                return
            
            #Start receiving score 
            print("Start connection")
            self.socketThread.BindHost(self.addr, self.port)
            self.socketThread.start()
            self.isConnect = True
            
            #Start calculating score 
            print("Start Receiving score")
            self.startTime = time.time()
            self.scoreThread.start()
            self.list_score.append(0)
            self.list_time.append(time.time() - self.startTime)
            
            #Start Plting socre 
            self.sig_isCalandPlt.emit()
            
        else:
            try:
                reply = QMessageBox.warning(self,"Warning",
                                            "Are you Sure you gonna close the link ?\n All the current Client will be offline",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
                # close the host 
                self.totalTime = time.time() - self.startTime
                try:
                    self.socketThread.terminate()
                    self.sig_isCalandPlt.emit()
                    self.isConnect = False
                    
                    _avgScore = np.mean(self.list_score)
                    _msg = "Finshed, the total connection time is {0}, with average score of {1}".format(self.totalTime, _avgScore)
                    self.ui.text_currentScore.append(str(_msg))
                    
                except:
                    print("socket thread termination Error")
            except:
                return
            
            
    def ShowUpdateClientList(self,addr):
        print("Changing List of Connection for addr",addr)
        self.model_listClient.setStringList(list_connection)
        self.ui.list_clients.setModel(self.model_listClient)
    
    def UpdateTotalAvgScore(self, score):
        # update score list 
        _time = time.time() - self.startTime
        self.list_score.append(score)
        self.list_time.append(_time)
        print("Host get total avg score:{0} in time {1}".format(score,_time))
        
        _msg = "AVG Performace: {0}".format(score)
        self.ui.text_currentScore.append(str(_msg))
    

            
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
                self.s.bind(self.addr, self.port)  #checking avilibility of connection only
            except:
                reply = QMessageBox.warning(self,"Warning",
                                                        "Cannot connect to the Host server: {0} {1}\n Retry?".format(self.addr, self.port),
                                                        QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return False
            self.s.s.close() #only store bind info here, do not bind here 
            self.isConnect = True
        return True
    
    
        
    def __del__(self):
        print("Closing Application")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())