import tkinter as tk
from ui.pages.BasePage import BasePage
from service.employee_service import EmployeeService
from service.position_service import PositionService
from service.contract_service import ContractService
from tkinter import messagebox
from helper.CustomTreeView import CustomTreeView
from helper.FormPopup import FormPopup
from tkinter import ttk


class Employee(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.contract_service = ContractService()
        self.position_service = PositionService()
        self.employee_service = EmployeeService()
        self.on_show_frame()
        

    def search(self):
        rows = self.employee_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới nhân viên"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=300)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập nhân viên"
        data = self.employee_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=300)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.employee_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.employee_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.employee_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False
    def on_show_frame(self):
        self.label = tk.Label(self, text="QUẢN LÝ NHÂN SỰ", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.data_position = self.position_service.getCombobox()
        self.columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Họ tên',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key': 'Phone',
                'name': 'Số điện thoại',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key': 'Gender',
                'name': 'Giới tính',
                'width': 20,
                'anchor': 'center'
            },
            {
                'key': 'Position',
                'name': 'Chức vụ',
                'width': 80,
                'anchor': 'center'
            },
            {
                'key': 'StartDate',
                'name': 'Ngày bắt đầu',
                'width': 80,
                'anchor': 'center'
            },
            {
                'key': 'EndDate',
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
            {'name': 'employee_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'name', 'type': 'CustomInput', 'label': 'Họ và tên' , 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'date_of_birth', 'type': 'CustomDate', 'label': 'Ngày sinh', 'row': 0, 'col1' : 2, 'col2': 3},

            {'name': 'gender', 'type': 'ComboboxCustom', 'label': 'Giới tính', 'values': [(1, 'Nam'), (0, 'Nữ')], 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'address', 'type': 'CustomInput', 'label': 'Địa chỉ' , 'row': 1, 'col1' : 2, 'col2': 3},

            {'name': 'phone_number', 'type': 'CustomInput', 'label': 'Số điện thoại' , 'row': 2, 'col1' : 0, 'col2': 1},
            {'name': 'email', 'type': 'CustomInput', 'label': 'Email' , 'row': 2, 'col1' : 2, 'col2': 3},

            {'name': 'position_id', 'type': 'ComboboxCustom', 'label': 'Vị trí', 'values': self.data_position, 'row': 3, 'col1' : 0, 'col2': 1},
            {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu', 'row': 3, 'col1' : 2, 'col2': 3},

            {'name': 'id_card_number', 'type': 'CustomInput', 'label': 'CCCD/CMND' , 'row': 4, 'col1' : 0, 'col2': 1},
            {'name': 'username', 'type': 'CustomInput', 'label': 'Tên đăng nhập' , 'row': 4, 'col1' : 2, 'col2': 3},
        ]

        #Get view
        self.frame_view = tk.Frame(self)
        self.frame_view.pack(padx=10, fill="both", expand=True)
        self.datas = self.search()
        self.treeView = CustomTreeView(self.frame_view, self, self.datas, self.columns, len(self.columns) - 1)


    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()

        

