import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import calendar
from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk
import calendar
from datetime import datetime

class Timesheet(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="BẢNG CHẤM CÔNG", font=("Helvetica", 16))
        label.pack(pady=20)
