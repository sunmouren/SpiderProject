# SpiderProject
> 爬取网易云音乐某首歌曲的全部评论，以及生成相对应的词云图
测试环境：pycharm、win10、python3.5.4。

### 需要用的模块
##### 爬取评论
- base64
- json
- requests
- Crypto 注意这个是大写C开头的（如果安装了小写的，请先卸载再安装大写的），并且不是python3.6，因为Crypto好久没有维护了。如果是windows平台的话，建议不要从pycharm IDE中安装，要从windows cmd 中用pip3 install Crypto。

#### 生成词云图
- jieba
- wordcloud

### 注意事项
- 如果要爬取别的歌曲，要注意是否符合headers里的内容
- 不要连续爬取多次，以防封Ip，会一段时间不能使用。
