import cv2
import torch
import pygame
from datetime import datetime
import time
import sys
import subprocess
import numpy as np

# ---- SETTINGS ----
MODEL_PATH = 'best.pt'
BEAR_SOUND_PATH = 'bear.wav'
RACCOON_SOUND_PATH = 'raccoon.wav'
LOG_FILE_PATH = 'detection_log.txt'

# ---- LOAD MODEL ----
try:
    print("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)
except Exception as e:
    print(f"[ERROR] Failed to load YOLOv5 model: {e}")
    sys.exit(1)

# ---- INIT AUDIO ----
try:
    pygame.mixer.init()
    bear_sound = pygame.mixer.Sound(BEAR_SOUND_PATH)
    raccoon_sound = pygame.mixer.Sound(RACCOON_SOUND_PATH)
except Exception as e:
    print(f"[ERROR] Audio init failed: {e}")
    sys.exit(1)

# ---- INIT CAMERA ----
try:
    print("Attempting to open camera with OpenCV...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[WARNING] Default camera capture failed. Trying ffmpeg pipe from libcamera-vid...")
        cap = cv2.VideoCapture("ffmpeg -i /dev/video0 -f v4l2 -pix_fmt yuyv422 -video_size 640x480 -", cv2.CAP_FFMPEG)

    if not cap.isOpened():
        raise Exception("Could not open camera via OpenCV.")

except Exception as e:
    print(f"[ERROR] Camera init failed: {e}")
    sys.exit(1)

# ---- UTILITIES ----
def log_detection(label):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE_PATH, "a") as f:
            f.write(f"{timestamp} - {label}\n")
        print(f"[LOGGED] {timestamp} - {label}")
    except Exception as e:
        print(f"[WARNING] Failed to log: {e}")

def play_sound(label):
    try:
        if label == "stuffed bear":
            bear_sound.play()
        elif label == "stuffed raccoon":
            raccoon_sound.play()
    except Exception as e:
        print(f"[WARNING] Sound playback failed for {label}: {e}")

# ---- MAIN LOOP ----
print("Starting detection loop. Press Ctrl+C to stop.")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Failed to capture frame.")
            time.sleep(1)
            continue

        try:
            results = model(frame)
            labels = results.pandas().xyxy[0]['name'].tolist()
        except Exception as e:
            print(f"[WARNING] Inference failed: {e}")
            continue

        detected = set()
        for label in labels:
            if label in ["stuffed bear", "stuffed raccoon"]:
                if label not in detected:
                    log_detection(label)
                    play_sound(label)
                    detected.add(label)

        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Exiting program...")

finally:
    cap.release()
    pygame.mixer.quit()

