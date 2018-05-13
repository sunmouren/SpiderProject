# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/5/12 22:42
@desc: 爬去网易云音乐全部评论
"""

import base64
import json
import codecs

import requests
from Crypto.Cipher import AES

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    'Cookie': "_ntes_nuid=bae6bddbcaae44ff2fb705f942b04429; usertrack=ezq0plqLoYlIU74bMVu/Ag==; _ntes_nnid=06b1f38610caa21ede9d767ad2370183,1519100299969; _ga=GA1.2.1528031140.1519100301; __f_=1521282707045; P_INFO=m15595757119_1@163.com|1524116518|0|mail163|00&99|CN&1524116454&mailsettings#zhj&330300#10#0#0|155119&1|mailsettings|15595757119@163.com; nts_mail_user=15595757119@163.com:-1:1; _iuqxldmzr_=32; WM_TID=bi2ul0cBG7fnlIOPLQRMlothc2PY0i5k; __e_=1525966530859; JSESSIONID-WYYY=yCXaNbRPwzwYr0mj7kc%2F31mUGrgjXDUhwcJUpWtfXRC3J33m0lJtADdIqI2H5g3fkFTtptyQtzJgxN1axfJxUZ0uv7fPUrT1kvaGuG0c2uI2Ge05oAfi6PpdT5281uNH4KmF3uS7Mqm3up8S5cEN47vDwnOQCMPt4WmGAl%2BmNeKiv%5C9p%3A1526119472806; __utma=94650624.1528031140.1519100301.1525754678.1526117673.2; __utmc=94650624; __utmz=94650624.1526117673.2.2.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utmb=94650624.5.10.1526117673",
    'Referer': "http://music.163.com/"
}

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"


def get_params(page):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1):
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page - 1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    if type(text) is bytes:
        text = text + (pad * chr(pad)).encode('utf-8')
    else:
        text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def get_json(url, params, encSecKey):
    data = {
        'params': params,
        'encSecKey': encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


def get_pages(url):
    params = get_params(1)
    encSeckey = get_encSecKey()
    json_text = get_json(url, params, encSeckey).decode()
    json_dict = json.loads(json_text)
    print(json_text)
    comments_num = int(json_dict['total'])
    if (comments_num % 20 == 0):
        pages = comments_num / 20
    else:
        pages = int(comments_num / 20) + 1
    print("一共有%d页评论, %条评论" % (pages, comments_num))
    return pages


def get_comments(url, pages):
    comments = list()
    for page in range(pages):
        params = get_params(page + 1)
        encSeckey = get_encSecKey()
        json_text = get_json(url, params, encSeckey).decode()
        json_dict = json.loads(json_text)
        for item in json_dict['comments']:
            content = item['content']
            comments.append(content)
        print("第%d页抓取完毕" % (page + 1))
    return comments


def save_to_file(comments, filename):
    with codecs.open(filename, 'a', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment)
    print("写入成功!")


if __name__ == '__main__':
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_31877636?csrf_token='
    pages = get_pages(url)
    comments = get_comments(url=url, pages=pages)
    save_to_file(comments=comments, filename="test.txt")

