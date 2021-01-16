from dbFunctions import *
from tkinter import messagebox

class Stories:
    def __init__(self,settings,db):
        self.settings = settings
        self.db = db
        self.title = 'My Stories'
        self.markAsReadedFlag = True
        self.picturesFolder = self.settings['pics']['storiesFolderPath']
        self.sortOptions = ['ID, Lowest first','ID, Latest first','Rating - Higher','Rating - Lower','Read Order','Read Order, Reverse','Story Name, ABC','Story Name, ZYX','Collection Name, ABC','Collection Name, ZYX','Number of Pages, Lowest first','Number of Pages, Biggest first','Publication Year, Lowest first','Publication Year, Latest first']
        self.sortTranslations = [['id',False],['id',True],['rating',True],['rating',False],['read',False],['read',True],['name',False],['name',True],['parent_name',False],['parent_name',True],['pages',False],['pages',True],['year',False],['year',True]]
        self.updateOption = None
        self.changeCover = True

    def setData(self):
        return fetchAllMyStories(self.db,self.settings)


    def fetchById(db,settings,id):
        return fetchStoryById(db,settings,id)


    def markReaded(db,settings,storyId,date):
        readedInfo = markStoryAsReaded(db,settings,storyId,date)
        alertString = f'''This is the {readedInfo['story']}th story you've readed.\n'''
        if readedInfo['book']:
            alertString += f'''By reading this story, you've completed the colletion, the {readedInfo['book']}th book you've readed!'''
        messagebox.showinfo('Change saved',alertString)
