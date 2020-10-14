from tkinter import *
from dbFunctions import *
from functions import *
from threading import Thread
import matplotlib.pyplot as plt

class Statistics:
    def __init__(self,win,settings,db):
        win.configure(background = 'black')
        thrd = Thread(target = lambda: self.getStatisticsFromDB(db,settings))
        thrd.daemon = True
        thrd.start()
        self.window = win
        self.addTitle()


    def addTitle(self):
        Label(self.window,
        text = f'''Library Statistics''',
        font=('Arial', 20),
        background='black',
        foreground='white'
        ).pack(pady=20)


    def getStatisticsFromDB(self,db,settings):
        stats = makeStats(db,settings)[0]
        self.body = Label(self.window, background = 'black')
        self.body.pack(fill=BOTH, expand=True)
        self.makeTotalStats(stats['total'][0])


    def makeSimpleLabel(self,text,parent):
        Label(parent,
        text=text,
        background = 'black',
        foreground = 'white',
        font=('Arial', 17),
        anchor='w'
        ).pack(fill=X,expand = True, padx=7, pady=0)


    def makeTotalStats(self,data):
        self.makeSimpleLabel(f"""You have {data['total_books']} books in your Library.""", self.body)
        self.makeSimpleLabel(f"""With total of {data['total_pages']} Pages.""", self.body)
        self.makeSimpleLabel(f"""You have readed {data['readed_books']} Books.""", self.body)
        self.makeSimpleLabel(f"""You have readed {data['readed_pages']} Pages.""", self.body)
        self.makePieChart(['Readed Books', 'Not Readed Books'], [data['readed_books'], data['total_books'] - data['readed_books'] ])


    def makePieChart(self,labels, sizes):
        explode =  [0] * len(labels)
        explode[0] = 0.1
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.ioff()
        plt.show()
