#!/usr/bin/env python3
"""
System Health Check for Face Recognition Attendance System
Run this script to verify everything is working correctly
"""

import sys
import os

def print_status(message, status):
    """Print colored status message"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def main():
    print("=" * 60)
    print("🔍 SYSTEM HEALTH CHECK")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Test 1: Module Imports
    print("📦 Testing Module Imports...")
    try:
        import config
        import attendance
        import automaticAttedance
        import takeImage
        import trainImage
        import show_attendance
        all_ok &= print_status("All modules imported successfully", True)
    except Exception as e:
        all_ok &= print_status(f"Module import failed: {e}", False)
    
    print()
    
    # Test 2: Config Loading
    print("⚙️  Testing Configuration...")
    try:
        import config
        all_ok &= print_status(f"Images per student: {config.IMAGES_PER_STUDENT}", True)
        all_ok &= print_status(f"Attendance duration: {config.ATTENDANCE_DURATION}s", True)
        all_ok &= print_status(f"Confidence threshold: {config.CONFIDENCE_THRESHOLD}", True)
    except Exception as e:
        all_ok &= print_status(f"Config error: {e}", False)
    
    print()
    
    # Test 3: Required Files
    print("📁 Checking Required Files...")
    required_files = [
        "haarcascade_frontalface_default.xml",
        "config.py",
        "attendance.py",
        "automaticAttedance.py",
        "takeImage.py",
        "trainImage.py",
        "show_attendance.py"
    ]
    
    for file in required_files:
        exists = os.path.exists(file)
        all_ok &= print_status(f"File exists: {file}", exists)
    
    print()
    
    # Test 4: Required Directories
    print("📂 Checking Required Directories...")
    required_dirs = [
        "StudentDetails",
        "TrainingImage",
        "TrainingImageLabel",
        "Attendance"
    ]
    
    for dir_name in required_dirs:
        exists = os.path.exists(dir_name) and os.path.isdir(dir_name)
        all_ok &= print_status(f"Directory exists: {dir_name}", exists)
    
    print()
    
    # Test 5: Trained Model
    print("🤖 Checking Trained Model...")
    model_path = "./TrainingImageLabel/Trainner.yml"
    model_exists = os.path.exists(model_path)
    if model_exists:
        model_size = os.path.getsize(model_path)
        all_ok &= print_status(f"Model exists: {model_path} ({model_size:,} bytes)", True)
    else:
        print_status(f"Model not found: {model_path} (train model first)", False)
    
    print()
    
    # Test 6: Student Database
    print("👥 Checking Student Database...")
    student_db = "./StudentDetails/studentdetails.csv"
    if os.path.exists(student_db):
        try:
            import pandas as pd
            df = pd.read_csv(student_db)
            num_students = len(df)
            all_ok &= print_status(f"Student database exists with {num_students} entries", True)
            
            # Check for duplicates
            duplicates = df[df.duplicated(subset=['Enrollment'], keep=False)]
            if len(duplicates) > 0:
                print_status(f"Warning: {len(duplicates)} duplicate enrollments found", False)
                all_ok = False
            else:
                print_status("No duplicate enrollments", True)
        except Exception as e:
            print_status(f"Error reading student database: {e}", False)
            all_ok = False
    else:
        print_status(f"Student database not found: {student_db}", False)
        all_ok = False
    
    print()
    
    # Test 7: Dependencies
    print("📚 Checking Python Dependencies...")
    dependencies = [
        'cv2',
        'numpy',
        'pandas',
        'PIL',
        'pyttsx3',
        'tkinter'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            all_ok &= print_status(f"Package installed: {dep}", True)
        except ImportError:
            all_ok &= print_status(f"Package missing: {dep}", False)
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("Your attendance system is ready to use.")
        print()
        print("Run: python attendance.py")
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("Please review the errors above and fix them.")
        print()
        print("See QUICK_REFERENCE.md for troubleshooting.")
    
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
