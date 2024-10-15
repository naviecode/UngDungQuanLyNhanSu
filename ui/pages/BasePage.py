import tkinter as tk
import configparser
from data.init_data import InitData
from helper.ButtonImage import ButtonImage


class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)       

        #Connect database and create table
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        self.db.connect_database()
        self.db.create_table()
        self.db.close_connection()

        nav_base = tk.Frame(self, height=40)
        nav_base.pack(padx=10,fill="x",expand=True)
        nav_base.pack_propagate(False)

        self.button_add = ButtonImage(nav_base, "./images/icons/add.png", "Thêm mới", self.add,width=150, height=30, bg="#0178bc", fg="white")
        self.button_add.pack(side="right")

    def add(self):
        print("Thêm mới")
    def export_excel(self):
        print("export")




