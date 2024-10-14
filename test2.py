import tkinter as tk
from tkinter import ttk

class PaginatedTreeview(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Phân Trang Treeview")
        self.geometry("400x300")

        # Dữ liệu giả lập
        self.data = [(f'Nguyen Van {i}', 20 + i, 'HCM') for i in range(100)]

        # Số mục trên mỗi trang
        self.items_per_page = 10
        self.current_page = 0

        # Tạo Treeview
        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Name', 'Age', 'Address')
        self.tree.column('#0', width=0, stretch=tk.NO)  # Ẩn cột đầu tiên
        self.tree.column('Name', anchor='center', width=100)
        self.tree.column('Age', anchor='center', width=50)
        self.tree.column('Address', anchor='center', width=150)

        # Đặt tiêu đề cho các cột
        self.tree.heading('#0', text='', anchor='center')
        self.tree.heading('Name', text='Name', anchor='center')
        self.tree.heading('Age', text='Age', anchor='center')
        self.tree.heading('Address', text='Address', anchor='center')

        self.tree.pack(pady=20)

        # Tạo nút trước và tiếp theo
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.prev_button = tk.Button(self.button_frame, text="Trước", command=self.prev_page)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Tiếp theo", command=self.next_page)
        self.next_button.grid(row=0, column=1, padx=5)

        # Hiển thị trang đầu tiên
        self.display_page()

    def display_page(self):
        # Xóa tất cả các mục hiện có
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu cho trang hiện tại
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data[start:end]

        # Thêm dữ liệu vào Treeview
        for entry in page_data:
            self.tree.insert('', 'end', values=entry)

        # Cập nhật trạng thái nút
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end < len(self.data) else tk.DISABLED)

    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.data):
            self.current_page += 1
            self.display_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

if __name__ == '__main__':
    app = PaginatedTreeview()
    app.mainloop()
