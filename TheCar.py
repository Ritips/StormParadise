import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QRectF


class Car(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)
        self.setMouseTracking(True)
        self.setWindowTitle('text')
        self.coord = (40, 40)

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if 20 <= x <= 460 and 20 <= y <= 460:
            self.coord = (x, y)
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_car(qp)
        qp.end()

    def draw_car(self, qp):  # download image https://disk.yandex.ru/i/qheMH7u8JGfeQA
        x, y = self.coord
        qp.drawImage(QRectF(x, y, 30, 30), QImage('TheBestCar.PNG'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Car()
    exe.show()
    sys.exit(app.exec_())
