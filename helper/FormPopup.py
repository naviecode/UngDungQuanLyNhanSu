import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

class EmployeeFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        """
            data:
            model:
            width:
            height:
            title: 
        
        """
        self.geometry("640x300")
        self.title(parent.title_popup)
        self.parent = parent
        self.selected_position_id = None
        
        window_width = 640
        window_height = 300
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
        self.position_combobox = ttk.Combobox(self, width=30-4, state="readonly")
        self.position_combobox.grid(row=3, column=1, padx=10, pady=10)
        self.position_combobox['values'] = [f"{pos[1]}" for pos in parent.data_position]
        self.position_combobox.current(0)
        self.position_combobox.bind("<<ComboboxSelected>>", self.on_position_selected)

        label_start_date = tk.Label(self, text="Ngày bắt đầu:")
        label_start_date.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.start_date = DateEntry(self, width=30-4, background='drakblue', foreground='white', borderwidth=2, year=1990)
        self.start_date.grid(row=3, column=3, padx=10, pady=10)

        label_id_card_number = tk.Label(self, text="CCCD/CMND:")
        label_id_card_number.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_id_card_number = tk.Entry(self, width=30)
        self.entry_id_card_number.grid(row=4, column=1, padx=10, pady=10)

        label_end_date = tk.Label(self, text="Ngày kết thúc:")
        label_end_date.grid(row=4, column=2, padx=10, pady=10, sticky="e")
        self.end_date = DateEntry(self, width=30-4, background='drakblue', foreground='white', borderwidth=2)
        self.end_date.grid(row=4, column=3, padx=10, pady=10)

        label_username = tk.Label(self, text="Tên đăng nhập:")
        label_username.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.entry_username = tk.Entry(self, width=30)
        self.entry_username.grid(row=5, column=1, padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            gender_value = 'Nam' if data[3] else 'Nữ'
            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.birth_day.set_date(data[2])
            self.gender_combobox.set(gender_value)
            self.entry_address.insert(0, data[4])
            self.entry_phone_number.insert(0, data[5])
            self.entry_email.insert(0, data[6])
            self.set_position_combobox(data[7])
            self.start_date.set_date(data[8])
            self.entry_id_card_number.insert(0, data[9])
            self.end_date.set_date(data[10])
            self.entry_username.insert(0, data[11])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save_employee)
        self.button_save.pack(side="right", padx=5)

    def save_employee(self):
        gender_value = 1 if self.gender_combobox.get() == 'Nam' else 0
        employee_id = self.entry_id.get() if self.entry_id.get() is not None else None
        position = self.selected_position_id

        employee_input = employee_model(
            employee_id= employee_id,
            name = self.entry_name.get(),
            date_of_birth = self.birth_day.get_date().strftime('%Y-%m-%d'),
            gender = gender_value,
            address = self.entry_address.get(),
            phone_number = self.entry_phone_number.get(),
            email = self.entry_email.get(),
            position_id = position,
            start_date = self.start_date.get_date().strftime('%Y-%m-%d'),
            id_card_number = self.entry_id_card_number.get(),
            password='1',
            end_date=self.end_date.get_date().strftime('%Y-%m-%d'),
            username=self.entry_username.get()
        )

        if employee_input.employee_id is None or employee_input.employee_id == "":
            self.parent.insert(employee_input)
            self.destroy()
        else:
            self.parent.update(employee_input)
            self.destroy()
            
    def on_position_selected(self, event):
        selected_position_name = self.position_combobox.get()
        self.selected_position_id = None
        for pos in self.parent.data_position:
            if pos[1] == selected_position_name:
                self.selected_position_id = pos[0]
                break
    
    def set_position_combobox(self, position_id):
        self.selected_position_id = position_id
        for pos in self.parent.data_position:
            if pos[0] == position_id:
                self.position_combobox.set(pos[1])  
                break
