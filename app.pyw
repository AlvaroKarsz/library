from settings import settings
from dbConnection import db
from bookList import App
from tkinter import *


window = Tk()
window.iconbitmap(default=settings['icons']['logo'])
window.title('My Library')
App(window,settings,db)
window.mainloop()
