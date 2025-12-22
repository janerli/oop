import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCharts import (
    QChart, QChartView,
    QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QAbstractBarSeries
)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QMargins


class BarChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменение курса доллара")
        self.resize(900, 450)

        values = self.read_data("data_bar.txt")
        if not values:
            values = [0.0]

        # --- серия/набор ---
        bar_set = QBarSet("USD")
        for v in values:
            bar_set.append(v)

        # Делаем бары зеленого цвета
        bar_set.setColor(QColor(50, 205, 50))
        bar_set.setBorderColor(QColor(0, 1, 0))
        # Зеленый цвет

        # Можно сделать градиент для более красивого вида
        # bar_set.setColor(QColor(0, 180, 0))  # Более яркий зеленый
        # bar_set.setBorderColor(QColor(0, 100, 0))  # Темно-зеленая граница

        series = QBarSeries()
        series.append(bar_set)

        # Подписи над столбиками
        series.setLabelsVisible(True)
        series.setLabelsPosition(QAbstractBarSeries.LabelsPosition.LabelsOutsideEnd)
        series.setLabelsFormat("<font color='black'>@value</font>")
        series.setLabelsPrecision(10)
        series.setLabelsAngle(0)

        # --- chart ---
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Изменение курса доллара")
        chart.legend().hide()
        chart.setMargins(QMargins(20, 40, 20, 20))

        # --- оси ---
        axis_x = QBarCategoryAxis()
        axis_x.append([str(i + 1) for i in range(len(values))])
        axis_x.setLabelsVisible(False)
        axis_x.setGridLineVisible(False)
        axis_x.setMinorGridLineVisible(False)

        # Y: увеличиваем диапазон для подписей
        mn = min(values)
        mx = max(values)

        if mx - mn > 0:
            pad = max(0.1 * (mx - mn), 0.05)
        else:
            pad = 0.1

        axis_y = QValueAxis()
        axis_y.setRange(mn - pad, mx + pad * 3)
        axis_y.setLabelsVisible(False)
        axis_y.setGridLineVisible(False)
        axis_y.setMinorGridLineVisible(False)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        # --- view ---
        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(view)

    def read_data(self, filename: str) -> list[float]:
        data: list[float] = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                data.append(float(s.replace(",", ".")))
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = BarChart()
    w.show()
    sys.exit(app.exec())