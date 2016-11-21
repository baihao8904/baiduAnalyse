# -*- coding:utf-8 -*-
__author__ = 'lenovo'

import os

totalfile = open('./data/totaldata.txt')

goodNum = 0
for line in totalfile.readlines():
    LineList = line.split('\t')
    if int(LineList[-1])>=30:
        goodNum+=1

print('有效问题：'+str(goodNum))

os_path = './data'
if not os.path.exists(os_path):
    os.mkdir(os_path)

#指针指回文件头
totalfile.seek(0)

with open(os_path+'/GoodQuestionWithFile.txt','w') as _file:
    for item in totalfile.readlines():
        LineList = line.split('\t')
        print(LineList)
        if int(LineList[-1])>=30:
            _file.write(item)

print('final!')