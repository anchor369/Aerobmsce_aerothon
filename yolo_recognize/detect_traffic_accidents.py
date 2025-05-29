from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("D:/coding/aerothon/disaster_detection/runs/detect/train/weights/best.pt")

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame, conf=0.5)

    # Draw the boxes
    annotated_frame = results[0].plot()

    # Show the frame
    cv2.imshow("Webcam Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
