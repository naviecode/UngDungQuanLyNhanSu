import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import calendar
from datetime import datetime
from service.timesheet_service import TimeSheetService
from tkinter import Toplevel, Label
import globals
from ui.pages import BasePage

class Timesheet(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.timesheet_service = TimeSheetService()
        self.set_permission_button(btn_add_show=True, btn_export_show=False)


    def export_excel(self):
        print("export")

    def search(self, filterInput):
        rows = self.timesheet_service.search(filterInput)
        return rows
    
    def dataSummarize(self, filterInput):
        rows = self.timesheet_service.dataSummarize(filterInput)
        return rows
    
    def lateNSoonSummarize(self, filterInput):
        rows = self.timesheet_service.lateNSoonSummarize(filterInput)
        return rows
    
    def onLeaveSummarize(self, filterInput):
        rows = self.timesheet_service.onLeaveSummarize(filterInput)
        return rows

    def show_tooltip(self, widget, summary_data):
        tooltip = Toplevel(widget)
        tooltip.wm_overrideredirect(True) 
        tooltip.geometry(f"+{widget.winfo_rootx()}+{widget.winfo_rooty() + widget.winfo_height()}")

        text = f"""
        Tổng số lần đi muộn: {summary_data['Late_Count']}
        Tổng thời gian đi muộn: {summary_data['Total_Late_Minutes']} phút
        Tổng số lần về sớm: {summary_data['Early_Out_Count']}
        Tổng thời gian về sớm: {summary_data['Total_Early_Out_Minutes']} phút
        -------------------------
        Tổng số lần đi muộn, về sớm: {summary_data['Total_Late_and_Early_Out_Count']}
        Tổng thời gian đi muộn, về sớm: {summary_data['Total_Minutes_Late_and_Early']} phút
        """

        label = Label(tooltip, text=text, justify="left", background="white", relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=5, ipady=5)

        widget.tooltip = tooltip
    
    def show_leave_tooltip(self, widget, leave_data):
        tooltip = Toplevel(widget)
        tooltip.wm_overrideredirect(True)  
        tooltip.geometry(f"+{widget.winfo_rootx()}+{widget.winfo_rooty() + widget.winfo_height()}")

        text = f"""
        Nghỉ phép: {leave_data['Total_ONLEAVE']} ngày
        Nghỉ không lương: {leave_data['Total_UNPLEAVE']} ngày
        -------------------------
        Tổng số ngày nghỉ: {leave_data['Total_LEAVE']} ngày
        """

        label = Label(tooltip, text=text, justify="left", background="white", relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=5, ipady=5)

        widget.tooltip = tooltip

    def hide_tooltip(self, widget):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
        
    def on_month_year_change(self, event):
        month_index = self.month_combobox.get()  
        year = int(self.year_combobox.get())  

        filterInput = {
            "month": int(month_index),
            "year": year,
            "emp_id": globals.current_user.employee_id
        }
        rows = self.search(filterInput)
        print(rows)
        self.update_calendar(int(month_index), year, rows)
        
        summary_data = self.lateNSoonSummarize(filterInput)
        if summary_data:
            summary = summary_data[0] 

            self.total_late_soon_frame.bind("<Enter>", lambda event: self.show_tooltip(self.total_late_soon_frame, summary))
            self.total_late_soon_frame.bind("<Leave>", lambda event: self.hide_tooltip(self.total_late_soon_frame))

        leave_data = self.onLeaveSummarize(filterInput)
        if leave_data:
            leave_summary = leave_data[0] 

            self.total_off_frame.bind("<Enter>", lambda event: self.show_leave_tooltip(self.total_off_frame, leave_summary))
            self.total_off_frame.bind("<Leave>", lambda event: self.hide_tooltip(self.total_off_frame))

        self.update_summary(filterInput)


    def update_calendar(self, month, year, data):
        for widget in self.frame_calendar.winfo_children():
            widget.destroy()

        self.create_calendar(self.frame_calendar, month, year, data)

    def create_calendar(self, parent, month, year, data):
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
        resized_image = original_image.resize((130, 65), Image.Resampling.LANCZOS)
        stripe_img = ImageTk.PhotoImage(resized_image)

        today = datetime.today()
        row_number = 1

        def get_day_data(day):
            for row in data:
                work_date = row['work_date']
                if work_date.day == day and work_date.month == month and work_date.year == year:
                    return row
            return None

        for week_index, week in enumerate(month_days):
            for col, day in enumerate(week):
                day_frame = tk.Frame(parent, borderwidth=2, relief="solid", width=15, height=7)
                day_frame.grid(row=row_number, column=col, sticky="nsew")

                if day == 0:  
                    if week_index == 0:  
                        empty_cells = week.count(0)  
                        day = (prev_month_days - empty_cells + 1) + col
                        display_date = f'{day}'
                    else:  
                        display_date = f'{next_month_day}'
                        next_month_day += 1

                    date_label = tk.Label(day_frame, text=display_date, padx=5, pady=5, anchor="n")
                    date_label.pack(side="top", fill="x")

                    hours_label = tk.Label(day_frame, image=stripe_img, padx=5, pady=5, anchor="center")
                    hours_label.pack(side="top", expand=True, fill="both")
                    hours_label.image = stripe_img  
                else: 
                    label_text = f'{day} (Today)' if (day == today.day and month == today.month and year == today.year) else f'{day}'
                    date_label = tk.Label(day_frame, text=label_text, padx=5, pady=5, anchor="n")
                    date_label.pack(side="top", fill="x")

                    day_data = get_day_data(day)

                    if day_data:
                        check_in_time = day_data['check_in_time']
                        check_out_time = day_data['check_out_time']
                        check_in_status = day_data['check_in_status']
                        check_out_status = day_data['check_out_status']

                        if check_in_status == 'ONLEAVE':
                            check_in_text = 'Nghỉ phép'
                            check_in_color = 'red'
                        elif check_in_status == 'UNPLEAVE':
                            check_in_text = 'Nghỉ không phép'
                            check_in_color = 'red'
                        elif check_in_status == 'LATE':
                            check_in_text = check_in_time
                            check_in_color = '#fcb123'  
                        else: 
                            check_in_text = check_in_time
                            check_in_color = 'grey'

                        if check_out_status == 'ONLEAVE':
                            check_out_text = 'Nghỉ phép'
                            check_out_color = 'red'
                        elif check_out_status == 'UNPLEAVE':
                            check_out_text = 'Nghỉ không phép'
                            check_out_color = 'red'
                        elif check_out_status == 'SOON':
                            check_out_text = check_out_time
                            check_out_color = '#fcb123' 
                        else: 
                            check_out_text = check_out_time
                            check_out_color = 'grey'

                        combined_label = tk.Text(day_frame, height=3, width=15, borderwidth=0, padx=5, pady=5)
                        combined_label.pack(side="top", fill="x")

                        combined_label.config(state="normal")

                        if check_in_text == 'Nghỉ không phép' or check_out_text == 'Nghỉ không phép' or check_in_text == 'Nghỉ phép' or check_out_text == 'Nghỉ phép': 
                            combined_label.insert("insert", check_in_text, "check_in")
                            combined_label.insert("insert", "\n-\n")
                            combined_label.insert("insert", check_out_text, "check_out")
                        elif (check_in_text == 'Nghỉ không phép' and check_out_text == 'Nghỉ không phép') or (check_in_text == 'Nghỉ phép' and check_out_text == 'Nghỉ phép'):
                            combined_label.insert("insert", check_in_text, "check_in")
                        else:
                            combined_label.insert("insert", check_in_text, "check_in")
                            combined_label.insert("insert", " - ")
                            combined_label.insert("insert", check_out_text, "check_out")

                        combined_label.tag_configure("check_in", foreground=check_in_color)
                        combined_label.tag_configure("check_out", foreground=check_out_color)

                        combined_label.tag_configure("center", justify="center")
                        combined_label.tag_add("center", "1.0", "end")

                        combined_label.config(state="disabled")

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
            parent.grid_columnconfigure(i, weight=1, minsize=140)
        for i in range(1, 7):
            parent.grid_rowconfigure(i, weight=1, minsize=100)

        parent.stripe_img = stripe_img  




        
    def on_show_frame(self):
        self.center_frame = tk.Frame(self, width=1000, height=600)
        self.center_frame.pack(expand=True)

        label = tk.Label(self.center_frame, text="BẢNG CHẤM CÔNG", font=("Helvetica", 16))
        label.pack(pady=20, side="top")

        self.on_show_filterInput()

        self.summary_frame = tk.Frame(self.center_frame)
        self.summary_frame.pack(pady=10)

        self.total_workday_frame = tk.Frame(self.summary_frame, borderwidth=1, relief="solid", padx=10, pady=5)
        self.total_workday_frame.pack(side="left", padx=(0, 20))

        self.total_late_soon_frame = tk.Frame(self.summary_frame, borderwidth=1, relief="solid", padx=10, pady=5)
        self.total_late_soon_frame.pack(side="left", padx=(0, 20))

        self.total_off_frame = tk.Frame(self.summary_frame, borderwidth=1, relief="solid", padx=10, pady=5)
        self.total_off_frame.pack(side="left", padx=(0, 20))

        today = datetime.today()
        self.month_combobox.current(today.month - 1)
        self.year_combobox.current(5)  

        self.canvas = tk.Canvas(self.center_frame, width=1000, height=600)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.center_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame_calendar = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_calendar, anchor="nw")

        filterInput = {
            "month": int(today.month),
            "year": int(today.year),
            "emp_id": globals.current_user.employee_id
        }

        rows = self.search(filterInput)
        self.update_calendar(today.month, today.year, rows)

        summary_data = self.lateNSoonSummarize(filterInput)
        if summary_data:
            summary = summary_data[0]  

            self.total_late_soon_frame.bind("<Enter>", lambda event: self.show_tooltip(self.total_late_soon_frame, summary))
            self.total_late_soon_frame.bind("<Leave>", lambda event: self.hide_tooltip(self.total_late_soon_frame))
        
        leave_data = self.onLeaveSummarize(filterInput)
        if leave_data:
            leave_summary = leave_data[0] 

            self.total_off_frame.bind("<Enter>", lambda event: self.show_leave_tooltip(self.total_off_frame, leave_summary))
            self.total_off_frame.bind("<Leave>", lambda event: self.hide_tooltip(self.total_off_frame))

        self.update_summary(filterInput)

        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_year_change)
        self.year_combobox.bind("<<ComboboxSelected>>", self.on_month_year_change)

        self.canvas.after(50, lambda: self.canvas.yview_moveto(0))
    
    def on_show_filterInput(self):
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
    
    def update_summary(self, filterInput):
        summary_data = self.dataSummarize(filterInput)

        if summary_data and len(summary_data) > 0:
            summary = summary_data[0]

            total_workday = summary.get('Total_Workday', '0')
            total_late_soon = summary.get('Total_LateNSoonTimes', '0')
            total_off = summary.get('Total_Off', '0')

            self.create_summary_label(self.total_workday_frame, "Tổng công hưởng lương", total_workday, "./images/Icons/check_calendar.png")
            self.create_summary_label(self.total_late_soon_frame, "Số lần đi muộn, về sớm", total_late_soon, "./images/Icons/lateNsoon_calendar.png")
            self.create_summary_label(self.total_off_frame, "Tổng số ngày nghỉ", total_off, "./images/Icons/off_calendar.png")
        else:
            self.create_summary_label(self.total_workday_frame, "Tổng công hưởng lương", '0', "./images/Icons/check_calendar.png")
            self.create_summary_label(self.total_late_soon_frame, "Số lần đi muộn, về sớm", '0', "./images/Icons/lateNsoon_calendar.png")
            self.create_summary_label(self.total_off_frame, "Tổng số ngày nghỉ", '0', "./images/Icons/off_calendar.png")

    def create_summary_label(self, frame, text, value, imageLink):
        for widget in frame.winfo_children():
            widget.destroy()

        clipboard_image = Image.open(imageLink)
        resized_image = clipboard_image.resize((30, 30), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(resized_image)

        label_text = tk.Label(frame, text=text, font=("Helvetica", 12), anchor="w")
        label_text.pack(side="left", padx=(0, 5))

        label_value = tk.Label(frame, text=value, font=("Helvetica", 20, "bold"), anchor="w")
        label_value.pack(side="left", padx=(0, 5))

        icon_label = tk.Label(frame, image=icon)
        icon_label.pack(side="left", padx=(10, 0))
        icon_label.image = icon 


    def clear_frame_data(self):
        for widget in self.winfo_children():
            if getattr(widget, '_from_base', False):  
                """"""
            else:
                widget.pack_forget()


