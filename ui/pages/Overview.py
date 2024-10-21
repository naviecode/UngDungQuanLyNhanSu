import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Overview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
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

    def on_show_frame(self):
        self.frame_1 = tk.Frame(self , height=20)
        self.frame_1.pack(padx=10, pady=10,fill="x")

        label = tk.Label(self.frame_1, text="Chào mừng trở lại, Quang Sơn", font=("Helvetica", 16))
        label.pack(anchor="w")
        
        label_2 = tk.Label(self.frame_1, text="Hôm này là Monday, 27 April 2020", font=("Helvetica", 11))
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
            widget.pack_forget()
    