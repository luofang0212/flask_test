#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import threading
from queue import Queue
from lxml import etree
import re
import random
import os
from urllib import request
import warnings
warnings.simplefilter("ignore")

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 下载表情包到本地
def down_page_url():
    for x in range(1,101):
        url = 'https://www.doutula.com/photo/list/?page={0}'.format(x)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }

        response = requests.get(url, headers=headers, verify=False)
        # print(response.text)

        with open('html/doutula_{0}.html'.format(x), 'wb') as fp:
            fp.write(response.content)
            print("{0} 成功下载到本地！！！".format(url))

class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
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
        # print(html_file_name)
        # 读取72个html文件，进行解析
        parser = etree.HTMLParser(encoding='utf-8')
        html = etree.parse(url + '.html', parser=parser)

        # 获取所有img
        imgs = html.xpath("//li[@class='list-group-item']//img[@referrerpolicy='no-referrer']")

        for img in imgs:
            img_url = img.xpath('.//@data-backup')[0]
            img_name = img.xpath('.//@alt')[0]
            img_name = re.sub('[*\?？\.。！@@!/、\s]+', '', img_name)
            if img_name == '':
                img_name = str(random.randint(100000, 20000000)) + str(random.randint(10, 200000))
            suffix = os.path.split(img_url)[1]
            name, ext = os.path.splitext(suffix)
            file_name = img_name + ext
            self.img_queue.put((img_url,file_name))

class Consumer(threading.Thread):

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()
            # print(img_url,filename)
            request.urlretrieve(img_url,'images/'+filename)
            print('下载成功： {0}'.format(filename))


def start():
    page_queue = Queue(100)
    img_queue = Queue(100)

    for x in range(1,72):
        url = 'html/doutula_{0}'.format(x)
        page_queue.put(url)

    for x in range(5):
        t1 = Producer(page_queue,img_queue,name='生产者{0}'.format(x))
        t1.start()

    for x in range(5):
        t1 = Consumer(page_queue,img_queue,name='消费者{0}'.format(x))
        t1.start()


if __name__ == '__main__':
    start()





















