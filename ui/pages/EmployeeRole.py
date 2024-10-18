import tkinter as tk
from tkinter import ttk
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.employee_role.employee_role_model import employee_role_model
from service.employee_role_service import EmployeeRoleService
from service.employee_service import EmployeeService
from service.role_service import RoleService
from helper.FormPopup import FormPopup
class EmployeeRole(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="PHÂN QUYỀN", font=("Helvetica", 16))
        label.pack(pady=20)
        self.employee_service = EmployeeService()
        self.role_service = RoleService()
        self.data_role = self.role_service.getCombobox()
        self.data_employee = self.employee_service.getCombox()
        columns = [
                {
                    'key': 'ID',
                    'name': 'ID',
                    'width': 10,
                    'anchor': 'center'
                },
                {
                    'key': 'NameEmployee',
                    'name': 'Tên nhân viên',
                    'width': 150,
                    'anchor': 'center'
                },   
                {
                    'key': 'NameRole',
                    'name': 'Tên quyền',
                    'width': 150,
                    'anchor': 'center'
                },
                {
                    'key': 'Action',
                    'name': 'Hành động',
                    'width': 100,
                    'anchor': 'center'
                }
                
            ]
        
        self.fields = [
            {'name': 'employee_role_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},
            {'name': 'employee_id', 'type': 'ComboboxCustom', 'label': 'Tên nhân viên','values': self.data_employee, 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'role_id', 'type': 'ComboboxCustom', 'label': 'Tên quyền','values': self.data_role, 'row': 0, 'col1' : 2, 'col2': 3}
        ]

        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.employee_role_service = EmployeeRoleService()
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)

    def search(self):
        rows = self.employee_role_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=600, height=120)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.employee_role_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=600, height=120)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.employee_role_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.employee_role_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.employee_role_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False