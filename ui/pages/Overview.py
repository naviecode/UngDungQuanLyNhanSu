import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from ui.pages.BasePage import BasePage
import pandas as pd
import matplotlib.pyplot as plt

class Overview(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.set_permission(btn_add_show=False, btn_export_show=False)

    def create_pie_char(self, frame, hover_label):
        departments = ['Phòng Kỹ Thuật', 'Phòng Kế Toán', 'Phòng Nhân Sự', 'Phòng IT', 'Phòng Marketing']
        employee_counts = [30, 20, 25, 15, 10]
        
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        fig, ax = plt.subplots(figsize=(4, 4))

        wedges, texts, autotexts = ax.pie(
            employee_counts, labels=departments, colors=colors, autopct='%1.1f%%', startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 3},
            pctdistance=0.85, 
            explode=(0.05, 0.05, 0.05, 0.05, 0.05)
        )
        
        # Thêm viền trắng ở giữa
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title('Tỷ lệ nhân viên theo phòng ban', fontsize=13, weight='bold')

        # Function để xử lý hover
        def on_hover(event):
            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    if wedge.contains_point([event.x, event.y]):
                        hover_label.config(text=f"Phòng ban: {departments[i]}")
                        return
                hover_label.config(text="")  # Không hover vào phần nào thì label trống

        # Thêm sự kiện hover vào figure
        fig.canvas.mpl_connect('motion_notify_event', on_hover)

        # Chuyển figure thành canvas để hiển thị trong Tkinter
        chart = FigureCanvasTkAgg(fig, master=frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_bar_chart(self, frame):
        departments = ['Phòng Kỹ Thuật', 'Phòng Kế Toán', 'Phòng Nhân Sự', 'Phòng IT', 'Phòng Marketing']
        avg_late_count = [5, 2, 6, 3, 1]  # Trung bình số lần đi trễ của mỗi phòng ban

        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Vẽ biểu đồ cột
        ax.bar(departments, avg_late_count, color=colors)
        ax.set_title('Số lần đi trễ trung bình trong tháng', fontsize=14, weight='bold')
        ax.set_ylabel('Số lần đi trễ')
        ax.set_xlabel('Phòng ban')

        # Chuyển figure thành canvas để hiển thị trong Tkinter
        chart = FigureCanvasTkAgg(fig, master=frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_bar_char_employee(self):
        # Dữ liệu mẫu: Ngày và số phút đi trễ của một nhân viên trong 1 tháng
        data = {
            'date': pd.date_range(start='2023-09-01', end='2023-09-30'),
            'late_minutes': [5, 0, 10, 3, 8, 0, 12, 4, 6, 9, 0, 7, 5, 3, 0, 0, 15, 4, 6, 10, 8, 7, 0, 12, 3, 6, 4, 0, 9, 10]
        }

        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)

        # Vẽ biểu đồ cột (bar chart)
        plt.figure(figsize=(10, 6))
        plt.bar(df['date'], df['late_minutes'], color='skyblue')

        # Thêm tiêu đề và nhãn
        plt.title('Số phút đi trễ trung bình của nhân viên mỗi ngày trong tháng', fontsize=16)
        plt.xlabel('Ngày', fontsize=12)
        plt.ylabel('Số phút đi trễ', fontsize=12)

        # Hiển thị giá trị trên từng cột
        for i, txt in enumerate(df['late_minutes']):
            plt.text(df['date'][i], df['late_minutes'][i] + 0.5, str(txt), ha='center')

        # Xoay nhãn ngày để dễ đọc
        plt.xticks(rotation=45)

        # Hiển thị biểu đồ
        plt.tight_layout()
        plt.show()

    def on_show_frame(self):
        self.frame_1 = tk.Frame(self , height=20)
        self.frame_1.pack(padx=10, pady=10,fill="x")
        nowTime = datetime.now()
        formatted_time = nowTime.strftime("%A, %d %B %Y")
        label = tk.Label(self.frame_1, text="Chào mừng trở lại, Quang Sơn", font=("Helvetica", 16))
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
        self.create_pie_char(self.left_frame, hover_label)

        self.right_frame = tk.Frame(self.frame_2, bg="white", height=220)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10) 
        hover_label1 = ttk.Label(self.right_frame, text="", font=("Helvetica", 12))
        hover_label1.pack(pady=10)
        self.create_pie_char(self.right_frame, hover_label1)

        self.frame_3 = tk.Frame(self, height=200)
        self.frame_3.pack(padx=20, pady=0, fill="x", expand=True)

        self.create_bar_chart(self.frame_3)

    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()
    