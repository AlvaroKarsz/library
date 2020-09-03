from tkinter import *
from functions import *
from PIL import ImageTk, Image
from threading import Thread


class DisplayStories:
    def __init__(self,win,stories, bookName, bookAuthor, picturesPath, picW=90, picH=120):
        self.window = win
        self.stories = stories
        self.bookName = bookName
        self.bookAuthor = bookAuthor
        self.picturesPath = picturesPath
        self.picW = picW
        self.picH = picH
        self.addTitle()
        self.createMainCanvas()
        self.setBgColor(win,'black')
        bodyBuilderThread = Thread(target = lambda: self.buildBody())
        bodyBuilderThread.daemon = True
        bodyBuilderThread.start()



    def addTitle(self):
        Label(self.window,
        text = f'''{self.bookName} Stories({len(self.stories)})''',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=20)


    def buildBody(self):
        for val in self.stories:
            self.postLine(self.body, f'''{val['name']}''',f'''{val['pages']}''', val['id'])



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


    def postLine(self, parent, name,pages, id):
        path = getExtensionIfExist(self.picturesPath + str(id))
        pic = Image.open(path)
        pic = pic.resize((self.picW, self.picH))
        pic = ImageTk.PhotoImage(pic)
        line = Label(parent)
        line.pack(fill=X,expand=True)
        picHolder = Label(line,image = pic)
        picHolder.image = pic
        picHolder.pack(side=LEFT)
        dataHolder = Label(line)
        dataHolder.pack(side=LEFT)
        titleHolder = Label(dataHolder, text = name, font=('Arial', 14))
        titleHolder.pack(fill=X, expand=True)
        pagesHolder = Label(dataHolder, text = str(pages) + " Pages", font=('Arial', 14))
        pagesHolder.pack(fill=X, expand=True)
        self.setBgColor([pagesHolder,titleHolder,dataHolder,picHolder,line],'black')
        self.setFgColor([pagesHolder,titleHolder,dataHolder,picHolder,line],'white')


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
