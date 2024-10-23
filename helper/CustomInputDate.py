import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

class CustomInputDate:
    def __init__(self, parent, text, width, selectMode, date_pattern , required = False):
        self.text = text
        self.date_entry = DateEntry(parent, width=width, selectmode='day', date_pattern='dd-mm-y')
        self.novalidate = True
        if(required):
            self.novalidate = False


    def validate_input(self):
        if(self.novalidate):
            return True
        if self.get_value() == "":
            messagebox.showerror("Lỗi nhập liệu", f"vui lòng chọn ngày hợp lệ {self.text}")
            return False
        try:
            entered_date = self.get_value().strftime('%d-%m-%Y')
            return True
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Định dạng ngày không hợp lệ! Vui lòng nhập đúng định dạng (DD-MM-YYYY).")
            return False
        
    def set_date(self, data):
        self.date_entry.set_date(data)
        
    def get_value(self):
        return self.date_entry.get_date()
    
    def grid(self, row, column, padx=10, pady=10):
        self.date_entry.grid(row=row, column=column, padx=padx, pady=pady)
