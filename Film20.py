import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, \
    QApplication, QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QTabWidget, QMessageBox
from PyQt5.Qt import QMenu, QFrame
import sqlite3


class AddFilm(QWidget):
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


class EditFilm(QWidget):
    def __init__(self, table_item, main_window):
        super().__init__()
        self.id_film = table_item
        self.setWindowTitle('Edit Film')
        self.main_window = main_window
        self.setGeometry(500, 200, 600, 400)
        titles = ('Name', 'Year', 'Duration', 'Genre')
        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()
        id_film, title, year, genre, duration = self.get_info()
        label_titles = [title, year, duration, genre]
        self.lines = []
        for i in range(4):
            label = QLabel(titles[i], self)
            label.setStyleSheet('''font-size: 20px''')
            label.setGeometry(20, 60 * (i + 1), 300, 30)
            if i == 3:
                break
            line = QLineEdit(str(label_titles[i]), self)
            line.setStyleSheet('''font-size: 20px''')
            line.setGeometry(100, 60 * (i + 1), 400, 30)
            self.lines.append(line)
        self.btn_genre = QPushButton(genre, self)
        self.btn_genre.setGeometry(100, 60 * (i + 1), 400, 30)
        self.btn_genre.setStyleSheet('''font-size: 20px''')
        self.add_actions()

        self.add_btn = QPushButton('Edit', self)
        self.add_btn.setGeometry(300, 60 * (i + 2), 200, 30)
        self.add_btn.setStyleSheet('''font-size^ 20px''')
        self.add_btn.clicked.connect(self.command)

        self.line_error = QLabel('', self)
        self.line_error.setGeometry(20, 60 * (i + 3), 500, 30)
        self.line_error.setStyleSheet('''font-size: 20px''')

    def get_info(self):
        res = self.cur.execute("""SELECT * FROM films WHERE id = ?""", (self.id_film, )).fetchone()
        id_film, title, year, genre, duration = res
        genre = self.cur.execute("""SELECT title FROM genres WHERE id = ?""", (genre, )).fetchone()[0]
        return id_film, title, year, genre, duration

    def add_actions(self):
        genres = self.cur.execute("""SELECT title FROM genres""").fetchall()
        menu = QMenu()
        for item in genres:
            menu.addAction(item[0], self.change_text)
        self.btn_genre.setMenu(menu)

    def change_text(self):
        sender = self.sender()
        self.btn_genre.setText(sender.text())

    def command(self):
        genre = self.btn_genre.text()
        title, year, duration = [line.text() for line in self.lines]
        genre_id = self.cur.execute("""SELECT id FROM genres WHERE title = ?""", (genre, )).fetchone()[0]
        self.cur.execute("""UPDATE films
        SET title = ?,
        genre = ?,
        duration = ?,
        year = ?
        WHERE films.id = ?""", (title, genre_id, duration, year, self.id_film))
        self.con.commit()
        self.main_window.update_table()
        self.close()


class AddGenre(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Add Genre')
        self.setGeometry(500, 200, 500, 600)
        self.label = QLabel('Input name of genre', self)
        self.label.setGeometry(20, 40, 200, 40)
        self.label.setStyleSheet('''font-size: 15px''')

        self.edit_line = QLineEdit(self)
        self.edit_line.setGeometry(230, 40, 200, 40)
        self.edit_line.setStyleSheet('''font-size: 15px''')

        self.add_btn = QPushButton('Add', self)
        self.add_btn.setGeometry(300, 80, 200, 40)
        self.add_btn.setStyleSheet('''font-size: 20px''')
        self.add_btn.clicked.connect(self.command_add_genre)

    def command_add_genre(self):
        genre = self.edit_line.text()
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        cur.execute("""INSERT INTO genres(title)
        VALUES(?)""", (genre, ))
        con.commit()
        self.main_window.update_table_genres()
        self.close()


class EditGenre(QWidget):
    def __init__(self, id_genre, main_window):
        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()
        previous_title = self.cur.execute("""SELECT title FROM genres WHERE id = ?""", (id_genre, )).fetchone()[0]
        super().__init__()
        self.setWindowTitle('Edit genre')
        self.setGeometry(500, 200, 500, 600)
        self.id_genre = id_genre
        self.main_window = main_window

        self.label = QLabel('Input name of genre', self)
        self.label.setGeometry(20, 40, 200, 40)
        self.label.setStyleSheet('''font-size: 15px''')

        self.edit_line = QLineEdit(previous_title, self)
        self.edit_line.setGeometry(230, 40, 200, 40)
        self.edit_line.setStyleSheet('''font-size: 15px''')

        self.add_btn = QPushButton('Edit', self)
        self.add_btn.setGeometry(300, 80, 200, 40)
        self.add_btn.setStyleSheet('''font-size: 20px''')
        self.add_btn.clicked.connect(self.command_add_genre)

    def command_add_genre(self):
        title = self.edit_line.text()
        self.cur.execute("""UPDATE genres
        SET title = ?
        WHERE id = ?""", (title, self.id_genre))
        self.con.commit()
        self.main_window.update_table_genres()
        self.close()


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
        self.btn_add_genre.clicked.connect(self.add_genre)
        self.btn_edit_genre.clicked.connect(self.edit_genre)
        self.btn_delete_genre.clicked.connect(self.delete_genre)

        self.btn_add_film = QPushButton('Add film')
        self.btn_delete_film = QPushButton('Delete film')
        self.btn_edit_film = QPushButton('Edit film')
        self.btn_edit_film.clicked.connect(self.edit_film)
        self.btn_delete_film.clicked.connect(self.delete_film)
        self.btn_add_film.clicked.connect(self.add_film)

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
            tab_layout.addLayout(box_table, stretch=9999)
            tab.setLayout(tab_layout)
            self.tab.addTab(tab, btn_tabs[i])
        self.update_table()
        self.update_table_genres()

    def update_table(self):
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT films.id, films.title, films.year, genres.title, films.duration FROM films
        LEFT JOIN genres ON genres.id == films.genre""").fetchall()
        self.table_widget_film.setRowCount(len(res))
        titles = [description[0] for description in cur.description]
        if res:
            self.table_widget_film.setColumnCount(len(res[0]))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table_widget_film.setItem(i, j, QTableWidgetItem(str(val)))
            self.table_widget_film.setHorizontalHeaderLabels(titles)
        con.close()

    def update_table_genres(self):
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM genres""").fetchall()
        self.table_widget_genre.setRowCount(len(res))
        if res:
            titles = [description[0] for description in cur.description]
            self.table_widget_genre.setColumnCount(len(res[0]))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table_widget_genre.setItem(i, j, QTableWidgetItem(str(val)))
            self.table_widget_genre.setHorizontalHeaderLabels(titles)
        con.close()

    def add_film(self):
        self.widget_add_film = AddFilm(self)
        self.widget_add_film.show()

    def edit_film(self):
        row, column = self.table_widget_film.currentRow(), self.table_widget_film.currentColumn()
        if row < 0 or column < 0:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText('Select cell to edit')
            message.exec()
            return
        table_item = self.table_widget_film.item(row, 0).text()
        self.widget_edit_film = EditFilm(table_item, self)
        self.widget_edit_film.show()

    def delete_film(self):
        row = self.table_widget_film.currentRow()
        widget_item = self.table_widget_film.item(row, 0)
        try:
            id_film = widget_item.text()
            valid = QMessageBox.question(self, 'Delete film', 'Are you sure?', QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                con = sqlite3.connect('films_db.sqlite')
                cur = con.cursor()
                cur.execute('DELETE FROM films WHERE id=?', (id_film, ))
                con.commit()
                self.update_table()
        except AttributeError:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setGeometry(800, 600, 200, 40)
            message.setText('Select cell to delete')
            message.exec()

    def add_genre(self):
        self.widget_add_genre = AddGenre(self)
        self.widget_add_genre.show()

    def edit_genre(self):
        row, column = self.table_widget_genre.currentRow(), self.table_widget_genre.currentColumn()
        if row < 0 or column < 0:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText('Select cell to edit')
            message.exec()
            return
        table_item = self.table_widget_genre.item(row, 0).text()
        self.widget_edit_genre = EditGenre(table_item, self)
        self.widget_edit_genre.show()

    def delete_genre(self):
        row, column = self.table_widget_genre.currentRow(), self.table_widget_genre.currentColumn()
        if row < 0 or column < 0:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText('Select cell to edit')
            message.exec()
            return
        id_genre = self.table_widget_genre.item(row, 0).text()
        valid = QMessageBox.question(self, 'Delete genre', 'Are you sure?', QMessageBox.Yes, QMessageBox.No)
        if valid:
            con = sqlite3.connect('films_db.sqlite')
            cur = con.cursor()
            cur.execute("""DELETE FROM genres WHERE id = ?""", (id_genre, ))
            con.commit()
            self.update_table_genres()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = FilmTable()
    exe.show()
    sys.exit(app.exec_())
