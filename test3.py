import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Tạo Treeview
tree = ttk.Treeview(root, columns=('Name', 'Age'), show='headings')
tree.pack(fill='both', expand=True)

# Đặt tên cho cột
tree.heading('Name', text='Name')
tree.heading('Age', text='Age')

# Thêm dữ liệu vào Treeview
tree.insert('', 'end', iid=1, values=('John Doe', 25))
tree.insert('', 'end', iid=2, values=('Jane Smith', 30))

# Hiển thị Treeview trước khi lấy bbox
root.update()

# Lấy tọa độ và kích thước của ô trong item 1, cột 'Age'
bbox_value = tree.bbox(1, column='Age')

if bbox_value:
    x0, y0, width, height = bbox_value
    print(f"x0: {x0}, y0: {y0}, width: {width}, height: {height}")
else:
    print("Không tìm thấy tọa độ cho ô này.")

root.mainloop()
