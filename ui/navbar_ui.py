import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
from models.attendance.attendance_model import attendance_model
from service.attendance_service import AttendanceService
from ui.pages.Overview import Overview
from ui.pages.Employee import Employee
from ui.pages.Contract import Contract
from ui.pages.License import License
from ui.pages.Role import Role
from ui.pages.Timesheet import Timesheet
from ui.pages.Department import Department
from ui.pages.Position import Position
from ui.pages.EmployeeRole import EmployeeRole
import globals




class Navbar(tk.Frame):
    def __init__(self, parent, frames):
        super().__init__(parent)
        self.attendance_service = AttendanceService()
        #Navigation
        navigation = tk.Frame(self, bg="white", width=250)
        navigation.pack(side="left", fill="y")
        navigation.pack_propagate(False)   

        nav_user = tk.Frame(navigation, bg="yellow", height=140)
        nav_user.pack(fill="x")
        nav_user.pack_propagate(False)   
        nav_user_background_img = Image.open("./images/background/nav_user_background.jpg")
        self.nav_user_background_photo = ImageTk.PhotoImage(nav_user_background_img)
        nav_user_background_label = tk.Label(nav_user, image=self.nav_user_background_photo)
        nav_user_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        nav_user_image = Image.open("./images/icons/fingerprint.png")
        resized_nav_user_image = nav_user_image.resize((40,40))
        self.nav_user_image = ImageTk.PhotoImage(resized_nav_user_image)
        nav_user_image_button = tk.Button(nav_user, image=self.nav_user_image, bg="#0178bc", cursor="hand2", command=self.attendance, bd=0)
        nav_user_image_button.pack(pady=20)

        label = tk.Label(nav_user, text= globals.current_user.username, font=("Arial", 16), bg="#0178bc", fg="white")
        label.pack()

        nav_main = tk.Frame(navigation, bg="white", height=420)
        nav_main.pack(fill="x", padx=10, pady=10)
        nav_main.pack_propagate(False)  

        self.buttons = []
        self.frames = frames
        
        self.button_main = self.CreateButtonNav(nav_main, "Tổng quan", "./images/icons/overview.png",True,lambda: self.change_color(self.button_main, Overview))
        self.button_main.pack()
        self.buttons.append(self.button_main)

        self.button_dep = self.CreateButtonNav(nav_main, "Phòng ban", "./images/icons/department.png",False,lambda: self.change_color(self.button_dep, Department))
        self.button_dep.pack()
        self.buttons.append(self.button_dep)

        self.button_position = self.CreateButtonNav(nav_main, "Chức vụ", "./images/icons/position.png",False,lambda: self.change_color(self.button_position, Position))
        self.button_position.pack()
        self.buttons.append(self.button_position)
        
        self.button_employee = self.CreateButtonNav(nav_main, "Nhân viên", "./images/icons/user_menu.png",False,lambda: self.change_color(self.button_employee, Employee))
        self.button_employee.pack()
        self.buttons.append(self.button_employee)

        self.button_timesheet = self.CreateButtonNav(nav_main,"Bảng chấm công", "./images/icons/timesheet.png",False,lambda: self.change_color(self.button_timesheet, Timesheet))
        self.button_timesheet.pack()
        self.buttons.append(self.button_timesheet)

        self.button_license = self.CreateButtonNav(nav_main,"Đơn từ", "./images/icons/license.png",False,lambda: self.change_color(self.button_license, License))
        self.button_license.pack()
        self.buttons.append(self.button_license)

        self.button_contract = self.CreateButtonNav(nav_main,"Hợp đồng", "./images/icons/contract.png",False,lambda: self.change_color(self.button_contract, Contract))
        self.button_contract.pack()
        self.buttons.append(self.button_contract)

        self.button_employee_role = self.CreateButtonNav(nav_main,"Phân quyền", "./images/icons/role_employee.png",False,lambda: self.change_color(self.button_employee_role, EmployeeRole))
        self.button_employee_role.pack()
        self.buttons.append(self.button_employee_role)

        self.button_role = self.CreateButtonNav(nav_main,"Quyền", "./images/icons/permission.png",False,lambda: self.change_color(self.button_role, Role))
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
            
        
    def CreateButtonNav(self, parent, text, image_path,active, command):
        button_image = Image.open(image_path)
        resized_button_image = button_image.resize((20,20))
        self.button_image_photo = ImageTk.PhotoImage(resized_button_image)
        bg_button_active = "#0178bc" if active else "white"
        fg_button_active = "white" if active else "black"
        button = tk.Button(parent,
            image= self.button_image_photo,
            compound="left",
            text=text,font=(11),
            width=250,
            relief="flat",
            activebackground="#0178bc",
            activeforeground="white",
            cursor="hand2",
            highlightthickness=0,
            bd=0,
            pady=8,
            padx=10,
            bg=bg_button_active, 
            fg=fg_button_active,
            anchor="w",
            command= command
        )
        button.image = self.button_image_photo 
        return button
    
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
            data = attendance_model(
                employee_id=globals.current_user.employee_id,
                check_in = datetime.now(),
                check_out = datetime.now(),
                status = 'Present',
                work_date = datetime.now().date(),
                remarks = "No"
            )
            self.attendance_service.handle(data)
            messagebox.showinfo("Thông báo", "Xin cảm ơn")

    
