from flask import Flask
from flask import render_template
from flask import request
import jieba  # 分词
from matplotlib import pyplot as plt  #绘图，数据可视化
from PIL import Image  #图片处理
import numpy as np  #矩阵运算
import pymysql  # mysql 数据库驱动
from wordcloud import WordCloud  #词云

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.debug=True
    app.run()
