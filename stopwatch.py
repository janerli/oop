import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt


class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Секундомер")
        self.resize(300, 160)

        # ---------- Время ----------
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 28px;")

        # ---------- Кнопки ----------
        self.btn_start = QPushButton("Пуск")
        self.btn_reset = QPushButton("Сброс")

        self.btn_start.clicked.connect(self.toggle)
        self.btn_reset.clicked.connect(self.reset)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_reset)

        # ---------- Layout ----------
        main = QVBoxLayout(self)
        main.addWidget(self.time_label)
        main.addLayout(btn_row)

        # ---------- Таймер ----------
        self.timer = QTimer(self)
        self.timer.setInterval(10)  # 10 мс
        self.timer.timeout.connect(self.tick)

        self.ms = 0
        self.running = False

    def tick(self):
        self.ms += 10
        total = self.ms // 10  # сотые
        seconds = total // 100
        minutes = seconds // 60
        seconds %= 60
        cs = total % 100

        self.time_label.setText(f"{minutes:02d}:{seconds:02d}:{cs:02d}")

    def toggle(self):
        if not self.running:
            self.timer.start()
            self.btn_start.setText("Стоп")
            self.running = True
        else:
            self.timer.stop()
            self.btn_start.setText("Пуск")
            self.running = False

    def reset(self):
        self.timer.stop()
        self.ms = 0
        self.running = False
        self.btn_start.setText("Пуск")
        self.time_label.setText("00:00:00")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Stopwatch()
    w.show()
    sys.exit(app.exec())
