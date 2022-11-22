import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QInputDialog, QFileDialog


class TravelDiction(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Справочник Путешественника')

        self.name_file = self.ask_name_file()
        self.create_table_flags()
        self.create_table_languages()
        self.create_main_table()

        self.setGeometry(300, 300, 500, 500)
        self.btn1 = QPushButton(self)
        self.btn1.move(100, 100)
        self.btn1.resize(200, 50)
        self.btn1.setStyleSheet('''font-size: 20px''')
        self.btn1.setText('add information')
        self.btn1.clicked.connect(self.button_function)

        # self.btn2 = QPushButton('test', self)
        # self.btn2.move(400, 400)
        # self.btn2.clicked.connect(self.test_function)

    def test_function(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM info""")
        for i in res:
            print(i)

    def add_info(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        country = QInputDialog.getText(self, 'Name Country', 'Input name of country')[0]
        official_language = QInputDialog.getText(self, 'language', 'Input name of language')[0]
        year = QInputDialog.getInt(self, 'Year', 'When was it founded? (Input year)')[0]
        link_file = QFileDialog.getOpenFileName(self, 'Flag', 'Choose flag of country')
        cur.execute("""INSERT INTO languages(title)
        VALUES(?)""", (official_language, ))
        id_language = cur.execute("""SELECT id FROM languages WHERE title=?""", (official_language, )).fetchone()[0]
        cur.execute("""INSERT INTO flags(link)
        VALUES(?)""", (link_file[0], ))

        id_flag = cur.execute("""SELECT id FROM flags WHERE link=?""", (link_file[0], )).fetchone()[0]
        cur.execute("""INSERT INTO info(title, year, language_id, flag_id)
        VALUES(?, ?, ?, ?)""", (country, year, id_language, id_flag))
        con.commit()

    def button_function(self):
        to_do, ok_pressed = QInputDialog.getItem(self, 'Functions', 'Select Function',
                                                 ('add', ), 1, False)
        if not ok_pressed:
            return
        self.add_info()

    def create_table_languages(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS languages(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT);''')
        con.commit()

    def create_table_flags(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS flags(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        link TEXT);''')
        con.commit()

    def create_main_table(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS info(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        year INTEGER,
        title TEXT,
        language_id INTEGER,
        flag_id INTEGER,
        FOREIGN KEY (language_id) REFERENCES languages (id)
        FOREIGN KEY (flag_id) REFERENCES flags (id)
        );''')
        con.commit()

    def ask_name_file(self):
        while True:
            name_file = QInputDialog.getText(self, 'File Name', 'Input File Name')[0]
            if name_file:
                return name_file


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = TravelDiction()
    exe.show()
    sys.exit(app.exec_())
