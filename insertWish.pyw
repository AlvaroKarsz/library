from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dbFunctions import *
from functions import *
from tkinter.filedialog import askopenfilename
from confirmPic import Confirm
import re
from threading import Thread


class InsertWish:
    def __init__(self,win,settings,db,rootWindow,autoValues = {},destoryAfter = False,updateID = False, hook = False):
        self.window = win
        self.rootWindow = rootWindow
        self.db = db
        self.sucess = BooleanVar()
        self.settings = settings
        self.destoryAfter = destoryAfter
        self.hook = hook
        self.updateID = updateID
        self.setCheckboxStyle()
        self.closeOnclick()
        self.addTitle()
        self.addInputs(autoValues)
        self.addSerie(autoValues)
        self.addInsertButton()
        self.addAutoFillLabel()


    def addTitle(self):
        Label(self.window,
        text = 'Insert New Wish Book',
        font=('Arial', 20),
        background='black',
        foreground='white'
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
            self.year.set(autoValues['year'])

        self.isbn = StringVar()
        if 'isbn' in autoValues:
            self.isbn.set(autoValues['isbn'])

        self.addNewLabelAndInput(fram,'Book Name','name')
        self.addNewLabelAndInput(fram,'Author Name','author')
        self.addNewLabelAndInput(fram,'Publication Year','year')
        self.addNewLabelAndInput(fram,'ISBN','isbn')
        fram.pack()


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
        self.autoFetcherLabel.pack()
        self.autoFetcherLabel.bind('<Button-1>',self.autoFillCallback)


    def autoFillCallback(self,event):
        isbn = self.isbn.get()
        name = self.name.get()

        if isbn or name:
            self.autoFetcherLabel.pack_forget()
            threadId = getRandomStr(50) #random string
            self.autoFetchThreadID = threadId
            #fetch as thread - if not the pack_forget will occur after the fetch - gui takes time..
            thread = Thread(target = lambda: self.autoFetchThread(threadId,isbn,name))
            thread.daemon = True # kill if window is closed
            thread.start()


    def autoFetchThread(self,threadId,isbn,name):
        #priority to isbn, if isbn is not set - go by name
        if isbn:
            #fetch by isbn
            data = getDataFromIsbn(isbn,self.settings)
            if self.autoFetchThreadID == threadId and data : # still relevant and the isbn was found
                self.name.set(data['name'])
                self.author.set(data['author'])
                self.year.set(data['year'])
        else:
            #fetch isbn by title, then get data
            isbn = getIsbn(name,self.settings)
            if self.autoFetchThreadID == threadId and isbn : # still relevant and the isbn was found
            #now fetch data from isbn
                data = getDataFromIsbn(isbn,self.settings)
                if self.autoFetchThreadID == threadId and data : # still relevant and the isbn was found
                    self.name.set(data['name'])
                    self.author.set(data['author'])
                    self.year.set(data['year'])
                    self.isbn.set(isbn)

        self.autoFetcherLabel.pack()


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


    def addNewLabelAndInput(self,prent,text,varName):
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


    def addSerie(self,autoValues):
        series = {}
        for serie in fetchAllSeries(self.db,self.settings):
            series[serie[1]] = serie[0]
        self.series = series
        self.isSerie = BooleanVar()

        tempFrame = Label(self.window,background='black',foreground='white')
        checkB = Checkbutton(tempFrame,
        text = 'Part Of Serie',
        style='Red.TCheckbutton',
        variable = self.isSerie,
        command = lambda : self.isSerieBind()
        )
        checkB.pack()
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
        btn.pack(pady=(5,0))
        btn.bind('<Button-1>',lambda e: self.checkOut())


    def checkOut(self):
        vars = self.getAllVars()
        check = self.checkVars(vars)
        if check != True:
            messagebox.showerror(title='Error', message=check)
            return

        if self.hook:
            self.hook(self,vars,self.updateID)
            #if set - remove the window
            if self.destoryAfter:
                self.justDissapear()

        else:
            flag = insertNewWish(self.db,self.settings,vars)
            if flag != True:
                insertError(f"""DB error - {flag}""",self.settings['errLog'])
                messagebox.showerror(title='Error', message="Oppsss\nDB error.\nPlease read LOG for mofe info.")
                return

            messagebox.showinfo('Message',f'''New Wish Book Saved.''')
            self.clearInputs()
            fileApiPath = fetchPic(vars['isbn'],self.settings)
            if fileApiPath: #cover was fetched
                confirmation = self.popupConfirmPic(fileApiPath,"Would you like to use this picture?","Yes","No")
                _self = self #acess from another class object
                confirmation.sucess.trace("w", lambda self, *args: _self.apiPictureResponse(confirmation.sucess,vars['name'],fileApiPath))
            else: # could not fetch cover from api, ask if want to upload new pic
                self.askOperatorToUploadPic(vars['name'])


    def apiPictureResponse(self,responseTrack,bookName,bookApiPath):
        self.displayMainWindow()
        if responseTrack.get():#user want to keep the picture
            copyFlag = self.copyPicture(bookName,bookApiPath)
            if not copyFlag: #could not copy - delete the file
                self.destoryPicture(bookApiPath)
        else: #not want to use the api cover, maybe want a pic from PC
            self.destoryPicture(bookApiPath)
            self.askOperatorToUploadPic(bookName)




    def killWidget(self,wid):
        if wid:
            wid.destroy()

    def justDissapear(self):
        self.window.destroy()


    def askOperatorToUploadPic(self,bookName):
        if messagebox.askyesno("Question","Would you like to add a picture?"):
            filename = askopenfilename()
            if filename:
                self.copyPicture(bookName,filename)


    def destoryPicture(self,path):
        destoryFlag = destroyFile(path)
        if path != True: #could not destory - update log
            insertError(f"""OS error - could not delete a file\nPath: {path}\nError: {destoryFlag}""",self.settings['errLog'])



    def copyPicture(self,bookName,filePath):
        bookNameAsFile = convertnameToPath(bookName) + getExtensionFromPath(filePath)
        flag = copyFile(filePath,self.settings['pics']['wishFolderPath'] + bookNameAsFile)
        if flag != True:
            insertError(f"""OS error - {flag}""",self.settings['errLog'])
            messagebox.showerror(title='Error', message="Oppsss\nOS error.\nCould not copy the picture.\nPlease read LOG for mofe info.")
            return True
        else:
            messagebox.showinfo('Message',f'''Picture Copied.''')
            return False


    def clearInputs(self):
        self.name.set('')
        self.isbn.set('')
        self.author.set('')
        self.year.set('')
        self.isSerie.set(False)
        self.serieFrame.pack_forget()


    def checkVars(self,vars):
        if not vars['isbn']:
            return 'Empty ISBN'
        if not re.match('^[0-9a-zA-Z\-]+$',vars['isbn']):
            return 'Invalid ISBN'
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
        res['isbn'] = self.isbn.get().strip().replace('-','')
        if self.isSerie.get():
            res['serie'] = {}
            res['serie']['id'] = self.series[self.serieVar.get().strip()]
            res['serie']['number'] = self.serieNumber.get().strip()
        return res


    def setCheckboxStyle(self):
        s = Style()
        s.configure('Red.TCheckbutton', foreground='white',background='black')


    def popupConfirmPic(self,path,str,yesBtn,noBtn):
        self.hideMainWindow()
        canvas = self.makeOverlayAndPopUp(self.rootWindow,"black",2,"white",self.settings['confirm']['padx_popup'],self.settings['confirm']['pady_popup'])
        return Confirm(canvas,self.settings,path,str,yesBtn,noBtn)


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


    def hideMainWindow(self):
        self.window.pack_forget()


    def displayMainWindow(self):
        self.window.pack(
        side="top",
        fill="both",
        expand=True,
        padx=self.settings['insertWish']['padx_popup'],
        pady=self.settings['insertWish']['pady_popup']
        )
