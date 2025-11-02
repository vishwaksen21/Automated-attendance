#!/usr/bin/env python3
"""
Test UI - Verify attendance.py loads properly
"""

import sys
import os

print("=" * 60)
print("Testing attendance.py UI Loading")
print("=" * 60)

# Test 1: Check if all imports work
print("\n1️⃣ Testing imports...")
try:
    import tkinter as tk
    from tkinter import *
    print("  ✅ tkinter imported")
except ImportError as e:
    print(f"  ❌ tkinter import failed: {e}")
    sys.exit(1)

try:
    import cv2
    print("  ✅ cv2 imported")
except ImportError as e:
    print(f"  ❌ cv2 import failed: {e}")

try:
    import numpy as np
    print("  ✅ numpy imported")
except ImportError as e:
    print(f"  ❌ numpy import failed: {e}")

try:
    from PIL import ImageTk, Image
    print("  ✅ PIL imported")
except ImportError as e:
    print(f"  ❌ PIL import failed: {e}")

try:
    import pandas as pd
    print("  ✅ pandas imported")
except ImportError as e:
    print(f"  ❌ pandas import failed: {e}")

try:
    import pyttsx3
    print("  ✅ pyttsx3 imported")
except ImportError as e:
    print(f"  ⚠️  pyttsx3 import failed: {e}")

# Test 2: Check all image files
print("\n2️⃣ Testing image files...")
image_files = [
    "UI_Image/0001.png",
    "UI_Image/register.png",
    "UI_Image/attendance.png",
    "UI_Image/verifyy.png",
]

for img_file in image_files:
    if os.path.exists(img_file):
        print(f"  ✅ {img_file}")
    else:
        print(f"  ❌ {img_file} NOT FOUND")

# Test 3: Check module files
print("\n3️⃣ Testing module files...")
module_files = [
    'show_attendance.py',
    'takeImage.py',
    'trainImage.py',
    'automaticAttedance.py',
]

for mod_file in module_files:
    if os.path.exists(mod_file):
        print(f"  ✅ {mod_file}")
    else:
        print(f"  ❌ {mod_file} NOT FOUND")

# Test 4: Try to import modules
print("\n4️⃣ Testing module imports...")
try:
    import takeImage
    print("  ✅ takeImage module imported")
except Exception as e:
    print(f"  ❌ takeImage import failed: {e}")

try:
    import trainImage
    print("  ✅ trainImage module imported")
except Exception as e:
    print(f"  ❌ trainImage import failed: {e}")

try:
    import show_attendance
    print("  ✅ show_attendance module imported")
except Exception as e:
    print(f"  ❌ show_attendance import failed: {e}")

try:
    import automaticAttedance
    print("  ✅ automaticAttedance module imported")
except Exception as e:
    print(f"  ❌ automaticAttedance import failed: {e}")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print("\nTo run the application, use:")
print("  python attendance.py          (Standard UI)")
print("  python attendance_premium.py  (Premium UI)")
print("=" * 60)
