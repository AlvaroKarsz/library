from dbFunctions import *

class Books:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.markAsReadedFlag = True
        self.picturesFolder = self.settings['pics']['picFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Book Name, ABC','Book Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['id',False],['id',True],['name',False],['name',True],['pages',False],['pages',True],['year',False],['year',True]]


    def setData(self):
        return fetchMyLibrary(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchBookById(db,settings,id)
