from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractItemView
import sys
import sqlite3
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.base = sqlite3.connect('coffee.sqlite')
        self.cur = self.base.cursor()
        self.initUi()

    def initUi(self):
        uic.loadUi('main.ui', self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.update_values()

    def update_values(self):
        data = self.cur.execute("SELECT * FROM coffee").fetchall()
        if not data:
            return
        self.titles = [desc[0] for desc in self.cur.description]

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels(self.titles)
        for index, value in enumerate(data):
            for base_index, base_value in enumerate(value):
                self.table.setItem(index, base_index, QTableWidgetItem(str(base_value)))
        self.table.resizeColumnsToContents()

        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
