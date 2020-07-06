from dbFunctions import *

class Reads:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'My Read List'
        self.markAsReadedFlag = False
        self.picturesFolder = self.settings['pics']['picFolderPath']
        self.sortOptions = ['Read Order','Read Order, Reverse','ID, Lowest first','ID, Latest first','Book Name, ABC','Book Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['read',False],['read',True],['id',False],['id',True],['name',False],['name',True],['pages',False],['pages',True],['year',False],['year',True]]
        self.updateOption = 1

    def setData(self):
        return fetchMyReadList(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchReadById(db,settings,id)

    def updateById(db,settings,json,id):
        return updateBookById(db,settings,json,id)
