from tkinter import *
from tkinter.ttk import *


class Filter:
    def __init__(self,parent,comboBox,textvariable=None):
        self.__list = list
        self.__comboBox = comboBox
        self.__allOptions = comboBox['values']
        self.__textvariable = textvariable
        self.__filterValue = StringVar()
        self.__filter = Entry(parent, textvariable = self.__filterValue)
        self.__initSort()
        self.__setKeyEventFilter()


    def __initSort(self):
        vals = list(self.__allOptions)
        vals.sort()
        self.__comboBox['values'] = vals
        if self.__textvariable:
            self.__textvariable.set(vals[0] if len(vals) > 0 else "")

    def __setKeyEventFilter(self):
        self.__filter.bind("<KeyRelease>",self.__doFilter)


    def __doFilter(self,evt):
        leftOptions = []
        filter = self.__filterValue.get().strip().lower()
        for opt in self.__allOptions:
            if filter in str(opt).lower():
                leftOptions.append(opt)


        leftOptions.sort()
        self.__comboBox['values'] = leftOptions

        if self.__textvariable:
            self.__textvariable.set(leftOptions[0] if len(leftOptions) > 0 else "")


    def get(self):
        return self.__filter
