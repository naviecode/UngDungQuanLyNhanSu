import tkinter as tk
from ui.main_window import main_window

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x600")
        self.main_frame = main_window(self)
        self.main_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
