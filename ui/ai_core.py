import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtWidgets import QWidget


class AICore(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0
        self.core_size = 150
        self.target_size = 150
        self.center_x = 0

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def set_gesture_data(self, gesture):
        # Zoom
        self.target_size += gesture["zoom"] * 0.015

        self.target_size = max(
            90,
            min(260, self.target_size)
        )

        # Horizontal movement
        self.center_x += gesture["move_x"] * 0.03

        limit = self.width() * 0.30

        self.center_x = max(
            -limit,
            min(limit, self.center_x)
        )

    def animate(self):
        self.angle += 1

        if self.angle >= 360:
            self.angle = 0

        self.core_size += (
            self.target_size - self.core_size
        ) * 0.08

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        cx = self.width() / 2 + self.center_x
        cy = self.height() / 2

        size = self.core_size

        # Outer scanning rings
        for i in range(5):
            radius = size + i * 24

            pen = QPen(
                Qt.GlobalColor.cyan,
                1
            )

            painter.setPen(pen)

            painter.drawEllipse(
                int(cx - radius),
                int(cy - radius),
                int(radius * 2),
                int(radius * 2),
            )

        # Rotating segments
        painter.save()

        painter.translate(cx, cy)
        painter.rotate(self.angle)

        for i in range(8):
            painter.rotate(45)

            pen = QPen(
                Qt.GlobalColor.cyan,
                3
            )

            painter.setPen(pen)

            painter.drawLine(
                int(size + 10),
                0,
                int(size + 35),
                0,
            )

        painter.restore()

        # Core
        painter.setBrush(
            QBrush(Qt.GlobalColor.black)
        )

        painter.setPen(
            QPen(Qt.GlobalColor.cyan, 4)
        )

        painter.drawEllipse(
            int(cx - size / 2),
            int(cy - size / 2),
            int(size),
            int(size),
        )

        # Inner core
        pulse = 12 + 5 * math.sin(
            math.radians(self.angle * 4)
        )

        painter.setBrush(
            QBrush(Qt.GlobalColor.cyan)
        )

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            int(cx - pulse),
            int(cy - pulse),
            int(pulse * 2),
            int(pulse * 2),
        )
