from gui.untitled2.main_ui import Ui_Phenom
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class main_window(QWidget, Ui_Phenom):

    send_bt = QtCore.pyqtSignal()
    mic_bt = QtCore.pyqtSignal()

    def __init__(self, *args, obj=None, **kwargs):
        super(main_window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.register_button.clicked.connect(self.register_button_click)
        # self.close_bt.clicked.connect(lambda:self.close())
        # self.minize_bt.clicked.connect(self.minizing)
        self.gif_lable = QMovie("gui/untitled2/icons/main_page/phenom_gif.gif", QByteArray(), self)
        self.gif_lable.setCacheMode(QMovie.CacheAll)
        # self.mic_button.clicked.connect(self.mic_bt_click)
        # self.send_button.clicked.connect(self.send_bt_click)
        self.label.setMovie(self.gif_lable)
        self.gif_lable.start()
        self.thread = QThread()
        self.speak_thread = QThread()

    def send_bt_click(self):
        self.send_bt.emit()

    def mic_bt_click(self):
        self.mic_bt.emit()

    def update_mic_send_button(self):
        self.mic_button.setEnabled(True)
        self.send_button.setEnabled(True)


        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = main_window()
    mainWindow.show()
    sys.exit(app.exec_())



