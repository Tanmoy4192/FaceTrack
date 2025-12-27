import cv2
import face_recognition
import os
import time
import threading
import queue
from datetime import datetime

from config import *
from face_utils import (
    load_known_faces,
    recognize_face,
    register_new_person,
    save_unknown_face
)
from tracking_utils import PersonTracker
from db_utils import init_db, create_session, update_exit

print("[INFO] IPMAS is starting up...")

# ===================== DISPLAY SETTINGS =====================

# Target smooth display speed
TARGET_FPS = 30
FRAME_DELAY = int(1000 / TARGET_FPS)

# ===================== INITIAL SETUP =====================

# Make sure required folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)
os.makedirs(INTRUDER_SNAPSHOTS_DIR, exist_ok=True)

# Initialize database
init_db(DATABASE_PATH)

# Load known faces from disk
known_encodings, known_names = load_known_faces(KNOWN_FACES_DIR)

# Tracker keeps track of who enters and exits
tracker = PersonTracker()

# Open camera / video source
cap = cv2.VideoCapture(VIDEO_SOURCE)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("[ERROR] Unable to access camera")
    exit()

# ===================== THREADING VARIABLES =====================

# Queue holds the latest frame for recognition
frame_queue = queue.Queue(maxsize=1)

# Shared data between threads
latest_results = []
unknown_counter = 0
latency_ms = 0

# ===================== FACE RECOGNITION THREAD =====================

def recognition_worker():
    global latest_results, unknown_counter, latency_ms

    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        start_time = time.time()

        # Resize frame to improve recognition speed
        small = cv2.resize(
            frame, (0, 0),
            fx=FRAME_RESIZE_SCALE,
            fy=FRAME_RESIZE_SCALE
        )

        # Convert to RGB for face_recognition
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        # Detect face locations
        locations = face_recognition.face_locations(
            rgb_small, model="hog"
        )

        # Extract face encodings
        encodings = face_recognition.face_encodings(
            rgb_small, locations, num_jitters=1
        )

        results = []
        detected_now = set()

        for encoding, loc in zip(encodings, locations):
            top, right, bottom, left = [
                int(v / FRAME_RESIZE_SCALE) for v in loc
            ]

            # Try to match face with known people
            name = recognize_face(
                encoding,
                known_encodings,
                known_names,
                FACE_MATCH_THRESHOLD
            )

            # Handle unknown faces
            if name is None:
                unknown_id = tracker.identify_unknown(
                    encoding, FACE_MATCH_THRESHOLD
                )

                if unknown_id is None:
                    unknown_id = f"UNKNOWN_{unknown_counter}"
                    tracker.add_unknown(encoding, unknown_id)
                    unknown_counter += 1

                    # Save unknown face safely
                    h, w = frame.shape[:2]
                    if top < bottom and left < right and bottom <= h and right <= w:
                        save_unknown_face(
                            frame, (top, right, bottom, left), unknown_id
                        )

                name = unknown_id

            # Final safety check
            if not name or name.strip() == "":
                name = "Unknown"

            detected_now.add(name)

            # Track entry and exit events
            state = tracker.seen(name)

            if state == "ENTER":
                create_session(
                    DATABASE_PATH, name, datetime.now().isoformat()
                )

            elif isinstance(state, tuple):
                update_exit(
                    DATABASE_PATH,
                    name,
                    datetime.now().isoformat(),
                    state[1]
                )

            results.append((name, (top, right, bottom, left)))

        # Check for people who left the frame
        for pid in list(tracker.state.keys()):
            if pid not in detected_now:
                tracker.check_exit(pid, EXIT_TIMEOUT_SECONDS)

        latency_ms = int((time.time() - start_time) * 1000) 
        latest_results = results


# Start recognition in background thread
threading.Thread(
    target=recognition_worker,
    daemon=True
).start()

print("[INFO] Press 'q' to quit | Press 'r' to register a new face")

# ===================== MAIN CAMERA LOOP =====================

frame_count = 0
fps_counter = 0
fps = 0
fps_timer = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    fps_counter += 1

    # Update FPS every second
    if time.time() - fps_timer >= 1:
        fps = fps_counter
        fps_counter = 0
        fps_timer = time.time()

    # Send frame to recognition thread when allowed
    if frame_count % FRAME_SKIP == 0 and frame_queue.empty():
        frame_queue.put(frame.copy())

    display = frame.copy()

    # Draw last known recognition results
    for name, (top, right, bottom, left) in latest_results:
        color = (0, 255, 0) if not name.startswith("UNKNOWN") else (0, 0, 255)

        cv2.rectangle(display, (left, top), (right, bottom), color, 2)
        cv2.putText(
            display,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    # Show performance details
    cv2.putText(
        display,
        f"FPS: {fps} | Recognition Time: {latency_ms} ms",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow("IPMAS - Live Camera Feed", display)

    key = cv2.waitKey(FRAME_DELAY) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('r'):
        cap.release()
        cv2.destroyAllWindows()

        person = input("Enter the person's name to register: ").strip()
        cap = cv2.VideoCapture(VIDEO_SOURCE)
        time.sleep(1)

        success = register_new_person(
            cap,
            KNOWN_FACES_DIR,
            person
        )

        if success is not False:
            known_encodings, known_names = load_known_faces(KNOWN_FACES_DIR)
            print("[INFO] Face data updated successfully")

# ===================== CLEANUP =====================

frame_queue.put(None)
cap.release()
cv2.destroyAllWindows()
print("[INFO] IPMAS has been shut down safely")
