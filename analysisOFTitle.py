# -*- coding: utf-8 -*-

import json
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import jieba
from collections import Counter
import re
from wordcloud import WordCloud

df = pd.read_json('jianshu.json', typ='frame', encoding='utf-8')

datastr = ''

# ts = pd.Series(df['title'].values, index=df['_id'])

# print ts.value_counts()[:10]


for row in df.itertuples(index=True, name='Pandas'):
    datastr += getattr(row, 'title') + '\n'

datastr = datastr.strip()

pattern = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~\s]+'
reg = '[\u3002\uff1f\uff01\uff0c\u3001\uff1b\uff1a\u201c\u201d\u2018\u2019\uff08\uff09\u300a\u300b\u3008\u3009\u3010\u3011\u300e\u300f\u300c\u300d\ufe43\ufe44\u3014\u3015\u2026\u2014\uff5e\ufe4f\uffe5]+'
datastr = re.sub(reg, '', datastr)
datastr = re.sub(pattern, '', datastr)

cut_title = jieba.cut(datastr)
result = "/".join(cut_title)

wc = WordCloud(font_path='./msyh.ttf' ,background_color='black', width=800, height=600, max_font_size=50, max_words=1000, min_font_size=10,
               mode='RGBA', colormap='pink')

wc.generate(result)
wc.to_file(r"./4578.png")

# c = Counter(cut_title).most_common(20)

# print(result)
