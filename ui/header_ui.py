import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

class Header(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
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
            cursor="hand2",
            command=self.show_popup_notify
        )
        button_image_notify.pack(side="left", padx=20)


        button_image_user = tk.Button(header_right,
            image=self.image_user,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2",
            command=self.show_popup_user
        )
        button_image_user.pack(side="left", padx=20)

        button_image_setting = tk.Button(header_right,
            image=self.image_setting,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2",
            command=self.show_popup_setting
        )
        button_image_setting.pack(side="left", padx=20)


    def show_popup_user(self):
        # Tạo cửa sổ popup
        popup = tk.Toplevel(self.master)
        x = (self.main_app.screen_width //2) - (300//2)
        y = (self.main_app.screen_height //2) - (150//2)
        popup.title("Thông tin người dùng")
        popup.geometry(f'{300}x{150}+{x}+{y}') # Kích thước popup
        
        # Nội dung trong popup
        label = tk.Label(popup, text="Đây là nội dung trong popup!", font=("Helvetica", 12))
        label.pack(pady=20)

        # Nút Đóng
        close_button = tk.Button(popup, text="Đăng xuất", command=self.logout)
        close_button.pack(pady=10)

    def show_popup_notify(self):
        # Tạo cửa sổ popup
        popup = tk.Toplevel(self.master)
        x = (self.main_app.screen_width //2) - (300//2)
        y = (self.main_app.screen_height //2) - (150//2)
        popup.title("Thông báo")
        popup.geometry(f'{300}x{150}+{x}+{y}') # Kích thước popup
        
        # Nội dung trong popup
        label = tk.Label(popup, text="Đây là nội dung trong popup!", font=("Helvetica", 12))
        label.pack(pady=20)
    
    def show_popup_setting(self):
        # Tạo cửa sổ popup
        popup = tk.Toplevel(self.master)
        x = (self.main_app.screen_width //2) - (300//2)
        y = (self.main_app.screen_height //2) - (150//2)
        popup.title("Cài đặt")
        popup.geometry(f'{300}x{150}+{x}+{y}') # Kích thước popup
        
        # Nội dung trong popup
        label = tk.Label(popup, text="Đây là nội dung trong popup!", font=("Helvetica", 12))
        label.pack(pady=20)

    def logout(self):
        # Hiển thị thông báo xác nhận đăng xuất
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            # Xóa giao diện chính
            self.main_app.logout()