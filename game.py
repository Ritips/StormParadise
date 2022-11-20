import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPolygonF
from PyQt5.QtCore import QPointF
import random


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(350, 350, 800, 800)
        self.setWindowTitle('First')
        self.setMouseTracking(True)
        self.coord = [0, 0]
        self.mouse_btn = None
        self.key_btn = None

    def mouseMoveEvent(self, event):
        self.coord[0] = event.x()
        self.coord[1] = event.y()

    def mousePressEvent(self, event):
        self.mouse_btn = event.button()
        self.repaint()

    def keyPressEvent(self, event):
        self.key_btn = event.key()
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        r, g, b = [random.randint(0, 255) for _ in range(3)]
        qp.setBrush(QColor(r, g, b))
        if self.mouse_btn == 2:
            self.mouse_btn = None
            self.draw_square(qp)
        elif self.mouse_btn == 1:
            self.mouse_btn = None
            self.draw_round(qp)
        elif self.key_btn == 32:
            self.key_btn = None
            self.draw_triangle(qp)

        qp.end()

    def draw_square(self, qp):
        side = random.randint(25, 300)
        qp.drawRect(self.coord[0], self.coord[1], side, side)

    def draw_round(self, qp):
        radius = random.randint(25, 300)
        qp.drawEllipse(self.coord[0], self.coord[1], radius, radius)

    def draw_triangle(self, qp):
        side = random.randint(25, 300)
        points = (QPointF(self.coord[0], self.coord[1]),
                  QPointF(self.coord[0] - side, self.coord[1] + side * 3 ** 0.5),
                  QPointF(self.coord[0] + side, self.coord[1] + side * 3 ** 0.5)
                  )
        poly = QPolygonF(points)
        qp.drawPolygon(poly)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Test()
    exe.show()
    sys.exit(app.exec_())
