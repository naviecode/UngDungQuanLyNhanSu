import tkinter as tk
import configparser
from tkinter import messagebox
from ui import Header, LoginScreen, Navbar
from ui.pages import Overview
from models import UserModel
from data import InitData
import globals


class MainWindow:
    def __init__(self, master):
        self.root = master
        self.root.title("Ứng dụng Quản lý Nhân sự")
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.state('zoomed')
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        self.db.connect_database()
        self.db.create_table()
        self.db.create_data()
        self.db.close_connection()

        self.root.frames = {}
        self.is_logged_in = False
        self.login_window = None

        self.check_login()
        
    def check_login(self):
        if not self.is_logged_in:
            self.root.withdraw()
            self.open_login_window()
        

    def open_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        LoginScreen(self.login_window, self)

    def open_main_window(self):
        self.is_logged_in = True 
        self.root.deiconify()
        self.root.state('zoomed')
        self.root.iconbitmap('./images/icons/manager_main.ico')

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
        self.is_logged_in = False
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất!")
        globals.current_user = None
        self.main_frame.destroy() 
        self.check_login()  

    def exit(self):
        self.root.destroy()

    


