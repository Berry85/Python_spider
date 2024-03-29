# # -*- coding:UTF-8 -*-
import lxml
from bs4 import BeautifulSoup
import requests
import os
import sys


# 这个爬虫尚未完全完成，目前仅支持笔趣看网站爬文章，
# 在下载时注意，当目录名中存在英文冒号时候，将出现文件无法创建，该章节无法下载但不会报错


# ‘User_Anger’: 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'

class downloader(object):

    # 初始化
    def __init__(self):
        # 网站根路径
        self.server = 'http://www.biqukan.com/'
        # 小说路径
        self.target = 'https://www.biqukan.com/64_64315/'
        # 存放地址根路径
        self.save_path = 'F://爬虫'
        # 存放章节名
        self.names = []
        # 存放章节连接
        self.urls = []
        # 章节数量
        self.nums = 0
        # 文章名
        self.article_name = ""
        # 文件名，数组模式，存放的是章节，每一章节单独是一个txt文档
        self.file = []
        # # 文件名，字符串模式，存放文件路径，一个txt包含每一章节
        # self.file = ""
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        }

    # 获取文章名
    def get_name(self):
        req = requests.get(url=self.target, headers=self.head)
        req.encoding = 'GBK'
        # 解析
        soup = BeautifulSoup(req.text, "lxml")
        # 获取文章名字
        article = soup.find_all('h2')
        self.article_name = article[0].text.strip('/u003A')

    # 获取连接
    def get_urls(self):
        req = requests.get(url=self.target, headers=self.head)
        req.encoding = 'GBK'
        # 解析
        soup = BeautifulSoup(req.text, "lxml")
        # 获取文章的章节
        lists = soup.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(lists[0]), "lxml")
        a = a_bf.find_all('a')
        # 将前面章节忽略，也就是前面最新章节
        self.nums = len(a[12:])
        for each in a[12:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    # 获取章节内容，list_url是获取的url
    def get_text(self, list_url):
        req = requests.get(url=list_url, headers=self.head)
        req.encoding = 'GBK'
        # 解析
        soup = BeautifulSoup(req.text, "lxml")
        # 获取文章
        txt = soup.find_all('div', class_='showtxt')
        # 忽略空格转成换行
        texts = txt[0].text.replace('\u3000', '\n')
        return texts

    # 将获取的文件内容写入文件
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a+', encoding='UTF-8')as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')
            f.close()

    # 创建文件夹
    def create_path(self):
        dir_path = self.save_path + '/' + self.article_name
        if not os.path.exists(dir_path):
            os.path.join(self.save_path, self.article_name)
            os.mkdir(dir_path)
        self.save_path = dir_path


if __name__ == '__main__':
    # 实例化
    dl = downloader()
    dl.get_urls()
    dl.get_name()
    dl.create_path()
    print('开始下载小说《' + dl.article_name + '》：')
    # # 字符串模式，一个txt正片文章
    # dl.file = dl.save_path + '/' + dl.article_name + '.txt'
    for i in range(dl.nums):
        # 数组模式，单独章节单独txt
        dl.file.append(dl.save_path + '/' + dl.names[i] + '.txt')
        dl.writer(dl.names[i], dl.file[i], dl.get_text(dl.urls[i]))

        # # 字符串模式，一个txt正片文章
        # dl.writer(dl.names[i], dl.file, dl.get_text(dl.urls[i]))
        sys.stdout.flush()
    print('下载完成')
