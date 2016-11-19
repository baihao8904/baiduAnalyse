# -*- coding:utf-8 -*-
__author__ = 'lenovo'

import time
from NewMain import sougou_info

while True:
    print('已抓问题')
    print(sougou_info.find().count())
    time.sleep(5)