#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request, parse
import requests
from lxml import etree
import re
import json
from util.do_mysql import DoMySQL
from util import get_path
from util.do_logs import TestLog

log = TestLog().getlog()  # 放在class上面

mysql = DoMySQL()


def down_catgoods_url():
    url = '''
    http://yangkeduo.com/classification.html?refer_page_name=login&refer_page_id=10169_1630929576461_t6bwzpzi3c&refer_page_sn=10169&page_id=10031_1630929599021_fgkaqgz2bd&is_back=1&bsch_is_search_mall=&bsch_show_active_page=
    '''

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }

    response = requests.get(url, headers=headers)
    # print(response.content.decode('utf-8'))

    filename = get_path.project_path + "/爬取拼多多最低价/html_list/" + "goods_category.html"
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(response.content.decode('utf-8'))
        print("{0} 下载完成".format(filename))


def parser_category_page():
    filename = get_path.project_path + "/爬取拼多多最低价/html_list/" + "goods_category.html"
    parser = etree.HTMLParser(encoding='utf-8')
    html_element = etree.parse(filename, parser=parser)

    # 获取商品分类json数据
    min_categorys_json = html_element.xpath("//script[contains(text(),'window.rawData')]")[0]
    categorys_text = min_categorys_json.xpath("./text()")[0]
    categorys_json_text = re.sub(r"[window.rawData=;]+", "", categorys_text).strip()
    # print(categorys_json_text)
    # 将字符串加载成python对象
    data = parse.parse_qs(categorys_json_text)

    # 该json内容不合法，已修改
    with open("1.txt", 'w', encoding='utf-8') as fp:
        fp.write(categorys_json_text)


def lode_json_catgoods():
    filename = get_path.project_path + "/爬取拼多多最低价/json/category_info.json"
    with open(filename, 'r', encoding='utf-8') as fp:
        categorys_json = json.load(fp)
        # print(categorys_json)

    iems = categorys_json['se']['cata']['Iems'][1:-3]
    iems_data = []
    for iem in iems:
        big_pI = iem['pI']
        big_pNme = iem['pNme']
        ls_list = iem['ls']
        for ls in ls_list:
            two_pI = ls['pI']
            two_pNme = ls['pNme']
            two_ls = ls['ls']
            for min_ls in two_ls:
                iems_dict = {}
                min_pI = min_ls['pI']
                min_pNme = min_ls['pNme']
                min_lkUl = min_ls['lkUl']
                iems_dict = {
                    "big_pI": big_pI,
                    "big_pNme": big_pNme,
                    "two_pI": two_pI,
                    "two_pNme": two_pNme,
                    "min_pI": min_pI,
                    "min_pNme": min_pNme,
                    "min_lkUl": min_lkUl
                }

                #                 sql = '''
                #                 INSERT INTO spider_data.pingduoduo_categorys (big_pI, big_pNme, two_pI, two_pNme, min_pI, min_pNme, min_lkUl)
                # VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
                #                 '''.format(big_pI, big_pNme, two_pI, two_pNme, min_pI, min_pNme, min_lkUl)
                #
                #                 mysql.update(sql)
                #                 print("{0}插入成功 ".format(min_pI))
                #                 log.info("{0}插入成功,详细数据：{1}".format(min_pI,iems_dict))
                headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                }

                url = "http://yangkeduo.com" + min_lkUl
                respone = requests.get(url, headers=headers)
                print(respone.content.decode('utf-8'))

                filename = get_path.project_path + "/爬取拼多多最低价/detail_html/{0}.html".format(min_pI)
                with open(filename,'w',encoding='utf-8') as fp:
                    fp.write(respone.content.decode('utf-8'))
                    print("{0},{1} 下载成功".format(min_pI,min_lkUl))


def start():
    # down_catgoods_url()
    # parser_category_page()
    lode_json_catgoods()


if __name__ == '__main__':
    start()
