# -*- encoding: utf-8 -*-

import os
import re
from snownlp import SnowNLP
import urllib2
import urllib
import jieba
import jieba.analyse
from bs4 import BeautifulSoup


def baidu_inputscore():
	base_url = 'http://zhidao.baidu.com/question/'
	print u'输入数据：'
	ch = input('please input a question number :')
	print u'获得问题'
	id = ch
	url = base_url + str(id)
	htmlpage = urllib2.urlopen(url).read()
	soup = BeautifulSoup(htmlpage)
	ask_title, ask_content = '', ''
	answer_content = []
	bestanswer_content = []
	comment = []
	cainalv = []
	rank = []
	zan = []
	piping = []
	#获得信息
	for line in soup.find_all('span'):
		if 'ask-title' in str(line):
			ask_title = line.get_text()
		if 'class="ml-10"' in str(line):
			cainalv = line.get_text()
		if 'class="evaluate evaluate-32"' in str(line):
			s = str(line)
			zan_list = s.split(' ')
			pzan = zan_list[4]
			zan = pzan[15:-1]
		if 'class="evaluate evaluate-bad evaluate-32"' in str(line):
			s2 = str(line)
			piping_list = s2.split(' ')
			ppiping = piping_list[5]
			piping = ppiping[15:-1]
	for line in soup.find_all('pre'):
		if 'q-content' in str(line):
			ask_content = line.get_text()
		if 'best-content' in str(line):
			bestanswer_content = line.get_text()
		if 'answer-content' in str(line) or 'best-content' in str(line):
			answer_content.append(line.get_text())
		if 'accuse="qThanks"' in str(line):
			comment = line.get_text()
		for line in soup.find_all('a'):
			if ' href="http://www.baidu.com/search/zhidao_help.html#如何选择头衔"' in str(line):
				arank = line.get_text()
	print ask_title + ask_content
	
	try:
	#关键词比较
		ask = ''
		ask = ask_title + ask_content
		ask_keyword = jieba.analyse.extract_tags(ask,5)
		list1 = []
		for w in ask_keyword:
			list1.append(str(w.encode('utf-8')))
		bestanswer_keyword = jieba.analyse.extract_tags(bestanswer_content,5)
		list2 = []
		for w in bestanswer_keyword:
			list2.append(str(w.encode('utf-8')))
	
	#关键词内容的输出
		qresult = ''
		for w in ask_keyword:
			qresult += str(w.encode('utf-8')) + '/'
		print u'问题中的关键词是：',qresult.decode('utf-8').encode('gbk')
		aresult = ''
		for w in bestanswer_keyword:
			aresult += str(w.encode('utf-8')) + '/'
		print u'答案中的关键词是：',aresult.decode('utf-8').encode('gbk')
		tmp = [val for val in list1 if val in list2]
	#判断两个关键字list是否存在交集
		if len(tmp) == 0:
			print u'问题可能无效' + '\n'
			score1 = 0
		else:
			print u'问题有效性有了最基本保证 获得了30积分' + '\n'
			score1 = 30
		
	#情感分析
		s1 = SnowNLP(str(ask.encode('utf-8')))
		asksentiments = s1.sentiments
		print u'问题的积极程度:',s1.sentiments
		s2 = SnowNLP(str(bestanswer_content.encode('utf-8')))
		bestsentiments = s2.sentiments
		print u'首要回答的积极程度:',s2.sentiments
		test = bestsentiments - asksentiments
		print u'问题与回答的差距是：',test
		if  test > 0.5 or test < -0.5:
			print u'问题可能无效'
		elif 0.5 > test > 0.4 or -0.5 < test < -0.4:
			print u'问题情感分析有了保证 获得了5积分' 
			fen = 5
		elif 0.4 > test > 0.3 or -0.4 < test < -0.3:
			print u'问题情感分析有了保证 获得了10积分'
			fen = 10
		elif 0.3 > test > 0.2 or -0.3 < test < -0.2:
			print u'问题情感分析有了保证 获得了15积分' 
			fen = 15
		elif 0.2 > test > 0.1 or -0.2 < test < -0.1:
			print u'问题情感分析有了保证 获得了20积分' 
			fen = 20
		else:
			fen = 30
			print u'问题情感分析有了保证 获得了30积分' 
		
	#对赞和批评数进行分析
		zan_num = int(zan)
		score_zan = 0
		if 10 > zan_num > 5:
			score_zan = 5
		elif 20 > zan_num > 10:
			score_zan = 10
		elif 30 > zan_num > 20:
			score_zan = 20
		elif zan_num > 30:
			score_zan = 30
		piping_num = int(piping)
		score_piping = 0
		if 10 > piping_num > 5:
			score_piping = -5
		elif 20 > piping_num > 10:
			score_piping = -10
		elif 30 > piping_num > 20:
			score_piping = -15
		elif piping_num > 30:
			score_piping = -20
		print u'赞得分：',score_zan,'\n',u'批评得分：',score_piping
	
		try:
		#对采纳率进行分析
			cainalv_num = int(cainalv[3:-1])
			cainalv_score = cainalv_num/2
			print u'采纳率得分：',cainalv_score
		except:
			print u'回答者没有在百度注册'
			pass
	
		try:
	#对等级进行分析
			rank = str(arank.encode('utf-8'))
			if rank[0] == '一' :
				rank_score = 3
			elif rank[0] == '二' :
				rank_score = 6
			elif rank[0] == '三' :
				rank_score = 9
			elif rank[0] == '四' :
				rank_score = 12
			elif rank[0] == '五' :
				rank_score = 15
			elif rank[0] == '六' :
				rank_score = 18
			else :
				rank_score = 20
		except:
			print u'回答者没有在百度注册'
			pass
		print u'rank得分：',rank_score
	
	#计算总得分
		fscore = score1 + fen + score_piping + score_zan + cainalv_score + rank_score
		print u'最终得分：',fscore
	except:
		print u'问题不存在'
	
if __name__ == '__main__':
    baidu_inputscore()