# -*- encoding: utf-8 -*-

import os
import re
from bs4 import BeautifulSoup


def get_info():
    dir_list = os.listdir('./pages')
    for item in dir_list:
        print u'处理 %s' % item
        file_path = os.path.join('./pages', item)
        with open(file_path, 'r') as _file:
			text = _file.read()
			unicode_text = text.decode('gbk')
			soup = BeautifulSoup(unicode_text)
			ask_title, ask_content = '', ''
			answer_content = []
			bestanswer_content = []
			comment = []
			cainalv = []
			rank = []
			zan = []
			piping = []
			for line in soup.find_all('span'):
				if 'ask-title' in str(line):
					ask_title = line.get_text()
				if 'class="ml-10"' in str(line):
					cainalv = line.get_text()
				if 'class="evaluate evaluate-32"' in str(line):
					s = str(line)
					#以空格分块
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
						rank = line.get_text()
			output_path = './text/%s' % item
			if not os.path.exists(output_path):
				os.makedirs(output_path)
			with open(os.path.join(output_path, 'ask.txt'), 'w') as _f_out:
				_f_out.write(ask_title.encode('utf-8') + '\n')
				_f_out.write(ask_content.encode('utf-8'))
			with open(os.path.join(output_path, 'anwsers.txt'), 'w') as _f_out:
				for item in answer_content:
					_f_out.write(item.encode('utf-8'))
					_f_out.write('\n\n\n')
			try:	
				with open(os.path.join(output_path, 'bestanswer.txt') , 'w') as file_saved:
					file_saved.write(bestanswer_content.encode('utf-8'))
			except:
				print u'此问题没有最佳回答'
			try:	
				with open(os.path.join(output_path, 'caina.txt') , 'w') as file_saved:
					file_saved.write(cainalv.encode('utf-8'))
			except:
				print u'此问题作者不存在'
			try:
				with open(os.path.join(output_path, 'comment.txt') , 'w') as file_saved:
					file_saved.write(comment.encode('utf-8'))
			except:
				print u'此问题没有评论'
			try:
				with open(os.path.join(output_path, 'rank.txt') , 'w') as file_saved:
					file_saved.write(rank.encode('utf-8'))
			except:
				print u'此问题没有rank'
			try:
				with open(os.path.join(output_path, 'zan.txt') , 'w') as file_saved:
					file_saved.write(zan.encode('utf-8'))
			except:
				print u'此问题没有赞'
			try:
				with open(os.path.join(output_path, 'piping.txt') , 'w') as file_saved:
					file_saved.write(piping.encode('utf-8'))
			except:
				print u'此问题没有批评' + '\n'
			


if __name__ == '__main__':
    get_info()
