from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
import re
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import pandas as pd
from threading import Thread
from filterWidget import Filter

class InsertBook:
    def __init__(self,win,settings,db,autoValues = {},destoryAfter = False,updateID = False, hook = False):
        self.window = win
        self.db = db
        self.updateID = updateID
        self.hook = hook
        self.sucess = StringVar() # trace
        self.idTrace = StringVar()
        self.settings = settings
        self.destoryAfter = destoryAfter
        self.folderToFetchPics = None
        self.setCheckboxStyle()
        self.setFrameStyle()
        self.closeOnclick()
        self.addTitle()
        self.addAutoFillLabel()
        self.addInputs(autoValues)
        self.addType(autoValues)
        self.addSerie(autoValues)
        self.addNextBook(autoValues)
        self.addPrevBook(autoValues)
        self.addCollectionElements(autoValues)


    def addAutoFillLabel(self):
        l = Label(self.window,
        background='black',
        foreground='white'
        )
        l.pack(fill=X,expand=True,padx=5)
        self.autoFetcherLabel = Label(l,
        background='black',
        foreground='white',
        font=('Arial',9,'bold'),
        cursor = 'hand2',
        text='Auto Fill'
        )
        self.autoFetcherLabel.pack(pady=1)
        self.autoFetcherLabel.bind('<Button-1>',self.autoFillCallback)


    def autoFillCallback(self,event):
        isbn = self.isbn.get()
        name = self.name.get()
        author = self.author.get()

        if isbn or name:
            self.autoFetcherLabel.pack_forget()
            threadId = getRandomStr(50) #random string
            self.autoFetchThreadID = threadId
            #fetch as thread - if not the pack_forget will occur after the fetch - gui takes time..
            thread = Thread(target = lambda: self.autoFetchThread(threadId,isbn,name,author))
            thread.daemon = True # kill if window is closed
            thread.start()


    def autoFetchThread(self,threadId,isbn,name,author):
        #clear the collection table (from prev. ones)
        self.killAllChildren(self.isCollectionFrame)
        self.isCollectionNextRow = 0
        self.collectionArr = []
        self.isCollection.set(False)

        #priority to isbn, if isbn is not set - go by name
        if isbn:
            #fetch by isbn
            data = getDataFromIsbn(isbn,self.settings)
            if self.autoFetchThreadID == threadId and data : # still relevant and the isbn was found
                self.name.set(data['name'])
                self.author.set(data['author'])
                self.year.set(data['year'])
                self.pages.set(data['pages'])
                if data['collection']:
                    self.autoFillCollection(data['collection'])
        else:
            #fetch isbn by title, then get data
            isbn = getIsbn(name,author,self.settings)
            if self.autoFetchThreadID == threadId and isbn : # still relevant and the isbn was found
            #now fetch data from isbn
                data = getDataFromIsbn(isbn,self.settings)
                if self.autoFetchThreadID == threadId and data : # still relevant and the isbn was found
                    self.name.set(data['name'])
                    self.author.set(data['author'])
                    self.year.set(data['year'])
                    self.pages.set(data['pages'])
                    self.isbn.set(isbn)
                    if data['collection']:
                        self.autoFillCollection(data['collection'])

        self.autoFetcherLabel.pack(pady=1)



    def addType(self,autoValues = {}):
        self.addCheckBoxGroup(self.window,[{'value':'H','text':'Hard Cover','row':8,'column':0},{'value':'P','text':'Paper Back','row':8,'column':1},{'value':'HN','text':'Hardcover No Dust Jacket','row':8,'column':2}],autoValues)

    def addTitle(self):
        Label(self.window,
        text = 'Insert New Book' if not self.updateID else f'''Alter Book {self.updateID}''',
        font=('Arial', 20),
        background='black',
        foreground='white',
        ).pack(pady=(20,0))

    def addInputs(self,autoValues):
        fram = Label(self.window,background='black',foreground='white')

        self.name = StringVar()
        if 'name' in autoValues:
            self.name.set(autoValues['name'])

        self.author = StringVar()
        if 'author' in autoValues:
            self.author.set(autoValues['author'])

        self.year = StringVar()
        if 'year' in autoValues:
            self.year.set(str(autoValues['year']))

        self.pages = StringVar()
        if 'pages' in autoValues:
            self.pages.set(str(autoValues['pages']))

        self.lang = StringVar()
        if 'language' in autoValues:
            self.lang.set(str(autoValues['language']))

        self.oriLan = StringVar()
        if 'o_language' in autoValues:
            self.oriLan.set(str(autoValues['o_language']))

        self.isbn = StringVar()
        if 'isbn' in autoValues:
            self.isbn.set(str(autoValues['isbn']))
        self.addNewLabelAndInput(fram,'Book Name',1,0,'name')
        self.addNewLabelAndInput(fram,'Author Name',2,0,'author')
        self.addNewLabelAndInput(fram,'Publication Year',3,0,'year')
        self.addNewLabelAndInput(fram,'Number Of Pages',4,0,'pages')
        self.addNewLabelAndInput(fram,'Book Language',5,0,'lang')
        self.addNewLabelAndInput(fram,'Book Origin Language',6,0,'oriLan')
        self.addNewLabelAndInput(fram,'Book ISBN',7,0,'isbn')
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


    def justDissapear(self):
        self.window.destroy()

    def killWindow(self):
        self.justDissapear()
        self.sucess.set(0)


    def addNewLabelAndInput(self,prent,text,row,column,varName):
        innerFrame = Label(prent,background='black',foreground='white')
        label = Label(innerFrame,text=text,background='black',foreground='white')
        label.pack(side=LEFT)
        entry = Entry(innerFrame,textvariable = getattr(self, varName))
        entry.pack(side=RIGHT)
        innerFrame.pack(pady=5,fill=X)


    def addCheckBoxGroup(self,parent,optionJson,autoValues):
        innerFrame = Label(parent,background='black',foreground='white')
        self.type = StringVar()
        if 'type' in autoValues:
            self.type.set(str(autoValues['type']))
        else:
            self.type.set(False)

        for cBox in optionJson:
            Checkbutton(innerFrame,onvalue = cBox['value'],text = cBox['text'],variable = self.type,style='Red.TCheckbutton').pack(side=LEFT,padx=7,pady=5)
        innerFrame.pack()


    def addCollectionElements(self,autoValues = {}):
        fr = Label(self.window,background='black',foreground='white')
        topNav = Label(fr,background='black',foreground='white')
        self.isCollection = BooleanVar()
        Checkbutton(topNav,
        text = 'Collection of stories',
        variable = self.isCollection,
        style='Red.TCheckbutton',
        command = lambda : self.isCollectionBind(btn,tableWidget,collPicturesHandler)
        ).pack(side=LEFT)

        btn = Label(topNav,
        text = "+",
        width=3,
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.bind('<Button-1>',lambda e: self.addNewCollectionEntry())

        tableWidget = self.addExcelCsvHandler(topNav)

        collPicturesHandler = self.addCollectionPicsHandler(topNav) if jsonIsEmpty(autoValues) else None #select pictures for collection only if a new book is insrted, not in a update

        topNav.pack()
        fr.pack()

        self.createView()
        self.isCollectionNextRow = 0
        self.collectionArr = []

        if 'stories' in autoValues:
            if autoValues['stories'] and notEmptyEls(autoValues['stories']):
                self.isCollection.set(True)
                Thread(target = lambda: self.insertAutoValuesCollection(autoValues['stories'])).start()


    def addExcelCsvHandler(self,parent):
        tableWidget = Label(parent,
        text='Import Csv/Excel',
        background='black',foreground='white'
        )
        tableWidget.bind('<Button-1>',lambda event: self.handleTableImport())
        tableWidget.configure(cursor="hand2")
        fTemp = font.Font(tableWidget, tableWidget.cget("font"))
        fTemp.configure(weight='bold')
        fTemp.configure(size=7)
        tableWidget.configure(font=fTemp)
        return tableWidget


    def addCollectionPicsHandler(self,parent):
        collPicturesHandler = Label(parent,
        text='Chosse Pictures Folder',
        background='black',foreground='white'
        )
        collPicturesHandler.bind('<Button-1>',lambda event: self.chossePicturesFolder())
        collPicturesHandler.configure(cursor="hand2")
        fTemp = font.Font(collPicturesHandler, collPicturesHandler.cget("font"))
        fTemp.configure(weight='bold')
        fTemp.configure(size=7)
        collPicturesHandler.configure(font=fTemp)
        return collPicturesHandler


    def chossePicturesFolder(self):
        folder = askdirectory()
        if folder:
            self.folderToFetchPics = folder


    def autoFillCollection(self,vals):
        self.isCollection.set(True)
        for name in vals:
            self.addNewCollectionEntry([name,''])


    def insertAutoValuesCollection(self,values):
        for entry in values:
            self.addNewCollectionEntry([entry['name'],entry['pages']])


    def handleTableImport(self):
        filename = askopenfilename()
        if not filename:
            return
        sheet =  'Sheet1'
        df = pd.read_excel(io=filename, sheet_name=sheet)
        nameColumn = df.columns[0]
        pagesColumn = df.columns[1]
        self.killAllChildren(self.isCollectionFrame)
        #self.isCollectionFrame.pack_forget()
        self.isCollectionNextRow = 0
        self.collectionArr = []
        #self.isCollectionFrame.pack()
        thread = Thread(target = lambda: self.iterateExcelAndInsert(df))
        thread.start()


    def iterateExcelAndInsert(self,dfPointer):
        nameColumn = dfPointer.columns[0]
        pagesColumn = dfPointer.columns[1]
        for i, j in dfPointer.iterrows():
            self.addNewCollectionEntry([j[nameColumn],j[pagesColumn]])


    def killAllChildren(self,widget):
        for i in widget.winfo_children():
            i.destroy()
        self.removeEmptySpaceInElement(widget)


    def removeEmptySpaceInElement(self,element):
        Frame(element,style='Red.TFrame').pack()
        #pack empty frame after destorying all



    def isCollectionBind(self,btn,label,collPicturesHandler):
        if not self.isCollection.get():
            self.killAllChildren(self.isCollectionFrame)
            #self.isCollectionFrame.pack_forget()
            btn.pack_forget()
            label.pack_forget()
            if collPicturesHandler:#may be null in update case
                collPicturesHandler.pack_forget()
            self.isCollectionNextRow = 0
            self.collectionArr = []
            self.folderToFetchPics = None
        else:
            btn.pack(side=LEFT)
            label.pack(side=LEFT,padx=20)
            if collPicturesHandler:#may be null in update case
                collPicturesHandler.pack(side=LEFT,padx=20)
            #self.isCollectionFrame.pack()
            self.addNewCollectionEntry()


    def addNewCollectionEntry(self,defaultValues = None):
        line = Label(self.isCollectionFrame,background='black',foreground='white')
        a = StringVar()
        b = StringVar()
        self.collectionArr.append({'name':a,'pages':b})
        Label(line,text='Story Name:',background='black',foreground='white').pack(side=LEFT)
        e1 = Entry(line,textvariable = a)
        e1.pack(side=LEFT)
        Label(line,text='Pages:',background='black',foreground='white').pack(side=LEFT)
        e2 = Entry(line,textvariable = b)
        e2.pack(side=LEFT)
        line.pack(pady=7)
        self.isCollectionNextRow += 1
        if defaultValues:
            e1.insert(0,defaultValues[0])
            e2.insert(0,defaultValues[1])
        self.scrollDown()


    def addSerie(self,autoValues):
        series = {}
        for serie in fetchAllSeries(self.db,self.settings):
            series[serie[1]] = serie[0]
        self.series = series
        self.isSerie = BooleanVar()

        tempFrame = Label(self.window,background='black',foreground='white')
        Checkbutton(tempFrame,
        text = 'Part Of Serie',
        variable = self.isSerie,
        style='Red.TCheckbutton',
        command = lambda : self.isSerieBind()
        ).pack()
        self.serieVar = StringVar()
        self.serieNumber = StringVar()
        self.serieVar.set(list(series)[0])
        self.serieFrame = Label(tempFrame,background='black',foreground='white')
        self.serieFrame.pack()
        combo = Combobox(self.serieFrame,
        textvariable = self.serieVar,
        values = [*series.keys()],
        state="readonly")



        filterBox = Filter(self.serieFrame,combo,self.serieVar).get()
        filterBox.configure(width=5)

        Label(self.serieFrame,text = 'Filter: ',background='black',foreground='white').pack(side=LEFT)
        filterBox.pack(side=LEFT,padx=5)
        Label(self.serieFrame,text = 'Options: ',background='black',foreground='white').pack(side=LEFT)
        combo.pack(side=LEFT, padx=5)

        Label(self.serieFrame,text = 'Number',background='black',foreground='white').pack(side=LEFT)
        Entry(self.serieFrame,textvariable = self.serieNumber,width=3).pack(side=LEFT)
        tempFrame.pack()
        self.serieFrame.pack_forget()
        if 'serie' in autoValues and autoValues['serie'] and 'serie_num' in autoValues and autoValues['serie_num']:
            self.isSerie.set(True)
            self.serieFrame.pack()
            self.serieVar.set(autoValues['serie'])
            self.serieNumber.set(autoValues['serie_num'])


    def isSerieBind(self):
        if not self.isSerie.get():
            self.serieFrame.pack_forget()
        else:
            self.serieFrame.pack(pady=7)


    def addInsertButton(self,p):
        btn = Label(p,
        text = 'Save',
        font=('Arial',16,'bold'),
        background='black',
        foreground = 'white',
        cursor = 'hand2'
        )
        btn.pack(pady=(2,10))
        btn.bind('<Button-1>',lambda e: self.checkOut())


    def checkOut(self):
        vars = self.getAllVars()
        check = self.checkVars(vars)
        newId = self.updateID
        if check != True:
            messagebox.showerror(title='Error', message=check)
            return
        else:
            if not self.hook:
                newId = insertNewBook(self.db,self.settings,vars)
                if self.folderToFetchPics != None:
                    self.movePicsToCollection(newId)

                self.idTrace.set(newId)
            else:
                self.hook(self,vars,self.updateID)

            self.clearInputs()
            if self.destoryAfter:
                self.justDissapear()
            else :
                if messagebox.askyesno("Question","Would you like to add a picture?"):
                    filename = askopenfilename()
                    if filename:
                        bookNameAsFile = str(newId) + getExtensionFromPath(filename)
                        flag = copyFile(filename,self.settings['pics']['picFolderPath'] + bookNameAsFile)
                        if flag != True:
                            insertError(f"""OS error - {flag}""",self.settings['errLog'])
                            messagebox.showerror(title='Error', message="Oppsss\nOS error.\nCould not copy the picture.\nPlease read LOG for mofe info.")
                        else:
                            messagebox.showinfo('Message',f'''Picture Copied.''')
            self.sucess.set(vars['name'])



    def clearInputs(self):
        self.name.set('')
        self.author.set('')
        self.year.set('')
        self.pages.set('')
        self.lang.set('')
        self.oriLan.set('')
        self.isbn.set('')
        self.type.set(False)
        self.isCollection.set(False)
        self.isSerie.set(False)
        self.serieVar.set('')
        self.serieNumber.set('')
        self.serieFrame.pack_forget()


    def checkVars(self,vars):
        if not vars['name']:
            return 'Empty Name'
        if not vars['author']:
            return 'Empty Author'
        if not vars['year']:
            return 'Empty Year'
        if not  re.match('^[0-9]{4}$',vars['year']):
            return 'Invalid Year'
        if not vars['pages']:
            return 'Empty Pages'
        if not  re.match('^[0-9]+$',vars['pages']):
            return 'Invalid Pages'
        if not vars['lang']:
            return 'Empty Language'
        if not vars['oriLan']:
            return 'Empty Original Language'
        if not vars['isbn']:
            return 'Empty ISBN'
        if not re.match('^[0-9a-zA-Z\-]+$',vars['isbn']):
            return 'Invalid ISBN'
        if not vars['type'] or vars['type'] == '0':
            return 'Empty Type'
        if 'next' in vars and not vars['next']:
            return 'Bad Follow by Book'
        if 'prev' in vars:
            if not vars['prev']:
                return 'Bad Preceded by Book'
            if previousBookAlreadyHaveFollow(self.db,self.settings,vars['prev'],self.updateID):
                return 'Preceded Book have a Different Follow'
        if 'serie' in vars:
            if not vars['serie']['id']:
                return 'Empty Serie Name'
            if not vars['serie']['number']:
                return 'Empty Serie Number'
            if not  re.match('^[0-9]+$',vars['serie']['number']):
                return 'Invalid Serie Number'
        if 'collection' in vars:
            for i in vars['collection']:
                if not i['name']:
                    return 'Empty Story Name'
                if not i['pages']:
                    return 'Empty Story Pages'
                if not re.match('^[0-9]+$',i['pages']):
                    return 'Invalid Story Pages'
        return True


    def getAllVars(self):
        res = {}
        res['name'] = self.name.get().strip()
        res['author'] = self.author.get().strip()
        res['year'] = self.year.get().strip()
        res['pages'] = self.pages.get().strip()
        res['lang'] = self.lang.get().strip()
        res['oriLan'] = self.oriLan.get().strip()
        res['isbn'] = self.isbn.get().strip().replace('-','')
        res['type'] = self.type.get().strip()
        if self.isFollowed.get():
            res['next'] = self.books[self.followedVar.get().strip()]
        if self.isPreceded.get():
            res['prev'] = self.books[self.precededVar.get().strip()]
        if self.isSerie.get():
            res['serie'] = {}
            res['serie']['id'] = self.series[self.serieVar.get().strip()]
            res['serie']['number'] = self.serieNumber.get().strip()
        if self.isCollection.get():
            res['collection'] = []
            for i in self.collectionArr:
                if i['name'].get() and i['pages'].get() :
                    res['collection'].append({'name':i['name'].get().strip(),'pages':i['pages'].get().strip()})

        if 'collection' in res and not res['collection']:
            del res['collection']

        return res

    def addNextBook(self,autoValues = {}):
        books = {}
        for book in getBookNames(self.db,self.settings):
            books[book[1]] = book[0]
        self.books = books
        tempF = Label(self.window,background='black',foreground='white')
        self.isFollowed = BooleanVar()
        Checkbutton(tempF,
        text = 'Is Followed',
        style='Red.TCheckbutton',
        variable = self.isFollowed,
        command = lambda : self.isFollowedBind()
        ).pack()
        self.followedVar = StringVar()
        self.followedVar.set(list(books)[0])
        self.followedFrame = Label(tempF, background='black',foreground='white')
        self.followedFrame.pack()
        combo = Combobox(self.followedFrame,
        textvariable = self.followedVar,
        values = [*books.keys()],
        width=70,
        state="readonly")

        filterBox = Filter(self.followedFrame,combo,self.followedVar).get()
        filterBox.configure(width=5)

        Label(self.followedFrame,text = 'Filter: ',background='black',foreground='white').pack(side=LEFT)
        filterBox.pack(side=LEFT,padx=5)
        Label(self.followedFrame,text = 'Options: ',background='black',foreground='white').pack(side=LEFT)
        combo.pack(side=LEFT, padx=5)

        self.followedFrame.pack_forget()
        tempF.pack()
        if 'next_name' in autoValues and autoValues['next_name']:
            self.isFollowed.set(True)
            self.followedFrame.pack(pady=7)
            self.followedVar.set(self.getBookFullInfoFromNameAndAuthor(books,autoValues['next_name'] + ' - ' + autoValues['next_author']))


    def getBookFullInfoFromNameAndAuthor(self,json,needle):
        for key in json:
            if needle in key:
                return key
        return ''


    def isFollowedBind(self):
        if not self.isFollowed.get():
            self.followedFrame.pack_forget()
        else:
            self.followedFrame.pack(pady=7)

    def addPrevBook(self,autoValues = {}):
        self.isPreceded = BooleanVar()
        fr = Label(self.window,background='black',foreground='white')
        Checkbutton(fr,
        text = 'Is Preceded',
        variable = self.isPreceded,
        style='Red.TCheckbutton',
        command = lambda : self.isPrecededBind()
        ).pack()
        self.precededVar = StringVar()
        self.precededVar.set(list(self.books)[0])
        self.precededFrame = Label(fr,background='black',foreground='white')
        self.precededFrame.pack()
        combo = Combobox(self.precededFrame,
        textvariable = self.precededVar,
        values = [*self.books.keys()] ,
        width=70,
        state="readonly")

        filterBox = Filter(self.precededFrame,combo,self.precededVar).get()
        filterBox.configure(width=5)

        Label(self.precededFrame,text = 'Filter: ',background='black',foreground='white').pack(side=LEFT)
        filterBox.pack(side=LEFT,padx=5)
        Label(self.precededFrame,text = 'Options: ',background='black',foreground='white').pack(side=LEFT)
        combo.pack(side=LEFT, padx=5)

        combo.pack()
        self.precededFrame.pack_forget()
        fr.pack()
        if 'prev_name' in autoValues and autoValues['prev_name']:
            self.isPreceded.set(True)
            self.precededFrame.pack(pady=7)
            self.precededVar.set(self.getBookFullInfoFromNameAndAuthor(self.books,autoValues['prev_name'] + ' - ' + autoValues['prev_author']))


    def isPrecededBind(self):
        if not self.isPreceded.get():
            self.precededFrame.pack_forget()
        else:
            self.precededFrame.pack(pady=7)


    def setCheckboxStyle(self):
        s = Style()
        s.configure('Red.TCheckbutton', foreground='white',background='black')


    def setFrameStyle(self):
        st = Style()
        st.configure('Red.TFrame', foreground='white',background='black')


    def createView(self):
        self.canvas = Canvas(self.window,bg='black',highlightthickness=0, highlightbackground='black')
        mainP = Label(self.canvas,background='black',foreground='white')
        self.isCollectionFrame = Label(mainP,background='black',foreground='white')
        self.isCollectionFrame.pack()
        self.scroll = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y",padx=(0,7),pady=(0,7))
        self.canvas.pack(side="left", fill="both", expand=True, padx=5,pady=(0,5))
        self.canvas.create_window((4,4), window=mainP, anchor="nw",tags='mainF')
        self.canvas.bind("<Configure>", self.setCanvasSize)
        self.isCollectionFrame.bind("<Configure>", self.onFrameConfigure)
        self.addInsertButton(mainP)


    def setCanvasSize(self,event):
        self.canvas.itemconfig('mainF', width=self.canvas.winfo_width())


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def scrollDown(self):
        self.canvas.yview_moveto('1')


    def movePicsToCollection(self,parentId):
        stories = getStoriesFromParent(self.db,self.settings,parentId)
        if not stories:
            insertError(f"""DB error - Could not fetch Stories from Parent ID""",self.settings['errLog'])
            messagebox.showerror(title='Error', message="Oppsss\nCould not get pictures from selected folder.")
            return

        picturesFromFolder = listDir(self.folderToFetchPics,['png','jpg','jpeg'])
        tempFilenames = None
        tempPicturesFolderIndex = None
        copyFlag = None
        ErrorsFlag = False
        for story in stories:
            tempFilenames = [convertnameToPath(story['name']), convertnameToPath(story['name'],True)]
            tempPicturesFolderIndex = self.findStoryPictureFromName(tempFilenames,picturesFromFolder)
            if tempPicturesFolderIndex: #pic found
                copyFlag = copyFile(picturesFromFolder[tempPicturesFolderIndex],self.settings['pics']['storiesFolderPath'] + str(story['id']) + '.' + picturesFromFolder[tempPicturesFolderIndex].split('.')[-1])
                if copyFlag != True: #err copying file
                    insertError(f"""OS error - {copyFlag}""",self.settings['errLog'])
                    ErrorsFlag = True
        if ErrorsFlag:
            messagebox.showerror(title='Error', message="Oppsss\nCould not copy all Pictures to App\nPlease read log for more info.")



    def findStoryPictureFromName(self,storyNameOptionsArr,directoryContentArr):
        for index,fileName in enumerate(directoryContentArr):
            for storyName in storyNameOptionsArr:
                if fileName.split('/')[-1].split('.')[0].lower() == storyName.lower():
                    return index

        return None
