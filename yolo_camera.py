
import cv2
import pyttsx3
import threading
import queue
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Create speech queue
speech_queue = queue.Queue()


# Speech function
def speech_worker():

    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    print("Speech engine started!")

    while True:

        message = speech_queue.get()

        if message is None:
            speech_queue.task_done()
            break

        print("Speaking:", message)

        engine.say(message)
        engine.runAndWait()

        speech_queue.task_done()

    engine.stop()


# Start speech thread
speech_thread = threading.Thread(target=speech_worker)
speech_thread.start()


# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    speech_queue.put(None)
    speech_thread.join()
    exit()

print("Vision-Scribe started!")
print("Press q to quit")


# Object priority list
priority_objects = [
    "person",
    "car",
    "bus",
    "motorcycle",
    "bicycle",
    "dog"
]

# Remember last announced object
last_announced_object = None

# Track when objects were last seen
last_seen = {}

# Cooldown period
grace_period = 8

# Prevent frequent announcements
announcement_cooldown = 5

last_announcement_time = 0


while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Detect objects
    results = model(frame, verbose=False)

    # Draw detection boxes
    detected_frame = results[0].plot()

    # Get detected object names
    current_objects = set()

    for box in results[0].boxes:

        object_name = model.names[int(box.cls[0])]
        current_objects.add(object_name)

    current_time = time.time()

    # Update last seen time
    for object_name in current_objects:
        last_seen[object_name] = current_time

    # Remove objects not seen for 8 seconds
    for object_name in list(last_seen.keys()):

        if current_time - last_seen[object_name] > grace_period:
            del last_seen[object_name]

            if object_name == last_announced_object:
                last_announced_object = None

    # Select the highest-priority detected object
    selected_object = None

    for object_name in priority_objects:

        if object_name in current_objects:
            selected_object = object_name
            break

    # If no priority object is present, select another object
    if selected_object is None and current_objects:

        selected_object = sorted(current_objects)[0]

    # Announce selected object
    if selected_object is not None:

        if (
            selected_object != last_announced_object
            and current_time - last_announcement_time > announcement_cooldown
        ):

            message = "I can see a " + selected_object

            print(message)

            speech_queue.put(message)

            last_announced_object = selected_object
            last_announcement_time = current_time

    # Display camera
    cv2.imshow("Vision-Scribe", detected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Close camera
cap.release()
cv2.destroyAllWindows()


# Finish pending announcements
speech_queue.put(None)
speech_thread.join()

print("Vision-Scribe stopped.")
