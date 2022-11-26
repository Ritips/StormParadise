import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, \
    QApplication, QMainWindow, QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QTabWidget, QInputDialog
from PyQt5.Qt import QMenu, QFrame
import sqlite3


class FilmTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 1000, 800)
        self.setWindowTitle('Film Library')
        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)

        self.tab = QTabWidget()
        self.btn_films = QPushButton('Films')
        self.btn_genres = QPushButton('Genres')

        self.btn_add_genre = QPushButton('Add genre')
        self.btn_edit_genre = QPushButton('Edit genre')
        self.btn_delete_genre = QPushButton('Delete genre')

        self.btn_add_film = QPushButton('Add film')
        self.btn_delete_film = QPushButton('Delete film')
        self.btn_edit_film = QPushButton('Edit film')

        self.table_widget_film = QTableWidget()
        self.table_widget_genre = QTableWidget()

        self.main_box.addWidget(self.tab)
        self.create_tabs()

    def create_tabs(self):
        sp_film = [self.btn_add_film, self.btn_edit_film, self.btn_delete_film]
        sp_genre = [self.btn_add_genre, self.btn_edit_genre, self.btn_delete_genre]
        table_widget_sp = [self.table_widget_film, self.table_widget_genre]
        btn_tabs = [self.btn_films.text(), self.btn_genres.text()]
        sp_tabs = [sp_film, sp_genre]
        for i in range(2):
            box_btn = QHBoxLayout()
            box_table = QVBoxLayout()
            box_table.addWidget(table_widget_sp[i])
            for btn in sp_tabs[i]:
                box_btn.addWidget(btn)
            tab = QFrame()
            tab_layout = QVBoxLayout()
            tab_layout.addLayout(box_btn, stretch=100)
            tab_layout.addLayout(box_table, stretch=800)
            tab.setLayout(tab_layout)
            self.tab.addTab(tab, btn_tabs[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = FilmTable()
    exe.show()
    sys.exit(app.exec_())





