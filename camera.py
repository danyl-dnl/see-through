
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access camera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera started successfully!")
print("Click the camera window and press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    cv2.imshow("Vision-Scribe Camera", frame)

    key = cv2.waitKey(30) & 0xFF

    if key == ord('q') or cv2.getWindowProperty(
        "Vision-Scribe Camera", cv2.WND_PROP_VISIBLE
    ) < 1:
        break

cap.release()
cv2.destroyAllWindows()

print("Camera closed.")
