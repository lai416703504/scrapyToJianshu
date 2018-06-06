# -*- coding: utf-8 -*-
import jieba
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
from wordcloud import WordCloud
import datetime
import re

df = pd.read_json('../jianshu.json')

text = ''

for content_text in df.content_text:
    text += content_text

text = re.sub(u'[\x00-\xff\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\uff01\s]', '', text)
cut_text = jieba.cut(text)

result = "/".join(cut_text)

cutList = result.split('/')

s = Series(cutList)

wc = WordCloud(font_path='./msyh.ttf', background_color='white', width=800, height=600, max_font_size=100,
               max_words=1000, min_font_size=10,
               mode='RGBA', colormap='pink')

wc.generate(result)
wc.to_file(r"./" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".png")
