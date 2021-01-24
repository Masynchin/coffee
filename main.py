import random
import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Сорт", "Степень обжарки",
            "Молотый/В зёрнах", "Вкус", "Цена", "Объём упаковки"
        ])

        for i, data in enumerate(self.get_data()):
            self.table.setRowCount(i + 1)
            for j, value in enumerate(data):
                self.table.setItem(i, j, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()

    def get_data(self):
        with sqlite3.connect("coffee.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM coffee
            """)
            return (map(str, row) for row in cursor.fetchall())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
