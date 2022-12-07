import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, \
    QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox


class Sql(QWidget):
    def __init__(self):
        super().__init__()
        self.main_box = QVBoxLayout()
        self.setGeometry(400, 200, 1000, 800)
        self.setLayout(self.main_box)
        self.create_alphabet_buttons()

    def create_alphabet_buttons(self):
        btn_layout = QHBoxLayout()
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            btn = QPushButton(letter)
            btn_layout.addWidget(btn)
        self.main_box.addLayout(btn_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Sql()
    exe.show()
    sys.exit(app.exec_())
