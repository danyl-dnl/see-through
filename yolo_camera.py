
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11n.pt")

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()

print("Vision-Scribe object detection started!")
print("Press q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Detect objects in the camera frame
    results = model(frame, verbose=False)

    # Draw detection boxes and labels
    detected_frame = results[0].plot()

    # Display the result
    cv2.imshow("Vision-Scribe - Object Detection", detected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
