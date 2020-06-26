from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class Confirm:
    def __init__(self,win,settings,picPath,string,okBtn1Text,cancelBtn2Text):
        self.window = win
        self.settings = settings
        self.sucess = BooleanVar() # trace
        self.closeOnclick()
        self.addText(string)
        self.addPic(picPath)
        self.addButtons(okBtn1Text,cancelBtn2Text)

    def addButtons(self,okText,cancelText):
        label = Label(self.window,background='white')
        Button(label,
        text = okText,
        command = lambda:self.killWindow(True)
        ).pack(side=LEFT, anchor=SE,padx=60,pady=3)
        Button(label,
        text = cancelText,
        command = self.killWindow
        ).pack(side=LEFT, anchor=SW,padx=60,pady=3)
        label.pack(side=BOTTOM,pady=15)


    def addPic(self,path):
        img = Image.open(path)
        img = img.resize((self.settings['confirm']['picWidth'],self.settings['confirm']['picHeight']))
        img = ImageTk.PhotoImage(img)
        frame = Label(self.window)
        label = Label(frame, image = img,anchor='c')
        label.image = img # keep a reference!
        label.pack()
        frame.pack()#dont pack here- pack in travelers function



    def addText(self,text):
        Label(self.window,
        text = text,
        font=('Arial', 20),
        background='white',
        ).pack(pady=20)


    def closeOnclick(self):
        btn = Button(self.window,
        text = 'X',
        command = self.killWindow
        )
        btn.pack(side=TOP, anchor=NE,padx=3,pady=3)


    def killWindow(self,sucess=False):
        self.window.destroy()
        self.sucess.set(sucess)
