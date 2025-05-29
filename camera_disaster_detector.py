import cv2
from ultralytics import YOLO

# Load the trained model
model = YOLO("yolo_recognize/yolov8n.pt")
model.conf = 0.5  # Confidence threshold

def init_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("❌ Camera not accessible")
    return cap

def detect_disaster_and_direction(cap, target_classes=['road_incident', 'traffic_incident']):
    ret, frame = cap.read()
    if not ret:
        return False, None

    results = model(frame)
    detections = results[0].boxes.data

    frame_width = frame.shape[1]
    cv2.imshow("Detection", frame)
    for box in detections:
        x1, y1, x2, y2, conf, cls = box.tolist()
        label = model.names[int(cls)]
        if label in target_classes:
            cx = (x1 + x2) / 2

            if cx < frame_width * 0.33:
                return True, "left"
            elif cx > frame_width * 0.66:
                return True, "right"
            else:
                return True, "center"

    return False, None
