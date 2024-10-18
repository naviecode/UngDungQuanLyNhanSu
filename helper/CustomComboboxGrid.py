import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CustomComboboxGrid:
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
        self.combobox = ttk.Combobox(parent, width=30-4, state="readonly")
        self.combobox.grid(row=gridRow, column=gridCol, padx=10, pady=10)
        self.combobox.set('')


    def validate_input(self):
        if self.get_value() == "":
            messagebox.showerror("Lỗi", f"Vui lòng chọn giá trị cho {self.text}")
            return False
        else:
            return True
    
    def insert_combobox(self, data):
        """"""
    
    def get_value(self):
        return self.combobox.get()
        