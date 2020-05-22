from dbFunctions import *

class Series:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'My Series'
        self.markAsReadedFlag = False
        self.picturesFolder = self.settings['pics']['seriesFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Serie Name, ABC','Serie Name, ZYX','Owned Books, Biggest First','Owned Books, Lowest First','Readed Books, Biggest First','Readed Books, Lowest First','Wished Books, Biggest First','Wished Books, Lowest First']
        self.sortTranslations = [['id',False],['id',True],['name',False],['name',True],['books',True],['books',False],['books_read',True],['books_read',False],['wish_books',True],['wish_books',False]]


    def setData(self):
        return fetchAllMySeries(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchSerieById(db,settings,id)
