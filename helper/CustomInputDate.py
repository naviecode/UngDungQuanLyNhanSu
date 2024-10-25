import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

class CustomInputDate:
    def __init__(self, parent, width, text = None, selectMode='day', date_pattern='dd-mm-y' , required = False):
        self.text = text
        self.date_entry = DateEntry(parent, width=width, selectmode=selectMode, date_pattern=date_pattern)
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
    

    def grid(self, **kwargs):
        self.date_entry.grid(**kwargs)

    def pack(self, **kwargs):
        self.date_entry.pack(**kwargs)
