#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
#from pprint import pprint
#from bs4 import BeautifulSoup
#import json
#import csv
#from urllib import parse
#from socket import timeout as socket_timeout
#from urllib import error
#import time
#import random
import re
#from urllib.request import urlopen#
#from pprint import pprint
from bs4 import BeautifulSoup
import requests
from pathlib import Path



def getHtmlCode(url):  # 该方法传入url，返回url的html的源码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    # 增加异常处理，主要是会遇到requests.exceptions.ConnectionError异常
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        print("Exception: {}".format(e))
        # 延迟6分钟，保险起见！
        time.sleep(360)
        r = requests.get(url, headers=headers)

    #r.encoding = 'UTF-8'
    #  台湾网页需要制定big5编码！！！
    r.encoding = 'big5'
    page = r.text
    return page
	
def myGetTable(url, site):
    '''
    获取目录
    return:返回一个列表，每个值都是字典
	根据不同的网站需要修改这个函数
    '''
    page = getHtmlCode(url)
    bs_obj = BeautifulSoup(page, 'html.parser')
    # string可以查找tag的文本，还可以配合正则表达式
    for links in bs_obj.find_all('a',string=re.compile("第")):
        ul.append({'name': links.get_text(), 'url': site + links['href']})
    return ul
	
	
	

def my_get_context(num, name, url):
    """
    保存网页内容用于电子书制作
    :param num: 保存的网页文件的序号
    :param name: 页面名称
    :param url: 网址
    :return:
    """

    save_dir = Path('廖雪峰')
    if not save_dir.exists():
        save_dir.mkdir()
    print(name)
    # 由于原来的目录名中有一个是map/reduce的名字，如果不处理，会影响文件名，故去掉‘/’
    name = re.sub(r'/', r'', name)
    print(name)
    filename1 = str(num) + name + '.html'
    filename = save_dir / filename1
    print(filename)
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    for links in bs_obj.find_all('div', {'class': 'x-content'}):
        print(links)
        with open( filename, 'w', encoding='utf8') as f:
            f.write(str(links))
        # 下面是保存网页中的图片
        pic = []
        for piclinks in links.find_all('img'):
            pic.append('https://www.liaoxuefeng.com' + piclinks['src'])
        for pic1 in pic:
            print(pic1)
        filename2 = str(num) + name
        #save_dir_pic = Path('廖雪峰/'+ filename2 )
        #if not save_dir_pic.exists():
        #    save_dir_pic.mkdir()
        i = 0
        for pic1 in pic:
            i = i + 1
            picname1 = filename2 + '_' + str(i) + '.jpg'
            picname = save_dir / picname1
            with urlopen(pic1) as res, picname.open('wb') as f1:
                f1.write(res.read())












if __name__ == '__main__':
    '''
    # auther: xujie
    # date: 2017年8月16日
    # mysql5.7在线文档，爬取了通过sigil制作epub电子书
	# requests 库 结合 beautifulSoup4 库的使用实例
    '''

    url = "https://dev.mysql.com/doc/refman/5.7/en/"
    site = "https://dev.mysql.com"
    html = urlopen(url)
	
	# localPath是自己设定的保存路径
    localPath = 'D:/dump/mysql_doc'
	
	# ul保存目录链接
    page = getHtmlCode(url)
    print(page)
    ul = []
    #ul = myGetTable(url, site)
	
	
    #r = requests.get(url)
    #print(r)
    bs_obj = BeautifulSoup(html, 'html.parser')
    # query_url = url
    # with urlopen(query_url, timeout=timeout) as html:
    #    s = html.read().decode('utf-8')
    #    print(s)
    #print(bs_obj)
    #print(bs_obj.get_text())
    ul = []
    #for links in bs_obj.find_all('a', {'href': re.compile("wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/")}):
    #    #print('https://www.liaoxuefeng.com/' + links['href'])
    #    #print(links.get_text())
    #    ul.append({'name': links.get_text(), 'url':site + links['href']})
    #i = 0
    #for link in ul:
    #    #print(link)
    #    i = i + 1
    #    my_get_context(i, link['name'], link['url'])
    #
    #print(ul[1]['name'])
    #my_get_context(1, ul[1]['name'], ul[1]['url'])
    #for links in bs_obj.find_all('div', {'class': 'x-content'}):
    #    print(links)







