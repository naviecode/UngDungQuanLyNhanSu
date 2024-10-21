import tkinter as tk

class Timesheet(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)






        self.on_show_frame()

        
    def on_show_frame(self):
        label = tk.Label(self, text="BẢNG CHẤM CÔNG", font=("Helvetica", 16))
        label.pack(pady=20)
        
    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()