import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow
import random


class Run(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('the light striking all over the world')
        self.setGeometry(400, 400, 600, 600)
        self.setMouseTracking(True)
        self.btn = QPushButton(self)
        self.btn.setText('Run')
        self.x, self.y = (100, 100)
        self.btn.setGeometry(self.x, self.y, 40, 40)

    def mouseMoveEvent(self, event):
        delta_x = random.randint(100, 200)
        delta_y = random.randint(100, 200)
        x, y = (event.x(), event.y())
        if abs(x - self.x) < 40 or abs(y - self.y) < 40:
            self.x, self.y = x, y
            self.x = self.x + delta_x if self.x < 560 - delta_x else self.x - delta_x
            self.y = self.y + delta_y if self.y < 560 - delta_y else self.y - delta_y
            self.btn.setGeometry(self.x, self.y, 40, 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Run()
    exe.show()
    sys.exit(app.exec_())
