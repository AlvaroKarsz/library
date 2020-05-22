from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
import re

class InsertBook:
    def __init__(self,win,settings,db,autoValues = {},destoryAfter = False):
        self.window = win
        self.db = db
        self.sucess = StringVar() # trace
        self.settings = settings
        self.destoryAfter =
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
        background='white',
        ).pack(pady=20)

    def addInputs(self,autoValues):
        fram = Label(self.window,background='white')

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
        btn = Button(self.window,
        text = 'X',
        command = self.killWindow
        )
        btn.pack(side=TOP, anchor=NE,padx=3,pady=3)


    def justDissapear(self):
        self.window.destroy()

    def killWindow(self):
        self.justDissapear()
        self.sucess.set(0)


    def addNewLabelAndInput(self,prent,text,row,column,varName):
        innerFrame = Label(prent,background='white')
        label = Label(innerFrame,text=text,background='white')
        label.pack(side=LEFT)
        entry = Entry(innerFrame,textvariable = getattr(self, varName))
        entry.pack(side=RIGHT)
        innerFrame.pack(pady=5,fill=X)

    def addCheckBoxGroup(self,parent,optionJson):
        innerFrame = Label(parent,background='white')
        self.type = StringVar()
        self.type.set(False)
        for cBox in optionJson:
            Checkbutton(innerFrame,onvalue = cBox['value'],text = cBox['text'],variable = self.type).pack(side=LEFT,padx=7,pady=5)
        innerFrame.pack()


    def addCollectionElements(self):
        fr = Label(self.window,background='white')
        topNav = Label(fr,background='white')
        self.isCollection = BooleanVar()
        Checkbutton(topNav,
        text = 'Collection of stories',
        variable = self.isCollection,
        command = lambda : self.isCollectionBind(btn)
        ).pack(side=LEFT)
        btn = Button(topNav,
        text = "+",
        width=3,
        command = lambda : self.addNewCollectionEntry()
        )
        self.isCollectionFrame = Label(fr,background='white')
        self.isCollectionNextRow = 0
        self.collectionArr = []
        topNav.pack()
        fr.pack()

    def isCollectionBind(self,btn):
        if not self.isCollection.get():
            for i in self.isCollectionFrame.winfo_children():
                i.destroy()
            self.isCollectionFrame.pack_forget()
            btn.pack_forget()
            self.isCollectionNextRow = 0
            self.collectionArr = []
        else:
            btn.pack(side=LEFT)
            self.isCollectionFrame.pack()
            self.addNewCollectionEntry()

    def addNewCollectionEntry(self):
        line = Label(self.isCollectionFrame,background='white')
        a = StringVar()
        b = StringVar()
        self.collectionArr.append({'name':a,'pages':b})
        Label(line,text='Story Name:',background='white').pack(side=LEFT)
        Entry(line,textvariable = a).pack(side=LEFT)
        Label(line,text='Pages:',background='white').pack(side=LEFT)
        Entry(line,textvariable = b).pack(side=LEFT)
        line.pack(pady=7)
        self.isCollectionNextRow += 1

    def addSerie(self,autoValues):
        series = {}
        for serie in fetchAllSeries(self.db,self.settings):
            series[serie[1]] = serie[0]
        self.series = series
        self.isSerie = BooleanVar()

        tempFrame = Label(self.window,background='white')
        Checkbutton(tempFrame,
        text = 'Part Of Serie',
        variable = self.isSerie,
        command = lambda : self.isSerieBind()
        ).pack()
        self.serieVar = StringVar()
        self.serieNumber = StringVar()
        self.serieVar.set(list(series)[0])
        self.serieFrame = Label(tempFrame,background='white')
        self.serieFrame.pack()
        Combobox(self.serieFrame,
        textvariable = self.serieVar,
        values = [*series.keys()],
        state="readonly").pack(side=LEFT,padx=5)
        Label(self.serieFrame,text = 'Number',background='white').pack(side=LEFT)
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
        Button(self.window,
        text = 'Save',
        command = self.checkOut
        ).pack()

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
        tempF = Label(self.window,background='white')
        self.isFollowed = BooleanVar()
        Checkbutton(tempF,
        text = 'Is Followed',
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
        fr = Label(self.window,background='white')
        Checkbutton(fr,
        text = 'Is Preceded',
        variable = self.isPreceded,
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
