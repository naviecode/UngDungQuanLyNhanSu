import tkinter as tk
from tkinter import messagebox
from helper import CustomTreeView, FormPopup
from ui.pages import BasePage
from service import DepartMentService, EmployeeService
from PIL import Image, ImageTk 


class Department(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.employee_service = EmployeeService()
        self.department_service = DepartMentService()
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
        rows = self.department_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=170)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.department_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=170)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.department_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.department_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.department_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False
    
    def on_show_frame(self):
        label = tk.Label(self, text="QUẢN LÝ PHÒNG BAN", font=("Helvetica", 16))
        label.pack(pady=20)
        self.data_employee = self.employee_service.getCombox()
        self.datas = self.search()
        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên phòng ban',
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
                'key': 'Location',
                'name': 'Địa điểm',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key' : 'CreateDate',
                'name' : 'Ngày tạo',
                'width' : 100,
                'anchor': 'center'
            },
            {
                'key': 'Manager_id',
                'name': 'Người quản lý',
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
            {'name': 'department_id', 'type': 'ID', 'label': 'ID' , 'required': False, 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'department_name', 'type': 'CustomInput', 'label': 'Tên phòng ban' , 'required': True, 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'location', 'type': 'CustomInput', 'label': 'Địa điểm', 'row': 0, 'required': False, 'col1' : 2, 'col2': 3},

            {'name': 'description', 'type': 'CustomInput', 'label': 'Mô tả', 'required': False, 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'manager_id', 'type': 'ComboboxCustom', 'label': 'Người quản lý', 'required': True, 'values': self.data_employee , 'row': 1, 'col1' : 2, 'col2': 3},
        ]


        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)

    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()
