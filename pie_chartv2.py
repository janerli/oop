import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QMargins


class PieChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Круговая диаграмма")
        self.resize(950, 520)  # побольше, и окно свободно ресайзится

        self.title = ""
        self.values = []
        self.labels = []
        self.total = 0.0

        self.read_data("data_pie.txt")  # формат как у тебя: title, n, дальше "value label"

        series = QPieSeries()
        series.setHoleSize(0.0)  # обычный круг (не donut)

        # Палитра (можешь менять как хочешь)
        palette = [
            QColor("#4C78A8"), QColor("#F58518"), QColor("#E45756"),
            QColor("#72B7B2"), QColor("#54A24B"), QColor("#EECA3B"),
            QColor("#B279A2"), QColor("#FF9DA6"), QColor("#9D755D"),
            QColor("#BAB0AC"),
        ]

        if self.total <= 0:
            # чтобы не падало, если файл пустой/битый
            self.total = 1.0

        for i, (val, lab) in enumerate(zip(self.values, self.labels)):
            slice_ = series.append(lab, val)
            slice_.setLabelVisible(False)          # никаких подписей на круге
            slice_.setExploded(False)              # никаких "вылетов"
            slice_.setBrush(palette[i % len(palette)])

            percent = (val / self.total) * 100.0
            # легенда будет показывать вот это:
            slice_.setLabel(f"{lab}: {percent:.2f}%")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.title if self.title else "Круговая диаграмма")

        # Круг слева + легенда справа
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        # Чуть компактнее, чтобы круг был крупнее
        chart.setMargins(QMargins(8, 8, 8, 8))

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(view)

    def read_data(self, filename: str):
        self.title = ""
        self.values = []
        self.labels = []
        self.total = 0.0

        try:
            with open(filename, "r", encoding="cp1251") as f:
                self.title = f.readline().strip()
                n_line = f.readline().strip()
                n = int(n_line) if n_line else 0

                for _ in range(n):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split(maxsplit=1)

                    value = float(parts[0].replace(",", "."))
                    label = parts[1].strip() if len(parts) > 1 else f"Item {_ + 1}"

                    self.values.append(value)
                    self.labels.append(label)
                    self.total += value

        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
        except Exception as e:
            print("Ошибка чтения данных:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PieChart()
    w.show()
    sys.exit(app.exec())
