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
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton)

#借用GUI用于显示PM2.5并保存
#开一个子窗口显示是否成功，更有仪式感
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
        
class win(QDialog):
    def __init__(self):

        # 初始化一个img的ndarray, 用于存储图像
        self.text = np.ndarray(())

        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnGet = QPushButton('Get', self)
        self.btnQuit = QPushButton('Quit', self)
 ##       self.label = QLabel('空气质量获取器')
        self.setWindowTitle('空气质量获取器')
        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnGet, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnGet.clicked.connect(self.getSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        # 调用打开文件diglog
 #       fileName, tmp = QFileDialog.getOpenFileName(
 #           self, 'Open Image', './__data', '*.txt')

  #      if fileName is '':
  #          return

        # 采用opencv函数读取数据
        self.refreshShow()
 #       if self.img.size == 1:
 #           return
     #判断文件打开失败语句
 #       self.refreshShow()
#把数据以txt形式保存
    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Data', './__data', '*.txt', '*.txt')

        if fileName is '':
            return
        f=open(fileName,"w")
        f.write(self.text)

    def getSlot(self):
 #抓取数据       
        r = requests.get('http://www.pm25.in/api/querys/co.json?city=hefei&token=5j1znBVAsnSf5xQyNQyq')
        hjson = json.loads(r.text)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.text = js
        newWindow = subwin()
        newWindow.show()
        newWindow.exec_()
#制作中的显示函数
    def refreshShow(self):
        # 显示txt文件中的数据
        show = QDialog()
        show.setWindowTitle('show the aqi of the city')
        show.resize(500,400)
        label = QLabel("城市空气质量：")
        show.addWidget(label, 0, 0)  
        show.addWidget(self.text, 0, 0, 1, 40) 

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())