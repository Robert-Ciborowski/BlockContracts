import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
import image

LARGE_FONT = ("Verdana", 12)
XLARGE_FONT = ("Verdana", 30)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, UploadContract, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas(self, height=700, width=800)
        canvas.pack()

        # Logo and background
        self.logo_image = ImageTk.PhotoImage(Image.open(
            "./image/logo.png"))
        logo_label = tk.Label(self, image=self.logo_image)
        logo_label.place(relwidth=1, relheight=0.4)

        # image for create contract button
        self.createContact_image = ImageTk.PhotoImage(
            file='./image/create.png')

        # image for vefiry contract button
        self.verifyContact_image = ImageTk.PhotoImage(
            file='./image/verify.png')

        # image for read contract button
        self.readContact_image = ImageTk.PhotoImage(  # image for read contact button
            file='./image/read.png')

        # create contract button
        button = tk.Button(self, image=self.createContact_image, bd=0,
                           command=lambda: controller.show_frame(UploadContract))
        button.place(x=300, y=290)

        # verify contract button
        button2 = tk.Button(self, image=self.verifyContact_image, bd=0,
                            command=lambda: controller.show_frame(PageTwo))
        button2.place(x=300, y=375)

        # read contract button
        button3 = tk.Button(self, image=self.readContact_image, bd=0)
        button3.place(x=300, y=460)


class UploadContract(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Upload Contract", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        self.contract = ''

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        # image for upload button
        self.UploadContract = ImageTk.PhotoImage(
            file='./image/upload.png')

        # button for upload contract
        button2 = tk.Button(self, text="Page Two",
                            bd=0, image=self.UploadContract, command=lambda: self.uploadfile())
        button2.place(x=280, y=250)

        # label for file path
        self.path = tk.Label(self, text="No File been upload yet")
        self.path.pack(pady=240, padx=7)

    def uploadfile(self):
        self.contract = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
        self.path.configure(text=self.contract)
        print(self.contract)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(UploadContract))
        button2.pack()


app = SeaofBTCapp()
app.mainloop()
