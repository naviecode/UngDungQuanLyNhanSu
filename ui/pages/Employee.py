import tkinter as tk
from tkinter import messagebox
from ui.pages import BasePage
from service import EmployeeService, PositionService
from helper import CustomTreeView, FormPopup
from PIL import Image, ImageTk 

class Employee(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.position_service = PositionService()
        self.employee_service = EmployeeService()
        self.set_permission_button(btn_add_show=True, btn_export_show=False, btn_add_search=False)
        # self.set_background()

    def set_background(self):
        self.background_image = Image.open("./images/background/CloudBackground.png")
        self.background_image = self.background_image.resize((self.winfo_screenwidth() - 250, self.winfo_screenheight() - 100), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1) 

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
            self.show_loading()
            result = self.employee_service.insert(data)
            self.treeView.loadData()
            return True
        self.simulate_loading()
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            self.show_loading()
            result = self.employee_service.update(data)
            self.treeView.loadData()
            return True
        self.simulate_loading()
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            self.show_loading()
            result = self.employee_service.delete(row_id)
            self.treeView.loadData()
            return True
        self.simulate_loading()
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
                'key': 'Department',
                'name': 'Phòng ban',
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
            {'name': 'employee_id', 'type': 'ID', 'label': 'ID' , 'required': False, 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'name', 'type': 'CustomInput', 'label': 'Họ và tên' , 'required': True, 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'date_of_birth', 'type': 'CustomDate', 'label': 'Ngày sinh', 'required': False, 'row': 0, 'col1' : 2, 'col2': 3},

            {'name': 'gender', 'type': 'ComboboxCustom', 'label': 'Giới tính', 'required': True, 'values': [(1, 'Nam'), (0, 'Nữ')], 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'address', 'type': 'CustomInput', 'label': 'Địa chỉ' , 'required': False, 'row': 1, 'col1' : 2, 'col2': 3},

            {'name': 'phone_number', 'type': 'CustomInput', 'label': 'Số điện thoại' , 'required': False, 'row': 2, 'col1' : 0, 'col2': 1},
            {'name': 'email', 'type': 'CustomInput', 'label': 'Email' , 'required': False, 'row': 2, 'col1' : 2, 'col2': 3},

            {'name': 'position_id', 'type': 'ComboboxCustom', 'label': 'Vị trí', 'required': True, 'values': self.data_position, 'row': 3, 'col1' : 0, 'col2': 1},
            {'name': 'start_date', 'type': 'CustomDate', 'label': 'Ngày bắt đầu', 'required': True, 'row': 3, 'col1' : 2, 'col2': 3},

            {'name': 'id_card_number', 'type': 'CustomInput', 'label': 'CCCD/CMND' , 'required': True, 'row': 4, 'col1' : 0, 'col2': 1},
            {'name': 'username', 'type': 'CustomInput', 'label': 'Tên đăng nhập' , 'required': True, 'row': 4, 'col1' : 2, 'col2': 3},
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

        

