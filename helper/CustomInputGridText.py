import tkinter as tk
from tkinter import messagebox

class CustomInputGridText:
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
        self.entry_input = tk.Entry(parent, width=30)
        self.entry_input.grid(row=gridRow, column=gridCol + 1, padx=10, pady=10)


    def validate_input(self):
        # Nếu chuỗi rỗng thì báo lỗi
        if self.entry_input.get() == "":
            messagebox.showerror("Lỗi", f"Không được để trống {self.text}")
            return False
        else:
            return True
        
    def is_number(self):
        if self.entry_input.get() == "":
            messagebox.showerror("Lỗi", f"Không được để trống {self.text}")
            return False
        elif not self.entry_input.get().isdigit():
            messagebox.showerror("Lỗi", f"Chỉ được nhập số cho {self.text}")
            return False
        return True
    
    def insert_input(self, data):
        """"""
    
    def get_value(self):
        return self.entry_input.get()
        