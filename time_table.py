import tkinter as tk
from tkinter import ttk, messagebox # Themed Tkinter
import sqlite3
from datetime import datetime

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Planner")

        ttk.Style().theme_use('classic')

        # configure fonts
        style = ttk.Style()
        style.configure("TLabelframe.Label", font=('Segoe UI', 10, 'bold'))
        style.configure("TLabel", font=('Segoe UI', 9))
        style.configure("TEntry", font=('Segoe UI', 9))
        style.configure("TButton", font=('Segoe UI', 9, 'bold'))
        style.configure("TCombobox", font=('Segoe UI', 9))

        self.db_name = 'timetable.db'
        self.create_table()

        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.timetable_data = self.fetch_timetable()

        self.create_widgets()

    # Function to create a table using python's in-built sqlite3
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week TEXT NOT NULL,
                end_time TEXT NOT NULL,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()

    # Function to Select the columns and fecth their data from the db, 
    def fetch_timetable(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, day_of_week, end_time, notes FROM timetable ORDER BY day_of_week, end_time")
        rows = cursor.fetchall()
        conn.close()
        timetable = {day: [] for day in self.days} # Populate a dictionary using key-value pairs of day : [list]
        for row in rows:
            _id, day, end_time, notes = row
            timetable[day].append({
                'id': _id,
                'end_time': end_time,
                'notes': notes
            }) 
        return timetable

    # Function to Create Widgets when app runs, which are then populated with the data
    def create_widgets(self):
        # Timetable Display
        self.timetable_frames = {}
        for i, day in enumerate(self.days):
            frame = ttk.LabelFrame(self.root, text=day)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            self.root.grid_columnconfigure(i, weight=1)
            self.timetable_frames[day] = frame
            self.populate_day_schedule(day, frame)

        # Add New Entry Section
        add_frame = ttk.LabelFrame(self.root, text="Add New Entry")
        add_frame.grid(row=1, column=0, columnspan=len(self.days), padx=10, pady=10, sticky='ew')

        ttk.Label(add_frame, text="Day:").grid(row=0, column=0, padx=5, pady=5)
        self.day_combo = ttk.Combobox(add_frame, values=self.days)
        self.day_combo.grid(row=0, column=1, padx=5, pady=5)
        self.day_combo.set(self.days[datetime.now().weekday()])

        ttk.Label(add_frame, text="End Time (HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        self.end_time_entry = ttk.Entry(add_frame)
        self.end_time_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Notes:").grid(row=0, column=2, padx=5, pady=5)
        self.notes_entry = ttk.Entry(add_frame)
        self.notes_entry.grid(row=0, column=3, padx=5, pady=5)

        add_button = ttk.Button(add_frame, text="Add Entry", command=self.add_timetable_entry)
        add_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # Configure row and column weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        for i in range(len(self.days)):
            self.root.grid_columnconfigure(i, weight=1)

    # Function to generate the widgets and fill the events in their respective days
    def populate_day_schedule(self, day, frame):
        for widget in frame.winfo_children():
            widget.destroy() # Delete the widgets before loading new ones to prevent repetition

        schedule = self.timetable_data.get(day, [])
        if not schedule:
            ttk.Label(frame, text="No entries for " + day + ".").pack(padx=5, pady=5)
        else:
            for entry in schedule:
                label_text = f"End Time: {entry['end_time']}"
                if entry.get('notes'):
                    label_text += f"\n{entry['notes']}"
                entry_label = ttk.Label(frame, text=label_text, borderwidth=1, relief="solid", anchor="w", padding=8)
                entry_label.pack(fill='x', padx=2, pady=2)
                entry_label.bind("<Double-1>", lambda event, entry_id=entry['id']: self.edit_timetable_entry(entry_id))

    # Function to add events in the timetable through input fields 
    def add_timetable_entry(self):
        day = self.day_combo.get()
        end_time = self.end_time_entry.get()
        notes = self.notes_entry.get()

        if not all([day, end_time]):
            messagebox.showerror("Error", "Please fill in all required fields (Day, End Time).")
            return

        if not (len(end_time) == 5 and end_time[2] == ':' and end_time[:2].isdigit() and end_time[3:].isdigit()):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO timetable (day_of_week, end_time, notes)
            VALUES (?, ?, ?)
        """, (day, end_time, notes))
        conn.commit()
        conn.close()

        self.timetable_data = self.fetch_timetable()
        self.populate_day_schedule(day, self.timetable_frames[day])

        # After adding the data - delete the text in the input fields - clear state
        self.end_time_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)