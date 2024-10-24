import tkinter as tk
from PIL import Image, ImageTk

class ButtonImage:
    def __init__(self, parent, image_path, text="", command=None, width=150, height=40, active = False, activeBg="white", activefg="black", bg = "white", fg = "black", anchor = "w", cursor = "hand2", fontsize=11, compound="left", pady=0, padx=10):
        self.frame = tk.Frame(parent, width=width, height=height)
        self.frame.pack_propagate(False)

        self.button_image = Image.open(image_path)
        self.resized_button_image = self.button_image.resize((20,20))
        self.button_image_photo = ImageTk.PhotoImage(self.resized_button_image)

        if(active):
            bg = "#0178bc" if active else "white"
            fg = "white" if active else "black"

        self.button = tk.Button(self.frame,
            image= self.button_image_photo,
            compound=compound,
            text=text,font=(fontsize),
            width=width,
            height=height,
            relief="flat",
            activebackground=activeBg,
            activeforeground=activefg,
            cursor=cursor,
            highlightthickness=0,
            bd=0,
            padx=padx,
            pady=pady,
            bg=bg, 
            fg=fg,
            anchor=anchor,
            command= command
        )
        self.button.image = self.button_image_photo 
        self.button.pack(fill="both", expand=True)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self, **kwargs):
        self.frame.pack_forget(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)
    
    def destroy(self):
        self.button.destroy()
        self.frame.destroy()
    
    def config(self, **kwargs):
        self.button.config(**kwargs)