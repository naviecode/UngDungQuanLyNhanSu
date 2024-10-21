import tkinter as tk
from ui.header_ui import Header
from ui.navbar_ui import Navbar
from ui.pages.Overview import Overview
from ui.login_screen import LoginScreen
from models.user.user_model import User
from data.init_data import InitData
import configparser
from tkinter import messagebox
import globals

class main_window:
    def __init__(self, master):
        globals.current_user = User(1,"username",1, "username")

        self.root = master
        self.root.title("Ứng dụng Quản lý Nhân sự")
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        self.db.connect_database()
        self.db.create_table()
        self.db.create_data()
        self.db.close_connection()

        self.root.frames = {}
        self.is_logged_in = False  # Biến theo dõi trạng thái đăng nhập
        self.login_window = None

        # Khi mở chương trình, kiểm tra trạng thái đăng nhập
        # self.check_login()
        self.open_main_window()


        
    def check_login(self):
        if not self.is_logged_in:
            self.root.withdraw()
            self.open_login_window()
        

    def open_login_window(self):
        # Mở trang đăng nhập
        self.login_window = tk.Toplevel(self.root)
        LoginScreen(self.login_window, self)

    def open_main_window(self):
        # Hiển thị giao diện chính sau khi đăng nhập thành công
        self.is_logged_in = True  # Đánh dấu trạng thái đăng nhập
        self.root.deiconify()       

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        #header
        header = Header(self.main_frame, self)
        header.pack(side="top", fill="x")
        
        #navbar
        navbar = Navbar(self.main_frame, self.root.frames)
        navbar.pack(side="left", fill="y")

        #content
        content = tk.Frame(self.main_frame)
        content.pack(fill="x")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        navbar.initNav(content, self.main_frame)

        #Chọn trang đầu
        navbar.show_page(Overview)
        

    def logout(self):
        # Hàm đăng xuất
        self.is_logged_in = False
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất!")
        globals.current_user = None
        self.main_frame.destroy()  # Xóa giao diện chính
        self.check_login()  # Quay lại trang đăng nhập

    def exit(self):
        self.root.destroy()

    


