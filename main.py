# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 13:38:50 2019

@author: zeng
"""

import sys
import cv2 as cv
import numpy as np
import requests
import json
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QInputDialog,QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton,QTextEdit,QLineEdit)
from PyQt5.QtCore import pyqtSignal
from subwin import subwin

#借用GUI用于显示PM2.5并保存
#开一个子窗口显示是否成功，更有仪式感
'''
class subwin(QDialog):
    def __init__(self):
        
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(200,150)
        self.btnClose = QPushButton('click to close',self)
        self.label = QLabel('successfully get!')
        self.setWindowTitle('获取成功！')
        
        layout = QGridLayout(self)
        layout.addWidget(self.label,0,1,3,4)
        layout.addWidget(self.btnClose,4,1,1,1)
        
        self.btnClose.clicked.connect(self.close) 
'''        
class showwin(QDialog):
    #显示窗口
    
    
    
    
    
    def __init__(self):
        
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(600,400)
        self.text=QTextEdit()
        leftLayout = QGridLayout() 
        leftLayout.addWidget(self.text, 2, 1, 1, 40)
        mainLayout = QGridLayout(self)
        mainLayout.addLayout(leftLayout, 0, 0)
        #信号到来时启用显示函数
        w.mySignal.connect(self.show)

    def show(self,connect):
        #显示接收到的数据
        self.text.setText(connect)

       
class win(QDialog):
    mySignal = pyqtSignal(str)
    #信号传递，将主窗口爬虫爬下来的数据传递给显示窗口
    
    def __init__(self):

        # 初始化一个ndarray, 用于存储爬取的数据
        self.text = np.ndarray(())

        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Show', self)
        self.btnSave = QPushButton('Save', self)
        self.btnGet = QPushButton('Get', self)
        self.btnQuit = QPushButton('Quit', self)
        self.btnOk = QPushButton('Input city',self)
        self.setWindowTitle('空气质量获取器')
        
        
        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnGet, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)
 #       layout.addWidget(label1,5,1,1,1)
        layout.addWidget(self.btnOk,3,2,1,2)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.showSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnGet.clicked.connect(self.getSlot)
        self.btnQuit.clicked.connect(self.close)
        self.btnOk.clicked.connect(self.to)
        
    def to(self):
        self.city, okPressed = QInputDialog.getText(self,"Get City","The city you want to check",QLineEdit.Normal,"")      
        
        
        
    def showSlot(self):
        #输出函数，打开一个新的窗口输出
        showWin=showwin()
        #传递函数
        self.mySignal.emit(self.text)       
        showWin.exec_()
        
    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Data', './__data', '*.txt', '*.txt')

        if fileName is '':
            return
        f=open(fileName,"w")
        f.write(self.text)

    def getSlot(self):
        #使用之前得到的城市字符串完善URL爬取数据
        string1='http://www.pm25.in/api/querys/co.json?city='
        string2='&token=5j1znBVAsnSf5xQyNQyq'
        url=string1+self.city+string2
        r = requests.get(url)
        hjson = json.loads(r.text)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.text = js
        #成功获取的提示
        newWindow = subwin()
        newWindow.show()
        newWindow.exec_()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())