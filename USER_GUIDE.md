# 🧸 Animal Detection System – User Guide

This guide walks you through setting up and running the Animal Audio Alert System. 
The system detects bears and raccoons using a Raspberry Pi, a YOLOv5 model, and a connected USB speaker, and plays audio alerts based on the detected object.

---

## 📦 Hardware Requirements

- Raspberry Pi 5 (or equivalent with sufficient power)
- IMX462 2MP Color Ultra Low Light STARVIS HDR Camera (connected via ribbon cable)
- USB-powered speaker
- MicroSD card with Raspberry Pi OS installed
- Internet connection for initial setup
- HDMI monitor and keyboard for first-time setup (optional if using SSH)

---

## 🔧 Wiring & Setup

- Connect the **IMX462 camera** to the Pi's CSI camera port 1.
- Plug in the **USB speaker** to a free USB port.
- Ensure the camera is enabled via `raspi-config`:
  ```bash
  sudo raspi-config

💾 Software Installation

1. Clone the Repository

  git clone https://github.com/sunshinemadeline/ChickenProject.git
  cd Chicken Project

2. Set Up Python Environment

  python3 -m venv venv
  source venv/bin/activate

3. Set Up Raspi
   # Upgrade pip
   sudo apt-get update
   sudo apt-get install python3-pip
   pip install --upgrade pip

4. Install YOLOv5 and Dependencies

  git clone https://github.com/ultralytics/yolov5.git
  cd yolov5
  pip install -r requirements.txt
  Ensure that best.pt is moved to and placed inside Yolov5/runs/train/animal_detection/weights

6. Install Libraries/Requirements
  pip3 install torch 
  pip3 install torch torchvision torchaudio
  sudo apt install python3-opencv
  pip3 install pygame

7. Check Audio:
  aplay -l
  sudo nano /etc/asound.conf
  defaults.pcm.card 2
  defaults.ctl.card 2
  sudo reboot

8. Check Camera:
  wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
  chmod +x install_pivariety_pkgs.sh
  ./install_pivariety_pkgs.sh -p libcamera_dev
  ./install_pivariety_pkgs.sh -p libcamera_apps
  sudo nano /boot/firmware/config.txt 
  #Find the line: [all], add the following item under it:
  dtoverlay=arducam-pivariety
  #Save and reboot.
  libcamera-still -t 5000

9. SSH:
  sudo nmcli device wifi hotspot ssid <ssid> password <password> ifname wlan0
  - get the UUID
  sudo systemctl edit systemd-rfkill
  [Service]
  ExecStart=
  ExecStart=/usr/sbin/rfkill unblock all
  sudo nmcli connection modify <hotspot UUID> connection.autoconnect yes
  sudo nmcli connection modify <hotspot UUID> connection.autoconnect-priority 100
  sudo nmcli connection up <hotspot UUID>
  sudo reboot now
  
  ssh ID@IPaddress

▶️ Running the Program
From the main project directory:
python main.py

The script will:

Capture video via the IMX462 camera using OpenCV.

Run YOLOv5 inference on each frame.

Play a sound via USB speaker if a bear (bear.wav) or raccoon (raccoon.wav) is detected.

Log the time and detection to detection_log.txt.

🧪 Testing Your Setup
Show the camera a photo or object that resembles your labeled bear or raccoon.

Verify that:

The correct .wav file plays.

A log is added to detection_log.txt.

🛠 Troubleshooting

Issue	Solution
No camera found	-> Check camera ribbon cable and run raspi-config to enable the camera.
Audio doesn't play ->	Ensure your USB speaker is selected as the default output using alsamixer or sudo raspi-config.
Model not detecting anything	-> Check if best.pt is correctly placed in the directory. Try adjusting the lighting or object distance.
Dependency errors	-> Run pip install -r requirements.txt again. Make sure you're in the virtual environment.
"No module named torch"	-> Install PyTorch manually: pip install torch torchvision torchaudio. Make sure your Pi has enough memory.


