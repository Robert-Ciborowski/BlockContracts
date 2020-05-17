import re
import tkinter as tk
from hashlib import sha256

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
    userHTTP = UserHTTP
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

        # post_object = {
        #     'content': "Hello world!",
        # }

        EndUserApp.userHTTP = UserHTTP()
        # EndUserApp.userHTTP.create_new_blockchain_transaction(post_object)
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
        logo_label.place(x=2, y=0, relwidth=1, relheight=0.4)

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
                            bd=0,
                            command=lambda: controller.show_frame(ReadContract))
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
        button = tk.Button(self, text="Page Two",
                            bd=0, image=self.UploadContract,
                            command=lambda: self.uploadfile())
        button.place(x=280, y=250)

        # upload hover animations
        def upload_hover(e):
            upload_hover_img = ImageTk.PhotoImage(file='image/upload_hover.png')
            button['image'] = upload_hover_img
            button.image = upload_hover_img

        def upload_revert(e):
            upload_hover_img = ImageTk.PhotoImage(file='image/upload.png')
            button['image'] = upload_hover_img
            button.image = upload_hover_img

        button.bind("<Enter>", upload_hover)
        button.bind('<Leave>', upload_revert)

        # button for home page
        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=180, y=450)

        # home button hover animations
        def home_hover(e):
            upload_hover_img = ImageTk.PhotoImage(file='image/home_hover.png')
            button1['image'] = upload_hover_img
            button1.image = upload_hover_img

        def home_revert(e):
            upload_hover_img = ImageTk.PhotoImage(file='image/home.png')
            button1['image'] = upload_hover_img
            button1.image = upload_hover_img

        button1.bind("<Enter>", home_hover)
        button1.bind('<Leave>', home_revert)

        # button for next page
        button_next = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: self.onNext())
        button_next.place(x=380, y=450)

        # next button hover animation
        def next_hover(e):
            next_hover_img = ImageTk.PhotoImage(file='image/next_hover.png')
            button_next['image'] = next_hover_img
            button_next.image = next_hover_img

        def next_revert(e):
            next_hover_img = ImageTk.PhotoImage(file='image/next1.png')
            button_next['image'] = next_hover_img
            button_next.image = next_hover_img

        button_next.bind("<Enter>", next_hover)
        button_next.bind('<Leave>', next_revert)

        # label for file path
        self.path = tk.Label(self, text="No File been upload yet")
        self.path.pack(pady=270, padx=7)

    def uploadfile(self):
        self.contract = filedialog.askopenfilename(
            initialdir="/", title="Select A File",
            filetype=(("text", "*.txt"), ("All Files", "*.*")))
        self.path.configure(text=self.contract)

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
                                              "very ambiguous.\nYou may want to "
                                              "rewrite the contract or refuse "
                                              "to sign it.")
        else:
            tk.messagebox.showwarning(title="Your contract",
                                      message="The contract you submitted has "
                                              "been flagged by the system as "
                                              "safe! :)")


class Signee1(tk.Frame):
    signee1Name = ""
    signee1Key = ""

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
        Signee1.signee1Key = sha256(info.encode(encoding='UTF-8')).hexdigest()
        EndUserApp.contract.data += "\n#~#~" + name + "," + Signee1.signee1Key
        EndUserApp.contract.add_digital_signature(Signee1.signee1Key)
        self.controller.show_frame(Signee2)

    def saveInfo(self, name, info):
        self.inputState.configure(text="Save Successful")


class Signee2(tk.Frame):
    signee2Name = ""
    signee2Key = ""

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

        Signee2.signee2Name = name
        Signee2.signee2Key = sha256(info.encode(encoding='UTF-8')).hexdigest()
        EndUserApp.contract.data += "," + name + "," + Signee2.signee2Key
        EndUserApp.contract.add_digital_signature(Signee2.signee2Key)
        Finish.uploadContract()
        self.controller.show_frame(Finish)

    def saveInfo(self, name, info):
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
        encrypted_data, key = EndUserApp.contract.encrypt_data()
        encrypted_data = str(encrypted_data, "utf-8")
        key = str(key, "utf-8")

        post_object = {
            'content': encrypted_data,
        }

        userHTTP = UserHTTP()
        userHTTP.create_new_blockchain_transaction(post_object)
        code, text = userHTTP.mine_transaction()

        if code != 200:
            Finish.finishLabel.configure(text="There was an error with creating your secure contract!")
        else:
            try:
                EndUserApp.contract.block_of_chain = int(text)
                path1 = "./contracts/" + Signee1.signee1Name + ".contract"
                path2 = "./contracts/" + Signee2.signee2Name + ".contract"
                EndUserApp.contract.encryption_key = key
                EndUserApp.contract.export_to_files(path1, 0)
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
        self.label = tk.Label(self, text="Upload your .contract file", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.file = ''
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
        self.file = filedialog.askopenfilename(
            initialdir="/", title="Select A File",
            filetype=(("contract", "*.contract"), ("All Files", "*.*")))
        self.path.configure(text=self.file)
        print(self.file)

    def onNext(self):
        try:
            EndUserApp.contract = Contract()
            f = open(self.file, "r")
            text = f.read()
            text = re.split(r',|\n', text)
            EndUserApp.contract.encryption_key = text[3]
            EndUserApp.contract.block_of_chain = int(text[4])
            EndUserApp.contract.add_digital_signature(text[5])
            self.controller.show_frame(Info1)
        except:
            self.path.configure(text="Please upload a valid .contract file!")


class Info1(tk.Frame):
    Signee1Info = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(
            self, text="Enter your information ", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.controller = controller

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=75, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=130, y=280, relwidth=0.55, relheight=0.08)

        # button to save
        # self.save = ImageTk.PhotoImage(
        #     file='image/save.png')
        # saveButton = tk.Button(self, image=self.save, bd=0,
        #                        command=lambda: self.saveInfo(
        #                            self.info.get()))
        # saveButton.place(x=530, y=235)

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
                            command=lambda: self.onNext())
        button2.place(x=380, y=380)

    def saveInfo(self, info):
        self.inputState.configure(text="Save Successful")

    def onNext(self):
        info = self.info.get()

        if info == "":
            tk.messagebox.showerror(title="Error",
                                    message="Info is invalid!")
            return

        Info1.Signee1Info = info
        self.controller.show_frame(Info2)


class Info2(tk.Frame):
    Signee2Info = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(
            self, text="Enter person #2 information", font=XLARGE_FONT)
        self.label.pack(pady=50, padx=10)
        self.controller = controller

        # enter for info
        infoLabel = tk.Label(self, text="Info", font=LARGE_FONT)
        infoLabel.place(x=75, y=295)
        self.info = tk.Entry(self)
        self.info.place(x=130, y=280, relwidth=0.55, relheight=0.08)

        # button to save
        # self.save = ImageTk.PhotoImage(
        #     file='image/save.png')
        # saveButton = tk.Button(self, image=self.save, bd=0,
        #                        command=lambda: self.saveInfo(
        #                            self.info.get()))
        # saveButton.place(x=530, y=235)

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
                            command=lambda: self.onNext())
        button2.place(x=380, y=380)

    def saveInfo(self, info):
        self.inputState.configure(text="Save Successful")

    def onNext(self):
        info = self.info.get()

        if info == "":
            tk.messagebox.showerror(title="Error",
                                    message="Info is invalid!")
            return

        Info2.Signee2Info = info

        # verify results with blockchain!
        posts = EndUserApp.userHTTP.fetch_posts()
        whichPost = EndUserApp.contract.block_of_chain

        if len(posts) <= whichPost - 1:
            tk.messagebox.showerror(title="Error",
                                    message="Error!")
            return

        try:
            post = posts[len(posts) - whichPost]
            content = post["content"]
            decrypt = Decrypt()
            content = decrypt.unscramble(bytes(EndUserApp.contract.encryption_key, 'utf8'),
                                         content)
            content = str(content).split("#~#~")
            content = content[1].split(",")
            info1 = content[1]
            info2 = content[3]

            matchingInfo1 = sha256(Info1.Signee1Info.encode(encoding='UTF-8')).hexdigest()
            matchingInfo2 = sha256(Info2.Signee2Info.encode(encoding='UTF-8')).hexdigest()
            successString = ""

            info2 = info2[0 : len(info2) - 1]

            if info1 == matchingInfo1:
                successString += "Signee #1 has signed this contract.\n"
            else:
                successString += "Signee #1 has NOT signed this contract.\n"

            if info2 == matchingInfo2:
                successString += "Signee #2 has signed this contract."
            else:
                successString += "Signee #2 has NOT signed this contract."

        except:
            print("Error!!!")
            successString = "An error occurred when processing " \
                                  "verification. Your contract file must be "\
                            "invalid."

        Result.resultText.configure(text=successString)
        self.controller.show_frame(Result)

class Result(tk.Frame):
    resultText = None

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
        Result.resultText = self.resultText

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
        button1.place(x=180, y=490)

        # button for next page
        button2 = tk.Button(self, text="Page Two", bd=0, image=self.next,
                            command=lambda: self.onNext())
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
            filetype=(("contract", "*.contract"), ("All Files", "*.*")))
        self.path.configure(text=self.file)
        self.after(3000)
        self.inputState.configure(text="Upload Successful")

    def onNext(self):
        try:
            EndUserApp.contract = Contract()
            f = open(self.file, "r")
            text = f.read()
            text = re.split(r',|\n', text)
            EndUserApp.contract.encryption_key = text[3]
            EndUserApp.contract.block_of_chain = int(text[4])
            EndUserApp.contract.add_digital_signature(text[5])

            # verify results with blockchain!
            posts = EndUserApp.userHTTP.fetch_posts()
            whichPost = EndUserApp.contract.block_of_chain

            if len(posts) <= whichPost - 1:
                tk.messagebox.showerror(title="Error",
                                        message="Error!")
                return

            post = posts[len(posts) - whichPost]
            content = post["content"]
            decrypt = Decrypt()
            content = decrypt.unscramble(
                bytes(EndUserApp.contract.encryption_key, 'utf8'),
                content)
            content = str(content).split("#~#~")[0]
            path = "./saved_contracts/exported_contract.txt"
            print(path)
            f.close()

            try:
                f = open(path, "w+")
                f.write(content)
                f.close()
            except:
                self.path.configure(text="Error with contract!")
                return

            self.controller.show_frame(Result2)

        except:
            self.path.configure(text="Please upload a valid .contract file!")



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
            self, text='Export complete: saved_contracts/exported_contract.txt', font=LARGE_FONT)
        self.resultText.pack(pady=60, padx=10)

        # image for home button
        self.home = ImageTk.PhotoImage(
            file='image/home.png')

        button1 = tk.Button(self, text="Back to Home", bd=0, image=self.home,
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=290, y=450)
