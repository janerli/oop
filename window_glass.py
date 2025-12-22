import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QRadioButton, QCheckBox, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout,
    QGroupBox, QMessageBox
)


class Glass(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стеклопакет")
        self.resize(500, 320)

        # ---------- Размер окна ----------
        self.w_edit = QLineEdit()
        self.h_edit = QLineEdit()

        row_w = QHBoxLayout()
        row_w.addWidget(QLabel("Ширина (см)"))
        row_w.addWidget(self.w_edit)

        row_h = QHBoxLayout()
        row_h.addWidget(QLabel("Высота (см)"))
        row_h.addWidget(self.h_edit)

        size_box = QGroupBox("Размер окна")
        size_layout = QVBoxLayout(size_box)
        size_layout.addLayout(row_w)
        size_layout.addLayout(row_h)

        # ---------- Тип стеклопакета ----------
        self.rb_one = QRadioButton("Однокамерный")
        self.rb_two = QRadioButton("Двухкамерный")
        self.rb_one.setChecked(True)

        pack_box = QGroupBox("Стеклопакет")
        pack_layout = QVBoxLayout(pack_box)
        pack_layout.addWidget(self.rb_one)
        pack_layout.addWidget(self.rb_two)

        # ---------- Верхняя часть ----------
        top = QHBoxLayout()
        top.addWidget(size_box)
        top.addWidget(pack_box)

        # ---------- Подоконник ----------
        self.cb_sill = QCheckBox("Подоконник")

        # ---------- Кнопка ----------
        self.btn_ok = QPushButton("Ok")
        self.btn_ok.clicked.connect(self.calculate)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_ok)
        btn_row.addStretch()

        # ---------- Результат ----------
        self.result = QTextEdit()
        self.result.setReadOnly(True)

        # ---------- Главный layout ----------
        main = QVBoxLayout(self)
        main.addLayout(top)
        main.addWidget(self.cb_sill)
        main.addLayout(btn_row)
        main.addWidget(self.result)

    def calculate(self):
        try:
            w = float(self.w_edit.text().replace(",", "."))
            h = float(self.h_edit.text().replace(",", "."))
        except ValueError:
            QMessageBox.information(self, "Стеклопакет", "Введите корректные размеры.")
            return

        area = (w * h) / 10000  # м²

        price = 5000 if self.rb_one.isChecked() else 6000
        total = area * price

        if self.cb_sill.isChecked():
            total += 20 * w

        pack = "Однокамерный" if self.rb_one.isChecked() else "Двухкамерный"

        self.result.setText(
            f"Размер окна: {w} x {h} см\n"
            f"Тип стеклопакета: {pack}\n"
            f"Подоконник: {'да' if self.cb_sill.isChecked() else 'нет'}\n"
            f"Стоимость: {total:.2f} руб."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Glass()
    w.show()
    sys.exit(app.exec())
