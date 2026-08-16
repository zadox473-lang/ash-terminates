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

        self.setWindowTitle("ASH-X")
        self.showFullScreen()

        self.camera = Camera()
        self.tracker = HandTracker()
        self.gestures = GestureEngine()

        self.core = AICore()
        self.setCentralWidget(self.core)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system)
        self.timer.start(16)

        self.hands = 0
        self.pinch = False

    def update_system(self):
        frame = self.camera.read()

        if frame is None:
            return

        results = self.tracker.process(frame)

        gesture = self.gestures.analyze(results)

        self.hands = gesture["hands"]
        self.pinch = gesture["pinch"]

        self.core.set_gesture_data(gesture)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

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

        painter.drawText(
            40,
            50,
            "ASH-X // ADVANCED SYSTEM CORE"
        )

        painter.drawText(
            40,
            80,
            f"VISION     : {'ONLINE' if self.hands else 'SEARCHING'}"
        )

        painter.drawText(
            40,
            110,
            f"HANDS      : {self.hands}"
        )

        painter.drawText(
            40,
            140,
            f"PINCH      : {'ACTIVE' if self.pinch else 'STANDBY'}"
        )

        painter.drawText(
            self.width() - 280,
            50,
            "SYSTEM STATUS"
        )

        painter.drawText(
            self.width() - 280,
            80,
            "AI CORE     ONLINE"
        )

        painter.drawText(
            self.width() - 280,
            110,
            "GESTURE     ONLINE"
        )

        painter.drawText(
            self.width() - 280,
            140,
            "CAMERA      ONLINE"
        )

    def closeEvent(self, event):
        self.camera.release()
        event.accept()
