import tkinter as tk
from tkinter import ttk
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.position.position_model import position_model
from service.position_service import PositionService
from service.department_service import DepartMentService
from datetime import datetime


class Position(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUẢN LÝ CHỨC VỤ", font=("Helvetica", 16))
        label.pack(pady=20)
        self.department_service = DepartMentService()
        self.data_department = self.department_service.getCombobox()
        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên chức vụ',
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
                'key' : 'CreateDate',
                'name' : 'Ngày tạo',
                'width' : 100,
                'anchor': 'center'
            },
            {
                'key': 'Department_id',
                'name': 'Phòng ban',
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
        self.position_service = PositionService()
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, 5)

    def search(self):
        rows = self.position_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = PositionFormPopup(self, None)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        print(row_id)
        data = self.position_service.getById(row_id)
        form_popup = PositionFormPopup(self, data)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.position_service.insert(data)
            self.treeView.loadData()

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.position_service.update(data)
            self.treeView.loadData()
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.position_service.delete(row_id)
            self.treeView.loadData()

class PositionFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.geometry("600x170")
        self.title(parent.title_popup)
        self.parent = parent
        self.selected_deparment_id = None

        window_width = 600
        window_height = 170
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

        label_name = tk.Label(self, text="Tên chức vụ:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)


        label_desc = tk.Label(self, text="Mô tả:")
        label_desc.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_desc = tk.Entry(self, width=30)
        self.entry_desc.grid(row=0, column=3, padx=10, pady=10)

        label_department = tk.Label(self, text="Phòng ban:")
        label_department.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.department_combobox = ttk.Combobox(self, width=30-4, state="readonly")
        self.department_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.department_combobox['values'] = [f"{dep[1]}" for dep in parent.data_department]
        self.department_combobox.current(0)
        self.department_combobox.bind("<<ComboboxSelected>>", self.on_department_selected)


        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.entry_desc.insert(0, data[2])
            self.set_department_combobox(data[3])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save)
        self.button_save.pack(side="right", padx=5)

    def save(self):
        position_id = self.entry_id.get() if self.entry_id.get() is not None else None
        position_input = position_model(
            position_id=position_id,
            position_name=self.entry_name.get(),
            description=self.entry_desc.get(),
            create_date= datetime.now().date(),
            department_id= self.selected_deparment_id
        )

        if position_input.position_id is None or position_input.position_id == "":
            self.parent.insert(position_input)
            self.destroy()
        else:
            self.parent.update(position_input)
            self.destroy()

    def on_department_selected(self, event):
        selected_department_name = self.department_combobox.get()
        self.selected_deparment_id = None
        for pos in self.parent.data_department:
            if pos[1] == selected_department_name:
                self.selected_deparment_id = pos[0]
                break
    
    def set_department_combobox(self, department_id):
        self.selected_deparment_id = department_id
        for pos in self.parent.data_department:
            if pos[0] == department_id:
                self.department_combobox.set(pos[1])  
                break