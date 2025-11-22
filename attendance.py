import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance
import config
import logger_config

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = config.HAARCASCADE_PATH
trainimagelabel_path = config.TRAINING_IMAGE_LABEL_PATH
trainimage_path = config.TRAINING_IMAGE_PATH
studentdetail_path = config.STUDENT_DETAIL_PATH
attendance_path = config.ATTENDANCE_PATH

# Create required directories if they don't exist
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)
if not os.path.exists("./TrainingImageLabel"):
    os.makedirs("./TrainingImageLabel")
if not os.path.exists("./StudentDetails"):
    os.makedirs("./StudentDetails")
if not os.path.exists(attendance_path):
    os.makedirs(attendance_path)

# ===== MAIN WINDOW =====
root = Tk()
root.title("CLASS VISION | Face Recognition Attendance System")
root.geometry("1000x650")
root.resizable(False, False)
root.configure(bg="#F5F6FA")

# ===== HELPER FUNCTIONS =====
def err_screen():
    dialog = Toplevel(root)
    dialog.geometry("400x150")
    dialog.title("⚠️ Warning")
    dialog.configure(bg="#F5F6FA")
    dialog.resizable(0, 0)
    
    Label(dialog, text="⚠️ Enrollment & Name Required!",
          bg="#F5F6FA", fg="#E63946",
          font=("Segoe UI", 14, "bold")).pack(pady=10)
    Label(dialog, text="Please fill in both fields to continue.",
          bg="#F5F6FA", fg="#2C3E50",
          font=("Segoe UI", 11)).pack(pady=5)
    
    Button(dialog, text="OK", command=lambda: dialog.destroy(),
           bg="#0078D7", fg="white", font=("Segoe UI", 11, "bold"),
           relief=FLAT, cursor="hand2", padx=20).pack(pady=15)

def testVal(inStr, acttyp):
    if acttyp == "1" and not inStr.isdigit():
        return False
    return True

# ===== TOP NAVIGATION BAR =====
top_frame = Frame(root, bg="#0078D7", height=70)
top_frame.pack(fill=X, side=TOP)
top_frame.pack_propagate(False)

try:
    logo = Image.open("UI_Image/classvision_logo.png")
    logo = logo.resize((50, 50))
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(top_frame, image=logo, bg="#0078D7")
    logo_label.image = logo
    logo_label.place(x=30, y=10)
except:
    pass

title = Label(
    top_frame,
    text="CLASS VISION",
    bg="#0078D7",
    fg="white",
    font=("Arial Rounded MT Bold", 28),
)
title.place(x=100, y=10)

tagline = Label(
    top_frame,
    text="Face Recognition Attendance System",
    bg="#0078D7",
    fg="white",
    font=("Helvetica", 12, "italic"),
)
tagline.place(x=360, y=25)

# ===== WELCOME SECTION =====
welcome_label = Label(
    root,
    text="Welcome to CLASS VISION - Automated Attendance System",
    bg="#F5F6FA",
    fg="#000000",
    font=("Segoe UI Semibold", 18),
)
welcome_label.pack(pady=50)

# ===== MAIN CARD SECTION =====
card_frame = Frame(root, bg="#F5F6FA")
card_frame.pack(pady=20)

def create_card(parent, emoji, text, command=None):
    """Create a card with hover effects"""
    card = Frame(parent, bg="white", width=220, height=220, 
                 highlightbackground="#DADADA", highlightthickness=1)
    card.pack(side=LEFT, padx=40)
    card.pack_propagate(False)
    
    icon_label = Label(card, text=emoji, font=("Segoe UI Emoji", 48), bg="white")
    icon_label.pack(pady=(25, 10))

    label = Label(card, text=text, font=("Segoe UI Semibold", 14), 
                  bg="white", fg="#000000")
    label.pack(pady=(0, 10))

    btn = Button(
        card,
        text="Open",
        bg="#0078D7",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        activebackground="#005A9E",
        activeforeground="white",
        relief=FLAT,
        cursor="hand2",
        width=12,
        command=command,
    )
    btn.pack(pady=10)

    # Hover effect
    def on_enter(e):
        card.config(bg="#F0F8FF")
        label.config(bg="#F0F8FF")
        icon_label.config(bg="#F0F8FF")
    
    def on_leave(e):
        card.config(bg="white")
        label.config(bg="white")
        icon_label.config(bg="white")
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    icon_label.bind("<Enter>", on_enter)
    icon_label.bind("<Leave>", on_leave)

    return card

def open_register():
    """Register student window"""
    register_window = Toplevel(root)
    register_window.title("Register Student")
    register_window.geometry("700x550")
    register_window.configure(bg="#F5F6FA")
    register_window.resizable(False, False)

    # Header
    header = Frame(register_window, bg="#06A77D", height=60)
    header.pack(fill=X)
    header.pack_propagate(False)
    
    Label(header, text="📸 Register Your Face",
          bg="#06A77D", fg="white",
          font=("Segoe UI", 22, "bold")).pack(pady=10)

    # Content
    content = Frame(register_window, bg="#F5F6FA")
    content.pack(fill=BOTH, expand=True, padx=30, pady=20)

    Label(content, text="Enrollment Number",
          bg="#F5F6FA", fg="#000000",
          font=("Segoe UI", 12, "bold")).pack(anchor=W, pady=(10, 5))

    txt1 = Entry(content, width=35, bd=1, validate="key",
                 bg="white", fg="#000000", relief=FLAT,
                 font=("Segoe UI", 12), insertbackground="#0078D7")
    txt1.pack(fill=X, pady=(0, 15))
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    Label(content, text="Student Name",
          bg="#F5F6FA", fg="#000000",
          font=("Segoe UI", 12, "bold")).pack(anchor=W, pady=(10, 5))

    txt2 = Entry(content, width=35, bd=1,
                 bg="white", fg="#000000", relief=FLAT,
                 font=("Segoe UI", 12), insertbackground="#0078D7")
    txt2.pack(fill=X, pady=(0, 15))

    Label(content, text="Status",
          bg="#F5F6FA", fg="#000000",
          font=("Segoe UI", 12, "bold")).pack(anchor=W, pady=(10, 5))

    message = Label(content, text="", width=40, height=3,
                    bd=0, bg="white", fg="#000000",
                    relief=FLAT, font=("Segoe UI", 10),
                    wraplength=400, justify=LEFT)
    message.pack(fill=X, pady=(0, 20))

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(l1, l2, haarcasecade_path,
                            trainimage_path, message, err_screen, text_to_speech)
        # Only clear if window and widgets still exist
        try:
            if register_window.winfo_exists():
                txt1.delete(0, "end")
                txt2.delete(0, "end")
        except:
            pass

    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path,
                              trainimagelabel_path, message, text_to_speech)

    buttons_frame = Frame(content, bg="#F5F6FA")
    buttons_frame.pack(fill=X, pady=15)

    Button(buttons_frame, text="📷 Capture Images",
           command=take_image, bd=0,
           font=("Segoe UI", 11, "bold"),
           bg="#0078D7", fg="white",
           height=2, relief=FLAT, cursor="hand2",
           activebackground="#005A9E").pack(side=LEFT, padx=8, fill=BOTH, expand=True)

    Button(buttons_frame, text="🤖 Train Model",
           command=train_image, bd=0,
           font=("Segoe UI", 11, "bold"),
           bg="#06A77D", fg="white",
           height=2, relief=FLAT, cursor="hand2",
           activebackground="#048a5e").pack(side=LEFT, padx=8, fill=BOTH, expand=True)

# Create three main cards
create_card(card_frame, "🧍‍♂️", "Register Student", open_register)
create_card(card_frame, "📸", "Take Attendance", 
            lambda: automaticAttedance.subjectChoose(text_to_speech))
create_card(card_frame, "📋", "View Attendance", 
            lambda: show_attendance.subjectchoose(text_to_speech))

# ===== FOOTER =====
footer = Label(
    root,
    text="© CLASS VISION | Automated Face Recognition Attendance System",
    bg="#EAF3FA",
    fg="#000000",
    font=("Segoe UI", 10),
    pady=10,
)
footer.pack(side=BOTTOM, fill=X)

# Log system startup
logger = logger_config.get_logger('Main')
logger.info("Application GUI initialized successfully")
logger.info(f"Configuration loaded - Students directory: {trainimage_path}")

root.mainloop()

# Log system shutdown
logger.info("Application closed by user")
logger.info("=" * 70)
