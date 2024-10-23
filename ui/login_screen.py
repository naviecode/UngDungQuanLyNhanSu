import tkinter as tk
from tkinter import messagebox
from service.employee_service import EmployeeService
import globals
from models.user.user_model import User
from helper.CustomInputText import CustomInputText


class LoginScreen:
    def __init__(self, master, main_app):
        self.master = master
        self.main_app = main_app
        self.employee_service = EmployeeService()
        x = (main_app.screen_width //2) - (350//2)
        y = (main_app.screen_height //2) - (200//2)
        self.master.geometry(f'{350}x{200}+{x}+{y}')

        self.master.title("Đăng nhập nhân viên")
        # Label và Entry cho tên người dùng
        self.label_username = tk.Label(master, text="Tên người dùng:")
        self.label_username.pack(pady=5)
        self.entry_username = CustomInputText(master, 'Tên người dùng')
        self.entry_username.pack(pady=5)

        # Label và Entry cho mật khẩu
        self.label_password = tk.Label(master, text="Mật khẩu:")
        self.label_password.pack(pady=5)
        self.entry_password = CustomInputText(master,'Mật khẩu', show="*")  # Hiển thị dấu *
        self.entry_password.pack(pady=5)

        # Nút Đăng Nhập
        self.button_login = tk.Button(master, text="Đăng Nhập", command=self.check_login)
        self.button_login.pack(pady=20)

        #Nút thoát
        self.button_exit = tk.Button(master, text="Thoát", command=self.main_app.exit)
        self.button_exit.pack(pady=20)
    
    def is_login(self, username, password):
        result = self.employee_service.getLoginUser(username, password)
        if result is not None:
            globals.current_user = User(result[0],result[1],result[2], result[3])

            return True
        else:
            return False
        

    def check_login(self):

        if(not self.entry_username.validate_input() or not self.entry_password.validate_input()):return

        username = self.entry_username.get_value().strip()
        password = self.entry_password.get_value().strip()

        if self.is_login(username, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.master.destroy() 
            self.main_app.open_main_window() 
        else:
            messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
