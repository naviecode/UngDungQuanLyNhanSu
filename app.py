import tkinter as tk
from ui.main_window import main_window
# from ui.login_screen import LoginScreen

if __name__ == "__main__":
    root = tk.Tk()
    app = main_window(root)
    root.mainloop()
