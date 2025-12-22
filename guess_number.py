import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QMessageBox, QStatusBar
)
from PyQt6.QtCore import QTimer


class GuessNumber(QWidget):
    DIGITS = 3  # количество цифр

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Угадай число")
        self.resize(520, 260)

        # ---------- Описание ----------
        self.info = QLabel(
            "Угадайте загаданное компьютером трехзначное число.\n"
            "Введите свой вариант и нажмите <Enter>"
        )

        # ---------- Группа "Число" ----------
        self.input = QLineEdit()
        self.input.setMaxLength(self.DIGITS)
        self.input.setEnabled(False)
        self.input.returnPressed.connect(self.check)

        group = QGroupBox("Число")
        g_layout = QVBoxLayout(group)
        g_layout.addWidget(self.input)

        # ---------- Результаты ----------
        self.lbl_guess = QLabel("Угадано цифр: 0")
        self.lbl_pos = QLabel("Цифр на правильных позициях: 0")

        # ---------- Кнопки ----------
        self.btn_start = QPushButton("Начать")
        self.btn_end = QPushButton("Завершить")

        self.btn_start.clicked.connect(self.toggle_game)
        self.btn_end.clicked.connect(self.close)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_end)

        # ---------- StatusBar ----------
        self.status = QStatusBar()

        # ---------- Layout ----------
        main = QVBoxLayout(self)
        main.addWidget(self.info)
        main.addWidget(group)
        main.addWidget(self.lbl_guess)
        main.addWidget(self.lbl_pos)
        main.addLayout(btn_row)
        main.addWidget(self.status)

        # ---------- Логика ----------
        self.secret = []      # загаданное число (список цифр)
        self.attempts = 0
        self.seconds = 0

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)

        self.reset_ui_only()

    # ===== СБРОСЫ =====

    def reset_ui_only(self):
        """Сброс интерфейса/счетчиков, НО без стирания self.secret."""
        self.attempts = 0
        self.seconds = 0
        self.input.clear()
        self.input.setEnabled(False)
        self.lbl_guess.setText("Угадано цифр: 0")
        self.lbl_pos.setText("Цифр на правильных позициях: 0")
        self.status.showMessage("Попыток: 0 | Время: 0 сек")

    def full_reset(self):
        """Полный сброс (и интерфейс, и загадка)."""
        self.secret = []
        self.reset_ui_only()

    # ===== ГЕНЕРАЦИЯ =====

    def generate_number(self):
        """Генерирует трехзначное число без повторов, первая цифра не 0."""
        digits = list("0123456789")
        first = random.choice("123456789")
        digits.remove(first)
        rest = random.sample(digits, self.DIGITS - 1)
        self.secret = [int(first)] + list(map(int, rest))

    # ===== ИГРА =====

    def toggle_game(self):
        # Старт
        if not self.timer.isActive():
            self.reset_ui_only()        # сбросили счетчики/интерфейс
            self.generate_number()      # сгенерили загадку (И НЕ СТИРАЕМ ЕЁ)
            self.input.setEnabled(True)
            self.input.setFocus()
            self.timer.start()
            self.btn_start.setText("Стоп")
        # Стоп
        else:
            self.timer.stop()
            self.btn_start.setText("Начать")
            self.full_reset()

    def tick(self):
        self.seconds += 1
        self.status.showMessage(f"Попыток: {self.attempts} | Время: {self.seconds} сек")

    def check(self):
        # защита от ввода, если игра не запущена/загадка не создана
        if not self.timer.isActive() or len(self.secret) != self.DIGITS:
            QMessageBox.information(self, "Игра", "Нажмите «Начать» для старта игры.")
            return

        text = self.input.text().strip()
        if len(text) != self.DIGITS or not text.isdigit():
            QMessageBox.information(self, "Ошибка", "Введите трехзначное число.")
            return

        self.attempts += 1

        guess = list(map(int, text))

        # pos = сколько цифр на правильных местах
        pos = sum(1 for i in range(self.DIGITS) if guess[i] == self.secret[i])

        # guessed = сколько цифр угадано вообще (без учета позиций)
        # Чтобы не считать повторы неверно — используем множества.
        guessed = len(set(guess) & set(self.secret))

        self.lbl_guess.setText(f"Угадано цифр: {guessed}")
        self.lbl_pos.setText(f"Цифр на правильных позициях: {pos}")

        if pos == self.DIGITS:
            self.timer.stop()
            QMessageBox.information(
                self,
                "Победа!",
                f"Вы угадали число!\nПопыток: {self.attempts}\nВремя: {self.seconds} сек"
            )
            self.btn_start.setText("Начать")
            self.full_reset()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GuessNumber()
    w.show()
    sys.exit(app.exec())
