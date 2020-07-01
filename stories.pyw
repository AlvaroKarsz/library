from dbFunctions import *

class Stories:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'My Stories'
        self.markAsReadedFlag = False
        self.picturesFolder = self.settings['pics']['storiesFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Story Name, ABC','Story Name, ZYX','Collection Name, ABC','Collection Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['id',False],['id',True],['name',False],['name',True],['parent_name',False],['parent_name',True],['pages',False],['pages',True],['year',False],['year',True]]
        self.updateOption = None

    def setData(self):
        return fetchAllMyStories(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchStoryById(db,settings,id)
