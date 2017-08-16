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







# auther: xujie
# date: 2017年7月19日
# 廖雪峰的python教程，爬取了通过sigil制作epub电子书




if __name__ == '__main__':
    #url = "https://detail.tmall.com/item.htm?id=536013418359&spm=a1z09.2.0.0.6Otvb5&_u=u7kf35v1d5e"
    #url = "http://www.baidu.com"
    url = "https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    site = "https://www.liaoxuefeng.com"
    html = urlopen(url)
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
    for links in bs_obj.find_all('a', {'href': re.compile("wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/")}):
        #print('https://www.liaoxuefeng.com/' + links['href'])
        #print(links.get_text())
        ul.append({'name': links.get_text(), 'url':site + links['href']})
    i = 0
    for link in ul:
        #print(link)
        i = i + 1
        my_get_context(i, link['name'], link['url'])

    #print(ul[1]['name'])
    #my_get_context(1, ul[1]['name'], ul[1]['url'])
    #for links in bs_obj.find_all('div', {'class': 'x-content'}):
    #    print(links)







