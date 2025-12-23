import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMessageBox
)
from PyQt6.QtGui import (
    QPainter, QPen, QFont
)
from PyQt6.QtCore import Qt


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cv = []

        self.setWindowTitle("График")
        self.resize(600, 300)
        self.setStyleSheet("background-color: white;")

        try:
            self.read_data()
        except FileNotFoundError as e:
            QMessageBox.critical(
                self, "График",
                f"Файл исходных данных не найден.\n{e}"
            )
        except ValueError as e:
            QMessageBox.critical(
                self, "График",
                f"Ошибка формата исходных данных.\n{e}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "График",
                f"{e}"
            )

    # =============================
    # чтение данных
    # =============================
    def read_data(self):
        with open("dinput.txt", "r", encoding="utf-8") as f:
            n = int(f.readline())
            for _ in range(n):
                self.cv.append(float(f.readline()))

        if not self.cv:
            raise ValueError("Файл исходных данных пуст.")

        if len(self.cv) != n:
            raise ValueError(
                "Файл исходных данных поврежден\n"
                "или имеет неверное количество записей."
            )

    # =============================
    # перерисовка
    # =============================
    def paintEvent(self, event):
        if not self.cv:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # шрифты
        header_font = QFont("Tahoma", 10, QFont.Weight.Bold)
        mark_font = QFont("Tahoma", 10)

        painter.setFont(header_font)
        painter.drawText(5, 20, "Изменение курса доллара")

        # геометрия
        width = self.width()
        height = self.height()

        sw = (width - 20) // (len(self.cv) - 1)

        cvmax = max(self.cv)
        cvmin = min(self.cv)

        # первая точка
        x1 = 8
        y1 = height - 20 - int(
            (height - 70) * (self.cv[0] - cvmin) / (cvmax - cvmin)
        )

        pen = QPen(Qt.GlobalColor.black)
        painter.setPen(pen)

        painter.drawRect(x1 - 2, y1 - 2, 4, 4)

        for i in range(1, len(self.cv)):
            x2 = 8 + i * sw
            y2 = height - 20 - int(
                (height - 70) * (self.cv[i] - cvmin) / (cvmax - cvmin)
            )

            # точка
            painter.drawRect(x2 - 2, y2 - 2, 4, 4)

            # линия
            painter.drawLine(x1, y1, x2, y2)

            # подпись
            painter.setFont(mark_font)
            painter.drawText(x1 - 5, y1 - 10, f"{self.cv[i - 1]:.2f}")

            x1, y1 = x2, y2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphWindow()
    w.show()
    sys.exit(app.exec())