import tkinter as tk
from tkinter import ttk
from ui.pages.BasePage import BasePage
from service.employee_service import EmployeeService
from models.employee.employee_model import employee_model
class Employee(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        label = tk.Label(self, text="QUẢN LÝ NHÂN SỰ", font=("Helvetica", 16))
        label.pack(pady=20, side="top", fill="x", expand=True)

        frame_view = tk.Frame(self, bg="red")
        frame_view.pack(padx=10, fill="both", expand=True)

        frame_view.tree = ttk.Treeview(frame_view, columns=('ID', 'Name', 'Address', 'Position','Action'), show='headings')
        frame_view.tree.heading('ID', text='ID')
        frame_view.tree.heading('Name', text='Họ tên')
        frame_view.tree.heading('Address', text='Địa chỉ')
        frame_view.tree.heading('Position', text='Chức vụ')
        frame_view.tree.heading('Action', text='Hành động')

        # Kích thước cho các cột
        frame_view.tree.column('ID', width=20, anchor="center")
        frame_view.tree.column('Name', width=150)
        frame_view.tree.column('Address', width=150)
        frame_view.tree.column('Position', width=80)
        frame_view.tree.column('Action', width=100)

        frame_view.tree.grid(row=0, column=0, sticky='nsew')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(frame_view, orient=tk.VERTICAL, command=frame_view.tree.yview)
        frame_view.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Tùy chỉnh việc mở rộng
        frame_view.grid_rowconfigure(0, weight=1)
        frame_view.grid_columnconfigure(0, weight=1)

        employees = [
            (1, 'Nguyen Van A', 'HCM', 'Manager',''),
            (2, 'Tran Thi B', 'HN', 'Developer'),
            (3, 'Le Van C', 'Da Nang', 'Designer'),
            (3, 'Le Van C', 'Da Nang', 'Designer'),
        ]

        for employee in employees:
            frame_view.tree.insert('', tk.END, values=employee)


        frame_view.update()
        

        # Tạo button trong Treeview
        for child in frame_view.tree.get_children():
            row_id = frame_view.tree.index(child)
            print(row_id, child, frame_view.tree.bbox(child, column="Name"))
            # x0, y0, width, height = frame_view.tree.bbox(child, column=4)  # Vị trí cột Action

            # # Tạo Button tại vị trí đã tính toán
            # button = tk.Button(frame_view.tree, text="Action", command=lambda id=row_id: self.button_action(id))
            # button.place(x=x0 + 10, y=y0 + 2, width=80, height=20)

    def button_action(self, row_id):
        print(f"Button in row {row_id+1} clicked!")

    def add(self):
        print("Thêm mới nhân viên")
    
    def edit(self):
        print("Điều chỉnh")
    
    def delete(self):
        print("Xóa nhân viên")

    def show_popup(self):
        form_popup = EmployeeFormPopup(self, self.db)

class EmployeeFormPopup(tk.Toplevel):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.geometry("500x300")
        self.title("Thêm mới nhân viên")
        self.db = database
        self.employee_service = EmployeeService(database)

        window_width = 500
        window_height = 300
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        #Căn giữa popup
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.grab_set()

        self.label_name = tk.Label(self, text="Họ và tên:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_date = tk.Label(self, text="Ngày sinh:")
        self.label_date.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_date = tk.Entry(self)
        self.entry_date.grid(row=0, column=3, padx=10, pady=10)

        self.label_gender = tk.Label(self, text="Giới tính:")
        self.label_gender.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_gender = tk.Entry(self)
        self.entry_gender.grid(row=1, column=1, padx=10, pady=10)

        self.label_address = tk.Label(self, text="Địa chỉ:")
        self.label_address.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.entry_address = tk.Entry(self)
        self.entry_address.grid(row=1, column=3, padx=10, pady=10)

        self.label_phone_number = tk.Label(self, text="Số điện thoại:")
        self.label_phone_number.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_phone_number = tk.Entry(self)
        self.entry_phone_number.grid(row=2, column=1, padx=10, pady=10)

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=2, column=3, padx=10, pady=10)

        self.label_position = tk.Label(self, text="Vị trí:")
        self.label_position.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_position = tk.Entry(self)
        self.entry_position.grid(row=3, column=1, padx=10, pady=10)

        self.label_department = tk.Label(self, text="Phòng ban:")
        self.label_department.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.entry_department = tk.Entry(self)
        self.entry_department.grid(row=3, column=3, padx=10, pady=10)

        self.label_start_date = tk.Label(self, text="Ngày bắt đầu:")
        self.label_start_date.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_start_date = tk.Entry(self)
        self.entry_start_date.grid(row=4, column=1, padx=10, pady=10)

        self.label_id_card_number = tk.Label(self, text="CCCD/CMND:")
        self.label_id_card_number.grid(row=4, column=2, padx=10, pady=10, sticky="e")
        self.entry_id_card_number = tk.Entry(self)
        self.entry_id_card_number.grid(row=4, column=3, padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save_employee)
        self.button_save.pack(side="right", padx=5)

    def save_employee(self):
        new_employee = employee_model(None,
            self.entry_name.get(),
            self.entry_address.get()
        )
        self.insert_employee(new_employee)
        # if new_employee.employee_id is None or new_employee.employee_id == "":
        #     self.insert_employee(new_employee)
        # else:
        #     self.update_employee(new_employee)

    
    def insert_employee(self, input):
        result = self.employee_service.insert(input)
        return ""
        
    def update_employee(self):
        return ""
    def delete_employee(self):
        return ""
    def search_employee(self):
        data = self.employee_service.search()
        return data    

