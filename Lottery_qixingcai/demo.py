# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/6/20 13:22
@desc: 从官网获取七星彩数据
"""

import urllib.request
import numpy

from bs4 import BeautifulSoup


class Lottery():
    def __init__(self, issue):
        self.url = "http://www.lottery.gov.cn/historykj/history.jspx?page=false&_ltype=qxc&termNum=" + str(issue) + "&startTerm=&endTerm="
        self.filename = str(issue) + ".txt"
        tds = self.get_numbers_for_internet()
        self.save_number(tds=tds)

    def get_numbers_for_internet(self):
        """
        从网络上获取七星彩开奖结果
        :param url: 要请求的url
        :return: 开奖结果html的标签td
        """
        # 获取url的html数据
        html = urllib.request.urlopen(self.url).read()
        # 指定编码格式
        html = html.decode('UTF-8')
        # 利用BeautifulSoup分析html
        soup = BeautifulSoup(html, 'html.parser')
        # 找到全部td标签
        tds = soup.find_all('td')
        return tds

    def save_number(self, tds):
        """
        保存开奖结果到文件
        :param tds: 开奖结果的html标签
        :param filename: 要写入的文件名
        """
        for td in tds:
            if len(td.text) == 7 and ',' not in td.text:
                num = td.text
                with open(self.filename, 'a') as file_obj:
                    file_obj.write(num + "\n")

    def get_str_numbers_lists(self):
        """
        从文件中读取开奖结果
        :param filename: 要读取的文件名
        :return: 字符型的倒序开奖结果列表（副本）
        """
        try:
            with open(self.filename) as file_object:
                nums_str_lists = file_object.read()
        except FileNotFoundError:
            # 如果文件名不存在
            error_msg = "Sorry, the file " + self.filename + " does not exist."
            print(error_msg)
        else:
            # 切片
            nums_str_lists = nums_str_lists.split()
            # 倒序副本
            return nums_str_lists[::-1]

    def get_int_numbers_lists(self):
        """
        将字符型的开奖结果转为整型，以便以后分析
        :param nums_str_lists: 字符型开奖结果列表
        :return: 整型开奖结果
        """
        nums_str_lists = self.get_str_numbers_lists()
        temp_lists = []
        for nums_str_list in nums_str_lists:
            temp_lists.append(list(nums_str_list))
        for temp_list in temp_lists:
            for index, item in enumerate(temp_list):
                temp_list[index] = int(item)
        return temp_lists


if __name__ == '__main__':
    lottery_1690 = Lottery(issue=1690)
    num_int_lists = lottery_1690.get_int_numbers_lists()
    data = numpy.array(num_int_lists)
    print(data)