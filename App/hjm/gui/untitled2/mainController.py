import sys
from PyQt5 import  QtWidgets
from main_main_ui import main_window
from Login_main_ui import login_window



class Controller():
    def __init__(self):
        pass

    def show_login(self):
        self.login = login_window()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.window = main_window()
        self.login.close()
        self.window.show()



def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()