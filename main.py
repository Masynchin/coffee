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
        self.setWindowTitle("CoffeeDB")
        self.update_table()

        self.add_button.clicked.connect(self.add)
        self.change_button.clicked.connect(self.change)

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

    def add(self):
        self.widget = AddWidget(self)
        self.widget.set_as_add()
        self.widget.show()

    def add_values(self, values):
        with sqlite3.connect("coffee.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO coffee (sort, roasting, type, flavor, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, values)
            conn.commit()

        self.update_table()

    def change(self):
        row_no = self.table.currentRow()
        if row_no != -1:
            values = [
                self.table.item(row_no, j).text()
                for j in range(self.table.columnCount())
            ]
            self.widget = AddWidget(self)
            self.widget.set_as_change(values)
            self.widget.show()

    def change_values(self, values):
        with sqlite3.connect("coffee.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE coffee
                SET sort = ?, roasting = ?, type = ?,
                    flavor = ?, price = ?, volume = ?
                WHERE id = ?
            """, values)
            conn.commit()

        self.update_table()
            


class AddWidget(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Add")
        self.parent = parent
        self.typing.addItems(["Молотый", "В зёрнах"])

    def set_as_add(self):
        self.button.clicked.connect(self.add)

    def add(self):
        values = (
            self.sort.text(), self.roasting.text(), self.typing.currentText(),
            self.flavor.text(), self.price.value(), self.volume.value(),
        )
        
        if any(v in ("", 0) for v in values):
            return

        self.parent.add_values(values)
        self.close()

    def set_as_change(self, values):
        self.button.clicked.connect(self.change)
        self.id, *values = values

        self.sort.setText(values[0])
        self.roasting.setText(values[1])
        self.flavor.setText(values[3])
        self.price.setValue(int(values[4]))
        self.volume.setValue(int(values[5]))

    def change(self):
        values = (
            self.sort.text(), self.roasting.text(), self.typing.currentText(),
            self.flavor.text(), self.price.value(), self.volume.value(),
        )
        
        if any(v in ("", 0) for v in values):
            return

        self.parent.change_values(values + (self.id,))
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
