import tkinter as tk
from tkinter import ttk
from ui.pages.BasePage import BasePage
from service.employee_service import EmployeeService
from models.employee.employee_model import employee_model
from helper.ButtonImage import ButtonImage
from tkcalendar import DateEntry
from datetime import datetime

class Employee(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUẢN LÝ NHÂN SỰ", font=("Helvetica", 16))
        label.pack(pady=20, side="top", fill="x", expand=True)

        # Số mục trên mỗi trang
        self.items_per_page = 2
        self.current_page = 0

        self.employee_service = EmployeeService(self.db)
        self.datas = self.employee_service.search()
        self.buttons = []
        self.get_treeView(datas=self.datas)

        #Load trang đầu
        self.loadData()

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
        result = self.employee_service.insert(data)
        self.loadData()
    
    def update(self, data):
        print(data.employee_id)
        result = self.employee_service.update(data)
        self.loadData()
    
    def delete(self, row_id):
        row_id = row_id + 1
        result = self.employee_service.delete(row_id)
        self.loadData()
    
    def loadData(self):
        for child in self.frame_view.tree.get_children():
            self.frame_view.tree.delete(child)

        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        
        self.data_reload = self.employee_service.search()

        # Lấy dữ liệu cho trang hiện tại
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data_reload[start:end]

        for employee in page_data:
            self.frame_view.tree.insert('', tk.END, values=employee)
        
        self.after(100, self.get_button_view)

        # Cập nhật trạng thái nút
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end < len(self.data_reload) else tk.DISABLED)

        


    def get_treeView(self, datas):
        self.frame_view = tk.Frame(self)
        self.frame_view.pack(padx=10, fill="both", expand=True)

        self.frame_view.tree = ttk.Treeview(self.frame_view, columns=('ID', 'Name', 'Address','Gender','Position','Department','Action'), show='headings')
        self.frame_view.tree.heading('ID', text='ID')
        self.frame_view.tree.heading('Name', text='Họ tên')
        self.frame_view.tree.heading('Address', text='Địa chỉ')
        self.frame_view.tree.heading('Gender', text='Giới tính')
        self.frame_view.tree.heading('Position', text='Chức vụ')
        self.frame_view.tree.heading('Department', text='Phòng ban')
        self.frame_view.tree.heading('Action', text='Hành động')

        # Kích thước cho các cột
        self.frame_view.tree.column('ID', width=10, anchor="center")
        self.frame_view.tree.column('Name', width=150)
        self.frame_view.tree.column('Address', width=150)
        self.frame_view.tree.column('Gender', width=20, anchor="center")
        self.frame_view.tree.column('Position', width=80)
        self.frame_view.tree.column('Department', width=80)
        self.frame_view.tree.column('Action', width=100, anchor="e")

        self.frame_view.tree.grid(row=0, column=0, sticky='nsew')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_view, orient=tk.VERTICAL, command=self.frame_view.tree.yview)
        self.frame_view.tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(self.frame_view, orient=tk.HORIZONTAL, command=self.frame_view.tree.xview)
        self.frame_view.tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        # Tùy chỉnh việc mở rộng
        self.frame_view.grid_rowconfigure(0, weight=1)
        self.frame_view.grid_columnconfigure(0, weight=1)

        for employee in datas:
            self.frame_view.tree.insert('', tk.END, values=employee)
        
        self.after(100, self.get_button_view)

        # Tạo nút trước và tiếp theo
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="both", expand=True, pady=10)

        self.next_button = tk.Button(self.button_frame, text="Tiếp theo", command=self.next_page, width=10)
        self.next_button.pack(padx=10, side="right")

        self.prev_button = tk.Button(self.button_frame, text="Trước", command=self.prev_page, width=10)
        self.prev_button.pack(padx=20, side="right")


    def get_button_view(self):
        # Tạo button trong Treeview
        for child in self.frame_view.tree.get_children():
            row_id = self.frame_view.tree.index(child)
            x0, y0, width, height = self.frame_view.tree.bbox(child, column=6)  
            button_delete = ButtonImage(self.frame_view.tree, "./images/icons/delete.png", "", command=lambda id=row_id: self.delete(id),width=50, height=30, bg="white", fg="white")
            button_update = ButtonImage(self.frame_view.tree, "./images/icons/edit.png", "", command=lambda id=row_id: self.edit(id),width=50, height=30, bg="white", fg="white")
            
            button_update.place(x=x0 + width - 30, y=y0 + 2, width=30, height=20)
            button_delete.place(x=x0 + width - 30 - 30, y=y0 + 2, width=30, height=20)

            self.buttons.append(button_update)
            self.buttons.append(button_delete)



    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.datas):
            self.current_page += 1
            self.loadData()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.loadData()

    
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
            convert_birth_day = datetime.strptime(data[2], '%Y-%m-%d').date()
            convert_start_date = datetime.strptime(data[9], '%Y-%m-%d').date()

            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.birth_day.set_date(convert_birth_day)
            self.gender_combobox.set("Nam")
            self.entry_address.insert(0, data[4])
            self.entry_phone_number.insert(0, data[5])
            self.entry_email.insert(0, data[6])
            self.position_combobox.set("Nhân viên")
            self.department_combobox.set("IT")
            self.start_date.set_date(convert_start_date)
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
            date_of_birth = self.birth_day.get_date(),
            gender = gender_value,
            address = self.entry_address.get(),
            phone_number = self.entry_phone_number.get(),
            email = self.entry_email.get(),
            position_id = position,
            department_id = department,
            start_date = self.start_date.get_date(),
            id_card_number = self.entry_id_card_number.get(),
            password='1'
        )

        
        if employee_input.employee_id is None or employee_input.employee_id == "":
            self.parent.insert(employee_input)
            self.destroy()
        else:
            self.parent.update(employee_input)
            self.destroy()


