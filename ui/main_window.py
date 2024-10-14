import tkinter as tk
from ui.header_ui import Header
from ui.navbar_ui import Navbar
from ui.content_ui import Content
from ui.pages.Overview import Overview
from ui.pages.BasePage import BasePage


class main_window(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_frames = BasePage(self)
        self.frames = {}
        #header
        header = Header(self)
        header.pack(side="top", fill="x")
        
        #navbar
        navbar = Navbar(self, self.frames)
        navbar.pack(side="left", fill="y")

        #content
        content = Content(self)
        content.pack(fill="x")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        navbar.initNav(content)

        navbar.show_page(Overview)

