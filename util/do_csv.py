#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def read_csv():
    with open('issues.csv','r') as fp:
        reader = csv.DictReader(fp)
        for x in reader:
            # print(x['#'])
            # print(x['项目'])
            # print(x['跟踪'])
            read_dict={
                "编号":x['#'],
                "项目":x['项目'],
                "跟踪":x['跟踪']
            }
            print(read_dict)


def write_csv():
    headers = ['name', 'age', 'classroom']

    values = [
        {"name":"zhangsan","age":18,"classroom":'101'},
        {"name": "zhangsan", "age": 14, "classroom": '102'},
        {"name": "zhangsan", "age": 15, "classroom": '103'},
    ]

    with open('test_2.csv','w',newline='',encoding='utf-8') as fp:
        writer = csv.DictWriter(fp,headers)
        writer.writeheader()
        writer.writerow({"name":"zhangsan","age":18,"classroom":'101'})
        writer.writerows(values)
        headers = ['name', 'age', 'classroom']

    values = [
        {"name":"zhangsan","age":18,"classroom":'101'},
        {"name": "zhangsan", "age": 14, "classroom": '102'},
        {"name": "zhangsan", "age": 15, "classroom": '103'},
    ]

    with open('test_2.csv','w',newline='',encoding='utf-8') as fp:
        writer = csv.DictWriter(fp,headers)
        writer.writeheader()
        writer.writerow({"name":"zhangsan","age":18,"classroom":'101'})
        writer.writerows(values)

if __name__ == '__main__':
    pass