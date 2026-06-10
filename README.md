# AirNav — Redefining Interaction Through Motion✨

AirNav is a Python-based virtual mouse that enables touch-free computer interaction using hand gestures and a webcam. It tracks hand movements in real time and converts them into cursor actions, clicks, scrolling, and volume control.

## Features

- ☝️ Move cursor using index finger
- 🤏 Left click using index + middle finger pinch
- 🤟 Right click using three fingers up
- ✌️ Smooth scrolling using two fingers
- 👍 Volume control using thumb–index distance
- Real-time hand tracking with gesture recognition

## Tech Stack

- Python
- OpenCV
- CVZone / MediaPipe
- NumPy
- PyAutoGUI
- Pycaw
- Comtypes

## Installation📦

### 1. Clone the repository

```bash
git clone https://github.com/aasthadhavan/AirNav.git
cd AirNav
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install opencv-python cvzone mediapipe pyautogui numpy pycaw comtypes
```

Or:

```bash
pip install -r requirements.txt
```

## Run

```bash
python virtualmouse.py
```

Press **Q** to quit.

## Gesture Controls🎮

| Gesture | Action |
|----------|---------|
| Index Finger | Cursor Movement |
| Index + Middle Pinch | Left Click |
| Three Fingers Up | Right Click |
| Two Fingers Up | Scroll |
| Thumb ↔ Index Distance | Volume Control |

## Future Improvements

- Drag & Drop Support
- Custom Gestures
- Multi-Hand Tracking
- Media Controls
- Brightness Control


