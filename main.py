from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import uic
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 400, 400, 400)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        db_data = QSqlTableModel(self, db)
        db_data.setTable('coffee')
        db_data.select()
        self.table.setModel(db_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
