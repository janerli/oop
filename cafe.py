import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QCheckBox,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt


class Cafe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кафе")
        self.resize(420, 260)

        # ---------- Верхняя строка ----------
        title = QLabel("Стоимость заказа:")
        self.sum_label = QLabel("0.00")
        self.sum_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        top = QHBoxLayout()
        top.addWidget(title)
        top.addStretch()
        top.addWidget(self.sum_label)

        # ---------- CheckBox ----------
        self.cb_sandwich = QCheckBox("Сэндвич")
        self.cb_potato = QCheckBox("Картошка")
        self.cb_sauce = QCheckBox("Соус")
        self.cb_cola = QCheckBox("Coca-Cola")

        self.cb_sauce.setEnabled(False)

        # ---------- Кнопка ----------
        self.btn_ok = QPushButton("Ok")
        self.btn_ok.clicked.connect(self.calculate)

        bottom = QHBoxLayout()
        bottom.addWidget(self.btn_ok)
        bottom.addStretch()

        # ---------- Главный layout ----------
        main = QVBoxLayout(self)
        main.addLayout(top)
        main.addWidget(self.cb_sandwich)
        main.addWidget(self.cb_potato)
        main.addWidget(self.cb_sauce)
        main.addWidget(self.cb_cola)
        main.addStretch()
        main.addLayout(bottom)

        # ---------- Цены ----------
        self.prices = {
            self.cb_sandwich: 54.0,
            self.cb_potato: 24.5,
            self.cb_sauce: 10.5,
            self.cb_cola: 18.0
        }

        # ---------- Сигналы ----------
        self.cb_potato.stateChanged.connect(self.potato_changed)

    def potato_changed(self):
        if self.cb_potato.isChecked():
            self.cb_sauce.setEnabled(True)
        else:
            self.cb_sauce.setChecked(False)
            self.cb_sauce.setEnabled(False)

    def calculate(self):
        total = 0.0
        selected = 0

        for cb, price in self.prices.items():
            if cb.isChecked():
                total += price
                selected += 1

        if total == 0:
            QMessageBox.information(self, "Кафе", "Вы ничего не выбрали.")
            return

        if selected == len(self.prices):
            total *= 0.9

        self.sum_label.setText(f"{total:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Cafe()
    w.show()
    sys.exit(app.exec())
