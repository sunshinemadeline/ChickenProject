import cv2
import torch
import pygame
import time

# --- CAMERA TEST ---
print("[1/3] Testing camera...")
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if not ret:
    print("❌ Failed to capture image from camera.")
else:
    print("✅ Camera working. Saving test image as 'test.jpg'")
    cv2.imwrite("test.jpg", frame)

cap.release()

# --- YOLOv5 TEST ---
print("[2/3] Testing YOLOv5...")
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # Nano model = faster
    results = model("test.jpg")  # Run detection on the test image
    results.print()  # Print results to terminal
    print("✅ YOLOv5 ran successfully on captured image.")
except Exception as e:
    print("❌ YOLOv5 error:", e)

# --- SPEAKER TEST ---
print("[3/3] Testing speaker...")
try:
    pygame.mixer.init()
    pygame.mixer.music.load("test.wav")  # Replace with your actual test file
    pygame.mixer.music.play()
    print("✅ Speaker playing 'test.wav'. Waiting for it to finish...")
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
except Exception as e:
    print("❌ Speaker error:", e)
