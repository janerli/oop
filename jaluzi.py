import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QRadioButton, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)


class Blinds(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Жалюзи")
        self.resize(420, 300)

        # ---------- Ввод размеров ----------
        self.w_edit = QLineEdit()
        self.h_edit = QLineEdit()

        row_w = QHBoxLayout()
        row_w.addWidget(QLabel("Ширина (см)"))
        row_w.addWidget(self.w_edit)

        row_h = QHBoxLayout()
        row_h.addWidget(QLabel("Высота (см)"))
        row_h.addWidget(self.h_edit)

        # ---------- Материал ----------
        self.rb_al = QRadioButton("алюминий")
        self.rb_pl = QRadioButton("пластик")
        self.rb_al.setChecked(True)

        mat_box = QVBoxLayout()
        mat_box.addWidget(self.rb_al)
        mat_box.addWidget(self.rb_pl)

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
        main.addLayout(row_w)
        main.addLayout(row_h)
        main.addLayout(mat_box)
        main.addLayout(btn_row)
        main.addWidget(self.result)

    def calculate(self):
        try:
            w = float(self.w_edit.text().replace(",", "."))
            h = float(self.h_edit.text().replace(",", "."))
        except ValueError:
            QMessageBox.information(self, "Жалюзи", "Введите корректные числа.")
            return

        area = (w * h) / 10000  # м²
        price = 3600 if self.rb_al.isChecked() else 1800
        total = area * price

        material = "алюминий" if self.rb_al.isChecked() else "пластик"

        self.result.setText(
            f"Размер: {w} x {h} см\n"
            f"Материал: {material}\n"
            f"Стоимость: {total:.2f} руб."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Blinds()
    w.show()
    sys.exit(app.exec())
