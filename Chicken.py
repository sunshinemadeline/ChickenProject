import cv2
import torch
import RPi.GPIO as GPIO
import pygame
from datetime import datetime

# Setup for camera, GPIO, and pygame
cap = cv2.VideoCapture(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # GPIO pin for floodlight
pygame.mixer.init()

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

while True:
    ret, frame = cap.read()  # Capture a frame
    results = model(frame)  # Detect objects

    labels = results.names
    detections = results.xywh[0]  # Bounding boxes and labels

    for detection in detections:
        label = labels[int(detection[5])]
        
        if label == 'person':
            print("Detected a human.")
            # Do nothing for human but log it
            with open('animal_log.txt', 'a') as file:
                file.write(f"{datetime.now()} - Detected human\n")
        
        elif label == 'bear':
            print("Detected a stuffed bear.")
            GPIO.output(17, GPIO.HIGH)  # Turn on floodlight
            pygame.mixer.music.load("bear_sound.wav")  # Play bear sound
            pygame.mixer.music.play()
            with open('animal_log.txt', 'a') as file:
                file.write(f"{datetime.now()} - Detected stuffed bear\n")
        
        elif label == 'raccoon':
            print("Detected a stuffed raccoon.")
            GPIO.output(17, GPIO.HIGH)  # Turn on floodlight
            pygame.mixer.music.load("raccoon_sound.wav")  # Play raccoon sound
            pygame.mixer.music.play()
            with open('animal_log.txt', 'a') as file:
                file.write(f"{datetime.now()} - Detected stuffed raccoon\n")

    # Reset floodlight after some time (optional)
    GPIO.output(17, GPIO.LOW)

cap.release()  # Release camera when done
GPIO.cleanup()  # Clean up GPIO
