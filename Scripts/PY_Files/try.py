from PyQt5.Qt import (QApplication, QWidget, QPushButton, QThread,QMutex,pyqtSignal)
import sys
import time
 
qmut_1 = QMutex() # 创建线程锁
# 继承QThread
class Thread_1(QThread):  # 线程1
    def __init__(self,a):
        super().__init__()
        self.a = a
    def run(self):
        qmut_1.lock() # 加锁
        values = [1, 2, 3, 4, 5]
        for i in values:
            print(i)
            print(self.a)
            time.sleep(0.5)  # 休眠
        qmut_1.unlock() # 解锁
 
class MyWin(QWidget):
    def __init__(self):
        super().__init__()
        # 按钮初始化
        self.btn_1 = QPushButton('按钮1', self)
        self.btn_1.move(120, 80)
        self.btn_1.clicked.connect(self.click_1)  # 绑定槽函数
    # 这里的click_1函数就是btn_1按钮对应的函数，如果这个函数里面的计算过于复杂，
    # 会造成界面卡顿。所以在这个click_1函数里面开启一个新的线程，将复杂的计算放在新线程里。
    # 这样可以避免界面卡顿。把相关的计算放在线程的run函数里，也可以传递参数。
    def click_1(self):
        print('............')
        self.thread_1 = Thread_1(10)  # 创建线程
        self.thread_1.start()  # 开始线程
        print('')
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = MyWin()
    myshow.show()
    sys.exit(app.exec_())