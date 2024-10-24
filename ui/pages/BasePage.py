import tkinter as tk
import threading
from helper import ButtonImage, LoadingPopup

class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)       

        self.nav_base = tk.Frame(self, height=30)
        self.nav_base.pack(padx=10,fill="x",expand=True)
        self.nav_base.pack_propagate(False)

        self.button_export = ButtonImage(self.nav_base, "./images/icons/export_excel.png", "Xuất Excel", self.export_excel,width=150, height=30, bg="#0178bc", fg="white")
        self.button_export.pack(side="right",padx=10)

        self.button_add = ButtonImage(self.nav_base, "./images/icons/add.png", "Thêm mới", self.add,width=150, height=30, bg="#0178bc", fg="white")
        self.button_add.pack(side="right",padx=10)

        self.button_search = ButtonImage(self.nav_base, "./images/icons/add.png", "Tìm kiếm", self.search,width=150, height=30, bg="#0178bc", fg="white")
        self.button_search.pack(side="right")

        # set widget thuộc base
        self.nav_base._from_base = True
        
    def add(self):
        print("Thêm mới")
    def search(self):
        print("Tìm theo filter")
    def export_excel(self):
        print("export")
    def set_permission_button(self, btn_export_show = True, btn_add_show = True):
        if btn_export_show:
            self.button_export.pack()
        else:
            self.button_export.pack_forget()
        if btn_add_show:
            self.button_add.pack()
        else:
            self.button_add.pack_forget()

        if(btn_add_show is not True and btn_export_show is not True):
            self.nav_base.pack_forget()

    def show_loading(self):
        self.loading_popup = LoadingPopup(self)
        self.loading_popup._from_base = True
        # Gọi quá trình load dữ liệu trong một thread khác
        threading.Thread(target=self.simulate_loading).start()

    def simulate_loading(self):
        self.loading_popup.complete_loading()




