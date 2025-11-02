"""
ATTENDANCE PREMIUM - Modern UI Version
Enhanced Face Recognition Attendance System with Premium Design
Features: Modern gradient backgrounds, improved buttons, consistent styling, animations
"""

import os
import shutil
import csv
import datetime
import time
import traceback

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np
import pandas as pd
import pyttsx3

# project modules (keep these as you had them)
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# ============================================================================
# COLOR SCHEME - PREMIUM DESIGN SYSTEM
# ============================================================================
COLORS = {
    'primary': '#2E86AB',        # Professional Blue
    'primary_light': '#A23B72',  # Purple Accent
    'secondary': '#F18F01',      # Vibrant Orange
    'success': '#06A77D',        # Fresh Green
    'warning': '#D62828',        # Alert Red
    'dark_bg': '#0F1419',        # Very Dark Blue-Black
    'card_bg': '#1A1F2E',        # Card Background
    'text_primary': '#FFFFFF',   # White Text
    'text_secondary': '#B8C5D6', # Light Gray Text
    'accent': '#FFD60A',         # Gold Accent
    'border': '#2A3550',         # Border Color
}

# Font definitions
FONT_TITLE = ("Segoe UI", 36, "bold")
FONT_SUBTITLE = ("Segoe UI", 24, "bold")
FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_LABEL = ("Segoe UI", 12, "bold")
FONT_BUTTON = ("Segoe UI", 14, "bold")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def text_to_speech(user_text: str):
    """Convert text to speech (best-effort)."""
    try:
        engine = pyttsx3.init()
        engine.say(user_text)
        engine.runAndWait()
    except Exception:
        # don't crash the app if TTS fails
        pass


def create_rounded_button(parent, text, command, width=15, height=2, bg_color=COLORS['primary'],
                          fg_color=COLORS['text_primary'], font_style=FONT_BUTTON):
    """Create a modern rounded-looking button (tkinter doesn't support real rounded corners)."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        font=font_style,
        bd=0,
        padx=20,
        pady=12,
        relief=tk.FLAT,
        cursor="hand2",
        activebackground=COLORS['primary_light'],
        activeforeground=COLORS['text_primary'],
    )
    return btn


def create_modern_entry(parent, width=25, font_size=14):
    """Create a modern entry field with consistent styling"""
    entry = tk.Entry(
        parent,
        width=width,
        bd=2,
        bg=COLORS['card_bg'],
        fg=COLORS['text_primary'],
        font=("Segoe UI", font_size),
        relief=tk.FLAT,
        insertbackground=COLORS['accent'],
    )
    return entry


def create_label(parent, text, font_style=FONT_BODY, color=COLORS['text_primary'], bg=None):
    """Create a modern label"""
    return tk.Label(
        parent,
        text=text,
        font=font_style,
        fg=color,
        bg=bg or COLORS['dark_bg'],
        relief=tk.FLAT,
    )


def testVal(inStr, acttyp):
    """
    Validate numeric input for enrollment field.
    inStr: proposed new value (%P)
    acttyp: action type (%d) - "1" for insert, "0" for delete, "-1" for others
    Returns True if valid.
    """
    # allow empty string (so deletion works)
    if inStr == "":
        return True
    # only digits allowed on insert
    if acttyp == "1":
        return inStr.isdigit()
    return True


def show_info(title, message):
    messagebox.showinfo(title, message)


def show_error(title, message):
    messagebox.showerror(title, message)


def err_screen():
    show_error("Warning!!", "Enrollment & Name required!!!")


# ============================================================================
# PATH CONFIGURATIONS
# ============================================================================
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"
if not os.path.exists(attendance_path):
    os.makedirs(attendance_path)

# ============================================================================
# MAIN WINDOW SETUP
# ============================================================================
window = tk.Tk()
window.title("CLASS VISION - Premium Attendance System")
window.geometry("1400x800")
window.configure(background=COLORS['dark_bg'])
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", window.quit)

# ============================================================================
# HEADER SECTION
# ============================================================================
header_frame = tk.Frame(window, bg=COLORS['primary'], height=80)
header_frame.pack(fill=tk.X)
header_frame.pack_propagate(False)

# Load and resize logo
try:
    logo = Image.open("UI_Image/0001.png")
    resample = getattr(Image, "LANCZOS", Image.ANTIALIAS)
    logo = logo.resize((50, 50), resample)
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(header_frame, image=logo_img, bg=COLORS['primary'])
    logo_label.image = logo_img
    logo_label.pack(side=tk.LEFT, padx=20, pady=15)
except Exception:
    # silently ignore missing logo
    pass

title_label = tk.Label(
    header_frame,
    text="CLASS VISION",
    font=("Segoe UI", 32, "bold"),
    fg=COLORS['text_primary'],
    bg=COLORS['primary'],
)
title_label.pack(side=tk.LEFT, padx=20)

subtitle_label = tk.Label(
    header_frame,
    text="Premium Face Recognition Attendance System",
    font=("Segoe UI", 12),
    fg=COLORS['accent'],
    bg=COLORS['primary'],
)
subtitle_label.pack(side=tk.LEFT, padx=20)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
main_frame = tk.Frame(window, bg=COLORS['dark_bg'])
main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

# Welcome section
welcome_label = tk.Label(
    main_frame,
    text="Welcome to CLASS VISION",
    font=("Segoe UI", 28, "bold"),
    fg=COLORS['accent'],
    bg=COLORS['dark_bg'],
)
welcome_label.pack(pady=(0, 10))

subtitle = tk.Label(
    main_frame,
    text="Efficient attendance management through facial recognition",
    font=("Segoe UI", 12),
    fg=COLORS['text_secondary'],
    bg=COLORS['dark_bg'],
)
subtitle.pack(pady=(0, 40))

# ============================================================================
# BUTTON GRID LAYOUT
# ============================================================================
button_frame = tk.Frame(main_frame, bg=COLORS['dark_bg'])
button_frame.pack(fill=tk.BOTH, expand=True)

# Create card frames for better organization
def create_card_button(parent, icon_path, title, description, command):
    """Create a card-style button with icon and description"""
    card_frame = tk.Frame(parent, bg=COLORS['card_bg'], relief=tk.FLAT, bd=1,
                         highlightthickness=2, highlightbackground=COLORS['border'],
                         highlightcolor=COLORS['primary'])
    card_frame.pack(side=tk.LEFT, padx=15, pady=20, expand=True, fill=tk.BOTH)

    # Try to load icon
    try:
        img = Image.open(icon_path)
        resample = getattr(Image, "LANCZOS", Image.ANTIALIAS)
        img = img.resize((60, 60), resample)
        photo = ImageTk.PhotoImage(img)
        icon_label = tk.Label(card_frame, image=photo, bg=COLORS['card_bg'])
        icon_label.image = photo
        icon_label.pack(pady=(20, 10))
    except Exception:
        # If icon not present, show simple text placeholder
        placeholder = tk.Label(card_frame, text="🖼", font=("Segoe UI", 28), bg=COLORS['card_bg'],
                               fg=COLORS['text_secondary'])
        placeholder.pack(pady=(24, 10))

    # Title
    title_label = tk.Label(
        card_frame,
        text=title,
        font=("Segoe UI", 16, "bold"),
        fg=COLORS['text_primary'],
        bg=COLORS['card_bg'],
    )
    title_label.pack(pady=10)

    # Description
    desc_label = tk.Label(
        card_frame,
        text=description,
        font=("Segoe UI", 10),
        fg=COLORS['text_secondary'],
        bg=COLORS['card_bg'],
        wraplength=150,
        justify=tk.CENTER,
    )
    desc_label.pack(pady=(0, 10))

    # Button
    btn = create_rounded_button(
        card_frame,
        "ACCESS",
        command,
        width=12,
        height=1,
        bg_color=COLORS['primary'],
    )
    btn.pack(pady=(10, 20))


# ============================================================================
# TAKE IMAGE UI
# ============================================================================
def TakeImageUI():
    """Premium UI for taking student images"""
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Register New Student")
    ImageUI.geometry("900x650")
    ImageUI.configure(background=COLORS['dark_bg'])
    ImageUI.resizable(False, False)

    # Header
    header_frame = tk.Frame(ImageUI, bg=COLORS['primary'], height=70)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    title = tk.Label(
        header_frame,
        text="📸 Register Your Face",
        font=("Segoe UI", 24, "bold"),
        fg=COLORS['text_primary'],
        bg=COLORS['primary'],
    )
    title.pack(pady=15)

    # Content area
    content_frame = tk.Frame(ImageUI, bg=COLORS['dark_bg'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # Instruction label
    instruction_label = tk.Label(
        content_frame,
        text="Enter the following details to register:",
        font=("Segoe UI", 14, "bold"),
        fg=COLORS['accent'],
        bg=COLORS['dark_bg'],
    )
    instruction_label.pack(pady=(0, 20))

    # Enrollment number section
    enroll_frame = tk.Frame(content_frame, bg=COLORS['dark_bg'])
    enroll_frame.pack(fill=tk.X, pady=15)

    enroll_label = tk.Label(
        enroll_frame,
        text="📋 Enrollment Number",
        font=FONT_LABEL,
        fg=COLORS['text_primary'],
        bg=COLORS['dark_bg'],
        width=20,
        anchor=tk.W,
    )
    enroll_label.pack(side=tk.LEFT)

    txt1 = create_modern_entry(enroll_frame, width=30)
    txt1.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

    # register validation on the root window
    reg = window.register(testVal)
    txt1.config(validate="key", validatecommand=(reg, "%P", "%d"))

    # Name section
    name_frame = tk.Frame(content_frame, bg=COLORS['dark_bg'])
    name_frame.pack(fill=tk.X, pady=15)

    name_label = tk.Label(
        name_frame,
        text="👤 Student Name",
        font=FONT_LABEL,
        fg=COLORS['text_primary'],
        bg=COLORS['dark_bg'],
        width=20,
        anchor=tk.W,
    )
    name_label.pack(side=tk.LEFT)

    txt2 = create_modern_entry(name_frame, width=30)
    txt2.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

    # Notification area
    notification_label = tk.Label(
        content_frame,
        text="📢 Status & Notifications",
        font=FONT_LABEL,
        fg=COLORS['text_primary'],
        bg=COLORS['dark_bg'],
    )
    notification_label.pack(pady=(20, 10), anchor=tk.W)

    message = tk.Label(
        content_frame,
        text="Ready to capture images...",
        font=("Segoe UI", 11),
        fg=COLORS['success'],
        bg=COLORS['card_bg'],
        relief=tk.FLAT,
        anchor=tk.W,
        justify=tk.LEFT,
        padx=15,
        pady=15,
        wraplength=400,
    )
    message.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Button section
    button_section = tk.Frame(content_frame, bg=COLORS['dark_bg'])
    button_section.pack(fill=tk.X, pady=20)

    def take_image():
        l1 = txt1.get().strip()
        l2 = txt2.get().strip()
        if not l1 or not l2:
            message.config(text="❌ Please enter both enrollment and name!", fg=COLORS['warning'])
            return
        message.config(text="📸 Capturing images...", fg=COLORS['accent'])
        ImageUI.update()
        # call your takeImage module - keep the API you used earlier
        try:
            takeImage.TakeImage(
                l1,
                l2,
                haarcasecade_path,
                trainimage_path,
                message,
                lambda: message.config(text="❌ Error: Enrollment & Name required!", fg=COLORS['warning']),
                text_to_speech,
            )
            message.config(text="✅ Capture complete.", fg=COLORS['success'])
        except Exception as e:
            traceback.print_exc()
            message.config(text=f"❌ Error capturing: {e}", fg=COLORS['warning'])
            show_error("Capture Error", str(e))
        finally:
            txt1.delete(0, "end")
            txt2.delete(0, "end")

    def train_image():
        message.config(text="🔄 Training model... This may take a moment...", fg=COLORS['accent'])
        ImageUI.update()
        try:
            trainImage.TrainImage(
                haarcasecade_path,
                trainimage_path,
                trainimagelabel_path,
                message,
                text_to_speech,
            )
            message.config(text="✅ Training complete.", fg=COLORS['success'])
        except Exception as e:
            traceback.print_exc()
            message.config(text=f"❌ Training failed: {e}", fg=COLORS['warning'])
            show_error("Training Error", str(e))

    take_btn = create_rounded_button(
        button_section,
        "📸 Capture Images",
        take_image,
        width=15,
        height=2,
        bg_color=COLORS['primary'],
    )
    take_btn.pack(side=tk.LEFT, padx=10)

    train_btn = create_rounded_button(
        button_section,
        "🤖 Train Model",
        train_image,
        width=15,
        height=2,
        bg_color=COLORS['success'],
    )
    train_btn.pack(side=tk.LEFT, padx=10)

    close_btn = create_rounded_button(
        button_section,
        "❌ Close",
        ImageUI.destroy,
        width=15,
        height=2,
        bg_color=COLORS['warning'],
    )
    close_btn.pack(side=tk.LEFT, padx=10)


# ============================================================================
# ATTENDANCE UI
# ============================================================================
def automatic_attendance():
    """Launch automatic attendance capture"""
    try:
        automaticAttedance.subjectChoose(text_to_speech)
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"Failed to start attendance: {e}")


# ============================================================================
# VIEW ATTENDANCE UI
# ============================================================================
def view_attendance():
    """View attendance records"""
    try:
        show_attendance.subjectchoose(text_to_speech)
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"Failed to view attendance: {e}")


# ============================================================================
# CREATE MAIN BUTTONS
# ============================================================================
create_card_button(
    button_frame,
    "UI_Image/register.png",
    "Register Student",
    "Capture and train new student faces",
    TakeImageUI,
)

create_card_button(
    button_frame,
    "UI_Image/attendance.png",
    "Take Attendance",
    "Mark attendance using face recognition",
    automatic_attendance,
)

create_card_button(
    button_frame,
    "UI_Image/verifyy.png",
    "View Records",
    "Check attendance history and reports",
    view_attendance,
)

# ============================================================================
# FOOTER SECTION
# ============================================================================
footer_frame = tk.Frame(window, bg=COLORS['primary'], height=60)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
footer_frame.pack_propagate(False)

footer_label = tk.Label(
    footer_frame,
    text="© 2024 CLASS VISION - Face Recognition Attendance System | Premium Edition",
    font=("Segoe UI", 10),
    fg=COLORS['text_secondary'],
    bg=COLORS['primary'],
)
footer_label.pack(pady=15)

# Exit button in footer
exit_btn = tk.Button(
    footer_frame,
    text="EXIT",
    command=window.quit,
    bg=COLORS['warning'],
    fg=COLORS['text_primary'],
    font=FONT_BUTTON,
    bd=0,
    padx=20,
    pady=8,
    relief=tk.FLAT,
    cursor="hand2",
)
exit_btn.pack(side=tk.RIGHT, padx=20)

# ============================================================================
# MAIN LOOP
# ============================================================================
if __name__ == "__main__":
    window.mainloop()
