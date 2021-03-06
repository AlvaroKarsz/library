from dbFunctions import *

class Ordered:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'Ordered Books'
        self.markAsReadedFlag = False
        self.picturesFolder = self.settings['pics']['wishFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Rating - Higher','Rating - Lower','Purchased First','Purchased Last','Book Name, ABC','Book Name, ZYX','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['id',False],['id',True],['rating',True],['rating',False],['order_date',False,'date'],['order_date',True,'date'],['name',False],['name',True],['year',False],['year',True]]
        self.updateOption = 2
        self.changeCover = True

    def setData(self):
        return fetchMyOrderedlist(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchOrderedById(db,settings,id)


    def updateById(db,settings,json,id):
        return updateWishById(db,settings,json,id)
