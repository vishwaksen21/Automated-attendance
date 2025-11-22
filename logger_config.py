"""
Logging Configuration for Face Recognition Attendance System
Provides centralized logging functionality across all modules
"""

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = "./Logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Log file path
LOG_FILE = os.path.join(LOGS_DIR, "attendance_system.log")

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Create logger
def get_logger(name):
    """
    Get a configured logger instance
    
    Args:
        name (str): Name of the module requesting the logger
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler - logs everything to file
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        
        # Console handler - logs INFO and above to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Convenience functions for common log operations
def log_student_registration(enrollment_id, name, num_images):
    """Log student registration event"""
    logger = get_logger('Registration')
    logger.info(f"Student registered - ID: {enrollment_id}, Name: {name}, Images: {num_images}")

def log_attendance_marked(enrollment_id, name, subject, confidence):
    """Log attendance marking event"""
    logger = get_logger('Attendance')
    logger.info(f"Attendance marked - ID: {enrollment_id}, Name: {name}, Subject: {subject}, Confidence: {confidence:.2f}")

def log_model_trained(num_students, num_images):
    """Log model training event"""
    logger = get_logger('Training')
    logger.info(f"Model trained successfully - Students: {num_students}, Total images: {num_images}")

def log_error(module, error_message, exception=None):
    """Log error event"""
    logger = get_logger(module)
    if exception:
        logger.error(f"{error_message} - Exception: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)

def log_system_event(event_type, message):
    """Log general system event"""
    logger = get_logger('System')
    logger.info(f"[{event_type}] {message}")

# Initialize logging on module import
startup_logger = get_logger('System')
startup_logger.info("=" * 70)
startup_logger.info("Face Recognition Attendance System Started")
startup_logger.info("=" * 70)
