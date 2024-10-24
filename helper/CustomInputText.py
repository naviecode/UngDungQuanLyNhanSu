import tkinter as tk
from tkinter import messagebox

class CustomInputText:
    def __init__(self, parent, text, width = None, show = None, required = False, type = "Text"):
        self.text = text
        self.entry_input = tk.Entry(parent, width=width, show=show)
        self.type = type
        self.novalidate = True
        if(required):
            self.novalidate = False


    def validate_input(self):
        if self.type == "Text":
            if(self.novalidate):
                return True
            if self.entry_input.get() == "":
                messagebox.showerror("Lỗi nhập liệu", f"Không được để trống {self.text}")
                return False
            else:
                return True
        elif self.type == "Number":
            if self.entry_input.get() == "":
                messagebox.showerror("Lỗi nhập liệu", f"Không được để trống {self.text}")
                return False
            elif not self.entry_input.get().isdigit():
                messagebox.showerror("Lỗi dữ liệu", f"Chỉ được nhập số cho {self.text}")
                return False
            else:
                return True
        else:
            return True
                
    
    def set_value(self, value):
        self.entry_input.insert(0, value)
    
    def get_value(self):
        return self.entry_input.get()
    
    def delete_value(self):
        self.entry_input.delete(0, tk.END)
    
    # def grid(self, row, column, padx = 0, pady = 0):
    #     self.entry_input.grid(row=row, column=column, padx=padx, pady=pady)

    # def pack(self, padx=0, pady=0):
    #     self.entry_input.pack(padx=padx, pady=pady)

    def grid(self, **kwargs):
        self.entry_input.grid(**kwargs)

    def pack(self, **kwargs):
        self.entry_input.pack(**kwargs)