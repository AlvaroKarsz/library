from tkinter import *
from tkinter.ttk import *
from functions import *
from PIL import ImageTk, Image
import re
from tkinter import messagebox
from dbFunctions import *

class bookRead:
    def __init__(self,win,db,settings,title,author,pages,bookID,folderPath, markAsReadedCallback):
        self.window = win
        self.db = db
        self.settings = settings
        self.author = author
        self.title = title
        self.originalPages = pages
        self.id = bookID
        self.picPath = getExtensionIfExist(folderPath + '/' + str(bookID))
        self.date = StringVar()
        self.completed = BooleanVar()
        self.pages = StringVar()
        self.doneFlag = BooleanVar()# flag to update root window when finished
        self.markAsReadedCallback = markAsReadedCallback
        self.setBgColor(win,'black')
        self.configureStyle()
        self.makeHeader()
        self.makeBody()
        self.makeIndicatorLine()
        self.addInputs()
        self.addCommitButton()
        self.setOncloseEventListener()


    def makeIndicatorLine(self):
        Label(self.window,
        text = "Date Examples: Jan 2020 - Mar 2020, Feb 2020",
        font=('Arial', 9,'italic'),
        background='black',
        foreground='white'
        ).pack()


    def configureStyle(self):
        s = Style()
        s.configure('Red.TCheckbutton', foreground='white',background='black',font=('Arial', 14))


    def makeHeader(self):
        Label(self.window,
        text = self.title + " - " + self.author,
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=6)



    def addInputs(self):
        inputsHolder = Label(self.window,background='black',foreground='white')
        self.addNewLabelAndInput(inputsHolder,"When did you read this book:", "date" )
        Checkbutton(inputsHolder,
        text = '''Book wasn't Completed''',
        variable = self.completed,
        style = "Red.TCheckbutton",
        command = lambda : self.completeToggle()
        ).pack()
        self.pagesFrame = self.addNewLabelAndInput(inputsHolder,"How much pages did you read:","pages",False)
        inputsHolder.pack(pady=5, fill=BOTH, expand=True)


    def addCommitButton(self):
        btnHolder = Label(self.window,background='black',foreground='white')

        b = Label(btnHolder,
        text = 'Save',
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        b.pack(pady=7)
        b.bind('<Button-1>',lambda e: self.commit())
        btnHolder.pack(pady=5, fill=BOTH, expand=True)


    def commit(self):
        date = self.date.get().strip()
        completedFlag = self.completed.get()
        pages = self.pages.get().strip()

        date = dateForDB(date)
        if not date: #invalid date
            messagebox.showerror(title='Error', message="Invalid Date Format")
            self.window.lift()
            return

        if completedFlag: #book not completed
            if not re.match('^[0-9]+$',pages): #pages not a number
                messagebox.showerror(title='Error', message="Invalid Number of Pages")
                self.window.lift()
                return
            if int(pages) > int(self.originalPages):
                messagebox.showerror(title='Error', message="There aren't so many pages in this book")
                self.window.lift()
                return
        else: #book completed
            pages = False

        self.markAsReadedCallback(date,self.id, pages)
        self.die()


    def addNewLabelAndInput(self,prent,text,varName, doPack = True):
        innerFrame = Label(prent,background='black',foreground='white')
        label = Label(innerFrame,text=text,background='black',foreground='white', font=('Arial', 14))
        label.pack(side=LEFT, padx=3)
        entry = Entry(innerFrame,textvariable = getattr(self, varName))
        entry.pack(side=RIGHT)
        if doPack:
            innerFrame.pack(pady=7,padx=3)
        return innerFrame

    def makeBody(self):
        self.body = Label(self.window)
        self.body.pack(fill=BOTH,expand=True,padx=10,pady=8)
        self.setBgColor(self.body,'black')
        self.setFgColor(self.body,'white')
        pic = Image.open(self.picPath)
        pic = pic.resize((self.settings['pics']['covers_width'],self.settings['pics']['covers_height']))
        pic = ImageTk.PhotoImage(pic)
        imgHolder = Label(self.body,image = pic)
        imgHolder.image = pic
        imgHolder.pack(side=LEFT,expand=True)
        imgHolder.configure(borderwidth=2, relief="raised")
        self.setFgColor(imgHolder,'white')
        self.setBgColor(imgHolder,'black')



    def setBgColor(self,widget,clr):
        if not isArray(widget):
            widget = [widget]

        for wid in widget:
            try:
                wid.configure(background=clr)
            except:
                try:
                    wid.configure(bg=clr)
                except:
                    continue


    def setFgColor(self,widget,clr):
        if not isArray(widget):
            widget = [widget]
        for wid in widget:
            try:
                wid.configure(foreground=clr)
            except:
                try:
                    wid.configure(fg=clr)
                except:
                    continue


    def completeToggle(self):
        if self.completed.get():
            self.pagesFrame.pack(pady=5,padx=3)
        else:
            self.pagesFrame.pack_forget()

    def die(self):
        self.doneFlag.set(True)
        self.window.destroy()

    def setOncloseEventListener(self):
        self.window.protocol("WM_DELETE_WINDOW", self.die)
