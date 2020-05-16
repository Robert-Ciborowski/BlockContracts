import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog, messagebox
import image
import time as time
from user_http import UserHTTP

from ml.AmbiguityDetector import AmbiguityDetector
from ml.LayerParameter import LayerParameter
from utils.cypter import Encrypt, Decrypt
from utils.StringSplitter import StringSplitter
from contracts.contract import Contract

LARGE_FONT = ("Verdana", 12)
XLARGE_FONT = ("Verdana", 30)


class EndUserApp(tk.Tk):
    contract = None
    userHTTP: UserHTTP
    currentContract: Contract
    model = None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.frames = {}

        for F in (
        StartPage, UploadContract, Signee1, Finish, Signee2, UploadFile, Info1,
        Info2, Result, ReadContract, Result2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        post_object = {
            'content': "Hello world!",
        }

        self.userHTTP = UserHTTP()
        self.userHTTP.fetch_posts()
        self.userHTTP.create_new_blockchain_transaction(post_object)
        print(self.userHTTP.mine_transaction())
        self.currentContract = None

        EndUserApp.model = AmbiguityDetector()
        EndUserApp.model.setupWithDefaultValues("../../ml/data/sarcasm.json")

        layerParameters = [
            LayerParameter(24, "relu")
        ]

        EndUserApp.model.createModel(layerParameters)
        EndUserApp.model.exportPath = "../../ml/exports/ambiguitydetector"
        EndUserApp.model.load()

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
        logo_label.place(relwidth=1, relheight=0.4)

        # image for create contract button
        self.createContact_image = ImageTk.PhotoImage(
            file='image/create.png')

        # image for vefiry contract button
        self.verifyContact_image = ImageTk.PhotoImage(
            file='image/verify.png')

        # image for read contract button
        self.readContact_image = ImageTk.PhotoImage(
            # image for read contact button
            file='image/read.png')

        # create contract button
        button = tk.Button(self, image=self.createContact_image, bd=0,
                           command=lambda: controller.show_frame(
                               UploadContract))
        button.place(x=300, y=290)

        # verify contract button
        button2 = tk.Button(self, image=self.verifyContact_image, bd=0,
                            command=lambda: controller.show_frame(UploadFile))
        button2.place(x=300, y=375)

        # read contract button
        button3 = tk.Button(self, image=self.readContact_image,
                            bd=0,
                            command=lambda: controller.show_frame(ReadContract))
        button3.place(x=300, y=460)


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
                            bd=0, image=self.UploadContract,
                            command=lambda: self.uploadfile())
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
            initialdir="/", title="Select A File",
            filetype=(("text", "*.txt"), ("All Files", "*.*")))
        self.path.configure(text=self.contract)
        print(self.contract)

    def onNext(self):
        text = ""

        try:
            EndUserApp.contract = Contract()
            f = open(self.contract, "r")
            text = f.read()
            EndUserApp.contract.data = text
            self.controller.show_frame(Signee1)
        except:
            self.path.configure(text="Please upload a valid contract!")
            return

        string_splitter = StringSplitter(text)
        string_splitter.string_splitter(EndUserApp.model.maxInputLength)
        values = string_splitter.show_list()
        is_ambiguous = EndUserApp.model.detect(values)

        if is_ambiguous:
            tk.messagebox.showwarning(title="Your contract",
                                      message="The contract you submitted has "
                                              "been flagged by the system as "
                                              "ambiguous.\nYou may want to "
                                              "rewrite the contract or refuse "
                                              "to sign it.")
        else:
            tk.messagebox.showwarning(title="Your contract",
                                      message="The contract you submitted has "
                                              "been flagged by the system as "
                                              "safe! :)")




class Signee1(tk.Frame):
    signee1Name = ""

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
        # self.save = ImageTk.PhotoImage(
        #     file='image/save.png')
        # saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
        #     self.name.get(), self.info.get()))
        # saveButton.place(x=530, y=190)

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

        if name == "" or info == "":
            tk.messagebox.showerror(title="Error",
                                    message="Name or info is invalid!")
            return

        Signee1.signee1Name = name

        # encrypt = Encrypt()
        # add stuff like info = encrypt.scramble(encrypt)
        # encrypt.scramble()
        EndUserApp.contract.data += "\n " + name + ": " + info + ", "
        EndUserApp.contract.add_digital_signature(info)
        self.controller.show_frame(Signee2)

    def saveInfo(self, name, info):
        print(name)
        print(info)
        self.inputState.configure(text="Save Successful")


class Signee2(tk.Frame):
    signee2Name = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Signee #2", font=XLARGE_FONT)
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
        # self.save = ImageTk.PhotoImage(
        #     file='image/save.png')
        # saveButton = tk.Button(self, image=self.save, bd=0, command=lambda: self.saveInfo(
        #     self.name.get(), self.info.get()))
        # saveButton.place(x=530, y=190)

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

        if name == "" or info == "":
            tk.messagebox.showerror(title="Error",
                                    message="Name or info is invalid!")
            return

        Signee2.signee2Name = name

        # encrypt = Encrypt()
        # add stuff like info = encrypt.scramble(encrypt)
        # encrypt.scramble()
        EndUserApp.contract.data += name + ": " + info + ", "
        EndUserApp.contract.add_digital_signature(info)
        Finish.uploadContract()
        self.controller.show_frame(Finish)

    def saveInfo(self, name, info):
        print(name)
        print(info)
        self.inputState.configure(text="Save Successful")


class Finish(tk.Frame):
    finishLabel = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.finish = ImageTk.PhotoImage(
            file='image/finish1.png')
        self.label = tk.Label(self, image=self.finish, font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)

        finishLabel = tk.Label(self, text="placeholder", font=LARGE_FONT)
        finishLabel.place(x=320, y=100)
        Finish.finishLabel = finishLabel

        # button for home page
        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=290, y=450)

    @staticmethod
    def uploadContract():
        encrypted_data = EndUserApp.contract.encrypt_data()

        post_object = {
            'content': "Hello world!",
        }

        userHTTP = UserHTTP()
        userHTTP.create_new_blockchain_transaction(post_object)
        code, text = userHTTP.mine_transaction()

        if code != 200:
            print("HTTP Error " + str(code))
            Finish.finishLabel.configure(text="There was an error with creating your secure contract!")
        else:
            try:
                print(text)
                EndUserApp.contract.block_of_chain = int(text)
                path1 = "./contracts/" + Signee1.signee1Name + ".contract"
                path2 = "./contracts/" + Signee2.signee2Name + ".contract"
                print("sdsdsd")
                EndUserApp.contract.export_to_files(path1, 0)
                print("sdsdsd")
                EndUserApp.contract.export_to_files(path2, 1)
                Finish.finishLabel.configure(text="Your secure contract has been completed." \
                                     "\nSignee #1: " + path1 + "\nSignee #2: " + path2)
            except IOError as e:
                print(e)
                Finish.finishLabel.configure(text="There was an error with exporting your contract!")
            except:
                print("Error creating final .contract file!")
                Finish.finishLabel.configure(text="There was an error with exporting your contract!")

        EndUserApp.currentContract = None


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
                            bd=0, image=self.UploadContract,
                            command=lambda: self.uploadfile())
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
            initialdir="/", title="Select A File",
            filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
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
        saveButton = tk.Button(self, image=self.save, bd=0,
                               command=lambda: self.saveInfo(
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
        saveButton = tk.Button(self, image=self.save, bd=0,
                               command=lambda: self.saveInfo(
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
                            bd=0, image=self.UploadContract,
                            command=lambda: self.uploadfile())
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
            initialdir="/", title="Select A File",
            filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
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
