import tkinter as tk
from tkinter import ttk, messagebox 
import sqlite3
from datetime import datetime

class DailyTasks:
    def __init__(self, root):
        self.root = root
        self.root.title("Tasks")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTasks(root)
    root.mainloop()
