from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, \
    QAbstractItemView
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
        self.edit_button.clicked.connect(self.edit_table)

    def edit_table(self):
        self.editor = Table_Editor(self)
        self.editor.show()

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


class Table_Editor(QWidget):
    def __init__(self, up_table):
        super().__init__()
        self.base = sqlite3.connect('coffee.sqlite')
        self.cur = self.base.cursor()
        self.up_table = up_table
        self.initUi()

    def initUi(self):
        uic.loadUi('allEditCoffeeForm.ui', self)
        self.update_values()

        self.table.itemChanged.connect(self.itemHasChanged)
        self.save_button.clicked.connect(self.save_changes)
        self.newline_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)

        self.modified = {}

    def itemHasChanged(self, item):
        if item.row() + 1 in self.modified:
            self.modified[item.row() + 1][self.titles[item.column()]] = item.text()
        else:
            self.modified[item.row() + 1] = {
                self.titles[item.column()]: item.text()
            }

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

    def save_changes(self):
        for item in self.modified:
            request = 'UPDATE coffee SET ' + ', '.join([f'"{i}" = "{j}"' for i, j in self.modified[item].items()])
            request += f' WHERE {self.titles[0]} = {item}'
            self.cur.execute(request)
        self.base.commit()
        self.modified = {}

    def delete_row(self):
        answer = QMessageBox.question(self, '', 'Вы уверены?', QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.No:
            return
        if self.table.currentRow() == -1:
            error = QErrorMessage(self)
            error.showMessage('Такого значения не существует')
        request = 'DELETE FROM coffee WHERE ID = ?'
        self.cur.execute(request, (self.table.currentRow() + 1,))
        self.base.commit()
        self.update_values()

    def add_row(self):
        self.cur.execute('INSERT INTO coffee VALUES(?, ?, ?, ?, ?, ?, ?)',
                         tuple([self.table.rowCount() + 1] + ['' for _ in range(6)]))
        self.base.commit()
        self.update_values()

    def closeEvent(self, e):
        self.up_table.update_values()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
