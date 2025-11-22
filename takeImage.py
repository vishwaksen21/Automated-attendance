import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
import tkinter as tk
from tkinter import messagebox
import config
import logger_config

# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    logger = logger_config.get_logger('TakeImage')
    
    if (l1 == "") and (l2==""):
        t='Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
        logger.warning("Registration attempted with empty enrollment and name")
    elif l1=='':
        t='Please Enter your Enrollment Number.'
        text_to_speech(t)
        logger.warning("Registration attempted with empty enrollment number")
    elif l2 == "":
        t='Please Enter your Name.'
        text_to_speech(t)
        logger.warning("Registration attempted with empty name")
    else:
        # Check for duplicate enrollment ID
        studentdetail_path = config.STUDENT_DETAIL_PATH
        if os.path.exists(studentdetail_path):
            try:
                df = pd.read_csv(studentdetail_path)
                if l1 in df['Enrollment'].astype(str).values:
                    t = f'Enrollment {l1} already exists! Please use a different enrollment number.'
                    text_to_speech(t)
                    messagebox.showerror("Duplicate Entry", t)
                    logger.warning(f"Duplicate registration attempt - Enrollment ID: {l1} already exists")
                    return
            except Exception as e:
                logger.error(f"Error checking for duplicates: {str(e)}")
        
        logger.info(f"Starting registration - Enrollment: {l1}, Name: {l2}")
        
        try:
            # Create a stylish window for camera feedback
            cam_window = tk.Toplevel()
            cam_window.title("📸 Capturing Images")
            cam_window.geometry("600x350")
            cam_window.configure(bg="white")
            cam_window.resizable(False, False)

            # Header
            header = tk.Frame(cam_window, bg="#0078D7", height=80)
            header.pack(fill="x")
            header.pack_propagate(False)

            title = tk.Label(
                header,
                text="📸 Face Capture in Progress",
                bg="#0078D7",
                fg="white",
                font=("Segoe UI", 20, "bold"),
                pady=15
            )
            title.pack(fill="x")

            # Content frame
            content = tk.Frame(cam_window, bg="white")
            content.pack(fill="both", expand=True, padx=30, pady=30)

            info_label = tk.Label(
                content,
                text="Your face is being captured.",
                bg="white",
                fg="#0078D7",
                font=("Segoe UI", 14, "bold")
            )
            info_label.pack(pady=(0, 10))

            progress_label = tk.Label(
                content,
                text="Initializing camera...",
                bg="white",
                fg="#666666",
                font=("Segoe UI", 12)
            )
            progress_label.pack(pady=20)

            # Progress bar
            progress_frame = tk.Frame(content, bg="#E0E0E0", height=8)
            progress_frame.pack(fill="x", pady=20)
            progress_frame.pack_propagate(False)
            
            progress_bar = tk.Frame(progress_frame, bg="#0078D7", height=8)
            progress_bar.pack(side="left", fill="x", expand=False)

            status_label = tk.Label(
                content,
                text="Please ensure good lighting and face the camera.",
                bg="white",
                fg="#999999",
                font=("Segoe UI", 11, "italic")
            )
            status_label.pack(pady=(20, 0))

            cam_window.update()

            # Original logic starts here (unchanged)
            cam = cv2.VideoCapture(0)
            
            # Check if camera opened successfully
            if not cam.isOpened():
                cam_window.destroy()
                err_msg = "❌ Camera not accessible!\n\nPlease check:\n• Camera permissions\n• Camera is not used by another app\n• Camera is properly connected"
                message.configure(text=err_msg, fg="#FF5555")
                text_to_speech("Camera not accessible. Please check camera permissions.")
                return
            
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            rejected_count = 0  # Track rejected images
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            
            # Check if directory already exists
            if os.path.exists(path):
                import shutil
                shutil.rmtree(path)  # Remove old images
                logger.info(f"Removed existing images for Enrollment: {Enrollment}")
            os.mkdir(path)

            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                # Quality Check 1: Single face detection
                if len(faces) > 1:
                    cv2.putText(img, "Multiple faces detected! Only one person allowed.", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Face Capture", img)
                    continue
                
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # Quality Check 2: Minimum face size
                    if w < 100 or h < 100:
                        cv2.putText(img, "Face too small! Move closer to camera.", 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 2)
                        cv2.imshow("Face Capture", img)
                        rejected_count += 1
                        continue
                    
                    # Quality Check 3: Brightness check
                    brightness = np.mean(face_roi)
                    if brightness < 50 or brightness > 200:
                        status_text = "Too dark! Improve lighting." if brightness < 50 else "Too bright! Reduce lighting."
                        cv2.putText(img, status_text, 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 2)
                        cv2.imshow("Face Capture", img)
                        rejected_count += 1
                        continue
                    
                    # Quality Check 4: Blur detection (Laplacian variance)
                    laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
                    if laplacian_var < 100:
                        cv2.putText(img, "Image blurry! Hold steady.", 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 2)
                        cv2.imshow("Face Capture", img)
                        rejected_count += 1
                        continue
                    
                    # All quality checks passed - save image
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 150), 2)
                    cv2.putText(img, f"Quality: Good (Brightness: {int(brightness)}, Sharpness: {int(laplacian_var)})", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    sampleNum += 1
                    progress_label.config(
                        text=f"Capturing Image {sampleNum}/{config.IMAGES_PER_STUDENT}... (Quality: ✓)",
                        fg="#06A77D"
                    )
                    cam_window.update_idletasks()

                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        face_roi,
                    )
                    cv2.imshow("Face Capture", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    logger.info(f"Image capture cancelled by user - Enrollment: {Enrollment}")
                    break
                elif sampleNum >= config.IMAGES_PER_STUDENT:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Log registration statistics
            logger.info(f"Image capture completed - Enrollment: {Enrollment}, Name: {Name}")
            logger.info(f"Images captured: {sampleNum}/{config.IMAGES_PER_STUDENT}, Rejected: {rejected_count}")
            
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()

            logger_config.log_student_registration(Enrollment, Name, sampleNum)
            
            res = f"✅ Images Saved for ER No: {Enrollment} | Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)

            progress_label.config(
                text="✅ Capture Completed Successfully!",
                fg="#00FF88",
                font=("Consolas", 14, "bold")
            )

            done_label = tk.Label(
                cam_window,
                text="All 50 images have been saved successfully.",
                bg="#0D1117",
                fg="#B0B0B0",
                font=("Consolas", 13)
            )
            done_label.pack(pady=15)

            def close_cam():
                cam_window.destroy()

            ok_btn = tk.Button(
                cam_window,
                text="Close",
                command=close_cam,
                bg="#161B22",
                fg="#00FF88",
                activebackground="#00FF88",
                activeforeground="black",
                font=("Consolas", 13, "bold"),
                bd=0,
                width=12,
                height=1
            )
            ok_btn.pack(pady=10)

            ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg="#00FF88", fg="black"))
            ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg="#161B22", fg="#00FF88"))

            cam_window.mainloop()

        except FileExistsError as fe:
            F = "⚠️ Student Data already exists!"
            text_to_speech(F)
            logger.error(f"File exists error during registration - Enrollment: {l1}, Error: {str(fe)}")
            err_screen.configure(
                text=F,
                bg="#1E1E1E",
                fg="#FF5555",
                font=("Consolas", 13, "bold"),
                width=35
            )
        except Exception as e:
            F = f"❌ Error: {str(e)}"
            text_to_speech("An error occurred during registration")
            logger_config.log_error('TakeImage', f"Registration failed for Enrollment: {l1}", e)
            err_screen.configure(
                text=F,
                bg="#1E1E1E",
                fg="#FF5555",
                font=("Consolas", 13, "bold"),
                width=35
            )
            err_screen.place(x=20, y=250)
