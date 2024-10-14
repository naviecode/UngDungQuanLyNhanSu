import tkinter as tk

class License(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="License Page", font=("Helvetica", 16))
        label.pack(pady=20)
