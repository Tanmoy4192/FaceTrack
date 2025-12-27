import face_recognition
import cv2
import os
from datetime import datetime
from config import UNKNOWN_FACES_DIR, INTRUDER_SNAPSHOTS_DIR


# ===================== KNOWN FACE LOADING =====================

def load_known_faces(known_dir):
    encodings = []
    names = []

    if not os.path.exists(known_dir):
        return encodings, names

    for person in os.listdir(known_dir):
        person_path = os.path.join(known_dir, person)
        if not os.path.isdir(person_path):
            continue

        for img in os.listdir(person_path):
            img_path = os.path.join(person_path, img)
            try:
                image = face_recognition.load_image_file(img_path)
                face_encs = face_recognition.face_encodings(image)
                if face_encs:
                    encodings.append(face_encs[0])
                    names.append(person)
            except Exception:
                # Skip unreadable or invalid images
                continue

    return encodings, names


# ===================== FACE MATCHING =====================

def recognize_face(face_encoding, known_encodings, known_names, threshold):
    if not known_encodings:
        return None

    distances = face_recognition.face_distance(
        known_encodings, face_encoding
    )

    min_dist = distances.min()
    if min_dist < threshold:
        return known_names[distances.argmin()]

    return None


# ===================== FACE REGISTRATION =====================

def register_new_person(cap, save_dir, person_name, samples=15):
    person_dir = os.path.join(save_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)

    print(f"[INFO] Starting registration for {person_name}. Please face the camera.")

    saved = 0
    attempts = 0
    max_attempts = samples * 5   # avoid endless capture attempts

    while saved < samples and attempts < max_attempts:
        ret, frame = cap.read()
        if not ret:
            attempts += 1
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, locations)

        display = frame.copy()

        if len(encodings) == 1:
            top, right, bottom, left = locations[0]

            # Validate crop bounds
            h, w = frame.shape[:2]
            if top < bottom and left < right and bottom <= h and right <= w:
                face_img = frame[top:bottom, left:right]

                img_path = os.path.join(
                    person_dir, f"{saved}.jpg"
                )
                cv2.imwrite(img_path, face_img)

                saved += 1

                cv2.rectangle(
                    display, (left, top), (right, bottom), (0, 255, 0), 2
                )
                cv2.putText(
                    display,
                    f"Captured {saved}/{samples}",
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("Registration", display)
                cv2.waitKey(400)  # slower capture improves image clarity
                continue

        # User feedback when face detection is not ideal
        cv2.putText(
            display,
            "Hold still, keep your face visible",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )
        cv2.imshow("Registration", display)
        cv2.waitKey(1)

        attempts += 1

    cv2.destroyWindow("Registration")

    if saved >= samples:
        print(f"[SUCCESS] Registration completed for {person_name}.")
        return True
    else:
        print("[ERROR] Registration incomplete. Please retry in better lighting.")
        return False


# ===================== UNKNOWN / INTRUDER HANDLING =====================

def save_unknown_face(frame, face_location, unknown_id):
    os.makedirs(INTRUDER_SNAPSHOTS_DIR, exist_ok=True)

    top, right, bottom, left = face_location
    h, w = frame.shape[:2]

    if not (top < bottom and left < right and bottom <= h and right <= w):
        return None

    face_img = frame[top:bottom, left:right]
    if face_img.size == 0:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(
        INTRUDER_SNAPSHOTS_DIR,
        f"{unknown_id}_{timestamp}.jpg"
    )

    cv2.imwrite(path, face_img)
    return path
