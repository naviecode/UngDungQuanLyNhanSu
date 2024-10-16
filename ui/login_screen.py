import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self, master, main_app):
        self.master = master
        self.main_app = main_app

        x = (main_app.screen_width //2) - (350//2)
        y = (main_app.screen_height //2) - (200//2)
        self.master.geometry(f'{350}x{200}+{x}+{y}')

        self.master.title("Đăng nhập nhân viên")
        # Label và Entry cho tên người dùng
        self.label_username = tk.Label(master, text="Tên người dùng:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=5)

        # Label và Entry cho mật khẩu
        self.label_password = tk.Label(master, text="Mật khẩu:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, show="*")  # Hiển thị dấu *
        self.entry_password.pack(pady=5)

        # Nút Đăng Nhập
        self.button_login = tk.Button(master, text="Đăng Nhập", command=self.check_login)
        self.button_login.pack(pady=20)

        #Nút thoát
        self.button_exit = tk.Button(master, text="Thoát", command=self.main_app.exit)
        self.button_exit.pack(pady=20)
    
    def is_login(self, username, password):
        # Kiểm tra username và password
        if username == "admin" and password == "1":
            return True
        else:
            return False
        

    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.is_login(username, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.master.destroy()  # Đóng cửa sổ đăng nhập
            self.main_app.open_main_window()  # Gọi cửa sổ chính từ main_app
        else:
            messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
