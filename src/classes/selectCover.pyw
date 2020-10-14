from tkinter import *
from tkinter.ttk import *
from functions import *
from PIL import ImageTk, Image
from threading import Thread
from tkinter import messagebox


class CoverSelector:
    def __init__(self,win,settings,title,author,folderPath=False,id=False,returnValue=False,clearTemp=True,confirmAlert=True):
        self.window = win
        self.settings = settings
        self.returnValue = returnValue
        self.confirmAlert = confirmAlert
        self.clearTemp = clearTemp
        self.originalPic = self.getDestinationPath(folderPath,id) if folderPath and id else None
        self.selected = None
        self.trace = StringVar()
        self.defaultStringVarValue = 'abcd'
        self.trace.set(self.defaultStringVarValue)
        self.imagesHolder = []
        self.setBgColor(win,'black')
        self.addTitle()
        self.makeBody()
        self.setFetchingMessage()
        self.setOncloseEventListener()
        thId = Thread(target = lambda: self.fetchAndDisplayCovers(title,author))
        thId.daemon = True
        thId.start()

    def setOncloseEventListener(self):
        self.window.protocol("WM_DELETE_WINDOW", self.clearTmpOnclose)


    def clearTmpOnclose(self):
        if self.clearTemp:
            clearFolder(self.settings['tmp'])
        self.killWindow()


    def getDestinationPath(self,folder,id):
        path = getExtensionIfExist(folder + '/' + str(id))
        return path if path else folder + '/' + str(id) + '.jpg'


    def fetchAndDisplayCovers(self,title,author):
        picArr = getVarietyOfCoversFromBookNameAndAuthor(title,author,self.settings)
        self.addPictures(picArr)
        self.addSelectOption()


    def setFetchingMessage(self):
        self.fetchingLabel = Label(self.body,font=('Arial',20), text = 'Fetching Web...')
        self.fetchingLabel.pack(expand=True,pady=50)
        self.setBgColor(self.fetchingLabel,'black')
        self.setFgColor(self.fetchingLabel,'white')


    def makeBody(self):
        self.body = Label(self.window)
        self.body.pack(fill=BOTH,expand=True,padx=10,pady=10)
        self.setBgColor(self.body,'black')
        self.setFgColor(self.body,'white')

    def addPictures(self,picArr):
        self.fetchingLabel.destroy()
        row = Label(self.body)
        row.pack(fill=X,expand=True,padx=10,pady=10)
        self.setBgColor(row,'black')
        self.setFgColor(row,'white')
        imgHolder = False
        pic = False
        for i,val in enumerate(picArr):

            if i % 3 == 0 and i != 0: #3 in a row - create a new row
                row = Label(self.body)
                row.pack(fill=X,expand=True,padx=10,pady=10)
                self.setBgColor([row],'black')
                self.setFgColor([row],'white')

            pic = Image.open(val)
            pic = pic.resize((self.settings['pics']['covers_width'],self.settings['pics']['covers_height']))
            pic = ImageTk.PhotoImage(pic)
            imgHolder = Label(row,image = pic)
            self.clickableWidget(imgHolder)
            self.imagesHolder.append(imgHolder)
            imgHolder.image = pic
            imgHolder.pack(side=LEFT,expand=True)
            self.setFgColor(imgHolder,'white')
            self.setBgColor(imgHolder,'black')
            imgHolder.bind('<Button-1>',lambda z, img = imgHolder, path = val: self.selectThisCover(path,img)) #to pass by reference


    def selectThisCover(self,path,wid):
        #disselect all images
        for i in self.imagesHolder:
            self.removeBorder(i)
        #select this one
        self.addBorder(wid)
        #save path
        self.selected = path


    def clickableWidget(self,wid):
        wid.configure(cursor="hand2")


    def addBorder(self,wid):
        wid.configure(borderwidth = 30, relief="raised")


    def removeBorder(self,wid):
        wid.configure(borderwidth=0, relief="flat")


    def addTitle(self):
        Label(self.window,
        text = "Select the Wanted Cover",
        font=('Arial', 20),
        background='black',foreground='white'
        ).pack(pady=20)


    def setBgColor(self,widget,clr):
        if not isArray(widget):
            widget = [widget]

        for wid in widget:
            try:
                wid.configure(background=clr)
            except:
                try:
                    wid.configure(bg=clr)
                except:
                    continue


    def setFgColor(self,widget,clr):
        if not isArray(widget):
            widget = [widget]
        for wid in widget:
            try:
                wid.configure(foreground=clr)
            except:
                try:
                    wid.configure(fg=clr)
                except:
                    continue


    def addSelectOption(self):
        select = Label(self.body,font=('Arial', 18), text = "Select", cursor="hand2",background='black',foreground='white')
        select.pack(expand=True)
        select.bind('<Button-1>',self.select) #to pass by reference


    def select(self,evt):
        if not self.selected:
            messagebox.showerror(title='Error', message="Please select the wanted cover.")
            return

        if self.confirmAlert and not messagebox.askyesno(title='Sure?', message="Are you sure you want to save this cover?"):
            return

        if self.returnValue:
            self.trace.set(self.selected)
            self.killWindow()
            return

        if moveFile(self.selected,self.originalPic,self.settings,True) != True:
            messagebox.showerror(title='Error', message="Could not save the cover.")
            return

        messagebox.showinfo('Sucess','Cover was changed.\nReload the pictures to see the change.')
        self.clearTmpOnclose()


    def killWindow(self):
        if self.trace.get() == self.defaultStringVarValue:
            self.trace.set(False)
        self.window.destroy()
