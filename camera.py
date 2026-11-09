import cv2

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera opened:", cap.isOpened())

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame capture failed")
        break

    print("Shape:", frame.shape)
    print("Minimum:", frame.min())
    print("Maximum:", frame.max())
    print("Mean:", frame.mean())

    cv2.imshow("Vision-Scribe Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()