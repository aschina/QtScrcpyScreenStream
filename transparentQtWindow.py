import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

app = QApplication(sys.argv)


class TransparentWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.windowWidth = 200  # 获得当前窗口宽
        self.windowHeight = 430  # 获得当前窗口高
        self.resize(self.windowWidth, self.windowHeight)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.windowWidth, self.windowHeight)
        self.onClick = None

    def updateImage(self, image):
        pixmap = image.toqpixmap()
        self.label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            print(self.m_Position)
            if self.onClick:
                self.m_Position.x = self.m_Position.x()
                self.m_Position.y = self.m_Position.y()
                self.onClick(self.m_Position)
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
        elif event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
