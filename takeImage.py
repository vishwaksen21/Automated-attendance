import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
import tkinter as tk
from tkinter import messagebox

# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter your Name.'
        text_to_speech(t)
    else:
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
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            os.mkdir(path)

            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 150), 2)
                    sampleNum += 1
                    progress_label.config(
                        text=f"Capturing Image {sampleNum}/50...",
                        fg="#0078D7"
                    )
                    cam_window.update_idletasks()

                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y:y+h, x:x+w],
                    )
                    cv2.imshow("Face Capture", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()

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

        except FileExistsError:
            F = "⚠️ Student Data already exists!"
            text_to_speech(F)
            err_screen.configure(
                text=F,
                bg="#1E1E1E",
                fg="#FF5555",
                font=("Consolas", 13, "bold"),
                width=35
            )
            err_screen.place(x=20, y=250)
