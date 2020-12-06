from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from threading import Thread
from tkinter import messagebox
from functions import *

class AuthorBooks:
    def __init__(self,win,settings,author):
        self.window = win
        self.settings = settings
        self.author = author
        self.clearWindow()
        self.createbooksBase()
        self.closeBooksOnclick()
        self.setFetchingBooksMessage()
        fetchThread = Thread(target = lambda:self.getBooksAndPostThem())
        fetchThread.deamon = True
        fetchThread.start()


    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()


    def closeBooksOnclick(self):
        btn = Label(self.mainWid,
        text = 'X',
        font=('Arial',20,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.pack(side=TOP, anchor=NE,padx=8,pady=5)
        btn.bind('<Button-1>',lambda e: self.clearAndCloseOverlay())


    def clearAndCloseOverlay(self):
        clearFolder(self.settings['tmp'])
        self.killWindow()


    def killWindow(self):
        self.window.destroy()


    def setFetchingBooksMessage(self):
        self.waitingLabel = Label(self.mainWid,text='Fetching, may take a minute...',background='black',foreground='white', font=('Arial', 20))
        self.waitingLabel.pack(side=TOP, expand=YES,pady=150)


    def clearFetchingText(self):
        self.waitingLabel.destroy()


    def createbooksTitle(self):
        Label(self.mainWid,
        text = f'''{self.author} Books''',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=(0,10))


    def getBooksAndPostThem(self):
        books = getMoreBooksFromThisAuthor(self.author,self.settings)
        if not books:
            messagebox.showerror(title='Error', message="Oppsss\nCould not find books.")
            self.killWindow()
            return

        self.clearFetchingText()
        self.createbooksTitle()
        self.buildBooksBody(books)


    def buildBooksBody(self,books):
        for val in books:
            self.postBook(val['title'],val['publication'],val['isbn13'] if val['isbn13'] else val['isbn10'],val['description'],f'''{val['rating']}/5 ({val['ratingCount']})''',val['cover'])


    def postBook(self, title,year,isbn,description,rating,cover):
        line = Label(self.mainWid,foreground='white',background='black')
        mainPicHolder = Label(line,foreground='white',background='black')
        path = cover if cover else self.settings['pics']['blank_pic']
        pic = Image.open(path)
        pic = pic.resize((self.settings['booksSeries']['picW'], self.settings['booksSeries']['picH']))
        pic = ImageTk.PhotoImage(pic)
        picHolder = Label(mainPicHolder,image = pic,borderwidth=2, relief="raised",foreground='white',background='black')
        picHolder.image = pic
        picHolder.pack(fill=X)
        coverString = StringVar()
        changeCoverBtn = Label(mainPicHolder,
        text = 'Change Cover',
        font=('Arial',10,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        changeCoverBtn.pack()
        mainPicHolder.pack(side=LEFT)


        dataHolder = Label(line,foreground='white',background='black')

        titleHolder = Label(dataHolder, foreground='white',background='black')
        Label(titleHolder,text="Name: ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        titleEntry = Entry(titleHolder)
        titleEntry.insert(0,title)
        titleEntry.pack(side=RIGHT)
        titleHolder.pack(fill=X,pady=7)

        ratingHolder = Label(dataHolder,foreground='white',background='black')
        Label(ratingHolder,text="Rating ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        ratingEntry = Entry(ratingHolder)
        ratingEntry.insert(0,rating)
        ratingEntry.pack(side=RIGHT)
        ratingHolder.pack(fill=X,pady=7)


        isbnHolder = Label(dataHolder,foreground='white',background='black')
        Label(isbnHolder,text="ISBN ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        isbnEntry = Entry(isbnHolder)
        isbnEntry.insert(0,isbn)
        isbnEntry.pack(side=RIGHT)
        isbnHolder.pack(fill=X,pady=7)

        yearHolder = Label(dataHolder,foreground='white',background='black')
        Label(yearHolder,text="Publication Year: ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        yearEntry = Entry(yearHolder)
        yearEntry.insert(0,year)
        yearEntry.pack(side=RIGHT)
        yearHolder.pack(fill=X,pady=7)

        descriptionHolder = Label(dataHolder,foreground='white',background='black')
        Label(descriptionHolder,text="Description: ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        descriptionEntry = Text(descriptionHolder,width=40, height=5)
        descriptionEntry.insert(INSERT, description)
        descriptionEntry.pack(side=RIGHT)
        descriptionHolder.pack(fill=X,pady=7)

        dataHolder.pack(side=RIGHT,padx=5)
        line.pack(pady=8)



    def createbooksBase(self):
        self.canvas = Canvas(self.window,bg='black',highlightthickness=0, highlightbackground='white')
        self.mainWid = Label(self.canvas,background='black',foreground='white')
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.mainWid, anchor="nw",tags='mainF')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.mainWid.bind("<Configure>", self.onFrameConfigure)

    def setCanvasSize(self,event):
        self.canvas.itemconfig('mainF', width=self.canvas.winfo_width())

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
