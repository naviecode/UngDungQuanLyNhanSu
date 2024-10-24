import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from ui.pages import BasePage
from service import OverviewService
import globals

class Overview(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.overview_service = OverviewService()
        self.set_permission_button(btn_add_show=False, btn_export_show=False)

    def create_pie_char(self, frame, hover_label, data = None, title = None, title_hover = None):
        data_names = []
        data_values = []
        colors = []
        explodes = []
        for value in data:
            if value[1] != 0:
                data_names.append(value[0])
                data_values.append(value[1])
        length_arr = len(data_names)
        for _ in range(length_arr):
            color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            colors.append(color)
        for _ in range(length_arr):
            explodes.append(0.05)
        
        fig, ax = plt.subplots(figsize=(4, 4))

        wedges, texts, autotexts = ax.pie(
            data_values, labels=data_names, colors=colors, autopct='%1.1f%%', startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 3},
            pctdistance=0.85, 
            explode=explodes
        )
        
        # Thêm viền trắng ở giữa
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title(f'{title}', fontsize=13, weight='bold')

        # Function để xử lý hover
        def on_hover(event):
            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    if wedge.contains_point([event.x, event.y]):
                        hover_label.config(text=f"{title_hover}: {data_names[i]}")
                        return
                hover_label.config(text="")  # Không hover vào phần nào thì label trống

        # Thêm sự kiện hover vào figure
        fig.canvas.mpl_connect('motion_notify_event', on_hover)

        # Chuyển figure thành canvas để hiển thị trong Tkinter
        chart = FigureCanvasTkAgg(fig, master=frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_bar_chart(self, frame, title = None, title_2 = None, title_3 = None, data = None):
        dataNames = []
        dataValues = []
        colors = []
        for value in data:
            if value[1] != 0:
                dataNames.append(value[1])
                dataValues.append(int(value[2]))
        length_arr = len(dataNames)
        for _ in range(length_arr):
            color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            colors.append(color)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Vẽ biểu đồ cột
        ax.bar(dataNames, dataValues, color=colors)
        ax.set_title('Số lần đi trễ trung bình trong tháng của các phòng ban', fontsize=14, weight='bold')
        ax.set_ylabel('Số lần đi trễ')
        ax.set_xlabel('Phòng ban')

        # Chuyển figure thành canvas để hiển thị trong Tkinter
        chart = FigureCanvasTkAgg(fig, master=frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_bar_char_employee(self, frame, data=None):
        late_minutes = []
        now = datetime.now()
        first_day = now.replace(day=1)
        if now.month == 12:
            last_day = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day = now.replace(month=now.month + 1, day=1) - timedelta(days=1)
        for dateValue in pd.date_range(start=first_day, end=last_day):
            if(dateValue.strftime("%Y-%m-%d") in [item[1].strftime("%Y-%m-%d") for item in data]):
                for dataLateMin in data:
                    if dateValue.strftime("%Y-%m-%d") == dataLateMin[1].strftime("%Y-%m-%d"):
                        late_minutes.append(dataLateMin[2])
            else:
                late_minutes.append(0)
        data = {
            'date': pd.date_range(start=first_day, end=last_day),
            'late_minutes': late_minutes
        }
        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)

        # Vẽ biểu đồ cột (bar chart)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['date'], df['late_minutes'], color='skyblue')

        # Thêm tiêu đề và nhãn
        ax.set_title('Số phút đi trễ trung bình của nhân viên mỗi ngày trong tháng', fontsize=16)
        ax.set_xlabel('Ngày', fontsize=12)
        ax.set_ylabel('Số phút đi trễ', fontsize=12)

        # Hiển thị giá trị trên từng cột
        for i, txt in enumerate(df['late_minutes']):
            ax.text(df['date'][i], df['late_minutes'][i] + 0.5, str(txt), ha='center')

        # Xoay nhãn ngày để dễ đọc
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # Hiển thị biểu đồ trên frame
        canvas = FigureCanvasTkAgg(fig, master=frame)  # Tạo canvas
        canvas.draw()
        canvas.get_tk_widget().pack()  # Đưa canvas vào frame

    def on_show_frame(self):
        self.data_departments = self.overview_service.pie_department_data()
        self.data_positions = self.overview_service.pie_position_data()

        self.frame_1 = tk.Frame(self , height=20)
        self.frame_1.pack(padx=10, pady=10,fill="x")
        nowTime = datetime.now()
        formatted_time = nowTime.strftime("%A, %d %B %Y")
        label = tk.Label(self.frame_1, text=f"Chào mừng trở lại, {globals.current_user.username}", font=("Helvetica", 16))
        label.pack(anchor="w")
        
        label_2 = tk.Label(self.frame_1, text=f"Hôm này là {formatted_time}", font=("Helvetica", 11))
        label_2.pack(anchor="w")
        
        self.frame_2 = tk.Frame(self , bg="#f0f0f0", height=220)
        self.frame_2.pack(padx=10, pady=10, fill="x", expand=True)

        self.frame_2.columnconfigure(0, weight=1) 
        self.frame_2.columnconfigure(1, weight=1)

        self.left_frame = tk.Frame(self.frame_2, bg="white", height=220)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) 
        hover_label = ttk.Label(self.left_frame, text="", font=("Helvetica", 12))
        hover_label.pack(pady=10)
        self.create_pie_char(self.left_frame, hover_label,self.data_departments, 'Tỷ lệ nhân viên theo phòng ban', 'Phòng ban')

        self.right_frame = tk.Frame(self.frame_2, bg="white", height=220)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10) 
        hover_label1 = ttk.Label(self.right_frame, text="", font=("Helvetica", 12))
        hover_label1.pack(pady=10)
        self.create_pie_char(self.right_frame, hover_label1, self.data_positions,'Chức vụ nhân viên', 'Vị trí')

        self.frame_3 = tk.Frame(self, height=200)
        self.frame_3.pack(padx=20, pady=0, fill="x", expand=True)

        # User sẽ hiện biểu đồ này
        if globals.current_user.role_id == 2:
            self.data_employee_departments = self.overview_service.pie_employee_data(employee_id = globals.current_user.employee_id)
            self.create_bar_char_employee(self.frame_3, data=self.data_employee_departments)
        else:
            self.create_bar_chart(self.frame_3, title='Số lần đi trễ trung bình trong tháng của các phòng ban', title_2 = 'Số lần đi trễ', title_3='Phòng ban',data= self.overview_service.pie_employee_in_department_data())


    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False): 
                """"""
            else:
                widget.pack_forget()
    