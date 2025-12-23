import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMessageBox, QVBoxLayout
)
from PyQt6.QtCharts import (
    QChart, QChartView, QLineSeries
)
from PyQt6.QtGui import QPainter, QFont, QPen
from PyQt6.QtCore import Qt, QPointF


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("График")
        self.resize(600, 300)

        try:
            self.cv = self.read_data()
        except Exception as e:
            QMessageBox.critical(self, "График", str(e))
            self.cv = []

        if self.cv:
            self.init_ui()

    # =============================
    # чтение данных
    # =============================
    def read_data(self):
        values = []
        with open("dinput.txt", "r", encoding="utf-8") as f:
            n = int(f.readline())
            for _ in range(n):
                values.append(float(f.readline()))

        if len(values) != n:
            raise ValueError(
                "Файл исходных данных поврежден "
                "или имеет неверное количество записей."
            )
        return values

    # =============================
    # UI + график
    # =============================
    def init_ui(self):
        layout = QVBoxLayout(self)

        series = QLineSeries()

        # линия
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        series.setPen(pen)

        cv_min = min(self.cv)
        cv_max = max(self.cv)

        # нормализованные точки
        for i, v in enumerate(self.cv):
            y = (v - cv_min) / (cv_max - cv_min)
            series.append(i, y)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Изменение курса доллара")
        chart.legend().hide()

        # ❌ убираем оси и сетку
        chart.removeAllAxes()
        chart.setBackgroundBrush(Qt.GlobalColor.white)
        chart.setPlotAreaBackgroundVisible(False)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout.addWidget(view)

        # ⬛ квадратные маркеры + подписи
        font = QFont("Tahoma", 9)

        for i, v in enumerate(self.cv):
            pos = chart.mapToPosition(series.at(i))

            # квадратный маркер
            size = 6
            rect = chart.scene().addRect(
                pos.x() - size / 2,
                pos.y() - size / 2,
                size,
                size,
                QPen(Qt.GlobalColor.black)
            )

            # подпись значения
            text = chart.scene().addText(f"{v:.2f}", font)
            text.setDefaultTextColor(Qt.GlobalColor.black)
            text.setPos(pos + QPointF(-12, -22))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphWindow()
    w.show()
    sys.exit(app.exec())