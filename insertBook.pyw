from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
import re
from tkinter.filedialog import askopenfilename
import pandas as pd
from threading import Thread


class InsertBook:
    def __init__(self,win,settings,db,autoValues = {},destoryAfter = False):
        self.window = win
        self.db = db
        self.sucess = StringVar() # trace
        self.settings = settings
        self.destoryAfter = destoryAfter
        self.setCheckboxStyle()
        self.closeOnclick()
        self.addTitle()
        self.addInputs(autoValues)
        self.addType()
        self.addSerie(autoValues)
        self.addNextBook()
        self.addPrevBook()
        self.addCollectionElements()
        self.addInsertButton()

    def addType(self):
        self.addCheckBoxGroup(self.window,[{'value':'H','text':'Hard Cover','row':8,'column':0},{'value':'P','text':'Paper Back','row':8,'column':1},{'value':'HN','text':'Hardcover No Dust Jacket','row':8,'column':2}])

    def addTitle(self):
        Label(self.window,
        text = 'Insert New Book',
        font=('Arial', 20),
        background='black',
        foreground='white',
        ).pack(pady=20)

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
        self.lang = StringVar()
        self.oriLan = StringVar()
        self.isbn = StringVar()
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


    def addCheckBoxGroup(self,parent,optionJson):
        innerFrame = Label(parent,background='black',foreground='white')
        self.type = StringVar()
        self.type.set(False)
        for cBox in optionJson:
            Checkbutton(innerFrame,onvalue = cBox['value'],text = cBox['text'],variable = self.type,style='Red.TCheckbutton').pack(side=LEFT,padx=7,pady=5)
        innerFrame.pack()


    def addCollectionElements(self):
        fr = Label(self.window,background='black',foreground='white')
        topNav = Label(fr,background='black',foreground='white')
        self.isCollection = BooleanVar()
        Checkbutton(topNav,
        text = 'Collection of stories',
        variable = self.isCollection,
        style='Red.TCheckbutton',
        command = lambda : self.isCollectionBind(btn,lab)
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

        lab = Label(topNav,
        text='Import Csv/Excel',
        background='black',foreground='white'
        )
        lab.bind('<Button-1>',lambda event: self.handleTableImport())

        lab.configure(cursor="hand2")
        fTemp = font.Font(lab, lab.cget("font"))
        fTemp.configure(weight='bold')
        fTemp.configure(size=7)
        lab.configure(font=fTemp)


        self.isCollectionFrame = Label(fr,background='black',foreground='white')
        self.isCollectionNextRow = 0
        self.collectionArr = []
        topNav.pack()
        fr.pack()


    def handleTableImport(self):
        filename = askopenfilename()
        if not filename:
            return
        sheet =  'Sheet1'
        df = pd.read_excel(io=filename, sheet_name=sheet)
        nameColumn = df.columns[0]
        pagesColumn = df.columns[1]
        self.killAllChildren(self.isCollectionFrame)
        self.isCollectionFrame.pack_forget()
        self.isCollectionNextRow = 0
        self.collectionArr = []
        self.isCollectionFrame.pack()
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


    def isCollectionBind(self,btn,label):
        if not self.isCollection.get():
            self.killAllChildren(self.isCollectionFrame)
            self.isCollectionFrame.pack_forget()
            btn.pack_forget()
            label.pack_forget()
            self.isCollectionNextRow = 0
            self.collectionArr = []
        else:
            btn.pack(side=LEFT)
            label.pack(side=LEFT,padx=20)
            self.isCollectionFrame.pack()
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
        Combobox(self.serieFrame,
        textvariable = self.serieVar,
        values = [*series.keys()],
        state="readonly").pack(side=LEFT,padx=5)
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
        if check != True:
            messagebox.showerror(title='Error', message=check)
            return
        else:
            insertNewBook(self.db,self.settings,vars)
            self.clearInputs()
            if self.destoryAfter:
                self.justDissapear()
            else :
                if messagebox.askyesno("Question","Would you like to add a picture?"):
                    filename = askopenfilename()
                    if filename:
                        bookNameAsFile = convertnameToPath(vars['name']) + getExtensionFromPath(filename)
                        flag = copyFile(filename,self.settings['pics']['wishFolderPath'] + bookNameAsFile)
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
        if not vars['type'] or vars['type'] == '0':
            return 'Empty Type'
        if 'next' in vars and not vars['next']:
            return 'Bad Follow by Book'
        if 'prev' in vars:
            if not vars['prev']:
                return 'Bad Preceded by Book'
            if previousBookAlreadyHaveFollow(self.db,self.settings,vars['prev']):
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
        res['isbn'] = self.isbn.get().strip()
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

    def addNextBook(self):
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
        self.followedFrame = Frame(tempF)
        self.followedFrame.pack()
        Combobox(self.followedFrame,
        textvariable = self.followedVar,
        values = [*books.keys()],
        width=70,
        state="readonly").pack()
        self.followedFrame.pack_forget()
        tempF.pack()

    def isFollowedBind(self):
        if not self.isFollowed.get():
            self.followedFrame.pack_forget()
        else:
            self.followedFrame.pack(pady=7)

    def addPrevBook(self):
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
        self.precededFrame = Frame(fr)
        self.precededFrame.pack()
        combo = Combobox(self.precededFrame,
        textvariable = self.precededVar,
        values = [*self.books.keys()] ,
        width=70,
        state="readonly")
        combo.pack()
        self.precededFrame.pack_forget()
        fr.pack()

    def isPrecededBind(self):
        if not self.isPreceded.get():
            self.precededFrame.pack_forget()
        else:
            self.precededFrame.pack(pady=7)


    def setCheckboxStyle(self):
        s = Style()
        s.configure('Red.TCheckbutton', foreground='white',background='black')
