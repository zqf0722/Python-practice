# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:36:33 2019

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
#from homework.py import win

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
        
