import torch
import pygame
from datetime import datetime
import time
from picamera2 import Picamera2
import cv2

# ---- SETTINGS ----
MODEL_PATH = 'best.pt'
BEAR_SOUND_PATH = 'bear.wav'
RACCOON_SOUND_PATH = 'raccoon.wav'
LOG_FILE_PATH = 'detection_log.txt'

# ---- INITIALIZE MODEL ----
print("Loading YOLOv5 model...")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)

# ---- INITIALIZE CAMERA ----
print("Initializing Pi Camera with Picamera2...")
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# ---- INITIALIZE AUDIO ----
print("Initializing audio...")
pygame.mixer.init()
bear_sound = pygame.mixer.Sound(BEAR_SOUND_PATH)
raccoon_sound = pygame.mixer.Sound(RACCOON_SOUND_PATH)

# ---- UTILITIES ----
def log_detection(label):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"{timestamp} - {label}\n")
    print(f"[LOGGED] {timestamp} - {label}")

def play_sound(label):
    if label == "stuffed bear":
        bear_sound.play()
    elif label == "stuffed raccoon":
        raccoon_sound.play()

# ---- MAIN LOOP ----
print("Starting detection loop. Press Ctrl+C to exit.")
try:
    while True:
        frame = picam2.capture_array()
        results = model(frame)
        labels = results.pandas().xyxy[0]['name'].tolist()

        detected = set()
        for label in labels:
            if label in ["stuffed bear", "stuffed raccoon"]:
                if label not in detected:
                    log_detection(label)
                    play_sound(label)
                    detected.add(label)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    pygame.mixer.quit()
    picam2.stop()
