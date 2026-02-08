import sys
import os

# Add local libs to path to fix import issues
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

from PyQt6.QtWidgets import QApplication
from ui.overlay import OverlayWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    sys.exit(app.exec())
