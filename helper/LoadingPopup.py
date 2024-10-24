import tkinter as tk
from PIL import Image, ImageTk


class LoadingPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.overrideredirect(True)

        self.img = Image.open("./images/loading/loading_2.gif")
        self.frames = [ImageTk.PhotoImage(self.img.copy())] 

        try:
            while True:
                self.img.seek(self.img.tell() + 1)  # Chuyển frame
                self.frames.append(ImageTk.PhotoImage(self.img.copy()))
        except EOFError:
            pass

        self.label = tk.Label(self, image=self.frames[0], borderwidth=0, highlightthickness=0)
        self.label.pack()
        self.frame_index = 0
        self.after(100, self.animate_loading)

        self.center_window()

        

    def animate_loading(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.frame_index])
        self.after(100, self.animate_loading)  # Cập nhật mỗi 100ms

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

    def center_window(self):
        self.update_idletasks()
        window_width = 300
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.transient(self.parent)  # Đảm bảo popup nằm trên cửa sổ chính
        self.grab_set()  # Chặn tất cả các sự kiện từ cửa sổ khác
        
        # Sử dụng after để kiểm tra việc hoàn thành của thread
        self.check_thread_completion()