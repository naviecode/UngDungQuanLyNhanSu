import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

class CustomInputDateGrid:
    def __init__(self, parent, text, type, gridCol, gridRow):
        """
            text:
            type: Text, Number, 
            gridCol: 0 , 2
            gridRow: 0
        """
        self.text = text
        self.label = tk.Label(parent, text=text)
        self.label.grid(row=gridRow, column=gridCol, padx=10, pady=10, sticky="e")
        self.date_entry = DateEntry(parent, width=30-4, selectmode='day', date_pattern='dd-mm-y')
        self.date_entry.grid(row=gridRow, column=gridCol+1, padx=10, pady=10)

    def validate_input(self):
        if self.get_value() == "":
            messagebox.showerror("Lỗi", f"vui lòng chọn ngày hợp lệ {self.text}")
            return False
        try:
            entered_date = self.get_value().strftime('%d-%m-%Y')
            messagebox.showinfo("Thành công", f"Ngày bạn chọn là: {entered_date}")
            return True
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ! Vui lòng nhập đúng định dạng (DD-MM-YYYY).")
            return False
        
    def insert_date(self, data):
        """"""
        
    def get_value(self):
        return self.date_entry.get_date()
        