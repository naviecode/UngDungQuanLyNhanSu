import tkinter as tk
from ui.header_ui import Header
from ui.navbar_ui import Navbar
from ui.content_ui import Content
from ui.pages.Overview import Overview
from ui.pages.BasePage import BasePage
from tkinter import ttk


class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x600")

        self.frames = {}
        #header
        header = Header(self)
        header.pack(side="top", fill="x")
        
        #navbar
        navbar = Navbar(self, self.frames)
        navbar.pack(side="left", fill="y")

        #content
        content = tk.Frame(self)
        content.pack(fill="x")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        navbar.initNav(content, self)

        #Chọn trang đầu
        navbar.show_page(Overview)


