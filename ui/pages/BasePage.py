import tkinter as tk
import threading
from helper import ButtonImage, LoadingPopup
from PIL import Image, ImageTk 
from helper import ButtonImage, LoadingPopup, CustomInputText, CustomInputDate

class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)       

        self.nav_base = tk.Frame(self, height=30)
        self.nav_base.pack(padx=10,fill="x",expand=True)
        self.nav_base.pack_propagate(False)

        self.frame_filter = tk.Frame(self.nav_base, width=400, height=30)
        self.frame_filter.pack(padx=10, side="left")

        self.label_name = tk.Label(self.frame_filter, text="Tên")
        self.label_name.grid(padx=8,row=1, column=0)
        self.param_name = CustomInputText(self.frame_filter, width=30, required=False, type="Text")
        self.param_name.grid(padx=8,row=1, column=1)
        self.label_from_date = tk.Label(self.frame_filter, text="Từ ngày")
        self.label_from_date.grid(padx=8,row=1, column=2)
        self.param_from_date = CustomInputDate(self.frame_filter, width=30-4, required=False)
        self.param_from_date.grid(padx=8,row=1, column=3)
        self.label_to_date = tk.Label(self.frame_filter, text="Đến ngày")
        self.label_to_date.grid(padx=8,row=1, column=4)
        self.param_to_date = CustomInputDate(self.frame_filter, width=30-4, required=False)
        self.param_to_date.grid(padx=8,row=1, column=5)

        self.button_export = ButtonImage(self.nav_base, "./images/icons/export_excel.png", "Xuất Excel", self.export_excel,width=150, height=30, bg="#0178bc", fg="white")
        self.button_export.pack(side="right",padx=10)

        self.button_add = ButtonImage(self.nav_base, "./images/icons/add.png", "Thêm mới", self.add,width=150, height=30, bg="#0178bc", fg="white")
        self.button_add.pack(side="right",padx=10)

        self.button_search = ButtonImage(self.nav_base, "./images/icons/add.png", "Thêm mới", self.search,width=150, height=30, bg="#0178bc", fg="white")
        self.button_search.pack(side="right")

        # set widget thuộc base
        self.nav_base._from_base = True

        # set background
        self.set_background()

    def set_background(self):
        self.background_image = Image.open("./images/background/CloudBackground.png")
        self.background_image = self.background_image.resize((self.winfo_screenwidth() - 250, self.winfo_screenheight() - 100), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1) 
        
    def add(self):
        print("Thêm mới")

    def search(self):
        self.param = {
            'name': self.param_name.get_value(),
            'from_date': self.param_from_date.get_value().strftime('%Y-%m-%d'),
            'to_date': self.param_to_date.get_value().strftime('%Y-%m-%d')
        }

    def export_excel(self):
        print("export")
    def set_permission_button(self, btn_export_show = False, btn_add_show = False, btn_add_search = False):
        if btn_export_show:
            self.button_export.pack()
        else:
            self.button_export.pack_forget()
        if btn_add_show:
            self.button_add.pack()
        else:
            self.button_add.pack_forget()
        if btn_add_search:
            self.button_search.pack()
            self.frame_filter.pack()
        else:
            self.button_search.pack_forget()
            self.frame_filter.pack_forget()

        if(btn_add_show is not True and btn_export_show is not True and btn_add_search is not True):
            self.nav_base.pack_forget()

    def show_loading(self):
        self.loading_popup = LoadingPopup(self)
        self.loading_popup._from_base = True
        # Gọi quá trình load dữ liệu trong một thread khác
        threading.Thread(target=self.simulate_loading).start()

    def simulate_loading(self):
        self.loading_popup.complete_loading()




