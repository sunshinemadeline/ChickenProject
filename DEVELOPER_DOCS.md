# 🧸Animal Detection System – Developer Documentation

This document provides a detailed technical overview for future developers who want to maintain, modify, or extend this Raspberry Pi-based object detection system. 
It is targeted at future CSC students or engineering team members who are comfortable with Python, hardware integration, and machine learning.

---

## 🧠 Project Purpose

This system uses a custom YOLOv5 object detection model to classify between animals (bear or raccoon) using a Raspberry Pi and camera module. 
Based on the detected class, it plays a specific `.mp3` file via a connected speaker and logs the detection.

---

## 🗂 Project Structure
animal-detector/ 
├── detect_animals.py # Main program script 
├── best.pt # Trained YOLOv5 model 
├── bear.mp3 # Audio file for bear
├── raccoon.mp3 # Audio file for stuffed raccoon
├── detection_log.txt # Automatically generated log of detections
├── README.md # Project overview
├── USER_GUIDE.md # End-user documentation 
├── REQUIREMENTS.md # Functional & non-functional requirements 
└── DEVELOPER_DOCS.md # This file

---

## 🔧 Major Modules

### `main.py`

This is the main script that:

1. **Initializes** the camera using OpenCV (`cv2.VideoCapture`).
2. **Loads** the YOLOv5 model from the `torch.hub` or local repo.
3. **Processes** each camera frame in a loop:
   - Feeds the frame into the YOLOv5 model.
   - Extracts predictions.
   - Matches label (`bear` or `raccoon`) with predefined actions.
4. **Plays** corresponding `.mp3` file using `pygame` to call `pygame.mixer.music.load`.
5. **Logs** detection time and label to a local file.

---

## 🖼️ System Architecture

```text
+--------------------+
|  Raspberry Pi 4    |
|--------------------|
| Camera Module (CSI)|
| YOLOv5 Inference   |
| Audio Playback     |
| Detection Logging  |
+--------------------+
        |                
     [Camera] ---------> [YOLOv5 Model]
                          |       |
                    [bear.mp3] [raccoon.mp3]
                          |
                    [detection_log.txt]
---

## 🧠 Key Concepts

YOLOv5 Integration:

YOLOv5 is loaded using torch.hub.load() or local clone.
The model must be trained to recognize "bear" and "raccoon" classes.
Run inference on each frame from the camera.
Results are filtered based on label name.

Audio Playback:

.mp3 files are played using:
    pygame.mixer.init()
    pygame.mixer.music.load("bear.mp3")
    pygame.mixer.music.play()
Ensure the USB speaker is the default audio output.

Logging:

Format: "YYYY-MM-DD HH:MM:SS - Detected: <label>".
Appended to detection_log.txt on every detection.

## 🔍 Setup Notes

Camera uses OpenCV via cv2.VideoCapture(1)

If USB audio doesn't work, use alplay or sudo raspi-config to change the output device.

All required Python libraries are listed in USER_GUIDE.md.

## 🧪 Testing and Debugging Tips

Use test images to verify camera and model functionality.

Check camera and USB speaker functionality separately before running the main script.

Use print/debug statements to verify detection logic if the audio doesn't play.

## 🚀 Future Improvements

🔊 Add volume control or dynamic audio playback options.

🤖 Add more classes (e.g., other animals, humans, unknown objects).

💡 Add LED or screen output to indicate detections visually.

🌐 Enable cloud syncing of detection logs or notifications.

🛠 Improve robustness with retries and fallback logic.





