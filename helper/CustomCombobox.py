from tkinter import ttk
from tkinter import messagebox

class CustomCombobox:
    def __init__(self, parent, text, dataArray, width, required = False):
        self.selected_id = None
        self.datas = dataArray
        self.text = text
        self.combobox = ttk.Combobox(parent, width=width, state="readonly")
        self.combobox['values'] = [f"{pos[1]}" for pos in dataArray]
        self.combobox.set('')
        self.combobox.bind("<<ComboboxSelected>>", self.on_selected)
        self.novalidate = True
        if(required):
            self.novalidate = False


    def validate_input(self):
        if(self.novalidate):
            return True
        if self.combobox.get() == "":
            messagebox.showerror("Lỗi nhập liệu", f"Vui lòng chọn giá trị cho {self.text}")
            return False
        else:
            return True
    
    def get_value(self):
        return self.selected_id
    
    def on_selected(self, event):
        selected_name = self.combobox.get()
        self.selected_id = None
        for data in self.datas:
            if data[1] == selected_name:
                self.selected_id = data[0]
                break
    
    def set_combobox(self, position_id):
        self.selected_id = position_id
        for data in self.datas:
            if data[0] == position_id:
                self.combobox.set(data[1])  
                break
    def grid(self, row, column, padx=10, pady=10):
        self.combobox.grid(row=row, column=column, padx=padx, pady=pady)

        