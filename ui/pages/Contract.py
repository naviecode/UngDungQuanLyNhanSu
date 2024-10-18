import tkinter as tk
from ui.pages.BasePage import BasePage

class Contract(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="DANH SÁCH HỢP ĐỒNG NHÂN VIÊN", font=("Helvetica", 16))
        label.pack(pady=20)
