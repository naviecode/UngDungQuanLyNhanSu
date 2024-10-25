import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import globals
from models import AttendanceModel
from service import AttendanceService
from ui.pages import Overview, Employee, Contract, License, Role, Timesheet, Department, Position, EmployeeRole
from helper import ButtonImage



class Navbar(tk.Frame):
    def __init__(self, parent, frames):
        super().__init__(parent)

        self.attendance_service = AttendanceService()

       # Set the size of the navigation frame
        nav_width = 250
        nav_height = 600  # Adjust this based on your layout

        # Load your background image and resize it to fit the navigation frame
        navigation_bg_img = Image.open("./images/background/VintageSideBar.png")  # Path to your uploaded image
        resized_nav_bg_img = navigation_bg_img.resize((nav_width, nav_height), Image.Resampling.LANCZOS)  # Corrected constant

        self.navigation_bg_photo = ImageTk.PhotoImage(resized_nav_bg_img)

        # Navigation Frame with resized background image
        navigation = tk.Frame(self, width=nav_width, height=nav_height)
        navigation.pack(side="left", fill="y")
        navigation.pack_propagate(False)

        # Set background image for the navigation frame
        navigation_background_label = tk.Label(navigation, image=self.navigation_bg_photo)
        navigation_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # User Info Section
        nav_user = tk.Frame(navigation, bg="yellow", height=140)
        nav_user.pack(fill="x")
        nav_user.pack_propagate(False)   
        nav_user_background_img = Image.open("./images/background/nav_user_background_2.jpg")
        resized_nav_user_background_img = nav_user_background_img.resize((280,160), Image.Resampling.LANCZOS)
        self.nav_user_background_photo = ImageTk.PhotoImage(resized_nav_user_background_img)
        nav_user_background_label = tk.Label(nav_user, image=self.nav_user_background_photo)
        nav_user_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        nav_user_image = Image.open("./images/icons/fingerprint.png")
        resized_nav_user_image = nav_user_image.resize((40, 40))
        self.nav_user_image = ImageTk.PhotoImage(resized_nav_user_image)
        nav_user_image_button = tk.Button(nav_user, image=self.nav_user_image, bg="#0178bc", cursor="hand2", command=self.attendance, bd=0)
        nav_user_image_button.pack(pady=20)

        label = tk.Label(nav_user, text=globals.current_user.username, font=("Arial", 16), bg="#0178bc", fg="white")
        label.pack()

        # Navigation buttons
        nav_main = tk.Frame(navigation, height=420)  # No bg="transparent" here
        nav_main.pack(fill="x", padx=10, pady=10)
        nav_main.pack_propagate(False)
        self.buttons = []
        self.frames = frames
        
        self.button_main = ButtonImage(parent=nav_main, image_path="./images/icons/overview.png", text="Tổng quan", command=lambda: self.change_color(self.button_main, Overview), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=True)
        self.button_main.pack()
        self.buttons.append(self.button_main)

        self.button_dep = ButtonImage(parent=nav_main, image_path="./images/icons/department.png", text="Phòng ban", command=lambda: self.change_color(self.button_dep, Department), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_dep.pack()
        self.buttons.append(self.button_dep)

        self.button_position = ButtonImage(parent=nav_main, image_path="./images/icons/position.png", text="Chức vụ", command=lambda: self.change_color(self.button_position, Position), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_position.pack()
        self.buttons.append(self.button_position)

        self.button_employee = ButtonImage(parent=nav_main, image_path="./images/icons/user_menu.png", text="Nhân viên", command=lambda: self.change_color(self.button_employee, Employee), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_employee.pack()
        self.buttons.append(self.button_employee)

        self.button_timesheet = ButtonImage(parent=nav_main, image_path="./images/icons/timesheet.png", text="Bảng chấm công", command=lambda: self.change_color(self.button_timesheet, Timesheet), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_timesheet.pack()
        self.buttons.append(self.button_timesheet)

        self.button_license = ButtonImage(parent=nav_main, image_path="./images/icons/license.png", text="Đơn từ", command=lambda: self.change_color(self.button_license, License), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_license.pack()
        self.buttons.append(self.button_license)

        self.button_contract = ButtonImage(parent=nav_main, image_path="./images/icons/contract.png", text="Hợp đồng", command=lambda: self.change_color(self.button_contract, Contract), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_contract.pack()
        self.buttons.append(self.button_contract)

        self.button_employee_role = ButtonImage(parent=nav_main, image_path="./images/icons/role_employee.png", text="Phân quyền", command=lambda: self.change_color(self.button_employee_role, EmployeeRole), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_employee_role.pack()
        self.buttons.append(self.button_employee_role)

        self.button_role = ButtonImage(parent=nav_main, image_path="./images/icons/permission.png", text="Quyền", command=lambda: self.change_color(self.button_role, Role), width=250, activeBg="#0178bc", activefg="white", bg="white", fg="black", active=False)
        self.button_role.pack()
        self.buttons.append(self.button_role)

        self.set_permission()

    def set_permission(self):
        if globals.current_user.role_id == 1:
            """ADMIN"""
            self.button_main.pack()
            self.button_dep.pack()
            self.button_position.pack()
            self.button_employee.pack()
            self.button_timesheet.pack()
            self.button_license.pack()
            self.button_contract.pack()
            self.button_employee_role.pack()
            self.button_role.pack()
        elif globals.current_user.role_id == 3:
            """MANAGER"""
            self.button_main.pack()
            self.button_dep.pack()
            self.button_position.pack()
            self.button_employee.pack()
            self.button_timesheet.pack()
            self.button_license.pack()
            self.button_contract.pack_forget()
            self.button_employee_role.pack_forget()
            self.button_role.pack_forget()
        else:
            """USER"""
            self.button_main.pack()
            self.button_dep.pack_forget()
            self.button_position.pack_forget()
            self.button_employee.pack_forget()
            self.button_timesheet.pack()
            self.button_license.pack()
            self.button_contract.pack_forget()
            self.button_employee_role.pack_forget()
            self.button_role.pack_forget()
    
    def change_color(self, button, page):
        # Đặt màu cho các button
        for b in self.buttons:
            b.config(bg="white", fg="black")
        button.config(bg="#0178bc", fg="white")
        self.show_page(page)

    def show_page(self, page):
        frame = self.frames[page]
        frame.show_loading()
        frame.clear_frame_data()
        frame.tkraise()
        frame.on_show_frame()
        frame.simulate_loading()
        

    def initNav(self, content, parent):
        for F in (Overview, Department, Position, Employee, Contract, Role, Timesheet, License, EmployeeRole):
            frame = F(content, parent)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def attendance(self):
        response = messagebox.askyesno("Chấm công", "Bạn có muốn thực hiện chấm công?")
        if response:
            # Lấy thời gian hiện tại
            now = datetime.now()
            current_time = now.time()

            # Định nghĩa các mốc thời gian
            checkin_end_time = datetime.strptime('09:30', '%H:%M').time()
            checkout_start_time = datetime.strptime('15:30', '%H:%M').time()

            if current_time <= datetime.strptime('12:00', '%H:%M').time():
                data = AttendanceModel(
                    employee_id=globals.current_user.employee_id,
                    check_in = datetime.now(),
                    status = 'Present',
                    work_date = datetime.now().date(),
                    remarks = "No"
                )
            
            if current_time > datetime.strptime('12:00', '%H:%M').time():
                data = AttendanceModel(
                    employee_id=globals.current_user.employee_id,
                    check_out = datetime.now(),
                    status = 'Present',
                    work_date = datetime.now().date(),
                    remarks = "No"
                )
            self.attendance_service.handle(data)
            messagebox.showinfo("Thông báo", "Xin cảm ơn")

    
