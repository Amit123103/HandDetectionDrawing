import cv2
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QPoint

from core.camera import CameraThread
from core.tracker import HandTracker, HeadTracker
from core.drawing import CanvasLogic
from ui.hud import HeadsUpDisplay

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture-Based Digital Art")
        self.setGeometry(100, 100, 1280, 720)
        
        # Core Components
        self.camera_thread = CameraThread()
        self.hand_tracker = HandTracker()
        self.head_tracker = HeadTracker()
        self.canvas = CanvasLogic()
        
        # State
        self.current_color = (0, 0, 255) # BGR Red
        self.current_size = 5
        self.colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255)] # BGR
        self.color_names = ["Red", "Green", "Blue", "Yellow", "Magenta"]
        self.color_index = 0
        self.is_drawing = False
        
        self.last_head_tilt = 0 # Simple debounce/state for head tilt
        
        # UI Setup
        self.init_ui()
        
        # Connect Camera
        self.camera_thread.frame_signal.connect(self.process_frame)
        self.camera_thread.start()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Video Background
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setGeometry(0, 0, 1280, 720)
        self.video_label.setScaledContents(True) # Ensure video scales
        
        # HUD
        self.hud = HeadsUpDisplay(self)
        self.hud.move(20, 20)
        self.hud.update_color(self.color_names[self.color_index], 255, 0, 0)

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1) # Mirror effect
        h, w, c = frame.shape
        
        # 1. Hand Tracking
        frame = self.hand_tracker.find_hands(frame, draw=False) # We will draw custom wireframe
        lm_list = self.hand_tracker.find_position(frame)
        
        cursor_pos = None
        
        if lm_list:
            # Check Undo (Fist)
            if self.hand_tracker.is_fist(lm_list):
                 if self.canvas.undo():
                     print("Undo Performed")

            # Check Pinch (Draw)
            pinching, px, py = self.hand_tracker.is_pinching(lm_list)
            
            # Cursor position (Index tip)
            ix, iy = lm_list[8][1], lm_list[8][2]
            cursor_pos = (ix, iy)

            if pinching:
                self.is_drawing = True
                self.hud.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #00FF00; }") # Visual feedback
                
                # Convert BGR color to RGB for display if needed, but Canvas stores logical color
                # Storing (R, G, B) for Qt
                b, g, r = self.colors[self.color_index]
                self.canvas.add_point(px, py, (r, g, b), self.current_size)
            else:
                if self.is_drawing:
                    self.canvas.end_stroke()
                self.is_drawing = False
                self.canvas.start_stroke() # Reset stroke state
                self.hud.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #FFFF00; }")
                
            # Draw Skeleton (Custom)
            for id, cx, cy in lm_list:
                 cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            
            # Highlight Index Tip
            cv2.circle(frame, (ix, iy), 10, self.colors[self.color_index], 2)

        # 2. Head Tracking
        pitch, yaw = self.head_tracker.find_head_pose(frame)
        if pitch is not None and yaw is not None:
             # Head Tilt (Yaw) for Color - Thresholds
             if yaw > 20: # Right
                 if self.last_head_tilt == 0:
                     self.color_index = (self.color_index + 1) % len(self.colors)
                     b, g, r = self.colors[self.color_index]
                     self.hud.update_color(self.color_names[self.color_index], r, g, b)
                     self.last_head_tilt = 1
             elif yaw < -20: # Left
                 if self.last_head_tilt == 0:
                     self.color_index = (self.color_index - 1) % len(self.colors)
                     b, g, r = self.colors[self.color_index]
                     self.hud.update_color(self.color_names[self.color_index], r, g, b)
                     self.last_head_tilt = -1
             else:
                 self.last_head_tilt = 0
            
             # Head Nod (Pitch) for Size
             if pitch > 20: # Down
                 self.current_size = max(1, self.current_size - 1)
                 self.hud.update_brush_size(self.current_size)
             elif pitch < -20: # Up
                 self.current_size = min(50, self.current_size + 1)
                 self.hud.update_brush_size(self.current_size)

        # 3. Draw Canvas on Frame
        # Create a separate layer for drawing to blend?
        # For simplicity, we can draw directly on the frame using OpenCV capabilities
        # Or better, we draw on a Qt Overlay.
        # Here: Draw strokes on the 'frame' using OpenCV functions for high performance
        
        strokes = self.canvas.get_strokes()
        current_stroke = self.canvas.get_current_stroke()
        
        all_strokes = strokes + [current_stroke] if current_stroke else strokes
        
        for stroke in all_strokes:
            for i in range(1, len(stroke)):
                p1 = stroke[i-1]
                p2 = stroke[i]
                
                # p1 = (x, y, (r,g,b), size)
                # cv2 uses BGR
                color = (p1[2][2], p1[2][1], p1[2][0]) # RGB to BGR
                cv2.line(frame, (p1[0], p1[1]), (p2[0], p2[1]), color, p1[3])

        self.update_video_label(frame)

    def update_video_label(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

