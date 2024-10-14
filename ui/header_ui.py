import tkinter as tk
from PIL import Image, ImageTk

class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        header = tk.Frame(self, bg="#0178bc", height=40)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        header_left = tk.Frame(header, width=250, bg="#0178bc")
        header_left.pack(side="left", fill="y")
        header_left.pack_propagate(False)   

        header_left_logo = tk.Label(header_left, text="QUẢN LÝ NHÂN SỰ", bg="#0178bc", fg="white",font=("Arial", 14), cursor="hand2")
        header_left_logo.pack(expand=True)
        header_left_logo.pack()

        header_right = tk.Frame(header, bg="#0178bc", width=250)
        header_right.pack(side="right", fill="y")
        header_right.pack_propagate(False)

        image_user = Image.open("./images/icons/user.png")
        resized_image_user = image_user.resize((25,25))
        self.image_user = ImageTk.PhotoImage(resized_image_user)
        image_setting = Image.open("./images/icons/setting.png")
        resized_image_setting = image_setting.resize((25,25))
        self.image_setting = ImageTk.PhotoImage(resized_image_setting)
        image_notify = Image.open("./images/icons/notify.png")
        resized_image_notify = image_notify.resize((25,25))
        self.image_notify = ImageTk.PhotoImage(resized_image_notify)

        button_image_notify = tk.Button(header_right,
            image=self.image_notify,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2"
        )
        button_image_notify.pack(side="left", padx=20)


        button_image_user = tk.Button(header_right,
            image=self.image_user,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2"
        )
        button_image_user.pack(side="left", padx=20)

        button_image_setting = tk.Button(header_right,
            image=self.image_setting,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2"
        )
        button_image_setting.pack(side="left", padx=20)