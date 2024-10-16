import tkinter as tk
from tkinter import ttk
from ui.pages.BasePage import BasePage
from service.employee_service import EmployeeService
from models.employee.employee_model import employee_model
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
from helper.CustomTreeView import CustomTreeView

class Employee(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUẢN LÝ NHÂN SỰ", font=("Helvetica", 16))
        label.pack(pady=20, side="top", fill="x", expand=True)
        colums = [
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
                'key': 'Address',
                'name': 'Địa chỉ',
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
                'key': 'Action',
                'name': 'Hành động',
                'width': 100,
                'anchor': 'center'
            }
        ]
        

        #Get view
        self.frame_view = tk.Frame(self)
        self.frame_view.pack(padx=10, fill="both", expand=True)
        self.employee_service = EmployeeService()
        self.datas = self.employee_service.search()
        self.treeView = CustomTreeView(self.frame_view, self, self.datas, colums)

    def search(self):
        return ""
    
    def add(self):
        self.title_popup = "Thêm mới nhân viên"
        form_popup = EmployeeFormPopup(self, None)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập nhân viên"
        row_id = row_id + 1
        data = self.employee_service.getById(row_id)
        form_popup = EmployeeFormPopup(self, data)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            print(data)
            result = self.employee_service.insert(data)
            self.treeView.loadData()

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.employee_service.update(data)
            self.treeView.loadData()
    
    def delete(self, row_id):
        row_id = row_id + 1
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.employee_service.delete(row_id)
            self.treeView.loadData()

    
class EmployeeFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.geometry("680x20")
        self.title(parent.title_popup)
        self.parent = parent
        
        window_width = 680
        window_height = 280
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

        label_name = tk.Label(self, text="Họ và tên:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        label_date = tk.Label(self, text="Ngày sinh:")
        label_date.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.birth_day = DateEntry(self, width=30-4, background='drakblue', foreground='white', borderwidth=2, year=1990)
        self.birth_day.grid(row=0, column=3, padx=10, pady=10)

        label_gender = tk.Label(self, text="Giới tính:")
        label_gender.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.gender_combobox = ttk.Combobox(self, width=30-4, values=["Nam", "Nữ"], state="readonly")
        self.gender_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.gender_combobox.current(0)

        label_address = tk.Label(self, text="Địa chỉ:")
        label_address.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.entry_address = tk.Entry(self, width=30)
        self.entry_address.grid(row=1, column=3, padx=10, pady=10)

        label_phone_number = tk.Label(self, text="Số điện thoại:")
        label_phone_number.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_phone_number = tk.Entry(self, width=30)
        self.entry_phone_number.grid(row=2, column=1, padx=10, pady=10)

        label_email = tk.Label(self, text="Email:")
        label_email.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.entry_email = tk.Entry(self, width=30)
        self.entry_email.grid(row=2, column=3, padx=10, pady=10)

        label_position = tk.Label(self, text="Vị trí:")
        label_position.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.position_combobox = ttk.Combobox(self, width=30-4, values=["Nhân viên", "Quản lý"], state="readonly")
        self.position_combobox.grid(row=3, column=1, padx=10, pady=10)
        self.position_combobox.current(0)

        label_department = tk.Label(self, text="Phòng ban:")
        label_department.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.department_combobox = ttk.Combobox(self, width=30-4, values=["IT", "Nhân sự"], state="readonly")
        self.department_combobox.grid(row=3, column=3, padx=10, pady=10)
        self.position_combobox.current(0)

        label_start_date = tk.Label(self, text="Ngày bắt đầu:")
        label_start_date.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.start_date = DateEntry(self, width=30-4, background='drakblue', foreground='white', borderwidth=2, year=1990)
        self.start_date.grid(row=4, column=1, padx=10, pady=10)

        label_id_card_number = tk.Label(self, text="CCCD/CMND:")
        label_id_card_number.grid(row=4, column=2, padx=10, pady=10, sticky="e")
        self.entry_id_card_number = tk.Entry(self, width=30)
        self.entry_id_card_number.grid(row=4, column=3, padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.birth_day.set_date(data[2])
            self.gender_combobox.set("Nam")
            self.entry_address.insert(0, data[4])
            self.entry_phone_number.insert(0, data[5])
            self.entry_email.insert(0, data[6])
            self.position_combobox.set("Nhân viên")
            self.department_combobox.set("IT")
            self.start_date.set_date(data[9])
            self.entry_id_card_number.insert(0, data[10])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save_employee)
        self.button_save.pack(side="right", padx=5)

    def save_employee(self):
        gender_value = 1 if self.gender_combobox.get() == 'Nam' else 0
        employee_id = self.entry_id.get() if self.entry_id.get() is not None else None
        position = 1
        department = 1

        employee_input = employee_model(
            employee_id= employee_id,
            name = self.entry_name.get(),
            date_of_birth = self.birth_day.get_date().strftime('%Y-%m-%d'),
            gender = gender_value,
            address = self.entry_address.get(),
            phone_number = self.entry_phone_number.get(),
            email = self.entry_email.get(),
            position_id = position,
            department_id = department,
            start_date = self.start_date.get_date().strftime('%Y-%m-%d'),
            id_card_number = self.entry_id_card_number.get(),
            password='1'
        )


        
        if employee_input.employee_id is None or employee_input.employee_id == "":
            self.parent.insert(employee_input)
            self.destroy()
        else:
            self.parent.update(employee_input)
            self.destroy()


