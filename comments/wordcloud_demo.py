# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/5/13 13:54
@desc: 通过爬取的网页云音乐全部评论生成词云图
"""

import jieba
from wordcloud import WordCloud

if __name__ == '__main__':
    # 读取文本
    text = open("test.txt", "r", encoding='utf-8').read()
    # 分词
    cut_text = jieba.cut(text)
    result = "/".join(cut_text)
    # 生成词云图, xingkai.ttf是中文字体，用到它是因为WordCloud本身好像没有支持中文的。
    wordcloud = WordCloud(font_path=r"E:\PycharmWorkPlace\wordcloud_demo\xingkai.ttf", background_color='white',
                          width=800,
                          height=600, max_font_size=50,
                          max_words=1000, mode='RGBA',colormap='pink')
    wordcloud.generate(result)
    wordcloud.to_file("test.png")









