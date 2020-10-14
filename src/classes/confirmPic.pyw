from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class Confirm:
    def __init__(self,win,settings,picPath,string=None,okBtn1Text=None,cancelBtn2Text=None):
        self.window = win
        self.settings = settings
        self.sucess = BooleanVar() # trace
        self.closeOnclick()
        self.addText(string)
        self.addPic(picPath)
        self.addButtons(okBtn1Text,cancelBtn2Text)

    def addButtons(self,okText,cancelText):
        if not okText or not cancelText:
            return
        label = Label(self.window,background='black',foreground='white')

        okBtn = Label(label,
        text = okText,
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        okBtn.pack(side=LEFT, anchor=SE,padx=60,pady=3)
        okBtn.bind('<Button-1>',lambda e: self.killWindow(True))

        noBtn = Label(label,
        text = cancelText,
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        noBtn.pack(side=LEFT, anchor=SW,padx=60,pady=3)
        noBtn.bind('<Button-1>',lambda e: self.killWindow())

        label.pack(side=BOTTOM,pady=15)


    def addPic(self,path):
        img = Image.open(path)
        img = img.resize((self.settings['confirm']['picWidth'],self.settings['confirm']['picHeight']))
        img = ImageTk.PhotoImage(img)
        frame = Label(self.window,background='black',foreground='white')
        label = Label(frame, image = img,anchor='c',background='black',foreground='white')
        label.image = img # keep a reference!
        label.pack()
        frame.pack()#dont pack here- pack in travelers function



    def addText(self,text):
        if not text:
            return
        Label(self.window,
        text = text,
        font=('Arial', 20),
        background='black',foreground='white'
        ).pack(pady=20)


    def closeOnclick(self):
        btn = Label(self.window,
        text = 'X',
        font=('Arial',20,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.pack(side=TOP, anchor=NE,padx=8,pady=5)
        btn.bind('<Button-1>',lambda e: self.killWindow())


    def killWindow(self,sucess=False):
        self.window.destroy()
        self.sucess.set(sucess)
