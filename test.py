import tkinter as tk
from tkcalendar import DateEntry

class EmployeeFormPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Employee Form")
        self.geometry("300x200")

        tk.Label(self, text="Employee Name:").pack(pady=10)
        tk.Entry(self).pack()

        tk.Label(self, text="Date of Birth:").pack(pady=10)
        
        # DatePicker for Date of Birth
        self.dob = DateEntry(self, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=1990)
        self.dob.pack(pady=5)

        tk.Button(self, text="Close", command=self.destroy).pack(pady=20)

# Main window
root = tk.Tk()
root.geometry("600x400")

def open_popup():
    form_popup = EmployeeFormPopup(root)

tk.Button(root, text="Open Employee Form", command=open_popup).pack(pady=100)

root.mainloop()
