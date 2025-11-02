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

# ===== COLOR SCHEMES =====
COLOR_REGISTER = "#0078D7"      # Blue
COLOR_ATTENDANCE = "#0078D7"    # Green
COLOR_VIEW = "#0078D7"          # Orange
COLOR_BG = "#F5F6FA"            # Light background
COLOR_DARK_BG = "#E8EEF5"       # Darker background for contrast

# ===== MAIN WINDOW =====
root = Tk()
root.title("CLASS VISION | Face Recognition Attendance System")
root.configure(bg="white")

# Start in fullscreen mode by default
root.state("zoomed")
root.resizable(True, True)

# Toggle fullscreen with F11
def toggle_fullscreen(event=None):
    if root.state() == "zoomed":
        root.state("normal")
        root.geometry("1100x700")
    else:
        root.state("zoomed")

root.bind("<F11>", toggle_fullscreen)

# ===== HELPER FUNCTIONS =====
def err_screen():
    dialog = Toplevel(root)
    dialog.geometry("400x150")
    dialog.title("⚠️ Warning")
    dialog.configure(bg="white")
    dialog.resizable(0, 0)
    
    Label(dialog, text="⚠️ Enrollment & Name Required!",
          bg="white", fg="#E63946",
          font=("Segoe UI", 14, "bold")).pack(pady=10)
    Label(dialog, text="Please fill in both fields to continue.",
          bg="white", fg="#000000",
          font=("Segoe UI", 11)).pack(pady=5)
    
    Button(dialog, text="OK", command=lambda: dialog.destroy(),
           bg="#0078D7", fg="white", font=("Segoe UI", 11, "bold"),
           relief=FLAT, cursor="hand2", padx=20).pack(pady=15)

def testVal(inStr, acttyp):
    if acttyp == "1" and not inStr.isdigit():
        return False
    return True

# ===== TOP NAVIGATION BAR =====
top_frame = Frame(root, bg="#0078D7", height=100)
top_frame.pack(fill=X, side=TOP)
top_frame.pack_propagate(False)

try:
    logo = Image.open("UI_Image/classvision_logo.png")
    logo = logo.resize((50, 50))
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(top_frame, image=logo, bg="#0078D7")
    logo_label.image = logo
    logo_label.place(x=30, y=25)
except:
    pass

title = Label(
    top_frame,
    text="CLASS VISION",
    bg="#0078D7",
    fg="white",
    font=("Arial Rounded MT Bold", 36, "bold"),
)
title.place(x=100, y=15)

tagline = Label(
    top_frame,
    text="Face Recognition Attendance System",
    bg="#0078D7",
    fg="white",
    font=("Helvetica", 11, "italic"),
)
tagline.place(x=100, y=60)

# ===== WELCOME SECTION =====
welcome_frame = Frame(root, bg="white")
welcome_frame.pack(fill=X, padx=40, pady=(25, 10))

welcome_label = Label(
    welcome_frame,
    text="Welcome to CLASS VISION",
    bg="white",
    fg="#0078D7",
    font=("Segoe UI Semibold", 24, "bold"),
)
welcome_label.pack(anchor=W)

subtitle_label = Label(
    welcome_frame,
    text="Automated Face Recognition Attendance System",
    bg="white",
    fg="#666666",
    font=("Segoe UI", 13),
)
subtitle_label.pack(anchor=W, pady=(5, 0))

instruction_label = Label(
    welcome_frame,
    text="Choose an option below to get started",
    bg="white",
    fg="#999999",
    font=("Segoe UI", 11, "italic"),
)
instruction_label.pack(anchor=W, pady=(8, 0))

# ===== MAIN CARD SECTION =====
card_container = Frame(root, bg="white")
card_container.pack(pady=(20, 40), fill=BOTH, expand=True)

def adjust_color_brightness(hex_color, brightness_offset):
    """Adjust brightness of hex color"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    new_rgb = tuple(max(0, min(255, c + brightness_offset)) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(new_rgb[0], new_rgb[1], new_rgb[2])

def create_modern_card(parent, emoji, text, button_text, command, color):
    """Create a modern card with shadow, color bar, and better styling"""
    # Outer frame with consistent sizing
    outer = Frame(parent, bg="white")
    outer.pack(side=LEFT, padx=20, pady=0, fill=BOTH, expand=True)
    
    # Shadow effect (dark frame behind)
    shadow = Frame(outer, bg="#CCCCCC", height=280, width=260)
    shadow.place(x=4, y=4)
    shadow.pack_propagate(False)
    
    # Main card frame
    card = Frame(outer, bg="white", height=280, width=260, relief=FLAT, bd=0)
    card.pack(fill=BOTH, expand=True)
    card.pack_propagate(False)
    
    # Top colored bar
    top_bar = Frame(card, bg=color, height=8)
    top_bar.pack(fill=X)
    
    # Content frame with better spacing
    content = Frame(card, bg="white")
    content.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Large emoji (increased size and spacing)
    icon_label = Label(content, text=emoji, font=("Segoe UI Emoji", 64), bg="white")
    icon_label.pack(pady=(15, 10))
    
    # Card title with improved font size for accessibility
    label = Label(content, text=text, font=("Segoe UI Semibold", 16, "bold"), 
                  bg="white", fg="#000000", wraplength=200, justify=CENTER)
    label.pack(pady=(8, 20))
    
    # Colored button (filled, larger and more prominent)
    btn = Button(
        content,
        text=button_text,
        bg=color,
        fg="white",
        font=("Segoe UI", 13, "bold"),
        activebackground=color,
        activeforeground="white",
        relief=FLAT,
        cursor="hand2",
        bd=0,
        padx=25,
        pady=12,
        command=command,
    )
    btn.pack(pady=(10, 0))
    
    # Hover effects
    def on_enter(e):
        card.config(bg="white")
        content.config(bg="white")
        label.config(bg="white")
        icon_label.config(bg="white")
        darker_color = adjust_color_brightness(color, -20)
        btn.config(bg=darker_color, activebackground=darker_color)
        outer.config(bg="white")
    
    def on_leave(e):
        card.config(bg="white")
        content.config(bg="white")
        label.config(bg="white")
        icon_label.config(bg="white")
        btn.config(bg=color, activebackground=color)
        outer.config(bg="white")
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    content.bind("<Enter>", on_enter)
    content.bind("<Leave>", on_leave)
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    icon_label.bind("<Enter>", on_enter)
    icon_label.bind("<Leave>", on_leave)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return outer

def open_register():
    """Register student window"""
    register_window = Toplevel(root)
    register_window.title("Register Student")
    register_window.geometry("700x550")
    register_window.configure(bg="white")
    register_window.resizable(False, False)

    # Header with gradient-like effect
    header = Frame(register_window, bg=COLOR_REGISTER, height=70)
    header.pack(fill=X)
    header.pack_propagate(False)
    
    Label(header, text="� Register Your Face",
          bg=COLOR_REGISTER, fg="white",
          font=("Segoe UI", 24, "bold")).pack(pady=15)

    # Content
    content = Frame(register_window, bg="white")
    content.pack(fill=BOTH, expand=True, padx=35, pady=25)

    # Enrollment Number
    Label(content, text="Enrollment Number",
          bg="white", fg="#000000",
          font=("Segoe UI", 13, "bold")).pack(anchor=W, pady=(10, 8))

    txt1 = Entry(content, width=35, bd=1, validate="key",
                 bg="white", fg="#000000", relief=FLAT,
                 font=("Segoe UI", 12), insertbackground=COLOR_REGISTER)
    txt1.pack(fill=X, pady=(0, 20))
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Student Name
    Label(content, text="Student Name",
          bg="white", fg="#000000",
          font=("Segoe UI", 13, "bold")).pack(anchor=W, pady=(10, 8))

    txt2 = Entry(content, width=35, bd=1,
                 bg="white", fg="#000000", relief=FLAT,
                 font=("Segoe UI", 12), insertbackground=COLOR_REGISTER)
    txt2.pack(fill=X, pady=(0, 20))

    # Status
    Label(content, text="Status",
          bg="white", fg="#000000",
          font=("Segoe UI", 13, "bold")).pack(anchor=W, pady=(10, 8))

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

    buttons_frame = Frame(content, bg="white")
    buttons_frame.pack(fill=X, pady=15)

    Button(buttons_frame, text="📷 Capture Images (50)",
           command=take_image, bd=0,
           font=("Segoe UI", 12, "bold"),
           bg=COLOR_REGISTER, fg="white",
           height=2, relief=FLAT, cursor="hand2",
           activebackground=adjust_color_brightness(COLOR_REGISTER, -20)).pack(side=LEFT, padx=8, fill=BOTH, expand=True)

    Button(buttons_frame, text="🤖 Train Model",
           command=train_image, bd=0,
           font=("Segoe UI", 12, "bold"),
           bg=COLOR_ATTENDANCE, fg="white",
           height=2, relief=FLAT, cursor="hand2",
           activebackground=adjust_color_brightness(COLOR_ATTENDANCE, -20)).pack(side=LEFT, padx=8, fill=BOTH, expand=True)

# Create three main cards with different colors
create_modern_card(card_container, "🧍", "Register\nStudent", "OPEN", open_register, COLOR_REGISTER)
create_modern_card(card_container, "📸", "Take\nAttendance", "OPEN", 
                   lambda: automaticAttedance.subjectChoose(text_to_speech), COLOR_ATTENDANCE)
create_modern_card(card_container, "📋", "View\nAttendance", "OPEN", 
                   lambda: show_attendance.subjectchoose(text_to_speech), COLOR_VIEW)

# ===== FOOTER =====
footer_frame = Frame(root, bg="#F8F8F8", height=60)
footer_frame.pack(side=BOTTOM, fill=X)
footer_frame.pack_propagate(False)

footer = Label(
    footer_frame,
    text="© CLASS VISION | Automated Face Recognition Attendance System",
    bg="#F8F8F8",
    fg="#555555",
    font=("Segoe UI", 11),
)
footer.pack(pady=15)

root.mainloop()