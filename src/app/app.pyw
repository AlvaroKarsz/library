import sys
appSrcPath = 'C:\/Users\/Alvaro\/Desktop\/myApp\/src\/'
sys.path.insert(0, appSrcPath + 'db')
sys.path.insert(0, appSrcPath + 'insertions')
sys.path.insert(0, appSrcPath + 'display')
sys.path.insert(0, appSrcPath + 'drive')
sys.path.insert(0, appSrcPath + 'classes')
sys.path.insert(0, appSrcPath + 'functions')
sys.path.insert(0, appSrcPath + 'statistics')


from settings import settings
from dbConnection import db
from bookList import App
from tkinter import *



window = Tk()
window.iconbitmap(default=settings['icons']['logo'])
window.title('My Library')

App(window,settings,db)
window.mainloop()
