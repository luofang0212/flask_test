#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''爬取51job，python职位'''
import json

import requests
from util import get_path
import time
from urllib import request
from lxml import etree
import html5lib
import re
from util.do_mysql import DoMySQL
from util.do_logs import TestLog
import threading
from queue import Queue
from bs4 import  BeautifulSoup
import warnings

warnings.simplefilter("ignore")
file_path = get_path.project_path
log = TestLog().getlog()  # 放在class上面

class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "macOS"
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        print(url)

        parser = etree.HTMLParser(encoding='gbk')
        html_element = etree.parse(url, parser=parser)
        # 获取标签里的文本信息
        position_list_json = html_element.xpath("//script[contains(text(),'window.__SEARCH_RESULT__')]")[0]
        position_text = position_list_json.xpath("./text()")[0]
        # 获取职位信息json串，职位列表存在engine_jds标签里
        position_text = re.sub(r"window.__SEARCH_RESULT__ =", "", position_text).strip()

        # 将获取的json字符串，转换成python对象
        position_json = json.loads(position_text)
        engine_jds = position_json['engine_jds']

        for engine_jd in engine_jds:
            jobid = engine_jd['jobid']
            job_href = engine_jd['job_href']
            job_name = engine_jd['job_name']
            company_name = engine_jd['company_name']
            self.page_queue.put(job_href)
            # jobid, job_href =  self.page_queue.get()
            # print(jobid,job_href)


class Consumer(threading.Thread):

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        print("我是消费者")
        while True:
            if self.page_queue.empty() and self.page_queue.empty():
                break
            jobid,job_href = self.img_queue.get()
            print("我是消费者: ",jobid,job_href)

def start():
    page_queue = Queue(100)
    img_queue = Queue(100)

    for x in range(1,5):
        file_name = get_path.project_path + r'/爬取51job职位信息/html/'
        url = file_name + 'position_{0}'.format(x) + '.html'
        page_queue.put(url)

    for x in range(5):
        t1 = Producer(page_queue,img_queue,name='生产者{0}'.format(x))
        t1.start()

    for x in range(5):
        t1 = Consumer(page_queue,img_queue,name='消费者{0}'.format(x))
        t1.start()


if __name__ == '__main__':
    start()








