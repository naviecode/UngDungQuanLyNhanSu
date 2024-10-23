import tkinter as tk


class LoadingPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Loading")

        window_width = 300
        window_height = 150
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        #Căn giữa popup
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # self.geometry("300x150")
        self.label = tk.Label(self, text="Loading... Please wait", font=("Helvetica", 14))
        self.label.pack(pady=30)

        # Cấu hình chế độ modal
        self.transient(parent)  # Đảm bảo popup nằm trên cửa sổ chính
        self.grab_set()  # Chặn tất cả các sự kiện từ cửa sổ khác
        
        # Sử dụng after để kiểm tra việc hoàn thành của thread
        self.check_thread_completion()

    def complete_loading(self):
        # Đóng popup khi quá trình loading hoàn tất
        self.is_complete = True

    def check_thread_completion(self):
        # Kiểm tra trạng thái của quá trình tải dữ liệu
        if hasattr(self, 'is_complete') and self.is_complete:
            self.destroy()  # Đóng popup khi quá trình hoàn thành
        else:
            # Tiếp tục kiểm tra sau 100ms
            self.after(100, self.check_thread_completion)