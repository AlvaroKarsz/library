from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
from tkinter.filedialog import askopenfilename
import re

class InsertWish:
    def __init__(self,win,settings,db):
        self.window = win
        self.db = db
        self.sucess = BooleanVar()
        self.settings = settings
        self.closeOnclick()
        self.addTitle()
        self.addInputs()
        self.addSerie()
        self.addInsertButton()


    def addTitle(self):
        Label(self.window,
        text = 'Insert New Wish Book',
        font=('Arial', 20),
        background='white',
        ).pack(pady=20)


    def addInputs(self):
        fram = Label(self.window,background='white')

        self.name = StringVar()

        self.author = StringVar()

        self.year = StringVar()
        self.addNewLabelAndInput(fram,'Book Name',1,0,'name')
        self.addNewLabelAndInput(fram,'Author Name',2,0,'author')
        self.addNewLabelAndInput(fram,'Publication Year',3,0,'year')
        fram.pack()


    def closeOnclick(self):
        btn = Button(self.window,
        text = 'X',
        command = self.killWindow
        )
        btn.pack(side=TOP, anchor=NE,padx=3,pady=3)


    def killWindow(self):
        self.window.destroy()
        self.sucess.set(True)


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


    def addSerie(self):
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
            flag = insertNewWish(self.db,self.settings,vars)
            if flag != True:
                insertError(f"""DB error - {flag}""",self.settings['errLog'])
                messagebox.showerror(title='Error', message="Oppsss\nDB error.\nPlease read LOG for mofe info.")
            else:
                messagebox.showinfo('Message',f'''New Wish Book Saved.''')
                self.clearInputs()
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



    def clearInputs(self):
        self.name.set('')
        self.author.set('')
        self.year.set('')
        self.isSerie.set(False)
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
        if 'serie' in vars:
            if not vars['serie']['id']:
                return 'Empty Serie Name'
            if not vars['serie']['number']:
                return 'Empty Serie Number'
            if not  re.match('^[0-9]+$',vars['serie']['number']):
                return 'Invalid Serie Number'
        return True


    def getAllVars(self):
        res = {}
        res['name'] = self.name.get().strip()
        res['author'] = self.author.get().strip()
        res['year'] = self.year.get().strip()
        if self.isSerie.get():
            res['serie'] = {}
            res['serie']['id'] = self.series[self.serieVar.get().strip()]
            res['serie']['number'] = self.serieNumber.get().strip()
        return res
