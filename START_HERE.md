# 🚀 Quick Start Guide - Updated

## ✅ Pre-Launch Checklist (Completed)
- [x] TrainingImageLabel directory created
- [x] Duplicate student entries removed
- [x] Error handling improved
- [x] Configuration file added

---

## 📋 Step-by-Step Usage

### 1️⃣ First Time Setup

```bash
# Navigate to project directory
cd ~/Desktop/Automated-attendance/Automated-attendance

# Run the application
python attendance.py
```

**Expected**: Application window opens (ignore terminal warnings)

---

### 2️⃣ Train the Existing Model

You already have **53 training images** for student "vishwak" (ID: 17)

**Steps**:
1. Click **"REGISTER STUDENT"** button on main screen
2. In the registration window, click **"🤖 Train Model"** button
3. Wait 10-30 seconds for training to complete
4. You'll see: "✅ Image Trained Successfully!"
5. Close the registration window

**This creates**: `TrainingImageLabel/Trainner.yml` file

---

### 3️⃣ Mark Attendance

**Steps**:
1. Click **"TAKE ATTENDANCE"** button on main screen
2. Enter subject name (e.g., "Math", "Science")
3. Click **"📸 Mark Attendance"**
4. Camera will open for 20 seconds
5. Face the camera - your face will be detected
6. After 20 seconds, attendance is saved automatically

**Output**: CSV file saved in `Attendance/[SubjectName]/`

---

### 4️⃣ View Attendance

**Steps**:
1. Click **"VIEW ATTENDANCE"** button on main screen
2. Enter the subject name (same as used in step 3)
3. Click **"📊 View Attendance"**
4. Attendance table will appear with percentages

---

## 🔧 Customization

Edit `config.py` to adjust:

```python
# Recognition strictness (lower = stricter)
CONFIDENCE_THRESHOLD = 70  # Try 60 for stricter matching

# Images per student during registration
IMAGES_PER_STUDENT = 50

# Attendance capture duration
ATTENDANCE_DURATION = 20  # seconds

# Color scheme
COLOR_PRIMARY = "#0078D7"  # Change to your preferred color
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Model not found" Error
**Cause**: Haven't trained the model yet  
**Fix**: Follow Step 2 above to train model

### Issue 2: Camera Not Working
**Causes**:
- Camera permissions not granted
- Another app using camera
- Wrong camera index

**Fix**:
```bash
# For macOS - Grant camera permissions:
System Preferences → Security & Privacy → Camera → Enable for Terminal

# In config.py, try different camera:
CAMERA_INDEX = 0  # Try 1 if default doesn't work
```

### Issue 3: Face Not Recognized
**Causes**:
- Poor lighting
- Face too far from camera
- Model not trained with your face

**Fix**:
1. Ensure good lighting
2. Move closer to camera
3. Retrain model if needed
4. Lower CONFIDENCE_THRESHOLD in config.py

### Issue 4: "No attendance data to save"
**Cause**: No faces were recognized during capture  
**Fix**: 
- Make sure you've trained the model
- Ensure good lighting
- Face the camera directly

---

## 📊 File Structure After Setup

```
Automated-attendance/
├── TrainingImageLabel/
│   └── Trainner.yml          ✅ Model file (created after training)
├── TrainingImage/
│   └── 17_vishwak/           ✅ 53 images already exist
│       ├── vishwak_17_1.jpg
│       └── ...
├── StudentDetails/
│   └── studentdetails.csv    ✅ Cleaned (no duplicates)
├── Attendance/
│   └── [SubjectName]/        ✅ Created when you mark attendance
│       └── attendance_[date].csv
└── config.py                 ✅ New configuration file
```

---

## 🎯 Your Next Steps

1. **Train the model** (Step 2 above) - Takes 30 seconds
2. **Test attendance** with yourself
3. **Customize settings** in config.py if needed
4. **Register more students** as needed

---

## 💡 Pro Tips

1. **Better Recognition**: Capture images with various angles and lighting
2. **Faster Registration**: Set `IMAGES_PER_STUDENT = 30` in config.py
3. **Stricter Matching**: Set `CONFIDENCE_THRESHOLD = 60` in config.py
4. **Longer Capture**: Set `ATTENDANCE_DURATION = 30` in config.py
5. **Keyboard Shortcut**: Press `F11` to toggle fullscreen mode

---

## 📞 Need Help?

Check these files:
- `IMPROVEMENTS_APPLIED.md` - Recent changes and fixes
- `config.py` - All customizable settings
- Error messages in the GUI - They now provide clear instructions!

---

**Ready to start?** Run `python attendance.py` and train your model! 🎉
