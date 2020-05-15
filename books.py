from dbFunctions import *

class Books:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db



    def setData(self):
        return fetchMyLibrary(self.db,self.settings)


    def setSortOptions(self):
        return ['ID, Lowest first','ID, Latest first','Book Name, ABC','Book Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']


    def setSortTranslations(self):
        return [['id',False],['id',True],['name',False],['name',True],['pages',False],['pages',True],['year',False],['year',True]]


    def setPituresFolder(self):
        return self.settings['pics']['picFolderPath']


    def fetchById(db,settings,id):
        return fetchBookById(db,settings,id)
