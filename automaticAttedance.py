import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
import config
import logger_config

haarcasecade_path = config.HAARCASCADE_PATH
trainimagelabel_path = config.TRAINING_IMAGE_LABEL_PATH
trainimage_path = config.TRAINING_IMAGE_PATH
studentdetail_path = config.STUDENT_DETAIL_PATH
attendance_path = config.ATTENDANCE_PATH

def subjectChoose(text_to_speech):
    logger = logger_config.get_logger('Attendance')
    
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + config.ATTENDANCE_DURATION
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            logger.warning("Attendance attempted without subject name")
        else:
            logger.info(f"Starting attendance for subject: {sub}")
            
            # Check if model file exists before proceeding
            if not os.path.exists(trainimagelabel_path):
                e = "❌ Model not found! Please train the model first.\n\nSteps:\n1. Click 'Register Student'\n2. Click 'Train Model'"
                Notifica.configure(
                    text=e, bg="#1E1E1E", fg="#FF5555", width=50, font=("Segoe UI", 12, "bold")
                )
                Notifica.place(x=60, y=240)
                text_to_speech("Model not found, please train model first")
                logger.error(f"Attendance failed - Model not found at: {trainimagelabel_path}")
                return
            
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except Exception as read_error:
                    e = f"❌ Error loading model: {str(read_error)}\nPlease re-train the model."
                    Notifica.configure(
                        text=e, bg="#1E1E1E", fg="#FF5555", width=50, font=("Segoe UI", 11, "bold")
                    )
                    Notifica.place(x=60, y=240)
                    text_to_speech("Error loading model, please retrain")
                    return
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                
                # Check if camera opened successfully
                if not cam.isOpened():
                    e = "❌ Camera not accessible!\n\nPlease check camera permissions and ensure\nno other app is using the camera."
                    Notifica.configure(
                        text=e, bg="#1E1E1E", fg="#FF5555", width=50, font=("Segoe UI", 11, "bold")
                    )
                    Notifica.place(x=60, y=240)
                    text_to_speech("Camera not accessible")
                    return
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    if im is None:
                        continue
                    
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    
                    for (x, y, w, h) in faces:
                        try:
                            global Id
                            # Ensure we have a valid face region
                            face_region = gray[y:y+h, x:x+w]
                            if face_region.size == 0:
                                continue
                            
                            Id, conf = recognizer.predict(face_region)
                            
                            # LBPH returns distance (lower = better match)
                            # Only accept if confidence is BELOW threshold (good match)
                            if conf < config.CONFIDENCE_THRESHOLD:
                                global Subject, aa, date, timeStamp
                                Subject = tx.get()
                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                                
                                # Verify ID exists in database
                                aa = df.loc[df["Enrollment"] == Id]["Name"].values
                                if len(aa) > 0:
                                    aa_str = aa[0]
                                    tt = str(Id) + "-" + aa_str
                                    
                                    # Check if already marked (to avoid logging duplicates)
                                    if Id not in attendance['Enrollment'].values:
                                        attendance.loc[len(attendance)] = [Id, aa_str]
                                        logger_config.log_attendance_marked(Id, aa_str, Subject, conf)
                                    
                                    # Draw green box for recognized student
                                    cv2.rectangle(im, (x, y), (x+w, y+h), (0, 260, 0), 4)
                                    cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0), 4)
                                else:
                                    # ID predicted but not in database - treat as Unknown
                                    Id = "Unknown"
                                    cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                                    cv2.putText(im, "Unknown", (x + h, y), font, 1, (0, 25, 255), 4)
                            else:
                                # Confidence too high (poor match) - Unknown face
                                Id = "Unknown"
                                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                                cv2.putText(im, f"Unknown (conf:{int(conf)})", (x + h, y), font, 0.8, (0, 25, 255), 3)
                        except Exception as pred_error:
                            # Handle prediction errors gracefully
                            logger.warning(f"Prediction error: {str(pred_error)}")
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                            cv2.putText(im, "Error", (x + h, y), font, 1, (0, 25, 255), 4)
                            
                    if time.time() > future:
                        break
                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break
                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                if len(attendance) == 0:
                    raise Exception("No attendance data to save! No faces were recognized.")
                full_path = os.path.join(path, fileName)
                attendance.to_csv(full_path, index=False)
                
                # Backup attendance data
                backup_dir = os.path.join(attendance_path, "Backups")
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                backup_path = os.path.join(backup_dir, fileName)
                attendance.to_csv(backup_path, index=False)
                
                # Log attendance completion
                num_students = len(attendance)
                logger.info(f"Attendance completed - Subject: {Subject}, Students: {num_students}, File: {fileName}")
                for _, row in attendance.iterrows():
                    logger.info(f"  Marked present - ID: {row['Enrollment']}, Name: {row['Name']}")
                
                m = "Attendance Filled Successfully for " + Subject
                Notifica.configure(
                    text=m, bg="#1E1E1E", fg="#00FF88",
                    width=40, relief=FLAT, font=("Consolas", 15, "bold")
                )
                text_to_speech(m)
                Notifica.place(x=90, y=260)
                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("✅ Attendance Marked - " + Subject)
                root.configure(background="white")
                
                with open(full_path, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # Header styling
                            if r == 0:
                                bg_color = "#F8F8F8"
                                fg_color = "#000000"
                                font_style = ("Segoe UI", 12, "bold")
                            else:
                                bg_color = "white" if r % 2 == 0 else "#FAFAFA"
                                fg_color = "#000000"
                                font_style = ("Segoe UI", 11)
                            
                            label = tkinter.Label(
                                root, width=14, height=1, fg=fg_color,
                                font=font_style,
                                bg=bg_color, text=row, relief=tkinter.FLAT,
                                padx=10, pady=8
                            )
                            label.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                            c += 1
                        r += 1
                root.mainloop()
            except Exception as e:
                logger_config.log_error('Attendance', f"Attendance marking failed for subject: {tx.get()}", e)
                f = "Error: No Face found or file error."
                Notifica.configure(
                    text=f, bg="#1E1E1E", fg="#FF5555",
                    width=40, font=("Consolas", 15, "bold")
                )
                Notifica.place(x=90, y=260)
                text_to_speech(f)
                try:
                    cv2.destroyAllWindows()
                    cam.release()
                except:
                    pass

    subject = Tk()
    subject.title("📸 Mark Attendance")
    subject.geometry("700x500")
    subject.resizable(True, True)
    subject.configure(bg="white")

    # ===== HEADER =====
    header = Frame(subject, bg="#0078D7", height=90)
    header.pack(fill=X, side=TOP)
    header.pack_propagate(False)

    title = tk.Label(
        header, text="📸 Fill Attendance by Face Recognition", bg="#0078D7",
        fg="white", font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=(10, 5))

    subtitle = tk.Label(
        header, text="Enter subject name and click Mark Attendance", bg="#0078D7",
        fg="white", font=("Segoe UI", 11)
    )
    subtitle.pack(pady=(0, 10))

    # ===== INPUT SECTION =====
    input_frame = tk.Frame(subject, bg="white")
    input_frame.pack(fill=X, padx=30, pady=25, side=TOP)

    sub_label = tk.Label(
        input_frame, text="Subject Name:", bg="white",
        fg="#0078D7", font=("Segoe UI", 13, "bold")
    )
    sub_label.pack(anchor=W, pady=(0, 8))

    tx = tk.Entry(
        input_frame, width=35, bd=1, bg="white",
        fg="#000000", insertbackground="#0078D7",
        relief=FLAT, font=("Segoe UI", 12), justify="left"
    )
    tx.pack(pady=(0, 20), ipady=8, fill=X)

    # ===== NOTIFICATION AREA =====
    Notifica = tk.Label(
        input_frame, text="", bg="white", fg="#0078D7",
        font=("Segoe UI", 11, "bold"), wraplength=400, justify="center"
    )
    Notifica.pack(pady=(0, 20), fill=X)

    # ===== BUTTONS =====
    button_frame = tk.Frame(input_frame, bg="white")
    button_frame.pack(fill=X, pady=(10, 0))

    fill_a = tk.Button(
        button_frame, text="📸 Mark Attendance", command=FillAttendance,
        bd=0, bg="#0078D7", fg="white",
        activebackground="#0066B3", activeforeground="white",
        font=("Segoe UI", 12, "bold"), padx=15, pady=10, relief=FLAT, cursor="hand2"
    )
    fill_a.pack(side=LEFT, padx=8, pady=10, fill=BOTH, expand=True)

    exit_btn = tk.Button(
        button_frame, text="❌ Close", command=subject.destroy,
        bd=0, bg="#E63946", fg="white",
        activebackground="#C0262D", activeforeground="white",
        font=("Segoe UI", 12, "bold"), padx=15, pady=10, relief=FLAT, cursor="hand2"
    )
    exit_btn.pack(side=LEFT, padx=8, pady=10, fill=BOTH, expand=True)

    # ===== FOOTER =====
    footer = tk.Frame(subject, bg="#F8F8F8", height=45)
    footer.pack(fill=X, side=BOTTOM)
    footer.pack_propagate(False)
    
    tk.Label(
        footer,
        text="© CLASS VISION | Face Recognition Attendance System",
        bg="#F8F8F8",
        fg="#555555",
        font=("Segoe UI", 10)
    ).pack(side=LEFT, padx=15, pady=10)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            import subprocess, platform
            path = f"./Attendance/{sub}"
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])

    subject.wait_window()
