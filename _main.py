# -*- encoding: utf-8 -*-

import requests
import os


def get_page(lower_bound=1, upper_bound=2000):
    if not os.path.exists('./pages/'):
        os.mkdir('./pages')
    base_url = 'http://zhidao.baidu.com/question/'
    for question_num in range(lower_bound, upper_bound):
        url = base_url + '%d.html' % question_num
        r = requests.get(url)
        try:
            _text = r.content.decode('gbk')
        except:
            print 'Decode Error'
            continue
        if r.status_code == 404 or u'该问题可能已经失效' in _text:
            print 'Question No. %d not found' % question_num
        elif r.status_code == 200:
            with open('./pages/%d.html' % question_num, 'w') as file_saved:
                _text_encode = _text.encode('gbk')
                file_saved.write(_text_encode)
            print 'Save Question No. %d as ./pages/%d.html' \
                  % (question_num, question_num)
        else:
            print 'Request Error, code %d' % r.status_code

if __name__ == '__main__':
    get_page(400201271, 400202000)  #400200000
