# ===================== CAMERA SETTINGS =====================

# Camera index or IP camera stream URL
VIDEO_SOURCE = 0  # "http://10.144.224.143:8000/video"

# Frame scaling factor used during recognition
# Lower values increase speed but reduce accuracy
FRAME_RESIZE_SCALE = 0.25   # Avoid going lower than this


# ===================== PERFORMANCE TUNING =====================

# Run face recognition once every N frames
FRAME_SKIP = 8   # Balanced for smooth display and stable recognition

# Face match sensitivity (lower = stricter matching)
FACE_MATCH_THRESHOLD = 0.45


# ===================== TRACKING / EXIT LOGIC =====================

# Time (in seconds) before a person is considered to have exited
EXIT_TIMEOUT_SECONDS = 5


# ===================== FILE PATHS =====================

KNOWN_FACES_DIR = "data/known_faces"
UNKNOWN_FACES_DIR = "data/unknown_faces"
INTRUDER_SNAPSHOTS_DIR = "data/intruders"

DATABASE_PATH = "data/attendance.db"


# ===================== RUNTIME BEHAVIOR =====================

# Whether to flag and store unknown faces
ALERT_UNKNOWN = True
