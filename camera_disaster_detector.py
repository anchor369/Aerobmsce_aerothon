from picamera2 import Picamera2
import time
import cv2
from ultralytics import YOLO

# Load model
model = YOLO("yolo_recognize/yolov8n.pt")
model.conf = 0.5

picam2 = None  # Global for reuse

def init_camera():
    global picam2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    picam2.start()
    time.sleep(2)  # Camera warm-up
    print("📷 AI Pi Camera initialized.")
    return picam2

def detect_disaster_and_direction(picam2, target_classes=['road_incident', 'traffic_accident']):
    frame = picam2.capture_array()

    results = model(frame)
    detections = results[0].boxes.data
    frame_width = frame.shape[1]

    # Show with bounding boxes
    annotated = results[0].plot()
    cv2.imshow("Detection", annotated)
    cv2.waitKey(1)

    for box in detections:
        x1, y1, x2, y2, conf, cls = box.tolist()
        label = model.names[int(cls)]
        print(f"🔍 Detected label: {label}, Confidence: {conf:.2f}")
        
        if label in target_classes and conf >= 0.6:
            cx = (x1 + x2) / 2
            print(f"📦 BBox detected at cx: {cx}")
    
            if cx < frame_width * 0.33:
                return True, "left"
            elif cx > frame_width * 0.66:
                return True, "right"
            else:
                return True, "center"


    return False, None
