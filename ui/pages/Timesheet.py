import tkinter as tk

class Timesheet(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="BẢNG CHẤM CÔNG", font=("Helvetica", 16))
        label.pack(pady=20)
