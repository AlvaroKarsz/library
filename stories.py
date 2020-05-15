from dbFunctions import *

class Stories:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db



    def setData(self):
        return fetchAllMyStories(self.db,self.settings)


    def setSortOptions(self):
        return ['ID, Lowest first','ID, Latest first','Story Name, ABC','Story Name, ZYX','Collection Name, ABC','Collection Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']


    def setSortTranslations(self):
        return [['id',False],['id',True],['name',False],['name',True],['parent_name',False],['parent_name',True],['pages',False],['pages',True],['year',False],['year',True]]


    def setPituresFolder(self):
        return self.settings['pics']['storiesFolderPath']


    def fetchById(db,settings,id):
        return fetchStoryById(db,settings,id)
