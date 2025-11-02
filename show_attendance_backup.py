import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    # ===== COLOR SCHEME (UPDATED - WHITE & BLACK THEME) =====
    COLOR_PRIMARY = "#0078D7"
    COLOR_HEADER_BG = "white"
    COLOR_TEXT = "#000000"
    COLOR_TEXT_SECONDARY = "#666666"
    COLOR_LABEL = "#999999"
    COLOR_ACCENT = "#FFD60A"
    COLOR_INPUT_BG = "white"
    COLOR_TABLE_BG = "white"
    COLOR_TABLE_HEADER = "#F8F8F8"
    COLOR_TABLE_BORDER = "#E0E0E0"

    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        filenames = glob(f"./Attendance/{Subject}/{Subject}*.csv")
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        newdf.to_csv(f"./Attendance/{Subject}/attendance.csv", index=False)

        root = tkinter.Toplevel()
        root.title("Attendance of " + Subject)
        root.configure(background=COLOR_TABLE_BG)

        cs = f"./Attendance/{Subject}/attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    # Header row styling
                    if r == 0:
                        bg_color = COLOR_TABLE_HEADER
                        fg_color = COLOR_TEXT
                        font_style = ("Segoe UI", 12, "bold")
                    else:
                        bg_color = "white" if r % 2 == 0 else "#FAFAFA"
                        fg_color = COLOR_TEXT
                        font_style = ("Segoe UI", 11)
                    
                    label = tkinter.Label(
                        root,
                        width=12,
                        height=1,
                        fg=fg_color,
                        font=font_style,
                        bg=bg_color,
                        text=row,
                        relief=tkinter.FLAT,
                        padx=10,
                        pady=8,
                        borderwidth=1
                    )
                    label.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("📘 View Attendance")
    subject.geometry("700x450")
    subject.resizable(True, True)
    subject.configure(background="white")

    # ===== HEADER =====
    header = tk.Frame(subject, bg=COLOR_PRIMARY, height=100)
    header.pack(fill=X)
    header.pack_propagate(False)

    # Header title
    title_lbl = tk.Label(
        header,
        text="� View Attendance Records",
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI Semibold", 24, "bold")
    )
    title_lbl.pack(pady=(20, 10))
    
    # Header subtitle
    subtitle_lbl = tk.Label(
        header,
        text="Enter subject name to view attendance details",
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI", 12)
    )
    subtitle_lbl.pack(pady=(0, 15))

    # ===== INPUT SECTION =====
    input_frame = tk.Frame(subject, bg="white")
    input_frame.pack(fill=BOTH, expand=True, padx=40, pady=30)

    # Label with improved styling
    sub_label = tk.Label(
        input_frame,
        text="Subject Name:",
        bg="white",
        fg=COLOR_PRIMARY,
        font=("Segoe UI", 14, "bold")
    )
    sub_label.pack(anchor=W, pady=(0, 10))

    # Input entry with better styling
    tx = tk.Entry(
        input_frame,
        width=30,
        bd=2,
        bg="white",
        fg=COLOR_TEXT,
        relief=FLAT,
        font=("Segoe UI", 13),
        insertbackground=COLOR_PRIMARY,
        justify="left"
    )
    tx.pack(pady=(0, 25), ipady=10, fill=X)

    # ===== BUTTONS FRAME =====
    button_frame = tk.Frame(input_frame, bg="white")
    button_frame.pack(fill=X, pady=20)

    def on_enter(e, btn): 
        btn.config(bg="#0066B3")
    
    def on_leave(e, btn): 
        btn.config(bg=COLOR_PRIMARY)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                os.startfile(f"Attendance\\{sub}")
            except:
                pass

    # Button styling with consistent appearance
    style = {
        "bd": 0, 
        "relief": FLAT, 
        "cursor": "hand2", 
        "font": ("Segoe UI", 13, "bold"),
        "fg": "white", 
        "height": 2, 
        "activeforeground": "white"
    }

    fill_a = tk.Button(
        button_frame,
        text="📊 View Attendance",
        command=calculate_attendance,
        bg=COLOR_PRIMARY,
        activebackground="#0066B3",
        **style
    )
    fill_a.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

    attf = tk.Button(
        button_frame,
        text="📁 Open Sheets",
        command=Attf,
        bg="#06A77D",
        activebackground="#058060",
        **style
    )
    attf.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

    exit_btn = tk.Button(
        button_frame,
        text="❌ Close",
        command=subject.destroy,
        bg="#E63946",
        activebackground="#C0262D",
        **style
    )
    exit_btn.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

    # Hover Effects
    for btn, color in [(fill_a, "#0066B3"), (attf, "#058060"), (exit_btn, "#C0262D")]:
        btn.bind("<Enter>", lambda e, b=btn, c=color: on_enter(e, b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    # ===== FOOTER =====
    footer = tk.Frame(subject, bg="#F8F8F8", height=50)
    footer.pack(fill=X, side=BOTTOM)
    footer.pack_propagate(False)
    
    tk.Label(
        footer,
        text="© CLASS VISION | Face Recognition Attendance System",
        bg="#F8F8F8",
        fg="#555555",
        font=("Segoe UI", 11)
    ).pack(side=LEFT, padx=15, pady=12)

    subject.mainloop()
