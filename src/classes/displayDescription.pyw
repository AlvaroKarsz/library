from tkinter import *
from functions import *
from PIL import ImageTk, Image
from threading import Thread

class Description:
    def __init__(self,win,name,author,isbn,id,picFolder,settings):
        self.window = win
        self.setBgColor(win,'black')
        self.addTitle(name,author)
        self.createMainCanvas()
        self.addPic(picFolder,id)
        self.addDescription()
        fetchDescriptionThread = Thread(target = lambda: self.updateDescription(getBookDescription(isbn,settings)))
        fetchDescriptionThread.daemon = True
        fetchDescriptionThread.start()


    def updateDescription(self,desc):
        self.descriptionLabel['text'] = desc if desc else 'Nothing Found...'
        #to handle the dissapearing pictures bug
        self.picLabel.pack_forget()
        self.picLabel.pack()





    def addTitle(self,bookName,bookAuthor):
        Label(self.window,
        text = f'''{bookName} by {bookAuthor}''',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=20)

    def addPic(self,folderPath,id):
        path = getExtensionIfExist(folderPath + str(id))
        self.img = Image.open(path)
        self.img = self.img.resize((300,360))
        self.img = ImageTk.PhotoImage(self.img)
        self.picFrame = Label(self.body,background='black',foreground='white')
        self.picLabel = Label(self.picFrame, image = self.img,anchor='c',background='black',foreground='white',borderwidth=2, relief="raised")
        self.picLabel.image = self.img # keep a reference!
        self.picLabel.pack()
        self.picFrame.pack()#dont pack here- pack in travelers function


    def addDescription(self):
        self.descriptionLabel = Label(self.body,
        background='black',
        foreground='white',
        text = "Fetching...",
        font=('Arial', 14),
        wraplengt = 500,
        anchor='w'
        )
        self.descriptionLabel.pack()


    def createMainCanvas(self):
        self.canvas = Canvas(self.window,bg='black',highlightthickness=0, highlightbackground='black')
        self.body = Label(self.canvas)
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.body, anchor="nw",tags='ff')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.body.bind("<Configure>", self.onFrameConfigure)
        self.setBgColor(self.body,'black')
        self.setFgColor(self.body,'white')


    def setCanvasSize(self,event):
        self.canvas.itemconfig('ff', width=self.canvas.winfo_width())


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


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
