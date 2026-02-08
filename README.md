# Hand Detection & Gesture Drawing App

An AI-powered desktop application that allows you to draw on a digital canvas using hand gestures and control the interface with head movements. Built with **Python**, **MediaPipe**, **OpenCV**, and **PyQt6**.

## 🚀 Features

*   **Hand Tracking**: Uses MediaPipe Hands to detect hand landmarks in real-time.
*   **Gesture Drawing**:
    *   **Index Finger**: Move the cursor.
    *   **Pinch (Thumb + Index)**: Start drawing.
    *   **Fist**: Undo the last stroke.
*   **Head Gestures**:
    *   **Head Tilt (Left/Right)**: Cycle through brush colors.
    *   **Head Nod (Up/Down)**: Adjust brush size.
*   **GUI Overlay**: A transparent HUD built with PyQt6 showing the camera feed, stability bar, and current tool settings.
*   **Web Deployment Ready**: Includes a fallback server for cloud deployments (Render/Heroku).

## 📦 Requirements

To run this project efficiently, you need the following Python packages:

*   `opencv-python`: For image processing and camera access.
*   `mediapipe`: For AI-based hand and face tracking.
*   `numpy`: For numerical operations and array handling.
*   `PyQt6`: For the graphical user interface.

## 🛠️ Installation Guide

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Amit123103/HandDetectionDrawing.git
cd HandDetectionDrawing
```

### 2. Set Up a Virtual Environment (Recommended)
It's best practice to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required packages using `pip`:
```bash
pip install -r requirements.txt
```

## ▶️ How to Run

### On Desktop (Windows/macOS/Linux)
Make sure you have a webcam connected. Run the following command:

```bash
python main.py
```
This will launch the application window.

### On Cloud/Headless Servers (Render)
If deploying to a cloud service like Render, the app will automatically start in **Server Mode** (API only) to prevent crashing on headless systems.
*   Start Command: `python main.py` or `uvicorn server:app --host 0.0.0.0 --port $PORT`

## 🎮 Controls

| Gesture | Action |
| :--- | :--- |
| **Index Finger** | Move Cursor |
| **Pinch (Index + Thumb)** | Draw / Paint |
| **Closed Fist** | Undo Last Stroke |
| **Head Tilt Left** | Previous Color |
| **Head Tilt Right** | Next Color |
| **Head Nod Up** | Increase Brush Size |
| **Head Nod Down** | Decrease Brush Size |

## 📝 Troubleshooting

*   **`ModuleNotFoundError`**: Ensure you have activated your virtual environment and installed requirements.
*   **Camera not opening**: Check if another application is using the webcam.
*   **Render Deployment**: Remember that the drawing interface **cannot** be seen on Render. It is a backend deployment only. Run locally for the full experience.