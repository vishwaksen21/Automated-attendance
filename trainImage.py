import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image


# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    # Create a stylish pop-up window for training progress
    progress_window = Toplevel()
    progress_window.title("🤖 Training Model")
    progress_window.geometry("550x320")
    progress_window.config(bg="white")
    progress_window.resizable(False, False)

    # Header
    header = Frame(progress_window, bg="#0078D7", height=70)
    header.pack(fill=X)
    header.pack_propagate(False)

    heading = Label(
        header,
        text="🔧 Training Facial Recognition Model",
        fg="white",
        bg="#0078D7",
        font=("Segoe UI", 18, "bold"),
        pady=15
    )
    heading.pack()

    # Content frame
    content = Frame(progress_window, bg="white")
    content.pack(fill=BOTH, expand=True, padx=40, pady=30)

    info_label = Label(
        content,
        text="Processing face data and training the recognition model.",
        bg="white",
        fg="#0078D7",
        font=("Segoe UI", 12, "bold")
    )
    info_label.pack(pady=(0, 20))

    # Progress bar
    style = ttk.Style()
    style.configure("TProgressbar", thickness=15, troughcolor="#E0E0E0", background="#0078D7", bordercolor="white")
    progress = ttk.Progressbar(content, orient=HORIZONTAL, length=450, mode='indeterminate', style="TProgressbar")
    progress.pack(pady=20)
    progress.start(10)

    status_label = Label(
        content,
        text="Training in progress... Please wait.",
        bg="white",
        fg="#666666",
        font=("Segoe UI", 11, "italic"),
    )
    status_label.pack(pady=15)

    progress_window.update()

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        faces, Id = getImagesAndLables(trainimage_path)

        recognizer.train(faces, np.array(Id))
        recognizer.save(trainimagelabel_path)

        progress.stop()
        progress_window.destroy()

        res = "✅ Image Trained Successfully!"
        message.configure(text=res, fg="#06A77D")
        text_to_speech(res)

        # Success popup
        success = Toplevel()
        success.title("✅ Training Complete")
        success.geometry("480x240")
        success.config(bg="white")
        success.resizable(False, False)

        # Header
        header = Frame(success, bg="#06A77D", height=60)
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(header, text="🎉 Training Completed!", bg="#06A77D", fg="white",
              font=("Segoe UI", 18, "bold"), pady=10).pack()
        
        # Content
        content = Frame(success, bg="white")
        content.pack(fill=BOTH, expand=True, padx=30, pady=30)

        Label(content, text="Your facial recognition model has been trained successfully.",
              bg="white", fg="#666666", font=("Segoe UI", 12), wraplength=400, justify="center").pack(pady=15)

        ttk.Button(content, text="✓ OK", command=success.destroy).pack(pady=15)

    except Exception as e:
        progress.stop()
        progress_window.destroy()
        message.configure(text=f"⚠️ Error during training: {e}", fg="red")
        text_to_speech("Error during training")



def getImagesAndLables(path):
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    faces = []
    Ids = []
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
