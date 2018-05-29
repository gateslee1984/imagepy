# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:57:53 2016
@author: yxl
"""
import threading, wx

from ... import IPy
from ...ui.panelconfig import ParaDialog
from ...core.manager import WindowsManager, TextLogManager, TaskManager, WidgetsManager
from time import time

class Free:
    title = 'Free'
    view = None
    para = None
    prgs = (None, 1)
    asyn = True

    def progress(self, i, n):
        self.prgs = (i, n)

    def run(self, para=None):
        print('this is a plugin')
        
    def runasyn(self, para, callback=None):
        TaskManager.add(self)
        start = time()
        self.run(para)
        IPy.set_info('%s: cost %.3fs'%(self.title, time()-start))
        TaskManager.remove(self)
        if callback!=None:callback()

    def load(self):return True
        
    def show(self):
        if self.view==None:return wx.ID_OK
        with ParaDialog(WindowsManager.get(), self.title) as dialog:
            dialog.init_view(self.view, self.para, False, True)
            return dialog.ShowModal()
        
    def start(self, para=None, callback=None):
        if not self.load():return
        if para!=None or self.show() == wx.ID_OK:
            if para==None:para = self.para
            win = WidgetsManager.getref('Macros Recorder')
            if win!=None: 
                win.write('{}>{}'.format(self.title, para))
            if self.asyn and IPy.uimode()!='no':
                threading.Thread(target = self.runasyn, args = (para, callback)).start()
            else: 
                self.runasyn(para, callback)