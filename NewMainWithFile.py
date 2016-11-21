# -*- coding:utf-8 -*-
#新的百度抓取程序 不再存在本地的html文件中，利用Mongodb存储相关信息

import pymongo
from snownlp import SnowNLP
import jieba
import jieba.analyse
import requests
import re
from bs4 import BeautifulSoup
import time
import os

client = pymongo.MongoClient('localhost',27017)
sougou_infoProject = client['sougou_infoProject']
sougou_info = sougou_infoProject['sougou_info']
path = './data'

def get_info(base_url,start,totalnum=1):
    if not os.path.exists(path):
        os.mkdir(path)
    for questionNum in range(start,start+totalnum):
        time.sleep(0.1)
        url = base_url.format(str(questionNum))
        wb_data = requests.get(url)
        Soup = BeautifulSoup(wb_data.text,'lxml')
        print(url)
        if not Soup.select('div.question-tit'):
            print('该问题已失效')
        else:
            #反映最佳答案的标签 写一个判断
            if Soup.select('div.question-main.satisfaction-answer'):
                print('找到了最佳答案')

                print('正在处理%d问题' %questionNum)
                #获得提问标题
                ask_title = Soup.select('h3#questionTitle')[0].text
                #获得提问描述
                askContent = Soup.select('div.replenish-con')
                ask_content=''
                for item in askContent:
                    ask_content += item.text
                answerCon = Soup.select('#s_main > div.container > div.column1 > div:nth-of-type(3) > div > div.answer-con')
                if len(answerCon)>0:
                    answerContext = answerCon[0].text.strip()
                    ansText = ''
                    for i in answerContext:
                        if i!='\r' and i!= '\n' and i!='\t' and i!=' ':
                            ansText +=i
                    #用正则表达式将最佳答案中的描述分开,并找出最佳答案
                    bestAnsList = []
                    bestAnswer=''
                    if re.findall(r'追问',ansText):
                         bestAnsList = ansText.split('追问：')
                         if re.findall(r'补充',bestAnsList[0]):
                             bestAnswer = ''.join(bestAnsList[0].split('补充：'))
                else:
                    continue

                #用提问和回答进行关键词和情感分析
                #提问关键词
                ask_keyword = jieba.analyse.extract_tags(ask_title+ask_content,5)
                #回答关键词
                answer_keyword = jieba.analyse.extract_tags(bestAnswer,5)
                askKeywordList=[]
                answerKeywordList=[]
                for item in ask_keyword:
                    askKeywordList.append(item)
                for item in answer_keyword:
                    answerKeywordList.append(item)
                tmp = [val for val in askKeywordList if val in answerKeywordList]
                if len(tmp)>0:
                    keywordScore =len(tmp)*20
                else:
                    keywordScore = 0

                #情感分析
                try:
                    askSE = SnowNLP(ask_title+ask_content).sentiments
                    answerSE = SnowNLP(bestAnswer).sentiments
                    SEscore = (askSE-answerSE)**2
                    Sentiment_score = 70 - SEscore*100
                except:
                    SEscore = 0.5
                    Sentiment_score = 30


                #获得问题的点赞数和反对数
                supportNum = int(Soup.select('a.operate-support')[0].get('num'))
                opposeNum = int(Soup.select('a.operate-oppose')[0].get('num'))


                data = {
                    'ask_id':questionNum,
                    'keyword_score':len(tmp),
                    'Sentiment_score':SEscore,
                    'Support_num':supportNum,
                    'Oppose_num':opposeNum,
                    'final_score':keywordScore+Sentiment_score+opposeNum+supportNum
                }

                with open(path+'/totaldata.txt','a') as _file:
                    _text = str(str(data['Support_num'])+'\t'+str(data['Oppose_num'])+'\t'+str(data['Sentiment_score'])+'\t'+   \
                      str(data['keyword_score'])+'\t'+str(data['final_score'])+'\n')
                    _file.write(_text)

            else:
                print('问题没有最佳答案 跳过')



if __name__ == '__main__':
    base_url = 'http://wenwen.sogou.com/z/q{}.htm'
    get_info(base_url,452566700,200000)

    #652549630
    #452578004