import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QFont, QColor
from PyQt6.QtCore import Qt


class PieChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Круговая диаграмма")
        self.resize(640, 360)

        # данные
        self.title = ""
        self.values = []
        self.labels = []
        self.total = 0.0

        self.read_data("data_pie.txt")

        self.setMinimumSize(400, 250)

    # ---------- чтение данных ----------
    def read_data(self, filename: str):
        try:
            with open(filename, "r", encoding="cp1251") as f:
                self.title = f.readline().strip()
                n = int(f.readline().strip())

                for _ in range(n):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split(maxsplit=1)
                    value = float(parts[0].replace(",", "."))
                    label = parts[1] if len(parts) > 1 else ""
                    self.values.append(value)
                    self.labels.append(label)
                    self.total += value
        except Exception as e:
            print("Ошибка чтения данных:", e)

    # ---------- отрисовка ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # >>> БЕЛЫЙ ФОН <<<
        painter.fillRect(self.rect(), Qt.GlobalColor.white)

        # шрифты
        title_font = QFont("Tahoma", 10, QFont.Weight.Bold)
        legend_font = QFont("Tahoma", 10)

        painter.setFont(title_font)
        painter.setPen(Qt.GlobalColor.black)

        # заголовок
        painter.drawText(10, 20, self.title)

        # диаметр круга
        sd = int(self.height() * 0.8) - 40
        sd = min(sd, self.width() // 2)

        x = 30
        y = (self.height() - sd) // 2 + 10

        # легенда
        lx = x + sd + 30
        ly = y + (sd - len(self.values) * 20) // 2

        # цвета (как в C# switch)
        colors = [
            QColor("lime"),
            QColor("gold"),
            QColor("deeppink"),
            QColor("violet"),
            QColor("orangered"),
            QColor("royalblue"),
            QColor("steelblue"),
            QColor("chocolate"),
            QColor("lightgray"),
            QColor("gold"),
        ]

        start_angle = -90 * 16  # Qt использует 1/16 градуса

        for i, value in enumerate(self.values):
            if self.total == 0:
                continue

            span_angle = int(360 * (value / self.total) * 16) + 16
            color = colors[i % len(colors)]

            painter.setBrush(color)
            painter.setPen(Qt.GlobalColor.black)

            # сектор
            painter.drawPie(x, y, sd, sd, start_angle, span_angle)

            start_angle += span_angle

            # легенда — цветной прямоугольник
            painter.fillRect(lx, ly + i * 20, 20, 10, color)
            painter.drawRect(lx, ly + i * 20, 20, 10)

            # подпись легенды
            percent = value / self.total * 100
            text = f"{self.labels[i]}: {percent:.2f}%".replace(".", ",")

            painter.setFont(legend_font)
            painter.drawText(lx + 26, ly + i * 20 + 9, text)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PieChartWindow()
    w.show()
    sys.exit(app.exec())
