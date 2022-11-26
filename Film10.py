import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, \
    QApplication, QMainWindow, QWidget, QLineEdit, QLabel
from PyQt5.Qt import QMenu
import sqlite3


class AddElement(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(500, 200, 600, 400)
        self.setWindowTitle('Add Element')
        titles = ('Name', 'Year', 'Duration', 'Genre')
        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()
        self.lines = []
        for i in range(4):
            label = QLabel(titles[i], self)
            label.setStyleSheet('''font-size: 20px''')
            label.setGeometry(20, 60 * (i + 1), 300, 30)
            if i == 3:
                break
            line = QLineEdit(self)
            line.setStyleSheet('''font-size: 20px''')
            line.setGeometry(100, 60 * (i + 1), 400, 30)
            self.lines.append(line)
        self.btn_genre = QPushButton(self)
        self.btn_genre.setGeometry(100, 60 * (i + 1), 400, 30)
        self.btn_genre.setStyleSheet('''font-size: 20px''')
        self.add_actions()

        self.add_btn = QPushButton('Add', self)
        self.add_btn.setGeometry(300, 60 * (i + 2), 200, 30)
        self.add_btn.setStyleSheet('''font-size^ 20px''')
        self.add_btn.clicked.connect(self.command)

        self.line_error = QLabel('', self)
        self.line_error.setGeometry(20, 60 * (i + 3), 500, 30)
        self.line_error.setStyleSheet('''font-size: 20px''')

    def change_text(self):
        sender = self.sender()
        self.btn_genre.setText(sender.text())

    def command(self):
        self.line_error.setText('')
        self.btn_genre.text()
        texts = list(map(lambda x: x.text(), (self.lines + [self.btn_genre])))
        if list(filter(lambda x: not x, texts)):
            self.line_error.setText('Error: empty lines were found')
            return
        try:
            num1, num2 = int(texts[1]), int(texts[2])
            if num1 < 0 or num2 < 0:
                self.line_error.setText('Error: year or duration less than 0')
                return
        except ValueError:
            self.line_error.setText('Error: year or duration is not integer')
            return
        id_genre = self.cur.execute("""SELECT id FROM genres WHERE title = ?""", (texts[-1], )).fetchone()[0]
        self.cur.execute("""INSERT INTO films (title, year, duration, genre)
        VALUES(?, ?, ?, ?)""", tuple(texts[:-1] + [id_genre]))
        self.con.commit()
        self.main_window.update_table()
        self.close()

    def add_actions(self):
        genres = self.cur.execute("""SELECT title FROM genres""").fetchall()
        menu = QMenu()
        for item in genres:
            menu.addAction(item[0], self.change_text)
        self.btn_genre.setMenu(menu)


class FilmTable(QMainWindow):
    def __init__(self):
        super(FilmTable, self).__init__()
        self.setGeometry(500, 200, 1000, 600)
        self.setWindowTitle('Film library')
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 75, 900, 500)

        self.add_btn = QPushButton('Add', self)
        self.add_btn.setGeometry(50, 10, 100, 40)
        self.add_btn.setStyleSheet('''font-size: 15px''')
        self.add_btn.clicked.connect(self.add_element)
        self.update_table()
        self.add_element = AddElement(self)

    def add_element(self):
        self.add_element = AddElement(self)
        self.add_element.show()

    def update_table(self):
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT films.id, films.title, films.year, genres.title, films.duration FROM films
        LEFT JOIN genres ON genres.id == films.genre""").fetchall()
        self.table_widget.setRowCount(len(res))
        titles = [description[0] for description in cur.description]
        if res:
            self.table_widget.setColumnCount(len(res[0]))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(val)))
            self.table_widget.setHorizontalHeaderLabels(titles)
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = FilmTable()
    exe.show()
    sys.exit(app.exec_())
