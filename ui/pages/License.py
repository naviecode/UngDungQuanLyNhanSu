import tkinter as tk
from tkinter import messagebox
from ui.pages import BasePage
from service import LicenseService, EmployeeService
from helper import FormPopup, CustomTreeView
import globals
from PIL import Image, ImageTk 

class License(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.employee_service = EmployeeService()
        self.license_service = LicenseService()
        self.set_permission_button(btn_add_show=True, btn_export_show=False)
        # set background
        self.set_background()

    def set_background(self):
        self.background_image = Image.open("./images/background/CloudBackground.png")
        self.background_image = self.background_image.resize((self.winfo_screenwidth() - 250, self.winfo_screenheight() - 100), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1) 

    def search(self):
        self.filters_license = {'employee_id': globals.current_user.employee_id}
        if globals.current_user.role_id == 2:
            rows = self.license_service.search(self.filters_license)
        else:
            rows = self.license_service.search(None)
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
   
        self.status_license =  [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected') ]
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
                'name': 'Trạng thái',
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
        self.datas = self.license_service.search()
        if globals.current_user.role_id == 2:
            self.employee_data = self.employee_service.getCombox({'employee_id': globals.current_user.employee_id})
            self.fields = [
                {'name': 'request_id', 'type': 'ID', 'label': 'ID' , 'required': False, 'row': 0, 'col1' : 1, 'col2': 2},

                {'name': 'employee_id', 'type': 'ComboboxCustom', 'label': 'Nhân viên' , 'required': True, 'values': self.employee_data, 'row': 0, 'col1' : 0, 'col2': 1},
                {'name': 'reason', 'type': 'CustomInput', 'label': 'Lý do', 'required': True, 'row': 0, 'col1' : 2, 'col2': 3},

                {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu', 'required': True, 'row': 1, 'col1' : 0, 'col2': 1},
                {'name': 'end_date', 'type': 'CustomDate', 'label': 'Ngày kết thúc' , 'required': True, 'row': 1, 'col1' : 2, 'col2': 3},
            ]
            
        else:
            self.employee_data = self.employee_service.getCombox(None)
            self.fields = [
                {'name': 'request_id', 'type': 'ID', 'label': 'ID' , 'required': False, 'row': 0, 'col1' : 1, 'col2': 2},

                {'name': 'employee_id', 'type': 'ComboboxCustom', 'label': 'Nhân viên' , 'required': True,'values': self.employee_data, 'row': 0, 'col1' : 0, 'col2': 1},
                {'name': 'reason', 'type': 'CustomInput', 'label': 'Lý do', 'required': True, 'row': 0, 'col1' : 2, 'col2': 3},

                {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu', 'required': True, 'row': 1, 'col1' : 0, 'col2': 1},
                {'name': 'end_date', 'type': 'CustomDate', 'label': 'Ngày kết thúc' , 'required': True, 'row': 1, 'col1' : 2, 'col2': 3},

                {'name': 'status', 'type': 'ComboboxCustom', 'label': 'Trạng thái', 'required': True,'values': self.status_license, 'row': 2, 'col1' : 0, 'col2': 1},
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