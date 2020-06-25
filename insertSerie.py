from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
from tkinter.filedialog import askopenfilename
import re

class InsertSerie:
    def __init__(self,win,settings,db):
        self.window = win
        self.db = db
        self.sucess = BooleanVar()
        self.settings = settings
        self.closeOnclick()
        self.addTitle()
        self.addInputs()
        self.addInsertButton()


    def addTitle(self):
        Label(self.window,
        text = 'Insert New Books Serie',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=20)


    def addInputs(self):
        fram = Label(self.window,background='black',foreground='white')
        self.name = StringVar()
        self.author = StringVar()
        self.addNewLabelAndInput(fram,'Serie Name',1,0,'name')
        self.addNewLabelAndInput(fram,'Author Name',2,0,'author')
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
        if check != True:
            messagebox.showerror(title='Error', message=check)
            return
        else:
            flag = insertNewSerie(self.db,self.settings,vars)
            if flag != True:
                insertError(f"""DB error - {flag}""",self.settings['errLog'])
                messagebox.showerror(title='Error', message="Oppsss\nDB error.\nPlease read LOG for mofe info.")
            else:
                messagebox.showinfo('Message',f'''New Books Serie Saved.''')
                self.clearInputs()
                if messagebox.askyesno("Question","Would you like to add a picture?"):
                    filename = askopenfilename()
                    if filename:
                        serieName = convertnameToPath(vars['name']) + getExtensionFromPath(filename)
                        flag = copyFile(filename,self.settings['pics']['seriesFolderPath'] + serieName)
                        if flag != True:
                            insertError(f"""OS error - {flag}""",self.settings['errLog'])
                            messagebox.showerror(title='Error', message="Oppsss\nOS error.\nCould not copy the picture.\nPlease read LOG for mofe info.")
                        else:
                            messagebox.showinfo('Message',f'''Picture Copied.''')


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
