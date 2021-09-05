#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 将使用到的路径 ，维护到该模块

import os
import re
import time

# 获取到顶级路径

file_path = os.path.realpath(__file__)  # 获取该文件绝对路径

#获取该项目的顶级目录
project_path =os.path.split(os.path.split(file_path)[0])[0]
# print(project_path)


# 日志文件路径

# 日志文件名生成
timestamp = time.strftime("%Y-%m-%d", time.localtime())
logfilename =  '%s.log' % timestamp
# 日志文件路径
log_file_path = os.path.join(project_path, 'static', 'logs', logfilename)
print(log_file_path)