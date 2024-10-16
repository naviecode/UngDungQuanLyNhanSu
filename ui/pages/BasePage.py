import tkinter as tk
from helper.ButtonImage import ButtonImage


class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)       

        nav_base = tk.Frame(self, height=40)
        nav_base.pack(padx=10,fill="x",expand=True)
        nav_base.pack_propagate(False)

        self.button_export = ButtonImage(nav_base, "./images/icons/add.png", "Xuất Excel", self.export_excel,width=150, height=30, bg="#0178bc", fg="white")
        self.button_export.pack(side="right",padx=10)

        self.button_add = ButtonImage(nav_base, "./images/icons/add.png", "Thêm mới", self.add,width=150, height=30, bg="#0178bc", fg="white")
        self.button_add.pack(side="right")

       

    def add(self):
        print("Thêm mới")
    def export_excel(self):
        print("export")




