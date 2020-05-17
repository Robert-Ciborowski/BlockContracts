import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
import image
import time as time
from user_http import UserHTTP
from utils.cypter import Encrypt, Decrypt
from utils.StringSplitter import StringSplitter
from contracts.contract import Contract

LARGE_FONT = ("Verdana", 12)
XLARGE_FONT = ("Verdana", 30)


class EndUserApp(tk.Tk):
    contract = None

    userHTTP: UserHTTP
    currentContract: Contract

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.frames = {}

        for F in (StartPage, UploadContract, Signee1, Finish, Signee2, UploadFile, Info1, Info2, Result, ReadContract, Result2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        post_object = {
            'author': "Tester",
            'content': "Hello world!",
        }

        print("Ummmm ---------------")
        self.userHTTP = UserHTTP()
        self.userHTTP.fetch_posts()
        time.sleep(1)
        self.userHTTP.create_new_blockchain_transaction(post_object)
        time.sleep(1)
        print(self.userHTTP.mine_transaction())
        self.currentContract = None

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
            "image/logo.png"))
        logo_label = tk.Label(self, image=self.logo_image)
        logo_label.place(x=2, y=0, relwidth=1, relheight=0.4)

        # image for create contract button
        self.createContact_image = ImageTk.PhotoImage(
            file='image/create.png')

        # image for vefiry contract button
        self.verifyContact_image = ImageTk.PhotoImage(
            file='image/verify.png')

        # image for read contract button
        self.readContact_image = ImageTk.PhotoImage(  # image for read contact button
            file='image/read.png')

        # create contract button
        button = tk.Button(self, image=self.createContact_image, bd=0,
                           command=lambda: controller.show_frame(UploadContract))
        button.place(x=300, y=290)

        # hover animation for create contract
        def create_contract_button_hover(e):
            create_contract_hover_img = ImageTk.PhotoImage(file='image/create_hover.png')
            button["image"] = create_contract_hover_img
            button.image = create_contract_hover_img

        def create_contract_revert(e):
            create_contract_hover_img = ImageTk.PhotoImage(
                file='image/create.png')
            button["image"] = create_contract_hover_img
            button.image = create_contract_hover_img

        button.bind("<Enter>", create_contract_button_hover)
        button.bind("<Leave>", create_contract_revert)

        # verify contract button
        button2 = tk.Button(self, image=self.verifyContact_image, bd=0,
                            command=lambda: controller.show_frame(UploadFile))
        button2.place(x=300, y=375)

        def verify_contract_button_hover(e):
            verify_contract_hover_img = ImageTk.PhotoImage(file='image/verify_hover.png')
            button2["image"] = verify_contract_hover_img
            button2.image = verify_contract_hover_img

        def create_verify_revert(e):
            verify_contract_hover_img = ImageTk.PhotoImage(
                file='image/verify.png')
            button2["image"] = verify_contract_hover_img
            button2.image = verify_contract_hover_img

        button2.bind("<Enter>", verify_contract_button_hover)
        button2.bind("<Leave>", create_verify_revert)

        # read contract button
        button3 = tk.Button(self, image=self.readContact_image,
                            bd=0, command=lambda: controller.show_frame(ReadContract))
        button3.place(x=300, y=460)

        # read contract button hover animation

        def read_contract_button_hover(e):
            read_contract_hover_img = ImageTk.PhotoImage(file='image/read_hover.png')
            button3["image"] = read_contract_hover_img
            button3.image = read_contract_hover_img

        def read_contract_revert(e):
            read_contract_hover_img = ImageTk.PhotoImage(
                file='image/read.png')
            button3["image"] = read_contract_hover_img
            button3.image = read_contract_hover_img

        button3.bind("<Enter>", read_contract_button_hover)
        button3.bind("<Leave>", read_contract_revert)


class UploadContract(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Upload Contract", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.contract = ''
        self.controller = controller

        # image for upload button
        self.UploadContract = ImageTk.PhotoImage(
            file='image/upload.png')

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for upload contract
        button2 = tk.Button(self, text="Page Two",
                            bd=0, image=self.UploadContract, command=lambda: self.uploadfile())
        button2.place(x=280, y=250)

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=450)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: self.onNext())
        button2.place(x=380, y=450)

        # label for file path
        self.path = tk.Label(self, text="No File been upload yet")
        self.path.pack(pady=270, padx=7)

    def uploadfile(self):
        self.contract = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("text", "*.txt"), ("All Files", "*.*")))
        self.path.configure(text=self.contract)
        print(self.contract)

    def onNext(self):
        try:
            EndUserApp.contract = Contract()
            f = open(self.contract, "r")
            text = f.read()
            EndUserApp.contract.data = text
            self.controller.show_frame(Signee1)
        except:
            self.path.configure(text="Please upload a valid contract!")



class Signee1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Signee #1", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.controller = controller

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=275, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=330, y=280, relwidth=0.25, relheight=0.08)

        # enter for name
        nameLabel = tk.Label(self, text="Name", font=LARGE_FONT)
        nameLabel.place(x=275, y=215)
        self.name = tk.Entry(self)
        self.name.place(x=330, y=200, relwidth=0.25, relheight=0.08)

        # button to save
        self.save = ImageTk.PhotoImage(
            file='image/save.png')
        saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
            self.name.get(), self.info.get()))
        saveButton.place(x=530, y=190)

        # label for state
        self.inputState = tk.Label(self, text="")
        self.inputState.place(x=550, y=300)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=380)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: self.onNext())
        button2.place(x=380, y=380)

    def onNext(self):
        name = self.name.get()
        info = self.info.get()
        encrypter = None
        self.controller.show_frame(Signee2)

    def saveInfo(self, name, info):
        print(name)
        print(info)
        self.inputState.configure(text="Save Successful")


class Signee2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Signee #2", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=275, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=330, y=280, relwidth=0.25, relheight=0.08)

        # enter for name
        nameLabel = tk.Label(self, text="Name", font=LARGE_FONT)
        nameLabel.place(x=275, y=215)
        self.name = tk.Entry(self)
        self.name.place(x=330, y=200, relwidth=0.25, relheight=0.08)

        # button to save
        self.save = ImageTk.PhotoImage(
            file='image/save.png')
        saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
            self.name.get(), self.info.get()))
        saveButton.place(x=530, y=190)

        # label for state
        self.inputState = tk.Label(self, text="")
        self.inputState.place(x=550, y=300)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=380)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: controller.show_frame(Finish))
        button2.place(x=380, y=380)

    def saveInfo(self, name, info):
        print(name)
        print(info)
        self.inputState.configure(text="Save Successful")


class Finish(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.finish = ImageTk.PhotoImage(
            file='image/finish1.png')

        self.label = tk.Label(self, image=self.finish, font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        fnishLabel = tk.Label(self, text="Process Completed", font=LARGE_FONT)
        fnishLabel.place(x=320, y=100)

        # button for home page
        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=290, y=450)


class UploadFile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Upload File", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.file = ''

        # image for upload button
        self.UploadContract = ImageTk.PhotoImage(
            file='image/upload.png')

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for upload contract
        button2 = tk.Button(self, text="Page Two",
                            bd=0, image=self.UploadContract, command=lambda: self.uploadfile())
        button2.place(x=280, y=250)

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=450)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: controller.show_frame(Info1))
        button2.place(x=380, y=450)

        # label for file path
        self.path = tk.Label(self, text="No File been upload yet")
        self.path.pack(pady=270, padx=7)

    def uploadfile(self):
        self.file = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
        self.path.configure(text=self.file)
        print(self.file)


class Info1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(
            self, text="Enter your information ", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=75, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=130, y=280, relwidth=0.55, relheight=0.08)

        # button to save
        self.save = ImageTk.PhotoImage(
            file='image/save.png')
        saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
            self.info.get()))
        saveButton.place(x=530, y=235)

        # label for state
        self.inputState = tk.Label(self, text="")
        self.inputState.place(x=550, y=350)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=380)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: controller.show_frame(Info2))
        button2.place(x=380, y=380)

    def saveInfo(self, info):
        print(info)
        self.inputState.configure(text="Save Successful")


class Info2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(
            self, text="Enter person #2 information", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=75, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=130, y=280, relwidth=0.55, relheight=0.08)

        # button to save
        self.save = ImageTk.PhotoImage(
            file='image/save.png')
        saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
            self.info.get()))
        saveButton.place(x=530, y=235)

        # label for state
        self.inputState = tk.Label(self, text="")
        self.inputState.place(x=550, y=350)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=380)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: controller.show_frame(Result))
        button2.place(x=380, y=380)

    def saveInfo(self, info):
        print(info)
        self.inputState.configure(text="Save Successful")


class Result(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # image for result button
        self.result = ImageTk.PhotoImage(
            file='image/result1.png')
        self.label = tk.Label(self, image=self.result)
        self.label.pack(pady=50, padx=10)

        # label for result text
        self.resultText = tk.Label(
            self, text='result text 123 123 123', font=LARGE_FONT)
        self.resultText.pack(pady=60, padx=10)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=290, y=450)


class ReadContract(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Upload File", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.file = ''

        # image for upload button
        self.UploadContract = ImageTk.PhotoImage(
            file='image/upload.png')

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        # image for next button
        self.next = ImageTk.PhotoImage(
            file='image/next1.png')

        # button for upload contract
        button2 = tk.Button(self, text="Page Two",
                            bd=0, image=self.UploadContract, command=lambda: self.uploadfile())
        button2.place(x=280, y=250)

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=490)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: controller.show_frame(Result2))
        button2.place(x=380, y=490)

        # label for file path
        self.path = tk.Label(self, text="No File been upload yet")
        self.path.pack(pady=270, padx=7)

        # label for state
        self.inputState = tk.Label(self, text="")
        self.inputState.place(x=340, y=450)

    def uploadfile(self):
        self.file = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
        self.path.configure(text=self.file)
        print(self.file)
        self.after(3000)
        self.inputState.configure(text="Upload Successful")


class Result2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # image for result button
        self.result = ImageTk.PhotoImage(
            file='image/result1.png')
        self.label = tk.Label(self, image=self.result)
        self.label.pack(pady=50, padx=10)

        # label for result text
        self.resultText = tk.Label(
            self, text='result text 123 123 123', font=LARGE_FONT)
        self.resultText.pack(pady=60, padx=10)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=290, y=450)
