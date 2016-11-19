# -*- coding:utf-8 -*-
__author__ = 'lenovo'

import pymongo
import os

client = pymongo.MongoClient('localhost',27017)
sougou_infoProject = client['sougou_infoProject']
sougou_info = sougou_infoProject['sougou_info']

print('总计有：'+str(sougou_info.find().count())+'个问题')
print('有效问题：'+str(sougou_info.find({'final_score':{'$gt':30}}).count()))

os_path = './data'
if not os.path.exists(os_path):
    os.mkdir(os_path)

with open(os_path+'/GoodQuestion.txt','w') as _file:
    for item in sougou_info.find({'final_score':{'$gt':30}}):
        #大部分数据没有赞成和反对
        #item['Support_num'])+'\t'+str(item['Oppose_num'])+'\t'+
        _text = str(str(item['Sentiment_score'])+'\t'+   \
                      str(item['keyword_score'])+'\t'+str(80)+'\n')
        _file.write(_text)

print('final!')