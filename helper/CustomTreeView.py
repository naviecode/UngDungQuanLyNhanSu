import tkinter as tk
from tkinter import ttk
from helper.ButtonImage import ButtonImage


class CustomTreeView:
    def __init__(self, frame_view, parent, datas, columns, columnShowBtn):
        """ 
            datas: dữ liệu theo thứ tự cột
            objcet: coulumn - column name - width - anchor
            columnShowBtn: vị trí hiển thị button trên treeView
        """
        self.frame_view = frame_view
        self.parent = parent
        self.datas = datas
        self.columns = columns
        self.columnShowBtn = columnShowBtn

        # Số mục trên mỗi trang
        self.items_per_page = 20
        self.current_page = 0
        self.buttons = []
        self.get_treeView()

        #Load trang đầu
        self.loadData()

    def get_treeView(self):
        columnsView = []
        for column in self.columns:
            columnsView.append(column['key'])
        
        self.frame_view.tree = ttk.Treeview(self.frame_view, columns=columnsView , show='headings',height=18)
        
        for col in self.columns:
            self.frame_view.tree.heading(col['key'], text=col['name'])
            self.frame_view.tree.column(col['key'], width=col['width'], anchor=col['anchor'])

        self.frame_view.tree.grid(row=0, column=0, sticky='nsew')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_view, orient=tk.VERTICAL, command=self.frame_view.tree.yview)
        self.frame_view.tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(self.frame_view, orient=tk.HORIZONTAL, command=self.frame_view.tree.xview)
        self.frame_view.tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        # Tùy chỉnh việc mở rộng
        self.frame_view.grid_rowconfigure(0, weight=1)
        self.frame_view.grid_columnconfigure(0, weight=1)

        for data in self.datas:
            self.frame_view.tree.insert('', tk.END, values=data)
        
        self.parent.after(200, self.get_button_view)

        # Tạo nút trước và tiếp theo
        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(fill="both", expand=True, pady=10)

        self.next_button = tk.Button(self.button_frame, text="Tiếp theo", command=self.next_page, width=10)
        self.next_button.pack(padx=10, side="right")

        self.prev_button = tk.Button(self.button_frame, text="Trước", command=self.prev_page, width=10)
        self.prev_button.pack(padx=20, side="right")


    def get_button_view(self):
        # Tạo button trong Treeview
        for child in self.frame_view.tree.get_children():
            id_index = self.parent.search()
            row_id = id_index[self.frame_view.tree.index(child) + self.current_page * self.items_per_page][0]
            x0, y0, width, height = self.frame_view.tree.bbox(child, column=self.columnShowBtn)  
            button_delete = ButtonImage(self.frame_view.tree, "./images/icons/delete.png", "", command=lambda id=row_id: self.parent.delete(id),width=50, height=30, bg="white", fg="white")
            button_update = ButtonImage(self.frame_view.tree, "./images/icons/edit.png", "", command=lambda id=row_id: self.parent.edit(id),width=50, height=30, bg="white", fg="white")
            
            button_update.place(x=x0 + width - 30, y=y0 + 2, width=30, height=20)
            button_delete.place(x=x0 + width - 30 - 30, y=y0 + 2, width=30, height=20)

            self.buttons.append(button_update)
            self.buttons.append(button_delete)
    
    def next_page(self):
        print(self.current_page)
        print(self.items_per_page)
        print(len(self.datas))
        0 + 1 * 20 < 20
        if (self.current_page + 1) * self.items_per_page < len(self.datas):
            self.current_page += 1
            self.loadData()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.loadData()

    def loadData(self):
        for child in self.frame_view.tree.get_children():
            self.frame_view.tree.delete(child)

        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        
        self.data_reload = self.parent.search()
        # Lấy dữ liệu cho trang hiện tại
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data_reload[start:end]

        for data in page_data:
            self.frame_view.tree.insert('', tk.END, values=data)
        
        self.parent.after(500, self.get_button_view)

        # Cập nhật trạng thái nút
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end < len(self.data_reload) else tk.DISABLED)
    def destroy(self):
        for widget in self.frame_view.tree.winfo_children():
            widget.destroy()
    def pack_forget(self):
        self.frame_view.tree.pack_forget()
    