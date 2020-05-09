from settings import settings
from dbConnection import db
from bookList import App
from tkinter import *

window = Tk()
App(window,settings,db)
window.mainloop()
