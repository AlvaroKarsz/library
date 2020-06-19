from dbFunctions import *

class Wishlist:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'My Wish List'
        self.markAsReadedFlag = False
        self.picturesFolder = self.settings['pics']['wishFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Book Name, ABC','Book Name, ZYX','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['id',False],['id',True],['name',False],['name',True],['year',False],['year',True]]


    def setData(self):
        return fetchMyWishlist(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchWishById(db,settings,id)


    def deleteById(db,settings,id):
        return deleteFromWishList(db,settings,id)
