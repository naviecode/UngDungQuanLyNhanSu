import tkinter as tk
from tkinter import messagebox

class CustomInputGridText:
    def __init__(self, parent, text, width, gridCol, gridRow):
        self.text = text
        self.entry_input = tk.Entry(parent, width=width)
        self.entry_input.grid(row=gridRow, column=gridCol, padx=10, pady=10)


    def validate_input(self):
        # Nếu chuỗi rỗng thì báo lỗi
        if self.entry_input.get() == "":
            messagebox.showerror("Lỗi nhập liệu", f"Không được để trống {self.text}")
            return False
        else:
            return True
        
    def is_number(self):
        if self.entry_input.get() == "":
            messagebox.showerror("Lỗi nhập liệu", f"Không được để trống {self.text}")
            return False
        elif not self.entry_input.get().isdigit():
            messagebox.showerror("Lỗi dữ liệu", f"Chỉ được nhập số cho {self.text}")
            return False
        return True
    
    def set_value(self, value):
        self.entry_input.insert(0, value)
    
    def get_value(self):
        return self.entry_input.get()
    
    def delete_value(self):
        self.entry_input.delete(0, tk.END)
        