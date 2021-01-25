from PyQt5.QtWidgets import *


class BaseMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.change_button = QPushButton("Изменить")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.change_button)

        main_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)


class BaseAddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        query_layout = QHBoxLayout()

        labels_layout = QVBoxLayout()
        for title in (
            "Название сорта", "Прожарка", "Молотый/В зёрнах",
            "Вкус", "Цена", "Объём упаковки",
        ):
            labels_layout.addWidget(QLabel(title))

        inputs_layout = QVBoxLayout()

        self.sort = QLineEdit()
        self.roasting = QLineEdit()
        self.typing = QComboBox()
        self.flavor = QLineEdit()
        self.price = QSpinBox()
        self.volume = QSpinBox()

        for input_ in (
            self.sort, self.roasting, self.typing,
            self.flavor, self.price, self.volume,
        ):
            inputs_layout.addWidget(input_)

        query_layout.addLayout(labels_layout)
        query_layout.addLayout(inputs_layout)
        main_layout.addLayout(query_layout)

        self.button = QPushButton("Добавить")
        main_layout.addWidget(self.button)
