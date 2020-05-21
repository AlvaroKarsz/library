from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import *
from PIL import ImageTk, Image
from dbFunctions import *
from functions import *
import re
from tkinter import font
from threading import Thread
from insertBook import InsertBook
from stories import Stories
from books import Books
from tkinter import messagebox

class App:
    def __init__(self,win,settings,db):
        self.window = win
        self.db = db
        self.nameFilterStr = 'nF'
        self.authorFilterStr = 'aF'
        self.settings = settings
        self.canvas = None
        self.nextSum = True
        self.goNextBind = None
        self.currentImageHodler = None
        self.goPrevBind = None
        self.nameValueFilter = ''
        self.authorValueFilter = ''
        self.currPage = 1
        self.totalPages = 1#default untill books loads
        self.booksCount = 1#default untill books loads
        self.currentOverlay = None
        self.perRow = settings['booksDisplayPreRow']
        centerWindow(win,settings['gui']['width'],settings['gui']['height'])
        self.addTopNav()
        self.addHeader()
        self.createView()
        self.loadBooks(True)#the default one is books, true to avoid loading the books, it will load next
        self.markRelevantLibrary()
        self.displyBooksThread()
        self.fitlerOnKeyUp()

    def filterYourself(self,event):
        if event.keycode != 13:
            return
        self.filter()


    def filter(self):
        self.killOverlay()
        self.goUp()
        self.readFilters()
        self.toggleBooks()
        self.removeBooks()
        self.resetYourCurrPage()
        self.resetCountRelevantBooks()
        self.updateBookCountIndicator()
        self.pagesLabel['text'] = "Page: 1/" + str(self.totalPages)
        self.updatePageNavigators()
        self.displyBooksThread()
        self.reCenterBooks()


    def displyBooksThread(self):
        id = getRandomNumber()
        self.currentThread = id
        thread = Thread(target = lambda: self.displayBooks(id))
        self.killThreadWhenWindowIsClosed(thread)
        thread.start()


    def markRelevantLibrary(self):
        mark = True
        for i,book in enumerate(self.data):
            if i == self.settings['maxBooksFetch']:
                mark = False
            book['relevant'] = mark


    def fitlerOnKeyUp(self):
        getattr(self,self.nameFilterStr).bind('<KeyRelease>', self.filterYourself)
        getattr(self,self.authorFilterStr).bind('<KeyRelease>', self.filterYourself)


    def reCenterBooks(self):
        currentW = self.window.winfo_width()
        currentH = self.window.winfo_height()
        maxW = self.window.winfo_screenwidth()
        w = currentW
        h = currentH

        if maxW == currentW:
            w -= 1
        else:
            if self.nextSum:
                w += 1
            else:
                w -= 1

        self.window.geometry('%dx%d' % (w, h))
        self.nextSum = not self.nextSum


    def goUp(self):
        self.canvas.yview_moveto(0.0)


    def toggleBooks(self):
        counter = 0
        for book in self.data:
            if counter >= self.settings['maxBooksFetch']:
                book['relevant'] = False
            else:
                if includeInsensitive(book['name'],self.nameValueFilter) and includeInsensitive(book['author'],self.authorValueFilter):
                    counter += 1
                    book['relevant'] = True
                else:
                    book['relevant'] = False


    def createView(self):
        if not self.canvas:
            self.canvas = Canvas(self.window)
        self.booksView = Frame(self.canvas)
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.booksView, anchor="nw",tags='mainF')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.booksView.bind("<Configure>", self.onFrameConfigure)


    def setCanvasSize(self,event):
        self.canvas.itemconfig('mainF', width=self.canvas.winfo_width())



    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def displayBooks(self,threadID):
        counter = 0
        for i,book in enumerate(self.data):
            if self.currentThread != threadID: # a new thread is running
                return
            if book['relevant']:
                self.addBookView(book,counter)
                counter += 1

        self.padTheRowWithBlankRows()


    def killThreadWhenWindowIsClosed(self,thr):
        thr.daemon = True


    def removeBooks(self):
        self.canvas.delete("all")
        self.scroll.destroy()
        self.createView()


    def addPic(self,name,parent,bigSize = False):
        path = name.replace(':','.').replace('/','.').lower()
        path = self.picFolder + re.sub('\s+','',path)
        path = getExtensionIfExist(path)
        path = path if path else self.settings['pics']['blank_pic']
        return self.postPic(path,parent,bigSize)


    def postPic(self,path,parent,bigSize):
        width = self.settings['pics']['width_big'] if bigSize else self.settings['pics']['width']
        height = self.settings['pics']['height_big'] if bigSize else self.settings['pics']['height']
        img = Image.open(path)
        img = img.resize((width,height))
        img = ImageTk.PhotoImage(img)
        frame = Label(parent) if not self.currentImageHodler else self.currentImageHodler
        label = Label(frame, image = img,anchor='c')
        if not bigSize:
            label.configure(cursor="hand2")
        label.image = img # keep a reference!
        if bigSize: # to allow the travelers buttons
            label.pack(side=LEFT)
        else :
            label.pack()
            frame.pack()#dont pack here- pack in travelers function
        return label


    def addBookView(self,book,index):
        if index % self.perRow == 0:
            self.currentRow = Frame(self.booksView)
            self.currentRow.pack(fill=BOTH,expand=True)

        bookView = Frame(self.currentRow)
        title = Label(bookView,
        text = book['name'],
        anchor='c',
        font=('Arial', 14),
        wraplengt = self.settings['pics']['width']
        )
        title.pack(expand = True,fill = X)

        img = self.addPic(book['name'],bookView)
        bookView.pack(side=LEFT,fill=BOTH,expand=True)
        if img:
            img.bind("<Button-1>",lambda event :self.selectBookOnclick(book['id']))


    def padTheRowWithBlankRows(self):
        while self.countWidgetChildren(self.currentRow) != self.settings['booksDisplayPreRow']:
            self.addBlankRow()


    def countWidgetChildren(self,widget):
        return len(widget.winfo_children())


    def addBlankRow(self):
        Frame(self.currentRow,width = self.settings['pics']['width']).pack(side=LEFT,fill=BOTH,expand=True)


    def createOverlay(self):
        self.currentOverlay = self.makeOverlayAndPopUp(self.canvas,'white',2,"black",self.settings['gui']['popup_pad_x'],self.settings['gui']['popup_pad_y'])


    def killOverlay(self):
        if self.currentOverlay:
            self.killWidget(self.currentOverlay)
            self.currentOverlay = None


    def killWidget(self,widget):
        widget.destroy()


    def addCloseButton(self,parent):
        btn = Button(parent,
        text = 'X',
        command = lambda : self.killOverlay()
        )
        btn.pack(side=RIGHT, anchor=NE,padx=3,pady=3)


    def postBookFormat(self,parent,type):
        str = "Paperback" if type == 'P' else 'Hardcover with dust jacket' if type == 'H' else 'Hardcover without dust jacket'
        pic = Image.open(self.settings['icons']['paperback'] if type == 'P' else self.settings['icons']['hardcover'] if type == 'H' else self.settings['icons']['hardcover_no_dj'])
        pic = pic.resize((self.settings['icons']['width'],self.settings['icons']['height']))
        pic = ImageTk.PhotoImage(pic)
        hol1 = Label(parent,background='white')
        hol2 = Label(hol1,image = pic,background='white')
        hol2.image = pic # keep a reference!
        strL = Label(hol1,text=str,font=('Arial',self.settings['gui']['popup_font_size']),anchor="w",background ='white')
        hol1.pack(fill=X,padx=15,pady=3)
        hol2.pack(side=LEFT)
        strL.pack(side=LEFT)

    def addReadStamp(self,parent,readFlag,bookID):
        string = "You've read this book" if readFlag else "You haven't read this book"
        stamp = Image.open(self.settings['icons']['has_been_read'] if readFlag else self.settings['icons']['has_not_been_read'])
        stamp = stamp.resize((self.settings['icons']['width'],self.settings['icons']['height']))
        stamp = ImageTk.PhotoImage(stamp)
        labelParent = Label(parent,background='white')
        holder = Label(labelParent,image = stamp,background='white')
        holder.image = stamp # keep a reference!
        stringLabel = Label(labelParent,text=string,background='white')
        labelParent.pack(side=LEFT)
        holder.pack(side=LEFT)
        if readFlag and not self.markReadedFlag:
            stringLabel.pack(side=LEFT)

        elif not readFlag and self.markReadedFlag:
            stringLabel.pack()
            toggle = Label(labelParent,text='Mark as readed',background='white',anchor='sw',font=('Arial',10))
            self.styleRedirectText(toggle)
            toggle.pack(side=LEFT)
            toggle.bind('<Button-1>',lambda event: self.markThisBoodReaded(bookID))


    def markThisBoodReaded(self,bookID):
        date = simpledialog.askstring("Read Date", "When did you read this book?\n\nExamples:\nJan 2020 - Mar 2020\nFeb 2020")
        validDate = dateForDB(date)
        if not validDate:
            messagebox.showerror(title='Error', message="Invalid Date Format")
        else :
            readNum = markBookAsReaded(self.db,self.settings,bookID,validDate)
            if type(readNum) is not int:
                messagebox.showerror(title='Error', message="Error Updating DB data.")
            else:
                messagebox.showinfo('Change saved',f'''This is the {readNum}th book you've read''')
                self.redirectPopUp(bookID) # reload with the new icon


    def selectBookOnclick(self,id):
        if self.currentOverlay:
            return
        bookObj = self.fetchById(self,id)
        self.createOverlay()
        selectedBookHeader = Label(self.currentOverlay,background='white')
        selectedBookHeader.pack(side=TOP,fill=X,padx=3,pady=3)
        self.addCloseButton(selectedBookHeader)
        self.addReadStamp(selectedBookHeader,bookObj['read'],bookObj['id'])
        Label(self.currentOverlay,
        text = bookObj['name'],
        font=('Arial', 22),
        anchor="n",
        background ='white'
        ).pack(fill=X,padx=3)
        self.makeTravelersWithPic(bookObj['name'],self.currentOverlay,id)
        self.addBookData(bookObj,self.currentOverlay)


    def makeTravelersWithPic(self,bookName,parent,bookID):
        self.currentImageHodler = Label(parent,background='white')

        prevB = Label(self.currentImageHodler,text='<< Prev.',font=('Arial',23),background='white',foreground = 'blue',cursor = 'hand2')
        prevB.pack(side=LEFT,expand=True,padx=(0,100))
        prevB.bind('<Button-1>',lambda event: self.navigatePrevBook(bookID))

        self.addPic(bookName,parent,True)

        nextB = Label(self.currentImageHodler,text='Next >>',font=('Arial',23),background='white',foreground = 'blue',cursor = 'hand2')
        nextB.pack(side=RIGHT,expand=True,padx=(100,0))
        nextB.bind('<Button-1>',lambda event: self.navigateNextBook(bookID))

        self.currentImageHodler.pack(fill=X,padx=3,pady=0)
        self.currentImageHodler = None


    def postSingleBookLine(self,line,parent,returnValue = False):
        label = Label(parent,
        text = line,
        font=('Arial',self.settings['gui']['popup_font_size']),
        anchor="w",
        background ='white'
        )
        label.pack(fill=X,padx=15,pady=3)
        if returnValue:
            return label


    def postStoriesList(self,stories,parent):
        label = self.postSingleBookLine('',parent,True)
        Label(label,text='Collection: ',font=('Arial',self.settings['gui']['popup_font_size']),anchor="w",background ='white').pack(side=LEFT,pady=3)
        storiesTag = Label(label,text = str(len(stories)) + ' Stories',font=('Arial',self.settings['gui']['popup_font_size']),anchor="w",background ='white')
        storiesTag.pack(side=LEFT,pady=3)
        self.styleRedirectText(storiesTag)
        storiesTag.bind('<Button-1>',lambda event: print(stories))


    def postSingleBookLineWithRedirect(self,line1,redirectline,parent,redirectId):
        label = self.postSingleBookLine('',parent,True)
        Label(label,text = line1,font=('Arial',self.settings['gui']['popup_font_size']),anchor="w",background ='white').pack(side=LEFT,pady=3)
        tag = Label(label,text = redirectline,font=('Arial',self.settings['gui']['popup_font_size']),anchor="w",background ='white')
        tag.pack(side=LEFT,pady=3)
        self.styleRedirectText(tag)
        tag.bind("<Button-1>",lambda event :self.redirectPopUp(redirectId))


    def styleRedirectText(self,widget):
        widget.configure(cursor="hand2")
        f = font.Font(widget, widget.cget("font"))
        f.configure(underline=True)
        widget.configure(font=f)
        widget.configure(foreground ='blue')


    def redirectPopUp(self,redirectId):
        self.killOverlay()
        self.selectBookOnclick(redirectId)


    def navigatePrevBook(self,id):
        prevBookID = getPrevValueInJsonByElementKey(self.data,'id',id)
        if prevBookID:
            self.killOverlay()
            self.selectBookOnclick(prevBookID)


    def navigateNextBook(self,id):
        nextBookID = getNextValueInJsonByElementKey(self.data,'id',id)
        if nextBookID:
            self.killOverlay()
            self.selectBookOnclick(nextBookID)


    def addTitleAndCount(self,parent):
        main = Label(parent)
        main.pack(side=LEFT)
        parent.update()
        Label(main,text='My Books',font=('Arial', 26)).pack(side=RIGHT)
        self.bookIndicatorLabel =  Label(self.header,
        text= f'''({str(self.booksCount)})''',
        font=('Arial', 16)
        )
        self.bookIndicatorLabel.pack(side=LEFT,fill=X)


    def addHeader(self):
        self.header = Frame(self.window)
        self.header.pack(side=TOP,fill=X, pady=(5,15))

        self.addSortingTool(self.header)
        self.addTitleAndCount(self.header)
        searchBox = Frame(self.header)
        searchBox.pack(side=LEFT,expand=True)

        searchHeader = Label(searchBox,anchor='ne')
        searchHeader.pack(expand=True,fill=X)

        Label(searchHeader,
        text = 'Search:',
        font=('Arial', 14),
        anchor="n"
        ).pack(side=LEFT,expand=True,fill=X)

        clearFilters = Label(searchHeader,
        text = 'clear',
        font=('Arial', 10))
        self.styleRedirectText(clearFilters)
        clearFilters.pack(side=LEFT,expand=True,fill=X)
        clearFilters.bind('<Button-1>',self.clearFilters)

        self.addFilterLine(searchBox,'Name: ',self.nameFilterStr)
        self.addFilterLine(searchBox,'Author: ',self.authorFilterStr)
        self.addPagesNavigator(searchBox)


    def addFilterLine(self,parent,title,entryName):
        line = Frame(parent)
        line.pack(fill=X,expand=True,pady=3)
        title = Label(line,text=title)
        entry = Entry(line)
        entry.pack(side=RIGHT)
        title.pack(side=RIGHT)
        setattr(self,entryName, entry)


    def addPagesNavigator(self,parent):
        frame = Frame(parent)
        self.goPrev = Label(frame,text='<<')
        self.pagesLabel = Label(frame,text="Page: " + str(self.currPage) + "/" + str(self.totalPages))

        if self.currPage > 1:#can be redirected back
            self.styleButtonEnableGUI(self.goPrev)
            self.goPrevBind = self.goPrev.bind('<Button-1>',self.goPrevPage)

        self.goNext = Label(frame,text='>>')

        if self.totalPages > self.currPage :#can be redirected forward
            self.styleButtonEnableGUI(self.goNext)
            self.goNextBind = self.goNext.bind('<Button-1>',self.goNextPage)

        self.goPrev.pack(side=LEFT)
        self.pagesLabel.pack(side=LEFT)
        self.goNext.pack(side=LEFT)
        frame.pack()


    def styleButtonEnableGUI(self,widget):
        widget.configure(cursor="hand2")
        f = font.Font(widget, widget.cget("font"))
        widget.configure(foreground ='blue')


    def cancelButtonEnableGUI(self,widget):
        widget.configure(cursor=None)
        f = font.Font(widget, widget.cget("font"))
        widget.configure(foreground ='black')


    def goPrevPage(self,event):
        self.goUp()
        self.updateMyPageDown()
        minRelevant = self.getIndexFirstRelevant() - 1
        self.notRelevantAll()
        count = 0
        while minRelevant >= 0 and count < self.settings['maxBooksFetch']:
            if includeInsensitive(self.data[minRelevant]['name'],self.nameValueFilter) and includeInsensitive(self.data[minRelevant]['author'],self.authorValueFilter):
                self.data[minRelevant]['relevant'] = True
                count += 1
            minRelevant -= 1
        self.removeBooks()
        self.displyBooksThread()
        self.reCenterBooks()
        self.pagesLabel['text'] = "Page: " + str(self.currPage) + "/" + str( self.totalPages)
        if not self.currPage > 1:
            self.goPrev.unbind('<Button-1>', self.goPrevBind)
            self.resetGoPrevBind()
            self.cancelButtonEnableGUI(self.goPrev)
        #enable go next
        self.styleButtonEnableGUI(self.goNext)
        self.goNextBind = self.goNext.bind('<Button-1>',self.goNextPage)


    def goNextPage(self,event):
        self.goUp()
        self.updateMyPageUp()
        maxRelevant = self.getIndexLastRelevant() + 1
        self.notRelevantAll()
        len = self.totalBooks - 1
        count = 0

        while maxRelevant <= len and count < self.settings['maxBooksFetch']:
            if includeInsensitive(self.data[maxRelevant]['name'],self.nameValueFilter) and includeInsensitive(self.data[maxRelevant]['author'],self.authorValueFilter):
                self.data[maxRelevant]['relevant'] = True
                count += 1
            maxRelevant += 1
        self.removeBooks()
        self.displyBooksThread()
        self.reCenterBooks()
        self.pagesLabel['text'] = "Page: " + str(self.currPage) + "/" + str( self.totalPages)
        if not self.totalPages > self.currPage:
            self.goNext.unbind('<Button-1>', self.goNextBind)
            self.resetGoNextBind()
            self.cancelButtonEnableGUI(self.goNext)
        #enable go prev
        self.styleButtonEnableGUI(self.goPrev)
        self.goPrevBind = self.goPrev.bind('<Button-1>',self.goPrevPage)


    def getIndexLastRelevant(self):
        len = self.totalBooks - 1
        count = len
        while len > -1 :
            if self.data[count]['relevant']:
                return count
            count -= 1
        return None


    def readFilters(self):
        self.nameValueFilter = getattr(self,self.nameFilterStr).get().strip()
        self.authorValueFilter = getattr(self,self.authorFilterStr).get().strip()


    def getIndexFirstRelevant(self):
        for i,book in enumerate(self.data):
            if book['relevant']:
                return i
        return None


    def notRelevantAll(self):
        for book in self.data:
            book['relevant'] = False


    def updateMyPageUp(self):
        self.currPage += 1


    def updateMyPageDown(self):
        self.currPage -= 1


    def resetYourCurrPage(self):
        self.currPage = 1


    def resetCountRelevantBooks(self):
        count = 0
        for book in self.data:
            if includeInsensitive(book['name'],self.nameValueFilter) and includeInsensitive(book['author'],self.authorValueFilter):
                count += 1
        self.booksCount = count
        self.totalPages = roundUpDividation(self.booksCount, self.settings['maxBooksFetch']) or 1


    def updateBookCountIndicator(self):
        self.bookIndicatorLabel['text'] = f'''({str(self.booksCount)})'''


    def updatePageNavigators(self):
        if self.currPage > 1:#can be redirected back
            self.styleButtonEnableGUI(self.goPrev)
            self.goPrevBind = self.goPrev.bind('<Button-1>',self.goPrevPage)
        else :
            if self.goPrevBind:
                self.goPrev.unbind('<Button-1>', self.goPrevBind)
                self.resetGoPrevBind()
            self.cancelButtonEnableGUI(self.goPrev)

        if self.totalPages > self.currPage :#can be redirected forward
            self.styleButtonEnableGUI(self.goNext)
            self.goNextBind = self.goNext.bind('<Button-1>',self.goNextPage)
        else :
            if self.goNextBind:
                self.goNext.unbind('<Button-1>', self.goNextBind)
                self.resetGoNextBind()
            self.cancelButtonEnableGUI(self.goNext)


    def resetGoNextBind(self):
        self.goNextBind = None


    def resetGoPrevBind(self):
        self.goPrevBind = None


    def emptyFilters(self):
        if hasattr(self,self.nameFilterStr):
            clearEntry(getattr(self,self.nameFilterStr))
        if hasattr(self,self.authorFilterStr):
            clearEntry(getattr(self,self.authorFilterStr))

    def clearFilters(self,event):
        self.emptyFilters()
        self.filter()


    def addBookData(self,bookO,parent):
        if 'id' in bookO:
            self.postSingleBookLine('ID: ' + str(bookO['id']),parent)

        if 'author' in bookO:
            self.postSingleBookLine('Author: ' + bookO['author'],parent)

        if 'year' in bookO:
            self.postSingleBookLine('Publication Year: ' + str(bookO['year']),parent)

        if 'parent_name' in bookO:
            self.postSingleBookLine('Part Of: ' + bookO['parent_name'],parent)

        if 'pages' in bookO:
            self.postSingleBookLine('Number of Pages: ' + str(bookO['pages']),parent)

        if 'language' in bookO:
            self.postSingleBookLine('Language: ' + bookO['language'],parent)

        if 'o_language' in bookO:
            self.postSingleBookLine('Original Language: ' + bookO['o_language'],parent)

        if 'isbn' in bookO:
            self.postSingleBookLine('ISBN: ' + str(bookO['isbn']),parent)

        if 'type' in bookO:
            self.postBookFormat(parent,bookO['type'])

        if 'serie' in bookO:
            self.postSingleBookLine('Serie: ' + ('None' if (not bookO['serie'] or not bookO['serie_num']) else bookO['serie'] + ' (' + str(bookO['serie_num']) + ')'),parent)

        if 'prev_name' in bookO:
            if bookO['prev_id'] :
                self.postSingleBookLineWithRedirect('Preceded by: ' ,  bookO['prev_name'] + ' by ' + (bookO['prev_author'] if 'prev_author' in bookO else bookO['author']),parent,bookO['prev_id'])
            else:
                self.postSingleBookLine('Preceded by: None',parent)

        if 'next_id' in bookO:
            if bookO['next_id'] :
                self.postSingleBookLineWithRedirect('Followed by: ' ,  bookO['next_name'] + ' by ' + (bookO['next_author'] if 'next_author' in bookO else bookO['author']),parent,bookO['next_id'])
            else:
                self.postSingleBookLine('Followed by: None',parent)

        if 'stories' in bookO:
            if bookO['stories'] and notEmptyEls(bookO['stories']):
                self.postStoriesList(bookO['stories'],parent)


    def addTopNav(self):
        topNav = Menu(self.window)
        self.window.config(menu = topNav)
        self.insertionsMenu = Menu(topNav,tearoff=False,bg='white',font=('Arial',11))
        self.insertionsMenu.add_command(label="Insert Book",command=self.insertBookWindow)
        self.insertionsMenu.add_command(label="Insert Serie")
        self.insertionsMenu.add_command(label="Insert Wishlist")
        topNav.add_cascade(label="Insert", menu=self.insertionsMenu)
        self.displayMenu = Menu(topNav,tearoff=False,bg='white',font=('Arial',11))
        self.displayMenu.add_checkbutton(label="Display Books", command = lambda : self.loadDsiplay(self.loadBooks))
        self.displayMenu.add_checkbutton(label="Display Series")
        self.displayMenu.add_checkbutton(label="Display Stories", command = lambda : self.loadDsiplay(self.loadStories))
        self.displayMenu.add_checkbutton(label="Display Wishlist")
        self.displayMenu.add_checkbutton(label="Display Reads")
        self.displayMenu.add_checkbutton(label="Display Stats")
        topNav.add_cascade(label="Display", menu=self.displayMenu)
        bckupMenu = Menu(topNav,tearoff=False,bg='white',font=('Arial',11))
        bckupMenu.add_command(label="Backup DB Structure")
        bckupMenu.add_command(label="Backup DB Data")
        topNav.add_cascade(label="BackUps", menu=bckupMenu)


    def loadDsiplay(self,callback):
        callback()

    def makeOverlayAndPopUp(self,parent,color='white',borderThicknes = 2, borderColor = "black",padx=0,pady=0):
        c = Canvas(parent,bg=color,highlightthickness=borderThicknes, highlightbackground=borderColor)
        c.pack(
        side="top",
        fill="both",
        expand=True,
        pady=pady,
        padx=padx
        )
        return c


    def insertBookWindow(self):
        self.insertBookCanvas = self.makeOverlayAndPopUp(self.canvas,"white",2,"black",self.settings['insertBook']['padx_popup'],self.settings['insertBook']['pady_popup'])
        InsertBook(self.insertBookCanvas,self.settings,self.db)


    def evalSortingFunction(self,key,reverseFlag):
        self.data.sort(key = lambda u : u[key], reverse = reverseFlag)


    def sortBooks(self,args):
        self.evalSortingFunction(*args)
        self.filter()


    def addSortingTool(self,parent):
        sortingLabel = Label(parent)
        sortingLabel.pack(side=LEFT,expand=True,fill=X)
        Label(sortingLabel,text="Sort By:",font=('Arial', 14),anchor="n").pack(side=TOP)
        self.sortInp = Combobox(sortingLabel,
        values = [] ,
        width=25,
        state="readonly"
        )
        self.sortInp.pack(side=BOTTOM)
        self.sortInp.bind('<<ComboboxSelected>>',lambda a : self.sortBooks(optionTranslation[self.sortInp.current()] ))


    def loadStories(self):
        self.emptyFilters()
        stories = Stories(self.settings,self.db)
        self.data = stories.setData()
        self.markReadedFlag = stories.markAsReadedFlag
        self.booksCount = len(self.data)
        self.totalBooks = self.booksCount
        self.totalPages = roundUpDividation(self.booksCount, self.settings['maxBooksFetch']) or 1
        self.picFolder = stories.picturesFolder
        self.sortOptions = stories.sortOptions
        self.sortTranslations = stories.sortTranslations
        self.fetchById = lambda self,id: Stories.fetchById(self.db,self.settings,id)
        self.reloadSortingTool()

    def loadBooks(self, addDisplayFlag = False):
        self.emptyFilters()
        books = Books(self.settings,self.db)
        self.data = books.setData()
        self.markReadedFlag = books.markAsReadedFlag
        self.booksCount = len(self.data)
        self.totalBooks = self.booksCount
        self.totalPages = roundUpDividation(self.booksCount, self.settings['maxBooksFetch']) or 1
        self.picFolder = books.picturesFolder
        self.sortOptions = books.sortOptions
        self.sortTranslations = books.sortTranslations
        self.fetchById = lambda self,id: Books.fetchById(self.db,self.settings,id)
        self.reloadSortingTool(addDisplayFlag)


    def reloadSortingTool(self,addDisplayFlag=False):
        self.sortInp['values'] = self.sortOptions
        self.sortInp.bind('<<ComboboxSelected>>',lambda a : self.sortBooks(self.sortTranslations[self.sortInp.current()] ))
        self.sortInp.set(self.sortOptions[0])
        if not addDisplayFlag:
            self.filter()
