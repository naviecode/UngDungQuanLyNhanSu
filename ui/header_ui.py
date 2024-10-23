import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from service import EmployeeService
from helper import CustomInputText
import globals

class Header(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.employee_service = EmployeeService()
        self.userInfo = self.employee_service.getInfoUser(globals.current_user.employee_id)

        header = tk.Frame(self, bg="#0178bc", height=40)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        header_left = tk.Frame(header, width=250, bg="#0178bc")
        header_left.pack(side="left", fill="y")
        header_left.pack_propagate(False)   

        header_left_logo = tk.Label(header_left, text="QUẢN LÝ NHÂN SỰ", bg="#0178bc", fg="white",font=("Arial", 14), cursor="hand2")
        header_left_logo.pack(expand=True)
        header_left_logo.pack()

        header_right = tk.Frame(header, bg="#0178bc", width=250)
        header_right.pack(side="right", fill="y")
        header_right.pack_propagate(False)

        image_user = Image.open("./images/icons/user.png")
        resized_image_user = image_user.resize((25,25))
        self.image_user = ImageTk.PhotoImage(resized_image_user)


        button_image_user = tk.Button(header_right,
            image=self.image_user,
            relief="flat",
            bd=0, 
            highlightthickness=0, 
            bg="#0178bc",
            activebackground="#0178bc",
            cursor="hand2",
            command=self.show_popup_user
        )
        button_image_user.pack(side="right", padx=20)


    def show_popup_user(self):
        # Tạo cửa sổ popup
        popup = tk.Toplevel(self.master)
        x = (self.main_app.screen_width //2) - (300//2)
        y = (self.main_app.screen_height //2) - (180//2)
        popup.title("Thông tin người dùng")
        popup.geometry(f'{300}x{180}+{x}+{y}') # Kích thước popup
        popup.grab_set()
        # Nội dung trong popup
        label = tk.Label(popup, text="Thông tin người dùng", font=("Helvetica", 13))
        label.pack()

        frame = tk.Frame(popup)
        frame.pack(padx=10)
        tk.Label(frame, text=f"Họ tên: {self.userInfo["name"]}", font=("Helvetica", 11)).pack(fill="x",expand=True , anchor="w")
        tk.Label(frame, text=f"Vị trí: {self.userInfo["position_name"]}", font=("Helvetica", 11)).pack(fill="x",expand=True, anchor="w")
        tk.Label(frame, text=f"Email: {self.userInfo["email"]}", font=("Helvetica", 11)).pack(fill="x",expand=True, anchor="w")
        tk.Label(frame, text=f"Ngày bắt đầu: {self.userInfo["start_date"]}", font=("Helvetica", 11)).pack(fill="x",expand=True, anchor="w")

        # Nút Đóng
        frame_button = tk.Frame(frame)
        frame_button.pack(padx=10,fill="both", expand=True)

        tk.Button(frame_button, text="Đổi mật khẩu", command=self.show_popup_changePass).pack(side="left",padx=10)
        tk.Button(frame_button, text="Đăng xuất", command=self.logout).pack(side="left")

    def show_popup_changePass(self):
        self.popup_changepass = tk.Toplevel(self.master)
        x = (self.main_app.screen_width //2) - (300//2)
        y = (self.main_app.screen_height //2) - (140//2)
        self.popup_changepass.title("Đổi mật khẩu")
        self.popup_changepass.geometry(f'{300}x{140}+{x}+{y}') 
        self.popup_changepass.grab_set()

        tk.Label(self.popup_changepass, text=f"Mật khẩu cũ:", font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=10)
        self.input_passOld = CustomInputText(self.popup_changepass, "Mật khẩu cũ", show="*")
        self.input_passOld.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.popup_changepass, text=f"Mật khẩu mới:", font=("Helvetica", 11)).grid(row=1, column=0, padx=10, pady=10)
        self.input_passNew = CustomInputText(self.popup_changepass, "Mật khẩu mới", show="*")
        self.input_passNew.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.popup_changepass, text="Xác nhận", anchor="w", command=self.confirm_changePass).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.popup_changepass, text="Đóng", anchor="e", command=self.close_changePass).grid(row=2, column=1, padx=10, pady=10)

    def close_changePass(self):
        self.popup_changepass.destroy()
    
    def confirm_changePass(self):
        if not self.input_passOld.validate_input() or not self.input_passNew.validate_input(): return
        result = self.employee_service.changePassword(globals.current_user.employee_id,self.input_passOld.get_value(), self.input_passNew.get_value())
        if result > 0:
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công")
            self.popup_changepass.destroy()
        else:
            messagebox.showinfo("Thất bại", "Đổi mật khẩu thất bại")

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.main_app.logout()