## 🚁 Autonomous Drone Disaster Detection System

This project presents a fully autonomous drone system powered by Raspberry Pi 5, Pixhawk (ArduPilot), and real-time AI-powered disaster detection using YOLOv8. The drone is capable of:

* Navigating within a defined geofence,
* Performing a spiral search pattern,
* Detecting disasters such as **traffic accidents** or **road incidents** using a live AI camera feed,
* Redirecting its flight toward the detected event,
* Executing a payload drop, and
* Returning safely to the launch point.

---

## 🎯 Project Objective

To build a robust **autonomous navigation system** for a drone that leverages onboard computer vision to detect real-world incidents in real time and respond with defined mission behaviors — useful in emergency response, aerial monitoring, and disaster relief.

---

## 🧩 Hardware Components

| Component             | Description                                     |
| --------------------- | ----------------------------------------------- |
| Raspberry Pi 5 (16GB) | Runs detection model and flight control scripts |
| AI Pi Camera          | Captures real-time video for object detection   |
| Pixhawk 4             | ArduPilot-based flight controller               |
| UART Serial Link      | Communication between Pi and Pixhawk            |
| Custom Payload System | Triggered for simulated delivery post-detection |

---

## 🛠 Software Stack

* **ArduPilot (ArduCopter firmware)** – for flight control
* **DroneKit-Python** – to interact with MAVLink via Pixhawk
* **YOLOv8 (Ultralytics)** – for onboard object detection
* **picamera2** – for Raspberry Pi camera interface
* **Python 3.11** – base scripting
* **QGroundControl** – used for live telemetry and geofence configuration

---

## 📁 Project Structure & File Descriptions

| File | Purpose |
| ---- | ------- |

### 🧠 Core AI & Detection

* **`yolo_recognize/best.pt`**
  Custom-trained YOLOv8 model (detects `traffic_accident` and `road_incident`).

* **`camera_disaster_detector.py`**
  Captures camera input using `picamera2`, runs YOLO, interprets direction of detection (left/right/center), and returns results.

* **`depth_estimator.py`**
  (Optional) Uses MiDaS depth estimation to calculate how far detected object is from the drone for better redirection.

---

### 🛰 Drone Navigation Logic

* **`main_mission.py`**
  The mission controller. Connects the drone, arms it, takes off, enters geofence, performs spiral search, detects disaster, drops payload, and returns to launch.

* **`spiral_search.py`**
  Performs an inward spiral flight path starting from geofence edge. Integrates detection logic and breaks loop to redirect drone upon disaster detection.

* **`arm_and_takeoff.py`**
  Handles vehicle arming and controlled takeoff to target altitude.

* **`rtl_home.py`**
  Triggers Return-To-Launch (RTL) using `VehicleMode("RTL")`.

* **`payload.py`**
  Simulates payload drop mechanism (e.g., opening a servo or triggering GPIO).

---

### 🔌 Vehicle Connection Interfaces

* **`connect_vehicle.py`**
  Connects to ArduPilot over SITL or UDP.

* **`connect_uart.py`**
  Used when Raspberry Pi communicates with Pixhawk over physical UART (`/dev/serial0`) using DroneKit.

---

### 📄 Miscellaneous

* **`README.md`**
  This documentation file.

* **`label.ipynb`**
  (Optional) Used for annotating training images for YOLO.

* **`yolov8n.pt`**
  Official base YOLOv8n weights file (pre-trained).

---

## 🚀 Flight Logic Overview

1. **Startup:** Pi connects to Pixhawk via UDP or UART.
2. **Takeoff:** Drone ascends to 15 meters in GUIDED mode.
3. **Spiral Search:** Drone flies inward spiral path inside geofence.
4. **Detection:** YOLOv8 scans each frame; if confidence > 0.6, returns direction.
5. **Redirect:** Drone stops spiral and flies 10–20m toward detected object.
6. **Payload Drop:** Drone descends to 10m, simulates payload release.
7. **Return:** Drone climbs to 15m and returns to home location via RTL.

---

## 📌 How to Run

1. Flash ArduPilot on Pixhawk.
2. Setup QGroundControl & geofence.
3. Power Raspberry Pi, connect camera and UART to Pixhawk.
4. SSH into Pi and run:

```bash
python3 main_mission.py
```

5. Watch drone behavior via QGC or SITL.

---

## ✅ Outcomes

This system allows a drone to:

* Operate autonomously with zero ground intervention
* Detect and respond to real-world disaster scenarios
* Adapt its mission flow based on onboard visual inference
---
