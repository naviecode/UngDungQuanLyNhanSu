import tkinter as tk
from ui.pages.BasePage import BasePage
from helper.CustomTreeView import CustomTreeView
from helper.FormPopup import FormPopup
from service.contract_service import ContractService
from service.employee_service import EmployeeService
from tkinter import messagebox

class Contract(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.employee_service = EmployeeService()
        self.contract_service = ContractService()
        self.on_show_frame()


    def search(self):
        rows = self.contract_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=180)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.contract_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=180)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.contract_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.contract_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.contract_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False

    def on_show_frame(self):
        label = tk.Label(self, text="DANH SÁCH HỢP ĐỒNG NHÂN VIÊN", font=("Helvetica", 16))
        label.pack(pady=20)

        self.data_employee = self.employee_service.getCombox()
        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên nhân viên',
                'width': 150,
                'anchor': 'center'
            },   
            {
                'key': 'Salary',
                'name': 'Mức lương',
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
            {'name': 'contract_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'employee_id', 'type': 'ComboboxCustom', 'label': 'Nhân viên' ,'values': self.data_employee, 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'salary', 'type': 'CustomInput', 'label': 'Mức lương', 'row': 0, 'col1' : 2, 'col2': 3},

            {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu' , 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'end_date', 'type': 'CustomDate', 'label': 'Ngày kết thúc', 'row': 1, 'col1' : 2, 'col2': 3},

            {'name': 'benefits', 'type': 'CustomInput', 'label': 'Đặc quyền(nếu có)', 'row': 2, 'col1' : 0, 'col2': 1}
        ]

        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)

    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()
