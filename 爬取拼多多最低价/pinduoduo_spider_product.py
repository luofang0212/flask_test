#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from urllib import request,parse
import requests
from lxml import etree
import re
import json
from util.do_mysql import DoMySQL
from util import get_path
from util.do_logs import TestLog

log = TestLog().getlog()  # 放在class上面

mysql = DoMySQL()


def down_detail_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Referer": "http://mobile.yangkeduo.com/classification.html?refer_page_name=index&refer_page_id=10002_1630941428994_8mq566w4h7&refer_page_sn=10002&page_id=10031_1630941437974_10ijhiohup&is_back=1&bsch_is_search_mall=&bsch_show_active_page=&is_recover=1",
        "Cookie": "api_uid=CiYUMGE2AoGxrgBYRB+hAg==; _nano_fp=XpEqX0Uqn5mbXpTYXC_HHjOxWR9EkEeddux9_R4N; jrpl=QWq4DB70AVdYpllRkpfFC0cDMBgPi0GD; njrpl=QWq4DB70AVdYpllRkpfFC0cDMBgPi0GD; dilx=VDJ1FUr4r0B9cRFpUXGyO; ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_14_6)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F93.0.4577.63%20Safari%2F537.36; webp=1; PDDAccessToken=5G33ITKBW6H3QB7AKJ2YMLWIMEO3ADEU5KWSGASYWZNIQ7VWZ5ZA1113582; pdd_user_id=4483108149; pdd_user_uin=M45FLX5W4CB6VN6E4WWQEVTCD4_GEXDA; pdd_vds=garCYedffTdseCcBDNlBueudwDDuLeCcluDDBsldDLlNsuwuxLCufdsDfCLf; JSESSIONID=2999F89C0BAA8E8B099A77D6D8CECD6A"
    }

    sql = '''
            select min_pI,min_lkUl from spider_data.pingduoduo_categorys;
            '''
    res = mysql.query(sql)
    # print(res)
    url = "http://yangkeduo.com"
    for x in range(2,10):
        print(x)
        min_lkUl = res[x]['min_lkUl']
        min_pI = res[x]['min_pI']
        detail_url = url + min_lkUl
        print(detail_url)
        data = "1=1p_10018&p1_9975&p2_999999&p_g1&p_ype3&p_me=%E5%B7%A7%E5%85%8B%E5%8A%9B&_x_lk_2855022-7f17-41bc-851-bb1371e542&_x_gs_258387728697"
        res1 = parse.parse_qs(data)
        print(res1)

        # url = detail_url

        # response = requests.get(url, headers=headers)
        # # print(response.content.decode('utf-8'))
        #
        # filename = get_path.project_path + "/爬取拼多多最低价/detail_html/detail_{0}.html".format(min_pI)
        # with open(filename, 'w', encoding='utf-8') as fp:
        #     fp.write(response.content.decode('utf-8'))
        #     print("{0} 下载完成".format(filename))
        #     time.sleep(2)


def start():
    down_detail_url()



if __name__ == '__main__':
    start()
