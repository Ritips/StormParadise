import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.Qt import QMenu


class SearchFilms(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''font-size:15px''')
        self.setWindowTitle('Search Film')
        self.setGeometry(400, 200, 1000, 100)
        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)

        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()

        self.select_btn = QPushButton('duration', self)
        self.search_btn = QPushButton('SEARCH', self)
        self.line_edit1 = QLineEdit(self)
        self.line_edit_id = QLineEdit(self)
        self.line_edit_title = QLineEdit(self)
        self.line_edit_year = QLineEdit(self)
        self.line_edit_genre = QLineEdit(self)
        self.line_edit_duration = QLineEdit(self)
        self.sp_lines = [self.line_edit_id, self.line_edit_title,
                         self.line_edit_year, self.line_edit_genre, self.line_edit_duration]
        self.create_interface()
        self.search_btn.clicked.connect(self.search)

    def create_interface(self):
        self.create_actions()
        titles = ['ID', 'TITLE', 'YEAR OF ISSUE', 'GENRE', 'DURATION']

        search_box = QHBoxLayout()
        search_box.addWidget(self.select_btn)
        search_box.addWidget(self.line_edit1)
        search_box.addWidget(self.search_btn)

        output_box = QHBoxLayout()
        output_box.addLayout(search_box, stretch=0)
        for i in range(5):
            box = QHBoxLayout()
            box.addWidget(QLabel(titles[i]))
            box.addWidget(self.sp_lines[i])
            self.sp_lines[i].setReadOnly(True)
            self.sp_lines[i].resize(200, 40)
            output_box.addLayout(box, stretch=0)
        self.main_box.addLayout(output_box, stretch=0)

    def create_actions(self):
        menu = QMenu()
        variety = ('year', 'title', 'duration')
        for el in variety:
            menu.addAction(el, self.change_text)
        self.select_btn.setMenu(menu)

    def change_text(self):
        self.select_btn.setText(self.sender().text())

    def search(self):
        condition_key = self.select_btn.text()
        condition_value = self.line_edit1.text()
        if not condition_value:
            message = QMessageBox()
            message.setText('Invalid input')
            message.setWindowTitle('Error')
            message.exec()
            return
        res = self.cur.execute(f"""SELECT * FROM films
        LEFT JOIN genres ON films.genre = genres.id
        WHERE films.{condition_key} = ?
        ORDER BY films.id""", (condition_value, )).fetchone()
        if not res:
            message = QMessageBox()
            message.setText('Nothing was found')
            message.setWindowTitle('Error')
            message.exec()
            return
        id_film, title, year, id_genre, duration, id_genre, genre_title = res
        self.line_edit_id.setText(str(id_film))
        self.line_edit_year.setText(str(year))
        self.line_edit_genre.setText(genre_title)
        self.line_edit_title.setText(title)
        self.line_edit_duration.setText(str(duration))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = SearchFilms()
    exe.show()
    sys.exit(app.exec_())
