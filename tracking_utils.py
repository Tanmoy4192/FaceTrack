from datetime import datetime
import numpy as np


class PersonTracker:
    def __init__(self):
        # Tracks current state for each person
        self.state = {}

        # Storage for unknown face encodings
        self.unknown_encodings = []
        self.unknown_ids = []

    def seen(self, person_id):
        """
        Update tracking state when a person is detected in the frame.
        """
        now = datetime.now()

        if person_id not in self.state:
            self.state[person_id] = {
                "inside": True,
                "last_seen": now,
                "last_exit": None
            }
            return "ENTER"

        person = self.state[person_id]

        if not person["inside"]:
            outside_time = (
                now - person["last_exit"]
            ).total_seconds()

            person["inside"] = True
            person["last_seen"] = now
            return "REENTER", outside_time

        person["last_seen"] = now
        return "INSIDE"

    def check_exit(self, person_id, timeout):
        """
        Mark a person as exited if they haven't been seen
        for longer than the given timeout.
        """
        now = datetime.now()
        person = self.state.get(person_id)

        if person and person["inside"]:
            diff = (
                now - person["last_seen"]
            ).total_seconds()

            if diff > timeout:
                person["inside"] = False
                person["last_exit"] = now
                return now

        return None

    def identify_unknown(self, face_encoding, threshold=0.45):
        """
        Try to match an unknown face against previously
        seen unknown encodings.
        """
        if not self.unknown_encodings:
            return None

        distances = np.linalg.norm(
            np.array(self.unknown_encodings) - face_encoding,
            axis=1
        )

        min_dist = min(distances)

        if min_dist < threshold:
            return self.unknown_ids[distances.argmin()]

        return None

    def add_unknown(self, face_encoding, unknown_id):
        """
        Store a new unknown face encoding for future matching.
        """
        self.unknown_encodings.append(face_encoding)
        self.unknown_ids.append(unknown_id)
