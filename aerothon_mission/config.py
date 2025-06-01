# config.py

# Mission Altitude Settings (in meters)
MISSION_ALTITUDE = 15         # Altitude for grid search
DROP_ALTITUDE = 10            # Altitude to descend to for payload drop

# Geofence Configuration (center of circular region)
GEOFENCE_CENTER = (12.9716, 77.5946)  # Latitude, Longitude
GEOFENCE_RADIUS_M = 40               # Radius in meters

# Camera Field of View (degrees)
CAMERA_HFOV = 62.2  # Horizontal FOV
CAMERA_VFOV = 48.8  # Vertical FOV

# Object Detection Model
MODEL_PATH = "yolo_recognize/best.pt"            # YOLO model path
DISASTER_CLASSES = ['fire', 'flooding', 'damage']  # Disaster class labels to detect

# Drone Communication (for SITL or UDP-based controller)
CONNECTION_STRING = 'udp:127.0.0.1:14550'
