import sys
import subprocess
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout, QSizePolicy, QGroupBox, QGridLayout
from gui.untitled2.login_ui import Ui_Login_page




class login_window(QWidget, Ui_Login_page):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, *args, obj=None, **kwargs):
        super(login_window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.register_button.clicked.connect(self.register_button_click)
        self.close_bt.clicked.connect(lambda:self.close())
        self.minize_bt.clicked.connect(self.minizing)

    def register_button_click(self):
        email = self.email_le.text()
        license_key = self.licenseKey_le.text()
        #print(license_key)
        if str(email) == "" or str(license_key) == "":
            self.unsuccessfull_label.setText('')
            self.unsuccessfull_label.setText('* wrong email or license key!')
            self.unsuccessfull_label.adjustSize()
            return
        try:    
            process = subprocess.run(["hwinfo", "--bios"], capture_output=True)
            results = str(process.stdout).split("\\n")
            hardware_id = str()
            for result in results:
                if "unique id" in result.lower():
                    hardware_id = result.split(": ")[1]
        except:
            hardware_id = ""
        
        r = requests.post('http://phenom.pythonanywhere.com/validate-license/',
                  json={'email': email, 'license': license_key, 'hardware_id' :hardware_id})
        print(r.json())
        if r.json()['isValid'] :
            self.switch_window.emit()
        else:
            self.unsuccessfull_label.setText('')
            self.unsuccessfull_label.setText('* wrong email or license key!')
            self.unsuccessfull_label.adjustSize()
            return

    def minizing(self):
        self.showMinimized()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = login_window()
    mainWindow.show()
    sys.exit(app.exec_())