import tkinter as tk
from ui.pages.BasePage import BasePage
from service.license_service import LicenseService
from helper.CustomTreeView import CustomTreeView
from service.employee_service import EmployeeService
from helper.FormPopup import FormPopup
from tkinter import messagebox
class License(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.employee_service = EmployeeService()
        self.license_service = LicenseService()
        self.on_show_frame()



    def search(self):
        rows = self.license_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới đơn"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=200)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập đơn"
        data = self.license_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=200)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            print(data)
            result = self.license_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.license_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.license_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False
    def on_show_frame(self):
        label = tk.Label(self, text="ĐƠN XIN PHÉP", font=("Helvetica", 16))
        label.pack(pady=20)
        self.employee_data = self.employee_service.getCombox()
        self.datas = self.search()
        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'employee_id',
                'name': 'Tên nhân viên',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key': 'reason',
                'name': 'Lý do',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key': 'start_date',
                'name': 'Ngày bắt đầu',
                'width': 80,
                'anchor': 'center'
            },
            {
                'key': 'end_date',
                'name': 'Ngày kết thúc',
                'width': 80,
                'anchor': 'center'
            },
            {
                'key': 'status',
                'name': 'Ngày kết thúc',
                'width': 80,
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
            {'name': 'request_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'employee_id', 'type': 'ComboboxCustom', 'label': 'Nhân viên' ,'values': self.employee_data, 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'reason', 'type': 'CustomInput', 'label': 'Lý do', 'row': 0, 'col1' : 2, 'col2': 3},

            {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu', 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'end_date', 'type': 'CustomDate', 'label': 'Ngày kết thúc' , 'row': 1, 'col1' : 2, 'col2': 3},

            {'name': 'status', 'type': 'ComboboxCustom', 'label': 'Trạng thái' ,'values': [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected') ], 'row': 2, 'col1' : 0, 'col2': 1},
        ]

        #Get view
        self.frame_view = tk.Frame(self)
        self.frame_view.pack(padx=10, fill="both", expand=True)
        self.treeView = CustomTreeView(self.frame_view, self, self.datas, columns, len(columns) - 1)

    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()