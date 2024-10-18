import tkinter as tk
from tkinter import ttk
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.employee_role.employee_role_model import employee_role_model
from service.employee_role_service import EmployeeRoleService
from service.employee_service import EmployeeService
from service.role_service import RoleService

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
        form_popup = EmployeeRoleFormPopup(self, None)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.employee_role_service.getById(row_id)
        form_popup = EmployeeRoleFormPopup(self, data)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.employee_role_service.insert(data)
            self.treeView.loadData()

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.employee_role_service.update(data)
            self.treeView.loadData()
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.employee_role_service.delete(row_id)
            self.treeView.loadData()
class EmployeeRoleFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.geometry("600x120")
        self.title(parent.title_popup)
        self.parent = parent
        self.selected_employee_id = None
        self.selected_role_id = None

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

        label_employee = tk.Label(self, text="Tên nhân viên:")
        label_employee.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.employee_combobox = ttk.Combobox(self, width=30-4, state="readonly")
        self.employee_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.employee_combobox['values'] = [f"{emp[1]}" for emp in parent.data_employee]
        self.employee_combobox.bind("<<ComboboxSelected>>", self.on_employee_selected)
        self.employee_combobox.set('')


        label_role = tk.Label(self, text="Tên quyền:")
        label_role.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.role_combobox = ttk.Combobox(self, width=30-4, state="readonly")
        self.role_combobox.grid(row=0, column=3, padx=10, pady=10)
        self.role_combobox['values'] = [f"{emp[1]}" for emp in parent.data_role]
        self.role_combobox.bind("<<ComboboxSelected>>", self.on_role_selected)
        self.role_combobox.set('')

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            self.entry_id.insert(0, data[0])
            self.set_employee_combobox(data[1])
            self.set_role_combobox(data[2])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save)
        self.button_save.pack(side="right", padx=5)

    def save(self):
        employee_role_id = self.entry_id.get() if self.entry_id.get() is not None else None
        employee_role_input = employee_role_model(
            employee_role_id=employee_role_id,
            employee_id=self.selected_employee_id,
            role_id=self.selected_role_id
        )

        if employee_role_input.employee_role_id is None or employee_role_input.employee_role_id == "":
            self.parent.insert(employee_role_input)
            self.destroy()
        else:
            self.parent.update(employee_role_input)
            self.destroy()
        
    def on_employee_selected(self, event):
        selected_position_name = self.employee_combobox.get()
        self.selected_employee_id = None
        for pos in self.parent.data_employee:
            if pos[1] == selected_position_name:
                self.selected_employee_id = pos[0]
                break
    
    def set_employee_combobox(self, employee_id):
        self.selected_employee_id = employee_id
        for pos in self.parent.data_employee:
            if pos[0] == employee_id:
                self.employee_combobox.set(pos[1])  
                break

    def on_role_selected(self, event):
        selected_position_name = self.role_combobox.get()
        self.selected_role_id = None
        for pos in self.parent.data_role:
            if pos[1] == selected_position_name:
                self.selected_role_id = pos[0]
                break
    
    def set_role_combobox(self, role_id):
        self.selected_role_id = role_id
        for pos in self.parent.data_role:
            if pos[0] == role_id:
                self.role_combobox.set(pos[1])  
                break