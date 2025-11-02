import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image, ImageFilter
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

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# ===== MODERN COLOR PALETTE =====
COLOR_PRIMARY = "#0078D7"
COLOR_SECONDARY = "#913175"
COLOR_SUCCESS = "#06A77D"
COLOR_WARNING = "#E63946"
COLOR_ACCENT = "#FFD60A"
COLOR_DARK = "#101820"
COLOR_CARD = "#1A1F2E"
COLOR_TEXT = "#FFFFFF"
COLOR_TEXT_DIM = "#B0B0B0"
COLOR_INPUT = "#2A3540"
COLOR_BG_GRADIENT_TOP = "#1F2B3D"
COLOR_BG_GRADIENT_BOTTOM = "#0E141B"

# ===== WINDOW =====
window = Tk()
window.title("📊 Face Recognition Attendance System")
window.geometry("1280x720")
window.configure(background=COLOR_DARK)
window.resizable(False, False)

# ===== Helper Functions =====
def del_sc1():
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("420x160")
    sc1.title("⚠️ Warning")
    sc1.configure(background=COLOR_CARD)
    sc1.resizable(0, 0)

    Label(sc1, text="⚠️ Enrollment & Name Required!", fg=COLOR_WARNING,
          bg=COLOR_CARD, font=("Segoe UI", 14, "bold")).pack(pady=10)
    Label(sc1, text="Please fill in both fields to continue.",
          fg=COLOR_TEXT_DIM, bg=COLOR_CARD, font=("Segoe UI", 11)).pack(pady=5)

    Button(sc1, text="OK", command=del_sc1, fg=COLOR_TEXT, bg=COLOR_PRIMARY,
           width=15, height=1, activebackground=COLOR_SECONDARY,
           activeforeground=COLOR_TEXT, font=("Segoe UI", 12, "bold"),
           bd=0, relief=FLAT, cursor="hand2").pack(pady=15)

def testVal(inStr, acttyp):
    if acttyp == "1" and not inStr.isdigit():
        return False
    return True

# ===== HEADER =====
header_frame = tk.Frame(window, bg=COLOR_PRIMARY, height=90)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

try:
    logo = Image.open("UI_Image/0001.png").resize((55, 50), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    l1 = tk.Label(header_frame, image=logo1, bg=COLOR_PRIMARY)
    l1.image = logo1
    l1.pack(side=LEFT, padx=25, pady=15)
except:
    pass

tk.Label(header_frame, text="📊 CLASS VISION",
         bg=COLOR_PRIMARY, fg=COLOR_TEXT,
         font=("Segoe UI Semibold", 32, "bold")).pack(side=LEFT, padx=15, pady=10)

tk.Label(header_frame, text="Face Recognition Attendance System",
         bg=COLOR_PRIMARY, fg=COLOR_ACCENT,
         font=("Segoe UI", 11, "italic")).pack(side=LEFT, padx=20, pady=0)

# ===== CONTENT =====
content_frame = tk.Frame(window, bg=COLOR_DARK)
content_frame.pack(fill=BOTH, expand=True, padx=30, pady=25)

welcome_label = tk.Label(content_frame,
                         text="Welcome to CLASS VISION - Automated Attendance System",
                         bg=COLOR_DARK, fg=COLOR_TEXT,
                         font=("Segoe UI", 20, "bold"))
welcome_label.pack(pady=30)

# ===== BUTTONS =====
button_frame = tk.Frame(content_frame, bg=COLOR_DARK)
button_frame.pack(fill=BOTH, expand=True, pady=20)

def create_action_button(parent, text, emoji, command, color):
    def on_enter(e): btn.config(bg=color, fg=COLOR_ACCENT)
    def on_leave(e): btn.config(bg=color, fg=COLOR_TEXT)

    btn = tk.Button(
        parent,
        text=f"{emoji}\n{text}",
        command=command,
        bd=0,
        font=("Segoe UI", 13, "bold"),
        bg=color,
        fg=COLOR_TEXT,
        relief=FLAT,
        cursor="hand2",
        activebackground=COLOR_SECONDARY,
        activeforeground=COLOR_TEXT,
        height=4,
        width=22,
        wraplength=150
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

row1_frame = tk.Frame(button_frame, bg=COLOR_DARK)
row1_frame.pack(fill=BOTH, expand=True, pady=10)

register_btn = create_action_button(
    row1_frame, "Register\nStudent", "👤", lambda: TakeImageUI(), COLOR_PRIMARY)
register_btn.pack(side=LEFT, padx=20, fill=BOTH, expand=True)

attendance_btn = create_action_button(
    row1_frame, "Take\nAttendance", "📸", lambda: automaticAttedance.subjectChoose(text_to_speech), COLOR_SUCCESS)
attendance_btn.pack(side=LEFT, padx=20, fill=BOTH, expand=True)

view_btn = create_action_button(
    row1_frame, "View\nAttendance", "📋", lambda: show_attendance.subjectchoose(text_to_speech), COLOR_ACCENT)
view_btn.pack(side=LEFT, padx=20, fill=BOTH, expand=True)

# ===== FOOTER =====
footer_frame = tk.Frame(window, bg=COLOR_CARD, height=60)
footer_frame.pack(fill=X, side=BOTTOM)
footer_frame.pack_propagate(False)

footer_info = tk.Label(footer_frame,
                       text="📊 CLASS VISION | Automated Face Recognition Attendance System",
                       bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Segoe UI", 10))
footer_info.pack(side=LEFT, padx=25, pady=15)

exit_btn = tk.Button(footer_frame, text="❌ EXIT",
                     command=lambda: window.quit(),
                     bd=0, font=("Segoe UI", 10, "bold"),
                     bg=COLOR_WARNING, fg=COLOR_TEXT,
                     relief=FLAT, cursor="hand2",
                     activebackground=COLOR_DARK,
                     activeforeground=COLOR_WARNING,
                     padx=15, pady=8)
exit_btn.pack(side=RIGHT, padx=20, pady=10)

# ===== SUBWINDOW (Register UI) =====
def TakeImageUI():
    ImageUI = Toplevel(window)
    ImageUI.title("📸 Register Student Face")
    ImageUI.geometry("700x550")
    ImageUI.configure(background=COLOR_DARK)
    ImageUI.resizable(False, False)

    header = tk.Frame(ImageUI, bg=COLOR_SUCCESS, height=60)
    header.pack(fill=X)
    header.pack_propagate(False)

    tk.Label(header, text="📸 Register Your Face",
             bg=COLOR_SUCCESS, fg=COLOR_TEXT,
             font=("Segoe UI", 22, "bold")).pack(pady=10)

    content = tk.Frame(ImageUI, bg=COLOR_DARK)
    content.pack(fill=BOTH, expand=True, padx=30, pady=20)

    lbl1 = tk.Label(content, text="Enrollment Number",
                    bg=COLOR_DARK, fg=COLOR_ACCENT,
                    font=("Segoe UI", 12, "bold"))
    lbl1.pack(anchor=W, pady=(10, 5))

    txt1 = tk.Entry(content, width=35, bd=1, validate="key",
                    bg=COLOR_INPUT, fg=COLOR_TEXT, relief=FLAT,
                    font=("Segoe UI", 12), insertbackground=COLOR_ACCENT)
    txt1.pack(fill=X, pady=(0, 15))
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    lbl2 = tk.Label(content, text="Student Name",
                    bg=COLOR_DARK, fg=COLOR_ACCENT,
                    font=("Segoe UI", 12, "bold"))
    lbl2.pack(anchor=W, pady=(10, 5))

    txt2 = tk.Entry(content, width=35, bd=1,
                    bg=COLOR_INPUT, fg=COLOR_TEXT, relief=FLAT,
                    font=("Segoe UI", 12), insertbackground=COLOR_ACCENT)
    txt2.pack(fill=X, pady=(0, 15))

    lbl3 = tk.Label(content, text="Status", bg=COLOR_DARK,
                    fg=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
    lbl3.pack(anchor=W, pady=(10, 5))

    message = tk.Label(content, text="", width=40, height=3,
                       bd=0, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                       relief=FLAT, font=("Segoe UI", 10),
                       wraplength=400, justify=LEFT)
    message.pack(fill=X, pady=(0, 20))

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(l1, l2, haarcasecade_path,
                            trainimage_path, message, err_screen, text_to_speech)
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path,
                              trainimagelabel_path, message, text_to_speech)

    buttons_frame = tk.Frame(content, bg=COLOR_DARK)
    buttons_frame.pack(fill=X, pady=15)

    takeImg = tk.Button(buttons_frame, text="📷 Capture Images",
                        command=take_image, bd=0,
                        font=("Segoe UI", 11, "bold"),
                        bg=COLOR_PRIMARY, fg=COLOR_TEXT,
                        height=2, relief=FLAT, cursor="hand2",
                        activebackground=COLOR_SECONDARY,
                        activeforeground=COLOR_TEXT)
    takeImg.pack(side=LEFT, padx=8, fill=BOTH, expand=True)

    trainImg = tk.Button(buttons_frame, text="🤖 Train Model",
                         command=train_image, bd=0,
                         font=("Segoe UI", 11, "bold"),
                         bg=COLOR_SUCCESS, fg=COLOR_TEXT,
                         height=2, relief=FLAT, cursor="hand2",
                         activebackground=COLOR_PRIMARY,
                         activeforeground=COLOR_TEXT)
    trainImg.pack(side=LEFT, padx=8, fill=BOTH, expand=True)

window.mainloop()
