from tkinter import *
from functions import *
from PIL import ImageTk, Image
from threading import Thread

class DisplayStories:
    def __init__(self,win,settings,stories, bookName, bookAuthor, picturesPath, picW=200, picH=240):
        self.window = win
        self.settings = settings
        self.stories = stories
        self.bookName = bookName
        self.bookAuthor = bookAuthor
        self.picturesPath = picturesPath
        self.picW = picW
        self.picH = picH
        self.addTitle()
        self.createMainCanvas()
        win.configure(background='black')
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
        self.row = Label(self.body,foreground='white',background='black')
        self.row.pack(expand=True,fill=BOTH)
        coutner = 0
        for val in self.stories:
            if coutner % 3 == 0 and coutner != 0:
                self.row = Label(self.body,foreground='white',background='black')
                self.row.pack(expand=True,fill=X)
            self.postLine(f'''{val['name']}''',f'''{val['pages']}''', val['id'])
            coutner += 1


    def postLine(self, name,pages, id):
        line = Label(self.row,foreground='white',background='black')
        titleHolder = Label(line, text = name, font=('Arial', 14),foreground='white',background='black')
        titleHolder.pack(fill=X, expand=True)
        pagesHolder = Label(line, text = str(pages) + " Pages", font=('Arial', 14),foreground='white',background='black')
        pagesHolder.pack(fill=X, expand=True)
        path = getExtensionIfExist(self.picturesPath + str(id))
        path = path if path else self.settings['pics']['blank_pic']
        pic = Image.open(path)
        pic = pic.resize((self.picW, self.picH))
        pic = ImageTk.PhotoImage(pic)
        picHolder = Label(line,image = pic,borderwidth=2, relief="raised",foreground='white',background='black')
        picHolder.image = pic
        picHolder.pack()
        line.pack(expand=True,side=LEFT,fill=BOTH)

    def createMainCanvas(self):
        self.canvas = Canvas(self.window,bg='black',highlightthickness=0, highlightbackground='black')
        self.body = Label(self.canvas,background='black',foreground='white')
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.body,anchor='nw',tags='ff')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.body.bind("<Configure>", self.onFrameConfigure)


    def setCanvasSize(self,event):
        self.canvas.itemconfig('ff', width=self.canvas.winfo_width())


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
