import sys
import textwrap
from math import *

import gui.untitled2.resources
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

DEFAULT_HEAD = 'gui/untitled2/icons/main_page/robot.svg'
DEFAULT_MSG = 'Hello is there anyone?'
DEFAULT_IMG = 'icons/main_page/robot.svg'
DEFAULT_MSG = "Hello World,zai zhe ge shijie shang meiyou shei nenggou sheipan wo"


def checkContainChinese(s):
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def splitStringByLen(text, Len):
    text = text.replace('\n', '.')
    (myText, nLen) = ('', 0)
    for s in text:
        myText += s
        nLen += 3 if checkContainChinese(s) else 1
        if nLen >= (Len - 1):
            myText += '\n'
            nLen = 0
    return myText


class BubbleText(QLabel):
    border = 3
    trigon = 15
    lineLen = 35

    minH = 2 * trigon + 2 * border
    minW = 2 * trigon + 2 * border

    def __init__(self, listItem, listView, text=DEFAULT_MSG, lr=True):
        self.listItem = listItem
        self.listView = listView
        self.text = text
        myText = "\n".join(textwrap.TextWrapper(width=40).wrap(text))
        #splitStringByLen(text, self.lineLen)
        super(BubbleText, self).__init__(myText)
        self.setMinimumWidth(self.minW)
        self.setFont(QFont("Chilanka", 15, QFont.Normal))
        #self.setStyleSheet("QLabel:hover{background-color:rgba(210,240,250,255);}")        #

        self.setState(False)
        self.lr = lr
        if self.lr:
            self.setContentsMargins(
                self.trigon*sqrt(3)/2 + 15, self.border + 10, self.border + 15, self.border + 10)
        else:
            self.setContentsMargins(
                self.border + 15, self.border + 10, self.trigon*sqrt(3)/2 + 15, self.border + 10)

    def paintEvent(self, e):
        size = self.size()
        qp = QPainter()
        qp.begin(self)
        if self.lr:
            self.leftBubble(qp, size.width(), size.height())
        else:
            self.rightBubble(qp, size.width(), size.height())
        qp.end()
        super(BubbleText, self).paintEvent(e)

    def leftBubble(self, qp, w, h):
        qp.setPen(self.colorLeftE)
        qp.setBrush(self.colorLeftM)
        middle = h*(1-0.618)
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        rL = QRectF(shiftx, 1, w-shiftx-self.border, h-3)
        pL = QPolygonF()
        pL.append(QPointF(0, middle))
        pL.append(QPointF(shiftx, middle + shifty))
        pL.append(QPointF(shiftx, middle-shifty))
        """
        pL.append(QPointF(w - self.border, h - self.border)) #第四点
        pL.append(QPointF(w - self.border, self.border)) #第五点
        pL.append(QPointF(shiftx, self.border)) #第六点
        pL.append(QPointF(shiftx, middle - shifty)) #第七点
        """
        qp.drawPolygon(pL)
        qp.drawRoundedRect(rL, 10, 10)
        qp.setPen(self.colorLeftM)
        # qp.setPen(QColor("#ff0000"))
        line = QLine(shiftx, middle+shifty, shiftx, middle-shifty)
        qp.drawLine(line)

    def rightBubble(self, qp, w, h):
        qp.setPen(self.colorRightE)
        qp.setBrush(self.colorRightM)
        middle = h*(1-0.618)
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        rL = QRectF(self.border, 1, w-shiftx-self.border, h-3)
        pL = QPolygonF()
        pL.append(QPointF(w, middle))
        pL.append(QPointF(w-shiftx, middle + shifty))
        pL.append(QPointF(w-shiftx, middle - shifty))
        """
        pL.append(QPointF(w - self.border, h - self.border)) #第四点
        pL.append(QPointF(w - self.border, self.border)) #第五点
        pL.append(QPointF(shiftx, self.border)) #第六点
        pL.append(QPointF(shiftx, middle - shifty)) #第七点
        """
        qp.drawPolygon(pL)
        qp.drawRoundedRect(rL, 10, 10)
        qp.setPen(self.colorRightM)
        # qp.setPen(QColor("#ff0000"))
        line = QLine(w-shiftx, middle+shifty, w-shiftx, middle-shifty)
        qp.drawLine(line)

    def setState(self, mouse):

        if mouse:
            # self.colorLeftM = QColor("#eaeaea")
            self.colorLeftM = QColor("#eaeaea")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#8FD648")
            self.colorRightE = QColor("#85AF65")
        else:
            self.colorLeftM = QColor("#fafafa")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#9FE658")
            self.colorRightE = QColor("#85AF65")
        self.update()

    def enterEvent(self, e):
        # print 'mouse entered'
        self.setState(True)

    def leaveEvent(self, e):
        # print 'mouse leaved'
        self.setState(False)

    def contextMenuEvent(self, e):
        editUser = QAction(QIcon('icons/copy.png'), u'copy', self)
        editUser.triggered.connect(self.copyText)
        menu = QMenu()
        menu.addAction(editUser)
        # menu.addAction(delUser)
        menu.exec_(QCursor.pos())
        e.accept()

    def copyText(self, b):
        # print 'msg copyed'
        cb = QApplication.clipboard()
        cb.setText(self.text)

    def delTextItem(self, b):
        # print 'msg deleted'
        self.listView.takeItem(
            self.listView.indexFromItem(self.listItem).row())


class TextItem(QWidget):

    def __init__(self, listItem, listView, text=DEFAULT_MSG, lr=True, head=DEFAULT_HEAD):
        super(TextItem, self).__init__()
        hbox = QHBoxLayout()
        text = BubbleText(listItem, listView, text, lr)
        head = LabelHead(head)
        head.setFixedSize(50, 50)
        if lr is not True:
            hbox.addSpacerItem(QSpacerItem(
                1, 1, QSizePolicy.Expanding, QSizePolicy.Preferred))

            hbox.addWidget(text)
            hbox.addWidget(head)
        else:
            hbox.addWidget(head)
            hbox.addWidget(text)

            hbox.addSpacerItem(QSpacerItem(
                1, 1, QSizePolicy.Expanding, QSizePolicy.Preferred))

        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setContentsMargins(0, 0, 0, 0)


class LabelHead(QLabel):
    def __init__(self, addr=DEFAULT_HEAD):
        super(LabelHead, self).__init__()
        self.setScaledContents(True)
        self.setReadOnly(True)
        self.setPicture(addr)

    def setReadOnly(self, b):
        self._readOnly = bool(b)

    def setPicture(self, addr):
        self._picAddr = addr
        img = QPixmap(addr)
        self.setPixmap(img)
        return True

    def getPicture(self):
        return self._picAddr


class MsgList(QListWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(MsgList, self).__init__(*args, **kwargs)
        # qssFile.open(QFile.ReadOnly|QFile.Text)
        # print(qssFile.read())
        # self.setStyleSheet(qssFile.read())

    def addTextMsg(self, sz=DEFAULT_MSG, lr=True, head=DEFAULT_HEAD):
        it = QListWidgetItem(self)
        wid = self.size().width()
        item = TextItem(it, self, sz, lr, head)
        # item.setEnabled(False)
        it.setSizeHint(item.sizeHint())
        it.setFlags(Qt.NoItemFlags)
        self.addItem(it)
        self.setItemWidget(it, item)
        self.scrollToItem(it, QAbstractItemView.PositionAtTop)
        # self.setCurrentItem(it)

    def addImageMsg(self, img=DEFAULT_IMG, lr=True, head=DEFAULT_HEAD):
        it = QListWidgetItem(self)
        wid = self.size().width()
        item = BubbleText(it, self, img, lr, head)
        # item.setEnabled(False)
        it.setSizeHint(item.sizeHint())
        it.setFlags(Qt.ItemIsEnabled)
        self.addItem(it)
        self.setItemWidget(it, item)
        self.setCurrentItem(it)


class Ui_Phenom(object):
    def setupUi(self, Phenom):
        Phenom.setObjectName("Phenom")
        Phenom.resize(1424, 698)
        Phenom.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.send_button = QtWidgets.QPushButton(Phenom)
        self.send_button.setGeometry(QtCore.QRect(460, 580, 151, 81))
        self.send_button.setStyleSheet("QPushButton\n"
                                       "{\n"
                                       "background-image: url(:/main_page/icons/main_page/send_button.png);\n"
                                       "}\n"
                                       "QPushButton:hover\n"
                                       "{\n"
                                       "background-image: url(:/main_page/icons/main_page/send_button.png);\n"
                                       "border: 0px\n"
                                       "}\n"
                                       "QPushButton:pressed\n"
                                       "{\n"
                                       "background-image: url(:/main_page/icons/main_page/send_button.png);\n"
                                       "margin: 2px;\n"
                                       "}\n"
                                       "")
        self.send_button.setText("")
        self.send_button.setFlat(True)
        self.send_button.setObjectName("send_button")
        self.chat_le = QtWidgets.QLineEdit(Phenom)
        self.chat_le.setGeometry(QtCore.QRect(20, 590, 375, 61))
        self.chat_le.setLayoutDirection(QtCore.Qt.LayoutDirectionAuto)
        self.chat_le.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "    border-color: rgb(32, 74, 135);\n"
                                   "    border-style: outset;\n"
                                   "    border-width: 2px;\n"
                                   "    border-radius: 10px;\n"
                                   "    padding: 6px;")
        self.chat_le.setText("")
        self.chat_le.setObjectName("chat_le")
        self.chat_widget = QtWidgets.QWidget(Phenom)
        self.messageBox = MsgList(self.chat_widget)
        self.messageBox.setGeometry(QtCore.QRect(21, 21, 550, 520))
        self.messageBox.setMinimumSize(550, 520)
        self.messageBox.setMaximumSize(550, 520)
        # self.messageBox.setAutoScroll(True)
        self.messageBox.setWordWrap(True)
        self.messageBox.setStyleSheet("border: none")
        self.chat_widget.setGeometry(QtCore.QRect(20, 20, 591, 551))
        self.chat_widget.setStyleSheet("/*border-color: rgb(4, 54, 90);*/\n"
                                       "border-style: outset;\n"
                                       "border-width: 2px;\n"
                                       "border-radius: 10px;\n"
                                       "border-color: rgb(32, 74, 135);\n"
                                       " padding: 2px;")
        self.chat_widget.setObjectName("chat_widget")
        self.messageBox.addTextMsg("Hello", False)
        self.label = QtWidgets.QLabel(Phenom)
        self.label.setGeometry(QtCore.QRect(700, 140, 391, 371))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet(
            "background-image: url(:/main_page/icons/main_page/phenom_gif.gif)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.setting_button = QtWidgets.QPushButton(Phenom)
        self.setting_button.setGeometry(QtCore.QRect(1190, 230, 204, 204))
        self.setting_button.setStyleSheet("QPushButton\n"
                                          "{\n"
                                          "background-image:url(:/main_page/icons/main_page/setting_button.png);\n"
                                          "}\n"
                                          "QPushButton:hover\n"
                                          "{\n"
                                          "background-image: url(:/main_page/icons/main_page/setting_button.png);\n"
                                          "border: 0px\n"
                                          "}\n"
                                          "QPushButton:pressed\n"
                                          "{\n"
                                          "background-image: url(:/main_page/icons/main_page/setting_button.png);\n"
                                          "margin: 2px;\n"
                                          "}\n"
                                          "")
        self.setting_button.setText("")
        self.setting_button.setObjectName("setting_button")
        self.mic_button = QtWidgets.QPushButton(Phenom)
        self.mic_button.setGeometry(QtCore.QRect(400, 590, 61, 51))
        self.mic_button.setStyleSheet("QPushButton\n"
                                      "{\n"
                                      "border-image: url(:/main_page/icons/main_page/mic_button.jpg);\n"
                                      "}\n"
                                      "QPushButton:hover\n"
                                      "{\n"
                                      "border-image: url(:/main_page/icons/main_page/mic_button.jpg);\n"
                                      "border: 0.5px\n"
                                      "}\n"
                                      "QPushButton:pressed\n"
                                      "{\n"
                                      "border-image: url(:/main_page/icons/main_page/mic_button.jpg);\n"
                                      "margin: 2px;\n"
                                      "}\n"
                                      "")
        self.mic_button.setText("")
        self.mic_button.setObjectName("mic_button")

        self.retranslateUi(Phenom)
        QtCore.QMetaObject.connectSlotsByName(Phenom)

    def retranslateUi(self, Phenom):
        _translate = QtCore.QCoreApplication.translate
        Phenom.setWindowTitle(_translate("Phenom", "Phenom"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Phenom = QtWidgets.QWidget()
    ui = Ui_Phenom()
    ui.setupUi(Phenom)
    Phenom.show()
    sys.exit(app.exec_())
