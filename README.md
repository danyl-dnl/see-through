# Vision-Scribe 👓

**An AI-powered assistive vision prototype for object detection and audio feedback.**

Vision-Scribe is an experimental project designed to help people who are blind or have low vision understand useful information about their surroundings.

The system uses a camera to capture the environment, AI to identify objects, and text-to-speech to communicate selected information through audio.

Our goal is to gradually develop this into a wearable smart-glasses prototype.

> **Project status:** Early software prototype. Live YOLO object detection works on the development Mac. YOLO-to-speech integration is under development and still needs reliability improvements.

## Current Features

- Live webcam capture using OpenCV.
- Object detection using the Ultralytics YOLO model.
- Bounding boxes and object labels displayed on the camera feed.
- Basic text-to-speech testing using `pyttsx3`.
- Background speech processing using Python threads and a message queue.
- Initial priority-based object announcement logic (provided, pending testing).

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Webcam access and image processing |
| Ultralytics YOLO | Object detection |
| YOLO11n | Pretrained object-detection model |
| pyttsx3 | Text-to-speech |
| threading | Running speech separately from camera processing |
| queue | Passing speech messages to the speech worker |

## How It Works

The current prototype follows this basic flow:

1. Open the laptop webcam.
2. Capture a video frame using OpenCV.
3. Pass the frame to YOLO.
4. Identify objects in the frame.
5. Display object labels and bounding boxes.
6. Select an object for announcement.
7. Send the announcement to a speech queue.
8. The background speech worker processes the message.

The intended result is for Vision-Scribe to identify selected objects and announce them aloud.

## Project Structure

```text
see-through/
│
├── camera.py
├── yolo_camera.py
├── speech_test.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── venv/              # Local Python environment; not committed
```

The YOLO model weights file (`yolo11n.pt`) is downloaded locally and excluded from Git.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/danyl-dnl/see-through.git
```

Move into the project directory:

```bash
cd see-through
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

On Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The current `requirements.txt` contains:

```text
opencv-python
ultralytics
pyttsx3
```

### 4. Run the webcam test

```bash
python camera.py
```

This tests basic webcam capture using OpenCV.

### 5. Run YOLO object detection and speech

```bash
python yolo_camera.py
```

The program opens the webcam, detects objects, and displays the detection results.

The pretrained model weights may be downloaded automatically the first time the model is loaded if they are not already available locally.

Press `q` while the camera window is active to exit.

### 6. Test speech separately

```bash
python speech_test.py
```

This checks whether the installed text-to-speech library can speak a sample sentence.

## Understanding the Main Technologies

### OpenCV

OpenCV is a Python library used to work with images and videos.

In this project, it helps us:
- Access the laptop webcam.
- Capture video frames.
- Display the camera feed.
- Show YOLO detection results.

### YOLO

YOLO stands for **You Only Look Once**.

It is a family of object-detection models that can identify objects in images.

For example, it may detect:
- Person
- Chair
- Bottle
- Laptop
- Cell phone

YOLO provides object labels and bounding boxes. Its confidence scores are estimates, not guarantees that a detection is correct.

### YOLO11n

We currently use `yolo11n.pt`.

- `yolo11` refers to the model family/version.
- `n` means the nano-sized variant.
- `.pt` is the model weights file.

A pretrained model has already learned patterns from training data, so we can use it without training our own model from scratch.

### Text-to-Speech

Text-to-speech (TTS) converts written text into spoken audio.

We currently use `pyttsx3` for our experiments.

Example:

```python
engine.say("I can see a person")
engine.runAndWait()
```

### Threads and Queues

We use a background thread for speech so that the camera-processing loop does not have to wait for every spoken sentence.

A queue acts like a waiting line:

- YOLO produces an announcement.
- The announcement enters the queue.
- The speech worker takes the next message.
- The speech engine speaks it.

This is our current design, but live speech playback still needs reliability improvements.

## Current Development Status

### Completed and tested

- [x] Python virtual environment created.
- [x] OpenCV installed.
- [x] Laptop webcam capture working on the development Mac.
- [x] Ultralytics installed.
- [x] YOLO11n model downloaded.
- [x] Live webcam object detection working.
- [x] Object labels and bounding boxes displayed.
- [x] `pyttsx3` installed.
- [x] Standalone speech test working.
- [x] Background speech queue and worker implemented.

### In progress

- [ ] Make YOLO-to-speech playback consistently reliable.
- [ ] Test the priority-based announcement implementation.
- [ ] Reduce repeated announcements.
- [ ] Prevent long queues of unnecessary speech messages.
- [ ] Improve announcement timing and wording.

### Planned

- [ ] Separate speech functionality into a reusable module.
- [ ] Implement and test cross-platform speech on macOS, Windows, and Linux.
- [ ] Add OCR to recognise printed text.
- [ ] Combine object detection, OCR, and speech into a complete software prototype.
- [ ] Test the system under different lighting and camera conditions.
- [ ] Explore an external camera such as ESP32-CAM.
- [ ] Develop a wearable camera prototype.
- [ ] Explore edge-AI hardware and additional assistive features.

## Current Announcement Design

We have chosen a **priority announcement style**.

Instead of announcing every detected object, Vision-Scribe should select one object category based on a priority list.

The initial proposed priority order is:

1. Person
2. Car
3. Bus
4. Motorcycle
5. Bicycle
6. Dog
7. Other detected objects if none of the listed categories are present

The latest proposed implementation includes an 8-second last-seen grace period and a 5-second announcement cooldown.

**Note:** This priority-based version is still awaiting testing. Category priority does not indicate actual danger, distance, or movement.

## Project Roadmap

### Phase 1 — Software Prototype

- Laptop webcam integration.
- YOLO object detection.
- Useful and reliable audio announcements.
- OCR for printed text.
- Testing and performance improvements.

### Phase 2 — External Camera

- Explore ESP32-CAM with OV2640.
- Send camera frames to the laptop over local Wi-Fi.
- Test image quality and transmission delay.

### Phase 3 — Wearable Prototype

- Mount the camera on glasses.
- Secure wiring and power.
- Test camera angle, comfort, and reliability.

### Phase 4 — Edge AI

- Explore suitable edge-AI hardware.
- Measure memory, speed, power consumption, and accuracy.
- Decide which tasks should run on the wearable and which should run on a nearby computer.

### Phase 5 — Advanced Assistance

- Explore distance sensors.
- Investigate directional alerts and haptic feedback.
- Add more advanced scene understanding after careful testing.

## Important Safety Note

Vision-Scribe is an experimental assistive information system.

Object detection alone cannot reliably determine whether a path is safe, how far away an object is, or whether an object is approaching.

It is not a validated navigation or collision-avoidance device and must not replace a white cane, guide dog, or other established mobility aid.

## Team Development Guidelines

- Keep code simple and beginner-friendly.
- Explain unfamiliar concepts before using them.
- Make one change at a time.
- Test every feature before marking it complete.
- Keep `requirements.txt` updated.
- Do not commit virtual environments or model-weight files.
- Never commit API keys, passwords, or other secrets.
- Test on Windows and Linux before claiming cross-platform support.

## Repository

GitHub: https://github.com/danyl-dnl/see-through

**Current focus:** Make YOLO-to-speech announcements useful, selective, and reliable before moving on to OCR or cross-platform speech refactoring.