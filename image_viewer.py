# image_viewer.py — список .jpg в папке + просмотр (с масштабированием).
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageViewer")

        v = QVBoxLayout(self)

        top = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        top.addWidget(self.path_edit)

        self.btn_folder = QPushButton("Папка")
        self.btn_folder.clicked.connect(self.pick_folder)
        top.addWidget(self.btn_folder)
        v.addLayout(top)

        mid = QHBoxLayout()
        self.listw = QListWidget()
        self.listw.currentTextChanged.connect(self.show_image)
        mid.addWidget(self.listw, 1)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setMinimumSize(300, 200)
        mid.addWidget(self.img_label, 3)

        v.addLayout(mid)

        # старт: папка запуска
        self.load_folder(Path.cwd())

    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.load_folder(Path(folder))

    def load_folder(self, folder: Path):
        self.folder = folder
        self.path_edit.setText(str(folder))
        self.listw.clear()

        files = sorted(folder.glob("*.jpg"))
        for f in files:
            self.listw.addItem(f.name)

        if files:
            self.listw.setCurrentRow(0)
        else:
            self.img_label.clear()
            QMessageBox.information(self, "Нет файлов", "В папке нет .jpg")

    def show_image(self, filename: str):
        if not filename:
            return
        path = self.folder / filename
        pix = QPixmap(str(path))
        if pix.isNull():
            self.img_label.setText("Не удалось загрузить изображение.")
            return

        # масштабируем "внутрь" области QLabel, сохраняя пропорции
        scaled = pix.scaled(
            self.img_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.img_label.setPixmap(scaled)

    def resizeEvent(self, e):
        # при ресайзе перерисовываем текущую картинку
        cur = self.listw.currentItem()
        if cur:
            self.show_image(cur.text())
        super().resizeEvent(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.resize(800, 500)
    w.show()
    sys.exit(app.exec())
