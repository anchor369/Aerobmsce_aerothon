# camera/vision.py (Simulation Mode)

import time
import cv2
import random
from picamera2 import Picamera2
from ultralytics import YOLO
from config import MODEL_PATH, DISASTER_CLASSES

# Load YOLO model (can be unused in pure simulation)
model = YOLO(MODEL_PATH)
model.conf = 0.5

picam2 = None
object_counts = {}

def init_camera():
    global picam2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    picam2.start()
    time.sleep(2)
    print("Camera initialized.")
    return picam2

def capture_frame():
    return picam2.capture_array()

def detect_objects(frame):
    simulated_objects = ['cone', 'ball', 'cylinder', 'cube']
    current_detection = {}
    for _ in range(random.randint(2, 4)):
        label = random.choice(simulated_objects)
        object_counts[label] = object_counts.get(label, 0) + 1
        current_detection[label] = current_detection.get(label, 0) + 1
    print(f"[SIM] Detected objects at this waypoint: {current_detection}")


def detect_disaster_and_direction(frame, target_classes=DISASTER_CLASSES):
    """
    Simulated disaster detection with randomized output.
    """
    if random.random() < 0.1:  # 10% chance to simulate a disaster
        direction = random.choice(["left", "center", "right"])
        print(f"[SIM] Disaster detected in {direction} direction")
        return True, direction

    return False, None
