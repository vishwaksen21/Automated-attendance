import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import subprocess
import platform

def subjectchoose(text_to_speech):
    # ===== COLOR SCHEME =====
    COLOR_PRIMARY = "#0078D7"
    COLOR_TEXT = "#000000"
    COLOR_TEXT_SECONDARY = "#666666"

    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        filenames = glob(f"./Attendance/{Subject}/{Subject}*.csv")
        if not filenames:
            t = f'No attendance records found for {Subject}.'
            text_to_speech(t)
            return
        
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0].copy()
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = ""
        for i in range(len(newdf)):
            newdf.loc[i, "Attendance"] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        newdf.to_csv(f"./Attendance/{Subject}/attendance.csv", index=False)

        root = tkinter.Toplevel()
        root.title("Attendance of " + Subject)
        root.configure(background="white")

        cs = f"./Attendance/{Subject}/attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    # Header row styling
                    if r == 0:
                        bg_color = "#F8F8F8"
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
                        pady=8
                    )
                    label.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("📊 View Attendance")
    subject.geometry("700x500")
    subject.resizable(True, True)
    subject.configure(background="white")

    # ===== HEADER =====
    header = tk.Frame(subject, bg=COLOR_PRIMARY, height=90)
    header.pack(fill=X, side=TOP)
    header.pack_propagate(False)

    # Header title
    title_lbl = tk.Label(
        header,
        text="📊 View Attendance Records",
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI Semibold", 20, "bold")
    )
    title_lbl.pack(pady=(10, 5))
    
    # Header subtitle
    subtitle_lbl = tk.Label(
        header,
        text="Enter subject name to view attendance details",
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI", 11)
    )
    subtitle_lbl.pack(pady=(0, 10))

    # ===== INPUT SECTION =====
    input_frame = tk.Frame(subject, bg="white")
    input_frame.pack(fill=X, padx=30, pady=25, side=TOP)

    # Label with improved styling
    sub_label = tk.Label(
        input_frame,
        text="Subject Name:",
        bg="white",
        fg=COLOR_PRIMARY,
        font=("Segoe UI", 13, "bold")
    )
    sub_label.pack(anchor=W, pady=(0, 8))

    # Input entry
    tx = tk.Entry(
        input_frame,
        width=35,
        bd=1,
        bg="white",
        fg=COLOR_TEXT,
        relief=FLAT,
        font=("Segoe UI", 12),
        insertbackground=COLOR_PRIMARY,
        justify="left"
    )
    tx.pack(pady=(0, 20), ipady=8, fill=X)

    # ===== BUTTONS FRAME =====
    button_frame = tk.Frame(input_frame, bg="white")
    button_frame.pack(fill=X, pady=(15, 0))

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            folder_path = f"Attendance/{sub}"
            # Check if folder exists
            if not os.path.exists(folder_path):
                t = f"Attendance folder for {sub} not found!"
                text_to_speech(t)
                return
            
            try:
                system = platform.system()
                if system == "Windows":
                    os.startfile(folder_path)
                elif system == "Darwin":  # macOS
                    subprocess.Popen(["open", folder_path])
                else:  # Linux and others
                    subprocess.Popen(["xdg-open", folder_path])
            except Exception as e:
                t = f"Could not open folder: {str(e)}"
                text_to_speech(t)

    # View button
    fill_a = tk.Button(
        button_frame,
        text="📊 View Attendance",
        command=calculate_attendance,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground="#0066B3",
        activeforeground="white",
        bd=0, 
        relief=FLAT, 
        cursor="hand2", 
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=10
    )
    fill_a.pack(side=LEFT, padx=8, pady=10, fill=BOTH, expand=True)

    # Open Sheets button
    attf = tk.Button(
        button_frame,
        text="📁 Open Sheets",
        command=Attf,
        bg="#06A77D",
        fg="white",
        activebackground="#058060",
        activeforeground="white",
        bd=0, 
        relief=FLAT, 
        cursor="hand2", 
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=10
    )
    attf.pack(side=LEFT, padx=8, pady=10, fill=BOTH, expand=True)

    # Close button
    exit_btn = tk.Button(
        button_frame,
        text="❌ Close",
        command=subject.destroy,
        bg="#E63946",
        fg="white",
        activebackground="#C0262D",
        activeforeground="white",
        bd=0, 
        relief=FLAT, 
        cursor="hand2", 
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=10
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

    subject.wait_window()
