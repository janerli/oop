# timer_app.py
# PyQt6: таймер обратного отсчёта как на шаблоне (layout-ами, без setGeometry)

import sys
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGroupBox, QSpinBox, QHBoxLayout, QVBoxLayout, QGridLayout
)


class TimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таймер")
        self.setFixedSize(340, 180)  # фиксируем, чтобы совпадало по ощущению со скрином

        # ====== ВЕРХ: label3 (00:00) ======
        self.time_label = QLabel("00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setStyleSheet("font-size: 28px;")  # крупно как в шаблоне

        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addWidget(self.time_label)
        top_row.addStretch()

        # ====== СЕРЕДИНА: GroupBox "Интервал" + spinbox минут/секунд ======
        box = QGroupBox("Интервал")

        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 999)
        self.min_spin.setFixedWidth(55)

        self.sec_spin = QSpinBox()
        self.sec_spin.setRange(0, 59)
        self.sec_spin.setFixedWidth(55)

        minutes_lbl = QLabel("минут")
        seconds_lbl = QLabel("секунд")

        grid = QGridLayout()
        # строка: [spin] [минут]   [spin] [секунд]
        grid.addWidget(self.min_spin, 0, 0)
        grid.addWidget(minutes_lbl, 0, 1)
        grid.addWidget(self.sec_spin, 0, 2)
        grid.addWidget(seconds_lbl, 0, 3)
        grid.setColumnStretch(4, 1)
        box.setLayout(grid)

        # ====== НИЗ: button1 "Пуск" ======
        self.start_btn = QPushButton("Пуск")
        self.start_btn.clicked.connect(self.on_start_stop)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch(1)
        bottom_row.addWidget(self.start_btn)
        bottom_row.addStretch(1)

        # ====== Главная компоновка как на скрине ======
        root = QVBoxLayout()
        root.addLayout(top_row)
        root.addWidget(box)
        root.addLayout(bottom_row)
        root.addStretch(1)
        self.setLayout(root)

        # ====== ЛОГИКА ТАЙМЕРА ======
        self._seconds_left = 0
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.tick)

    def format_time(self, total_seconds: int) -> str:
        m = total_seconds // 60
        s = total_seconds % 60
        return f"{m:02d}:{s:02d}"

    def on_start_stop(self):
        # если идёт — остановим (кнопка остаётся "Пуск" в шаблоне не меняется,
        # но можно менять при желании — я оставил простую логику)
        if self._timer.isActive():
            self._timer.stop()
            self.min_spin.setEnabled(True)
            self.sec_spin.setEnabled(True)
            return

        total = self.min_spin.value() * 60 + self.sec_spin.value()
        if total <= 0:
            # ничего не стартуем, просто оставим 00:00
            self.time_label.setText("00:00")
            return

        self._seconds_left = total
        self.time_label.setText(self.format_time(self._seconds_left))

        # во время отсчёта блокируем ввод (чтобы как в нормальных таймерах)
        self.min_spin.setEnabled(False)
        self.sec_spin.setEnabled(False)

        self._timer.start()

    def tick(self):
        self._seconds_left -= 1
        if self._seconds_left <= 0:
            self._timer.stop()
            self._seconds_left = 0
            self.time_label.setText("00:00")
            self.min_spin.setEnabled(True)
            self.sec_spin.setEnabled(True)
            QApplication.beep()
            return

        self.time_label.setText(self.format_time(self._seconds_left))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TimerWindow()
    w.show()
    sys.exit(app.exec())
