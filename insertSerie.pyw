from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
from PIL import ImageTk, Image
from selectCover import CoverSelector
from tkinter.filedialog import askopenfilename
import re
from threading import Thread


class InsertSerie:
    def __init__(self,win,settings,db,autoValues = {},destoryAfter = False,updateID = False, hook = False):
        self.window = win
        self.db = db
        self.sucess = BooleanVar()
        self.settings = settings
        self.destoryAfter = destoryAfter
        self.hook = hook
        self.updateID = updateID
        self.booksCollector = {}
        self.nextId = 1
        self.coverChangerWindow = None
        self.closeOnclick()
        self.addTitle()
        self.addInputs(autoValues)
        self.addInsertButton()


    def addTitle(self):
        Label(self.window,
        text = 'Insert New Books Serie',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=20)


    def addInputs(self,autoValues):
        fram = Label(self.window,background='black',foreground='white')
        self.name = StringVar()
        self.author = StringVar()
        self.addNewLabelAndInput(fram,'Serie Name',1,0,'name')
        self.addNewLabelAndInput(fram,'Author Name',2,0,'author')

        if 'author' in autoValues:
            self.author.set(autoValues['author'])

        if 'name' in autoValues:
            self.name.set(autoValues['name'])

        fram.pack()


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


    def killWindow(self):
        self.window.destroy()
        self.sucess.set(True)


    def addNewLabelAndInput(self,prent,text,row,column,varName):
        innerFrame = Label(prent,background='black',foreground='white')
        label = Label(innerFrame,text=text,background='black',foreground='white')
        label.pack(side=LEFT)
        entry = Entry(innerFrame,textvariable = getattr(self, varName))
        entry.pack(side=RIGHT)
        innerFrame.pack(pady=5,fill=X)


    def addCheckBoxGroup(self,parent,optionJson):
        innerFrame = Label(parent,background='black',foreground='white')
        self.type = StringVar()
        self.type.set(False)
        for cBox in optionJson:
            Checkbutton(innerFrame,onvalue = cBox['value'],text = cBox['text'],variable = self.type).pack(side=LEFT,padx=7,pady=5)
        innerFrame.pack()



    def addInsertButton(self):
        btn = Label(self.window,
        text = 'Save',
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.pack()
        btn.bind('<Button-1>',lambda e: self.checkOut())


    def checkOut(self):
        vars = self.getAllVars()
        check = self.checkVars(vars)
        newId = False
        if check != True:
            messagebox.showerror(title='Error', message=check)
            return

        if self.hook:
            self.hook(self,vars,self.updateID)
            #if set - remove the window
            if self.destoryAfter:
                self.killWindow()

        else:
            newId = insertNewSerie(self.db,self.settings,vars)
            if not str(newId).isdigit():
                insertError(f"""DB error - {newId}""",self.settings['errLog'])
                messagebox.showerror(title='Error', message="Oppsss\nDB error.\nPlease read LOG for mofe info.")
            else:
                messagebox.showinfo('Message',f'''New Books Serie Saved.''')
                self.clearInputs()
                if messagebox.askyesno("Question","Would you like to add a picture?"):
                    filename = askopenfilename()
                    if filename:
                        serieName = str(newId) + getExtensionFromPath(filename)
                        flag = copyFile(filename,self.settings['pics']['seriesFolderPath'] + serieName)
                        if flag != True:
                            insertError(f"""OS error - {flag}""",self.settings['errLog'])
                            messagebox.showerror(title='Error', message="Oppsss\nOS error.\nCould not copy the picture.\nPlease read LOG for mofe info.")
                        else:
                            messagebox.showinfo('Message',f'''Picture Copied.''')
        self.findBooks(vars,newId)


    def findBooks(self,vars,serieId):
        if not serieId:
            return
        if not messagebox.askyesno("Question","Would you like us to find seire's books for you?"):
            return
        self.clearWindow()
        self.resizePopup()
        self.createbooksBase()
        self.closeBooksOnclick()
        self.setFetchingBooksMessage()
        fetchThread = Thread(target = lambda:self.getBooksAndPostThem(vars,serieId))
        fetchThread.deamon = True
        fetchThread.start()


    def getBooksAndPostThem(self,vars,serieId):
        books = getSeriesBook(self.settings,vars['author'],vars['name'])
        if not books:
            messagebox.showerror(title='Error', message="Oppsss\nCould not find books.")
            self.killWindow()
            return
        self.clearFetchingText()
        self.createbooksTitle(vars['name'],vars['author'])
        self.buildBooksBody(books,serieId,vars['author'])
        self.reactToMouseWheel()



    def createbooksTitle(self, name, author):
        Label(self.booksView,
        text = f'''{name} by {author}''',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=(0,10))


    def clearFetchingText(self):
        self.waitingLabel.destroy()


    def addBookOption(self,author):
        l = Label(self.booksView, background='black',foreground = 'white',text = 'Add Another Book To list',font=('Arial',12,'bold'),cursor='hand2')
        l.pack(pady=10)
        l.bind('<Button-1>',lambda *a: self.addBlankBookRow(author))


    def addBlankBookRow(self,author):
        self.saveBooksButton.pack_forget()
        self.postLine('','','','','',author)
        self.saveBooksButton.pack(pady = 10)


    def buildBooksBody(self,books,serieId,author):
        self.addBookOption(author)
        for val in books:
            self.postLine(val['title'],val['number'], val['year'],val['isbn'],val['cover'],author)

        self.saveBooksButton = Label(self.booksView,
        text = 'Save',
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        self.saveBooksButton.pack(pady = 10)
        self.saveBooksButton.bind('<Button-1>',lambda e: self.saveBooks(books,serieId,author))


    def saveBooks(self,books,serieId,author):
        if not self.validateBooks():
            messagebox.showerror(title='Invalid Data', message="Oppsss\nPlease fill all inputs!\nMake sure 'Number in Serie' and 'Publication Year' are just a numbers")
            return

        data = self.collectBooksData(author,serieId)
        bookId = None
        newPicPath = None
        for book in data:
            bookId = insertNewWish(self.db,self.settings,book)
            if not str(bookId).isdigit():
                insertError(f"""DB error - {bookId}""",self.settings['errLog'])
                messagebox.showerror(title='Error', message="Oppsss\nDB error.\nPlease read LOG for mofe info.")
                return
            if book['cover']:
                newPicPath = self.settings['pics']['wishFolderPath'] + '/' + str(bookId) + getExtensionFromPath(book['cover'])
                moveFile(book['cover'],newPicPath,self.settings)

        messagebox.showinfo('Done',f'''Books Saved.''')
        self.closeBookFetcher()


    def collectBooksData(self,author,serieId):
        res = []
        for entryId in self.booksCollector:
            res.append({
            'name':self.booksCollector[entryId]['name'].get().strip(),
            'isbn':self.booksCollector[entryId]['isbn'].get().strip(),
            'year':self.booksCollector[entryId]['year'].get().strip(),
            'cover':self.booksCollector[entryId]['cover'].get().strip(),
            'author':author,
            'serie':{
            'id':serieId,
            'number':self.booksCollector[entryId]['number'].get().strip()
            }
            })
        return res


    def validateBooks(self):
        for entryId in self.booksCollector:
            if( self.booksCollector[entryId]['name'].get().strip() == ''
            or self.booksCollector[entryId]['number'].get().strip() == ''
            or not re.match('^[0-9]+$',self.booksCollector[entryId]['number'].get().strip())
            or self.booksCollector[entryId]['isbn'].get().strip() == ''
            or self.booksCollector[entryId]['year'].get().strip() == ''
            or not re.match('^[0-9]+$',self.booksCollector[entryId]['year'].get().strip()) ):
                return False
        return True


    def closeBooksOnclick(self):
        btn = Label(self.window,
        text = 'X',
        font=('Arial',20,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.pack(side=TOP, anchor=NE,padx=8,pady=5)
        btn.bind('<Button-1>',lambda e: self.closeBookFetcher())


    def postLine(self, name,number,year,isbn,pathCover,author):
        entryId = self.generateId()
        line = Label(self.booksView,foreground='white',background='black')
        mainPicHolder = Label(line,foreground='white',background='black')
        path = pathCover if pathCover else self.settings['pics']['blank_pic']
        pic = Image.open(path)
        pic = pic.resize((self.settings['booksSeries']['picW'], self.settings['booksSeries']['picH']))
        pic = ImageTk.PhotoImage(pic)
        picHolder = Label(mainPicHolder,image = pic,borderwidth=2, relief="raised",foreground='white',background='black')
        picHolder.image = pic
        picHolder.pack(fill=X)
        coverString = StringVar()
        coverInvisibleEntry = Entry(mainPicHolder,textvariable=coverString)
        coverInvisibleEntry.insert(0,pathCover)
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

        removeLabel = Label(dataHolder, foreground='white',background='black',cursor = 'hand2',font=('Arial',12,'bold'),text='Remove This One')
        removeLabel.pack(pady=7)

        titleString = StringVar()
        titleHolder = Label(dataHolder, foreground='white',background='black')
        Label(titleHolder,text="Name: ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        titleEntry = Entry(titleHolder, textvariable = titleString)
        titleEntry.insert(0,name)
        titleEntry.pack(side=RIGHT)
        titleHolder.pack(fill=X,pady=7)

        numberString = StringVar()
        numberHolder = Label(dataHolder,foreground='white',background='black')
        Label(numberHolder,text="Number in Serie ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        numberEntry = Entry(numberHolder, textvariable = numberString)
        numberEntry.insert(0,number)
        numberEntry.pack(side=RIGHT)
        numberHolder.pack(fill=X,pady=7)

        isbnString = StringVar()
        isbnHolder = Label(dataHolder,foreground='white',background='black')
        Label(isbnHolder,text="ISBN ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        isbnEntry = Entry(isbnHolder, textvariable = isbnString)
        isbnEntry.insert(0,isbn)
        isbnEntry.pack(side=RIGHT)
        isbnHolder.pack(fill=X,pady=7)

        yearString = StringVar()
        yearHolder = Label(dataHolder,foreground='white',background='black')
        Label(yearHolder,text="Publication Year: ", font=('Arial', 12),foreground='white',background='black').pack(side=LEFT)
        yearEntry = Entry(yearHolder, textvariable = yearString)
        yearEntry.insert(0,year)
        yearEntry.pack(side=RIGHT)
        yearHolder.pack(fill=X,pady=7)

        dataHolder.pack(side=RIGHT,padx=5)
        line.pack(pady=8)

        changeCoverBtn.bind('<Button-1>',lambda e: self.changeCoverForThisBook(coverString,picHolder,name,author))
        removeLabel.bind('<Button-1>',lambda e: self.removeThisBookEntry(entryId,line))
        self.booksCollector[entryId] = {'name':titleString, 'number':numberString, 'isbn':isbnString, 'year':yearString, 'cover':coverString}


    def removeThisBookEntry(self,entryId,widget):
        widget.destroy()
        del self.booksCollector[entryId]



    def selectLocalBookPicture(self,stringVarPicture,picWidget):
        filename = askopenfilename()
        if not filename:
            return
        pic = Image.open(filename)
        pic = pic.resize((self.settings['booksSeries']['picW'], self.settings['booksSeries']['picH']))
        pic = ImageTk.PhotoImage(pic)
        picWidget.configure(image=pic)
        picWidget.image = pic
        stringVarPicture.set(filename)



    def changeCoverForThisBook(self,coverStringVar, picturePointer,title,author):
        if self.coverChangerWindow:#remove the open one
            self.coverChangerWindow.destroy()
        if messagebox.askyesno("Question","Would you like us to fetch pictures for you?"):
            self.coverChangerWindow =  Toplevel(self.window)
            centerWindow(self.coverChangerWindow,self.settings['covers']['width'],self.settings['covers']['height'])
            trace = CoverSelector(self.coverChangerWindow,self.settings,title,author,None,None,True,False,False)
            _self = self #acess from another class object
            trace.trace.trace("w", lambda *args:_self.updateChangedCover(trace.trace,coverStringVar, picturePointer))#remove overlay indicator to allow another popups
        else:
            self.selectLocalBookPicture(coverStringVar, picturePointer)


    def updateChangedCover(self,StringVarTracer,stringVAR,pictureWidget):
        newVal = StringVarTracer.get()
        if newVal and newVal != '0':
            pic = Image.open(newVal)
            pic = pic.resize((self.settings['booksSeries']['picW'], self.settings['booksSeries']['picH']))
            pic = ImageTk.PhotoImage(pic)
            pictureWidget.configure(image=pic)
            pictureWidget.image = pic
            stringVAR.set(newVal)


    def resizePopup(self):
        self.window.pack_forget()
        self.window.pack(
        side="top",
        fill="both",
        expand=True,
        pady=self.settings['booksSeries']['pady'],
        padx=self.settings['booksSeries']['padx']
        )


    def createbooksBase(self):
        self.canvas = Canvas(self.window,bg='black',highlightthickness=0, highlightbackground='white')
        self.booksView = Label(self.canvas,background='black',foreground='white')
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.booksView, anchor="nw",tags='mainF')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.booksView.bind("<Configure>", self.onFrameConfigure)


    def setFetchingBooksMessage(self):
        self.waitingLabel = Label(self.booksView,text='Fetching, may take a minute...',background='black',foreground='white', font=('Arial', 20))
        self.waitingLabel.pack(side=TOP, expand=YES,pady=150)



    def setCanvasSize(self,event):
        self.canvas.itemconfig('mainF', width=self.canvas.winfo_width())

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()


    def clearInputs(self):
        self.name.set('')
        self.author.set('')


    def checkVars(self,vars):
        if not vars['name']:
            return 'Empty Name'
        if not vars['author']:
            return 'Empty Author'
        return True


    def getAllVars(self):
        res = {}
        res['name'] = self.name.get().strip()
        res['author'] = self.author.get().strip()
        return res

    def reactToMouseWheel(self):
        self.window.bind_all("<MouseWheel>", self.mouseWheelHandle)

    def mouseWheelHandle(self,evt):
         self.canvas.yview_scroll(int(-1*(evt.delta/120)), "units")

    def generateId(self):
        self.nextId += 1
        return self.nextId - 1

    def closeBookFetcher(self):
        clearFolder(self.settings['tmp'])
        self.killWindow()
