import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import calendar
from datetime import datetime
from ui.pages import BasePage

class Timesheet(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.set_permission_button(btn_add_show=True, btn_export_show=False)


    def export_excel(self):
        print("export")
        
    def on_month_year_change(self, event):
        month_index = self.month_combobox.get()  
        year = int(self.year_combobox.get())  
        self.update_calendar(int(month_index), year)

    def update_calendar(self, month, year):
        for widget in self.frame_calendar.winfo_children():
            widget.destroy()

        self.create_calendar(self.frame_calendar, month, year)

    def create_calendar(self, parent, month, year):
        days_of_week = ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ nhật']
        
        for col, day in enumerate(days_of_week):
            tk.Label(parent, text=day, padx=5, pady=2, borderwidth=2, relief="solid").grid(row=0, column=col, sticky="nsew")
        
        cal = calendar.Calendar(firstweekday=0)  
        month_days = cal.monthdayscalendar(year, month)

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
        next_month_day = 1

        original_image = Image.open("./images/background/stripe_timesheet.png")
        resized_image = original_image.resize((100, 80), Image.Resampling.LANCZOS)
        stripe_img = ImageTk.PhotoImage(resized_image)

        today = datetime.today()
        row_number = 1

        for week in month_days:
            for col, day in enumerate(week):
                if day == 0: 
                    if row_number == 1:  
                        day = prev_month_days - week[:col].count(0)
                        display_date = f'{day}'
                    else: 
                        display_date = f'{next_month_day}'
                        next_month_day += 1

                    day_frame = tk.Frame(parent, borderwidth=2, relief="solid", width=15, height=7)
                    day_frame.grid(row=row_number, column=col, sticky="nsew")

                    date_label = tk.Label(day_frame, text=display_date, padx=5, pady=5, anchor="n")
                    date_label.pack(side="top", fill="x")

                    hours_label = tk.Label(day_frame, image=stripe_img, padx=5, pady=5, anchor="center")
                    hours_label.pack(side="top", expand=True, fill="both")
                    hours_label.image = stripe_img  

                else:  
                    day_frame = tk.Frame(parent, borderwidth=2, relief="solid", width=15, height=7)
                    day_frame.grid(row=row_number, column=col, sticky="nsew")

                    if (day == today.day and month == today.month and year == today.year):
                        label_text = f'{day} (Today)'
                    else:
                        label_text = f'{day}'

                    date_label = tk.Label(day_frame, text=label_text, padx=5, pady=5, anchor="n")
                    date_label.pack(side="top", fill="x")

                    working_hours = f'07:48 - 17:48'
                    hours_label = tk.Label(day_frame, text=working_hours, padx=5, pady=5, anchor="center")
                    hours_label.pack(side="top", expand=True, fill="both")
            
            row_number += 1

        for extra_row in range(row_number, 7):
            for col in range(7):
                day_frame = tk.Frame(parent, borderwidth=2, relief="solid", width=15, height=7)
                day_frame.grid(row=extra_row, column=col, sticky="nsew")

                date_label = tk.Label(day_frame, text=f'{next_month_day}', padx=5, pady=5, anchor="n")
                date_label.pack(side="top", fill="x")

                hours_label = tk.Label(day_frame, image=stripe_img, padx=5, pady=5, anchor="center")
                hours_label.pack(side="top", expand=True, fill="both")
                hours_label.image = stripe_img 
                next_month_day += 1

        for i in range(7):
            parent.grid_columnconfigure(i, weight=1, minsize=100)
        for i in range(1, 7):
            parent.grid_rowconfigure(i, weight=1, minsize=100)

        parent.stripe_img = stripe_img  # Retain reference to the image
    def on_show_frame(self):
        self.center_frame = tk.Frame(self, width=760, height=600)
        self.center_frame.pack(expand=True)

        label = tk.Label(self.center_frame, text="BẢNG CHẤM CÔNG", font=("Helvetica", 16))
        label.pack(pady=20, side="top")

        selection_frame = tk.Frame(self.center_frame)
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text="Tháng :").pack(side="left", padx=(0, 5))
        
        self.month_var = tk.StringVar()
        self.month_combobox = ttk.Combobox(selection_frame, textvariable=self.month_var, width=5)
        self.month_combobox['values'] = [i for i in range(1, 13)] 
        self.month_combobox.pack(side="left", padx=(0, 20))

        tk.Label(selection_frame, text="Năm :").pack(side="left", padx=(20, 5))
        
        self.year_var = tk.StringVar()
        self.year_combobox = ttk.Combobox(selection_frame, textvariable=self.year_var, width=6)
        self.year_combobox['values'] = [str(year) for year in range(datetime.now().year - 5, datetime.now().year + 6)]
        self.year_combobox.pack(side="left", padx=(0, 20))

        today = datetime.today()
        self.month_combobox.current(today.month - 1)
        self.year_combobox.current(5)  

        self.canvas = tk.Canvas(self.center_frame, width=760, height=600)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.center_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame_calendar = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_calendar, anchor="nw")

        self.update_calendar(today.month, today.year)

        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_year_change)
        self.year_combobox.bind("<<ComboboxSelected>>", self.on_month_year_change)

        self.canvas.after(50, lambda: self.canvas.yview_moveto(0))

    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  # Kiểm tra widget có thuộc BasePage hay không
                """"""
            else:
                widget.pack_forget()


