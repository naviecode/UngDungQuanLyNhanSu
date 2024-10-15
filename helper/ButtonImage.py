import tkinter as tk
from PIL import Image, ImageTk

class ButtonImage:
    def __init__(self, parent, image_path, text="", command=None, width=150, height=30, bg="white", fg="black"):
        self.frame = tk.Frame(parent, width=width, height=height)
        self.frame.pack_propagate(False)

        self.button_image = Image.open(image_path)
        self.resized_button_image = self.button_image.resize((20,20))
        self.button_image_photo = ImageTk.PhotoImage(self.resized_button_image)
        self.button = tk.Button(self.frame,
            image= self.button_image_photo,
            compound="left",
            text=text,font=(10),
            width=width,
            height=height,
            relief="flat",
            activebackground=bg,
            activeforeground=fg,
            cursor="hand2",
            highlightthickness=0,
            padx=10,
            bd=0,
            bg=bg, 
            fg=fg,
            anchor="w",
            command= command
        )
        self.button.image = self.button_image_photo 
        self.button.pack(fill="both", expand=True)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)
    
    def destroy(self):
        self.button.destroy()
        self.frame.destroy()