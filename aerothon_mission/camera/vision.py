# camera/vision.py

import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from config import MODEL_PATH, DISASTER_CLASSES

# Load YOLO model
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
    print("📷 AI Pi Camera initialized.")
    return picam2

def capture_frame():
    return picam2.capture_array()

def detect_objects(frame):
    results = model(frame)[0].boxes
    for box in results:
        cls = int(box.cls.item())
        label = model.names[cls]
        object_counts[label] = object_counts.get(label, 0) + 1

def detect_disaster_and_direction(frame, target_classes=DISASTER_CLASSES):
    results = model(frame)
    detections = results[0].boxes.data
    frame_width = frame.shape[1]

    # Show detection preview
    annotated = results[0].plot()
    cv2.imshow("Detection", annotated)
    cv2.waitKey(1)

    for box in detections:
        x1, y1, x2, y2, conf, cls = box.tolist()
        label = model.names[int(cls)]
        print(f"Detected label: {label}, Confidence: {conf:.2f}")

        if label in target_classes and conf >= 0.6:
            cx = (x1 + x2) / 2
            print(f"Bounding box center at x = {cx:.2f} of frame width {frame_width}")

            if cx < frame_width * 0.33:
                return True, "left"
            elif cx > frame_width * 0.66:
                return True, "right"
            else:
                return True, "center"

    return False, None
