import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap


class UFO(QMainWindow):  # https://disk.yandex.ru/d/OTM99oOf4CSiCQ  -- ссылка на exe
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UFO')
        self.setGeometry(300, 300, 500, 500)
        self.pixmap = QPixmap('TheBestCar2.PNG')  # https://disk.yandex.ru/i/ykh32F5gXY7s1A -- ссылка на картинку
        self.ufo = QLabel(self)
        self.x, self.y = 250, 250
        self.ufo.move(self.x, self.y)
        self.ufo.resize(self.pixmap.width(), self.pixmap.height())
        self.ufo.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777234:
            self.x, self.y = self.x - 10, self.y
        if key == 16777235:
            self.x, self.y = self.x, self.y - 10
        if key == 16777236:
            self.x, self.y = self.x + 10, self.y
        if key == 16777237:
            self.x, self.y = self.x, self.y + 10
        self.ufo.move(self.x % 500, self.y % 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = UFO()
    exe.show()
    sys.exit(app.exec_())
