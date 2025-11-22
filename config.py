"""
Configuration file for Face Recognition Attendance System
Adjust these settings to customize the system behavior
"""

# ===== PATHS =====
HAARCASCADE_PATH = "haarcascade_frontalface_default.xml"
TRAINING_IMAGE_LABEL_PATH = "./TrainingImageLabel/Trainner.yml"
TRAINING_IMAGE_PATH = "./TrainingImage"
STUDENT_DETAIL_PATH = "./StudentDetails/studentdetails.csv"
ATTENDANCE_PATH = "Attendance"

# ===== FACE RECOGNITION SETTINGS =====
# Confidence threshold for face recognition (0-150)
# In LBPH, LOWER values = BETTER match (it's a distance metric)
# Recommended: 50-60 for strict recognition, 70-80 for lenient
# Faces with confidence ABOVE this threshold will be marked as Unknown
CONFIDENCE_THRESHOLD = 50  # Stricter - only very confident matches accepted

# Scale factor for face detection (1.1 - 1.5 recommended)
# Smaller values = more accurate but slower
SCALE_FACTOR = 1.2

# Minimum neighbors for face detection (3-6 recommended)
# Higher values = fewer false positives but might miss some faces
MIN_NEIGHBORS = 5

# ===== IMAGE CAPTURE SETTINGS =====
# Number of images to capture per student during registration
IMAGES_PER_STUDENT = 50

# Camera index (0 = default camera, 1+ for additional cameras)
CAMERA_INDEX = 0

# ===== ATTENDANCE SETTINGS =====
# Duration (in seconds) for automatic attendance capture
ATTENDANCE_DURATION = 20

# ===== UI COLOR SCHEME =====
COLOR_PRIMARY = "#0078D7"      # Blue - Primary buttons and headers
COLOR_SUCCESS = "#06A77D"      # Green - Success messages
COLOR_DANGER = "#E63946"       # Red - Error messages and close buttons
COLOR_WARNING = "#F77F00"      # Orange - Warning messages
COLOR_BG = "#FFFFFF"           # White - Background
COLOR_SECONDARY_BG = "#F8F8F8" # Light gray - Secondary background
COLOR_TEXT = "#000000"         # Black - Primary text
COLOR_TEXT_SECONDARY = "#666666"  # Gray - Secondary text
COLOR_DARK_BG = "#1E1E1E"      # Dark background for notifications

# ===== WINDOW SETTINGS =====
MAIN_WINDOW_TITLE = "CLASS VISION | Face Recognition Attendance System"
DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

# ===== VOICE SETTINGS =====
# Enable/disable text-to-speech announcements
ENABLE_TEXT_TO_SPEECH = True

# ===== LOGGING =====
# Enable/disable console logging for debugging
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# ===== ADVANCED SETTINGS =====
# Face recognition algorithm options:
# - LBPH (Local Binary Patterns Histograms) - Default, good for varying lighting
# - EigenFaces - Faster but less accurate
# - FisherFaces - Better accuracy but requires more training data
FACE_RECOGNITION_ALGORITHM = "LBPH"

# Auto-create required directories on startup
AUTO_CREATE_DIRECTORIES = True

# Save attendance backup
SAVE_ATTENDANCE_BACKUP = True
BACKUP_PATH = "./Attendance/Backups"