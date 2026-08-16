import cv2

from config import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    def read(self):
        if not self.cap.isOpened():
            return None

        ok, frame = self.cap.read()

        if not ok:
            return None

        return cv2.flip(frame, 1)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
