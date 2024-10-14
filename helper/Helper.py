import tkinter as tk
from PIL import Image, ImageTk


class Helper():

    def CreateButton(self, parent, text, image_path,active, command):
        button_image = Image.open(image_path)
        resized_button_image = button_image.resize((20,20))
        self.button_image_photo = ImageTk.PhotoImage(resized_button_image)
        bg_button_active = "#0178bc" if active else "white"
        fg_button_active = "white" if active else "black"
        button = tk.Button(parent,
            image= self.button_image_photo,
            compound="left",
            text=text,font=(11),
            width=250,
            relief="flat",
            activebackground="#0178bc",
            activeforeground="white",
            cursor="hand2",
            highlightthickness=0,
            bd=0,
            pady=8,
            padx=10,
            bg=bg_button_active, 
            fg=fg_button_active,
            anchor="w",
            command= command
        )
        button.image =self.button_image_photo 
        return button        
    
    def GetImage():
        return ""