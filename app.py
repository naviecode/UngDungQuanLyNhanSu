import tkinter as tk
from ui.main_window import main_window


if __name__ == "__main__":
    root = tk.Tk()
    app = main_window(root)
    root.mainloop()
