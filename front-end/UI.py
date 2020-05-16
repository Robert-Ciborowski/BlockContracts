import tkinter as tk
from PIL import ImageTk, Image
import image

HEIGHT = 700
WIDTH = 800

root = tk.Tk(className='Python UI')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


logo_image = ImageTk.PhotoImage(Image.open(
    "./image/logo.png"))  # Logo and background
logo_label = tk.Label(root, image=logo_image)
logo_label.place(relwidth=1, relheight=0.4)

root.mainloop()
