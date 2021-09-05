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

file_path = get_path.project_path
log = TestLog().getlog()  # 放在class上面

class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "macOS"
    }
    def __init__(self,page_queue,save_queue,*args,**kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue=page_queue
        self.save_queue=save_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.down_detail_url(url)


    # 2:解析已爬取的职位列表，获取到detail_url，下载到本地
    def down_detail_url(self,url):

        # 解析职位列表html
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
            positions = {}
            jobid = engine_jd['jobid']
            # print(jobid)
            job_href = engine_jd['job_href']
            job_name = engine_jd['job_name']
            company_name = engine_jd['company_name']
            positions = {
                "jobid": jobid,
                "job_name": job_name,
                "company_name": company_name,
                "job_href": job_href
            }
            self.save_queue.put((jobid, job_name,company_name,job_href))

class Consumer(threading.Thread):

    def __init__(self, page_queue, save_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.save_queue = save_queue


    def run(self):
        while True:
            if self.page_queue.empty() and self.page_queue.empty():
                break
            jobid, job_name,company_name,job_href = self.save_queue.get()
            self.get_detail_url()

    # 获取到detail_url
    def get_detail_url(self):

        jobid, job_name, company_name, job_href = self.save_queue.get()

        log.info("获取职位详情job_id: {1},\n 详情url: {2}".format(jobid,job_href))
        response = requests.get(job_href, headers=self.headers)
        detail_text = response.content
        html_element = etree.HTML(detail_text)
        html_text = etree.tostring(html_element, encoding='utf-8').decode('utf-8')
        # print(html_text)
        no_detail = html_element.xpath("//div[@class='research']")
        if len(no_detail) == 1:
            print("{0}无职位可爬取".format(job_href))
            log.info("{0}无职位可爬取".format(job_href))
        else:
            if "https://51rz.51job.com/job.html" in job_href:
                pass
            else:
                # 获取职位信息
                detal_info = html_element.xpath("//div[@class='tCompany_center clearfix']")
                # print(detal_info)
                for detal in detal_info:
                    log.info("{0} 开始爬取".format(job_href))
                    print("{0} 开始爬取".format(job_href))
                    positions_infos = {}
                    job_href = job_href
                    job_id = detal.xpath(".//div[@class='cn']/h1/input/@value")[0]
                    titile = detal.xpath(".//div[@class='cn']/h1/@title")[0]
                    company_name = detal.xpath(".//p[@class='cname']/a/@title")[0]
                    money = detal.xpath(".//div[@class='cn']//strong/text()")
                    print(money)

                    if len(money) == 0:
                        money = "无价格"
                    else:
                        money = detal.xpath(".//div[@class='cn']//strong/text()")[0]

                    infos = detal.xpath(".//p[@class='msg ltype']/@title")[0]

                    log.info("爬取的infos信息：{0}".format(infos))

                    infos = re.sub(r"\s+", "", infos)
                    infos = re.split(r"[|]", infos)
                    city = infos[0]

                    experience = infos[1]
                    certificate = infos[2]

                    if len(infos) == 3:
                        numbers = '未获取到人数'
                        release_date = '未获取到发布日期'
                    if len(infos) == 4:
                        numbers = infos[3]
                        release_date = '未获取到发布日期'
                    elif len(infos) == 5:
                        numbers = infos[3]
                        release_date = infos[4]
                    else:
                        numbers = '未获取到人数'
                        release_date = '未获取到发布日期'

                    # print(release_date)
                    tags = detal.xpath(".//div[@class='jtag']//span/text()")
                    tag_text = ""
                    for tag in tags:
                        tag_text = tag_text + tag + ','
                    tags = tag_text

                    job_info = detal.xpath(".//div[@class='bmsg job_msg inbox']//p/text()")
                    job_text = ''
                    for info in job_info:
                        job_text = job_text + info + '**'

                    job_info = job_text
                    # print(job_info)
                    positions_infos = {
                        "job_id": job_id,
                        "titile": titile,
                        "company_name": company_name,
                        "money": money,
                        "city": city,
                        "experience": experience,
                        "certificate": certificate,
                        "numbers": numbers,
                        "release_date": release_date,
                        "tags": tags,
                        "job_info": job_info,
                        "job_href": job_href
                    }
                    sql = sql = '''INSERT INTO spider_data.`51_job_info` (job_id, titile, company_name, city, experience, certificate, numbers,release_date, tags, job_info, detail_url,money)
                        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}','{11}');'''.format(job_id, titile, company_name, city, experience, certificate, numbers, release_date, tags,job_info, job_href, money)
                    DoMySQL().update(sql)
                    log.info("{0} 插入【51_job_info】表成功".format(job_id))
                    print("{0} 插入成功".format(job_id))

def start():
    page_queue = Queue(100)
    save_queue = Queue(100)

    for x in range(1,3):
        url = file_name = file_path + r"/爬取51job职位信息/html/" + "position_{0}.html".format(x)
        page_queue.put(url)

    for x in range(5):
        t1 = Producer(page_queue,save_queue,name='生产者{0}'.format(x))
        t1.start()

    for x in range(5):
        t1 = Consumer(page_queue,save_queue,name='消费者{0}'.format(x))
        t1.start()

if __name__ == '__main__':
    start()
