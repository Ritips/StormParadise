import sys
import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.Qt import QMenu


class FilterGenre(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()

        self.setGeometry(400, 200, 1000, 800)
        self.setWindowTitle('Filter Genre')
        self.setStyleSheet('''font-size: 15px''')

        self.btn_genre = QPushButton(self)
        self.btn_genre.setGeometry(10, 20, 200, 40)
        self.add_actions()
        self.start_filet = QPushButton('Filter', self)
        self.start_filet.setGeometry(10, 100, 200, 40)
        self.start_filet.clicked.connect(self.update_table_widget)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(230, 20, 750, 600)

    def add_actions(self):
        menu = QMenu()
        genres = self.cur.execute("""SELECT title FROM genres""").fetchall()
        for genre in genres:
            menu.addAction(genre[0], self.change_text)
        self.btn_genre.setMenu(menu)

    def change_text(self):
        self.btn_genre.setText(self.sender().text())

    def update_table_widget(self):
        message = QMessageBox()
        message.setWindowTitle('Error')
        if not self.btn_genre.text():
            message.setText('Select genre')
            message.exec()
            return
        id_genre = self.cur.execute("""SELECT id FROM genres WHERE title=?""", (self.btn_genre.text(), )).fetchone()[0]
        res = self.cur.execute("""SELECT films.title, films.genre, films.year FROM films
        WHERE films.genre=?""", (id_genre, )).fetchall()
        if not res:
            message.setText('Nothing was found')
            message.exec()
            return
        self.table_widget.setRowCount(len(res))
        self.table_widget.setColumnCount(len(res[0]))
        for i, val in enumerate(res):
            for j, el in enumerate(val):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(el)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = FilterGenre()
    exe.show()
    sys.exit(app.exec_())
