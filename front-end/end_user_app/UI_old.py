import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
import image

HEIGHT = 700
WIDTH = 800


def uploadFile():  # upload function
    contract = filedialog.askopenfilename(
        initialdir="/", title="Select A File", filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
    print(contract)


def createContract():  # create contract button function

    # Upload frame
    upload = tk.Tk(className="Create Contract")
    upload.geometry('290x200')

    # Upload window
    upload_label = tk.Label(upload, text='Upload Contact',
                            relief="solid", font=('arial', 12, 'bold'))
    upload_label.place(x=80, y=70)

    upload_button = tk.Button(
        upload, text='Browse A File', width=17, bg='brown', fg='white')  # verify contact button
    upload_button.place(x=80, y=110)
    tk.Button(upload, text="Next").place(x=230, y=160)


root = tk.Tk(className='Main UI')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


logo_image = ImageTk.PhotoImage(Image.open(
    "image/logo.png"))  # Logo and background
logo_label = tk.Label(root, image=logo_image)
logo_label.place(relwidth=1, relheight=0.4)


createContact_image = ImageTk.PhotoImage(
    file='image/create.png')  # image for create contact button

verifyContact_image = ImageTk.PhotoImage(
    file='image/verify.png')  # image for verify contact button

readContact_image = ImageTk.PhotoImage(  # image for read contact button
    file='image/read.png'
)

createContact_button = tk.Button(
    image=createContact_image, bd=0, command=createContract)  # craete contact button
createContact_button.place(x=300, y=290)

verifyContact_button = tk.Button(
    image=verifyContact_image, bd=0)  # verify contact button
verifyContact_button.place(x=300, y=375)

readContact_button = tk.Button(
    image=readContact_image, bd=0)  # read contact button
readContact_button.place(x=300, y=460)

root.mainloop()
