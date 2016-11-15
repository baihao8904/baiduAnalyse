# -*- coding:utf-8 -*-
#新的百度抓取程序 不再存在本地的html文件中，利用Mongodb存储相关信息

import pymongo
from snownlp import SnowNLP
import requests
import re
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost',27017)
sougou_infoProject = client['sougou_infoProject']
sougou_info = sougou_infoProject['sougou_info']


def get_info(base_url,start,totalnum=1):
    for questionNum in range(start,start+totalnum):
        url = base_url.format(str(questionNum))
        wb_data = requests.get(url)
        Soup = BeautifulSoup(wb_data.text,'lxml')
        print(url)
        if not Soup.select('div.question-tit'):
            print('该问题已失效')
        else:
            #div.question-main satisfaction-answer 反映最佳答案的标签 写一个判断
            print('正在处理%d问题' %questionNum)
            #获得提问标题
            ask_title = Soup.select('h3#questionTitle')[0].text
            print(ask_title)
            #获得提问描述
            askContent = Soup.select('div.replenish-con')
            ask_content=''
            for item in askContent:
                ask_content += item.text
            print(ask_content)
            # relatedAnswe##s_main > div.container > div.column1 > div:nth-child(3) > div > div.answer-con > p
            answerCon = Soup.select('#s_main > div.container > div.column1 > div:nth-of-type(3) > div > div.answer-con')
            answerContext = answerCon[0].text.strip()
            ansText = ''
            for i in answerContext:
                if i!='\r' and i!= '\n' and i!='\t' and i!=' ':
                    ansText +=i
            print(ansText)
            #用正则表达式将最佳答案中的描述分开

            print(re.findall(r's追问',ansText))



if __name__ == '__main__':
    base_url = 'http://wenwen.sogou.com/z/q{}.htm'
    get_info(base_url,652549450)