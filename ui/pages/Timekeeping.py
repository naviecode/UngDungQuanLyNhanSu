import tkinter as tk

class Timekeeping(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Timekeeping Page", font=("Helvetica", 16))
        label.pack(pady=20)
