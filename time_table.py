import tkinter as tk
from tkinter import ttk, messagebox # Themed Tkinter
import sqlite3
from datetime import datetime

week_days = {
    'Monday' : 0,
    'Tuesday' : 1,
    'Wednesday' : 2,
    'Thursday' : 3,
    'Friday' : 4,
    'Saturday' : 5,
    'Sunday' : 6
}

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
        self.delete_when_day_ends()
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
                'notes': notes,
                'day_of_week': day
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

        add_button = ttk.Button(add_frame, text="Add", command=self.add_timetable_entry)
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

                entry_frame = ttk.Frame(frame)
                entry_frame.pack(fill='x', padx=2, pady=2)

                entry_label = ttk.Label(entry_frame, text=label_text, borderwidth=1, relief="solid", anchor="w", padding=8)
                entry_label.pack(side='left', fill='x', expand=True)

                delete_btn = ttk.Button(entry_frame, text="Delete", command = lambda day = entry['day_of_week'], ID = entry['id']: self.delete_timetable_entry(day, frame, ID))
                # We use a lambda function here and not directly pass the function in the command to avoid instant delete when the app runs.
                # If we don't use ID, day to contain the params, it passes the same ID to each del btn i.e. ID of the last entry.
                delete_btn.pack(side='right')
            
                entry_label.bind("<Double-1>", lambda event, item = entry: self.show_dia_box(item))

    # Function to add events in the timetable through input fields 
    def add_timetable_entry(self):
        day = self.day_combo.get()
        end_time = self.end_time_entry.get()
        notes = self.notes_entry.get()

        if not all([day, end_time, notes]):
            messagebox.showerror("Error", "Please fill in all required fields (Day, End Time, Note).")
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

    # Function to delete entries - takes 3 args other than self
    # 1. Day where the delete btn is - to repopulate the widget after deletion
    # 2. The primary frame of each day
    # 3. ID of the entry to which the delete button is associated
    def delete_timetable_entry(self, day, frame, entry_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM timetable WHERE id = ?", (entry_id,))
            conn.commit()
            conn.close()
            print(f"Deleted entry with id: {entry_id}")
            self.timetable_data = self.fetch_timetable()
            self.populate_day_schedule(day, frame)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting entry: {e}")

    # Runs before the widgets are created, making sure the events before today are deleted as soon as app starts 
    def delete_when_day_ends(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        today = datetime.now().weekday()
        for day in week_days:
            if week_days[day] < today:
                cursor.execute("DELETE FROM timetable WHERE day_of_week = ?", (day,))
        conn.commit()
        conn.close()
        print(f"Deleted entries for days before {today}.")

    def show_dia_box(self, item):
        dia_box = tk.Toplevel(self.root)
        dia_box.title("Edit Event")
        dia_box.minsize(350,200)
        dia_box.maxsize(350,200)

        ttk.Label(dia_box, text = "Edit Note: ").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.edited_note = ttk.Entry(dia_box)
        self.edited_note.insert(0, item['notes'])
        self.edited_note.grid(row = 0, column = 2, padx = 10, pady = 10)
        ttk.Label(dia_box, text = "Edit Time(HH:MM): ").grid(row = 1, column = 0, padx = 10, pady = 10)
        self.edited_time = ttk.Entry(dia_box)
        self.edited_time.insert(0,item['end_time'])
        self.edited_time.grid(row = 1, column = 2, padx = 5, pady = 5)
        ttk.Button(dia_box, text = "Save", command = lambda item = item: self.edit_timetable_entry(item, dia_box)).grid(row = 2, column = 1, padx = 5, pady = 5)

        dia_box.columnconfigure(1, weight=1)
        dia_box.transient(self.root)
        dia_box.grab_set()
        self.root.wait_window(dia_box)

    def edit_timetable_entry(self, item, dia_box):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        new_note = self.edited_note.get()
        end_time = self.edited_time.get()
        if not (len(end_time) == 5 and end_time[2] == ':' and end_time[:2].isdigit() and end_time[3:].isdigit()):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
            return
        if new_note != item['notes']:
            if len(new_note) != 0:
                cursor.execute(
                """UPDATE timetable SET notes = ? WHERE id = ?""", (new_note, item['id'])
                )
                print("Note updated") 
        elif end_time != item['end_time']:
                cursor.execute(
                """UPDATE timetable SET end_time = ? WHERE id = ?""", (end_time, item['id'])
                )
                print("Time updated")  
        else: print("No update needed")
             
        conn.commit()
        conn.close()
        self.timetable_data = self.fetch_timetable()
        self.populate_day_schedule(item['day_of_week'], self.timetable_frames[item['day_of_week']])
        dia_box.destroy()
              