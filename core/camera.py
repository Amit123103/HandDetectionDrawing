import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    frame_signal = pyqtSignal(np.ndarray)

    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Emit the frame
                self.frame_signal.emit(frame)
        cap.release()

    def stop(self):
        self.running = False
        self.wait()
