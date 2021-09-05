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

log = TestLog().getlog()  # 放在class上面
file_path = get_path.project_path


# 1: 先请求网页,将爬取到的网页存到本地
def down_pag_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "macOS"
    }
    for x in range(100, 101):
        url = '''
        https://search.51job.com/list/010000%252c020000%252c030200%252c040000%252c180200,000000,0000,00,9,99,python,2,{0}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
        '''.format(x)

        response = requests.get(url, headers=headers)
        # print(response.text)
        file_name = file_path + r"/爬取51job职位信息/html/" + "position_{0}.html".format(x)
        with open(file_name, 'w', encoding='gbk') as fp:
            fp.write(response.content.decode('gbk'))
            print("{0} 下载成功".format(file_name))
            time.sleep(2)


# 2:解析已爬取的职位列表，获取到detail_url，下载到本地
def down_detail_url():
    positions_list = []
    for x in range(36, 101):
        # 解析职位列表html
        parser = etree.HTMLParser(encoding='gbk')
        file_name = file_path + r"/爬取51job职位信息/html/" + "position_{0}.html".format(x)
        html_element = etree.parse(file_name, parser=parser)
        top_url = "position_{0}.html".format(x)
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
                "top_url":top_url,
                "jobid": jobid,
                "job_name": job_name,
                "company_name": company_name,
                "job_href": job_href
            }
            positions_list.append(positions)
    # print(positions_list)
    # print(len(positions_list))
    return positions_list


# 获取到detail_url
def get_detail_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "macOS"
    }

    positions_list = down_detail_url()
    positions_infos_list = []
    try:
        for positions in positions_list:

            log.info("获取{0}中的职位列表".format(positions))
            detail_url = positions['job_href']
            detail_id = positions['jobid']
            top_url = positions['top_url']
            log.info("获取所在url:{0} \n 职位详情url: {1},\n job_id: {2}".format(top_url,detail_url, detail_id))
            response = requests.get(detail_url, headers=headers)
            detail_text = response.content
            html_element = etree.HTML(detail_text)
            html_text = etree.tostring(html_element, encoding='utf-8').decode('utf-8')
            # print(html_text)
            no_detail = html_element.xpath("//div[@class='research']")
            if len(no_detail) == 1:
                print("{0}无职位可爬取".format(detail_url))
                log.info("{0}无职位可爬取".format(detail_url))
            else:
                if "https://51rz.51job.com/job.html" in detail_url or "https://jobs.51job.com/guangzhou-thq/131931628.html?s=sou_sou_soulb&t=0_0" in detail_url:
                    pass
                else:
                    # 获取职位信息
                    detal_info = html_element.xpath("//div[@class='tCompany_center clearfix']")
                    # print(detal_info)
                    for detal in detal_info:
                        log.info("{0} 开始爬取".format(detail_url))
                        print("{0} 开始爬取".format(detail_url))
                        positions_infos = {}
                        detail_url = detail_url
                        job_id = detal.xpath(".//div[@class='cn']/h1/input/@value")[0]
                        titile = detal.xpath(".//div[@class='cn']/h1/@title")[0]
                        company_name = detal.xpath(".//p[@class='cname']/a/@title")[0]
                        money = detal.xpath(".//div[@class='cn']//strong/text()")
                        # print(money)

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

                        job_info = re.sub(r"[,']","，",job_text)


                        log.info("job_info信息{0}".format(job_info))
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
                            "detail_url": detail_url,
                            "top_url" : top_url
                        }

                        sql = '''INSERT INTO spider_data.`51_job_info` (job_id, titile, company_name, city, experience, certificate, numbers,release_date, tags, job_info, detail_url,money,top_url)
                                   VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}','{11}','{12}');'''.format(
                            job_id, titile, company_name, city, experience, certificate, numbers, release_date, tags,
                            job_info, detail_url, money,top_url)

                        DoMySQL().update(sql)
                        log.info("{0} 插入【51_job_info】表成功".format(job_id))
                        print("{0} 插入成功".format(job_id))

                        log.info("{0} 爬取完成".format(detail_url))
    except Exception as e:
        print("出错啦！！: {0}".format(e))
        log.error("出错啦！！: {0}".format(e))


def start():
    # down_pag_url()
    # down_detail_url()
    get_detail_url()



if __name__ == '__main__':
    start()
