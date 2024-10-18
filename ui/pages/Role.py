import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.role.role_model import role_model
from service.role_service import RoleService
from datetime import datetime

class Role(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUYỀN", font=("Helvetica", 16))
        label.pack(pady=20)

        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên quyền',
                'width': 150,
                'anchor': 'center'
            },   
            {
                'key': 'Description',
                'name': 'Mô tả',
                'width': 200,
                'anchor': 'center'
            },
            {
                'key': 'Action',
                'name': 'Hành động',
                'width': 100,
                'anchor': 'center'
            }
            
        ]


        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.role_service = RoleService()
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)
    
    def search(self):
        rows = self.role_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = RoleFormPopup(self, None)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.role_service.getById(row_id)
        form_popup = RoleFormPopup(self, data)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.role_service.insert(data)
            self.treeView.loadData()

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.role_service.update(data)
            self.treeView.loadData()
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.role_service.delete(row_id)
            self.treeView.loadData()


class RoleFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.geometry("600x120")
        self.title(parent.title_popup)
        self.parent = parent
        
        window_width = 600
        window_height = 120
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        #Căn giữa popup
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.grab_set()

        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)
        self.entry_id.grid_remove()

        label_name = tk.Label(self, text="Tên quyền:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)


        label_desc = tk.Label(self, text="Mô tả:")
        label_desc.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_desc = tk.Entry(self, width=30)
        self.entry_desc.grid(row=0, column=3, padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.entry_desc.insert(0, data[2])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save)
        self.button_save.pack(side="right", padx=5)

    def save(self):
        role_id = self.entry_id.get() if self.entry_id.get() is not None else None
        role_input = role_model(
            role_id=role_id,
            role_name=self.entry_name.get(),
            description=self.entry_desc.get()
        )

        if role_input.role_id is None or role_input.role_id == "":
            self.parent.insert(role_input)
            self.destroy()
        else:
            self.parent.update(role_input)
            self.destroy()
