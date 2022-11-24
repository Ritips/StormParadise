import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, \
    QInputDialog, QMenu, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class ExtendButton(QPushButton):
    def __init__(self, id_object=None):
        super().__init__()
        self.id_object = id_object

    def get_id_object(self):
        return self.id_object


class ShowInfoBook(QWidget):
    def __init__(self, id_book, filename):
        super().__init__()
        uic.loadUi('show_information.ui', self)  # https://disk.yandex.ru/d/wv9y5_WZ6XacrQ
        self.filename = filename
        self.id_book = id_book
        self.load_book()

    def load_book(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        book = cur.execute("""SELECT * FROM books
        LEFT JOIN authors ON books.id_author == authors.id
        WHERE books.id = ?""", (self.id_book, )).fetchone()
        self.title_book.setText(book[1])
        self.title_author.setText(book[-1])
        self.year.setText(str(book[-3]))
        self.genre.setText(book[-4])
        pixmap = QPixmap(book[3])
        self.label_pixmap.setPixmap(pixmap)


class CatalogLibrary(QWidget):
    def __init__(self, file_name='CatalogLibrary.db'):
        super().__init__()
        uic.loadUi('librarycatalog.ui', self)  # https://disk.yandex.ru/d/wCRiuyF4q-K3eg
        self.setWindowTitle('CatalogLibrary')
        self.setGeometry(400, 180, 1000, 800)

        self.btn.resize(100, 50)
        self.btn.move(50, 50)
        self.btn.setStyleSheet('''font-size: 20px''')
        menu = QMenu()
        menu.addAction('Author', self.set_author)
        menu.addAction('Book', self.set_title)
        self.btn.setMenu(menu)

        self.search_text.move(50, 130)
        self.search_text.resize(300, 50)
        self.search_text.setStyleSheet('''font-size: 20px''')

        self.search_btn.move(650, 50)
        self.search_btn.resize(200, 100)
        self.search_btn.setStyleSheet('''font-size: 20px''')
        self.search_btn.clicked.connect(self.search)

        self.file_name = file_name

    def search(self):
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        request = self.search_text.text()
        if self.btn.text() == 'Author':
            res = cur.execute(f"""SELECT * FROM books
            LEFT JOIN authors ON books.id_author == authors.id
            WHERE authors.title LIKE '%{request}%'""")
        else:
            res = cur.execute(f"""SELECT * FROM books
            LEFT JOIN authors ON authors.id == books.id_author
            WHERE books.title LIKE '%{request}%'""")
        row = -1
        self.table_widget.setColumnCount(1)
        self.table_widget.setRowCount(0)
        for i in res:
            row += 1
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            btn = ExtendButton(id_object=i[0])
            btn.setText(i[1])
            btn.clicked.connect(self.show_info)
            self.table_widget.setCellWidget(row, 0, btn)
        con.close()

    def show_info(self):
        id_book = self.sender().get_id_object()
        self.show_information = ShowInfoBook(id_book, self.file_name)
        self.show_information.show()

    def set_author(self):
        self.btn.setText('Author')

    def set_title(self):
        self.btn.setText('Book')


class CreateDataBase(QWidget):
    def __init__(self, file_name='CatalogLibrary.db'):
        print(self.__class__.__name__, file_name)
        super().__init__()
        self.setWindowTitle('Create DataBase')
        self.setGeometry(800, 150, 300, 400)

        self.con = sqlite3.connect(file_name)
        self.cur = self.con.cursor()
        self.create_table_authors()
        self.create_table_books()

        self.btn_author = QPushButton('Add Author', self)
        self.btn_book = QPushButton('Add Book', self)
        sp = [self.btn_author, self.btn_book]
        for i in range(len(sp)):
            button = sp[i]
            button.setStyleSheet('''font-size: 20px''')
            button.resize(200, 50)
            button.move(50, 60 * (i + 1))
        self.btn_book.clicked.connect(self.add_book)
        self.btn_author.clicked.connect(self.add_author)

    def add_author(self):
        name_author = QInputDialog.getText(self, 'Author', "Input author's name")[0]
        if name_author:
            self.cur.execute("""INSERT INTO authors(title)
            VALUES(?)""", (name_author, ))

    def add_book(self):
        name_book = QInputDialog.getText(self, 'Book', 'Input name of the book')[0]
        if not name_book:
            return
        genre = QInputDialog.getText(self, 'Genre', 'Input genre of the book')[0]
        year = QInputDialog.getInt(self, 'Year', 'Input year of publication of the book')[0]
        authors = self.cur.execute("""SELECT title FROM authors""").fetchall()
        image_file = ''
        if authors:
            valid = QMessageBox.question(self, '', 'Do you want to select author from the table of authors?',
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                items = [name[0] for name in authors]
                name_author = QInputDialog.getItem(self, 'Selection', 'Select author', items, 1, False)[0]
            else:
                name_author = QInputDialog.getText(self, 'Author', "Input author's name")[0]
        else:
            name_author = QInputDialog.getText(self, 'Author', "Input author's name")[0]
            is_added = self.cur.execute("""SELECT title FROM authors WHERE title=?""", (name_author, )).fetchone()
            if not is_added and name_author:
                self.cur.execute("""INSERT INTO authors (title)
                VALUES(?)""", (name_author, ))
        if not name_author:
            return
        id_author = self.cur.execute("""SELECT id FROM authors WHERE title=?""", (name_author, )).fetchone()[0]
        valid = QMessageBox.question(self, '', 'Do you want to add image?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            image_file = QFileDialog.getOpenFileName(self, 'Image', '')[0]
        self.cur.execute("""INSERT INTO books(title, id_author, id_image, genre, year)
        VALUES(?, ?, ?, ?, ?)""", (name_book, id_author, image_file, genre, year))

    def create_table_authors(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT);""")

    def create_table_books(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT,
        id_author INTEGER,
        id_image INTEGER,
        genre TEXT,
        year INTEGER,
        FOREIGN KEY (id_author) REFERENCES authors (id)
        );""")

    def closeEvent(self, event):
        valid = QMessageBox.question(self, '', 'Save changes?', QMessageBox.Yes, QMessageBox.No)
        if valid:
            self.con.commit()
        self.con.close()


class MainClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main')
        self.setGeometry(500, 500, 300, 200)
        self.btn1 = QPushButton('Create DataBase', self)
        self.btn2 = QPushButton('Search info', self)
        self.file_name = None
        sp = [self.btn1, self.btn2]
        for i in range(len(sp)):
            button = sp[i]
            button.move(50, 60 * (i + 1))
            button.resize(200, 50)
            button.setStyleSheet('''font-size: 20px''')
            button.clicked.connect(self.add_database) if not i else button.clicked.connect(self.start_searching_info)

    def add_database(self):
        self.file_name = QInputDialog.getText(self, 'Name of Database', 'Input name of database')[0]
        self.file_name = 'CatalogLibrary.db' if not self.file_name else self.file_name
        self.add_data = CreateDataBase(file_name=self.file_name)
        self.add_data.show()

    def start_searching_info(self):
        to_do = QInputDialog.getItem(self, 'Selection of action', 'Select action',
                                     ('Open Previous database', 'Open database from directory',
                                      'Input name of database'), 1, False)[0]
        if not to_do:
            return
        elif to_do == 'Open Previous database':
            self.file_name = self.file_name if self.file_name else 'CatalogLibrary.db'
        elif to_do == 'Open database from directory':
            file_name = QFileDialog.getOpenFileName(self, '', '')[0]
            self.file_name = file_name if file_name else 'CatalogLibrary.db'
        elif to_do == 'Input name of database':
            file_name = QInputDialog.getText(self, 'Name of database', 'Input name of database to open')[0]
            self.file_name = file_name if file_name else 'CatalogLibrary.db'
        self.search_data = CatalogLibrary(self.file_name)
        self.search_data.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = MainClass()
    exe.show()
    sys.exit(app.exec_())
