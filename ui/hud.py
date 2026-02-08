from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtGui import QColor, QPalette, QPainter, QBrush
from PyQt6.QtCore import Qt

class HeadsUpDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 150); border-radius: 10px; color: white;")
        
        layout = QVBoxLayout()
        
        # Title
        self.title = QLabel("Gesture Art")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        layout.addWidget(self.title)

        # Color Indicator
        self.color_label = QLabel("Color: ")
        layout.addWidget(self.color_label)
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(50, 50)
        self.color_preview.setStyleSheet("background-color: red; border-radius: 25px; border: 2px solid white;")
        layout.addWidget(self.color_preview)

        # Brush Size
        self.size_label = QLabel("Brush Size: 5")
        layout.addWidget(self.size_label)
        self.size_bar = QProgressBar()
        self.size_bar.setRange(1, 50)
        self.size_bar.setValue(5)
        self.size_bar.setTextVisible(False)
        self.size_bar.setStyleSheet("QProgressBar::chunk { background-color: #00ADB5; }")
        layout.addWidget(self.size_bar)
        
        # Stability Meter (Visual Feedback)
        self.stability_label = QLabel("Tracking Stability")
        layout.addWidget(self.stability_label)
        self.stability_bar = QProgressBar()
        self.stability_bar.setRange(0, 100)
        self.stability_bar.setValue(100)
        self.stability_bar.setTextVisible(False)
        self.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #00FF00; }")
        layout.addWidget(self.stability_bar)

        layout.addStretch()
        self.setLayout(layout)

    def update_color(self, color_name, r, g, b):
        self.color_label.setText(f"Color: {color_name}")
        self.color_preview.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); border-radius: 25px; border: 2px solid white;")

    def update_brush_size(self, size):
        self.size_label.setText(f"Brush Size: {size}")
        self.size_bar.setValue(size)

    def update_stability(self, stability):
        self.stability_bar.setValue(stability)
        if stability > 80:
             self.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #00FF00; }")
        elif stability > 40:
             self.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #FFFF00; }")
        else:
             self.stability_bar.setStyleSheet("QProgressBar::chunk { background-color: #FF0000; }")
