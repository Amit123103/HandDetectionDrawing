# Hand Detection Drawing

An AI-powered gesture-based drawing application using MediaPipe and OpenCV.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Amit123103/HandDetectionDrawing.git
    cd HandDetectionDrawing
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Start Command

To run the application, execute:

```bash
python main.py
```

## Note for Deployment

This application uses **PyQt6** and opens a GUI window (`OverlayWindow`). It is designed to run on a **desktop environment** with a display.

**It cannot be deployed directly to headless backend services** (like Render, Heroku, or Vercel) because these platforms do not support graphical interfaces by default. If you need to deploy logic to a backend, robust modifications are required to split the core processing from the UI.