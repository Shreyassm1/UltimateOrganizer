import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main App")
        self.root.geometry("400x300")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        empty_frame = tk.Frame(self.root, height=0)
        empty_frame.grid(row=0, column=0, sticky="nsew")

        self.create_buttons()

    def create_buttons(self):
        apps = {
            "Time Table App": "time_table.py",
            "Daily Tasks App": "to_do.py",
        }

        for i, (app_name, script_name) in enumerate(apps.items()):
            button = tk.Button(
                self.root,
                text=app_name,
                command=lambda script=script_name: self.run_app(script),
                width=20,
                height=2,
            )
            row = i + 1
            button.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")

    def run_app(self, script_name):
        try:
            subprocess.Popen([sys.executable, script_name])
        except FileNotFoundError:
            error_message = f"Script '{script_name}' not found. Make sure the file exists and the path is correct."
            print(error_message)
            messagebox.showerror("Error", error_message)
        except Exception as e:
            error_message = f"An error occurred while running '{script_name}': {e}"
            print(error_message)
            messagebox.showerror("Error", error_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
