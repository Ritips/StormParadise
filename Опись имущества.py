import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QLabel


class Solution(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)
        self.name_file = None
        self.input_file_name()

        self.btn_1 = QPushButton(self)
        self.btn_1.setGeometry(100, 100, 300, 50)
        self.btn_1.setText('Добавить комнату')
        self.btn_1.setStyleSheet('''font-size: 20px''')
        self.btn_1.clicked.connect(self.command_add_room)

        self.btn_2 = QPushButton(self)
        self.btn_2.setGeometry(100, 200, 300, 50)
        self.btn_2.setText('Добавить предмет')
        self.btn_2.setStyleSheet('''font-size: 20px''')
        self.btn_2.clicked.connect(self.command_add_item)

        self.label = QLabel(self)
        self.label.setStyleSheet('''font-size: 10px''')
        self.label.setGeometry(50, 300, 300, 20)

        self.create_rooms_table()
        self.create_genre_table()
        self.create_items_table()

    def command_add_room(self):
        self.label.setText('')
        name_room = QInputDialog.getText(self, 'Room', 'Введите название комнаты')[0]
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO table_rooms(title)
        VALUES('{name_room}')""")
        con.commit()

    def command_add_item(self):
        self.label.setText('')
        name_room = QInputDialog.getText(self, 'Room', 'Введите название комнаты')[0]
        text = QInputDialog.getText(self, 'Item', 'Введите название предмета, год покупки, тип (через ;)')[0].split(';')
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        try:
            name, year, genre = text
            room_id = cur.execute(f"""SELECT id FROM table_rooms WHERE title='{name_room}'""").fetchone()[0]

            cur.execute(f"""INSERT INTO genres(title)
            VALUES(?)""", (genre, ))

            genre_id = cur.execute(f"""
            SELECT id FROM genres
            WHERE title='{genre}'""").fetchone()[0]

            cur.execute("""INSERT INTO items(title, year, genre, room_id)
            VALUES(?, ?, ?, ?)""", (name, year, genre_id, room_id))
            con.commit()

        except Exception as er:
            self.label.setText(f'{er}')

    def create_genre_table(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS genres(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT);""")
        con.commit()

    def create_rooms_table(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS table_rooms(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                title TEXT);""")
        con.commit()

    def create_items_table(self):
        con = sqlite3.connect(self.name_file)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT,
        year INTEGER,
        genre INTEGER,
        room_id INTEGER NOT NULL,
        FOREIGN KEY (genre) REFERENCES genres (id) FOREIGN KEY (room_id) REFERENCES table_rooms (id)
        );""")
        con.commit()

    def input_file_name(self):
        while not self.name_file:
            self.name_file = QInputDialog.getText(self, 'File of Database', 'Введите название файла')[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Solution()
    exe.show()
    sys.exit(app.exec_())
