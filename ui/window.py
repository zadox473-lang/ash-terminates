import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtWidgets import QMainWindow

from ui.ai_core import AICore
from vision.camera import Camera
from vision.hand_tracker import HandTracker
from vision.gesture_engine import GestureEngine


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # IMPORTANT: initialize these BEFORE Qt paints
        self.hands = 0
        self.pinch = False
        self.zoom = 0
        self.move_x = 0

        self.setWindowTitle("ASH-X")
        self.setMinimumSize(1000, 700)

        self.camera = Camera()
        self.tracker = HandTracker()
        self.gestures = GestureEngine()

        self.core = AICore()
        self.setCentralWidget(self.core)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system)
        self.timer.start(16)

    def update_system(self):
        frame = self.camera.read()

        if frame is None:
            return

        results = self.tracker.process(frame)

        gesture = self.gestures.analyze(results)

        self.hands = gesture["hands"]
        self.pinch = gesture["pinch"]
        self.zoom = gesture["zoom"]
        self.move_x = gesture["move_x"]

        self.core.set_gesture_data(gesture)

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        try:
            painter.setRenderHint(
                QPainter.RenderHint.Antialiasing
            )

            painter.fillRect(
                self.rect(),
                Qt.GlobalColor.black
            )

            painter.setPen(
                QPen(Qt.GlobalColor.cyan, 1)
            )

            painter.setFont(
                QFont("Consolas", 14)
            )

            # Header
            painter.drawText(
                35,
                40,
                "ASH-X // ADVANCED SYSTEM CORE"
            )

            # Left status
            painter.drawText(
                35,
                75,
                f"VISION     : {'ONLINE' if self.hands else 'SEARCHING'}"
            )

            painter.drawText(
                35,
                105,
                f"HANDS      : {self.hands}"
            )

            painter.drawText(
                35,
                135,
                f"PINCH      : {'ACTIVE' if self.pinch else 'STANDBY'}"
            )

            painter.drawText(
                35,
                165,
                f"ZOOM       : {self.zoom}"
            )

            # Right status
            x = self.width() - 280

            painter.drawText(
                x,
                40,
                "SYSTEM STATUS"
            )

            painter.drawText(
                x,
                75,
                "AI CORE     ONLINE"
            )

            painter.drawText(
                x,
                105,
                "GESTURE     ONLINE"
            )

            painter.drawText(
                x,
                135,
                "CAMERA      ONLINE"
            )

            # Bottom
            painter.drawText(
                35,
                self.height() - 30,
                "ASH-X // VISION INTERFACE"
            )

        finally:
            painter.end()

    def keyPressEvent(self, event):

        # ESC = exit
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return

        super().keyPressEvent(event)

    def closeEvent(self, event):

        if hasattr(self, "timer"):
            self.timer.stop()

        if hasattr(self, "camera"):
            self.camera.release()

        event.accept()
