import sys
import os

if __name__ == "__main__":
    # Check if running on Render (or any headless CI/CD environment)
    if os.environ.get("RENDER") or os.environ.get("CI"):
        print("Detected Render/Headless environment. Starting Web Server...")
        import uvicorn
        # Import the app from server.py (assuming it's in the same directory)
        from server import app
        
        port = int(os.environ.get("PORT", 10000))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Desktop Environment - Run GUI
        try:
            from PyQt6.QtWidgets import QApplication
            from ui.overlay import OverlayWindow
            
            app = QApplication(sys.argv)
            window = OverlayWindow()
            window.show()
            sys.exit(app.exec())
        except ImportError as e:
            print(f"Error importing GUI dependencies: {e}")
            print("Ensure you are running on a machine with a display and PyQt6 installed.")
