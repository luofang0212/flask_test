#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request,parse
import requests
from lxml import etree

url = "http://yangkeduo.com/search_catgoods.html"
data  = '''
opt_id=9513&opt1_id=9490&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%A5%B3%E8%A3%85%E9%A3%8E%E8%A1%A3&_x_link_id=a94b5f49-3cf6-4f2f-b308-02209dba634c&_x_goods_id=257531072497&refer_page_name=search&refer_page_id=10031_1630929599021_fgkaqgz2bd&refer_page_sn=10031
'''
data2  = '''
opt_id=9498&opt1_id=9490&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%A5%B3%E8%A3%85T%E6%81%A4&_x_link_id=a94b5f49-3cf6-4f2f-b308-02209dba634c&_x_goods_id=247630431573&refer_page_name=search&refer_page_id=10031_1630929599021_fgkaqgz2bd&refer_page_sn=10031
'''

data3='''
opt_id=10161&opt1_id=9975&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E7%BE%8E%E7%99%BD%E5%85%BB%E9%A2%9C&_x_link_id=b6b236d6-ba0d-49b9-97cb-b33686f83ba2&_x_goods_id=232181801285&refer_page_name=search&refer_page_id=10031_1630929599021_fgkaqgz2bd&refer_page_sn=10031
'''

res = parse.parse_qsl(data)
res2 = parse.parse_qsl(data2)
res3 = parse.parse_qsl(data3)
print(res)
print(res2)
print(res3)