# -*- coding:utf-8 -*-

import jieba
import jieba.analyse

def comparekw():
	begin_id = 400155662
	for i in range(100):
		id = begin_id + i
		try:
			f = open('./text/%d.html/ask.txt' % id , 'r')
			qstr = f.read().decode('utf-8')
			qkw = jieba.analyse.extract_tags(qstr,5)
			#问题的关键词提取
			list1 = []
			for w in qkw:
				list1.append(str(w.encode('utf-8')))
			print u'获得%d.html 号问题的关键词列表' % id
			f.close
		except:
			print u'%d.html 号问题不符合规格' % id
			continue
		try:
			f = open('./text/%d.html/bestanswer.txt' % id , 'r')
			astr = f.read().decode('utf-8')
			akw = jieba.analyse.extract_tags(astr,5)
			#答案关键词提取
			list2 = []
			for w in akw:
				list2.append(str(w.encode('utf-8')))
			print u'获得 %d.html 号问题首要回答的关键字列表' % id
			f.close
		except:
			print u'该问题首要回答不存在' + '\n'
			continue
		tmp = [val for val in list1 if val in list2]
		#判断两个关键字list是否存在交集
		if len(tmp) == 0:
			print u'问题可能无效' + '\n'
		else:
			print u'问题有效性有了最基本保证 获得了30积分' + '\n'
			try:
				f = open('./text/%d.html/keyscore.txt' % id , 'r')
				score = int(f.read())
				score = score + 30
				result = str(score)
				f = open('./text/%d.html/keyscore.txt' % id , 'w')
				f.write(result)
				f.close
			except:
				with open('./text/%d.html/keyscore.txt' % id , 'w') as file_saved:
					text = str(30)
					file_saved.write(text)
		
			

if __name__ == '__main__':
	comparekw()